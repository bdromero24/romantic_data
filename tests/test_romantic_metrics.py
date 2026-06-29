"""Unit tests for romantic landing metric assembly."""

from datetime import datetime, timezone

from app import content_config
from app.chart_config import CHARTS_MAX_DATE
from services import romantic_metrics


def test_get_romantic_landing_metrics_builds_story_data(monkeypatch) -> None:
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_romantic_summary",
        lambda: {
            "total_messages": 1200,
            "total_conversation_days": 45,
            "first_message_timestamp": datetime(
                2026,
                1,
                1,
                tzinfo=timezone.utc,
            ),
            "last_message_timestamp": datetime(
                2026,
                6,
                1,
                tzinfo=timezone.utc,
            ),
        },
    )
    monkeypatch.setattr(
        romantic_metrics,
        "count_pattern_occurrences",
        lambda pattern: 7 if "amo" in pattern else 2,
    )
    hater_senders: list[str] = []

    def fake_count_hater_word_occurrences(sender_name: str) -> int:
        hater_senders.append(sender_name)
        return 11

    monkeypatch.setattr(
        romantic_metrics,
        "count_hater_word_occurrences",
        fake_count_hater_word_occurrences,
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_first_message",
        lambda: {
            "sender": "Mar",
            "message": "Hola mi amor",
            "timestamp": datetime(2026, 1, 1, tzinfo=timezone.utc),
        },
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_first_pattern_message",
        lambda pattern: {
            "sender": "David",
            "message": "Te amo",
            "timestamp": datetime(2026, 2, 1, tzinfo=timezone.utc),
        },
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_message_by_id",
        lambda message_id: {
            "id": message_id,
            "sender": "Mar",
            "message": "Te amo oficial",
            "timestamp": datetime(2026, 1, 15, tzinfo=timezone.utc),
        },
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_peak_day",
        lambda: {
            "message_day": datetime(2026, 3, 1, tzinfo=timezone.utc),
            "message_count": 90,
        },
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_peak_month",
        lambda: {
            "message_month": datetime(2026, 3, 1, tzinfo=timezone.utc),
            "message_count": 300,
        },
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_favorite_hour",
        lambda: {"message_hour": 22, "message_count": 80},
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_conversation_starter",
        lambda: {"sender": "Mar", "conversation_start_count": 12},
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_average_daily_messages",
        lambda: 26.7,
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_romantic_word_counts",
        lambda limit: [{"word": "amor", "word_count": 33}],
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_pattern_messages",
        lambda pattern, limit: [
            {
                "sender": "Mar",
                "message": "Me siento muy amada mi vida",
                "timestamp": datetime(2026, 4, 1, tzinfo=timezone.utc),
            }
        ],
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_hourly_rhythm",
        lambda: [{"label": 22, "message_count": 80}],
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_weekday_rhythm",
        lambda: [{"label": 5, "message_count": 60}],
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_monthly_rhythm",
        lambda: [
            {
                "label": datetime(2026, 3, 1, tzinfo=timezone.utc),
                "message_count": 300,
            }
        ],
    )
    sender_cutoffs: list[str | None] = []

    def fake_fetch_sender_rhythm(max_date: str | None) -> list[dict]:
        sender_cutoffs.append(max_date)
        return [{"label": "Mar", "value": 700}]

    monkeypatch.setattr(
        romantic_metrics,
        "fetch_sender_rhythm",
        fake_fetch_sender_rhythm,
    )
    monkeypatch.setitem(
        romantic_metrics.ROMANTIC_CONTENT,
        "special_message",
        {
            "title": "Un mensaje que quiero guardar",
            "subtitle": "Hay palabras que merecen quedarse <strong>aquÃ­</strong>.",
            "message_id": 39145,
            "blocks": [],
        },
    )
    romantic_metrics.ROMANTIC_CONTENT["special_message"]["subtitle"] = (
        "Hay palabras que merecen quedarse <strong>aqu\u00ed</strong>."
    )
    monkeypatch.setitem(
        romantic_metrics.ROMANTIC_CONTENT,
        "featured_quotes",
        {
            "title": "Mensajes para volver a leer despacio",
            "message_ids": [],
            "fallback_limit": 5,
        },
    )

    result = romantic_metrics.get_romantic_landing_metrics()

    assert result["hero"]["title"] == "Nuestra historia"
    assert result["summary_cards"][0]["value"] == "1.200"
    assert result["summary_cards"][0]["label"] == "Mensajes compartidos"
    assert result["summary_cards"][1]["label"] == "Primer te amo"
    assert result["summary_cards"][1]["value"] == "15/01/2026"
    assert result["summary_cards"][2]["label"] == "Mes mas intenso"
    assert result["summary_cards"][3]["label"] == "Dias hablando"
    assert result["summary_cards"][4] == {
        "label": "Promedio diario",
        "value": "27",
        "description": "mensajes al dia entre los dos.",
        "size": "small",
    }
    assert result["summary_cards"][5]["value"] == "7"
    assert result["summary_cards"][6]["label"] == "Veces que dijimos te extraño"
    assert result["summary_cards"][9] == {
        "label": "Hater de tiempo completo",
        "value": "odio",
        "description": "Utilizaste la palabra odio 11 veces",
        "size": "small",
    }
    assert result["summary_cards"][10] == {
        "label": "Quien inició mas veces la conversacion",
        "value": "Mar",
        "description": "12 dias iniciando la conversacion.",
        "size": "small",
    }
    assert result["hater_full_time"] == {
        "title": "Hater de tiempo completo",
        "keyword": "odio",
        "count": "11",
        "description": "Utilizaste la palabra odio 11 veces",
    }
    assert result["timeline"][0]["detail"] == "Mar: Hola mi amor"
    assert result["timeline"][1]["detail"] == "Mar: Te amo oficial"
    assert result["words"] == [{"word": "amor", "count": "33"}]
    assert result["special_message"]["message"] == "Te amo oficial"
    assert result["special_message"]["subtitle"] == (
        "Hay palabras que merecen quedarse <strong>aquí</strong>."
    )
    assert result["featured_messages"][0]["sender"] == "Mar"
    assert result["rhythm"]["hours"] == [{"label": "22:00", "value": 80}]
    assert result["rhythm"]["months"][0]["date"] == datetime(
        2026,
        3,
        1,
        tzinfo=timezone.utc,
    )
    assert result["rhythm"]["senders"] == [{"label": "Mar", "value": 700}]
    assert sender_cutoffs == [CHARTS_MAX_DATE]
    assert result["conversation_starter"]["sender"] == "Mar"
    assert hater_senders == [romantic_metrics.HER_SENDER_NAME]


