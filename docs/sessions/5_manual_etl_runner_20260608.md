# Manual ETL Runner Session

## Objective

Add a backend-only manual runner that orchestrates existing ETL stages without moving extraction, transformation, artifact, loading, or database read logic out of their modules.

## Changes

- Created `scripts/run_etl.py`.
- Added `run_etl()` for reusable orchestration over one or more input files.
- Added CLI support for input paths, optional staging artifacts, and artifact format selection.
- Kept PostgreSQL insertion delegated to `etl.load.load_messages()`.
- Kept staging persistence delegated to `etl.artifacts.save_stage_output()`.
- Logged runner errors through `logger/logger.py`.
- Added `tests/test_run_etl.py` with mocks and no real PostgreSQL dependency.

## Verification

```powershell
.\venv\Scripts\python.exe -m pytest tests/
```

```text
57 passed in 0.82s
```

## Commands

Run ETL:

```powershell
python scripts/run_etl.py data/raw/ig_message_1.json
```

Run ETL and save staging artifacts:

```powershell
python scripts/run_etl.py data/raw/ig_message_1.json --save-artifacts
```

Run ETL and save CSV artifacts:

```powershell
python scripts/run_etl.py data/raw/ig_message_1.json --save-artifacts --artifact-format csv
```
