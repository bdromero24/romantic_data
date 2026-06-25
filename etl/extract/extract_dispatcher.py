"""Extraction dispatcher for supported conversation export files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from etl.extract.file_discovery import detect_source
from etl.extract.instagram_extract import extract_instagram_messages
from etl.extract.whatsapp_extract import extract_whatsapp_messages


def extract_messages(file_path: str | Path) -> list[dict[str, Any]]:
    """Detect source and route extraction to the matching extractor."""
    source = detect_source(file_path)

    if source == "whatsapp":
        return extract_whatsapp_messages(file_path)

    if source == "instagram":
        return extract_instagram_messages(file_path)

    raise ValueError(f"Unsupported source: {source}")
