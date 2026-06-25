
---

# `docs/tasks.md`

```md
# Task List

## Phase 0: Project Documentation and Agent Rules

- [ ] Create `README.md`
- [ ] Create `docs/agents.md`
- [ ] Create `docs/context.md`
- [ ] Create `docs/tasks.md`
- [ ] Create `docs/next_prompt.md`
- [ ] Create `docs/prompts/`
- [ ] Create `docs/prompts/0_database_logger_setup.md`
- [ ] Create `docs/sessions/`
- [ ] Define project structure
- [ ] Define coding rules for Codex
- [ ] Define documentation update rules
- [ ] Define execution commands
- [ ] Define testing commands

---

## Phase 1: Database and Logging Infrastructure

### Project folders

- [ ] Create `app/`
- [ ] Create `etl/`
- [ ] Create `analysis/`
- [ ] Create `db/`
- [ ] Create `logger/`
- [ ] Create `scripts/`
- [ ] Create `tests/`
- [ ] Create `data/raw/`
- [ ] Create `logs/`

### Environment and dependencies

- [ ] Create `requirements.txt`
- [ ] Add `pandas`
- [ ] Add `sqlalchemy`
- [ ] Add `psycopg2-binary`
- [ ] Add `python-dotenv`
- [ ] Add `streamlit`
- [ ] Add `pytest`
- [ ] Create `.env.example`
- [ ] Define `DATABASE_URL` in `.env.example`
- [ ] Define fallback PostgreSQL environment variables in `.env.example`

### Database schema

- [ ] Create `db/schema.sql`
- [ ] Create `messages` table
- [ ] Create `logs` table
- [ ] Add unique constraint to avoid duplicate messages
- [ ] Add index `idx_messages_timestamp`
- [ ] Add index `idx_messages_sender`
- [ ] Add index `idx_messages_source`
- [ ] Add index `idx_messages_source_timestamp`
- [ ] Add index `idx_messages_sender_timestamp`
- [ ] Add index `idx_logs_timestamp`
- [ ] Add index `idx_logs_error_type`
- [ ] Add index `idx_logs_severity`

### Database connection

- [ ] Create `db/connection.py`
- [ ] Implement `get_database_url()`
- [ ] Implement `get_engine()`
- [ ] Implement `test_connection()`
- [ ] Implement `execute_schema()`
- [ ] Load environment variables with `python-dotenv`
- [ ] Support `DATABASE_URL`
- [ ] Support fallback PostgreSQL variables
- [ ] Handle `ProgrammingError`
- [ ] Handle `DatabaseError`
- [ ] Handle `OperationalError`
- [ ] Handle generic exceptions
- [ ] Send database errors to centralized logger

### Parameterized queries

- [ ] Create `db/queries.py`
- [ ] Add parameterized query to insert logs
- [ ] Add parameterized query to count all messages
- [ ] Add parameterized query to count messages by source
- [ ] Add parameterized query to count messages by sender
- [ ] Add parameterized query to count messages by day
- [ ] Add parameterized query to count messages by hour
- [ ] Add parameterized query to count keyword occurrences
- [ ] Add parameterized query to check duplicate message
- [ ] Ensure all queries use `sqlalchemy.text`
- [ ] Ensure no SQL uses string concatenation with user input

### Logger

- [ ] Create `logger/config.py`
- [ ] Create `logger/logger.py`
- [ ] Define log directory
- [ ] Define log file path
- [ ] Define log format
- [ ] Implement `get_file_logger()`
- [ ] Implement `log_critical_error()`
- [ ] Write critical errors to `.txt`
- [ ] Write critical errors to PostgreSQL `logs` table
- [ ] Prevent uncaught exception if DB logging fails
- [ ] Avoid circular imports between `logger/` and `db/`
- [ ] Capture database errors
- [ ] Capture ETL errors
- [ ] Capture Streamlit rendering errors
- [ ] Capture generic runtime errors

### Manual scripts

- [ ] Create `scripts/init_db.py`
- [ ] Implement schema initialization script
- [ ] Create `scripts/test_db_connection.py`
- [ ] Implement manual DB connection test script
- [ ] Document command `python scripts/init_db.py`
- [ ] Document command `python scripts/test_db_connection.py`

### Unit tests

- [ ] Create `tests/test_db_connection.py`
- [ ] Test `get_database_url()`
- [ ] Test `test_connection()`
- [ ] Test DB errors do not crash execution
- [ ] Create `tests/test_logger.py`
- [ ] Test logger writes to file
- [ ] Test `log_critical_error()` does not crash if DB logging fails
- [ ] Test log file is created
- [ ] Document command `pytest tests/`

### Documentation updates

- [ ] Update `README.md` with setup instructions
- [ ] Update `README.md` with DB initialization command
- [ ] Update `README.md` with DB connection test command
- [ ] Update `README.md` with pytest command
- [ ] Update `README.md` with Streamlit command
- [ ] Update `docs/context.md`
- [ ] Update `docs/tasks.md`
- [ ] Create `docs/sessions/0_database_logger_setup_<timestamp>.md`
- [ ] Update `docs/next_prompt.md`

---

## Phase 2: ETL Extraction

### ETL structure

- [ ] Create `etl/extract.py`
- [ ] Create `etl/transform.py`
- [ ] Create `etl/load.py`
- [ ] Create `etl/schemas.py`

### JSON inspection

- [ ] Implement JSON file loader
- [ ] Implement safe JSON parsing
- [ ] Implement schema inspection for unknown JSON structures
- [ ] Detect Instagram JSON structure
- [ ] Detect WhatsApp JSON structure
- [ ] Return raw pandas DataFrame
- [ ] Log invalid JSON errors
- [ ] Log unsupported schema errors

### Manual scripts

- [ ] Create `scripts/inspect_json_schema.py`
- [ ] Allow manual inspection of JSON structure
- [ ] Print detected columns/keys
- [ ] Print sample records safely
- [ ] Document execution command

### Tests

- [ ] Create `tests/test_extract.py`
- [ ] Test valid JSON loading
- [ ] Test invalid JSON handling
- [ ] Test missing file handling
- [ ] Test unsupported schema handling

### Documentation

- [ ] Update `docs/context.md`
- [ ] Update `docs/tasks.md`
- [ ] Create session summary in `docs/sessions/`
- [ ] Update `docs/next_prompt.md`

---

## Phase 3: ETL Transformation

### Text normalization

- [ ] Implement lowercase normalization
- [ ] Implement accent removal
- [ ] Implement punctuation removal
- [ ] Implement whitespace normalization
- [ ] Implement emoji-safe cleaning strategy
- [ ] Preserve original message text
- [ ] Store normalized text separately

### Message normalization

- [ ] Standardize column `sender`
- [ ] Standardize column `message`
- [ ] Standardize column `message_normalized`
- [ ] Standardize column `timestamp`
- [ ] Standardize column `source`
- [ ] Parse Instagram timestamps
- [ ] Parse WhatsApp timestamps
- [ ] Handle missing messages
- [ ] Handle media/system messages
- [ ] Handle null timestamps
- [ ] Log transformation errors

### Tests

- [ ] Create `tests/test_transform.py`
- [ ] Test text normalization
- [ ] Test accent removal
- [ ] Test punctuation removal
- [ ] Test schema normalization
- [ ] Test invalid timestamps
- [ ] Test missing fields

### Documentation

- [ ] Update `docs/context.md`
- [ ] Update `docs/tasks.md`
- [ ] Create session summary in `docs/sessions/`
- [ ] Update `docs/next_prompt.md`

---

## Phase 4: ETL Load

### Database loading

- [ ] Implement `etl/load.py`
- [ ] Insert normalized messages into PostgreSQL
- [ ] Use batch insert
- [ ] Avoid duplicate inserts
- [ ] Use parameterized SQL
- [ ] Log insertion errors
- [ ] Return inserted row count
- [ ] Return skipped duplicate count

### Manual script

- [ ] Create `scripts/run_etl.py`
- [ ] Load Instagram JSON
- [ ] Load WhatsApp JSON
- [ ] Transform both sources
- [ ] Insert both into database
- [ ] Print ETL summary
- [ ] Document execution command

### Tests

- [ ] Create `tests/test_load.py`
- [ ] Test successful insert
- [ ] Test duplicate handling
- [ ] Test DB failure handling
- [ ] Test empty DataFrame handling

### Documentation

- [ ] Update `docs/context.md`
- [ ] Update `docs/tasks.md`
- [ ] Create session summary in `docs/sessions/`
- [ ] Update `docs/next_prompt.md`

---

## Phase 5: Analysis Preprocessing

- [ ] Create `analysis/preprocessing.py`
- [ ] Implement tokenization
- [ ] Implement stopword removal
- [ ] Implement optional lemmatization strategy
- [ ] Implement word frequency preprocessing
- [ ] Handle Spanish text
- [ ] Handle emojis
- [ ] Handle empty messages
- [ ] Add tests for preprocessing
- [ ] Update documentation

---

## Phase 6: Metrics

### Word metrics

- [ ] Create `analysis/metrics.py`
- [ ] Compute most frequent words
- [ ] Compute most frequent words by sender
- [ ] Compute keyword counts
- [ ] Normalize variations of `te amo`
- [ ] Count all variations of `te amo`
- [ ] Count `odio`
- [ ] Count `estresada`
- [ ] Add tests for keyword normalization

### Time metrics

- [ ] Compute message distribution by hour
- [ ] Compute message distribution by weekday
- [ ] Compute message count by sender
- [ ] Compute message count by source
- [ ] Compute conversation volume over time

### Conversation behavior metrics

- [ ] Detect who says good morning first per day
- [ ] Detect who says goodbye first per day
- [ ] Support Spanish variations of good morning
- [ ] Support Spanish variations of goodbye
- [ ] Add tests for first-message behavior logic

### Documentation

- [ ] Update `docs/context.md`
- [ ] Update `docs/tasks.md`
- [ ] Create session summary in `docs/sessions/`
- [ ] Update `docs/next_prompt.md`

---

## Phase 7: Sentiment Analysis

- [ ] Create `analysis/sentiment.py`
- [ ] Select lightweight Spanish-compatible sentiment approach
- [ ] Implement sentiment score per message
- [ ] Implement sentiment aggregation by sender
- [ ] Implement sentiment aggregation over time
- [ ] Handle neutral/empty messages
- [ ] Add tests for sentiment functions
- [ ] Document limitations of sentiment model
- [ ] Update documentation

---

## Phase 8: Streamlit Backend Integration

- [ ] Create `app/main.py`
- [ ] Create `app/utils/`
- [ ] Create Streamlit data loader
- [ ] Connect Streamlit to PostgreSQL
- [ ] Load messages using pandas
- [ ] Cache database reads with Streamlit cache
- [ ] Handle dashboard rendering errors
- [ ] Log Streamlit errors
- [ ] Add minimal smoke test
- [ ] Document `streamlit run app/main.py`

---

## Phase 9: Streamlit UI Components

- [ ] Create `app/components/overview.py`
- [ ] Create `app/components/time_charts.py`
- [ ] Create `app/components/word_analysis.py`
- [ ] Create `app/components/sentiment_view.py`
- [ ] Create overview metrics section
- [ ] Create hourly histogram
- [ ] Create weekday chart
- [ ] Create word frequency chart
- [ ] Create keyword count section
- [ ] Create sentiment section
- [ ] Add error-safe rendering wrappers
- [ ] Update documentation

---

## Phase 10: Styling

- [ ] Create `app/styles/`
- [ ] Define base layout spacing
- [ ] Define typography rules
- [ ] Define padding rules
- [ ] Define alignment rules
- [ ] Define background colors
- [ ] Prepare compatibility with `taste-skill`
- [ ] Apply consistent Streamlit styling
- [ ] Validate UI visually

---

## Phase 11: Automated Browser Testing

- [ ] Configure Playwright MCP usage notes
- [ ] Run Streamlit app locally
- [ ] Test app opens in Chromium headed mode
- [ ] Test overview section renders
- [ ] Test charts render
- [ ] Test error states render
- [ ] Document Playwright manual test flow
- [ ] Add smoke test checklist

---

## Phase 12: Deployment Preparation

- [ ] Review Streamlit free deployment constraints
- [ ] Prepare deployment requirements
- [ ] Add `.streamlit/config.toml` if needed
- [ ] Validate dependency size
- [ ] Ensure no credentials are committed
- [ ] Document deployment steps
- [ ] Add deployment troubleshooting notes

---

## Phase 13: Final Documentation

- [ ] Finalize `README.md`
- [ ] Finalize `docs/context.md`
- [ ] Finalize `docs/tasks.md`
- [ ] Add architecture summary
- [ ] Add ETL flow diagram description
- [ ] Add testing guide
- [ ] Add deployment guide
- [ ] Add known limitations
- [ ] Add future improvements