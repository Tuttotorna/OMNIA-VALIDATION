# End-to-end backbone validation test

This document records the first end-to-end software check across the OMNIA backbone.

Verified flow:

OMNIA
  -> build_boundary_certificate_from_measurement()
  -> BoundaryCertificate
  -> omnia_limit.validate_certificate()
  -> OMNIA-VALIDATION process_boundary_step()
  -> ValidationEnvelope

Meaning:

The ecosystem no longer relies only on documentation-level compatibility between the core measurement engine, boundary validator, and validation control plane.

The following software boundary is now tested:

OMNIA measurement artifact
  -> schema-compatible BoundaryCertificate
  -> omnia-limit contract validation
  -> OMNIA-VALIDATION envelope emission

Test file:

tests/test_end_to_end_backbone.py

Covered cases:

1. stop / saturation flow
2. continue / measurement-required flow
3. invalid contract / violation flow

Boundary:

OMNIA emits a machine-readable measurement artifact.

omnia-limit validates the boundary contract.

OMNIA-VALIDATION emits the final ValidationEnvelope.

No semantic decision is introduced inside the measurement layer.
