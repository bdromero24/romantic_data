# Session 0 - Project Setup & Architecture Initialization

## 🎯 Objective
Initialize the full project structure for a modular Streamlit application that analyzes conversation data (Instagram + WhatsApp JSON), including ETL, database design, logging system, and base architecture.

---

## 🧱 Final Project Structure

project_root/

├── app/
│   ├── main.py
│   ├── components/
│   ├── styles/
│   └── utils/
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── schemas.py
│
├── analysis/
│   ├── sentiment.py
│   ├── metrics.py
│   └── preprocessing.py
│
├── db/
│   ├── connection.py
│   ├── queries.py
│   └── schema.sql
│
├── logger/
│   ├── logger.py
│   └── config.py
│
├── data/
│   └── raw/
│
├── docs/
│   ├── context.md
│   ├── tasks.md
│   ├── next_prompt.md
│   └── sessions/
│
└── requirements.txt

---

## ⚙️ Design Principles

1. Each script handles ONE responsibility only
2. No business logic inside Streamlit UI
3. ETL fully decoupled from analysis
4. Database interactions isolated
5. Logging centralized and reusable
6. Functions must be reusable and testable

---

## 🔄 ETL Responsibilities

### extract.py
- Load JSON files (Instagram, WhatsApp)
- Detect schema dynamically
- Return raw pandas DataFrames

### transform.py
- Normalize structure across sources
- Standardize columns:
  - sender
  - message
  - timestamp
  - source
- Clean text:
  - lowercase
  - remove accents
  - remove punctuation

### load.py
- Insert data into PostgreSQL
- Use batch inserts
- Avoid duplicates

### schemas.py
- Define expected schema mappings
- Handle unknown formats safely

---

## 🗄️ DATABASE DESIGN

### Tables

#### messages
- id (PK)
- sender
- message
- timestamp
- source

#### logs
- id (PK)
- error_type
- message
- timestamp

---

## 🧠 DB MODULE

### connection.py
- Create reusable connection engine

### queries.py
- ALL queries must be parameterized
- No raw string concatenation

Examples:
- count messages
- count words
- group by hour
- group by day
- keyword frequency

---

## 🧾 LOGGER SYSTEM

### Requirements

1. Log levels:
   - CRITICAL (mandatory)
2. Outputs:
   - .txt file
   - PostgreSQL table

### logger.py
- Central logging function

### config.py
- Logging format
- File path

### Must capture:

- Database errors:
  - ProgrammingError
  - DatabaseError
  - ConnectionError

- ETL errors
- Streamlit rendering errors

Each log must include:
- error_type
- message
- timestamp

---

## Implemented Analysis And Dashboard

- Deterministic preprocessing in `analysis/preprocessing.py`
- In-memory metrics in `analysis/metrics.py`
- Deterministic Spanish lexicon sentiment in `analysis/sentiment.py`
- Streamlit dashboard in `app/main.py`
- Reusable dashboard data helpers in `app/dashboard.py`

---

## 🧪 EXECUTION REQUIREMENTS

- Python 3.10+
- Local PostgreSQL running
- Streamlit installed

---

## 📤 OUTPUT FORMAT (STRICT FOR CODEX)

Return ONLY:

1. File creations (with paths)
2. No explanations
3. No repeated code
4. Modular functions only

---

## 📌 TASKS COMPLETED

- [x] Project structure defined
- [x] Responsibilities separated
- [x] Logging system designed
- [x] ETL architecture defined
- [x] Database schema defined

---

## 📌 FIRST TASKS

- [ ] Implement db/schema.sql
- [ ] Implement db/connection.py
- [ ] Implement logger system
- [ ] Implement ETL (extract)

---

## 🧠 NEXT PROMPT (AUTO-GENERATED)

Implement:

1. db/schema.sql
2. db/connection.py
3. logger/logger.py
4. logger/config.py

Requirements:
- PostgreSQL connection
- Table creation
- Logging to file + DB
- Error handling for:
  - ProgrammingError
  - DatabaseError
  - ConnectionError

Return only code files.

---

## Local Commands

Initialize database schema:

```bash
python scripts/init_db.py
```

Test database connection:

```bash
python scripts/test_db_connection.py
```

Run unit tests:

```bash
.\venv\Scripts\python.exe -m pytest tests/
```

If the virtual environment is activated, this is equivalent to:

```bash
pytest tests/
```

Latest local verification:

```text
Focused dashboard entrypoint tests: 5 passed in 0.46s
Full suite: 85 passed in 1.08s
Streamlit dashboard visually validated at http://localhost:8501
```

Run Instagram extraction through the dispatcher:

```bash
python -c "from etl.extract.extract_dispatcher import extract_messages; extract_messages('data/raw/ig_message_1.json')"
```

Run transformation for already extracted records:

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

python -c "from etl.artifacts import load_records; from etl.load import load_messages; records = load_records('data/staging/transformed/transformed_instagram_20260608_192214.parquet'); print(load_messages(records))"
```

Run the manual ETL runner:

```bash
python scripts/run_etl.py data/raw/ig_message_1.json
-- 
python -m scripts.run_etl data/raw/ig_message_1.json
python -m scripts.run_etl data/raw/ig_message_2.json
python -m scripts.run_etl data/raw/WhatsApp_Chat_with_Mar🍓.txt
```

Run the manual ETL runner and save staging artifacts:

```bash
python scripts/run_etl.py data/raw/ig_message_1.json --save-artifacts
```

Read loaded message count from PostgreSQL:

```bash
python -c "from db.messages import count_all_messages; print(count_all_messages())"
```

Run Streamlit entrypoint:

```bash
streamlit run app/main.py
```

## Romantic Landing Configuration

The sender used for her-only metrics is configured in:

```text
app/content_config.py
```

```python
HER_SENDER_NAME = "sender value stored in messages.sender"
```

The `Hater de tiempo completo` card counts real occurrences of the whole words
`odio` and `hate` in her valid `message_normalized` messages.
