# OMNIA Ecosystem Backbone Compliance Registry

## Status

This document is the official backbone compliance registry for the OMNIA ecosystem.

It records which repositories have been aligned to the canonical software chain and which role each repository is allowed to play.

This is not a conceptual map.

This is the current integration registry for the validated OMNIA backbone.

## Canonical backbone

    OMNIA measurement
      -> BoundaryCertificate
      -> omnia-limit validate_certificate()
      -> OMNIA-VALIDATION ValidationEnvelope
      -> CI regression
      -> satellite compliant producer / adapter / consumer / observer

## Current compliance count

    total registered entries: 14
    backbone core entries:    5
    satellite compliant:      9

## Registry table

| Repository | Status | Role | Commit | Contract position |
|---|---|---|---|---|
| `omnia-limit` | `backbone_core` | `boundary_contract_validator` | `26352c7` | Validates BoundaryCertificate schema and exposes the canonical boundary-state API. |
| `OMNIA` | `backbone_core` | `measurement_artifact_emitter` | `e4d2b39` | Emits BoundaryCertificate-compatible artifacts from OMNIA measurements. |
| `OMNIA-VALIDATION` | `backbone_core` | `control_plane_validator` | `394c6e3` | Consumes BoundaryCertificate artifacts, validates through omnia-limit, and emits ValidationEnvelope artifacts. |
| `OMNIA-VALIDATION` | `backbone_core` | `ci_regression_anchor` | `3fcdb2f` | Runs the canonical backbone regression path in GitHub Actions. |
| `OMNIA-VALIDATION` | `backbone_core` | `ecosystem_standard_owner` | `803b793` | Defines the minimum ecosystem integration standard and satellite compliance rules. |
| `OMNIAMIND` | `satellite_compliant` | `orchestrator` | `7f75b2d` | Orchestrates compliant producers, adapters, and consumers without replacing the backbone. |
| `OMNIA-RADAR` | `satellite_compliant` | `observer` | `3987745` | Observes validated backbone output without modifying the canonical contract. |
| `OMNIA-INVARIANCE` | `satellite_compliant` | `producer_adapter` | `4f4c453` | Adapts invariance measurements into BoundaryCertificate-compatible artifacts. |
| `OMNIA-CRYPTO` | `satellite_compliant` | `domain_adapter` | `010b680` | Maps crypto-domain measurements into the OMNIA-INVARIANCE / OMNIA backbone path. |
| `OMNIA-SECURITY` | `satellite_compliant` | `security_consumer_domain_adapter` | `c2524d0` | Consumes and adapts security-domain measurements while preserving decision boundaries. |
| `OMNIA-CONSTANT` | `satellite_compliant` | `constant_stability_producer_adapter` | `2c05176` | Adapts constant/stability measurements into BoundaryCertificate-compatible artifacts. |
| `OMNIA-THREE-BODY` | `satellite_compliant` | `domain_experiment_producer_adapter` | `bba656b` | Adapts three-body / trajectory measurements into BoundaryCertificate-compatible artifacts. |
| `OMNIABASE` | `satellite_compliant` | `base_invariance_producer_adapter` | `67bbae0` | Adapts multi-base / base-invariance measurements into BoundaryCertificate-compatible artifacts. |
| `lon-mirror` | `satellite_compliant` | `root_reference_observer` | `7404822` | Acts as root reference observer and may route measurements through the existing backbone for reference checks. |

## Current verified commits

- `omnia-limit`: `26352c7` - Add BoundaryCertificate API without breaking legacy limit API
- `OMNIA`: `e4d2b39` - Add BoundaryCertificate emission bridge
- `OMNIA-VALIDATION`: `394c6e3` - Add end-to-end backbone validation test
- `OMNIA-VALIDATION`: `3fcdb2f` - Run backbone end-to-end test in CI
- `OMNIA-VALIDATION`: `803b793` - Document backbone contract standard
- `OMNIAMIND`: `7f75b2d` - Add backbone-compliant orchestration bridge
- `OMNIA-RADAR`: `3987745` - Add backbone-compliant observer bridge
- `OMNIA-INVARIANCE`: `4f4c453` - Add backbone-compliant invariance adapter
- `OMNIA-CRYPTO`: `010b680` - Add backbone-compliant crypto domain adapter
- `OMNIA-SECURITY`: `c2524d0` - Add backbone-compliant security domain adapter
- `OMNIA-CONSTANT`: `2c05176` - Add backbone-compliant constant stability adapter
- `OMNIA-THREE-BODY`: `bba656b` - Add backbone-compliant three-body trajectory adapter
- `OMNIABASE`: `67bbae0` - Add backbone-compliant base-invariance adapter
- `lon-mirror`: `7404822` - Add backbone-compliant root reference observer

