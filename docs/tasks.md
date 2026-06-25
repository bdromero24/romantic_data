# Task List

## Phase 0: Project Documentation and Agent Rules

- [x] Create `README.md`
- [x] Create `docs/agents.md`
- [x] Create `docs/context.md`
- [x] Create `docs/tasks.md`
- [x] Create `docs/next_prompt.md`
- [x] Create `docs/prompts/`
- [x] Create `docs/prompts/0_database_logger_setup.md`
- [x] Create `docs/sessions/`
- [x] Define project structure
- [x] Define coding rules for Codex
- [x] Define documentation update rules
- [x] Define execution commands
- [x] Define testing commands

## Phase 1: Database and Logging Infrastructure

- [x] Create `app/`
- [x] Create `etl/`
- [x] Create `analysis/`
- [x] Create `db/`
- [x] Create `logger/`
- [x] Create `scripts/`
- [x] Create `tests/`
- [x] Create `data/raw/`
- [x] Create `logs/`
- [x] Create `requirements.txt`
- [x] Add `pandas`
- [x] Add `sqlalchemy`
- [x] Add `psycopg2-binary`
- [x] Add `python-dotenv`
- [x] Add `streamlit`
- [x] Add `pytest`
- [x] Create `.env.example`
- [x] Define `DATABASE_URL` in `.env.example`
- [x] Define fallback PostgreSQL environment variables in `.env.example`
- [x] Create `db/schema.sql`
- [x] Create `messages` table
- [x] Create `logs` table
- [x] Add unique constraint to avoid duplicate messages
- [x] Add message indexes
- [x] Add log indexes
- [x] Create `db/connection.py`
- [x] Implement `get_database_url()`
- [x] Implement `get_engine()`
- [x] Implement `test_connection()`
- [x] Implement `execute_schema()`
- [x] Load environment variables with `python-dotenv`
- [x] Support `DATABASE_URL`
- [x] Support fallback PostgreSQL variables
- [x] Handle `ProgrammingError`
- [x] Handle `DatabaseError`
- [x] Handle `OperationalError`
- [x] Handle generic exceptions
- [x] Send database errors to centralized logger
- [x] Create `db/queries.py`
- [x] Add parameterized query to insert logs
- [x] Add parameterized message count queries
- [x] Add parameterized keyword occurrence query
- [x] Add parameterized duplicate message query
- [x] Ensure all queries use `sqlalchemy.text`
- [x] Ensure no SQL uses string concatenation with user input
- [x] Create `logger/config.py`
- [x] Create `logger/logger.py`
- [x] Define log directory
- [x] Define log file path
- [x] Define log format
- [x] Implement `get_file_logger()`
- [x] Implement `log_critical_error()`
- [x] Write critical errors to `.txt`
- [x] Write critical errors to PostgreSQL `logs` table
- [x] Prevent uncaught exception if DB logging fails
- [x] Avoid circular imports between `logger/` and `db/`
- [x] Capture database errors
- [x] Capture ETL errors
- [x] Capture Streamlit rendering errors
- [x] Capture generic runtime errors
- [x] Create `scripts/init_db.py`
- [x] Implement schema initialization script
- [x] Create `scripts/test_db_connection.py`
- [x] Implement manual DB connection test script
- [x] Document command `python scripts/init_db.py`
- [x] Document command `python scripts/test_db_connection.py`
- [x] Create `tests/test_db_connection.py`
- [x] Test `get_database_url()`
- [x] Test `test_connection()`
- [x] Test DB errors do not crash execution
- [x] Create `tests/test_logger.py`
- [x] Test logger writes to file
- [x] Test `log_critical_error()` does not crash if DB logging fails
- [x] Test log file is created
- [x] Document command `pytest tests/`
- [x] Update `README.md` with setup instructions
- [x] Update `README.md` with DB initialization command
- [x] Update `README.md` with DB connection test command
- [x] Update `README.md` with pytest command
- [x] Update `README.md` with Streamlit command
- [x] Update `docs/context.md`
- [x] Update `docs/tasks.md`
- [x] Create `docs/sessions/0_database_logger_setup_<timestamp>.md`
- [x] Update `docs/next_prompt.md`

