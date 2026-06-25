# Project Context

## Objective

Build a modular data analysis application that processes personal conversation data and generates insights using ETL, PostgreSQL, logging, analysis modules, and Streamlit.

## Current Architecture

- `db/`: PostgreSQL schema, connection creation, schema execution, parameterized queries, and read-only message repository helpers.
- `logger/`: Centralized critical error logging to `logs/errors.txt` and PostgreSQL `logs`.
- `scripts/`: Manual infrastructure scripts for database initialization, connection testing, schema inspection, and end-to-end ETL execution.
- `tests/`: Unit tests for database connection behavior, message reads, logger resilience, ETL extraction, staging artifacts, transformation, loading, ETL runner orchestration, analysis preprocessing, metrics, sentiment, and dashboard helpers.
- `etl/`: Extraction utilities, deterministic transformation, staging artifact persistence, PostgreSQL loading, and schema placeholders.
- `analysis/`: Deterministic preprocessing, in-memory metrics helpers, and deterministic sentiment analysis.
- `app/`: Streamlit dashboard entrypoint and reusable dashboard data preparation helpers.

## Implemented Infrastructure Modules

- `db/schema.sql` creates `messages` and `logs` tables, duplicate protection, and indexes.
- `db/connection.py` loads environment variables, builds a PostgreSQL URL, creates a SQLAlchemy engine, tests connectivity, and executes schema SQL.
- `db/queries.py` stores SQLAlchemy `text()` query objects for logs, message counts, message reads, duplicate checks, and message inserts.
- `db/messages.py` executes read-only message queries through the database connection abstraction.
- `logger/config.py` defines log path, format, and default severity.
- `logger/logger.py` writes critical errors to `logs/errors.txt` and attempts PostgreSQL log insertion.

## Logging

Critical errors always write to `logs/errors.txt`. Database logging uses the parameterized insert query in `db/queries.py`. If database logging fails, the secondary failure is written to the same text log and does not raise an uncaught exception.

## ETL Extraction

`etl/extract/` contains focused extraction utilities. The package still exposes the legacy JSON inspection and loading helpers from `etl.extract` for compatibility with current tests and scripts.

WhatsApp `.txt` exports are the official source format currently supported for message extraction. WhatsApp messages are parsed into dictionaries in memory and are not converted into physical JSON files. Day/month and month/day dates with two-digit or four-digit years are supported. Multiline messages are preserved by appending continuation lines to the previous parsed message.

Instagram extraction supports Meta `.json` message exports and `.zip` archive message discovery. Extracted Instagram records stay in memory as Python dictionaries, are printed to the console by the dispatcher route, and are not written to disk or inserted into PostgreSQL.

Current extraction modules:

- `etl/extract/file_discovery.py`: detects supported source types from file path metadata without reading contents.
- `etl/extract/whatsapp_extract.py`: parses WhatsApp `.txt` export lines and returns message dictionaries.
- `etl/extract/instagram_extract.py`: parses Meta Instagram `.json` exports and discovers message JSON files inside `.zip` exports.
- `etl/extract/extract_dispatcher.py`: routes supported files to the matching extractor.

File access errors, JSON parsing errors, unsupported schemas, empty record sets, and runtime extraction errors are logged through `logger/logger.py`.

## ETL Transformation

`etl/transform.py` normalizes extracted Instagram and WhatsApp dictionaries into the standard in-memory schema:

- `sender`
- `message`
- `message_normalized`
- `timestamp`
- `source`

Transformation preserves the original message text in `message` and stores lowercase, accent-free, punctuation-free text in `message_normalized`. Instagram `timestamp_ms` values are parsed into UTC `datetime` values. Transformation does not write files, load PostgreSQL, run analysis, or execute SQL. Transformation errors are logged through `logger/logger.py` and re-raised.

## ETL Staging Artifacts

`etl/artifacts.py` saves and loads intermediate ETL records without mutating raw source files or loading PostgreSQL. Staged extracted records are stored in `data/staging/extracted/`. Staged transformed records are stored in `data/staging/transformed/`.

