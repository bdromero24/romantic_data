# Streamlit Visual Validation Session

## Objective

Run and visually validate the Streamlit dashboard without moving ETL, database SQL, preprocessing, metrics, or sentiment logic into the UI layer.

## Changes

- Updated `app/main.py` to add `ensure_project_root_on_path()` before project imports.
- Kept dashboard data fetching through `db.messages.fetch_messages()`.
- Kept preprocessing, metrics, and sentiment delegation inside existing modules.
- Added `tests/test_streamlit_entrypoint.py` for the Streamlit direct-run import bootstrap.
- Updated project documentation after validation.

## Validation

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_streamlit_entrypoint.py tests/test_dashboard.py
```

```text
5 passed in 0.46s
```

```powershell
.\venv\Scripts\python.exe -m pytest tests/
```

```text
85 passed in 1.08s
```

```powershell
streamlit run app/main.py
```

```text
Dashboard opened at http://localhost:8501.
Playwright Chromium screenshot validation rendered summary metrics and charts.
```

## Notes

- Playwright MCP could not launch Google Chrome because Chrome was missing at the expected local path.
- The repository Playwright CLI used bundled Chromium for validation without adding dependencies.
