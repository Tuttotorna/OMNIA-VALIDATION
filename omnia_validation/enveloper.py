from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from omnia_limit import BoundaryCertificate, validate_certificate


class ValidationEnvelope:
    """Final OMNIA-VALIDATION artifact freezing the boundary gate state."""

    def __init__(
        self,
        envelope_id: str,
        timestamp: str,
        status: str,
        details: dict[str, Any],
    ) -> None:
        self.payload = {
            "envelope_id": envelope_id,
            "timestamp": timestamp,
            "validation_status": status,
            "details": details,
        }


def process_boundary_step(raw_certificate: dict[str, Any]) -> dict[str, Any]:
    """Consume a BoundaryCertificate and produce a ValidationEnvelope."""
    try:
        cert: BoundaryCertificate = validate_certificate(raw_certificate)

        if cert.should_continue:
            status = "GATE_OPEN_MEASUREMENT_REQUIRED"
        else:
            status = "GATE_CLOSED_SATURATION_REACHED"

        details = {
            "target_repository": cert.target_repository,
            "certificate_id": cert.certificate_id,
            "reason": cert.reason,
            "saturation_detected": cert.saturation_detected,
            "ast_deformation_index": cert.ast_deformation_index,
            "perturbation_step": cert.perturbation_step,
        }

    except Exception as err:
        status = "GATE_ERROR_CONTRACT_VIOLATION"
        details = {
            "error": str(err),
            "error_type": type(err).__name__,
        }

    envelope = ValidationEnvelope(
        envelope_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        status=status,
        details=details,
    )

    return envelope.payload