## Layer separation

    measurement != validation
    validation != orchestration
    orchestration != decision
    decision != measurement
    observation != decision
    domain adaptation != backbone redefinition

## Backbone core

### OMNIA

Role:

    measurement_artifact_emitter

OMNIA emits BoundaryCertificate-compatible artifacts from measurements.

OMNIA does not own downstream validation.

OMNIA does not own final governance decisions.

OMNIA does not emit semantic truth.

### omnia-limit

Role:

    boundary_contract_validator

omnia-limit validates the BoundaryCertificate contract.

omnia-limit owns the canonical boundary validation API.

omnia-limit does not measure.

omnia-limit does not orchestrate.

omnia-limit does not decide semantic truth.

### OMNIA-VALIDATION

Role:

    control_plane_validator
    ci_regression_anchor
    ecosystem_standard_owner

OMNIA-VALIDATION consumes BoundaryCertificate artifacts.

OMNIA-VALIDATION validates through omnia-limit.

OMNIA-VALIDATION emits ValidationEnvelope artifacts.

OMNIA-VALIDATION owns the end-to-end regression path.

## Satellite roles

### OMNIAMIND

    orchestrator

OMNIAMIND may orchestrate compliant producers, adapters, consumers, and observers.

OMNIAMIND must not become a parallel control plane.

### OMNIA-RADAR

    observer

OMNIA-RADAR observes validated backbone output.

OMNIA-RADAR must not mutate the canonical contract.

### OMNIA-INVARIANCE

    producer_adapter

OMNIA-INVARIANCE owns generic invariance adaptation.

It may produce or adapt invariance measurements into BoundaryCertificate-compatible artifacts.

### OMNIA-CRYPTO

    domain_adapter

OMNIA-CRYPTO maps crypto-domain measurements into the OMNIA-INVARIANCE / OMNIA backbone path.

It must not duplicate generic invariance primitives.

### OMNIA-SECURITY

    security_consumer_domain_adapter

OMNIA-SECURITY consumes and adapts security-domain measurements.

It must not emit final secure / unsafe / approved / blocked decisions.

### OMNIA-CONSTANT

    constant_stability_producer_adapter

OMNIA-CONSTANT adapts constant/stability measurements.

It must not emit absolute constancy claims.

### OMNIA-THREE-BODY

    domain_experiment_producer_adapter

OMNIA-THREE-BODY adapts three-body / trajectory measurements.

It must not emit final physical-truth claims.

### OMNIABASE

    base_invariance_producer_adapter

OMNIABASE adapts multi-base / base-invariance measurements.

It must not emit final base-independent mathematical truth claims.

### lon-mirror

    root_reference_observer

lon-mirror acts as root reference observer.

It may route measurements through the existing backbone for reference checks.

It must not become a validator, control plane, decision engine, governance engine, or semantic-truth engine.

## Forbidden behavior by repository

- `omnia-limit` must not perform: semantic truth decision, measurement ownership, orchestration replacement.
- `OMNIA` must not perform: downstream validation ownership, governance decision, semantic truth decision.
- `OMNIA-VALIDATION` must not perform: measurement replacement, schema bypass, hidden continuation policy.
- `OMNIA-VALIDATION` must not perform: local-only compatibility, README-only compatibility, untested cross-repository handoff.
- `OMNIA-VALIDATION` must not perform: parallel validation contract, satellite contract drift, layer collapse.
- `OMNIAMIND` must not perform: BoundaryCertificate redefinition, ValidationEnvelope redefinition, control-plane replacement, semantic decision.
- `OMNIA-RADAR` must not perform: BoundaryCertificate redefinition, ValidationEnvelope redefinition, direct validation ownership, decision engine behavior.
- `OMNIA-INVARIANCE` must not perform: BoundaryCertificate redefinition, ValidationEnvelope redefinition, validation bypass, final truth claim.
- `OMNIA-CRYPTO` must not perform: generic invariance primitive duplication, BoundaryCertificate redefinition, ValidationEnvelope redefinition, security or crypto decision claim.
- `OMNIA-SECURITY` must not perform: secure or unsafe final decision, approved or blocked decision, BoundaryCertificate redefinition, ValidationEnvelope redefinition.
- `OMNIA-CONSTANT` must not perform: absolute constancy claim, BoundaryCertificate redefinition, ValidationEnvelope redefinition, decision engine behavior.
- `OMNIA-THREE-BODY` must not perform: physical truth claim, BoundaryCertificate redefinition, ValidationEnvelope redefinition, decision engine behavior.
- `OMNIABASE` must not perform: base-independent truth claim, final mathematical truth claim, BoundaryCertificate redefinition, ValidationEnvelope redefinition.
- `lon-mirror` must not perform: semantic truth claim, governance decision, BoundaryCertificate redefinition, ValidationEnvelope redefinition, decision engine behavior.

## Compliance acceptance rule

