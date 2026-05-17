"""HTTP client wrapper for the reels downloader microservice."""

import asyncio
import json

import httpx

from domain.exceptions import InvalidSourceError, SourceDownloadError, SourceFetchError
from domain.reel import DownloadedReel
from logger import get_logger

logger = get_logger(__name__)


class HttpReelDownloader:
    """HTTP client that calls the downloader microservice."""

    def __init__(
        self,
        base_url: str = "http://reels-downloader:8001",
        timeout: float = 300.0,
        max_retries: int = 3,
    ):
        """
        Initialize HTTP downloader client.

        Args:
            base_url: Base URL of the downloader service (e.g., http://localhost:8001)
            timeout: Request timeout in seconds (default 5 min for large videos)
            max_retries: Number of retry attempts on transient errors
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    def download_reel(self, reel_url: str) -> DownloadedReel:
        """
        Download a reel by calling the HTTP downloader service.

        Args:
            reel_url: Instagram reel URL

        Returns:
            DownloadedReel with video_path, caption, shortcode, author

        Raises:
            InvalidSourceError: For invalid URLs (HTTP 400)
            SourceDownloadError: For download failures (HTTP 500)
            SourceFetchError: For network/connection errors
        """
        # Use asyncio to run the async HTTP call
        return asyncio.run(self._download_reel_async(reel_url))

    async def _download_reel_async(self, reel_url: str) -> DownloadedReel:
        """Async implementation of download_reel."""
        payload = {"reel_url": reel_url}
        last_error: Exception | None = None
        logger.debug(
            "HTTP download request: reel_url=%s base_url=%s",
            reel_url,
            self.base_url,
        )

        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/download",
                        json=payload,
                    )

                if response.status_code == 400:
                    error_detail = response.json().get("detail", "Invalid reel URL")
                    logger.warning("Invalid source: %s", error_detail)
                    raise InvalidSourceError(error_detail)

                if response.status_code == 500:
                    error_detail = response.json().get("detail", "Download failed")
                    logger.error("Download service error: %s", error_detail)
                    raise SourceDownloadError(error_detail)

                if response.status_code != 200:
                    logger.error(
                        "Unexpected status: status_code=%s body=%s",
                        response.status_code,
                        response.text,
                    )
                    raise SourceDownloadError(
                        f"Downloader service returned {response.status_code}"
                    )

                data = response.json()
                result = DownloadedReel(**data)
                logger.info(
                    "HTTP downloader success: shortcode=%s",
                    result.shortcode,
                )
                return result

            except (InvalidSourceError, SourceDownloadError):
                # Don't retry on client errors (400, 500)
                raise
            except httpx.TimeoutException as e:
                last_error = e
                logger.warning(
                    "Timeout on attempt %s/%s: %s",
                    attempt,
                    self.max_retries,
                    e,
                )
                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** (attempt - 1))  # Exponential backoff
                continue
            except httpx.ConnectError as e:
                last_error = e
                logger.warning(
                    "Connection error on attempt %s/%s: %s",
                    attempt,
                    self.max_retries,
                    e,
                )
                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** (attempt - 1))  # Exponential backoff
                continue
            except httpx.RequestError as e:
                last_error = e
                logger.warning(
                    "Request error on attempt %s/%s: %s",
                    attempt,
                    self.max_retries,
                    e,
                )
                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** (attempt - 1))  # Exponential backoff
                continue
            except json.JSONDecodeError as e:
                last_error = e
                logger.error("Invalid JSON response from downloader: %s", e)
                raise SourceDownloadError("Downloader returned invalid response") from e
            except Exception as e:
                last_error = e
                logger.exception("Unexpected error during download: %s", e)
                raise SourceFetchError(f"Unexpected error: {e}") from e

        # All retries exhausted
        logger.error(
            "Failed to download after %s attempts: %s",
            self.max_retries,
            last_error,
        )
        raise SourceFetchError(
            f"Download failed after {self.max_retries} retries"
        ) from last_error
