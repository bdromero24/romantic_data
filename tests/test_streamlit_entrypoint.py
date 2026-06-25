"""Unit tests for the Streamlit entrypoint bootstrap."""

import sys
from pathlib import Path

from app import main as app_main
from app.main import ensure_project_root_on_path


def test_ensure_project_root_on_path_restores_project_imports(
    monkeypatch,
) -> None:
    project_root = str(Path(__file__).resolve().parents[1])
    filtered_path = [path for path in sys.path if path != project_root]
    monkeypatch.setattr(sys, "path", filtered_path)

    ensure_project_root_on_path()

    assert sys.path[0] == project_root


def test_main_uses_safe_error_boundary(monkeypatch) -> None:
    handled_errors: list[tuple[str, str]] = []
    rendered_errors: list[str] = []

    def broken_run_app() -> None:
        raise RuntimeError("DATABASE_URL=postgresql://user:secret@localhost/app")

    monkeypatch.setattr(app_main, "run_app", broken_run_app)
    monkeypatch.setattr(
        app_main,
        "log_app_exception",
        lambda error, context=None: handled_errors.append(
            (type(error).__name__, context or "")
        ),
    )
    monkeypatch.setattr(
        app_main,
        "render_safe_error_message",
        lambda: rendered_errors.append("rendered"),
    )

    app_main.main()

    assert handled_errors == [("RuntimeError", "app.main")]
    assert rendered_errors == ["rendered"]


def test_run_app_skips_featured_quotes_section_when_empty(monkeypatch) -> None:
    section_titles: list[str] = []
    quote_calls: list[list[dict[str, str]]] = []

    monkeypatch.setattr(app_main.st, "set_page_config", lambda **_kwargs: None)
    monkeypatch.setattr(app_main.st, "markdown", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        app_main,
        "get_romantic_landing_metrics",
        lambda: {
            "hero": {},
            "summary_cards": [],
            "conversation_starter": {},
            "rhythm": {},
            "special_message": {},
            "timeline": [],
            "featured_messages": [],
            "words": [],
        },
    )
    monkeypatch.setattr(app_main, "render_hero", lambda _hero: None)
    monkeypatch.setattr(app_main, "render_metric_cards", lambda _cards: None)
    monkeypatch.setattr(
        app_main,
        "render_conversation_starter",
        lambda _starter: None,
    )
    monkeypatch.setattr(app_main, "render_rhythm_charts", lambda _rhythm: None)
    monkeypatch.setattr(
        app_main,
        "render_special_message",
        lambda _message: None,
    )
    monkeypatch.setattr(app_main, "render_timeline", lambda _timeline: None)
    monkeypatch.setattr(app_main, "render_words", lambda _words: None)
    monkeypatch.setattr(app_main, "render_closing", lambda: None)
    monkeypatch.setattr(app_main, "render_reveal_observer", lambda: None)
    monkeypatch.setattr(
        app_main,
        "render_section_header",
        lambda kicker, title, copy: section_titles.append(title),
    )
    monkeypatch.setattr(
        app_main,
        "render_quotes",
        lambda messages: quote_calls.append(messages),
    )

    app_main.run_app()

    assert app_main.ROMANTIC_CONTENT["featured_quotes"]["title"] not in section_titles
    assert quote_calls == []
