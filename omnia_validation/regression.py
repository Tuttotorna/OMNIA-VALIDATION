"""Result regression helpers for OMNIA-VALIDATION.

Boundary:
    measurement != inference != decision

This module classifies structural differences between result artifacts.
It does not decide semantic truth, scientific correctness, or production safety.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from omnia_validation.schemas import validate_result_envelope

NO_REGRESSION = "NO_REGRESSION"
EXPECTED_DRIFT = "EXPECTED_DRIFT"
SCHEMA_REGRESSION = "SCHEMA_REGRESSION"
STATUS_REGRESSION = "STATUS_REGRESSION"
BOUNDARY_REGRESSION = "BOUNDARY_REGRESSION"
PAYLOAD_REGRESSION = "PAYLOAD_REGRESSION"
HASH_REGRESSION = "HASH_REGRESSION"

REGRESSION_CLASSIFICATIONS = {
    NO_REGRESSION,
    EXPECTED_DRIFT,
    SCHEMA_REGRESSION,
    STATUS_REGRESSION,
    BOUNDARY_REGRESSION,
    PAYLOAD_REGRESSION,
    HASH_REGRESSION,
}

EXPECTED_DRIFT_FIELDS = {
    "created_at_utc",
}


def read_result_file(path: str | Path) -> dict[str, Any]:
    """Read a JSON result file."""

    result_path = Path(path)
    data = json.loads(result_path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError(f"result must be a JSON object: {result_path}")

    return data


def _status_for_classification(classification: str) -> str:
    if classification == NO_REGRESSION:
        return "PASS"

    if classification == EXPECTED_DRIFT:
        return "CHECK"

    return "FAIL"


def _without_expected_drift_fields(result: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in result.items()
        if key not in EXPECTED_DRIFT_FIELDS
    }


def _only_expected_drift_changed(
    previous: dict[str, Any],
    current: dict[str, Any],
) -> bool:
    if previous == current:
        return False

    return _without_expected_drift_fields(previous) == _without_expected_drift_fields(current)


def _artifact_hash_map(result: dict[str, Any]) -> dict[str, str]:
    payload = result.get("payload")

    if not isinstance(payload, dict):
        return {}

    artifacts = payload.get("artifacts")

    if not isinstance(artifacts, list):
        return {}

    mapping: dict[str, str] = {}

    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue

        artifact_path = artifact.get("artifact_path")
        sha256 = artifact.get("sha256")

        if isinstance(artifact_path, str) and isinstance(sha256, str):
            mapping[artifact_path] = sha256

    return mapping


def _hash_regression_detected(
    previous: dict[str, Any],
    current: dict[str, Any],
) -> bool:
    previous_hashes = _artifact_hash_map(previous)
    current_hashes = _artifact_hash_map(current)

    common_paths = set(previous_hashes) & set(current_hashes)

    for artifact_path in common_paths:
        if previous_hashes[artifact_path] != current_hashes[artifact_path]:
            return True

    return False


def classify_result_regression(
    previous: dict[str, Any],
    current: dict[str, Any],
) -> dict[str, Any]:
    """Classify the difference between two result artifacts.

    The returned object uses the canonical OMNIA-VALIDATION result envelope.
    """

    # Boundary changes are classified before full schema validation because
    # changing the boundary string also makes the current envelope invalid.
    # That invalidity is specifically a boundary regression, not a generic
    # schema regression.
    if (
        "boundary" in previous
        and "boundary" in current
        and previous.get("boundary") != current.get("boundary")
    ):
        classification = BOUNDARY_REGRESSION
    else:
        previous_schema_errors = validate_result_envelope(previous)
        current_schema_errors = validate_result_envelope(current)

        if previous_schema_errors or current_schema_errors:
            classification = SCHEMA_REGRESSION
            return {
                "experiment": "result_regression_comparison_v0",
                "status": _status_for_classification(classification),
                "created_at_utc": "2026-05-07T00:00:00+00:00",
                "boundary": "measurement != inference != decision",
                "payload": {
                    "classification": classification,
                    "previous_schema_errors": previous_schema_errors,
                    "current_schema_errors": current_schema_errors,
                },
            }

        if previous == current:
            classification = NO_REGRESSION
        elif _only_expected_drift_changed(previous, current):
            classification = EXPECTED_DRIFT
        elif previous.get("status") != current.get("status"):
            classification = STATUS_REGRESSION
        elif _hash_regression_detected(previous, current):
            classification = HASH_REGRESSION
        elif previous.get("payload") != current.get("payload"):
            classification = PAYLOAD_REGRESSION
        else:
            classification = PAYLOAD_REGRESSION

    return {
        "experiment": "result_regression_comparison_v0",
        "status": _status_for_classification(classification),
        "created_at_utc": "2026-05-07T00:00:00+00:00",
        "boundary": "measurement != inference != decision",
        "payload": {
            "classification": classification,
            "previous_status": previous.get("status"),
            "current_status": current.get("status"),
            "previous_boundary": previous.get("boundary"),
            "current_boundary": current.get("boundary"),
            "changed_top_level_fields": [
                key
                for key in sorted(set(previous) | set(current))
                if previous.get(key) != current.get(key)
            ],
            "interpretation": {
                "correct": [
                    "result differences are classified structural evidence",
                    "NO_REGRESSION means compared artifacts are structurally identical",
                    "EXPECTED_DRIFT means only accepted drift fields changed",
                ],
                "incorrect": [
                    "NO_REGRESSION proves semantic truth",
                    "EXPECTED_DRIFT proves scientific correctness",
                    "regression classification replaces external review",
                ],
            },
        },
    }


def compare_result_files(
    previous_path: str | Path,
    current_path: str | Path,
) -> dict[str, Any]:
    """Read and classify two result files."""

    previous = read_result_file(previous_path)
    current = read_result_file(current_path)

    result = classify_result_regression(previous, current)
    result["payload"]["previous_path"] = str(previous_path)
    result["payload"]["current_path"] = str(current_path)

    return result

