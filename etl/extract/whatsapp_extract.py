"""WhatsApp text export extraction."""

from __future__ import annotations

import re
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from logger.logger import log_critical_error


PLAIN_LINE_PATTERN = re.compile(
    r"^(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s+"
    r"(?P<time>\d{1,2}:\d{2})(?:\s+(?P<ampm>[ap]\.?\s*m\.?))?\s+-\s+"
    r"(?P<sender>[^:]+):\s*(?P<message>.*)$",
    re.IGNORECASE,
)
BRACKETED_LINE_PATTERN = re.compile(
    r"^\[(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s+"
    r"(?P<time>\d{1,2}:\d{2}(?::\d{2})?)"
    r"(?:\s+(?P<ampm>[ap]\.?\s*m\.?))?\]\s+"
    r"(?P<sender>[^:]+):\s*(?P<message>.*)$",
    re.IGNORECASE,
)
BOGOTA_TIMEZONE = timezone(timedelta(hours=-5))
WHATSAPP_DATE_FORMATS = (
    "%m/%d/%Y",
    "%m/%d/%y",
)


def parse_whatsapp_datetime(
    date_text: str,
    time_text: str,
    ampm_text: str | None = None,
) -> datetime:
    """Parse WhatsApp date and time fragments into a datetime."""
    parsed_date = _parse_whatsapp_date(date_text)
    time_parts = [int(part) for part in time_text.split(":")]
    hour = time_parts[0]
    minute = time_parts[1]
    second = time_parts[2] if len(time_parts) == 3 else 0

    if ampm_text is not None:
        marker = ampm_text.lower().replace(".", "").replace(" ", "")
        if marker == "pm" and hour < 12:
            hour += 12
        elif marker == "am" and hour == 12:
            hour = 0

    return datetime(
        year=parsed_date.year,
        month=parsed_date.month,
        day=parsed_date.day,
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=BOGOTA_TIMEZONE,
    )


def _parse_whatsapp_date(date_text: str) -> date:
    for date_format in WHATSAPP_DATE_FORMATS:
        try:
            return datetime.strptime(date_text, date_format).date()
        except ValueError:
            continue

    raise ValueError(f"Unsupported WhatsApp date format: {date_text}")


def parse_whatsapp_line(line: str) -> dict[str, Any] | None:
    """Parse one WhatsApp message line or return None for non-message lines."""
    match = PLAIN_LINE_PATTERN.match(line) or BRACKETED_LINE_PATTERN.match(line)
    if match is None:
        return None

    timestamp = parse_whatsapp_datetime(
        date_text=match.group("date"),
        time_text=match.group("time"),
        ampm_text=match.group("ampm"),
    )

    return {
        "source": "whatsapp",
        "sender": match.group("sender").strip(),
        "message": match.group("message"),
        "timestamp": timestamp,
        "raw_line": line,
    }


def extract_whatsapp_messages(file_path: str | Path) -> list[dict[str, Any]]:
    """Extract WhatsApp messages from an official .txt chat export."""
    path = Path(file_path)
    messages: list[dict[str, Any]] = []

    try:
        with path.open("r", encoding="utf-8") as chat_file:
            for raw_line in chat_file:
                line = raw_line.rstrip("\n")
                parsed_message = parse_whatsapp_line(line)

                if parsed_message is not None:
                    messages.append(parsed_message)
                    continue

                if messages:
                    messages[-1]["message"] = f"{messages[-1]['message']}\n{line}"
                    messages[-1]["raw_line"] = f"{messages[-1]['raw_line']}\n{line}"
    except (FileNotFoundError, OSError, UnicodeError) as error:
        _log_extract_error(type(error).__name__, error, "extract_whatsapp_messages")
        raise
    except Exception as error:
        _log_extract_error(type(error).__name__, error, "extract_whatsapp_messages")
        raise

    return messages


def _log_extract_error(
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
