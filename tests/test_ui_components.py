"""Unit tests for Streamlit HTML component rendering."""

from __future__ import annotations

from ui import components


def test_timeline_renderer_uses_unsafe_markdown(monkeypatch) -> None:
    markdown_calls: list[tuple[str, bool | None]] = []
    blocked_calls: list[str] = []

    monkeypatch.setattr(
        components.st,
        "markdown",
        lambda html, unsafe_allow_html=None: markdown_calls.append(
            (html, unsafe_allow_html)
        ),
    )
    monkeypatch.setattr(
        components.st,
        "write",
        lambda *_args, **_kwargs: blocked_calls.append("write"),
        raising=False,
    )
    monkeypatch.setattr(
        components.st,
        "code",
        lambda *_args, **_kwargs: blocked_calls.append("code"),
        raising=False,
    )
    monkeypatch.setattr(
        components.st,
        "text",
        lambda *_args, **_kwargs: blocked_calls.append("text"),
        raising=False,
    )
    monkeypatch.setattr(
        components.st,
        "caption",
        lambda *_args, **_kwargs: blocked_calls.append("caption"),
        raising=False,
    )

    components.render_timeline(
        [
            {
                "date": "23/04/2026",
                "title": "Primer <te amo>",
                "detail": "Mar & David",
            }
        ]
    )

    assert blocked_calls == []
    rendered_html, unsafe_allow_html = markdown_calls[0]
    assert unsafe_allow_html is True
    assert rendered_html == components._normalize_html(
        components.build_timeline_html(
            [
                {
                    "date": "23/04/2026",
                    "title": "Primer <te amo>",
                    "detail": "Mar & David",
                }
            ]
        )
    )
    assert "\n            <article" not in rendered_html


def test_quote_and_special_message_html_escape_dynamic_values() -> None:
    quotes_html = components.build_quote_cards_html(
        [
            {
                "message": '<script>alert("x")</script>',
                "sender": "Mar & David",
                "date": "10/06/2026",
            }
        ]
    )
    special_html = components.build_special_message_html(
        {
            "title": "Mensaje <especial>",
            "message": "Te amo & te cuido",
            "sender": "Mar <3",
            "date": "10/06/2026",
        }
    )

    assert '<section class="quote-grid">' in quotes_html
    assert '<article class="quote-card reveal-on-scroll"' in quotes_html
    assert "<script>" not in quotes_html
    assert "&lt;script&gt;" in quotes_html
    assert "Mar &amp; David" in quotes_html

    assert '<article class="special-message-card' in special_html
    assert "ig-chat-card" in special_html
    assert "ig-bubble ig-bubble-her" in special_html
    assert "Mensaje &lt;especial&gt;" in special_html
    assert "Te amo &amp; te cuido" in special_html
    assert "Mar &lt;3" in special_html


def test_hero_renders_local_strawberry_asset(tmp_path, monkeypatch) -> None:
    strawberry_image = tmp_path / "strawberry_8bit.png"
    strawberry_image.write_bytes(b"fake-png")
    monkeypatch.setattr(components, "STRAWBERRY_IMAGE", strawberry_image)

    hero_html = components.build_hero_html(
        {
            "title": "Nuestra historia",
            "subtitle": "Un subtitulo bonito",
            "welcome": "Bienvenida",
            "date_range": "2024 - 2026",
        }
    )

    assert '<div class="hero-orb" aria-hidden="true">' in hero_html
    assert 'class="hero-strawberry"' in hero_html
    assert 'src="data:image/png;base64,ZmFrZS1wbmc="' in hero_html
    assert "Nuestra historia" in hero_html


def test_special_message_allows_only_manual_strong_html() -> None:
    special_html = components.build_special_message_html(
        {
            "subtitle": (
                "Esto <strong>queda</strong> "
                '<em>seguro</em> <strong class="bad">sin atributos</strong>'
            ),
            "message": '<strong>DB no pasa</strong>',
        }
    )

    assert "Esto <strong>queda</strong>" in special_html
    assert "&lt;em&gt;seguro&lt;/em&gt;" in special_html
    assert (
        '&lt;strong class=&quot;bad&quot;&gt;sin atributos&lt;/strong&gt;'
        in special_html
    )
    assert '"&lt;strong&gt;DB no pasa&lt;/strong&gt;"' in special_html


def test_special_message_renders_configured_chat_blocks() -> None:
    special_html = components.build_special_message_html(
        {
            "title": "Mensaje <especial>",
            "subtitle": "Texto <strong>seguro</strong>",
            "blocks": [
                {
                    "type": "her_messages",
                    "title": "Cosas <bonitas>",
                    "messages": [
                        {
                            "role": "her",
                            "message": "Hola <amor>",
                            "sender": "Mar",
                            "date": "01/01/2026",
                        },
                    ],
                },
                {
                    "type": "conversation_pair",
                    "title": "Conversacion",
                    "messages": [
                        {
                            "role": "me",
                            "message": "Yo & tu",
                            "sender": "David",
                            "date": "02/01/2026",
                        },
                    ],
                },
            ],
        }
    )

    assert "Mensaje &lt;especial&gt;" in special_html
    assert "Texto <strong>seguro</strong>" in special_html
    assert "Cosas &lt;bonitas&gt;" in special_html
    assert "Hola &lt;amor&gt;" in special_html
    assert "Yo &amp; tu" in special_html
    assert special_html.count('class="special-message-block') == 2
    assert "special-message-block-her-messages" in special_html
    assert "special-message-block-conversation-pair" in special_html
    assert "ig-bubble ig-bubble-her" in special_html
    assert "ig-bubble ig-bubble-me" in special_html
    assert "Ã‚Â·" not in special_html
    assert "Â·" not in special_html
    assert '<span class="message-meta-separator">-</span>' in special_html


def test_reveal_observer_uses_hidden_streamlit_component(monkeypatch) -> None:
    component_calls: list[tuple[str, int]] = []

    monkeypatch.setattr(
        components.streamlit_components,
        "html",
        lambda html, height=0: component_calls.append((html, height)),
    )

    components.render_reveal_observer()

    rendered_html, height = component_calls[0]
    assert height == 0
    assert "IntersectionObserver" in rendered_html
    assert ".reveal-on-scroll" in rendered_html
