"""Helpers for configured message references in romantic content."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MessageReference:
    """One manually configured message reference."""

    config_path: str
    message_id: int | None = None
    message_key: str | None = None


def extract_configured_message_references(
    content: dict[str, Any],
    root_path: str = "ROMANTIC_CONTENT",
) -> list[MessageReference]:
    """Return message references from manual content configuration."""
    references: list[MessageReference] = []
    _collect_references(content, root_path, references)
    return references


def valid_message_ids_from_references(
    references: list[MessageReference],
) -> list[int]:
    """Return unique valid message IDs preserving configured order."""
    message_ids: list[int] = []
    seen_ids: set[int] = set()

    for reference in references:
        message_id = reference.message_id
        if message_id is None or message_id in seen_ids:
            continue

        seen_ids.add(message_id)
        message_ids.append(message_id)

    return message_ids


def valid_message_keys_from_references(
    references: list[MessageReference],
) -> list[str]:
    """Return unique valid message keys preserving configured order."""
    message_keys: list[str] = []
    seen_keys: set[str] = set()

    for reference in references:
        message_key = reference.message_key
        if message_key is None or message_key in seen_keys:
            continue

        seen_keys.add(message_key)
        message_keys.append(message_key)

    return message_keys


def _collect_references(
    value: Any,
    path: str,
    references: list[MessageReference],
) -> None:
    if isinstance(value, dict):
        _collect_dict_references(value, path, references)
        return

    if isinstance(value, list):
        for index, item in enumerate(value):
            _collect_references(item, f"{path}[{index}]", references)


def _collect_dict_references(
    value: dict[str, Any],
    path: str,
    references: list[MessageReference],
) -> None:
    if "message_id" in value or "message_key" in value:
        message_id = _normalize_message_id(value.get("message_id"))
        message_key = _normalize_message_key(value.get("message_key"))
        if message_id is not None or message_key is not None:
            suffix = "message_id" if message_id is not None else "message_key"
            references.append(
                MessageReference(
                    config_path=f"{path}.{suffix}",
                    message_id=message_id,
                    message_key=message_key,
                )
            )

    if "message_ids" in value or "message_keys" in value:
        raw_ids = value.get("message_ids")
        raw_keys = value.get("message_keys", [])
        ids = raw_ids if isinstance(raw_ids, list) else []
        keys = raw_keys if isinstance(raw_keys, list) else []
        for index in range(max(len(ids), len(keys))):
            raw_id = ids[index] if index < len(ids) else None
            message_id = _normalize_message_id(raw_id)
            message_key = _matching_message_key(keys, index)
            if message_id is not None or message_key is not None:
                suffix = "message_ids" if message_id is not None else "message_keys"
                references.append(
                    MessageReference(
                        config_path=f"{path}.{suffix}[{index}]",
                        message_id=message_id,
                        message_key=message_key,
                    )
                )

    for key, child in value.items():
        if key in {"message_id", "message_key", "message_ids", "message_keys"}:
            continue
        _collect_references(child, f"{path}.{key}", references)


def _matching_message_key(raw_keys: Any, index: int) -> str | None:
    if not isinstance(raw_keys, list) or index >= len(raw_keys):
        return None

    return _normalize_message_key(raw_keys[index])


def _normalize_message_id(value: Any) -> int | None:
    if not isinstance(value, int) or isinstance(value, bool):
        return None

    return value


def _normalize_message_key(value: Any) -> str | None:
    if value is None or isinstance(value, bool):
        return None

    text = str(value).strip()
    if not text:
        return None

    return text
