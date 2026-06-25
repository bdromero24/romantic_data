"""Unit tests for ETL staging artifacts."""

from datetime import datetime, timezone

import pytest

from etl import artifacts


def test_ensure_directory_creates_staging_directory(tmp_path) -> None:
    directory = tmp_path / "data" / "staging" / "extracted"

    result = artifacts.ensure_directory(directory)

    assert result == directory
    assert directory.exists()


def test_build_artifact_path_uses_stage_source_and_format(monkeypatch) -> None:
    monkeypatch.setattr(artifacts, "STAGING_ROOT", artifacts.Path("custom"))

    path = artifacts.build_artifact_path(
        stage="extracted",
        source="Instagram Meta",
        file_format="parquet",
    )

    assert path.parent == artifacts.Path("custom") / "extracted"
    assert path.name.startswith("extracted_instagram_meta_")
    assert path.suffix == ".parquet"


def test_save_and_load_records_from_parquet_preserves_columns_and_timestamps(
    tmp_path,
) -> None:
    timestamp = datetime(2026, 5, 29, 19, 30, tzinfo=timezone.utc)
    records = [
        {
            "sender": "Alice",
            "message": "Hola",
            "message_normalized": "hola",
            "timestamp": timestamp,
            "source": "instagram",
        }
    ]
    path = tmp_path / "records.parquet"

    saved_path = artifacts.save_records(records, path)
    loaded_records = artifacts.load_records(saved_path)

    assert saved_path == path
    assert set(loaded_records[0]) == set(records[0])
    assert loaded_records[0]["timestamp"].to_pydatetime() == timestamp


def test_save_and_load_records_from_csv(tmp_path) -> None:
    records = [
        {
            "sender": "Bob",
            "message": "Hola",
            "message_normalized": "hola",
            "timestamp": "2026-05-29T19:30:00+00:00",
            "source": "whatsapp",
        }
    ]
    path = tmp_path / "records.csv"

    artifacts.save_records(records, path)
    loaded_records = artifacts.load_records(path)

    assert loaded_records == records


def test_save_stage_output_uses_conventional_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(artifacts, "STAGING_ROOT", tmp_path / "staging")
    records = [{"sender": "Alice", "timestamp": "2026", "source": "instagram"}]

    saved_path = artifacts.save_stage_output(
        records=records,
        stage="transformed",
        source="instagram",
        file_format="csv",
    )

    assert saved_path.parent == tmp_path / "staging" / "transformed"
    assert saved_path.exists()


def test_empty_record_list_fails_clearly(tmp_path) -> None:
    with pytest.raises(ValueError, match="empty ETL artifact"):
        artifacts.save_records([], tmp_path / "empty.parquet")


def test_artifact_errors_are_logged_and_reraised(monkeypatch, tmp_path) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        artifacts,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )
    monkeypatch.setattr(
        artifacts.pd,
        "read_parquet",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("failure")),
    )
    path = tmp_path / "broken.parquet"
    path.write_bytes(b"not parquet")

    with pytest.raises(RuntimeError, match="failure"):
        artifacts.load_records(path)

    assert logged_errors == ["RuntimeError"]


def test_unsupported_stage_and_format_fail_clearly() -> None:
    with pytest.raises(ValueError, match="Unsupported ETL artifact stage"):
        artifacts.build_artifact_path("raw", "instagram")

    with pytest.raises(ValueError, match="Unsupported ETL artifact file format"):
        artifacts.build_artifact_path("extracted", "instagram", "json")
