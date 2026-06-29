"""Static landing data loader for Streamlit Cloud deployments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATIC_LANDING_DATA_PATH = PROJECT_ROOT / "data" / "final" / "landing_data.json"
MISSING_STATIC_DATA_MESSAGE = (
    "Static landing data file not found. "
    "Run: python scripts/export_landing_data.py"
)


def _resolve_static_data_path(path: str | None = None) -> Path:
    if path is None:
        return DEFAULT_STATIC_LANDING_DATA_PATH

    candidate_path = Path(path)
    if candidate_path.is_absolute():
        return candidate_path

    return PROJECT_ROOT / candidate_path


def load_static_landing_data(path: str | None = None) -> dict[str, Any]:
    """Load frozen landing data from JSON."""
    static_data_path = _resolve_static_data_path(path)
    if not static_data_path.is_file():
        raise FileNotFoundError(MISSING_STATIC_DATA_MESSAGE)

    with static_data_path.open("r", encoding="utf-8") as static_data_file:
        landing_data = json.load(static_data_file)

    if not isinstance(landing_data, dict):
        raise ValueError("Static landing data must be a JSON object.")

    return landing_data
