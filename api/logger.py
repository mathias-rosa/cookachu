import logging
import os
import sys

_CONFIGURED = False


def _resolve_log_level() -> int:
    raw_level = (
        os.getenv("COOKACHU_LOG_LEVEL") or os.getenv("LOG_LEVEL") or "INFO"
    ).strip()
    return logging._nameToLevel.get(raw_level.upper(), logging.INFO)


def setup_logging() -> None:
    """Configure root logging once for the application."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    level = _resolve_log_level()
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(handler)

    _CONFIGURED = True


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger after ensuring logging is configured."""
    setup_logging()
    return logging.getLogger(name or "cookachu")
