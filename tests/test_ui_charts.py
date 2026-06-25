"""Unit tests for romantic chart helpers."""

from datetime import datetime

from ui import charts
from ui.charts import apply_plotly_romantic_theme


def test_apply_plotly_romantic_theme_updates_figure() -> None:
    figure = _FakePlotlyFigure()

    result = apply_plotly_romantic_theme(figure)

    assert result is figure
    assert figure.layout_updates[0]["paper_bgcolor"] == "rgba(0,0,0,0)"
    assert figure.layout_updates[0]["font"]["color"] == "#3f2435"
    assert figure.layout_updates[0]["font"]["size"] == 14
    assert figure.xaxis_updates[0]["gridcolor"] == "rgba(212,20,114,0.14)"
    assert figure.xaxis_updates[0]["tickfont"]["size"] == 13
    assert figure.yaxis_updates[0]["zerolinecolor"] == "rgba(212,20,114,0.16)"
    assert figure.yaxis_updates[0]["title_font"]["size"] == 15


def test_time_series_chart_groups_by_month_and_discards_invalid_future_dates() -> None:
    rows = [
        {"label": "05/2026", "date": datetime(2026, 5, 1), "value": 10},
        {"label": "05/2026", "date": datetime(2026, 5, 15), "value": 5},
        {"label": "06/2026", "date": datetime(2026, 6, 1), "value": 20},
        {"label": "Invalido", "date": "sin-fecha", "value": 30},
    ]

    chart = charts._build_time_series_chart(rows)
    values = chart.to_dict()["datasets"]
    dataset = next(iter(values.values()))

    assert len(dataset) == 1
    assert dataset[0]["month_label"] == "05/2026"
    assert dataset[0]["value"] == 15


def test_sender_pie_chart_normalizes_columns_and_percentages() -> None:
    rows = [
        {"sender": "Mar", "total_messages": 75},
        {"sender": "David", "total_messages": 25},
    ]

    chart = charts._build_sender_pie_chart(rows)
    values = chart.to_dict()["datasets"]
    dataset = next(iter(values.values()))

    assert dataset[0]["label"] == "Mar"
    assert dataset[0]["value"] == 75
    assert dataset[0]["percentage"] == 0.75
    assert dataset[1]["percentage"] == 0.25


class _FakePlotlyFigure:
    def __init__(self) -> None:
        self.layout_updates: list[dict] = []
        self.xaxis_updates: list[dict] = []
        self.yaxis_updates: list[dict] = []

    def update_layout(self, **kwargs) -> None:
        self.layout_updates.append(kwargs)

    def update_xaxes(self, **kwargs) -> None:
        self.xaxis_updates.append(kwargs)

    def update_yaxes(self, **kwargs) -> None:
        self.yaxis_updates.append(kwargs)
