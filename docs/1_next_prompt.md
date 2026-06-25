Read `README.md`, `docs/agents.md`, `docs/context.md`, and `docs/tasks.md`.

Current status:

1. Instagram Meta `.json` extraction is implemented in `etl/extract/instagram_extract.py`.
2. Instagram `.zip` handling discovers message JSON files inside Meta exports and returns records in memory.
3. WhatsApp `.txt` extraction remains unchanged.
4. Extracted Instagram records are Python dictionaries, printed by `extract_instagram_messages()` and dispatcher routing.
5. Extraction does not insert into PostgreSQL.
6. ETL transformation is implemented in `etl/transform.py`.
7. Transformation normalizes Instagram and WhatsApp extracted dictionaries to:

   * `sender`
   * `message`
   * `message_normalized`
   * `timestamp`
   * `source`
8. Transformation preserves original message text and stores normalized text separately.
9. Instagram `timestamp_ms` values are parsed into UTC `datetime` values.
10. SQL remains outside ETL modules.
11. Critical extraction and transformation errors are logged with the centralized logger and re-raised.

Unit test status:

```powershell
.\venv\Scripts\python.exe -m pytest tests/
```

Result:

```text
32 passed in 0.74s
```

Important:

The global Python installation currently does not expose `pytest`:

```text
pytest : El termino 'pytest' no se reconoce...
python -m pytest tests/ : No module named pytest
```

Use the local virtual environment command above, or activate `venv` before running:

```powershell
pytest tests/
```

## New architectural requirement: ETL staging artifacts

Before implementing database loading, add a small, focused artifact persistence layer for ETL intermediate outputs.

Purpose:

* Save the output of each ETL step to disk.
* Make each ETL step auditable.
* Allow the user to inspect the result of extraction and transformation.
* Avoid re-running expensive extraction from raw files when a staged artifact already exists.
* Keep raw source files unchanged.

Directory convention:

```text
data/
  raw/
  staging/
    extracted/
    transformed/
  processed/
```

Create:

* `etl/artifacts.py`
* focused tests under `tests/`

Implement in `etl/artifacts.py`:

* `ensure_directory(path: str | Path) -> Path`
* `build_artifact_path(stage: str, source: str, file_format: str = "parquet") -> Path`
* `save_records(records: list[dict], output_path: str | Path) -> Path`
* `load_records(input_path: str | Path) -> list[dict]`
* `save_stage_output(records: list[dict], stage: str, source: str, file_format: str = "parquet") -> Path`

Rules:

1. Supported stages:

   * `extracted`
   * `transformed`

2. Supported file formats:

   * `parquet`
   * `csv`

3. Prefer Parquet for staged ETL artifacts.

4. Add `pyarrow` to `requirements.txt` if Parquet support is implemented.

5. If Parquet support is not available, fail clearly with an actionable error message or fallback to CSV only if implemented explicitly.

6. Use `pandas` for serialization.

7. Do not save raw files again. Raw files remain in `data/raw/`.

8. Do not write artifacts from inside low-level extraction or transformation functions unless explicitly called by a wrapper function.

9. Keep extraction functions returning Python dictionaries in memory.

10. Keep transformation functions returning Python dictionaries in memory.

11. Add optional wrapper functions only if useful, for example:

    * `extract_and_save(...)`
    * `transform_and_save(...)`

12. Artifact file names should include:

    * stage
    * source
    * timestamp

Example:

```text
data/staging/extracted/extracted_instagram_20260529_193012.parquet
data/staging/transformed/transformed_instagram_20260529_193145.parquet
```

13. Datetime fields must be preserved correctly when saving/loading Parquet.

14. For CSV fallback, datetime fields may be serialized as ISO strings.

15. Use centralized logger for critical artifact persistence errors and re-raise exceptions.

16. Do not insert artifacts into PostgreSQL.

## Next task

Implement ETL loading only after reviewing the current:

* `etl/load.py`
* `etl/transform.py`
* `etl/artifacts.py`
* `db/queries.py`
* `db/connection.py`
* `db/schema.sql`
* tests