The preferred artifact format is Parquet through `pandas` and `pyarrow`, preserving datetime fields for staged ETL records. CSV support is also implemented explicitly for fallback and inspection; timestamp fields are serialized as CSV values.

Artifact file names include the stage, source, and UTC timestamp, for example:

```text
data/staging/extracted/extracted_instagram_20260529_193012.parquet
data/staging/transformed/transformed_instagram_20260529_193145.parquet
```

Artifact persistence remains separate from extraction, transformation, and database loading. Low-level extraction and transformation functions continue returning Python dictionaries in memory.

## ETL Loading

`etl/load.py` loads only already transformed records with these fields:

- `sender`
- `message`
- `message_normalized`
- `timestamp`
- `source`

Database loading uses the connection abstraction from `db/connection.py` and parameterized SQL from `db/queries.py`. Duplicate messages are skipped safely through the existing unique constraint and `ON CONFLICT DO NOTHING`. Loading accepts records in memory and can also load transformed records from a staged artifact through a wrapper that keeps artifact serialization separate from database insertion.

Loading errors are logged through `logger/logger.py` and re-raised. Loading tests use fakes and do not require a real PostgreSQL server.

## Manual ETL Runner

`scripts/run_etl.py` orchestrates extraction, transformation, optional staging artifact persistence, and PostgreSQL loading for one or more supported export files. It keeps source-specific extraction, deterministic transformation, artifact persistence, and database loading inside their existing modules.

Run without artifacts:

```bash
python scripts/run_etl.py data/raw/ig_message_1.json
```

Run and save extracted/transformed artifacts:

```bash
python scripts/run_etl.py data/raw/ig_message_1.json --save-artifacts
```

Use CSV artifacts:

```bash
python scripts/run_etl.py data/raw/ig_message_1.json --save-artifacts --artifact-format csv
```

Runner errors are logged through `logger/logger.py` and re-raised. Tests use mocks and do not require a real PostgreSQL server.

## Database Message Reads

`db/messages.py` provides read-only helpers for stored messages after ETL loading:

- `fetch_messages()`
- `count_all_messages()`
- `count_messages_by_source()`
- `count_messages_by_sender()`
- `count_messages_by_day()`
- `count_messages_by_hour()`
- `count_keyword_occurrences()`

All SQL remains in `db/queries.py`, all reads use `get_engine()` from `db/connection.py`, and keyword matching uses parameterized SQL with escaped literal `LIKE` patterns. Query errors are logged through `logger/logger.py` and re-raised. Tests use fakes and do not require a real PostgreSQL server.

## Analysis Preprocessing

`analysis/preprocessing.py` provides deterministic preprocessing helpers for analysis inputs without reading from PostgreSQL, writing SQL, running ETL, calculating metrics, or performing sentiment analysis.

Preprocessing accepts message dictionaries already returned by ETL/database layers and returns copied records with additional analysis fields:

- `message_preprocessed`
- `message_tokens`

Original fields such as `sender`, `message`, `message_normalized`, `timestamp`, and `source` are preserved. When `message_normalized` exists, preprocessing uses it as the source text. When it is missing, preprocessing falls back to `message`.

Preprocessing lowercases text, removes accents, removes punctuation, compacts whitespace, preserves emojis as symbols, and returns empty token lists for empty messages. Validation errors are logged through `logger/logger.py` and re-raised.

Focused preprocessing tests:

```bash
.\venv\Scripts\python.exe -m pytest tests/test_preprocessing.py
```

Latest focused verification:

```text
7 passed in 0.03s
```

Latest full-suite verification after WhatsApp date parsing fix:

```text
65 passed in 0.85s
```

## Analysis Metrics

`analysis/metrics.py` provides deterministic in-memory metrics for message dictionaries already returned by ETL, database reads, or analysis preprocessing. Metrics do not query PostgreSQL, write SQL, run ETL, perform sentiment analysis, or include Streamlit dashboard logic.

Metric helpers:

- `enrich_message_record()`
- `enrich_message_records()`
- `calculate_message_metrics()`
- `count_messages_by_field()`

