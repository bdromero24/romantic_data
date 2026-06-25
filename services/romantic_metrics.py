"""Romantic landing metrics assembled from database read helpers."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from app.content_config import (
    HER_SENDER_NAME,
    ROMANTIC_CONTENT,
    get_display_label,
    get_reserved_message_ids,
)
from db.romantic_queries import (
    count_hater_word_occurrences,
    count_pattern_occurrences,
    fetch_average_daily_messages,
    fetch_conversation_starter,
    fetch_favorite_hour,
    fetch_first_message,
    fetch_first_pattern_message,
    fetch_hourly_rhythm,
    fetch_monthly_rhythm,
    fetch_message_by_id,
    fetch_messages_by_ids,
    fetch_pattern_messages,
    fetch_peak_day,
    fetch_peak_month,
    fetch_romantic_summary,
    fetch_romantic_word_counts,
    fetch_sender_rhythm,
    fetch_weekday_rhythm,
)
from app.chart_config import CHARTS_MAX_DATE
from logger.logger import log_critical_error


ROMANTIC_PHRASES: tuple[dict[str, str], ...] = (
    {"key": "te_amo", "label": "te amo", "pattern": r"\mte\s+amo+\M"},
    {"key": "te_adoro", "label": "te adoro", "pattern": r"\mte\s+adoro+\M"},
    {"key": "te_extrano", "label": "te extrano", "pattern": r"\mte\s+extrano+\M"},
    {"key": "mi_amor", "label": "mi amor", "pattern": r"\mmi\s+amor\M"},
    {"key": "amor_mio", "label": "amor mio", "pattern": r"\mamor\s+mio\M"},
    {"key": "mi_vida", "label": "mi vida", "pattern": r"\mmi\s+vida\M"},
    {"key": "amor", "label": "amor", "pattern": r"\mamor\M"},
    {"key": "preciosa", "label": "preciosa", "pattern": r"\mpreciosa\M"},
    {"key": "hermosa", "label": "hermosa", "pattern": r"\mhermosa\M"},
    {"key": "linda", "label": "linda", "pattern": r"\mlinda\M"},
    {"key": "divina", "label": "divina", "pattern": r"\mdivina\M"},
    {
        "key": "me_haces_feliz",
        "label": "me haces feliz",
        "pattern": r"\mme\s+haces\s+feliz\M",
    },
    {"key": "odio", "label": "odio", "pattern": r"\modio\M"},
    {"key": "hate", "label": "hate", "pattern": r"\mhate\M"},
)

FEATURED_PATTERNS: tuple[str, ...] = (
    r"\mte\s+amo+\M",
    r"\mme\s+siento\s+muy\s+amada\M",
    r"\mme\s+gusta\M",
    r"\mbesitos\M",
    r"\mabrazos?\M",
    r"\mtranquila\M",
    r"\mmi\s+amor\M",
    r"\mmi\s+vida\M",
)

WEEKDAY_LABELS: dict[int, str] = {
    1: "Lunes",
    2: "Martes",
    3: "Miercoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sabado",
    7: "Domingo",
}


def get_romantic_landing_metrics() -> dict[str, Any]:
    """Return all data required by the romantic Streamlit landing."""
    try:
        summary = fetch_romantic_summary()
        phrase_counts = _build_phrase_counts()
        romantic_words = _build_romantic_words()
        first_message = fetch_first_message()
        first_te_amo = _fetch_configured_message(
            "first_te_amo",
            fallback_pattern=r"\mte\s+amo+\M",
        )
        first_te_extrano = fetch_first_pattern_message(r"\mte\s+extrano+\M")
        first_happy_message = fetch_first_pattern_message(
            r"\mme\s+haces\s+feliz\M"
        )
        peak_day = fetch_peak_day()
        peak_month = fetch_peak_month()
        favorite_hour = fetch_favorite_hour()
        conversation_starter = fetch_conversation_starter()
        average_daily_messages = fetch_average_daily_messages()
        hater_full_time = _build_hater_full_time_card(
            count_hater_word_occurrences(HER_SENDER_NAME)
        )

        return {
            "hero": _build_hero(summary),
            "summary_cards": _build_summary_cards(
                summary=summary,
                phrase_counts=phrase_counts,
                peak_month=peak_month,
                favorite_hour=favorite_hour,
                first_te_amo=first_te_amo,
                romantic_words=romantic_words,
                hater_full_time=hater_full_time,
                average_daily_messages=average_daily_messages,
            ),
            "hater_full_time": hater_full_time,
            "phrase_counts": phrase_counts,
            "timeline": _build_timeline(
                first_message=first_message,
                first_te_amo=first_te_amo,
                first_te_extrano=first_te_extrano,
                first_happy_message=first_happy_message,
                peak_day=peak_day,
                peak_month=peak_month,
            ),
            "words": romantic_words,
            "special_message": _build_special_message_card(),
            "featured_messages": _build_featured_messages(),
            "rhythm": {
                "hours": _format_hourly_rhythm(fetch_hourly_rhythm()),
                "weekdays": _format_weekday_rhythm(fetch_weekday_rhythm()),
                "months": _format_monthly_rhythm(fetch_monthly_rhythm()),
                "senders": _format_sender_rhythm(
                    fetch_sender_rhythm(CHARTS_MAX_DATE)
                ),
            },
            "conversation_starter": _format_conversation_starter(
                conversation_starter
            ),
        }
    except Exception as error:
        log_critical_error(
            error_type=type(error).__name__,
            error_message=str(error),
            module_name=__name__,
            function_name="get_romantic_landing_metrics",
        )
        raise


def _build_phrase_counts() -> list[dict[str, Any]]:
    return [
        {
            "key": phrase["key"],
            "label": get_display_label(phrase["label"]),
            "count": count_pattern_occurrences(phrase["pattern"]),
        }
        for phrase in ROMANTIC_PHRASES
    ]


def _build_hero(summary: dict[str, Any]) -> dict[str, str]:
    return {
        "title": "Nuestra historia",
        "subtitle": (
            "Contada con mensajes, recuerdos y pequenos datos bonitos."
        ),
        "date_range": _format_date_range(
            summary.get("first_message_timestamp"),
            summary.get("last_message_timestamp"),
        ),
        "welcome": "Un pedacito de nosotros, convertido en una pagina para recordar.",
    }


def _build_summary_cards(
    summary: dict[str, Any],
    phrase_counts: list[dict[str, Any]],
    peak_month: dict[str, Any] | None,
    favorite_hour: dict[str, Any] | None,
    first_te_amo: dict[str, Any] | None,
    romantic_words: list[dict[str, str]],
    hater_full_time: dict[str, str],
    average_daily_messages: float,
) -> list[dict[str, str]]:
    counts_by_key = {
        phrase_count["key"]: phrase_count["count"]
        for phrase_count in phrase_counts
    }
    return [
        {
            "label": "Mensajes compartidos",
            "value": _format_number(summary.get("total_messages", 0)),
            "description": "Cada uno guardando una parte de nuestra historia.",
            "size": "large",
        },
        {
            "label": "Primer te amo",
            "value": _format_date(
                first_te_amo.get("timestamp") if first_te_amo else None
            ),
            "description": _format_sender_description(first_te_amo),
            "size": "large",
        },
        {
            "label": "Mes mas intenso",
            "value": _format_month(
                peak_month.get("message_month") if peak_month else None
            ),
            "description": _format_count_description(
                peak_month,
                "mensajes en ese mes",
            ),
            "size": "large",
        },
        {
            "label": "Dias hablando",
            "value": _format_number(summary.get("total_conversation_days", 0)),
            "description": "Dias en los que nos encontramos en palabras.",
            "size": "small",
        },
        {
            "label": "Promedio diario",
            "value": _format_decimal(average_daily_messages),
            "description": "mensajes al dia entre los dos.",
            "size": "small",
        },
        {
            "label": "Veces que dijimos te amo",
            "value": _format_number(counts_by_key.get("te_amo", 0)),
            "description": "Una frase pequena para algo enorme.",
            "size": "small",
        },
        {
            "label": "Veces que dijimos te extraño",
            "value": _format_number(counts_by_key.get("te_extrano", 0)),
            "description": "Cuando nos hacemos falta.",
            "size": "small",
        },
        {
            "label": "Nuestra hora favorita",
            "value": _format_hour(
                favorite_hour.get("message_hour") if favorite_hour else None
            ),
            "description": _format_count_description(
                favorite_hour,
                "mensajes a esa hora",
            ),
            "size": "small",
        },
        {
            "label": "Palabra bonita mas usada",
            "value": romantic_words[0]["word"] if romantic_words else "Pendiente",
            "description": _format_word_description(romantic_words),
            "size": "small",
        },
        {
            "label": hater_full_time["title"],
            "value": hater_full_time["keyword"],
            "description": hater_full_time["description"],
            "size": "small",
        },
    ]


def _build_hater_full_time_card(count: int) -> dict[str, str]:
    formatted_count = _format_number(count)
    return {
        "title": "Hater de tiempo completo",
        "keyword": "odio",
        "count": formatted_count,
        "description": f"Utilizaste la palabra odio {formatted_count} veces",
    }


def _build_timeline(
    first_message: dict[str, Any] | None,
    first_te_amo: dict[str, Any] | None,
    first_te_extrano: dict[str, Any] | None,
    first_happy_message: dict[str, Any] | None,
    peak_day: dict[str, Any] | None,
    peak_month: dict[str, Any] | None,
) -> list[dict[str, str]]:
    automatic_events = {
        "auto_first_message": first_message,
        "auto_first_te_amo": first_te_amo,
        "auto_first_te_extrano": first_te_extrano,
        "auto_first_happy_message": first_happy_message,
    }
    events: list[dict[str, str]] = []

    for item in ROMANTIC_CONTENT.get("timeline", []):
        title = _safe_text(item.get("title"), "Momento guardado")
        mode = _safe_text(item.get("mode"), "manual_message")

        if mode == "manual_message":
            events.append(_message_event(title, _fetch_manual_timeline_message(item)))
            continue

        if mode in automatic_events:
            events.append(_message_event(title, automatic_events[mode]))
            continue

        if mode == "auto_peak_day":
            events.append(
                {
                    "title": title,
                    "date": _format_date(
                        peak_day.get("message_day") if peak_day else None
                    ),
                    "detail": _format_count_description(
                        peak_day,
                        "mensajes en ese dia",
                    ),
                }
            )
            continue

        if mode == "auto_peak_month":
            events.append(
                {
                    "title": title,
                    "date": _format_month(
                        peak_month.get("message_month") if peak_month else None
                    ),
                    "detail": _format_count_description(
                        peak_month,
                        "mensajes en ese mes",
                    ),
                }
            )

    return events


def _message_event(title: str, message_row: dict[str, Any] | None) -> dict[str, str]:
    if not message_row:
        return {
            "title": title,
            "date": "Pendiente",
            "detail": "Aun no aparece en los mensajes cargados.",
        }

    sender = _safe_text(message_row.get("sender"), "Nosotros")
    message = _safe_text(message_row.get("message"), "Mensaje guardado")
    return {
        "title": title,
        "date": _format_date(message_row.get("timestamp")),
        "detail": f"{sender}: {message}",
    }


def _build_romantic_words() -> list[dict[str, str]]:
    return [
        {
            "word": get_display_label(_safe_text(row.get("word"), "")),
            "count": _format_number(row.get("word_count", 0)),
        }
        for row in fetch_romantic_word_counts(limit=12)
        if _safe_text(row.get("word"), "")
    ]


def _build_featured_messages() -> list[dict[str, str]]:
    raw_manual_ids = ROMANTIC_CONTENT["featured_quotes"].get("message_ids", [])
    if isinstance(raw_manual_ids, list) and raw_manual_ids:
        manual_ids = _valid_message_ids(raw_manual_ids)
        return _build_manual_featured_messages(manual_ids)

    fallback_limit = _get_featured_quote_fallback_limit()
    reserved_message_ids = get_reserved_message_ids()
    featured_messages: list[dict[str, str]] = []
    seen_message_ids: set[int] = set()
    seen_messages: set[tuple[str, str, str]] = set()

    for pattern in FEATURED_PATTERNS:
        rows = fetch_pattern_messages(pattern=pattern, limit=4)
        for row in rows:
            message_id = row.get("id")
            if isinstance(message_id, int) and message_id in reserved_message_ids:
                continue

            message = _safe_text(row.get("message"), "")
            if not message:
                continue

            if isinstance(message_id, int):
                if message_id in seen_message_ids:
                    continue
                seen_message_ids.add(message_id)

            key = (
                _safe_text(row.get("sender"), ""),
                message,
                _format_date(row.get("timestamp")),
            )
            if key in seen_messages:
                continue

            seen_messages.add(key)
            featured_messages.append(
                _format_message_card(row)
            )

            if len(featured_messages) >= fallback_limit:
                return featured_messages

    return featured_messages


def _build_manual_featured_messages(message_ids: list[int]) -> list[dict[str, str]]:
    return [_format_message_card(row) for row in fetch_messages_by_ids(message_ids)]


def _build_special_message_card() -> dict[str, Any]:
    config = ROMANTIC_CONTENT["special_message"]
    blocks = _build_special_message_blocks(config)
    fallback_row = None if blocks else _fetch_configured_message("special_message")

    return {
        "title": _safe_text(config.get("title"), "Un mensaje que quiero guardar"),
        "subtitle": _safe_text(
            config.get("subtitle"),
            "Hay palabras que merecen quedarse aqui.",
        ),
        "blocks": blocks,
        "message": _safe_text(fallback_row.get("message"), "")
        if fallback_row
        else "",
        "sender": _safe_text(fallback_row.get("sender"), "Nosotros")
        if fallback_row
        else "Pendiente",
        "date": _format_date(fallback_row.get("timestamp"))
        if fallback_row
        else "Pendiente",
    }


def _build_special_message_blocks(config: dict[str, Any]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []

    for block in config.get("blocks", []):
        if not isinstance(block, dict):
            continue

        block_type = _safe_text(block.get("type"), "")
        if block_type == "her_messages":
            formatted_block = _build_her_messages_block(block)
        elif block_type == "conversation_pair":
            formatted_block = _build_conversation_pair_block(block)
        else:
            formatted_block = None

        if formatted_block:
            blocks.append(formatted_block)

    return blocks


def _build_her_messages_block(block: dict[str, Any]) -> dict[str, Any] | None:
    message_ids = _valid_message_ids(block.get("message_ids", []))
    messages = [
        _format_special_message_row(row, role="her")
        for row in fetch_messages_by_ids(message_ids)
    ]
    if not messages:
        return None

    return {
        "type": "her_messages",
        "title": _optional_text(block.get("title")),
        "messages": messages,
    }


def _build_conversation_pair_block(block: dict[str, Any]) -> dict[str, Any] | None:
    configured_messages = [
        message
        for message in block.get("messages", [])
        if isinstance(message, dict)
    ]
    message_ids = _valid_message_ids(
        [message.get("message_id") for message in configured_messages]
    )
    rows_by_id = {
        row["id"]: row
        for row in fetch_messages_by_ids(message_ids)
        if isinstance(row.get("id"), int)
    }
    messages: list[dict[str, str]] = []

    for configured_message in configured_messages:
        message_id = configured_message.get("message_id")
        if not isinstance(message_id, int) or isinstance(message_id, bool):
            continue

        row = rows_by_id.get(message_id)
        if row:
            messages.append(
                _format_special_message_row(
                    row,
                    role=_normalize_conversation_role(
                        configured_message.get("role")
                    ),
                )
            )

    if not messages:
        return None

    return {
        "type": "conversation_pair",
        "title": _optional_text(block.get("title")),
        "messages": messages,
    }


def _fetch_configured_message(
    key: str,
    fallback_pattern: str | None = None,
) -> dict[str, Any] | None:
    config = ROMANTIC_CONTENT.get(key, {})
    message_id = config.get("message_id")
    if message_id is not None:
        message = fetch_message_by_id(message_id)
        if message is not None:
            return message

    if fallback_pattern:
        return fetch_first_pattern_message(fallback_pattern)

    return None


def _fetch_special_message(
    key: str,
    fallback_pattern: str | None = None,
) -> dict[str, Any] | None:
    legacy_keys = {
        "primer_te_amo": "first_te_amo",
        "mensaje_especial": "special_message",
    }
    return _fetch_configured_message(
        legacy_keys.get(key, key),
        fallback_pattern=fallback_pattern,
    )


def _fetch_manual_timeline_message(item: dict[str, Any]) -> dict[str, Any] | None:
    message_id = item.get("message_id")
    if not isinstance(message_id, int) or isinstance(message_id, bool):
        return None

    return fetch_message_by_id(message_id)


def _get_featured_quote_message_ids() -> list[int]:
    raw_ids = ROMANTIC_CONTENT["featured_quotes"].get("message_ids", [])
    return _valid_message_ids(raw_ids)


def _get_featured_quote_fallback_limit() -> int:
    limit = ROMANTIC_CONTENT["featured_quotes"].get("fallback_limit", 5)
    if not isinstance(limit, int) or isinstance(limit, bool):
        return 5

    return max(1, min(limit, 50))


def _format_message_card(row: dict[str, Any]) -> dict[str, str]:
    return {
        "message": _safe_text(row.get("message"), ""),
        "sender": _safe_text(row.get("sender"), "Nosotros"),
        "date": _format_date(row.get("timestamp")),
    }


def _format_special_message_row(
    row: dict[str, Any],
    role: str,
) -> dict[str, str]:
    return {
        "role": _normalize_conversation_role(role),
        "message": _safe_text(row.get("message"), ""),
        "sender": _safe_text(row.get("sender"), "Nosotros"),
        "date": _format_date(row.get("timestamp")),
    }


def _normalize_conversation_role(value: Any) -> str:
    return "me" if value == "me" else "her"


def _valid_message_ids(raw_ids: Any) -> list[int]:
    if not isinstance(raw_ids, list):
        return []

    message_ids: list[int] = []
    seen_ids: set[int] = set()
    for raw_id in raw_ids:
        if not isinstance(raw_id, int) or isinstance(raw_id, bool):
            continue
        if raw_id in seen_ids:
            continue

        seen_ids.add(raw_id)
        message_ids.append(raw_id)

    return message_ids


def _format_hourly_rhythm(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "label": _format_hour(row.get("label")),
            "value": int(row.get("message_count") or 0),
        }
        for row in rows
    ]


def _format_weekday_rhythm(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "label": WEEKDAY_LABELS.get(int(row.get("label") or 0), "Dia"),
            "value": int(row.get("message_count") or 0),
        }
        for row in rows
    ]


def _format_monthly_rhythm(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "label": _format_month(row.get("label")),
            "date": row.get("label"),
            "value": int(row.get("message_count") or 0),
        }
        for row in rows
    ]


def _format_sender_rhythm(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "label": _safe_text(row.get("label"), "Nosotros"),
            "value": int(row.get("value") or 0),
        }
        for row in rows
    ]


def _format_conversation_starter(row: dict[str, Any] | None) -> dict[str, str]:
    if not row:
        return {
            "sender": "Pendiente",
            "detail": "Aun no hay suficientes mensajes para contar este recuerdo.",
        }

    return {
        "sender": _safe_text(row.get("sender"), "Nosotros"),
        "detail": _format_count_description(
            row,
            "dias iniciando la conversacion",
            count_key="conversation_start_count",
        ),
    }


def _format_date_range(start_value: Any, end_value: Any) -> str:
    start_text = _format_date(start_value)
    end_text = _format_date(end_value)
    if start_text == "Pendiente" and end_text == "Pendiente":
        return "Historia lista para llenarse de mensajes"

    return f"{start_text} - {end_text}"


def _format_count_description(
    row: dict[str, Any] | None,
    suffix: str,
    count_key: str = "message_count",
) -> str:
    if not row:
        return "Pendiente con los mensajes cargados."

    return f"{_format_number(row.get(count_key, 0))} {suffix}."


def _format_sender_description(row: dict[str, Any] | None) -> str:
    if not row:
        return "Pendiente con los mensajes cargados."

    sender = _safe_text(row.get("sender"), "Nosotros")
    message = _safe_text(row.get("message"), "Mensaje guardado")
    return f"{sender}: {message}"


def _format_word_description(words: list[dict[str, str]]) -> str:
    if not words:
        return "Pendiente con los mensajes cargados."

    count = words[0].get("count", "0")
    return f"Aparece {count} veces entre nuestras palabras bonitas."


def _format_number(value: Any) -> str:
    try:
        return f"{int(value or 0):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "0"


def _format_decimal(value: Any) -> str:
    try:
        number = float(value or 0)
    except (TypeError, ValueError):
        return "0"

    if number.is_integer():
        return _format_number(number)

    return f"{number:.1f}".replace(".", ",")


def _format_hour(value: Any) -> str:
    try:
        hour = int(value)
    except (TypeError, ValueError):
        return "Pendiente"

    return f"{hour:02d}:00"


def _format_date(value: Any) -> str:
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")

    return "Pendiente"


def _format_month(value: Any) -> str:
    if isinstance(value, datetime):
        return value.strftime("%m/%Y")
    if isinstance(value, date):
        return value.strftime("%m/%Y")

    return "Pendiente"


def _safe_text(value: Any, fallback: str) -> str:
    if value is None:
        return fallback

    text = str(value).strip()
    if not text or text.lower() in {"null", "none", "nan", "na", "n/a"}:
        return fallback

    return text


def _optional_text(value: Any) -> str:
    if value is None:
        return ""

    text = str(value).strip()
    if text.lower() in {"null", "none", "nan", "na", "n/a"}:
        return ""

    return text
