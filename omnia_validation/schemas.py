"""Schema helpers for OMNIA-VALIDATION result artifacts.

These validators are intentionally minimal.

They check structural shape only.
They do not validate semantic truth.

Boundary:
    measurement != inference != decision
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

ALLOWED_RESULT_STATUSES = frozenset({"PASS", "CHECK", "FAIL"})

REQUIRED_RESULT_FIELDS = frozenset(
    {
        "experiment",
        "status",
        "created_at_utc",
        "boundary",
        "payload",
    }
)

DEFAULT_BOUNDARY = "measurement != inference != decision"


def validate_result_envelope(result: Mapping[str, Any]) -> list[str]:
    """Validate the canonical OMNIA-VALIDATION result envelope.

    Returns a list of error messages.

    An empty list means the envelope passed the structural schema check.
    """
    errors: list[str] = []

    if not isinstance(result, Mapping):
        return ["result must be a mapping/object"]

    missing_fields = sorted(REQUIRED_RESULT_FIELDS - set(result.keys()))
    for field in missing_fields:
        errors.append(f"missing required field: {field}")

    experiment = result.get("experiment")
    if "experiment" in result and not isinstance(experiment, str):
        errors.append("experiment must be a string")
    elif isinstance(experiment, str) and not experiment.strip():
        errors.append("experiment must not be empty")

    status = result.get("status")
    if "status" in result and not isinstance(status, str):
        errors.append("status must be a string")
    elif isinstance(status, str) and status not in ALLOWED_RESULT_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_RESULT_STATUSES))
        errors.append(f"status must be one of: {allowed}")

    created_at_utc = result.get("created_at_utc")
    if "created_at_utc" in result and not isinstance(created_at_utc, str):
        errors.append("created_at_utc must be a string")
    elif isinstance(created_at_utc, str):
        if not created_at_utc.strip():
            errors.append("created_at_utc must not be empty")
        if "+00:00" not in created_at_utc and not created_at_utc.endswith("Z"):
            errors.append("created_at_utc should be UTC ISO-8601")

    boundary = result.get("boundary")
    if "boundary" in result and not isinstance(boundary, str):
        errors.append("boundary must be a string")
    elif isinstance(boundary, str) and boundary != DEFAULT_BOUNDARY:
        errors.append(f"boundary should be: {DEFAULT_BOUNDARY}")

    payload = result.get("payload")
    if "payload" in result and not isinstance(payload, Mapping):
        errors.append("payload must be a mapping/object")

    return errors


def is_valid_result_envelope(result: Mapping[str, Any]) -> bool:
    """Return True when a result envelope passes the structural schema check."""
    return not validate_result_envelope(result)


def require_valid_result_envelope(result: Mapping[str, Any]) -> None:
    """Raise ValueError if a result envelope fails the structural schema check."""
    errors = validate_result_envelope(result)

    if errors:
        joined = "; ".join(errors)
        raise ValueError(f"Invalid result envelope: {joined}")