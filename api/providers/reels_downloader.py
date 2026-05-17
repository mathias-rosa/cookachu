import os
from pathlib import Path

from instaloader import Instaloader, Post

from domain.exceptions import InvalidSourceError, SourceDownloadError, SourceFetchError
from domain.reel import DownloadedReel
from logger import get_logger

logger = get_logger(__name__)


class ReelDownloader:
    def __init__(self, target_dir: str = "downloaded_reels"):
        self.target_dir = target_dir

    def download_reel(self, reel_url: str) -> DownloadedReel:
        # Ensure download directory exists for temp files and media output.
        target_dir_path = Path(self.target_dir).resolve()
        target_dir_path.mkdir(parents=True, exist_ok=True)
        shortcode = self._extract_shortcode(reel_url)
        if not shortcode:
            logger.warning("Invalid source URL provided for reel download.")
            raise InvalidSourceError(
                "The provided URL does not appear to be a valid Instagram Reel URL."
            )

        logger.debug(
            "Download context: cwd=%s target_dir=%s exists=%s writable=%s",
            Path.cwd(),
            target_dir_path,
            target_dir_path.exists(),
            os.access(target_dir_path, os.W_OK),
        )

        loader = Instaloader(filename_pattern="{shortcode}")

        try:
            reel = self._fetch_post(loader, shortcode)
        except Exception as e:
            logger.error("Error fetching reel: %s", e)
            raise SourceFetchError(f"Error fetching reel: {e}") from e

        if not reel.is_video:
            logger.warning("The provided URL does not point to a video reel.")
            raise InvalidSourceError("The provided URL does not point to a video reel.")

        logger.info("Downloading reel media: shortcode=%s", shortcode)
        try:
            loader.download_post(reel, target=self.target_dir)
        except Exception as e:
            logger.error(
                "Error downloading reel media: %s (shortcode=%s target_dir=%s)",
                e,
                shortcode,
                target_dir_path,
            )
            raise SourceDownloadError(f"Error downloading reel media: {e}") from e
        logger.info("Reel downloaded successfully: shortcode=%s", shortcode)

        video_path = self._expected_video_path(reel.shortcode)
        if not Path(video_path).exists():
            logger.error(
                "Downloaded video not found at expected location: video_path=%s target_dir=%s",
                video_path,
                target_dir_path,
            )
            raise SourceDownloadError("Could not find downloaded video.")

        caption = reel.caption or ""
        return DownloadedReel(
            video_path=video_path,
            caption=caption,
            shortcode=shortcode,
            author=reel.owner_username,
        )

    @staticmethod
    def _extract_shortcode(reel_url: str) -> str | None:
        url_array = reel_url.split("/")
        is_reel = len(url_array) >= 3 and url_array[-3] == "reel"
        if not is_reel:
            return None

        shortcode = url_array[-2]
        if not shortcode:
            return None
        return shortcode

    def _fetch_post(self, loader: Instaloader, shortcode: str) -> Post:
        reel: Post = Post.from_shortcode(loader.context, shortcode)
        assert isinstance(reel, Post), "The fetched object is not a Post instance."
        return reel

    def _expected_video_path(self, shortcode: str) -> str:
        return str(Path(self.target_dir) / f"{shortcode}.mp4")
