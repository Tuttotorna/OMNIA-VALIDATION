"""OMNIA-VALIDATION package.

Reusable validation utilities for the OMNIA-VALIDATION repository.

Boundary:
    measurement != inference != decision

This package provides support utilities for:

- hashing
- JSON / JSONL IO
- simple structural metrics
- metadata envelopes
- result schema validation
- artifact manifest validation

It does not validate semantic truth.
It does not certify production safety.
It does not make final decisions.
"""

from __future__ import annotations

from omnia_validation.hashing import (
    compute_file_sha256,
    is_valid_sha256,
)
from omnia_validation.io import (
    read_json,
    read_jsonl,
    write_json,
    write_jsonl,
)
from omnia_validation.manifest import (
    VALID_ARTIFACT_ROLES,
    is_valid_artifact_manifest,
    require_valid_artifact_manifest,
    validate_artifact_entry,
    validate_artifact_manifest,
)
from omnia_validation.metadata import (
    build_file_metadata,
    build_result_envelope,
    utc_now_iso,
)
from omnia_validation.metrics import (
    compression_ratio,
    normalized_repetition_score,
    shannon_entropy,
)
from omnia_validation.schemas import (
    ALLOWED_RESULT_STATUSES,
    REQUIRED_RESULT_FIELDS,
    is_valid_result_envelope,
    require_valid_result_envelope,
    validate_result_envelope,
)

__all__ = [
    "ALLOWED_RESULT_STATUSES",
    "REQUIRED_RESULT_FIELDS",
    "VALID_ARTIFACT_ROLES",
    "build_file_metadata",
    "build_result_envelope",
    "compression_ratio",
    "compute_file_sha256",
    "is_valid_artifact_manifest",
    "is_valid_result_envelope",
    "is_valid_sha256",
    "normalized_repetition_score",
    "read_json",
    "read_jsonl",
    "require_valid_artifact_manifest",
    "require_valid_result_envelope",
    "shannon_entropy",
    "utc_now_iso",
    "validate_artifact_entry",
    "validate_artifact_manifest",
    "validate_result_envelope",
    "write_json",
    "write_jsonl",
]

__version__ = "0.1.0"