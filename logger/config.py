"""Central logging configuration."""

from pathlib import Path


LOG_DIRECTORY: Path = Path("logs")
LOG_FILE_PATH: Path = LOG_DIRECTORY / "errors.txt"
LOG_FORMAT: str = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
DEFAULT_SEVERITY: str = "CRITICAL"
