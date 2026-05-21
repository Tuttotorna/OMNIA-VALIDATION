# Ecosystem Map CI

## Status

The OMNIA-VALIDATION CI workflow now runs the ecosystem map documentation test.

This makes the public ecosystem map part of the executable validation surface.

## CI command

    python -m pytest -q tests/test_ecosystem_map_documentation.py

## Purpose

The test protects the public map of the OMNIA ecosystem.

It verifies that the map still exposes:

    OMNIA measurement
    BoundaryCertificate
    omnia-limit validate_certificate()
    OMNIA-VALIDATION ValidationEnvelope
    CI regression

It also verifies that the map still lists the compliant satellites:

    OMNIAMIND
    OMNIA-RADAR
    OMNIA-INVARIANCE
    OMNIA-CRYPTO
    OMNIA-SECURITY
    OMNIA-CONSTANT
    OMNIA-THREE-BODY
    OMNIABASE
    lon-mirror

## Protected layer rules

    measurement != validation
    validation != orchestration
    orchestration != decision
    decision != measurement
    observation != decision
    domain adaptation != backbone redefinition

## Boundary

This CI step does not create a new contract.

It only verifies that the public ecosystem map remains aligned with the already declared backbone and registry.
