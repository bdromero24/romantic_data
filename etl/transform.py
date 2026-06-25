"""Deterministic ETL transformation helpers."""

from __future__ import annotations

import unicodedata
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

from logger.logger import log_critical_error


STANDARD_FIELDS = (
    "sender",
    "message",
    "message_normalized",
    "timestamp",
    "source",
)

INVALID_TEXT_VALUES = {
    "",
    "na",
    "n/a",
    "nan",
    "none",
    "null",
    "<media omitted>",
    "media omitted",
    "omitted",
}

MOJIBAKE_MARKERS = (
    "Ã",
    "Â",
    "â",
    "ð",
    "�",
)

BOGOTA_TIMEZONE = timezone(timedelta(hours=-5))


def clean_text(message: str) -> str:
    """Return display-safe text with repaired encoding and normalized spacing."""
    if not isinstance(message, str):
        raise TypeError("Message text must be a string.")

    repaired_text = _fix_mojibake(message)
    normalized_text = unicodedata.normalize("NFC", repaired_text)
    visible_text = _remove_invisible_characters(normalized_text)

    return _normalize_display_spacing(visible_text)


def normalize_text(message: str) -> str:
    """Return lowercase searchable text without accents, punctuation, or extra spaces."""
    cleaned_message = clean_text(message)
    without_accents = _remove_accents(cleaned_message)
    without_punctuation = _remove_punctuation_and_symbols(without_accents)

    return " ".join(without_punctuation.lower().split())


def parse_instagram_timestamp(timestamp_ms: Any) -> datetime:
    """Parse an Instagram millisecond timestamp into a -0500 datetime."""
    try:
        timestamp_number = _coerce_millisecond_timestamp(timestamp_ms)
        return datetime.fromtimestamp(
            timestamp_number / 1000,
            tz=timezone.utc,
        ).astimezone(BOGOTA_TIMEZONE)
    except (TypeError, ValueError, OSError, OverflowError) as error:
        _log_transform_error(
            error_type=type(error).__name__,
            error=error,
            function_name="parse_instagram_timestamp",
        )
        raise


def transform_instagram_message(record: dict[str, Any]) -> dict[str, Any]:
    """Normalize one extracted Instagram message dictionary."""
    try:
        sender = _require_text_field(record, "sender_name")
        message = _get_instagram_message_text(record)
        timestamp = parse_instagram_timestamp(record.get("timestamp_ms"))

        return _build_standard_message(
            sender=sender,
            message=message,
            timestamp=timestamp,
            source="instagram",
            allow_empty_message=True,
        )
    except (KeyError, TypeError, ValueError, OSError, OverflowError) as error:
        _log_transform_error(
            error_type=type(error).__name__,
            error=error,
            function_name="transform_instagram_message",
        )
        raise


def transform_whatsapp_message(record: dict[str, Any]) -> dict[str, Any]:
    """Normalize one extracted WhatsApp message dictionary."""
    try:
        sender = _require_text_field(record, "sender")
        message = _require_text_field(record, "message")
        timestamp = _require_field(record, "timestamp")

        return _build_standard_message(
            sender=sender,
            message=message,
            timestamp=timestamp,
            source="whatsapp",
        )
    except (KeyError, TypeError, ValueError) as error:
        _log_transform_error(
            error_type=type(error).__name__,
            error=error,
            function_name="transform_whatsapp_message",
        )
        raise


def transform_message(record: dict[str, Any]) -> dict[str, Any]:
    """Normalize one extracted message dictionary from a supported source."""
    source = record.get("source")

    if source == "instagram":
        return transform_instagram_message(record)

    if source == "whatsapp":
        return transform_whatsapp_message(record)

    error = ValueError(f"Unsupported message source: {source}")
    _log_transform_error(
        error_type=type(error).__name__,
        error=error,
        function_name="transform_message",
    )
    raise error


