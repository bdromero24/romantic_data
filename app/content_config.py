"""Manual content configuration for the romantic landing."""

from __future__ import annotations

from typing import Any


DISPLAY_LABELS = {
    "te amo": "te amo",
    "te adoro": "te adoro",
    "te extrano": "te extraño",
    "extrano": "extraño",
    "mi amor": "mi amor",
    "amor mio": "amor mío",
    "mi vida": "mi vida",
    "me haces feliz": "me haces feliz",
}

HER_SENDER_NAME = "𝑴𝒂𝒓🍓"


ROMANTIC_CONTENT: dict[str, Any] = {
    "special_message": {
        "title": "Un mensaje que quiero guardar",
        "subtitle": "Hay palabras que merecen quedarse <strong>aquí</strong>.",
        "message_id": 1440,
        "blocks": [
            {
                "type": "her_messages",
                "title": "Cosas bonitas que que me dijiste",
                "message_ids": [5038, 5039, 5040, 5041, 5042],
            },
            {
                "type": "conversation_pair",
                "title": "Una conversacion que quiero recordar",
                "messages": [
                    {
                        "role": "me",
                        "message_id": 6157,
                    },
                    {
                        "role": "me",
                        "message_id": 6156,
                    },
                    {
                        "role": "me",
                        "message_id": 6155,
                    },
                    {
                        "role": "her",
                        "message_id": 6151,
                    },
                    {
                        "role": "her",
                        "message_id": 6150,
                    },
                    {
                        "role": "her",
                        "message_id": 6141,
                    },
                    {
                        "role": "her",
                        "message_id": 6218,
                    },
                    {
                        "role": "me",
                        "message_id": 6209,
                    },
                    {
                        "role": "her",
                        "message_id": 6085,
                    },
                    {
                        "role": "me",
                        "message_id": 5498,
                    },
                    {
                        "role": "me",
                        "message_id": 5505,
                    },            
                    {
                        "role": "her",
                        "message_id": 5506,
                    },
                ],
            },
        ],
    },
    "first_te_amo": {
        "title": "El primer te amo",
        "subtitle": "El primer momento donde esas palabras quedaron guardadas.",
        "message_id": 18729,
    },
    "timeline": [
        {
            "title": "El primer mensaje guardado",
            "message_id": None,
            "mode": "auto_first_message",
        },
        {
            "title": "El primer te amo",
            "message_id": 18729,
            "mode": "manual_message",
        },
        {
            "title": "El primer te extraño",
            "message_id": None,
            "mode": "auto_first_te_extrano",
        },
        {
            "title": "Primera vez que te hice feliz",
            "message_id": None,
            "mode": "auto_first_happy_message",
        },
        {
            "title": "El día que más hablamos",
            "message_id": None,
            "mode": "auto_peak_day",
        },
        {
            "title": "Nuestro mes más intenso",
            "message_id": None,
            "mode": "auto_peak_month",
        },
    ],
    "featured_quotes": {
        "title": "Mensajes para volver a leer despacio",
        "message_ids": [6180,6190,97,1840,6096,13928,17501,10633,11794],
        "fallback_limit": 5,
    },
}


def get_display_label(value: str) -> str:
    """Return the UI label for an internal normalized value."""
    return DISPLAY_LABELS.get(value, value)


def get_reserved_message_ids() -> set[int]:
    """Return manually selected IDs that automatic sections should not repeat."""
    configured_ids: list[Any] = []
    special_message = ROMANTIC_CONTENT.get("special_message", {})
    configured_ids.append(special_message.get("message_id"))
    configured_ids.extend(_get_special_message_block_ids(special_message))
    configured_ids.append(ROMANTIC_CONTENT["first_te_amo"].get("message_id"))
    configured_ids.extend(
        item.get("message_id")
        for item in ROMANTIC_CONTENT.get("timeline", [])
    )
    configured_ids.extend(ROMANTIC_CONTENT["featured_quotes"].get("message_ids", []))

    return {
        message_id
        for message_id in configured_ids
        if isinstance(message_id, int) and not isinstance(message_id, bool)
    }


def _get_special_message_block_ids(
    special_message: dict[str, Any],
) -> list[Any]:
    """Return raw IDs configured in special message blocks."""
    configured_ids: list[Any] = []

    for block in special_message.get("blocks", []):
        if not isinstance(block, dict):
            continue

        configured_ids.extend(block.get("message_ids", []))
        for message in block.get("messages", []):
            if isinstance(message, dict):
                configured_ids.append(message.get("message_id"))

    return configured_ids
