# OMNIA Ecosystem Map

## What this ecosystem is

The OMNIA ecosystem is a public structural-validation backbone.

Its purpose is not to generate answers, interpret meaning, or decide truth.

Its purpose is to preserve a strict software chain where measurements, boundary validation, control-plane validation, orchestration, observation, and domain adaptation remain separate.

The core rule is:

    measurement != validation
    validation != orchestration
    orchestration != decision
    decision != measurement

The ecosystem exists to prevent layer collapse.

## Canonical backbone

The current canonical backbone is:

    OMNIA measurement
      -> BoundaryCertificate
      -> omnia-limit validate_certificate()
      -> OMNIA-VALIDATION ValidationEnvelope
      -> CI regression
      -> compliant producer / adapter / consumer / observer

Each layer has a bounded role.

No layer is allowed to silently replace another layer.

## Core repositories

### OMNIA

Role:

    measurement_artifact_emitter

OMNIA emits BoundaryCertificate-compatible artifacts from structural measurements.

OMNIA does not own downstream validation.

OMNIA does not make governance decisions.

OMNIA does not emit semantic truth.

### omnia-limit

Role:

    boundary_contract_validator

omnia-limit validates the BoundaryCertificate contract.

It owns the boundary validation API.

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

## Compliant satellites

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

## Role separation

The ecosystem remains valid only if these separations remain true:

    measurement != validation
    validation != orchestration
    orchestration != decision
    decision != measurement
    observation != decision
    domain adaptation != backbone redefinition

This is the main architectural boundary.

## What the ecosystem does not claim

The ecosystem does not claim:

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

The ecosystem measures, validates contracts, preserves boundaries, and exposes executable regressions.

It does not decide what the world means.

## Where to start

Start here:

1. README.md

   Public entry point.

2. docs/ECOSYSTEM_STATUS.md

   Current public ecosystem status.

3. docs/ECOSYSTEM_BACKBONE_COMPLIANCE_REGISTRY.md

   Formal registry of repository roles, commits, responsibilities, and forbidden boundaries.

4. docs/ecosystem_backbone_compliance_registry.json

   Machine-readable registry.

5. tests/test_ecosystem_backbone_compliance_registry.py

   Executable registry protection.

6. tests/test_end_to_end_backbone.py

   End-to-end backbone validation.

## Minimal mental model

The ecosystem is not one repo pretending to do everything.

It is a separated chain:

    OMNIA measures.
    omnia-limit validates the boundary certificate.
    OMNIA-VALIDATION validates the control-plane envelope.
    OMNIAMIND orchestrates.
    Satellites adapt, observe, or consume.
    No satellite owns the backbone.

This is the point.

The backbone is valuable only while the roles remain separated.

<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:START -->
## lon-mirror root reference public link

lon-mirror exposes the public root reference side of the MB-X.01 / L.O.N. ecosystem.

Public link:

https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

Verified commit:

22a320d

Role:

root_reference_observer

Boundary:

observation != decision
<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:END -->

<!-- LON-MIRROR PUBLIC ENTRYPOINT REGISTRATION:START -->
## lon-mirror public entry point

`lon-mirror` now exposes a public first-reader doorway for its root reference observer role.

repository: lon-mirror
role: root_reference_observer
status: satellite_compliant
registry_commit: 22a320d
public_entrypoint_commit: f74b799
public_root_reference_commit: 22a320d

Links:

lon-mirror public entry point:
https://github.com/Tuttotorna/lon-mirror/blob/main/docs/PUBLIC_ENTRYPOINT.md

lon-mirror root reference link:
https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

Boundary:

lon-mirror observes.
lon-mirror does not validate independently.
lon-mirror does not replace OMNIA.
lon-mirror does not replace omnia-limit.
lon-mirror does not replace OMNIA-VALIDATION.
lon-mirror does not emit semantic truth.
lon-mirror does not make governance decisions.
<!-- LON-MIRROR PUBLIC ENTRYPOINT REGISTRATION:END -->

<!-- FIRST READER PATH COMMIT REGISTRATION:START -->
## First reader path commits

The public first-reader path is registered as a reader-facing orientation layer.

OMNIA-VALIDATION:
  first_reader_path_commit: 83fa07f
  first_reader_path_link: https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/FIRST_READER_PATH.md

lon-mirror:
  first_reader_path_commit: 4dd5cb5
  latest_first_reader_path_commit: 4dd5cb5
  first_reader_path_link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/FIRST_READER_PATH.md
  public_entrypoint_commit: f74b799
  latest_public_commit: f74b799
  root_reference_commit: 22a320d

Boundary:
  first-reader path != validation
  first-reader path != measurement
  first-reader path != orchestration
  first-reader path != decision
<!-- FIRST READER PATH COMMIT REGISTRATION:END -->
