"""
One-shot migration script: convert legacy French enum values to English.

Extracted from commit 8897e57948ed1f777d280b5be6593e22bcb90e24
(feat: add CuisineType enumeration with various global cuisines and update related schemas)

Usage:
    uv run python scripts/migrate_enum_values.py
    uv run python scripts/migrate_enum_values.py --dry-run

Environment variables:
    MONGODB_URI      MongoDB connection string (default: mongodb://localhost:27017)
    MONGODB_DATABASE       Database name (default: cookachu)
    COLLECTION_NAME  Collection name (default: recipes)
"""

import argparse
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# ---------------------------------------------------------------------------
# Mappings extracted directly from the diff of api/domain/recipe.py
# Keys   = old French values (stored in MongoDB before the migration commit)
# Values = new English values (current enum values)
# ---------------------------------------------------------------------------

CUISINE_TYPE_MAP: dict[str, str] = {
    "française": "french",
    "italienne": "italian",
    "asiatique": "other",  # no direct equivalent — mapped to "other"
    "moyen-orientale": "arabian",  # closest match
    "américaine": "american",
    "méditerranéenne": "mediterranean",
    "mexicaine": "mexican",
    "indienne": "indian",
    "autre": "other",
}

DISH_TYPE_MAP: dict[str, str] = {
    "entrée": "starter",
    "plat principal": "main_course",
    "dessert": "dessert",  # unchanged value
    "snack": "snack",  # unchanged value
    "boisson": "drink",
    "sauce": "sauce",  # unchanged value
}

DIFFICULTY_MAP: dict[str, str] = {
    "facile": "easy",
    "moyen": "medium",
    "difficile": "hard",
}

APPLIANCE_MAP: dict[str, str] = {
    "four": "oven",
    "airfryer": "air_fryer",
    "micro-ondes": "microwave",
    "mixeur": "blender",
    "robot culinaire": "food_processor",
    "batteur électrique": "hand_mixer",
    "cuiseur vapeur": "steamer",
    "plaque de cuisson": "stovetop",
    "autre": "other",
}

# All valid current English values — used to detect already-migrated documents
VALID_CUISINE_TYPES = set(CUISINE_TYPE_MAP.values())
VALID_DISH_TYPES = set(DISH_TYPE_MAP.values())
VALID_DIFFICULTIES = set(DIFFICULTY_MAP.values())
VALID_APPLIANCES = set(APPLIANCE_MAP.values())


def build_patch(doc: dict) -> dict:
    """
    Inspect a raw MongoDB document and return a $set patch.
    Returns an empty dict if the document needs no changes.
    """
    recipe = doc.get("recipe", {})
    set_fields: dict[str, object] = {}

    # cuisine_type
    ct = recipe.get("cuisine_type")
    if ct and ct not in VALID_CUISINE_TYPES:
        mapped = CUISINE_TYPE_MAP.get(ct)
        if mapped:
            set_fields["recipe.cuisine_type"] = mapped
        else:
            print(
                f"  WARNING: unknown cuisine_type '{ct}' in doc {doc['_id']} — skipping field"
            )

    # dish_type
    dt = recipe.get("dish_type")
    if dt and dt not in VALID_DISH_TYPES:
        mapped = DISH_TYPE_MAP.get(dt)
        if mapped:
            set_fields["recipe.dish_type"] = mapped
        else:
            print(
                f"  WARNING: unknown dish_type '{dt}' in doc {doc['_id']} — skipping field"
            )

    # difficulty
    diff = recipe.get("difficulty")
    if diff and diff not in VALID_DIFFICULTIES:
        mapped = DIFFICULTY_MAP.get(diff)
        if mapped:
            set_fields["recipe.difficulty"] = mapped
        else:
            print(
                f"  WARNING: unknown difficulty '{diff}' in doc {doc['_id']} — skipping field"
            )

    # appliances (list field)
    appliances = recipe.get("appliances") or []
    if appliances:
        migrated = []
        needs_update = False
        for appliance in appliances:
            if appliance not in VALID_APPLIANCES:
                mapped = APPLIANCE_MAP.get(appliance)
                if mapped:
                    migrated.append(mapped)
                    needs_update = True
                else:
                    print(
                        f"  WARNING: unknown appliance '{appliance}' in doc {doc['_id']} — keeping as-is"
                    )
                    migrated.append(appliance)
            else:
                migrated.append(appliance)
        if needs_update:
            set_fields["recipe.appliances"] = migrated

    if not set_fields:
        return {}

    return {"$set": set_fields}


def run(dry_run: bool) -> None:
    mongodb_url = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DATABASE", "cookachu")
    collection_name = os.getenv("COLLECTION_NAME", "recipes")

    client: MongoClient = MongoClient(mongodb_url)
    collection = client[db_name][collection_name]

    print(f"Connected to {mongodb_url} — db={db_name}, collection={collection_name}")
    if dry_run:
        print(">>> DRY RUN — no writes will be performed\n")

    scanned = 0
    updated = 0
    skipped = 0

    for doc in collection.find({}):
        scanned += 1
        patch = build_patch(doc)

        if not patch:
            skipped += 1
            continue

        print(f"  [{doc['_id']}] {patch['$set']}")

        if not dry_run:
            collection.update_one({"_id": doc["_id"]}, patch)

        updated += 1

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Done.")
    print(f"  Scanned : {scanned}")
    print(f"  Updated : {updated}")
    print(f"  Skipped : {skipped} (already up-to-date)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Migrate legacy French enum values to English in MongoDB."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be changed without writing to MongoDB.",
    )
    args = parser.parse_args()
    run(dry_run=args.dry_run)
