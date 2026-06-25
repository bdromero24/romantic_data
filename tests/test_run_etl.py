"""Unit tests for the manual ETL runner."""

from pathlib import Path

import pytest

from scripts import run_etl


def test_run_etl_extracts_transforms_and_loads(monkeypatch) -> None:
    extracted = [
        {
            "sender": "Alice",
            "message": "Hola",
            "timestamp": "raw",
            "source": "whatsapp",
        }
    ]
    transformed = [
        {
            "sender": "Alice",
            "message": "Hola",
            "message_normalized": "hola",
            "timestamp": "parsed",
            "source": "whatsapp",
        }
    ]
    calls: list[tuple] = []

    monkeypatch.setattr(
        run_etl,
        "extract_messages",
        lambda path: calls.append(("extract", path)) or extracted,
    )
    monkeypatch.setattr(
        run_etl,
        "transform_messages",
        lambda records: calls.append(("transform", records)) or transformed,
    )
    monkeypatch.setattr(
        run_etl,
        "load_messages",
        lambda records: calls.append(("load", records))
        or {"received": 1, "inserted": 1, "skipped_duplicates": 0},
    )

    summary = run_etl.run_etl(["chat.txt"])

    assert summary == {
        "files": [
            {
                "path": "chat.txt",
                "source": "whatsapp",
                "extracted": 1,
                "transformed": 1,
            }
        ],
        "load": {"received": 1, "inserted": 1, "skipped_duplicates": 0},
    }
    assert calls == [
        ("extract", Path("chat.txt")),
        ("transform", extracted),
        ("load", transformed),
    ]


def test_run_etl_saves_artifacts_when_enabled(monkeypatch) -> None:
    extracted = [{"source": "instagram"}]
    transformed = [{"source": "instagram"}]
    artifact_calls: list[tuple] = []

    monkeypatch.setattr(run_etl, "extract_messages", lambda path: extracted)
    monkeypatch.setattr(run_etl, "transform_messages", lambda records: transformed)
    monkeypatch.setattr(
        run_etl,
        "save_stage_output",
        lambda records, stage, source, file_format: artifact_calls.append(
            (records, stage, source, file_format)
        )
        or Path(f"data/staging/{stage}/{stage}_{source}.csv"),
    )
    monkeypatch.setattr(
        run_etl,
        "load_messages",
        lambda records: {"received": 1, "inserted": 1, "skipped_duplicates": 0},
    )

    summary = run_etl.run_etl(
        ["instagram_messages.json"],
        save_artifacts=True,
        artifact_format="csv",
    )

    assert artifact_calls == [
        (extracted, "extracted", "instagram", "csv"),
        (transformed, "transformed", "instagram", "csv"),
    ]
    assert summary["files"][0]["extracted_artifact"].endswith(
        "extracted_instagram.csv"
    )
    assert summary["files"][0]["transformed_artifact"].endswith(
        "transformed_instagram.csv"
    )


def test_run_etl_rejects_empty_input_paths(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        run_etl,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(ValueError, match="At least one input path"):
        run_etl.run_etl([])

    assert logged_errors == ["ValueError"]


def test_run_etl_rejects_empty_transformed_records(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(run_etl, "extract_messages", lambda path: [{"source": "x"}])
    monkeypatch.setattr(run_etl, "transform_messages", lambda records: [])
    monkeypatch.setattr(
        run_etl,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(ValueError, match="No transformed records"):
        run_etl.run_etl(["empty.json"])

    assert logged_errors == ["ValueError"]


def test_main_prints_summary(monkeypatch, capsys) -> None:
    parser_arguments = ["run_etl.py", "chat.txt", "--save-artifacts"]
    monkeypatch.setattr("sys.argv", parser_arguments)
    monkeypatch.setattr(
        run_etl,
        "run_etl",
        lambda input_paths, save_artifacts, artifact_format: {
            "input_paths": input_paths,
            "save_artifacts": save_artifacts,
            "artifact_format": artifact_format,
        },
    )

    run_etl.main()

    output = capsys.readouterr().out
    assert "'input_paths': ['chat.txt']" in output
    assert "'save_artifacts': True" in output
    assert "'artifact_format': 'parquet'" in output
