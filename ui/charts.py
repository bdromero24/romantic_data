"""Chart helpers for the romantic Streamlit landing."""

from __future__ import annotations

from typing import Any, Protocol

import altair as alt
import pandas as pd
import streamlit as st

from app.chart_config import CHARTS_MAX_DATE


ROMANTIC_COLORS = {
    "bg": "#fff0f8",
    "surface": "rgba(255,240,248,0.42)",
    "pink_soft": "#ffb3d9",
    "pink": "#ff5fb7",
    "fuchsia": "#d41472",
    "fuchsia_deep": "#a90058",
    "text": "#3f2435",
    "muted": "#8a5872",
    "grid": "rgba(212,20,114,0.14)",
    "zero": "rgba(212,20,114,0.16)",
}

ROMANTIC_SCALE = alt.Scale(
    range=[
        ROMANTIC_COLORS["pink_soft"],
        ROMANTIC_COLORS["pink"],
        ROMANTIC_COLORS["fuchsia"],
        ROMANTIC_COLORS["fuchsia_deep"],
    ]
)


class PlotlyFigure(Protocol):
    """Minimal Plotly figure protocol used for optional theme application."""

    def update_layout(self, *args: Any, **kwargs: Any) -> Any:
        """Update Plotly layout."""

    def update_xaxes(self, *args: Any, **kwargs: Any) -> Any:
        """Update Plotly x axes."""

    def update_yaxes(self, *args: Any, **kwargs: Any) -> Any:
        """Update Plotly y axes."""


def render_rhythm_charts(rhythm: dict[str, list[dict[str, Any]]]) -> None:
    """Render soft rhythm charts for hours, weekdays, and months."""
    st.markdown('<section class="chart-grid">', unsafe_allow_html=True)
    _render_chart_card(
        title="Nuestra hora favorita para hablar",
        rows=rhythm.get("hours", []),
        reveal_delay=0,
    )
    _render_chart_card(
        title="Los dias donde mas nos encontramos",
        rows=rhythm.get("weekdays", []),
        reveal_delay=90,
    )
    st.markdown("</section>", unsafe_allow_html=True)

    _render_chart_card(
        title="Como fue creciendo nuestra historia mes a mes",
        rows=rhythm.get("months", []),
        chart_type="time_series",
        reveal_delay=0,
    )
    _render_chart_card(
        title="Cuanto escribio cada uno",
        rows=rhythm.get("senders", []),
        chart_type="pie",
        reveal_delay=90,
    )


def _render_chart_card(
    title: str,
    rows: list[dict[str, Any]],
    chart_type: str = "bar",
    reveal_delay: int = 0,
) -> None:
    st.markdown(
        (
            '<article class="chart-card reveal-on-scroll" '
            f'style="--reveal-delay: {reveal_delay}ms;">'
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h3 class="chart-title">{title}</h3>',
        unsafe_allow_html=True,
    )

    if not rows:
        st.info("Este recuerdo aparecera cuando haya mensajes cargados.")
        st.markdown("</article>", unsafe_allow_html=True)
        return

    if chart_type == "time_series":
        chart = _build_time_series_chart(rows)
    elif chart_type == "pie":
        chart = _build_sender_pie_chart(rows)
    else:
        chart = _build_bar_chart(rows)

    st.altair_chart(chart, use_container_width=True)
    st.markdown("</article>", unsafe_allow_html=True)


def _build_bar_chart(rows: list[dict[str, Any]]) -> alt.Chart:
    data = pd.DataFrame(rows)
    chart = (
        alt.Chart(data)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("label:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("value:Q", title=None),
            color=alt.Color("value:Q", scale=ROMANTIC_SCALE, legend=None),
            tooltip=[
                alt.Tooltip("label:N", title="Momento"),
                alt.Tooltip("value:Q", title="Mensajes"),
            ],
        )
        .properties(height=260)
    )

    return apply_altair_romantic_theme(chart)


def _build_time_series_chart(rows: list[dict[str, Any]]) -> alt.Chart:
    data = pd.DataFrame(rows).copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"])

    if CHARTS_MAX_DATE is not None:
        max_date = _coerce_chart_max_date(data["date"], CHARTS_MAX_DATE)
        data = data[data["date"] <= max_date]

    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["value"])
    data["month"] = data["date"].dt.to_period("M").dt.to_timestamp()
    data = (
        data.groupby("month", as_index=False)["value"]
        .sum()
        .sort_values("month")
    )
    data["month_label"] = data["month"].dt.strftime("%m/%Y")

    chart = (
        alt.Chart(data)
        .mark_line(point=True, color=ROMANTIC_COLORS["fuchsia"], strokeWidth=4)
        .encode(
            x=alt.X(
                "month_label:N",
                title=None,
                sort=list(data["month_label"]),
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y("value:Q", title=None),
            tooltip=[
                alt.Tooltip("month_label:N", title="Mes"),
                alt.Tooltip("value:Q", title="Mensajes"),
            ],
        )
        .properties(height=280)
    )

    return apply_altair_romantic_theme(chart)


def _coerce_chart_max_date(
    dates: pd.Series,
    max_date_value: str,
) -> pd.Timestamp:
    max_date = pd.to_datetime(max_date_value)
    timezone = getattr(dates.dt, "tz", None)
    if timezone is not None and max_date.tzinfo is None:
        return max_date.tz_localize(timezone)

    return max_date


def _build_sender_pie_chart(rows: list[dict[str, Any]]) -> alt.LayerChart:
    data = pd.DataFrame(rows).copy()

    if "sender" in data.columns and "label" not in data.columns:
        data = data.rename(columns={"sender": "label"})

    if "total_messages" in data.columns and "value" not in data.columns:
        data = data.rename(columns={"total_messages": "value"})

    if "label" not in data.columns or "value" not in data.columns:
        return _build_empty_pie_chart()

    data = data[["label", "value"]].dropna()
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["value"])
    data = data[data["value"] > 0]

    total_messages = data["value"].sum()
    if total_messages <= 0:
        return _build_empty_pie_chart()

    data["percentage"] = data["value"] / total_messages

    base = alt.Chart(data).encode(
        theta=alt.Theta("value:Q", stack=True),
        color=alt.Color(
            "label:N",
            scale=ROMANTIC_SCALE,
            legend=alt.Legend(
                title=None,
                orient="bottom",
                labelColor=ROMANTIC_COLORS["text"],
                labelFont="Nunito, Inter, system-ui, sans-serif",
                labelFontSize=14,
                labelFontWeight="bold",
                symbolSize=140,
            ),
        ),
        tooltip=[
            alt.Tooltip("label:N", title="Persona"),
            alt.Tooltip("value:Q", title="Mensajes", format=","),
            alt.Tooltip("percentage:Q", title="Porcentaje", format=".1%"),
        ],
    )

    pie = base.mark_arc(
        innerRadius=58,
        outerRadius=120,
        cornerRadius=5,
        stroke=ROMANTIC_COLORS["bg"],
        strokeWidth=3,
    )

    percentage_labels = base.mark_text(
        radius=96,
        font="Nunito, Inter, system-ui, sans-serif",
        fontSize=16,
        fontWeight="bold",
        color=ROMANTIC_COLORS["text"],
    ).encode(
        text=alt.Text("percentage:Q", format=".1%"),
        tooltip=[
            alt.Tooltip("label:N", title="Persona"),
            alt.Tooltip("value:Q", title="Mensajes", format=","),
            alt.Tooltip("percentage:Q", title="Porcentaje", format=".1%"),
        ],
    )

    chart = (pie + percentage_labels).properties(height=310)

    return apply_altair_romantic_theme(chart)


