# Backbone CI

This document records the CI-level validation for the OMNIA backbone.

The CI workflow checks out and installs the three backbone repositories together:

OMNIA
  -> omnia-limit
  -> OMNIA-VALIDATION

The tested flow is:

OMNIA
  -> build_boundary_certificate_from_measurement()
  -> BoundaryCertificate
  -> omnia_limit.validate_certificate()
  -> omnia_validation.enveloper.process_boundary_step()
  -> ValidationEnvelope

This converts the backbone from a local Colab verification into a GitHub Actions regression check.
