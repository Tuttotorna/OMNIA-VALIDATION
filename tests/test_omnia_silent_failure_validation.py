"""
Tests for OMNIA Silent Failure validation artifact.

These tests protect the executable validation bridge between:

    OMNIA
    OMNIA-VALIDATION

They do not test semantic truth.

They test that the recorded validation artifact preserves the minimal
structural pattern:

    stable_output    -> Surface PASS -> OMNIA GO
    fragile_output   -> Surface PASS -> OMNIA RISK
    collapsed_output -> Surface FAIL -> OMNIA STOP

Core boundary:

    measurement != inference != decision
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

VALIDATOR_PATH = ROOT / "examples" / "validate_omnia_silent_failure_pattern.py"
RESULT_PATH = ROOT / "results" / "omnia_silent_failure_validation_result.json"

EXPECTED_BOUNDARY = "measurement != inference != decision"

EXPECTED_PATTERN = {
    "stable_output": {
        "surface_status": "PASS",
        "omnia_status": "GO",
    },
    "fragile_output": {
        "surface_status": "PASS",
        "omnia_status": "RISK",
    },
    "collapsed_output": {
        "surface_status": "FAIL",
        "omnia_status": "STOP",
    },
}


def load_artifact() -> dict:
    assert RESULT_PATH.exists(), f"Missing validation artifact: {RESULT_PATH}"
    return json.loads(RESULT_PATH.read_text(encoding="utf-8"))


def test_validator_script_exists() -> None:
    assert VALIDATOR_PATH.exists(), f"Missing validator script: {VALIDATOR_PATH}"
    assert VALIDATOR_PATH.is_file()


def test_validation_artifact_exists() -> None:
    assert RESULT_PATH.exists(), f"Missing validation artifact: {RESULT_PATH}"
    assert RESULT_PATH.is_file()


def test_validation_artifact_identity() -> None:
    artifact = load_artifact()

    assert artifact["artifact_type"] == "omnia_silent_failure_validation_result"
    assert artifact["status"] == "PASS"
    assert artifact["failures"] == []


def test_validation_artifact_boundary() -> None:
    artifact = load_artifact()

    assert artifact["validation_target"]["boundary"] == EXPECTED_BOUNDARY
    assert artifact["interpretation"]["boundary"] == EXPECTED_BOUNDARY

    for item in artifact["raw_results"]:
        assert item["boundary"] == EXPECTED_BOUNDARY


def test_observed_pattern_matches_expected_pattern() -> None:
    artifact = load_artifact()

    assert artifact["validation_target"]["expected_pattern"] == EXPECTED_PATTERN
    assert artifact["observed_pattern"] == EXPECTED_PATTERN


def test_fragile_output_is_surface_pass_and_omnia_risk() -> None:
    artifact = load_artifact()

    fragile = artifact["observed_pattern"]["fragile_output"]

    assert fragile["surface_status"] == "PASS"
    assert fragile["omnia_status"] == "RISK"


def test_stable_output_is_surface_pass_and_omnia_go() -> None:
    artifact = load_artifact()

    stable = artifact["observed_pattern"]["stable_output"]

    assert stable["surface_status"] == "PASS"
    assert stable["omnia_status"] == "GO"


def test_collapsed_output_is_surface_fail_and_omnia_stop() -> None:
    artifact = load_artifact()

    collapsed = artifact["observed_pattern"]["collapsed_output"]

    assert collapsed["surface_status"] == "FAIL"
    assert collapsed["omnia_status"] == "STOP"


def test_hashes_are_recorded() -> None:
    artifact = load_artifact()

    hashes = artifact["hashes"]

    assert isinstance(hashes["stdout_sha256"], str)
    assert isinstance(hashes["raw_results_sha256"], str)
    assert len(hashes["stdout_sha256"]) == 64
    assert len(hashes["raw_results_sha256"]) == 64

    source = artifact["source"]

    assert isinstance(source["demo_file_sha256"], str)
    assert len(source["demo_file_sha256"]) == 64


def test_non_claims_are_preserved() -> None:
    artifact = load_artifact()

    non_claims = set(artifact["interpretation"]["non_claims"])

    assert "semantic correctness" in non_claims
    assert "factual truth" in non_claims
    assert "AI safety" in non_claims
    assert "deployment approval" in non_claims
    assert "benchmark replacement" in non_claims


def test_central_case_is_declared() -> None:
    artifact = load_artifact()

    assert artifact["validation_target"]["central_case"] == "fragile_output"
    assert artifact["validation_target"]["central_expected_pattern"] == {
        "surface_status": "PASS",
        "omnia_status": "RISK",
    }