## Phase 2: ETL Extraction
- [x] Unit test: Implement, document and test module db/ and logger/.
- [x] Implement JSON file loader
- [x] Implement safe JSON parsing
- [x] Implement schema inspection for unknown JSON structures
- [x] Detect Instagram JSON structure
- [x] Detect WhatsApp JSON structure
- [x] Return raw pandas DataFrame
- [x] Log invalid JSON errors
- [x] Log unsupported schema errors
- [x] Create `scripts/inspect_json_schema.py`
- [x] Create `tests/test_extract.py`
- [x] Update documentation
- [x] Create `etl/extract/file_discovery.py`
- [x] Create `etl/extract/whatsapp_extract.py`
- [x] Create `etl/extract/extract_dispatcher.py`
- [x] Detect WhatsApp `.txt` exports by path metadata
- [x] Detect Instagram `.json` and `.zip` exports by path metadata
- [x] Parse WhatsApp `.txt` messages into dictionaries in memory
- [x] Preserve WhatsApp multiline messages
- [x] Route WhatsApp extraction through dispatcher
- [x] Keep Instagram dispatcher route pending with `NotImplementedError`
- [x] Create focused extraction unit tests
- [x] Document command `pytest tests/test_file_discovery.py tests/test_whatsapp_extract.py tests/test_extract_dispatcher.py`

## Phase 3: Pending Instagram Extraction

- [x] Implement Instagram `.json` extraction from Meta exports
- [x] Implement Instagram `.zip` archive discovery without loading to database
- [x] Add unit tests for Instagram JSON message extraction
- [x] Add unit tests for Instagram ZIP export handling
- [x] Keep extracted Instagram records in memory
- [x] Update documentation with Instagram extraction execution commands
- [x] Verify complete unit test suite with project virtual environment
- [x] Document virtual environment test command for Windows

## Phase 4: Next ETL Transformation

- [x] Review current `etl/transform.py`
- [x] Implement deterministic text normalization helpers
- [x] Preserve original message text
- [x] Store normalized text separately
- [x] Normalize Instagram extracted dictionaries into the future standard message schema
- [x] Normalize WhatsApp extracted dictionaries into the future standard message schema
- [x] Parse Instagram `timestamp_ms` without database writes
- [x] Keep SQL out of ETL transformation modules
- [x] Log transformation errors through centralized logger
- [x] Add focused unit tests for transformation helpers
- [x] Update documentation after transformation work

## Phase 5: ETL Staging Artifacts

- [x] Create `etl/artifacts.py`
- [x] Create `data/staging/extracted/` convention
- [x] Create `data/staging/transformed/` convention
- [x] Implement `ensure_directory()`
- [x] Implement `build_artifact_path()`
- [x] Implement `save_records()`
- [x] Implement `load_records()`
- [x] Implement `save_stage_output()`
- [x] Support Parquet artifacts with `pandas` and `pyarrow`
- [x] Support CSV artifact fallback explicitly
- [x] Preserve datetime fields in Parquet round-trips
- [x] Keep raw files unchanged
- [x] Keep artifact persistence separate from extraction and transformation
- [x] Log artifact persistence errors through centralized logger
- [x] Add focused unit tests for staging artifacts
- [x] Document artifact save/load commands

## Phase 6: ETL Loading

- [x] Review current `etl/load.py`, `etl/transform.py`, `etl/artifacts.py`, `db/queries.py`, `db/connection.py`, `db/schema.sql`, and tests
- [x] Implement loading only after transformation records are validated
- [x] Use parameterized queries from `db/queries.py`
- [x] Use connection abstraction from `db/connection.py`
- [x] Handle duplicates safely with existing schema constraints
- [x] Log load errors through centralized logger
- [x] Add focused unit tests for load behavior without requiring a real database
- [x] Allow loading transformed records already in memory
- [x] Add wrapper for loading transformed staged artifact records
- [x] Keep artifact serialization separate from database loading logic
- [x] Update documentation after loading work

## Phase 7: Database Message Reads

- [x] Review current `etl/load.py`, `etl/transform.py`, `etl/artifacts.py`, `db/queries.py`, `db/connection.py`, `db/schema.sql`, and tests
- [x] Keep extraction, transformation, artifact persistence, loading, and database reads separate
- [x] Add read-only message repository helpers in `db/`
- [x] Add SQL only to `db/queries.py`
- [x] Use parameterized queries only
- [x] Use connection abstraction from `db/connection.py`
- [x] Escape literal keyword search patterns for `LIKE`
- [x] Log backend query errors through centralized logger
- [x] Add focused unit tests with fakes and no real PostgreSQL server
- [x] Verify complete unit test suite with project virtual environment
- [x] Update documentation after database read work

