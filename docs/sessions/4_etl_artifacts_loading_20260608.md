# Session 4 - ETL Artifacts and Loading

## Objective

Add a focused ETL staging artifact layer and implement PostgreSQL loading for already transformed message records.

## Implemented

- Created `etl/artifacts.py`.
- Added staging artifact helpers:
  - `ensure_directory()`
  - `build_artifact_path()`
  - `save_records()`
  - `load_records()`
  - `save_stage_output()`
- Added Parquet staging support with `pandas` and `pyarrow`.
- Added explicit CSV artifact fallback.
- Added `pyarrow` to `requirements.txt`.
- Implemented `etl/load.py` for transformed records only.
- Added parameterized `INSERT_MESSAGE_QUERY` to `db/queries.py`.
- Used `ON CONFLICT DO NOTHING` to skip duplicate messages safely.
- Added a staged-artifact wrapper in `etl/load.py` while keeping artifact persistence separate from database loading.
- Added focused unit tests for artifacts and loading without requiring PostgreSQL.

## Artifact Conventions

Extracted stage artifacts:

```text
data/staging/extracted/
```

Transformed stage artifacts:

```text
data/staging/transformed/
```

Preferred format:

```text
parquet
```

CSV fallback:

```text
csv
```

## Commands

Run tests:

```powershell
.\venv\Scripts\python.exe -m pytest tests/
```

Run extraction:

```powershell
python -c "from etl.extract.extract_dispatcher import extract_messages; print(extract_messages('data/raw/ig_message_1.json'))"
```

Run transformation:

```powershell
python -c "from etl.extract.extract_dispatcher import extract_messages; from etl.transform import transform_messages; print(transform_messages(extract_messages('data/raw/ig_message_1.json')))"
```

Save extracted output:

```powershell
python -c "from etl.extract.extract_dispatcher import extract_messages; from etl.artifacts import save_stage_output; records = extract_messages('data/raw/ig_message_1.json'); print(save_stage_output(records, stage='extracted', source='instagram'))"
```

Save transformed output:

```powershell
python -c "from etl.extract.extract_dispatcher import extract_messages; from etl.transform import transform_messages; from etl.artifacts import save_stage_output; extracted = extract_messages('data/raw/ig_message_1.json'); transformed = transform_messages(extracted); print(save_stage_output(transformed, stage='transformed', source='instagram'))"
```

Load transformed staged records:

```powershell
python -c "from etl.artifacts import load_records; from etl.load import load_messages; records = load_records('data/staging/transformed/transformed_instagram_YYYYMMDD_HHMMSS.parquet'); print(load_messages(records))"
```

## Verification

```text
46 passed in 3.02s
```
