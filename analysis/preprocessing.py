"""Deterministic preprocessing helpers for analysis inputs."""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable as IterableCollection
from typing import Any, Iterable

from logger.logger import log_critical_error


MESSAGE_FIELD = "message"
NORMALIZED_MESSAGE_FIELD = "message_normalized"
PREPROCESSED_MESSAGE_FIELD = "message_preprocessed"
TOKEN_FIELD = "message_tokens"


def preprocess_text(message: str) -> str:
    """Return analysis-ready text while preserving emojis as symbols."""
    try:
        if not isinstance(message, str):
            raise TypeError("Preprocessing message text must be a string.")

        text_without_accents = _remove_accents(message)
        text_without_punctuation = _remove_punctuation(text_without_accents)
        return " ".join(text_without_punctuation.lower().split())
    except TypeError as error:
        _log_preprocessing_error(
            error_type=type(error).__name__,
            error=error,
            function_name="preprocess_text",
        )
        raise


def tokenize_text(message: str) -> list[str]:
    """Return whitespace tokens from preprocessed message text."""
    preprocessed_message = preprocess_text(message)
    if not preprocessed_message:
        return []

    return preprocessed_message.split()


def preprocess_message_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of a message record with analysis preprocessing fields."""
    try:
        if not isinstance(record, dict):
            raise TypeError("Preprocessing message record must be a dictionary.")

        source_text = _get_source_text(record)
        preprocessed_message = preprocess_text(source_text)
        preprocessed_record = dict(record)
        preprocessed_record[PREPROCESSED_MESSAGE_FIELD] = preprocessed_message
        preprocessed_record[TOKEN_FIELD] = _tokens_from_preprocessed_text(
            preprocessed_message,
        )
        return preprocessed_record
    except (KeyError, TypeError) as error:
        _log_preprocessing_error(
            error_type=type(error).__name__,
            error=error,
            function_name="preprocess_message_record",
        )
        raise


def preprocess_message_records(
    records: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return preprocessed copies of message records without side effects."""
    if isinstance(records, (str, bytes)) or not isinstance(records, IterableCollection):
        error = TypeError("Preprocessing message records must be iterable.")
        _log_preprocessing_error(
            error_type=type(error).__name__,
            error=error,
            function_name="preprocess_message_records",
        )
        raise error

    return [preprocess_message_record(record) for record in records]


def _get_source_text(record: dict[str, Any]) -> str:
    if NORMALIZED_MESSAGE_FIELD in record:
        return _require_text_field(record, NORMALIZED_MESSAGE_FIELD)

    return _require_text_field(record, MESSAGE_FIELD)


def _require_text_field(record: dict[str, Any], field_name: str) -> str:
    if field_name not in record:
        raise KeyError(f"Missing required field: {field_name}")

    value = record[field_name]
    if not isinstance(value, str):
        raise TypeError(f"Field must be a string: {field_name}")

    return value


def _remove_accents(message: str) -> str:
    normalized_text = unicodedata.normalize("NFKD", message)
    return "".join(
        character
        for character in normalized_text
        if not unicodedata.combining(character)
    )


def _remove_punctuation(message: str) -> str:
    return "".join(
        character
        for character in message
        if not unicodedata.category(character).startswith("P")
    )


def _tokens_from_preprocessed_text(message: str) -> list[str]:
    if not message:
        return []

    return message.split()


def _log_preprocessing_error(
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
