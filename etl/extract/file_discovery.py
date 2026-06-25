"""Conversation export source detection by file path."""

from __future__ import annotations

from pathlib import Path


WHATSAPP_HINTS: frozenset[str] = frozenset(
    {
        "chat",
        "whatsapp",
        "whats_app",
        "wa",
    }
)
WHATSAPP_TEXT_HINTS: frozenset[str] = frozenset(
    {
        "chat",
        "whatsapp",
        "whats_app",
    }
)
INSTAGRAM_HINTS: frozenset[str] = frozenset(
    {
        "ig",
        "instagram",
        "meta",
    }
)


def detect_source(file_path: str | Path) -> str:
    """Detect a conversation export source from path metadata only."""
    path = Path(file_path)
    suffix = path.suffix.lower()
    path_text = path.as_posix().lower()
    path_parts = {part.lower() for part in path.parts}

    if suffix == ".txt" and _has_whatsapp_hint(path_text, path_parts):
        return "whatsapp"

    if suffix in {".json", ".zip"} and _has_instagram_hint(path_text, path_parts):
        return "instagram"

    raise ValueError(f"Could not detect source for file: {path}")


def _has_whatsapp_hint(path_text: str, path_parts: set[str]) -> bool:
    return any(hint in path_text for hint in WHATSAPP_TEXT_HINTS) or bool(
        path_parts.intersection(WHATSAPP_HINTS)
    )


def _has_instagram_hint(path_text: str, path_parts: set[str]) -> bool:
    return (
        "instagram" in path_text
        or "ig_" in path_text
        or bool(path_parts.intersection(INSTAGRAM_HINTS))
    )
