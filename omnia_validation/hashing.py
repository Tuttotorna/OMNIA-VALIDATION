"""Hashing utilities for reproducible structural validation artifacts."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

_SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")


def sha256_bytes(data: bytes) -> str:
    """Return the SHA-256 hexadecimal digest for raw bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str, *, encoding: str = "utf-8") -> str:
    """Return the SHA-256 hexadecimal digest for text."""
    return sha256_bytes(text.encode(encoding))


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 hexadecimal digest for a file.

    The file is read in chunks to avoid loading large artifacts fully in memory.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise IsADirectoryError(f"Not a file: {file_path}")

    digest = hashlib.sha256()

    with file_path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)

    return digest.hexdigest()


def is_sha256_hex(value: str) -> bool:
    """Return True when value is a valid SHA-256 hexadecimal string."""
    return bool(_SHA256_RE.fullmatch(value))

# ---------------------------------------------------------------------------
# Compatibility helpers for artifact manifest and CLI validation
# ---------------------------------------------------------------------------

def compute_file_sha256(path: object) -> str:
    """Compute the SHA-256 digest of a file.

    Boundary:
        measurement != inference != decision

    A matching hash proves byte-level artifact identity.
    It does not prove semantic correctness.
    """

    import hashlib
    from pathlib import Path

    file_path = Path(path)
    digest = hashlib.sha256()

    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def is_valid_sha256(value: object) -> bool:
    """Return True if value is a lowercase SHA-256 hexadecimal string."""

    if not isinstance(value, str):
        return False

    if len(value) != 64:
        return False

    return all(char in "0123456789abcdef" for char in value)
