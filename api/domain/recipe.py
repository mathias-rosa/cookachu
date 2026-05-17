from enum import StrEnum

from pydantic import BaseModel, Field

from .cuisine_type import CuisineType


class DishType(StrEnum):
    STARTER = "starter"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    SNACK = "snack"
    DRINK = "drink"
    SAUCE = "sauce"
    SIDE_DISH = "side_dish"
    SOUP = "soup"
    SALAD = "salad"
    BREAKFAST = "breakfast"
    BRUNCH = "brunch"
    APPETIZER = "appetizer"


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class Appliance(StrEnum):
    OVEN = "oven"
    AIR_FRYER = "air_fryer"
    MICROWAVE = "microwave"
    BLENDER = "blender"
    FOOD_PROCESSOR = "food_processor"
    STAND_MIXER = "stand_mixer"
    HAND_MIXER = "hand_mixer"
    STEAMER = "steamer"
    STOVETOP = "stovetop"
    INDUCTION_COOKTOP = "induction_cooktop"
    PRESSURE_COOKER = "pressure_cooker"
    SLOW_COOKER = "slow_cooker"
    RICE_COOKER = "rice_cooker"
    GRILL = "grill"
    BARBECUE = "barbecue"
    TOASTER = "toaster"
    TOASTER_OVEN = "toaster_oven"
    COFFEE_MACHINE = "coffee_machine"
    KETTLE = "kettle"
    WAFFLE_MAKER = "waffle_maker"
    PANINI_PRESS = "panini_press"
    DEEP_FRYER = "deep_fryer"
    OTHER = "other"


class Ingredient(BaseModel):
    name: str = Field(
        description="Nom de l'ingrédient uniquement. Ex: 'poulet', 'ail'."
    )
    quantity: float | None = Field(
        None,
        ge=0.0,
        description="Valeur numérique uniquement. Ex: 2.0, 0.5, 680.0. None si non mesurable.",
    )
    unit: str | None = Field(
        None,
        description="Unité de mesure. Ex: 'g', 'ml', 'c.à.s.', 'c.à.c.'. None si compté en unités.",
    )
    count: int | None = Field(
        None,
        ge=1,
        description="Nombre d'unités entières. Ex: 3 œufs, 2 citrons. None si quantity/unit renseignés.",
    )
    note: str | None = Field(
        None,
        description="Préparation ou précision. Ex: 'finement haché', 'à température ambiante'.",
    )
    group: str | None = Field(
        None,
        description="Groupe d'appartenance si la recette a des composants distincts. Ex: 'Marinade', 'Sauce', 'Garniture'. None si recette plate.",
    )


class InstructionStep(BaseModel):
    title: str | None = Field(
        None,
        description="Titre court de l'étape. Ex: 'Marinade', 'Cuisson du riz', 'Dressage'. None si l'étape ne correspond pas à une phase distincte.",
    )
    description: str = Field(description="Instructions détaillées de l'étape.")


class Recipe(BaseModel):
    is_recipe: bool = Field(
        default=True,
        description="Indique si l'entrée est une recette valide ou non.",
    )

    title: str
    description: str = Field(
        description="Une phrase qui donne envie et résume le plat."
    )
    cuisine_type: CuisineType
    dish_type: DishType
    difficulty: Difficulty

    prep_time_minutes: int | None = Field(
        None,
        ge=0,
        le=1440,
        description="Temps de préparation actif en minutes (0-1440).",
    )
    cook_time_minutes: int | None = Field(
        None, ge=0, le=1440, description="Temps de cuisson en minutes (0-1440)."
    )
    rest_time_minutes: int | None = Field(
        None,
        ge=0,
        le=1440,
        description="Marinade, repos, réfrigération (0-1440). None si absent.",
    )

    servings: int | None = Field(
        None,
        ge=1,
        le=100,
        description="Nombre de personnes (1-100). None si non déductible.",
    )

    appliances: list[Appliance] = Field(
        default_factory=list,
        description="Appareils électroménagers requis. Vide si cuisson standard.",
    )
    utensils: list[str] = Field(
        default_factory=list,
        description="Ustensiles notables. Ex: 'wok', 'mandoline'. Exclure couteau, planche, bol.",
    )

    ingredients: list[Ingredient]
    instructions: list[InstructionStep]

    tags: list[str] = Field(
        default_factory=list,
        description="Mots-clés courts. Ex: 'one-pan', 'meal-prep', 'sans gluten'.",
    )
    tips: list[str] = Field(
        default_factory=list,
        description="Astuces du créateur visibles dans la vidéo ou la caption.",
    )