def transform_messages(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize extracted message dictionaries without database writes.

    Empty textual records, NA-like values, and non-message Instagram records are skipped.
    Invalid structural records still raise errors through transform_message().
    """
    transformed_records: list[dict[str, Any]] = []

    for record in records:
        if _is_ignorable_message_record(record):
            continue

        transformed_records.append(transform_message(record))

    return transformed_records


def _fix_mojibake(message: str) -> str:
    """Repair common UTF-8 text decoded incorrectly as Latin-1.

    Examples:
    - extraÃ±o -> extraño
    - corazÃ³n -> corazón
    - â -> ’
    - ð -> 🍓
    """
    candidate = message

    for _ in range(2):
        if not _looks_like_mojibake(candidate):
            break

        try:
            repaired = candidate.encode("latin1").decode("utf-8")
        except UnicodeError:
            break

        if _text_quality_score(repaired) <= _text_quality_score(candidate):
            break

        candidate = repaired

    return candidate.replace("\ufffd", "")


def _looks_like_mojibake(message: str) -> bool:
    return any(marker in message for marker in MOJIBAKE_MARKERS)


def _text_quality_score(message: str) -> int:
    bad_marker_count = sum(message.count(marker) for marker in MOJIBAKE_MARKERS)
    replacement_count = message.count("\ufffd")

    spanish_character_count = sum(
        1
        for character in message
        if character in "áéíóúÁÉÍÓÚñÑüÜ¿¡"
    )

    control_character_count = sum(
        1
        for character in message
        if unicodedata.category(character) in {"Cc", "Cf"}
        and character not in {"\n", "\r", "\t"}
    )

    return (
        spanish_character_count * 3
        - bad_marker_count * 10
        - replacement_count * 20
        - control_character_count * 5
    )


def _remove_invisible_characters(message: str) -> str:
    cleaned_characters: list[str] = []

    for character in message:
        category = unicodedata.category(character)

        if category in {"Cc", "Cf"} and character not in {"\n", "\r", "\t"}:
            continue

        if character in {"\u00a0", "\u2007", "\u202f"}:
            cleaned_characters.append(" ")
            continue

        cleaned_characters.append(character)

    return "".join(cleaned_characters)


def _normalize_display_spacing(message: str) -> str:
    lines = [" ".join(line.split()) for line in message.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def _remove_accents(message: str) -> str:
    normalized_text = unicodedata.normalize("NFKD", message)
    return "".join(
        character
        for character in normalized_text
        if not unicodedata.combining(character)
    )


def _remove_punctuation_and_symbols(message: str) -> str:
    cleaned_characters: list[str] = []

    for character in message:
        category = unicodedata.category(character)

        if character.isspace():
            cleaned_characters.append(" ")
            continue

        if category.startswith("L") or category.startswith("N"):
            cleaned_characters.append(character)
            continue

        cleaned_characters.append(" ")

    return "".join(cleaned_characters)


def _coerce_millisecond_timestamp(timestamp_ms: Any) -> int:
    if isinstance(timestamp_ms, bool):
        raise TypeError("Instagram timestamp_ms must be a millisecond number.")

    if isinstance(timestamp_ms, int):
        return timestamp_ms

    if isinstance(timestamp_ms, float) and timestamp_ms.is_integer():
        return int(timestamp_ms)

    if isinstance(timestamp_ms, str) and timestamp_ms.strip().isdigit():
        return int(timestamp_ms.strip())

    raise TypeError("Instagram timestamp_ms must be a millisecond number.")


def _get_instagram_message_text(record: dict[str, Any]) -> str:
    if "content" in record:
        return _require_text_field(record, "content")

    if "message" in record:
        return _require_text_field(record, "message")

    return ""


def _require_field(record: dict[str, Any], field_name: str) -> Any:
    if field_name not in record:
        raise KeyError(f"Missing required field: {field_name}")

    return record[field_name]


def _require_text_field(record: dict[str, Any], field_name: str) -> str:
    value = _require_field(record, field_name)

    if not isinstance(value, str):
        raise TypeError(f"Field must be a string: {field_name}")

    cleaned_value = clean_text(value)

    if _is_invalid_text_value(cleaned_value):
        raise ValueError(f"Field contains empty or NA-like text: {field_name}")

    return cleaned_value


def _build_standard_message(
    sender: str,
    message: str,
    timestamp: Any,
    source: str,
    allow_empty_message: bool = False,
) -> dict[str, Any]:
    cleaned_sender = clean_text(sender)
    cleaned_message = clean_text(message)

    if _is_invalid_text_value(cleaned_sender):
        raise ValueError("Sender contains empty or NA-like text.")

    if not allow_empty_message and _is_invalid_text_value(cleaned_message):
        raise ValueError("Message contains empty or NA-like text.")

    return {
        "sender": cleaned_sender,
        "message": cleaned_message,
        "message_normalized": normalize_text(cleaned_message),
        "timestamp": timestamp,
        "source": source,
    }


def _is_ignorable_message_record(record: dict[str, Any]) -> bool:
    source = record.get("source")

    if source == "instagram":
        value = record.get("content", record.get("message"))
        return _is_ignorable_raw_text(value)

    if source == "whatsapp":
        value = record.get("message")
        return _is_ignorable_raw_text(value)

    return False


def _is_ignorable_raw_text(value: Any) -> bool:
    if value is None:
        return True

    if not isinstance(value, str):
        return False

    return _is_invalid_text_value(value)


def _is_invalid_text_value(value: str) -> bool:
    cleaned_value = clean_text(value)
    normalized_value = normalize_text_for_invalid_check(cleaned_value)

    return normalized_value in INVALID_TEXT_VALUES


def normalize_text_for_invalid_check(message: str) -> str:
    without_accents = _remove_accents(clean_text(message))
    without_punctuation = _remove_punctuation_and_symbols(without_accents)

    return " ".join(without_punctuation.lower().split())


def _log_transform_error(
    error_type: str,
    error: Exception,
    function_name: str,
) -> None:
    log_critical_error(
        error_type=error_type,
        error_message=str(error),
        module_name=__name__,
        function_name=function_name,
    )
