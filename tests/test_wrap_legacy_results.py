from pathlib import Path

from examples.wrap_legacy_results_in_envelope import (
    DEFAULT_STATUS,
    infer_experiment_name,
    infer_legacy_status,
    wrap_legacy_result,
)
from omnia_validation.io import write_json
from omnia_validation.schemas import validate_result_envelope


def test_default_status_is_check():
    assert DEFAULT_STATUS == "CHECK"


def test_infer_experiment_name_from_path():
    path = Path("results/example_validator_v0.json")

    assert infer_experiment_name(path) == "example_validator_v0"


def test_infer_experiment_name_removes_only_suffix():
    path = Path("results/example.validator.v0.json")

    assert infer_experiment_name(path) == "example.validator.v0"


def test_infer_legacy_status_from_mapping():
    data = {
        "status": "legacy_status_value",
        "value": 1,
    }

    assert infer_legacy_status(data) == "legacy_status_value"


def test_infer_legacy_status_returns_none_when_missing():
    data = {
        "value": 1,
    }

    assert infer_legacy_status(data) is None


def test_infer_legacy_status_from_non_mapping():
    data = ["not", "a", "mapping"]

    assert infer_legacy_status(data) is None


def test_wrap_legacy_result_produces_valid_envelope(tmp_path: Path):
    legacy_path = tmp_path / "legacy_result_v0.json"

    legacy_data = {
        "status": "legacy_passed",
        "score": 0.75,
        "details": {
            "example": True,
        },
    }

    write_json(legacy_path, legacy_data)

    wrapped = wrap_legacy_result(legacy_path)
    errors = validate_result_envelope(wrapped)

    assert errors == []
    assert wrapped["experiment"] == "legacy_result_v0"
    assert wrapped["status"] == "CHECK"
    assert wrapped["boundary"] == "measurement != inference != decision"

    payload = wrapped["payload"]

    assert payload["legacy_result_path"] == str(legacy_path)
    assert payload["legacy_status"] == "legacy_passed"
    assert payload["legacy_result"] == legacy_data
    assert "normalization_note" in payload


def test_wrap_legacy_result_preserves_legacy_result_without_status(tmp_path: Path):
    legacy_path = tmp_path / "legacy_without_status_v0.json"

    legacy_data = {
        "score": 0.33,
        "notes": ["legacy", "artifact"],
    }

    write_json(legacy_path, legacy_data)

    wrapped = wrap_legacy_result(legacy_path)
    errors = validate_result_envelope(wrapped)

    assert errors == []

    payload = wrapped["payload"]

    assert wrapped["experiment"] == "legacy_without_status_v0"
    assert wrapped["status"] == "CHECK"
    assert payload["legacy_status"] is None
    assert payload["legacy_result"] == legacy_data


def test_wrap_legacy_result_preserves_nested_payload(tmp_path: Path):
    legacy_path = tmp_path / "nested_legacy_v0.json"

    legacy_data = {
        "status": "legacy_drift",
        "metrics": {
            "aggregate_risk_score": 0.379255,
            "aggregate_risk_regime": "DRIFT",
            "regime_counts": {
                "CRITICAL": 4,
                "DRIFT": 10,
                "STABLE": 6,
            },
        },
        "records": [
            {
                "id": "a",
                "score": 0.1,
            },
            {
                "id": "b",
                "score": 0.9,
            },
        ],
    }

    write_json(legacy_path, legacy_data)

    wrapped = wrap_legacy_result(legacy_path)
    errors = validate_result_envelope(wrapped)

    assert errors == []

    payload = wrapped["payload"]

    assert payload["legacy_status"] == "legacy_drift"
    assert payload["legacy_result"] == legacy_data
    assert payload["legacy_result"]["metrics"]["aggregate_risk_regime"] == "DRIFT"
    assert payload["legacy_result"]["records"][1]["score"] == 0.9


def test_wrap_legacy_result_uses_check_because_it_is_not_revalidation(tmp_path: Path):
    legacy_path = tmp_path / "legacy_pass_result_v0.json"

    legacy_data = {
        "status": "PASS",
        "message": "Legacy file already claimed PASS.",
    }

    write_json(legacy_path, legacy_data)

    wrapped = wrap_legacy_result(legacy_path)

    assert wrapped["status"] == "CHECK"
    assert wrapped["payload"]["legacy_status"] == "PASS"
    assert "not scientific revalidation" in wrapped["payload"]["normalization_note"]