## Phase 8: Manual ETL Runner

- [x] Review current extraction, transformation, artifact, loading, DB read, schema, and test modules
- [x] Create `scripts/run_etl.py`
- [x] Orchestrate extraction, transformation, and loading without mixing responsibilities
- [x] Support one or more supported input export files
- [x] Support optional extracted and transformed staging artifacts
- [x] Keep SQL out of scripts and ETL modules
- [x] Use existing `etl.load.load_messages()` for PostgreSQL insertion
- [x] Keep raw source files unchanged
- [x] Log runner errors through centralized logger
- [x] Add focused unit tests with mocks and no real PostgreSQL server
- [x] Verify complete unit test suite with project virtual environment
- [x] Update documentation after ETL runner work

## Phase 9: Analysis Preprocessing

- [x] Review current `analysis/preprocessing.py`
- [x] Review current `etl/transform.py`
- [x] Review current `db/messages.py`
- [x] Keep ETL, database reads, and analysis preprocessing separate
- [x] Avoid sentiment analysis, Streamlit dashboard logic, and analysis metrics
- [x] Avoid SQL and database reads in preprocessing
- [x] Avoid new dependencies
- [x] Implement deterministic text preprocessing for Spanish text
- [x] Support accents, punctuation, emojis, and empty messages
- [x] Preserve original message fields in preprocessed records
- [x] Log preprocessing errors through centralized logger
- [x] Add focused preprocessing unit tests
- [x] Verify focused preprocessing tests with project virtual environment
- [x] Document full-suite status after preprocessing
- [x] Update documentation after preprocessing work

## Phase 10: WhatsApp Extraction Date Parsing

- [x] Review current `etl/extract/whatsapp_extract.py`
- [x] Review `tests/test_whatsapp_extract.py`
- [x] Review `tests/test_extract_dispatcher.py`
- [x] Keep extraction, transformation, database reads, and analysis preprocessing separate
- [x] Avoid SQL changes
- [x] Avoid sentiment analysis, Streamlit dashboard logic, and analysis metrics
- [x] Avoid new dependencies
- [x] Keep WhatsApp parsing deterministic and testable
- [x] Support tested WhatsApp day/month date formats
- [x] Preserve multiline message behavior
- [x] Add focused date parsing regression test
- [x] Verify focused WhatsApp extraction tests with project virtual environment
- [x] Verify complete unit test suite with project virtual environment
- [x] Update documentation after WhatsApp extraction work

## Phase 11: Analysis Metrics

- [x] Review current `analysis/metrics.py`
- [x] Review current `analysis/preprocessing.py`
- [x] Review current `db/messages.py`
- [x] Review `docs/context.md`
- [x] Review `docs/tasks.md`
- [x] Keep ETL, database reads, analysis preprocessing, and analysis metrics separate
- [x] Avoid sentiment analysis and Streamlit dashboard logic
- [x] Avoid SQL changes for metrics
- [x] Avoid new dependencies
- [x] Keep metrics deterministic and testable
- [x] Accept already-fetched or already-preprocessed message records in memory
- [x] Preserve original message fields when returning enriched records
- [x] Log metrics errors through centralized logger
- [x] Add focused metrics unit tests
- [x] Verify focused metrics tests with project virtual environment
- [x] Verify complete unit test suite with project virtual environment
- [x] Update documentation after metrics work

## Phase 12: Analysis Sentiment

- [x] Review current `analysis/sentiment.py`
- [x] Review current `analysis/preprocessing.py`
- [x] Review current `analysis/metrics.py`
- [x] Review `docs/context.md`
- [x] Review `docs/tasks.md`
- [x] Keep ETL, database reads, preprocessing, metrics, and sentiment analysis separate
- [x] Avoid Streamlit dashboard logic
- [x] Avoid SQL changes for sentiment analysis
- [x] Avoid new dependencies
- [x] Keep sentiment logic deterministic and testable
- [x] Accept already-fetched or already-preprocessed message records in memory
- [x] Preserve original message fields when returning enriched records
- [x] Log sentiment errors through centralized logger
- [x] Add focused sentiment unit tests
- [x] Verify focused sentiment tests with project virtual environment
- [x] Verify complete unit test suite with project virtual environment
- [x] Update documentation after sentiment work

## Phase 13: Streamlit Dashboard

