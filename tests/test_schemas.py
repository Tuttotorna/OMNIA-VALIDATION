import pytest

from omnia_validation.schemas import (
    ALLOWED_RESULT_STATUSES,
    DEFAULT_BOUNDARY,
    REQUIRED_RESULT_FIELDS,
    is_valid_result_envelope,
    require_valid_result_envelope,
    validate_result_envelope,
)


def valid_result() -> dict:
    return {
        "experiment": "example_validator_v0",
        "status": "PASS",
        "created_at_utc": "2026-05-07T00:00:00+00:00",
        "boundary": DEFAULT_BOUNDARY,
        "payload": {
            "record_count": 1,
            "main_signal": "record_presence",
        },
    }


def test_schema_constants():
    assert ALLOWED_RESULT_STATUSES == frozenset({"PASS", "CHECK", "FAIL"})
    assert DEFAULT_BOUNDARY == "measurement != inference != decision"
    assert REQUIRED_RESULT_FIELDS == frozenset(
        {
            "experiment",
            "status",
            "created_at_utc",
            "boundary",
            "payload",
        }
    )


def test_validate_result_envelope_passes_valid_result():
    result = valid_result()

    errors = validate_result_envelope(result)

    assert errors == []


def test_is_valid_result_envelope_returns_true_for_valid_result():
    result = valid_result()

    assert is_valid_result_envelope(result)


def test_require_valid_result_envelope_accepts_valid_result():
    result = valid_result()

    require_valid_result_envelope(result)


def test_validate_result_envelope_detects_missing_fields():
    result = {
        "experiment": "example_validator_v0",
        "status": "PASS",
    }

    errors = validate_result_envelope(result)

    assert "missing required field: boundary" in errors
    assert "missing required field: created_at_utc" in errors
    assert "missing required field: payload" in errors


def test_validate_result_envelope_detects_invalid_status():
    result = valid_result()
    result["status"] = "UNKNOWN"

    errors = validate_result_envelope(result)

    assert "status must be one of: CHECK, FAIL, PASS" in errors


def test_validate_result_envelope_detects_empty_experiment():
    result = valid_result()
    result["experiment"] = ""

    errors = validate_result_envelope(result)

    assert "experiment must not be empty" in errors


def test_validate_result_envelope_detects_non_utc_timestamp():
    result = valid_result()
    result["created_at_utc"] = "2026-05-07T00:00:00"

    errors = validate_result_envelope(result)

    assert "created_at_utc should be UTC ISO-8601" in errors


def test_validate_result_envelope_accepts_z_suffix_timestamp():
    result = valid_result()
    result["created_at_utc"] = "2026-05-07T00:00:00Z"

    errors = validate_result_envelope(result)

    assert errors == []


def test_validate_result_envelope_detects_wrong_boundary():
    result = valid_result()
    result["boundary"] = "measurement == decision"

    errors = validate_result_envelope(result)

    assert "boundary should be: measurement != inference != decision" in errors


def test_validate_result_envelope_detects_non_object_payload():
    result = valid_result()
    result["payload"] = []

    errors = validate_result_envelope(result)

    assert "payload must be a mapping/object" in errors


def test_validate_result_envelope_detects_non_mapping_result():
    errors = validate_result_envelope([])  # type: ignore[arg-type]

    assert errors == ["result must be a mapping/object"]


def test_require_valid_result_envelope_raises_for_invalid_result():
    result = valid_result()
    result["status"] = "BROKEN"

    with pytest.raises(ValueError, match="Invalid result envelope"):
        require_valid_result_envelope(result)