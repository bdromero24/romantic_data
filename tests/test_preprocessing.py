"""Unit tests for analysis preprocessing helpers."""

from datetime import datetime, timezone

import pytest

from analysis import preprocessing


def test_preprocess_text_supports_spanish_accents_punctuation_and_emojis() -> None:
    result = preprocessing.preprocess_text(
        "  H\u00f3la, coraz\u00f3n!!! \u00bfC\u00f3mo est\u00e1s? \ud83d\ude0a  "
    )

    assert result == "hola corazon como estas \ud83d\ude0a"


def test_tokenize_text_returns_empty_list_for_empty_message() -> None:
    assert preprocessing.tokenize_text("   !!! \u00bf? ") == []


def test_preprocess_message_record_preserves_original_fields() -> None:
    timestamp = datetime(2026, 6, 8, 14, 30, tzinfo=timezone.utc)
    record = {
        "sender": "Alice",
        "message": "H\u00f3la!!!",
        "message_normalized": "hola",
        "timestamp": timestamp,
        "source": "instagram",
    }

    result = preprocessing.preprocess_message_record(record)

    assert result == {
        "sender": "Alice",
        "message": "H\u00f3la!!!",
        "message_normalized": "hola",
        "timestamp": timestamp,
        "source": "instagram",
        "message_preprocessed": "hola",
        "message_tokens": ["hola"],
    }
    assert record == {
        "sender": "Alice",
        "message": "H\u00f3la!!!",
        "message_normalized": "hola",
        "timestamp": timestamp,
        "source": "instagram",
    }


def test_preprocess_message_record_falls_back_to_original_message() -> None:
    result = preprocessing.preprocess_message_record(
        {
            "sender": "Bob",
            "message": "Adi\u00f3s, mundo!",
            "source": "whatsapp",
        }
    )

    assert result["message_preprocessed"] == "adios mundo"
    assert result["message_tokens"] == ["adios", "mundo"]


def test_preprocess_message_records_returns_preprocessed_copies() -> None:
    records = [
        {"message": "Uno.", "source": "whatsapp"},
        {"message": "", "source": "instagram"},
    ]

    result = preprocessing.preprocess_message_records(records)

    assert [record["message_preprocessed"] for record in result] == ["uno", ""]
    assert [record["message_tokens"] for record in result] == [["uno"], []]
    assert "message_preprocessed" not in records[0]


def test_preprocessing_error_is_logged(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        preprocessing,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(TypeError, match="message text must be a string"):
        preprocessing.preprocess_text(None)

    assert logged_errors == ["TypeError"]


def test_preprocess_message_record_logs_missing_message(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        preprocessing,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(KeyError, match="Missing required field"):
        preprocessing.preprocess_message_record({"sender": "Alice"})

    assert logged_errors == ["KeyError"]