def test_safe_text_rejects_empty_markers() -> None:
    assert romantic_metrics._safe_text(" null ", "Pendiente") == "Pendiente"
    assert romantic_metrics._safe_text("amor", "Pendiente") == "amor"


def test_format_sender_rhythm_uses_expected_chart_shape() -> None:
    rows = [
        {"label": "Mar", "value": 12},
        {"label": "David", "value": "8"},
    ]

    assert romantic_metrics._format_sender_rhythm(rows) == [
        {"label": "Mar", "value": 12},
        {"label": "David", "value": 8},
    ]


def test_special_message_falls_back_to_first_pattern(monkeypatch) -> None:
    fallback = {
        "sender": "David",
        "message": "Te amo",
        "timestamp": datetime(2026, 2, 1, tzinfo=timezone.utc),
    }

    monkeypatch.setattr(romantic_metrics, "fetch_message_by_id", lambda _: None)
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_first_pattern_message",
        lambda _: fallback,
    )

    result = romantic_metrics._fetch_special_message(
        "primer_te_amo",
        fallback_pattern=r"\mte\s+amo+\M",
    )

    assert result == fallback


def test_featured_messages_skip_reserved_ids_in_fallback(monkeypatch) -> None:
    rows = [
        {
            "id": 39145,
            "sender": "Mar",
            "message": "Te amo oficial",
            "timestamp": datetime(2026, 1, 15, tzinfo=timezone.utc),
        },
        {
            "id": 40210,
            "sender": "David",
            "message": "Un mensaje distinto",
            "timestamp": datetime(2026, 2, 15, tzinfo=timezone.utc),
        },
    ]
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_pattern_messages",
        lambda pattern, limit: rows,
    )
    monkeypatch.setattr(
        romantic_metrics,
        "get_reserved_message_ids",
        lambda: {39145},
    )
    monkeypatch.setitem(
        romantic_metrics.ROMANTIC_CONTENT,
        "featured_quotes",
        {
            "title": "Mensajes para volver a leer despacio",
            "message_ids": [],
            "fallback_limit": 5,
        },
    )

    result = romantic_metrics._build_featured_messages()

    assert result == [
        {
            "message": "Un mensaje distinto",
            "sender": "David",
            "date": "15/02/2026",
        }
    ]


def test_featured_messages_do_not_use_fallback_when_configured_ids_are_invalid(
    monkeypatch,
) -> None:
    fallback_calls: list[str] = []

    monkeypatch.setitem(
        romantic_metrics.ROMANTIC_CONTENT,
        "featured_quotes",
        {
            "title": "Mensajes para volver a leer despacio",
            "message_ids": ["x", None],
            "fallback_limit": 5,
        },
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_messages_by_ids",
        lambda message_ids: [],
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_pattern_messages",
        lambda pattern, limit: fallback_calls.append(pattern) or [],
    )

    assert romantic_metrics._build_featured_messages() == []
    assert fallback_calls == []


