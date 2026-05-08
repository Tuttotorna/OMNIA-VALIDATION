from __future__ import annotations

import json
from pathlib import Path

from omnia_validation.regression import (
    BOUNDARY_REGRESSION,
    EXPECTED_DRIFT,
    HASH_REGRESSION,
    NO_REGRESSION,
    PAYLOAD_REGRESSION,
    SCHEMA_REGRESSION,
    STATUS_REGRESSION,
    classify_result_regression,
    compare_result_files,
)
from omnia_validation.schemas import validate_result_envelope


def _result(payload: dict | None = None) -> dict:
    return {
        "experiment": "example_result_v0",
        "status": "CHECK",
        "created_at_utc": "2026-05-07T00:00:00+00:00",
        "boundary": "measurement != inference != decision",
        "payload": payload or {"value": 1},
    }


def test_classify_no_regression() -> None:
    previous = _result()
    current = _result()

    comparison = classify_result_regression(previous, current)

    assert comparison["status"] == "PASS"
    assert comparison["payload"]["classification"] == NO_REGRESSION
    assert validate_result_envelope(comparison) == []


def test_classify_expected_drift_for_created_at_only() -> None:
    previous = _result()
    current = _result()
    current["created_at_utc"] = "2030-01-01T00:00:00+00:00"

    comparison = classify_result_regression(previous, current)

    assert comparison["status"] == "CHECK"
    assert comparison["payload"]["classification"] == EXPECTED_DRIFT


def test_classify_schema_regression() -> None:
    previous = _result()
    current = {"payload": {}}

    comparison = classify_result_regression(previous, current)

    assert comparison["status"] == "FAIL"
    assert comparison["payload"]["classification"] == SCHEMA_REGRESSION
    assert comparison["payload"]["current_schema_errors"]


def test_classify_boundary_regression() -> None:
    previous = _result()
    current = _result()
    current["boundary"] = "changed boundary"

    comparison = classify_result_regression(previous, current)

    assert comparison["status"] == "FAIL"
    assert comparison["payload"]["classification"] == BOUNDARY_REGRESSION


def test_classify_status_regression() -> None:
    previous = _result()
    current = _result()
    current["status"] = "FAIL"

    comparison = classify_result_regression(previous, current)

    assert comparison["status"] == "FAIL"
    assert comparison["payload"]["classification"] == STATUS_REGRESSION


def test_classify_payload_regression() -> None:
    previous = _result({"value": 1})
    current = _result({"value": 2})

    comparison = classify_result_regression(previous, current)

    assert comparison["status"] == "FAIL"
    assert comparison["payload"]["classification"] == PAYLOAD_REGRESSION


def test_classify_hash_regression() -> None:
    previous = _result(
        {
            "artifacts": [
                {
                    "artifact_path": "data/example.jsonl",
                    "sha256": "a" * 64,
                }
            ]
        }
    )
    current = _result(
        {
            "artifacts": [
                {
                    "artifact_path": "data/example.jsonl",
                    "sha256": "b" * 64,
                }
            ]
        }
    )

    comparison = classify_result_regression(previous, current)

    assert comparison["status"] == "FAIL"
    assert comparison["payload"]["classification"] == HASH_REGRESSION


def test_compare_result_files(tmp_path: Path) -> None:
    previous_path = tmp_path / "previous.json"
    current_path = tmp_path / "current.json"

    previous_path.write_text(json.dumps(_result()), encoding="utf-8")
    current_path.write_text(json.dumps(_result()), encoding="utf-8")

    comparison = compare_result_files(previous_path, current_path)

    assert comparison["status"] == "PASS"
    assert comparison["payload"]["classification"] == NO_REGRESSION
    assert comparison["payload"]["previous_path"] == str(previous_path)
    assert comparison["payload"]["current_path"] == str(current_path)