Enriched records preserve original fields and add:

- `message_character_count`
- `message_token_count`

Aggregate metrics include:

- total messages
- total characters
- total tokens
- average message character count
- average message token count
- messages by sender
- messages by source
- messages by day
- messages by hour
- top tokens

Metrics use `message_tokens` when records are already preprocessed. When tokens are unavailable, metrics fall back to whitespace token counts from `message_preprocessed`, `message_normalized`, or `message`. Validation errors are logged through `logger/logger.py` and re-raised.

Focused metrics tests:

```bash
.\venv\Scripts\python.exe -m pytest tests/test_metrics.py
```

Latest focused verification:

```text
7 passed in 0.04s
```

Latest full-suite verification after metrics:

```text
72 passed in 0.83s
```

## Analysis Sentiment

`analysis/sentiment.py` provides deterministic in-memory sentiment analysis for message dictionaries already returned by ETL, database reads, or analysis preprocessing. Sentiment analysis does not query PostgreSQL, write SQL, run ETL, calculate metrics, or include Streamlit dashboard logic.

Sentiment helpers:

- `analyze_text_sentiment()`
- `enrich_message_record()`
- `enrich_message_records()`
- `calculate_sentiment_summary()`

Enriched records preserve original fields and add:

- `sentiment_label`
- `sentiment_score`
- `sentiment_positive_token_count`
- `sentiment_negative_token_count`

Sentiment uses a deterministic Spanish lexicon over already tokenized messages when `message_tokens` exists. When tokens are unavailable, it uses existing preprocessing helpers over `message_preprocessed`, `message_normalized`, or `message`. Validation errors are logged through `logger/logger.py` and re-raised.

Focused sentiment tests:

```bash
.\venv\Scripts\python.exe -m pytest tests/test_sentiment.py
```

Latest focused verification:

```text
8 passed in 0.05s
```

Latest full-suite verification after sentiment:

```text
80 passed in 0.85s
```

## Streamlit Dashboard

`app/main.py` implements the Streamlit dashboard as a UI orchestration layer. It fetches stored messages only through `db.messages.fetch_messages()`, sends already fetched records through `app.dashboard.prepare_dashboard_data()`, and renders summary metrics, grouped charts, top tokens, and analyzed message rows.

`app/dashboard.py` contains reusable dashboard helper logic for already fetched message dictionaries. It delegates preprocessing, metrics, and sentiment analysis to existing analysis modules and returns copied records plus aggregate summaries. It does not query PostgreSQL, write SQL, run ETL, or contain Streamlit rendering code.

`app/main.py` bootstraps the project root on `sys.path` before importing project modules so `streamlit run app/main.py` works when Streamlit executes the file from the `app/` directory.

Dashboard errors are logged through `logger/logger.py`. Streamlit displays a generic safe error message instead of exposing database exception details.

Latest visual validation:

```text
streamlit run app/main.py opened successfully at http://localhost:8501.
Playwright Chromium screenshot validation rendered dashboard metrics and charts.
```

Focused dashboard tests:

```bash
.\venv\Scripts\python.exe -m pytest tests/test_dashboard.py
```

Latest focused verification:

```text
4 passed in 0.06s
```

Latest full-suite verification after dashboard:

```text
84 passed in 1.63s
```

Focused WhatsApp extraction verification:

```text
6 passed in 0.50s
```

Manual schema inspection:

```bash
python scripts/inspect_json_schema.py data/raw/example.json
```

Run extraction unit tests:

```bash
.\venv\Scripts\python.exe -m pytest tests/
```

The local global Python installation does not expose `pytest` as a command. Use the project virtual environment command above, or activate `venv` before running `pytest tests/`.

Latest verification:

```text
Focused dashboard entrypoint tests: 5 passed in 0.46s
Full suite: 85 passed in 1.08s
```

## Romantic Landing

`app/main.py` now renders a romantic landing page instead of the previous technical dashboard. Streamlit still acts only as a UI orchestration layer: it calls `services.romantic_metrics.get_romantic_landing_metrics()` and renders data that is already prepared for the page.

