"""Manual JSON schema inspection script for conversation exports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from etl.extract import inspect_json_schema, load_json_file


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a conversation JSON export schema."
    )
    parser.add_argument("json_path", type=Path)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    data = load_json_file(arguments.json_path)
    schema = inspect_json_schema(data)
    print(json.dumps(schema, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
