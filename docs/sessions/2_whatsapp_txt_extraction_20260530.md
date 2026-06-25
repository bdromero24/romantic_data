# Session 2 - WhatsApp TXT Extraction

## Objective

Add a focused extraction package for WhatsApp `.txt` exports and source discovery while preparing the project for pending Instagram exports.

## Implemented

- Created `etl/extract/file_discovery.py`.
- Created `etl/extract/whatsapp_extract.py`.
- Created `etl/extract/extract_dispatcher.py`.
- Converted `etl.extract` into a package entry point while preserving legacy JSON helper imports.
- Added source detection for WhatsApp `.txt` files.
- Added source detection for Instagram `.json` and `.zip` files.
- Added WhatsApp datetime, single-line, and multiline parsing.
- Added dispatcher routing for WhatsApp extraction.
- Added pending Instagram dispatcher behavior with `NotImplementedError`.
- Added focused unit tests under `tests/`.

## Current Source Support

WhatsApp `.txt` is the official source format currently supported. Messages are parsed into dictionaries in memory and are not converted into physical JSON.

Instagram extraction remains pending. The project detects Instagram `.json` and `.zip` exports from Meta, but extraction is not implemented yet.

## Execution

Run all tests:

```bash
pytest tests/
```

Run focused extraction tests:

```bash
pytest tests/test_file_discovery.py tests/test_whatsapp_extract.py tests/test_extract_dispatcher.py
```

Manual JSON schema inspection remains available:

```bash
python scripts/inspect_json_schema.py data/raw/example.json
```
