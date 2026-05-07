"""Artifact metadata helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .hashing import sha256_file


def utc_now_iso() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def file_metadata(path: str | Path) -> dict[str, Any]:
    """Return basic reproducibility metadata for a file."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    stat = file_path.stat()

    return {
        "path": str(file_path),
        "size_bytes": stat.st_size,
        "sha256": sha256_file(file_path),
    }


def result_envelope(
    *,
    experiment: str,
    status: str,
    payload: dict[str, Any],
    boundary: str = "measurement != inference != decision",
) -> dict[str, Any]:
    """Build a standard result envelope for validation outputs."""
    return {
        "experiment": experiment,
        "status": status,
        "created_at_utc": utc_now_iso(),
        "boundary": boundary,
        "payload": payload,
    }