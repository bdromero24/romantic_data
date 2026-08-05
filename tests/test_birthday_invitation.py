"""Unit tests for the birthday invitation component."""

from ui import birthday_invitation


def test_render_birthday_invitation_respects_enabled_flag(monkeypatch) -> None:
    rendered_calls: list[str] = []

    monkeypatch.setattr(
        birthday_invitation.components,
        "html",
        lambda *_args, **_kwargs: rendered_calls.append("rendered"),
    )

    birthday_invitation.render_birthday_invitation({"enabled": False})

    assert rendered_calls == []


def test_render_birthday_invitation_uses_streamlit_html(monkeypatch) -> None:
    rendered_payloads: list[tuple[str, int, bool]] = []

    monkeypatch.setattr(
        birthday_invitation.components,
        "html",
        lambda html, height, scrolling: rendered_payloads.append(
            (html, height, scrolling)
        ),
    )

    birthday_invitation.render_birthday_invitation(
        {
            "enabled": True,
            "closed_title": "Nueva carta",
            "primary_link_url": "https://example.com/one",
        }
    )

    html, height, scrolling = rendered_payloads[0]

    assert "birthday-invitation-root" in html
    assert height == 1040
    assert scrolling is False


def test_birthday_invitation_serializes_and_escapes_config() -> None:
    html = birthday_invitation.build_birthday_invitation_html(
        {
            "closed_title": "<script>alert(1)</script>",
            "letter_body": ["Hola <strong>Mar</strong>"],
            "primary_link_text": "Ver <opcion>",
            "primary_link_url": "https://example.com/?a=<x>&b=1",
            "secondary_link_text": "No renderizar",
            "secondary_link_url": "javascript:alert(1)",
        }
    )

    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "Hola &lt;strong&gt;Mar&lt;/strong&gt;" in html
    assert "https://example.com/?a=&lt;x&gt;&amp;b=1" in html
    assert "javascript:alert" not in html
    assert 'target="_blank" rel="noopener noreferrer"' in html


def test_birthday_invitation_uses_fallback_body_when_missing() -> None:
    html = birthday_invitation.build_birthday_invitation_html(
        {
            "letter_body": [],
            "primary_link_text": "Ver opcion 1",
            "primary_link_url": "",
            "secondary_link_text": "Ver opcion 2",
            "secondary_link_url": "",
        }
    )

    assert "Tengo una invitacion especial para ti." in html
    assert 'class="birthday-link-button"' not in html


def test_birthday_invitation_open_layout_keeps_letter_in_flow() -> None:
    html = birthday_invitation.build_birthday_invitation_html(
        {
            "letter_body": ["Parrafo uno", "Parrafo dos"],
            "primary_link_text": "Ver opcion 1",
            "primary_link_url": "https://example.com/one",
            "secondary_link_text": "Ver opcion 2",
            "secondary_link_url": "https://example.com/two",
        }
    )

    assert ".birthday-letter-open .birthday-closed-card" in html
    assert "display: none;" in html
    assert "min-height: 920px;" in html