A repository is compliant only if all of the following remain true:

    1. It has a declared backbone role.
    2. It does not redefine BoundaryCertificate.
    3. It does not redefine ValidationEnvelope.
    4. It validates only through omnia-limit.
    5. It emits envelopes only through OMNIA-VALIDATION.
    6. It does not replace OMNIA.
    7. It does not replace omnia-limit.
    8. It does not replace OMNIA-VALIDATION.
    9. It has a regression test or is covered by the control-plane CI path.
    10. It does not emit final semantic, physical, security, mathematical, governance, or absolute-truth decisions.

## Current ecosystem state

    BACKBONE CORE:
      OMNIA
      omnia-limit
      OMNIA-VALIDATION

    COMPLIANT ORCHESTRATOR:
      OMNIAMIND

    COMPLIANT OBSERVERS:
      OMNIA-RADAR
      lon-mirror

    COMPLIANT PRODUCERS / ADAPTERS / CONSUMERS:
      OMNIA-INVARIANCE
      OMNIA-CRYPTO
      OMNIA-SECURITY
      OMNIA-CONSTANT
      OMNIA-THREE-BODY
      OMNIABASE

## Final principle

The ecosystem remains valid only while the layers stay separated.

    measurement != validation
    validation != orchestration
    orchestration != decision
    decision != measurement

The registry exists to prevent backbone drift.

<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:START -->
## lon-mirror public root reference link

lon-mirror is the public root reference observer for the MB-X.01 / L.O.N. ecosystem.

Verified public link:

https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

Verified commit:

22a320d

Registered role:

root_reference_observer

Registered status:

satellite_compliant

Boundary:

lon-mirror observes validated backbone output and exposes the public root reference path.

It must not become a validator, control plane, governance engine, decision engine, or semantic-truth engine.
<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:END -->

<!-- LON-MIRROR PUBLIC ENTRYPOINT REGISTRATION:START -->
## lon-mirror public entry point registration

The `lon-mirror` registry entry keeps its root-reference registry commit while also recording the newer public entry point commit.

repository: lon-mirror
role: root_reference_observer
status: satellite_compliant
current_registered_commit: 22a320d
commit_message: Link MB-X.01 LON ecosystem entry point
public_entrypoint_commit: f74b799
public_entrypoint_link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/PUBLIC_ENTRYPOINT.md
public_root_reference_commit: 22a320d
public_root_reference_link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

This preserves compatibility with the existing root-reference registration test.

This does not change the layer boundary.

`lon-mirror` remains an observer, not a validator, not a control plane, not a governance engine, not a decision engine, and not a semantic-truth engine.
<!-- LON-MIRROR PUBLIC ENTRYPOINT REGISTRATION:END -->

<!-- FIRST READER PATH COMMIT REGISTRATION:START -->
## First reader path commit registration

The registry now records the public first-reader path commits.

OMNIA-VALIDATION:
  first_reader_path_commit: 83fa07f
  first_reader_path_link: https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/FIRST_READER_PATH.md

lon-mirror:
  registry_commit: 22a320d
  public_entrypoint_commit: f74b799
  latest_public_commit: f74b799
  first_reader_path_commit: 4dd5cb5
  latest_first_reader_path_commit: 4dd5cb5
  first_reader_path_link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/FIRST_READER_PATH.md

This registration does not change the backbone contract.

The first-reader path is orientation only.

first-reader path != validation
first-reader path != measurement
first-reader path != orchestration
first-reader path != decision
<!-- FIRST READER PATH COMMIT REGISTRATION:END -->

<!-- REGISTRY ANCHOR ROLE SEPARATION:START -->
## Registry anchor role separation

The ecosystem now separates commit identity from registry role identity.

    Commit equality is not role equality.
    Commit divergence is optional.
    Role divergence is mandatory.

Current protected anchors:

    OMNIA-VALIDATION registry_control_plane_commit: 60e4385
    OMNIA-VALIDATION latest_public_commit: 83fa07f
    OMNIA-VALIDATION first_reader_path_commit: 83fa07f
    OMNIA-VALIDATION registry_role: validator_backbone_core
    OMNIA-VALIDATION first_reader_path_role: first_reader_surface

    lon-mirror root_reference_commit: 22a320d
    lon-mirror public_entrypoint_commit: f74b799
    lon-mirror first_reader_path_commit: 4dd5cb5
    lon-mirror registry_role: root_reference_observer
    lon-mirror first_reader_path_role: first_reader_surface

Policy document:

    https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/REGISTRY_ANCHOR_ROLE_SEPARATION.md

Boundary:

    first-reader path != validation
    first-reader path != measurement
    first-reader path != orchestration
    first-reader path != decision
    registry topology != BoundaryCertificate
    commit identity != role identity
<!-- REGISTRY ANCHOR ROLE SEPARATION:END -->
