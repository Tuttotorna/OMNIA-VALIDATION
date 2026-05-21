# MB-X.01 / L.O.N. Ecosystem Entry Point

## Purpose

This document is the public entry point for the MB-X.01 / Logical Origin Node ecosystem.

It exists for readers who arrive from outside the project and need one clear orientation layer before entering the individual repositories.

The ecosystem is not a single monolithic system.

It is a separated structural-validation architecture.

The core principle is:

    measurement != validation
    validation != orchestration
    orchestration != decision
    decision != measurement
    observation != decision
    domain adaptation != backbone redefinition

The value of the ecosystem exists only while those boundaries remain preserved.

## Minimal definition

MB-X.01 / L.O.N. is an open structural-validation ecosystem built around a canonical backbone:

    OMNIA measurement
      -> BoundaryCertificate
      -> omnia-limit validate_certificate()
      -> OMNIA-VALIDATION ValidationEnvelope
      -> CI regression
      -> compliant producer / adapter / consumer / observer

The ecosystem does not ask the reader to trust intention.

It exposes roles, boundaries, registry files, CI tests, and executable regression paths.

## What L.O.N. means here

L.O.N. stands for Logical Origin Node.

In this software ecosystem, the term means:

    a root reference frame for preserving structural role separation

It does not mean consciousness.

It does not mean agency.

It does not mean semantic truth.

It does not mean mystical authority.

It means that the system has a declared origin point for structural consistency, contract preservation, and boundary verification.

## What MB-X.01 means here

MB-X.01 is the ecosystem identifier.

It names the full multi-repository architecture around OMNIA, L.O.N., and the compliant satellite repositories.

It is useful because the ecosystem is larger than any single repository.

    MB-X.01 = ecosystem layer
    L.O.N.  = root reference / origin node
    OMNIA   = measurement backbone component

## Core backbone repositories

### OMNIA

Role:

    measurement_artifact_emitter

OMNIA emits BoundaryCertificate-compatible artifacts from structural measurements.

OMNIA does not own downstream validation.

OMNIA does not decide.

OMNIA does not emit semantic truth.

### omnia-limit

Role:

    boundary_contract_validator

omnia-limit validates the BoundaryCertificate contract.

It owns the canonical boundary validation API.

It does not measure.

It does not orchestrate.

It does not decide.

### OMNIA-VALIDATION

Role:

    control_plane_validator
    ci_regression_anchor
    ecosystem_standard_owner

OMNIA-VALIDATION consumes BoundaryCertificate artifacts.

It validates through omnia-limit.

It emits ValidationEnvelope artifacts.

It owns the executable regression surface for the backbone.

## Compliant satellite repositories

### OMNIAMIND

Role:

    orchestrator

OMNIAMIND may orchestrate compliant producers, adapters, consumers, and observers.

It must not become a parallel validation layer.

It must not become a decision engine.

### OMNIA-RADAR

Role:

    observer

OMNIA-RADAR observes validated backbone output.

It must not mutate the canonical contract.

It must not validate directly.

### OMNIA-INVARIANCE

Role:

    producer_adapter

OMNIA-INVARIANCE adapts invariance measurements into BoundaryCertificate-compatible artifacts.

It owns generic invariance adaptation.

It must not emit final truth claims.

### OMNIA-CRYPTO

Role:

    domain_adapter

OMNIA-CRYPTO maps crypto-domain measurements into the OMNIA-INVARIANCE / OMNIA backbone path.

It must not duplicate generic invariance primitives.

It must not emit crypto/security decisions.

### OMNIA-SECURITY

Role:

    security_consumer_domain_adapter

OMNIA-SECURITY consumes and adapts security-domain measurements.

It must not emit final secure / unsafe / approved / blocked decisions.

### OMNIA-CONSTANT

Role:

    constant_stability_producer_adapter

OMNIA-CONSTANT adapts constant/stability measurements.

It must not emit absolute constancy claims.

### OMNIA-THREE-BODY

Role:

    domain_experiment_producer_adapter

OMNIA-THREE-BODY adapts three-body / trajectory measurements.

It must not emit final physical-truth claims.

### OMNIABASE

Role:

    base_invariance_producer_adapter

OMNIABASE adapts multi-base / base-invariance measurements.

It must not emit final base-independent mathematical truth claims.

### lon-mirror

Role:

    root_reference_observer

lon-mirror acts as root reference observer.

It may route measurements through the existing backbone for reference checks.

It must not become a validator, control plane, governance engine, decision engine, or semantic-truth engine.

## What the ecosystem is allowed to do

The ecosystem is allowed to:

    measure structural behavior
    emit measurement artifacts
    validate boundary certificates
    emit validation envelopes
    run executable regressions
    document repository roles
    detect layer drift
    preserve contract boundaries
    adapt domain measurements into the backbone
    observe validated outputs
    orchestrate compliant components

## What the ecosystem is not allowed to claim

The ecosystem is not allowed to claim:

    semantic truth
    final mathematical truth
    final physical truth
    absolute constancy
    security approval
    crypto correctness
    governance decisions
    consciousness
    agency
    meaning interpretation

Any repository that emits those as final conclusions is outside the declared backbone boundary.

## Reader path

For a first-time reader, use this order:

    1. README.md
    2. docs/MBX01_LON_ECOSYSTEM_ENTRYPOINT.md
    3. docs/ECOSYSTEM_MAP.md
    4. docs/ECOSYSTEM_STATUS.md
    5. docs/ECOSYSTEM_BACKBONE_COMPLIANCE_REGISTRY.md
    6. docs/ecosystem_backbone_compliance_registry.json
    7. tests/test_end_to_end_backbone.py
    8. tests/test_ecosystem_backbone_compliance_registry.py
    9. tests/test_ecosystem_map_documentation.py
    10. tests/test_mbx01_lon_entrypoint_documentation.py

## Machine-readable registry

The machine-readable registry is:

    docs/ecosystem_backbone_compliance_registry.json

That file records:

    repository
    github URL
    role
    status
    commit
    commit message
    responsibility
    forbidden behavior
    counts by status
    counts by role

## Executable protection

The ecosystem is protected by tests.

Important tests include:

    tests/test_end_to_end_backbone.py
    tests/test_ecosystem_backbone_compliance_registry.py
    tests/test_ecosystem_status_documentation.py
    tests/test_ecosystem_map_documentation.py
    tests/test_mbx01_lon_entrypoint_documentation.py

The entry point itself is not passive documentation.

It has an executable documentation test.

## Minimal mental model

The ecosystem should be understood like this:

    OMNIA measures.
    omnia-limit validates the boundary certificate.
    OMNIA-VALIDATION validates the control-plane envelope.
    OMNIAMIND orchestrates.
    Satellites adapt, observe, or consume.
    lon-mirror acts as root reference observer.
    No satellite owns the backbone.
    No layer silently replaces another layer.

## Final boundary

The ecosystem remains valid only while the following statement remains true:

    measurement != validation != orchestration != decision

This entry point exists to make that boundary visible before the reader enters the technical details.
