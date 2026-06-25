# Streamlit Dashboard Session

## Objective

Implement the Streamlit dashboard without moving database reads, preprocessing, metrics, sentiment, ETL, or SQL into the UI layer.

## Changes

- Created `app/dashboard.py`.
- Added `prepare_dashboard_data()` for reusable dashboard data preparation over already fetched records.
- Added `dictionary_to_rows()` for deterministic grouped metric table rows.
- Updated `app/main.py` to fetch messages through `db.messages.fetch_messages()`.
- Rendered summary metrics, source charts, hourly charts, sentiment charts, top senders, top tokens, and message rows in Streamlit.
- Logged dashboard errors through `logger/logger.py`.
- Returned a generic safe Streamlit error message instead of exposing database exception details.
- Added `tests/test_dashboard.py`.

## Verification

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_dashboard.py
```

```text
4 passed in 0.06s
```

```powershell
.\venv\Scripts\python.exe -m pytest tests/
```

```text
84 passed in 1.63s
```

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8501 | Select-Object -ExpandProperty StatusCode
```

```text
200
```

## Command

Run the dashboard:

```powershell
streamlit run app/main.py
```
