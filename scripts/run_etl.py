"""Manual ETL runner for supported conversation export files."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable

from etl.artifacts import save_stage_output
from etl.extract.extract_dispatcher import extract_messages
from etl.load import load_messages
from etl.transform import transform_messages
from logger.logger import log_critical_error


SUPPORTED_ARTIFACT_FORMATS = ("parquet", "csv")


def run_etl(
    input_paths: Iterable[str | Path],
    save_artifacts: bool = False,
    artifact_format: str = "parquet",
) -> dict[str, Any]:
    """Extract, transform, and load messages from supported export files."""
    try:
        paths = _validate_input_paths(input_paths)
        file_summaries: list[dict[str, Any]] = []
        transformed_records: list[dict[str, Any]] = []

        for input_path in paths:
            extracted = extract_messages(input_path)
            transformed = transform_messages(extracted)
            source = _get_source_name(transformed, input_path)

            summary: dict[str, Any] = {
                "path": str(input_path),
                "source": source,
                "extracted": len(extracted),
                "transformed": len(transformed),
            }

            if save_artifacts:
                summary["extracted_artifact"] = str(
                    save_stage_output(
                        extracted,
                        stage="extracted",
                        source=source,
                        file_format=artifact_format,
                    )
                )
                summary["transformed_artifact"] = str(
                    save_stage_output(
                        transformed,
                        stage="transformed",
                        source=source,
                        file_format=artifact_format,
                    )
                )

            file_summaries.append(summary)
            transformed_records.extend(transformed)

        load_summary = load_messages(transformed_records)
        return {
            "files": file_summaries,
            "load": load_summary,
        }
    except Exception as error:
        _log_run_etl_error(type(error).__name__, error, "run_etl")
        raise


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for the manual ETL runner."""
    parser = argparse.ArgumentParser(
        description="Extract, transform, and load conversation exports.",
    )
    parser.add_argument(
        "input_paths",
        nargs="+",
        help="Supported Instagram or WhatsApp export files.",
    )
    parser.add_argument(
        "--save-artifacts",
        action="store_true",
        help="Save extracted and transformed staging artifacts.",
    )
    parser.add_argument(
        "--artifact-format",
        choices=SUPPORTED_ARTIFACT_FORMATS,
        default="parquet",
        help="Artifact format used when --save-artifacts is enabled.",
    )
    return parser


def main() -> None:
    """Run ETL from command-line arguments and print a summary."""
    parser = build_argument_parser()
    arguments = parser.parse_args()
    summary = run_etl(
        input_paths=arguments.input_paths,
        save_artifacts=arguments.save_artifacts,
        artifact_format=arguments.artifact_format,
    )
    print(summary)


def _validate_input_paths(input_paths: Iterable[str | Path]) -> list[Path]:
    paths = [Path(input_path) for input_path in input_paths]
    if not paths:
        raise ValueError("At least one input path is required.")

    return paths


def _get_source_name(records: list[dict[str, Any]], input_path: Path) -> str:
    if not records:
        raise ValueError(f"No transformed records produced for: {input_path}")

    source = records[0].get("source")
    if not isinstance(source, str) or not source.strip():
        raise ValueError(f"Transformed records are missing source: {input_path}")

    return source.strip()


def _log_run_etl_error(
    error_type: str,
    error: Exception,
    function_name: str,
) -> None:
    log_critical_error(
        error_type=error_type,
        error_message=str(error),
        module_name=__name__,
        function_name=function_name,
    )


if __name__ == "__main__":
    main()