- [x] Review current `app/main.py`
- [x] Review current `db/messages.py`
- [x] Review current `analysis/preprocessing.py`
- [x] Review current `analysis/metrics.py`
- [x] Review current `analysis/sentiment.py`
- [x] Review `docs/context.md`
- [x] Review `docs/tasks.md`
- [x] Keep Streamlit UI separate from ETL, database SQL, preprocessing, metrics, and sentiment internals
- [x] Fetch messages only through `db/messages.py`
- [x] Run preprocessing, metrics, and sentiment through existing modules
- [x] Avoid SQL changes outside `db/queries.py`
- [x] Avoid new dependencies
- [x] Log dashboard errors through centralized logger
- [x] Hide sensitive database errors from Streamlit users
- [x] Add reusable dashboard helper logic in `app/dashboard.py`
- [x] Add focused dashboard helper unit tests
- [x] Verify focused dashboard tests with project virtual environment
- [x] Verify complete unit test suite with project virtual environment
- [x] Update documentation after dashboard work

## Phase 14: Streamlit Dashboard Visual Validation

- [x] Review `README.md`
- [x] Review `docs/agents.md`
- [x] Review `docs/context.md`
- [x] Review `docs/tasks.md`
- [x] Review `app/main.py`
- [x] Review `app/dashboard.py`
- [x] Review `db/messages.py`
- [x] Review `analysis/preprocessing.py`
- [x] Review `analysis/metrics.py`
- [x] Review `analysis/sentiment.py`
- [x] Run focused dashboard validation tests
- [x] Run complete unit test suite with project virtual environment
- [x] Start Streamlit locally
- [x] Validate dashboard opens in browser automation
- [x] Fix Streamlit direct-run project import path
- [x] Add focused entrypoint bootstrap unit test
- [x] Confirm dashboard renders summary metrics and charts
- [x] Avoid SQL, ETL, database, preprocessing, metrics, and sentiment responsibility changes
- [x] Avoid new dependencies
- [x] Update documentation after visual validation work

## Phase 15: Romantic Landing Business Logic And Visual Refactor

- [x] Review romantic landing scope in `docs/sessions/8_landing_romantica_scope_20260609.md`
- [x] Keep ETL, database SQL, service aggregation, and Streamlit UI separated
- [x] Add romantic SQL query constants in `db/queries.py`
- [x] Add read-only romantic database helpers in `db/romantic_queries.py`
- [x] Use parameterized regex patterns for romantic phrase counts
- [x] Use `message_normalized` for searches and `message` for displayed phrases
- [x] Add `services/romantic_metrics.py`
- [x] Build landing-ready romantic summary cards
- [x] Build timeline data for first message, first romantic phrases, peak day, and peak month
- [x] Build featured original-message cards
- [x] Build romantic word counts
- [x] Build rhythm datasets by hour, weekday, and month
- [x] Add custom Streamlit CSS in `ui/styles.py`
- [x] Add romantic HTML components in `ui/components.py`
- [x] Add romantic Altair chart helpers in `ui/charts.py`
- [x] Refactor `app/main.py` from technical dashboard to romantic landing page
- [x] Avoid Streamlit tables and technical NLP/sentiment language in the main page
- [x] Add focused unit tests for romantic metric aggregation
- [x] Preserve WhatsApp original multiline message text in ETL transformation
- [x] Keep Instagram direct transformation compatible with missing content
- [x] Verify focused tests
- [x] Verify full unit test suite
- [x] Start Streamlit locally on `http://localhost:8501`
- [x] Confirm Streamlit responds with HTTP 200
- [x] Document browser validation limitation caused by missing local Chrome

## Phase 16: Romantic Visual System Completion

- [x] Re-read `docs/prompts/02_refactor_visual_streamlit_romantico.md`
- [x] Keep visual implementation in centralized Streamlit styling layer
- [x] Strengthen `ui/styles.py` premium romantic palette usage
- [x] Strengthen glassmorphism card shadows and subtle inset highlights
- [x] Add subtle hero decorative treatment without extra dependencies
- [x] Improve mobile-first width constraints and responsive hero sizing
- [x] Add button styling aligned with fuchsia romantic palette
- [x] Add reusable Altair romantic theme helper in `ui/charts.py`
- [x] Add reusable Plotly romantic theme helper in `ui/charts.py`
- [x] Keep numeric/date typography in monospace and copy in sans-serif
- [x] Add focused unit test for Plotly theme helper without requiring Plotly
- [x] Verify focused UI tests
- [x] Verify full unit test suite
- [x] Confirm Streamlit still responds with HTTP 200