def test_special_message_blocks_preserve_configured_order(monkeypatch) -> None:
    monkeypatch.setitem(
        romantic_metrics.ROMANTIC_CONTENT,
        "special_message",
        {
            "title": "Un mensaje que quiero guardar",
            "subtitle": "Algunas palabras merecen quedarse aqui.",
            "message_id": None,
            "blocks": [
                {
                    "type": "her_messages",
                    "title": "Cosas bonitas que ella me dijo",
                    "message_ids": [3, 1],
                },
                {
                    "type": "conversation_pair",
                    "title": "Una conversacion que quiero recordar",
                    "messages": [
                        {"role": "me", "message_id": 2},
                        {"role": "her", "message_id": 4},
                    ],
                },
            ],
        },
    )

    rows_by_id = {
        1: {
            "id": 1,
            "sender": "Mar",
            "message": "Primer mensaje",
            "timestamp": datetime(2026, 1, 1, tzinfo=timezone.utc),
        },
        2: {
            "id": 2,
            "sender": "David",
            "message": "Mensaje mio",
            "timestamp": datetime(2026, 1, 2, tzinfo=timezone.utc),
        },
        3: {
            "id": 3,
            "sender": "Mar",
            "message": "Mensaje de ella",
            "timestamp": datetime(2026, 1, 3, tzinfo=timezone.utc),
        },
        4: {
            "id": 4,
            "sender": "Mar",
            "message": "Respuesta de ella",
            "timestamp": datetime(2026, 1, 4, tzinfo=timezone.utc),
        },
    }

    monkeypatch.setattr(
        romantic_metrics,
        "fetch_messages_by_ids",
        lambda message_ids: [rows_by_id[message_id] for message_id in message_ids],
    )

    result = romantic_metrics._build_special_message_card()

    assert result["blocks"][0]["messages"][0]["message"] == "Mensaje de ella"
    assert result["blocks"][0]["messages"][1]["message"] == "Primer mensaje"
    assert result["blocks"][1]["messages"][0]["role"] == "me"
    assert result["blocks"][1]["messages"][1]["role"] == "her"


def test_special_message_block_titles_can_be_empty(monkeypatch) -> None:
    monkeypatch.setitem(
        romantic_metrics.ROMANTIC_CONTENT,
        "special_message",
        {
            "title": "Un mensaje que quiero guardar",
            "subtitle": "Algunas palabras merecen quedarse aqui.",
            "message_id": None,
            "blocks": [
                {
                    "type": "her_messages",
                    "title": "",
                    "message_ids": [1],
                },
            ],
        },
    )
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_messages_by_ids",
        lambda message_ids: [
            {
                "id": 1,
                "sender": "Mar",
                "message": "Mensaje de ella",
                "timestamp": datetime(2026, 1, 1, tzinfo=timezone.utc),
            }
        ],
    )

    result = romantic_metrics._build_special_message_card()

    assert result["blocks"][0]["title"] == ""


def test_manual_featured_messages_use_configured_ids(monkeypatch) -> None:
    rows = [
        {
            "id": 20,
            "sender": "Mar",
            "message": "Segundo elegido",
            "timestamp": datetime(2026, 2, 2, tzinfo=timezone.utc),
        },
        {
            "id": 10,
            "sender": "David",
            "message": "Primer elegido",
            "timestamp": datetime(2026, 1, 1, tzinfo=timezone.utc),
        },
    ]
    monkeypatch.setattr(
        romantic_metrics,
        "fetch_messages_by_ids",
        lambda message_ids: rows,
    )

    result = romantic_metrics._build_manual_featured_messages([20, 10])

    assert result == [
        {"message": "Segundo elegido", "sender": "Mar", "date": "02/02/2026"},
        {"message": "Primer elegido", "sender": "David", "date": "01/01/2026"},
    ]


def test_reserved_message_ids_include_special_blocks(monkeypatch) -> None:
    monkeypatch.setitem(
        content_config.ROMANTIC_CONTENT,
        "special_message",
        {
            "message_id": 1,
            "blocks": [
                {"type": "her_messages", "message_ids": [2, None, "3"]},
                {
                    "type": "conversation_pair",
                    "messages": [
                        {"role": "me", "message_id": 4},
                        {"role": "her", "message_id": ""},
                    ],
                },
            ],
        },
    )
    monkeypatch.setitem(
        content_config.ROMANTIC_CONTENT,
        "first_te_amo",
        {"message_id": 5},
    )
    monkeypatch.setitem(
        content_config.ROMANTIC_CONTENT,
        "timeline",
        [{"message_id": 6}, {"message_id": None}],
    )
    monkeypatch.setitem(
        content_config.ROMANTIC_CONTENT,
        "featured_quotes",
        {"message_ids": [7, "8", None]},
    )

    assert content_config.get_reserved_message_ids() == {1, 2, 4, 5, 6, 7}
