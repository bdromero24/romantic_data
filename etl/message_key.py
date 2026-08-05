"""Deterministic message key helpers for ETL records."""

from __future__ import annotations

import hashlib
from datetime import date, datetime
from typing import Any


MESSAGE_KEY_FIELDS = (
    "source",
    "sender",
    "timestamp",
    "message_normalized",
)


def build_message_key(record: dict[str, Any]) -> str:
    """Return a stable SHA-256 key for one normalized message record."""
    raw_value = "|".join(
        (
            _normalize_source(record.get("source")),
            _normalize_sender(record.get("sender")),
            _normalize_timestamp(record.get("timestamp")),
            _normalize_message_normalized(record.get("message_normalized")),
        )
    )
    return hashlib.sha256(raw_value.encode("utf-8")).hexdigest()


def _normalize_source(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip().lower()


def _normalize_sender(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _normalize_message_normalized(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _normalize_timestamp(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, date):
        return value.isoformat()

    text = str(value).strip()
    if not text:
        return ""

    try:
        return datetime.fromisoformat(text).isoformat()
    except ValueError:
        return text
