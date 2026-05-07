"""JSON and JSONL IO utilities for OMNIA-VALIDATION."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json(path: str | Path) -> Any:
    """Read a JSON file."""
    file_path = Path(path)

    with file_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, data: Any, *, indent: int = 2) -> None:
    """Write JSON with deterministic formatting."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=indent, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    """Read a JSONL file as a list of dictionaries."""
    file_path = Path(path)
    records: list[dict[str, Any]] = []

    with file_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()

            if not stripped:
                continue

            value = json.loads(stripped)

            if not isinstance(value, dict):
                raise ValueError(
                    f"JSONL line {line_number} in {file_path} is not an object"
                )

            records.append(value)

    return records


def write_jsonl(path: str | Path, records: list[dict[str, Any]]) -> None:
    """Write dictionaries to a JSONL file with deterministic key ordering."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as handle:
        for record in records:
            if not isinstance(record, dict):
                raise TypeError("write_jsonl expects a list of dictionaries")

            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            handle.write("\n")