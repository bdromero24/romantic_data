"""Unit tests for safe Streamlit error boundary helpers."""

from __future__ import annotations

from ui import error_boundary


def test_sanitize_error_message_redacts_sensitive_values() -> None:
    message = (
        "DATABASE_URL=postgresql://user:secret@localhost/app "
        "PASSWORD=hunter2 "
        "C:\\Users\\User\\OneDrive\\Escritorio\\landing_page\\app\\main.py"
    )

    sanitized = error_boundary.sanitize_error_message(message)

    assert "secret" not in sanitized
    assert "hunter2" not in sanitized
    assert "C:\\Users\\User" not in sanitized
    assert "DATABASE_URL=***" in sanitized
    assert "PASSWORD=***" in sanitized
    assert "[local-path]" in sanitized


def test_render_safe_error_message_exposes_no_technical_details(monkeypatch) -> None:
    markdown_calls: list[tuple[str, bool | None]] = []

    monkeypatch.setattr(
        error_boundary.st,
        "markdown",
        lambda html, unsafe_allow_html=None: markdown_calls.append(
            (html, unsafe_allow_html)
        ),
    )

    error_boundary.render_safe_error_message()

    rendered_html, unsafe_allow_html = markdown_calls[0]
    assert unsafe_allow_html is True
    assert "Oops... Algo fall&oacute;. Contacta al administrador." in rendered_html
    assert "Traceback" not in rendered_html
    assert "DATABASE_URL" not in rendered_html
    assert "C:\\Users" not in rendered_html


def test_log_app_exception_writes_sanitized_traceback(monkeypatch) -> None:
    logged_errors: list[dict[str, str | None]] = []

    def fake_log_critical_error(
        error_type: str,
        error_message: str,
        module_name: str | None = None,
        function_name: str | None = None,
        write_to_db: bool = True,
    ) -> None:
        logged_errors.append(
            {
                "error_type": error_type,
                "error_message": error_message,
                "module_name": module_name,
                "function_name": function_name,
            }
        )

    monkeypatch.setattr(
        error_boundary,
        "log_critical_error",
        fake_log_critical_error,
    )

    try:
        raise RuntimeError("DATABASE_URL=postgresql://user:secret@localhost/app")
    except RuntimeError as error:
        error_boundary.log_app_exception(error, context="test.context")

    assert logged_errors[0]["error_type"] == "RuntimeError"
    assert "test.context" in str(logged_errors[0]["error_message"])
    assert "Traceback" in str(logged_errors[0]["error_message"])
    assert "secret" not in str(logged_errors[0]["error_message"])
