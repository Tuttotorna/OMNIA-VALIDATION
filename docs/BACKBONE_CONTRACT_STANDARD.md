# Backbone Contract Standard

## Status

This document defines the minimum software contract for the OMNIA ecosystem backbone.

It is not a conceptual note.

It is the integration standard that every satellite repository must follow if it wants to participate in the validated OMNIA software chain.

## Canonical backbone

OMNIA measurement
  -> BoundaryCertificate
  -> omnia-limit validate_certificate()
  -> OMNIA-VALIDATION ValidationEnvelope
  -> CI regression

## Current canonical repositories

OMNIA
  Role: measurement artifact emitter

omnia-limit
  Role: BoundaryCertificate schema validator and boundary-state API

OMNIA-VALIDATION
  Role: control-plane validation, envelope emission, evidence preservation, regression testing

## Non-negotiable rule

No satellite repository may create a parallel validation contract when the target is OMNIA ecosystem integration.

A satellite may define domain-specific adapters, experiments, views, reports, dashboards, or scenario runners.

A satellite must not bypass the canonical backbone.

## Canonical artifact chain

MeasurementArtifact
  -> BoundaryCertificate
  -> ValidationEnvelope

At the current implementation stage, the operational artifact is:

BoundaryCertificate

MeasurementArtifact may exist upstream as an internal or future formal artifact, but the mandatory cross-repository boundary is the BoundaryCertificate.

## BoundaryCertificate

The BoundaryCertificate is emitted by OMNIA or by a compliant OMNIA-facing adapter.

It must be machine-readable.

It must be schema-compatible with the boundary_certificate.schema.json contract exposed by omnia-limit.

The current required structure is:

metadata
  certificate_id
  timestamp
  target_repository

metrics
  ast_deformation_index
  perturbation_step

boundary_status
  should_continue
  saturation_detected
  reason

## BoundaryCertificate responsibilities

A BoundaryCertificate may contain measured structural state.

A BoundaryCertificate may contain continuation-relevant signals.

A BoundaryCertificate may contain extra metrics when schema-compatible.

A BoundaryCertificate must not contain unvalidated semantic conclusions.

A BoundaryCertificate must not act as a final decision.

A BoundaryCertificate must not encode a hidden policy outside the explicit boundary fields.

## OMNIA responsibilities

OMNIA is the measurement emitter.

OMNIA may build a BoundaryCertificate from a measurement dictionary.

OMNIA may expose helper functions such as:

build_boundary_certificate(...)
build_boundary_certificate_from_measurement(...)

OMNIA does not own downstream validation.

OMNIA does not own final governance decisions.

OMNIA does not replace omnia-limit.

OMNIA does not replace OMNIA-VALIDATION.

## omnia-limit responsibilities

omnia-limit owns the formal boundary contract validation.

It must expose a stable Python API for validating certificates.

The canonical API is:

validate_certificate(...)

It must return a structured object representing the validated boundary certificate.

It must preserve backward compatibility with its existing public limit API unless a major-version migration explicitly states otherwise.

## OMNIA-VALIDATION responsibilities

OMNIA-VALIDATION is the control-plane repository.

It consumes a BoundaryCertificate.

It validates the certificate through omnia-limit.

It emits a ValidationEnvelope.

It stores and tests the evidence chain.

It owns the end-to-end regression test that proves the backbone still works.

The canonical API is:

process_boundary_step(...)

## ValidationEnvelope

The ValidationEnvelope is the final control-plane artifact currently emitted by OMNIA-VALIDATION.

It must include:

envelope_id
timestamp
validation_status
details

The current validation statuses are:

GATE_OPEN_MEASUREMENT_REQUIRED
GATE_CLOSED_SATURATION_REACHED
GATE_ERROR_CONTRACT_VIOLATION

## CI requirement

The canonical backbone must be regression-tested in GitHub Actions.

The CI must verify the software path:

checkout OMNIA-VALIDATION
checkout OMNIA
checkout omnia-limit
install omnia-limit
install OMNIA
install OMNIA-VALIDATION
run omnia-limit tests
run OMNIA tests
run OMNIA-VALIDATION tests
run tests/test_end_to_end_backbone.py

