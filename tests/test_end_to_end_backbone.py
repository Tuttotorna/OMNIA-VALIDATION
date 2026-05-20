from omnia import build_boundary_certificate_from_measurement
from omnia_limit import BoundaryCertificate, validate_certificate
from omnia_validation.enveloper import process_boundary_step


def test_end_to_end_backbone_stop_flow():
    measurement = {
        "drift_score": 0.33,
        "perturbation_step": 2,
        "gate_status": "STOP",
        "omega": 0.7,
        "sei": 0.01,
        "iri": 0.98,
    }

    raw_certificate = build_boundary_certificate_from_measurement(
        measurement,
        target_repository="OMNIA",
        certificate_id="e2e-stop-cert",
        timestamp="2026-05-20T20:00:00Z",
    )

    validated_certificate = validate_certificate(raw_certificate)
    envelope = process_boundary_step(raw_certificate)

    assert isinstance(validated_certificate, BoundaryCertificate)
    assert validated_certificate.certificate_id == "e2e-stop-cert"
    assert validated_certificate.target_repository == "OMNIA"
    assert validated_certificate.ast_deformation_index == 0.33
    assert validated_certificate.perturbation_step == 2
    assert validated_certificate.should_continue is False
    assert validated_certificate.saturation_detected is True

    assert envelope["validation_status"] == "GATE_CLOSED_SATURATION_REACHED"
    assert envelope["details"]["certificate_id"] == "e2e-stop-cert"
    assert envelope["details"]["target_repository"] == "OMNIA"
    assert envelope["details"]["saturation_detected"] is True
    assert envelope["details"]["ast_deformation_index"] == 0.33
    assert envelope["details"]["perturbation_step"] == 2


def test_end_to_end_backbone_continue_flow():
    measurement = {
        "delta_omega": 0.12,
        "perturbation_step": 1,
        "gate_status": "CONTINUE",
        "omega": 0.91,
        "sei": 0.20,
        "iri": 0.40,
        "reason": "Additional measurement still yields structural information",
    }

    raw_certificate = build_boundary_certificate_from_measurement(
        measurement,
        target_repository="OMNIA",
        certificate_id="e2e-continue-cert",
        timestamp="2026-05-20T20:00:00Z",
    )

    validated_certificate = validate_certificate(raw_certificate)
    envelope = process_boundary_step(raw_certificate)

    assert isinstance(validated_certificate, BoundaryCertificate)
    assert validated_certificate.certificate_id == "e2e-continue-cert"
    assert validated_certificate.target_repository == "OMNIA"
    assert validated_certificate.ast_deformation_index == 0.12
    assert validated_certificate.perturbation_step == 1
    assert validated_certificate.should_continue is True
    assert validated_certificate.saturation_detected is False

    assert envelope["validation_status"] == "GATE_OPEN_MEASUREMENT_REQUIRED"
    assert envelope["details"]["certificate_id"] == "e2e-continue-cert"
    assert envelope["details"]["target_repository"] == "OMNIA"
    assert envelope["details"]["saturation_detected"] is False
    assert envelope["details"]["ast_deformation_index"] == 0.12
    assert envelope["details"]["perturbation_step"] == 1


def test_end_to_end_backbone_contract_violation_flow():
    broken_certificate = {
        "metadata": {
            "certificate_id": "e2e-broken-cert",
            "timestamp": "2026-05-20T20:00:00Z",
            "target_repository": "OMNIA",
        },
        "metrics": {
            "ast_deformation_index": 0.33,
            "perturbation_step": 2,
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
