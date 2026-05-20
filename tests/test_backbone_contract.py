from omnia_validation.enveloper import process_boundary_step


def test_valid_boundary_certificate_payload():
    mock_certificate = {
        "metadata": {
            "certificate_id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
            "timestamp": "2026-05-20T20:00:00Z",
            "target_repository": "OMNIA-CORE-TEST",
        },
        "metrics": {
            "ast_deformation_index": 0.42,
            "perturbation_step": 3,
        },
        "boundary_status": {
            "should_continue": False,
            "saturation_detected": True,
            "reason": "Structural saturation reached",
        },
    }

    envelope = process_boundary_step(mock_certificate)

    assert envelope["validation_status"] == "GATE_CLOSED_SATURATION_REACHED"
    assert "envelope_id" in envelope
    assert envelope["details"]["certificate_id"] == (
        "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
    )
    assert envelope["details"]["target_repository"] == "OMNIA-CORE-TEST"
    assert envelope["details"]["saturation_detected"] is True
    assert envelope["details"]["ast_deformation_index"] == 0.42
    assert envelope["details"]["perturbation_step"] == 3


def test_open_gate_boundary_certificate_payload():
    mock_certificate = {
        "metadata": {
            "certificate_id": "open-gate-cert",
            "timestamp": "2026-05-20T20:00:00Z",
            "target_repository": "OMNIA-CORE-TEST",
        },
        "metrics": {
            "ast_deformation_index": 0.12,
            "perturbation_step": 1,
        },
        "boundary_status": {
            "should_continue": True,
            "saturation_detected": False,
            "reason": "Additional measurement still yields structural information",
        },
    }

    envelope = process_boundary_step(mock_certificate)

    assert envelope["validation_status"] == "GATE_OPEN_MEASUREMENT_REQUIRED"
    assert envelope["details"]["certificate_id"] == "open-gate-cert"
    assert envelope["details"]["saturation_detected"] is False


def test_invalid_boundary_certificate_payload():
    broken_certificate = {
        "metadata": {
            "certificate_id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
            "timestamp": "2026-05-20T20:00:00Z",
            "target_repository": "OMNIA-CORE-TEST",
        },
        "metrics": {
            "ast_deformation_index": 0.42,
        },
    }

    envelope = process_boundary_step(broken_certificate)

    assert envelope["validation_status"] == "GATE_ERROR_CONTRACT_VIOLATION"
    assert envelope["details"]["error_type"] in {
        "ValidationError",
        "SchemaError",
        "FileNotFoundError",
        "KeyError",
    }
