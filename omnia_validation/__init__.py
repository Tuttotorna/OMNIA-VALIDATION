"""OMNIA-VALIDATION core utilities.

This package contains reusable support functions for the OMNIA-VALIDATION
experimental repository.

Boundary:
    measurement != inference != decision
"""

from .hashing import is_sha256_hex, sha256_bytes, sha256_file, sha256_text
from .io import read_json, read_jsonl, write_json, write_jsonl
from .metrics import compression_ratio, normalized_repetition_score, shannon_entropy
from .schemas import (
    ALLOWED_RESULT_STATUSES,
    DEFAULT_BOUNDARY,
    REQUIRED_RESULT_FIELDS,
    is_valid_result_envelope,
    require_valid_result_envelope,
    validate_result_envelope,
)

__all__ = [
    "ALLOWED_RESULT_STATUSES",
    "DEFAULT_BOUNDARY",
    "REQUIRED_RESULT_FIELDS",
    "compression_ratio",
    "is_sha256_hex",
    "is_valid_result_envelope",
    "normalized_repetition_score",
    "read_json",
    "read_jsonl",
    "require_valid_result_envelope",
    "sha256_bytes",
    "sha256_file",
    "sha256_text",
    "shannon_entropy",
    "validate_result_envelope",
    "write_json",
    "write_jsonl",
]