# MB-X.01 LON Entry Point CI

## Status

The OMNIA-VALIDATION CI workflow now runs the MB-X.01 / L.O.N. ecosystem entry point documentation test.

This makes the public entry point part of the executable validation surface.

## Entry point test

    python -m pytest -q tests/test_mbx01_lon_entrypoint_documentation.py

## Purpose

The entry point test protects the public orientation layer for the full ecosystem.

It verifies that the reader-facing document preserves:

    MB-X.01 identity
    L.O.N. identity
    canonical backbone
    core repositories
    compliant satellites
    layer separation rules
    forbidden overclaims
    links to executable tests
    README entry point markers

## Protected backbone statement

    OMNIA measurement
      -> BoundaryCertificate
      -> omnia-limit validate_certificate()
      -> OMNIA-VALIDATION ValidationEnvelope
      -> CI regression
      -> compliant producer / adapter / consumer / observer

## Protected layer rules

    measurement != validation
    validation != orchestration
    orchestration != decision
    decision != measurement
    observation != decision
    domain adaptation != backbone redefinition

## Boundary

This CI step does not create a new backbone contract.

It protects the public entry point that explains the existing contract.