New romantic landing modules:

- `db/queries.py`: stores the romantic SQL query constants.
- `db/romantic_queries.py`: executes read-only romantic queries through `db.connection.get_engine()`.
- `services/romantic_metrics.py`: assembles landing-ready hero data, summary cards, timeline events, romantic words, featured messages, rhythm datasets, and conversation starter details.
- `ui/styles.py`: centralizes custom Streamlit CSS.
- `ui/components.py`: renders hero, bento cards, timeline, word chips, quote cards, conversation starter, and closing sections.
- `ui/charts.py`: renders soft Altair charts for conversation rhythm.

Romantic phrase searches use `message_normalized`; displayed quotes use original `message` text. SQL remains parameterized and isolated in `db/queries.py`. The Streamlit page avoids technical NLP wording, raw tables, `st.dataframe`, and default technical metric cards in the main view.

ETL transformation was also corrected to preserve original WhatsApp multiline message text while keeping normalized text compact, and to keep direct Instagram transformation compatible with missing content.

Latest romantic landing verification:

```text
Focused romantic/transform tests: 9 passed in 0.23s
Full suite: 87 passed in 1.62s
Streamlit HTTP check: http://localhost:8501 returned 200 OK
Browser visual check: blocked because local Playwright Chrome is not installed.
```

## Romantic Visual System Completion

The visual system was tightened after re-reading `docs/prompts/02_refactor_visual_streamlit_romantico.md`.

Updates:

- `ui/styles.py` keeps the centralized Streamlit CSS injected through `st.markdown(..., unsafe_allow_html=True)`.
- The palette remains white, soft pink, fuchsia, and warm dark text.
- Cards use glassmorphism, subtle fuchsia borders, glow shadows, inset highlights, hover lift, and large rounded corners.
- The hero now has stronger premium treatment, responsive constraints, and a subtle decorative element.
- Bento, timeline, quote, word, and chart layouts remain mobile-first.
- `ui/charts.py` now exposes `apply_altair_romantic_theme()` and `apply_plotly_romantic_theme()` helpers.
- `tests/test_ui_charts.py` validates the Plotly theme helper using a fake figure, so no Plotly dependency is required.

Latest verification:

```text
Focused UI tests: 4 passed in 1.43s
Full suite: 88 passed in 1.62s
Streamlit HTTP check: http://localhost:8501 returned 200 OK
```

Run extraction:

```bash
python -c "from etl.extract.extract_dispatcher import extract_messages; print(extract_messages('data/raw/ig_message_1.json'))"
```

Run transformation:

```bash
python -c "from etl.extract.extract_dispatcher import extract_messages; from etl.transform import transform_messages; print(transform_messages(extract_messages('data/raw/ig_message_1.json')))"
```

Save extracted output:

```bash
python -c "from etl.extract.extract_dispatcher import extract_messages; from etl.artifacts import save_stage_output; records = extract_messages('data/raw/ig_message_1.json'); print(save_stage_output(records, stage='extracted', source='instagram'))"
```

Save transformed output:

```bash
python -c "from etl.extract.extract_dispatcher import extract_messages; from etl.transform import transform_messages; from etl.artifacts import save_stage_output; extracted = extract_messages('data/raw/ig_message_1.json'); transformed = transform_messages(extracted); print(save_stage_output(transformed, stage='transformed', source='instagram'))"
```

Load transformed staged records into PostgreSQL:

```bash
python -c "from etl.artifacts import load_records; from etl.load import load_messages; records = load_records('data/staging/transformed/transformed_instagram_YYYYMMDD_HHMMSS.parquet'); print(load_messages(records))"
```

Run the manual ETL runner:

```bash
python scripts/run_etl.py data/raw/ig_message_1.json
```

## Database Initialization

Database credentials are loaded from `.env` or process environment. `DATABASE_URL` is preferred. If it is missing, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` are used.

Run:

```bash
python scripts/init_db.py
```

## Tests

Run:

```bash
.\venv\Scripts\python.exe -m pytest tests/
```

## Streamlit

Run:

```bash
streamlit run app/main.py
```