def _build_empty_pie_chart() -> alt.LayerChart:
    data = pd.DataFrame([{"label": "Sin mensajes", "value": 1}])
    base = alt.Chart(data)
    ring = base.mark_arc(
        innerRadius=58,
        outerRadius=120,
        color=ROMANTIC_COLORS["pink_soft"],
        opacity=0.35,
    ).encode(theta=alt.Theta("value:Q"))
    label = base.mark_text(
        font="Nunito, Inter, system-ui, sans-serif",
        fontSize=15,
        fontWeight="bold",
        color=ROMANTIC_COLORS["muted"],
    ).encode(text=alt.value("Sin mensajes"))

    return apply_altair_romantic_theme((ring + label).properties(height=310))


def apply_altair_romantic_theme(chart: alt.Chart) -> alt.Chart:
    """Apply the romantic visual system to an Altair chart."""
    return (
        chart.configure(
            background="transparent",
            font="Nunito, Inter, system-ui, sans-serif",
        )
        .configure_axis(
            gridColor=ROMANTIC_COLORS["grid"],
            labelColor=ROMANTIC_COLORS["muted"],
            labelFontWeight="bold",
            titleColor=ROMANTIC_COLORS["text"],
            titleFontWeight="bold",
            tickColor="rgba(212,20,114,0.22)",
            domainColor="rgba(212,20,114,0.20)",
            labelFont="Nunito, Inter, system-ui, sans-serif",
            labelFontSize=13,
            titleFont="Nunito, Inter, system-ui, sans-serif",
            titleFontSize=15,
        )
        .configure_view(strokeWidth=0)
    )


def apply_plotly_romantic_theme(fig: PlotlyFigure) -> PlotlyFigure:
    """Apply the romantic visual system to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=ROMANTIC_COLORS["surface"],
        font={
            "color": ROMANTIC_COLORS["text"],
            "family": "Nunito, Inter, system-ui, sans-serif",
            "size": 14,
        },
        margin={"l": 20, "r": 20, "t": 48, "b": 24},
    )
    fig.update_xaxes(
        gridcolor=ROMANTIC_COLORS["grid"],
        zerolinecolor=ROMANTIC_COLORS["zero"],
        tickfont={
            "color": ROMANTIC_COLORS["muted"],
            "family": "Nunito, Inter, system-ui, sans-serif",
            "size": 13,
        },
        title_font={
            "color": ROMANTIC_COLORS["text"],
            "family": "Nunito, Inter, system-ui, sans-serif",
            "size": 15,
        },
    )
    fig.update_yaxes(
        gridcolor=ROMANTIC_COLORS["grid"],
        zerolinecolor=ROMANTIC_COLORS["zero"],
        tickfont={
            "color": ROMANTIC_COLORS["muted"],
            "family": "Nunito, Inter, system-ui, sans-serif",
            "size": 13,
        },
        title_font={
            "color": ROMANTIC_COLORS["text"],
            "family": "Nunito, Inter, system-ui, sans-serif",
            "size": 15,
        },
    )

    return fig
