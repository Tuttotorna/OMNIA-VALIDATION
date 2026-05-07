"""OMNIA-VALIDATION core utilities.

This package contains reusable support functions for the OMNIA-VALIDATION
experimental repository.

Boundary:
    measurement != inference != decision
"""

from .hashing import is_sha256_hex, sha256_bytes, sha256_file, sha256_text
from .io import read_json, read_jsonl, write_json, write_jsonl
from .metrics import compression_ratio, normalized_repetition_score, shannon_entropy

__all__ = [
    "compression_ratio",
    "is_sha256_hex",
    "normalized_repetition_score",
    "read_json",
    "read_jsonl",
    "sha256_bytes",
    "sha256_file",
    "sha256_text",
    "shannon_entropy",
    "write_json",
    "write_jsonl",
]