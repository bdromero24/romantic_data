"""Unit tests for WhatsApp text extraction."""

from datetime import datetime, timedelta, timezone

from etl.extract.whatsapp_extract import (
    extract_whatsapp_messages,
    parse_whatsapp_datetime,
    parse_whatsapp_line,
)


BOGOTA_TIMEZONE = timezone(timedelta(hours=-5))


def test_parse_whatsapp_datetime_with_pm_marker() -> None:
    timestamp = parse_whatsapp_datetime("5/29/2026", "7:45", "p. m.")

    assert timestamp == datetime(2026, 5, 29, 19, 45, tzinfo=BOGOTA_TIMEZONE)


def test_parse_whatsapp_datetime_with_two_digit_year() -> None:
    timestamp = parse_whatsapp_datetime("5/29/26", "19:45")

    assert timestamp == datetime(2026, 5, 29, 19, 45, tzinfo=BOGOTA_TIMEZONE)


def test_parse_whatsapp_datetime_uses_month_day_year_for_june_12() -> None:
    timestamp = parse_whatsapp_datetime("6/12/26", "11:30", "AM")

    assert timestamp == datetime(2026, 6, 12, 11, 30, tzinfo=BOGOTA_TIMEZONE)


def test_parse_whatsapp_datetime_uses_month_day_year_for_february_5() -> None:
    timestamp = parse_whatsapp_datetime("2/5/26", "00:00")

    assert timestamp == datetime(2026, 2, 5, tzinfo=BOGOTA_TIMEZONE)


def test_parse_whatsapp_datetime_keeps_unambiguous_month_day_year() -> None:
    timestamp = parse_whatsapp_datetime("12/25/26", "8:05", "PM")

    assert timestamp == datetime(2026, 12, 25, 20, 5, tzinfo=BOGOTA_TIMEZONE)


def test_parse_whatsapp_single_line_message() -> None:
    parsed_message = parse_whatsapp_line(
        "5/29/2026, 19:45 - Alice: Hola mundo"
    )

    assert parsed_message == {
        "source": "whatsapp",
        "sender": "Alice",
        "message": "Hola mundo",
        "timestamp": datetime(2026, 5, 29, 19, 45, tzinfo=BOGOTA_TIMEZONE),
        "raw_line": "5/29/2026, 19:45 - Alice: Hola mundo",
    }


def test_extract_whatsapp_multiline_message(tmp_path) -> None:
    chat_path = tmp_path / "whatsapp_chat.txt"
    chat_path.write_text(
        "5/29/2026, 19:45 - Alice: Primera linea\n"
        "segunda linea\n"
        "[5/29/2026, 19:46:05 p. m.] Bob: Respuesta\n",
        encoding="utf-8",
    )

    messages = extract_whatsapp_messages(chat_path)

    assert len(messages) == 2
    assert messages[0]["message"] == "Primera linea\nsegunda linea"
    assert messages[0]["raw_line"] == (
        "5/29/2026, 19:45 - Alice: Primera linea\nsegunda linea"
    )
    assert messages[1]["sender"] == "Bob"
    assert messages[1]["timestamp"] == datetime(
        2026,
        5,
        29,
        19,
        46,
        5,
        tzinfo=BOGOTA_TIMEZONE,
    )
