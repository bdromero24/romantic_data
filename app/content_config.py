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
    "spotify_capsule": {
        "enabled": True,
        "title": "Mujer Amante",
        "artist": "Rata Blanca",
        "badge_text": "La primera cancion que te dediqué",
        "song_path": "ui/assets/audio/Mujer_amante_fragment.mp3",
        "cover_image_path": "ui/assets/images/spotify_capsule_cover.png",
        "cover_image_paths": [
            "ui/assets/images/spotify_capsule_cover.png",
            "ui/assets/images/spotify_capsule_cover_2.png",
            "ui/assets/images/spotify_capsule_cover_3.png",
            "ui/assets/images/spotify_capsule_cover_4.jpg",
            "ui/assets/images/spotify_capsule_cover_5.jpg",
            "ui/assets/images/spotify_capsule_cover_6.jpg",
        ],
        "cover_rotation_seconds": 7,
        "start_time_seconds": 0,
        "duration_seconds": 70,
        "lyrics_data": [

            {
             "time": 0,
            "text": "Te la dedico una vez mas.",
            },
            {
                "time": 2,
                "text": "Siento el calor de toda tu piel.",
            },
            {
                "time": 6,
                "text": "En mi cuerpo otra vez.",
            },
            {
                "time": 10,
                "text": "Estrella fugaz.",
            },
            {
                "time": 12,
                "text": "Enciende mi sed.",
            },
            {
                "time": 14,
                "text": "Misteriosa mujer.",
            },
            {
                "time": 18,
                "text": "Con tú amor sensual.",
            },
            {
                "time": 22,
                "text": "Cuánto me das.",
            },
            {
                "time": 26,
                "text": "Haz que mi sueño.",
            },
            {
                "time": 29,
                "text": "Sea.",
            },
            {
                "time": 31,
                "text": "Una verdad.",
            },
            {
                "time": 35,
                "text": "Dame tú alma hoy.",
            },
            {
                "time": 38,
                "text": "Haz el ritual.",
            },
            {
                "time": 43,
                "text": "Llévame al mundo.",
            },
            {
                "time": 45,
                "text": "Donde.",
            },
            {
                "time": 48,
                "text": "Pueda soñar.",
            },
            {
                "time": 52,
                "text": "Uh.",
            },
            {
                "time": 54,
                "text":"Debo saber si en verdad",
            },
            {
                "time": 57,
                "text":"En algún lado estás",
            },
            {
                "time": 60,
                "text":"Voy a buscar",
            },
            {
                "time": 62,
                "text":"Una señal.",
            },
            {
                "time": 65,
                "text":"Una canción.",
            },
        ],
    },
    "birthday_invitation": {
        "enabled": True,
        "closed_title": "Nueva carta para ti \U0001f48c",
        "closed_subtitle": "Toca para abrir tú invitacion",
        "letter_title": "Amor mio:",
        "letter_body": [
            "Tengo una invitación especial para ti.",
            (
                "En 1 mes, 1 semana y 5 días cumple años la mujer que amo, es por esa razon, que a esa mujer, le quiero proponer algo que le puede interesar:"
            ),
            (
                "Te invito a pasar tú noche de cumpleaños en un lugar donde tendremos la vista nocturna mas increible de la ciudad"
            ),
            (
                "Hay dos opciones que quiero mostrarte. La idea es que "
                "escojamos juntos el lugar donde vamos a guardar otro "
                "recuerdo bonito."
            ),
            (
                "Se que parece loco y tal vez desubicado de mi parte, asi que entiendo si lo primero que piensas es que no se va a poder."
                "\n\n"
                "Sin embargo la propuesta esta sobre la mesa y quiero que sea una noche "
                "pensada para ti, para celebrar tu vida y para recordarte lo "
                "mucho que te amo."
            ),
        ],
        "signature": "Con amor, David",
        "primary_link_text": "Ver opcion 1",
        "primary_link_url": "https://www.instagram.com/reel/Da3LHXnRmyK/?igsh=MTBjeHpheWd4NXF4Mw==",
        "secondary_link_text": "Ver opcion 2",
        "secondary_link_url": "https://vt.tiktok.com/ZS4D3soyX/",
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
