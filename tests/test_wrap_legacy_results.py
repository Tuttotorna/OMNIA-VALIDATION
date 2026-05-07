from pathlib import Path

from examples.wrap_legacy_results_in_envelope import (
    infer_experiment_name,
    infer_legacy_status,
    wrap_legacy_result,
)
from omnia_validation.io import write_json
from omnia_validation.schemas import validate_result_envelope


def test_infer_experiment_name_from_path():
    path = Path("results/example_validator_v0.json")

    assert infer_experiment_name(path) == "example_validator_v0"


def test_infer_legacy_status_from_mapping():
    data = {
        "status": "legacy_status_value",
        "value": 1,
    }

    assert infer_legacy_status(data) == "legacy_status_value"


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