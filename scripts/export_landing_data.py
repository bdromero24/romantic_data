"""Export romantic landing data to a static JSON file."""

from __future__ import annotations

import json
import sys
import traceback
from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "final" / "landing_data.json"


def ensure_project_root_on_path() -> None:
    """Allow running this script directly from any working directory."""
    project_root_text = str(PROJECT_ROOT)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)


ensure_project_root_on_path()

from logger.logger import log_critical_error
from services.romantic_metrics import get_romantic_landing_metrics


def make_json_serializable(value: Any) -> Any:
    """Convert common metric values into JSON-serializable values."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (date, time)):
        return value.isoformat()
    if isinstance(value, dict):
        return {
            str(key): make_json_serializable(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple, set)):
        return [make_json_serializable(item) for item in value]

    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except (TypeError, ValueError):
            pass

    if hasattr(value, "item"):
        try:
            return make_json_serializable(value.item())
        except (TypeError, ValueError):
            pass

    return str(value)


def export_landing_data(output_path: Path = OUTPUT_PATH) -> Path:
    """Build and write the complete static landing data JSON file."""
    landing_data = get_romantic_landing_metrics()
    serializable_landing_data = make_json_serializable(landing_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(
            serializable_landing_data,
            output_file,
            ensure_ascii=False,
            indent=2,
        )
        output_file.write("\n")

    return output_path


def main() -> None:
    """Export frozen landing data for Streamlit Community Cloud."""
    try:
        output_path = export_landing_data()
    except Exception as error:
        log_critical_error(
            error_type=type(error).__name__,
            error_message=str(error),
            module_name=__name__,
            function_name="main",
        )
        print(f"Failed to export static landing data: {error}", file=sys.stderr)
        traceback.print_exc()
        raise

    relative_output_path = output_path.relative_to(PROJECT_ROOT)
    print(f"Static landing data exported to {relative_output_path.as_posix()}")


if __name__ == "__main__":
    main()
