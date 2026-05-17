from pathlib import Path

from core.ports import RecipeExtractor, RecipeRepository, ReelDownloader
from domain.exceptions import NotARecipeError
from domain.recipe_record import RecipeRecord
from domain.recipe_source import ReelRecipeSource
from logger import get_logger

logger = get_logger(__name__)


class ProcessReelService:
    def __init__(
        self,
        downloader: ReelDownloader,
        extractor: RecipeExtractor,
        repository: RecipeRepository,
    ):
        self.downloader = downloader
        self.extractor = extractor
        self.repository = repository

    def execute(self, reel_url: str) -> RecipeRecord:
        logger.info("Processing reel: reel_url=%s", reel_url)
        downloaded = self.downloader.download_reel(reel_url)

        try:
            source = ReelRecipeSource(
                reel_url=reel_url,
                shortcode=downloaded.shortcode,
                caption=downloaded.caption,
                author=downloaded.author,
            )

            existing_record = self.repository.find_by_id(source.canonical_id())
            if existing_record:
                logger.info(
                    "Source already processed: record_id=%s",
                    existing_record.id,
                )
                return existing_record

            recipe = self.extractor.extract_recipe(
                downloaded.video_path, downloaded.caption
            )

            if not recipe.is_recipe:
                logger.warning("Extracted content is not a recipe.")
                raise NotARecipeError("The extracted content is not a valid recipe.")

            recipe_result = RecipeRecord(
                recipe=recipe,
                source=source,
            )
            saved = self.repository.save(recipe_result)
            logger.info("Recipe saved: record_id=%s", saved.id)
            return saved
        finally:
            target_dir = str(Path(downloaded.video_path).parent)
            self._cleanup_video(downloaded.shortcode, target_dir)

    @staticmethod
    def _cleanup_video(shortcode: str, target_dir: str) -> None:
        """Clean up all downloaded files associated with the reel.

        Removes mp4 video, json metadata, and temp files for the given shortcode.
        """
        import re

        # Validate shortcode format (Instagram shortcodes are alphanumeric + -_)
        if not re.match(r"^[A-Za-z0-9_-]+$", shortcode):
            logger.warning(
                "Invalid shortcode format, skipping cleanup: shortcode=%s", shortcode
            )
            return

        target_dir_path = Path(target_dir)

        try:
            # Remove all files matching the shortcode pattern
            for file in target_dir_path.glob(f"{shortcode}*"):
                try:
                    file.unlink()
                    logger.debug("Cleaned up file: file=%s", file.name)
                except Exception as e:
                    logger.warning(
                        "Failed to clean up file: file=%s error=%s", file.name, e
                    )
        except Exception as exc:
            logger.warning(
                "Failed to clean up downloaded files: shortcode=%s target_dir=%s error=%s",
                shortcode,
                target_dir,
                exc,
            )
