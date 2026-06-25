Read `README.md`, `docs/agents.md`, `docs/context.md`, and `docs/tasks.md`.

Current status:

1. Instagram Meta `.json` extraction is implemented in `etl/extract/instagram_extract.py`.
2. Instagram `.zip` handling discovers message JSON files inside Meta exports and returns records in memory.
3. WhatsApp `.txt` extraction parses exported chat messages into dictionaries in memory.
4. WhatsApp date parsing supports day/month and month/day dates with two-digit or four-digit years.
5. WhatsApp multiline message behavior is preserved.
6. Extraction does not write output to disk unless `etl.artifacts.save_stage_output()` is explicitly called, and does not insert into PostgreSQL.
7. ETL transformation is implemented in `etl/transform.py`.
8. Transformation normalizes Instagram and WhatsApp extracted dictionaries to:
   - `sender`
   - `message`
   - `message_normalized`
   - `timestamp`
   - `source`
9. Transformation preserves original message text and stores normalized text separately.
10. SQL remains outside ETL modules.
11. ETL staging artifacts are implemented in `etl/artifacts.py`.
12. Extracted artifacts are stored in `data/staging/extracted/`.
13. Transformed artifacts are stored in `data/staging/transformed/`.
14. Loading is implemented in `etl/load.py`.
15. Loading uses parameterized SQL from `db/queries.py` and the engine abstraction from `db/connection.py`.
16. Duplicate messages are skipped safely with `ON CONFLICT DO NOTHING`.
17. Read-only message database access is implemented in `db/messages.py`.
18. Message read SQL remains in `db/queries.py`.
19. Message read helpers use `get_engine()` from `db/connection.py`.
20. Manual ETL orchestration is implemented in `scripts/run_etl.py`.
21. The ETL runner extracts, transforms, optionally saves staging artifacts, and loads transformed records through existing modules.
22. Runner errors are logged with the centralized logger and re-raised.
23. Real data is already loaded in table messages.
24. Analysis preprocessing is implemented in `analysis/preprocessing.py`.
25. Preprocessing keeps ETL, database reads, SQL, metrics, sentiment analysis, and Streamlit dashboard logic separate.
26. Preprocessing returns copied message records with:
   - `message_preprocessed`
   - `message_tokens`
27. Preprocessing preserves original message fields.
28. Preprocessing supports Spanish text, accents, punctuation, emojis, and empty messages.
29. Preprocessing errors are logged through `logger/logger.py`.
30. Analysis metrics are implemented in `analysis/metrics.py`.
31. Metrics operate only on already-fetched or already-preprocessed records in memory.
32. Metrics do not add SQL, read PostgreSQL, run ETL, perform sentiment analysis, or add Streamlit dashboard logic.
33. Metrics can enrich copied records with:
   - `message_character_count`
   - `message_token_count`
34. Metrics can calculate aggregate counts by sender, source, day, hour, top tokens, totals, and averages.
35. Metrics errors are logged through `logger/logger.py`.
36. Analysis sentiment is implemented in `analysis/sentiment.py`.
37. Sentiment operates only on already-fetched or already-preprocessed records in memory.
38. Sentiment does not add SQL, read PostgreSQL, run ETL, calculate metrics, or add Streamlit dashboard logic.
39. Sentiment can enrich copied records with:
   - `sentiment_label`
   - `sentiment_score`
   - `sentiment_positive_token_count`
   - `sentiment_negative_token_count`
40. Sentiment uses deterministic Spanish lexicon scoring and existing preprocessing helpers for fallback tokenization.
41. Sentiment can calculate aggregate sentiment counts by label and average sentiment score.
42. Sentiment errors are logged through `logger/logger.py`.
43. Streamlit dashboard rendering is implemented in `app/main.py`.
44. Dashboard helper logic is implemented in `app/dashboard.py`.
45. Streamlit fetches messages only through `db.messages.fetch_messages()`.
46. Dashboard helper logic delegates preprocessing, metrics, and sentiment to existing analysis modules.
47. Streamlit does not expose database exception details to users.
48. Dashboard errors are logged through `logger/logger.py`.
49. No new dependencies were added for dashboard work.
50. Streamlit visual validation is complete.
51. `streamlit run app/main.py` now resolves project imports correctly when Streamlit executes from the `app/` directory.
52. Browser validation rendered dashboard summary metrics and charts from loaded message data.
53. A focused entrypoint bootstrap test is implemented in `tests/test_streamlit_entrypoint.py`.

Focused test status:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_streamlit_entrypoint.py tests/test_dashboard.py
```

Result:

```text
5 passed in 0.46s
```

Full test suite status:

```powershell
.\venv\Scripts\python.exe -m pytest tests/
```

Result:

```text
85 passed in 1.08s
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

Next task:

Review the romantic landing in the browser at `http://localhost:8501` and tune copy, spacing, or selected romantic phrases if needed. Keep ETL, database reads, logging, service aggregation, and Streamlit UI responsibilities separated.

Useful commands:

```powershell
.\venv\Scripts\python.exe -m pytest tests/
```

```powershell
streamlit run app/main.py
```

Latest status:

```text
Romantic landing business logic and visual refactor implemented.
Romantic visual system completion implemented.
Full suite: 88 passed in 1.62s
Streamlit local check: HTTP 200 at http://localhost:8501
Browser automation limitation: Chrome is not installed for Playwright visual validation.
```

```powershell
python scripts/run_etl.py data/raw/ig_message_1.json
```

```powershell
python scripts/run_etl.py data/raw/ig_message_1.json --save-artifacts
```

Return only file paths and file contents using:

# file: path/to/file.py

<content>
