"""Safe Streamlit error boundary helpers."""

from __future__ import annotations

import re
import traceback

import streamlit as st

from logger.logger import log_critical_error


SAFE_ERROR_TEXT = "Oops... Algo fall&oacute;. Contacta al administrador."


def sanitize_error_message(message: str) -> str:
    """Redact sensitive values from messages used outside the UI."""
    redacted = re.sub(
        r"postgresql(?:\+psycopg2)?://[^:\s]+:[^@\s]+@",
        "postgresql://***:***@",
        message,
        flags=re.IGNORECASE,
    )
    redacted = re.sub(
        r"(?i)\b(PASSWORD|DATABASE_URL|PGPASSWORD|SECRET|TOKEN)\s*=\s*[^\s]+",
        r"\1=***",
        redacted,
    )
    redacted = re.sub(
        r"[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)+[^\\/:*?\"<>|\r\n]*",
        "[local-path]",
        redacted,
    )

    return redacted


def log_app_exception(error: BaseException, context: str | None = None) -> None:
    """Log complete app exceptions without exposing details in Streamlit UI."""
    traceback_text = "".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    )
    message = (
        f"context={context or 'unknown'} | "
        f"message={error} | "
        f"traceback={traceback_text}"
    )
    log_critical_error(
        error_type=type(error).__name__,
        error_message=sanitize_error_message(message),
        module_name=__name__,
        function_name="log_app_exception",
    )


def render_safe_error_message() -> None:
    """Render a generic error message with no technical details."""
    st.markdown(
        """
        <section class="safe-error-card">
          <h1>Oops... Algo fall&oacute;. Contacta al administrador.</h1>
        </section>
        """,
        unsafe_allow_html=True,
    )