Requirements:

1. Keep extraction and transformation modules unchanged unless a loading or artifact test exposes a real bug.
2. Do not implement sentiment analysis, Streamlit dashboard, or NLP metrics.
3. Keep SQL out of ETL modules.
4. Add any SQL needed for loading only to `db/queries.py`.
5. Use parameterized queries only.
6. Use the connection abstraction from `db/connection.py`.
7. Load only already transformed records with fields:

   * `sender`
   * `message`
   * `message_normalized`
   * `timestamp`
   * `source`
8. Handle duplicate messages safely according to existing schema constraints.
9. Log loading errors through `logger/logger.py`.
10. Add focused unit tests with `pytest` and mocks/fakes so tests do not require a real PostgreSQL server.
11. Loading should accept records already in memory.
12. Loading may also accept records loaded from a staged artifact file, but database loading logic must remain separate from artifact serialization logic.

## Suggested modules

Use this separation:

```text
etl/
  extract/
  transform.py
  artifacts.py
  load.py
```

Responsibilities:

* `extract/`: read raw source files and return extracted records.
* `transform.py`: normalize extracted records into database-ready dictionaries.
* `artifacts.py`: save/load intermediate ETL records as `.parquet` or `.csv`.
* `load.py`: insert transformed records into PostgreSQL.

## Unit tests for artifacts

Add tests for:

* creating staging directories
* building artifact paths
* saving records to Parquet
* loading records from Parquet
* saving records to CSV if CSV support is implemented
* loading records from CSV if CSV support is implemented
* preserving required columns
* preserving timestamps
* handling empty record lists clearly
* logging and re-raising persistence errors

Tests must not require PostgreSQL.

## Commands to document

Document how to run tests:

```powershell
.\venv\Scripts\python.exe -m pytest tests/
```

Document how to run extraction:

```powershell
python -c "from etl.extract.extract_dispatcher import extract_messages; print(extract_messages('data/raw/ig_message_1.json'))"
```

Document how to run transformation:

```powershell
python -c "from etl.extract.extract_dispatcher import extract_messages; from etl.transform import transform_messages; print(transform_messages(extract_messages('data/raw/ig_message_1.json')))"
```

Document how to save extracted output:

```powershell
python -c "from etl.extract.extract_dispatcher import extract_messages; from etl.artifacts import save_stage_output; records = extract_messages('data/raw/ig_message_1.json'); print(save_stage_output(records, stage='extracted', source='instagram'))"
```

Document how to save transformed output:

```powershell
python -c "from etl.extract.extract_dispatcher import extract_messages; from etl.transform import transform_messages; from etl.artifacts import save_stage_output; extracted = extract_messages('data/raw/ig_message_1.json'); transformed = transform_messages(extracted); print(save_stage_output(transformed, stage='transformed', source='instagram'))"
```

Document how to load transformed staged records and send them to the database loader once loading is implemented:

```powershell
python -c "from etl.artifacts import load_records; from etl.load import load_messages; records = load_records('data/staging/transformed/transformed_instagram_YYYYMMDD_HHMMSS.parquet'); print(load_messages(records))"
```

## Documentation updates

Update:

* `docs/context.md`
* `docs/tasks.md`
* `docs/next_prompt.md`
* create a new session summary under `docs/sessions/`

Document:

* staged ETL artifacts
* where extracted artifacts are stored
* where transformed artifacts are stored
* preferred format: Parquet
* CSV fallback if implemented
* how to run artifact save/load commands
* loading remains separate from artifact persistence

## Strict constraints

Do not implement:

* sentiment analysis
* Streamlit dashboard
* NLP metrics
* NLP preprocessing
* raw file mutation

Do not:

* write SQL in ETL extraction, transformation, or artifact modules
* create `.env`
* hardcode input paths
* physically convert WhatsApp `.txt` to `.json`
* create monolithic scripts
* mix artifact persistence with database loading
* suppress errors silently

Return only file paths and file contents using:

```text
# file: path/to/file.py
<content>
```

No explanations.
No extra commentary.
No markdown outside file blocks.
