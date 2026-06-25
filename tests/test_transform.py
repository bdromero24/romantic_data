"""Unit tests for ETL message transformation."""

from datetime import datetime, timedelta, timezone

import pytest

from etl import transform


BOGOTA_TIMEZONE = timezone(timedelta(hours=-5))


def test_normalize_text_removes_accents_punctuation_and_extra_spaces() -> None:
    normalized = transform.normalize_text("  H\u00f3la, MUNDO!!! \u00bfQu\u00e9 tal?  ")

    assert normalized == "hola mundo que tal"


def test_parse_instagram_timestamp_ms_returns_bogota_datetime() -> None:
    timestamp = transform.parse_instagram_timestamp(1700000000000)

    assert timestamp == datetime(
        2023,
        11,
        14,
        17,
        13,
        20,
        tzinfo=BOGOTA_TIMEZONE,
    )


def test_parse_instagram_timestamp_ms_keeps_june_21_in_local_timezone() -> None:
    timestamp = transform.parse_instagram_timestamp(1782103283941)

    assert timestamp == datetime(
        2026,
        6,
        21,
        23,
        41,
        23,
        941000,
        tzinfo=BOGOTA_TIMEZONE,
    )


def test_transform_instagram_message_preserves_original_message() -> None:
    transformed = transform.transform_instagram_message(
        {
            "sender_name": "Alice",
            "content": "H\u00f3la, Bob!",
            "timestamp_ms": "1700000000000",
            "source": "instagram",
        }
    )

    assert transformed == {
        "sender": "Alice",
        "message": "H\u00f3la, Bob!",
        "message_normalized": "hola bob",
        "timestamp": datetime(
            2023,
            11,
            14,
            17,
            13,
            20,
            tzinfo=BOGOTA_TIMEZONE,
        ),
        "source": "instagram",
    }


def test_transform_instagram_message_allows_missing_content() -> None:
    transformed = transform.transform_instagram_message(
        {
            "sender_name": "Alice",
            "timestamp_ms": 1700000000000,
            "source": "instagram",
        }
    )

    assert transformed["message"] == ""
    assert transformed["message_normalized"] == ""


def test_transform_whatsapp_message_returns_standard_fields() -> None:
    timestamp = datetime(2026, 5, 29, 19, 45)
    transformed = transform.transform_whatsapp_message(
        {
            "sender": "Bob",
            "message": "L\u00ednea uno.\nL\u00ednea dos!",
            "timestamp": timestamp,
            "source": "whatsapp",
            "raw_line": "ignored",
        }
    )

    assert transformed == {
        "sender": "Bob",
        "message": "L\u00ednea uno.\nL\u00ednea dos!",
        "message_normalized": "linea uno linea dos",
        "timestamp": timestamp,
        "source": "whatsapp",
    }


def test_transform_messages_routes_supported_sources() -> None:
    timestamp = datetime(2026, 5, 29, 19, 45)

    transformed = transform.transform_messages(
        [
            {
                "sender": "Bob",
                "message": "Hola!",
                "timestamp": timestamp,
                "source": "whatsapp",
            },
            {
                "sender_name": "Alice",
                "content": "Adi\u00f3s.",
                "timestamp_ms": 1700000000000,
                "source": "instagram",
            },
        ]
    )

    assert [message["source"] for message in transformed] == [
        "whatsapp",
        "instagram",
    ]
    assert [message["message_normalized"] for message in transformed] == [
        "hola",
        "adios",
    ]


def test_transform_error_is_logged(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        transform,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(KeyError):
        transform.transform_whatsapp_message(
            {
                "message": "missing sender",
                "timestamp": datetime(2026, 5, 29, 19, 45),
                "source": "whatsapp",
            }
        )

    assert logged_errors == ["KeyError"]
