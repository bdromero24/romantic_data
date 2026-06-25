"""Streamlit romantic landing entrypoint."""

from __future__ import annotations

import sys
from pathlib import Path
import streamlit as st


def ensure_project_root_on_path() -> None:
    """Allow Streamlit to run this file directly from the app directory."""
    project_root = Path(__file__).resolve().parents[1]
    project_root_text = str(project_root)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)


ensure_project_root_on_path()

from app.content_config import ROMANTIC_CONTENT
from services.romantic_metrics import get_romantic_landing_metrics
from ui.charts import render_rhythm_charts
from ui.components import (
    render_closing,
    render_conversation_starter,
    render_hero,
    render_metric_cards,
    render_quotes,
    render_reveal_observer,
    render_section_header,
    render_special_message,
    render_timeline,
    render_words,
)
from ui.error_boundary import log_app_exception, render_safe_error_message
from ui.styles import CUSTOM_CSS


def run_app() -> None:
    """Render the romantic Streamlit landing."""
    st.set_page_config(
        page_title="Nuestra historia",
        page_icon=":heart:",
        layout="wide",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    landing_data = get_romantic_landing_metrics()

    render_hero(landing_data["hero"])
    render_section_header(
        kicker="Nuestra historia en numeros",
        title="Pequeños datos bonitos",
        copy="Recuerdos de todo lo que hemos compartido.",
    )
    render_metric_cards(landing_data["summary_cards"])
    render_conversation_starter(landing_data["conversation_starter"])

    render_section_header(
        kicker="Nuestro ritmo",
        title="Cuando mas nos encontramos",
        copy="Horas, dias y meses donde nuestras conversaciones tuvieron mas vida.",
    )
    render_rhythm_charts(landing_data["rhythm"])

    render_section_header(
        kicker="Frases bonitas",
        title=ROMANTIC_CONTENT["special_message"]["title"],
        copy="Me gusta saber lo que sientes.",
    )
    render_special_message(landing_data["special_message"])

    render_section_header(
        kicker="Momentos",
        title="Lo que marco nuestra historia",
        copy="Una linea de tiempo con primeras veces, dias intensos y mensajes que se quedaron.",
    )
    render_timeline(landing_data["timeline"])

    if landing_data["featured_messages"]:
        render_section_header(
            kicker="Frases bonitas",
            title=ROMANTIC_CONTENT["featured_quotes"]["title"],
            copy="Mensajes que no quiero olvidar...",
        )
        render_quotes(landing_data["featured_messages"])

    render_section_header(
        kicker="Nuestro lenguaje",
        title="Las palabras que mas nos representan",
        copy="Palabras pequeñas que aparecen muchas veces porque tambien hacen parte de nosotros.",
    )
    render_words(landing_data["words"])
    render_closing()
    render_reveal_observer()


def main() -> None:
    """Run the landing inside a safe Streamlit error boundary."""
    try:
        run_app()
    except Exception as error:
        log_app_exception(error, context="app.main")
        render_safe_error_message()


if __name__ == "__main__":
    main()