A local-only pass is not sufficient as a final ecosystem guarantee.

## Satellite integration rule

Every satellite repository must choose one of these roles:

1. Producer
   Emits a BoundaryCertificate or produces data that OMNIA converts into one.

2. Adapter
   Translates domain-specific outputs into a BoundaryCertificate-compatible structure.

3. Consumer
   Reads validated envelopes or certificates without modifying the backbone contract.

4. Observer
   Reports, visualizes, or compares artifacts without changing them.

A satellite must explicitly declare its role.

## Satellite repositories affected

The following repositories must eventually align to this standard:

OMNIAMIND
OMNIA-RADAR
OMNIA-SECURITY
OMNIA-CRYPTO
OMNIA-INVARIANCE
OMNIA-CONSTANT
OMNIA-THREE-BODY
OMNIABASE
lon-mirror

## Domain-specific logic

Domain-specific logic belongs in satellite repositories.

Domain-specific logic must not redefine the backbone contract.

Example:

OMNIA-INVARIANCE
  should expose invariance primitives and structural transformations.

OMNIA-CRYPTO
  should act as a crypto-domain adapter or experiment layer.

OMNIA-CRYPTO
  should not duplicate generic invariance primitives if OMNIA-INVARIANCE owns them.

## Domain overlap rule

If two repositories contain overlapping domain logic, the generic layer wins the primitive.

The domain repository becomes an adapter.

Example:

Generic invariant computation
  belongs in OMNIA-INVARIANCE.

Crypto-specific experiment scenario
  belongs in OMNIA-CRYPTO.

Validation of output
  goes through BoundaryCertificate -> omnia-limit -> OMNIA-VALIDATION.

## OMNIAMIND rule

OMNIAMIND must not become a parallel control plane.

OMNIAMIND may orchestrate.

OMNIAMIND may route.

OMNIAMIND may coordinate experiments.

OMNIAMIND must consume the existing backbone instead of redefining it.

Correct position:

OMNIAMIND
  -> orchestrates compliant producers/adapters/consumers
  -> does not replace OMNIA-VALIDATION
  -> does not replace omnia-limit
  -> does not decide semantic truth

## Forbidden patterns

The following patterns are forbidden for backbone-compliant integration:

1. Local-only file handoff with no Python import boundary.
2. New schema names that duplicate BoundaryCertificate.
3. Satellite-specific validation envelopes that bypass OMNIA-VALIDATION.
4. Hidden continuation policy inside a satellite.
5. Domain repository redefining generic measurement primitives.
6. README-only compatibility with no regression test.
7. CI that tests the satellite alone but not the backbone path.

## Required pattern for new satellites

A new satellite integration must provide:

1. package importability
2. clear role declaration
3. adapter or producer function
4. BoundaryCertificate-compatible output
5. validation through omnia-limit
6. at least one regression test
7. CI path or inclusion in OMNIA-VALIDATION control-plane CI

## Minimal compliant integration

A minimal compliant satellite flow looks like this:

satellite_output
  -> adapter_to_boundary_certificate(...)
  -> omnia_limit.validate_certificate(...)
  -> omnia_validation.enveloper.process_boundary_step(...)

## Acceptance criteria

A repository is backbone-compliant only if:

1. It is installable as a Python package or exposes a stable import boundary.
2. It does not require manual file movement for the core validation path.
3. It emits or consumes a BoundaryCertificate-compatible structure.
4. It validates through omnia-limit.
5. It has a regression test proving the path.
6. It does not create a competing validation contract.

## Current verified backbone commits

At the time this standard was written, the backbone had been established through these commits:

omnia-limit:
26352c7 - Add BoundaryCertificate API without breaking legacy limit API

OMNIA:
e4d2b39 - Add BoundaryCertificate emission bridge

OMNIA-VALIDATION:
394c6e3 - Add end-to-end backbone validation test

OMNIA-VALIDATION:
3fcdb2f - Run backbone end-to-end test in CI

## Final principle

The OMNIA ecosystem must remain structurally layered.

measurement != validation
validation != orchestration
orchestration != decision
decision != measurement

The backbone exists to prevent these layers from collapsing into each other.

This standard is the minimum contract that preserves that separation.
