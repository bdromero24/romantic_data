"""Unit tests for deterministic message key generation."""

from datetime import datetime, timezone

from etl.message_key import build_message_key


def _record(**overrides):
    record = {
        "source": "Instagram",
        "sender": "Mar",
        "timestamp": datetime(2026, 5, 29, 19, 30, tzinfo=timezone.utc),
        "message_normalized": "hola mi amor",
    }
    record.update(overrides)
    return record


def test_build_message_key_is_deterministic() -> None:
    assert build_message_key(_record()) == build_message_key(_record())


def test_equal_records_generate_same_message_key() -> None:
    first = _record(source=" instagram ")
    second = _record(source="instagram")

    assert build_message_key(first) == build_message_key(second)


def test_changing_timestamp_changes_message_key() -> None:
    assert build_message_key(_record()) != build_message_key(
        _record(timestamp=datetime(2026, 5, 30, 19, 30, tzinfo=timezone.utc))
    )


def test_changing_message_normalized_changes_message_key() -> None:
    assert build_message_key(_record()) != build_message_key(
        _record(message_normalized="otro mensaje")
    )


def test_changing_source_changes_message_key() -> None:
    assert build_message_key(_record()) != build_message_key(
        _record(source="whatsapp")
    )
