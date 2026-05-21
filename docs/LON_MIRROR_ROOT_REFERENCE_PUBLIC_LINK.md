# lon-mirror Public Root Reference Link

## Status

This document records the public link between OMNIA-VALIDATION and lon-mirror.

lon-mirror is registered as the root reference observer for the MB-X.01 / L.O.N. ecosystem.

The verified public root reference link is:

https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

Verified lon-mirror commit:

22a320d

Expected reference commit:

22a320d

## Purpose

The purpose of this document is to close the public reference circuit:

OMNIA-VALIDATION
  -> MB-X.01 / L.O.N. ecosystem entry point
  -> ecosystem map
  -> ecosystem status
  -> backbone compliance registry
  -> lon-mirror root reference observer

This document does not create a new contract.

It records that lon-mirror now exposes the MB-X.01 / L.O.N. entry point from the root reference side.

## Canonical backbone

The canonical backbone remains:

OMNIA measurement
  -> BoundaryCertificate
  -> omnia-limit validate_certificate()
  -> OMNIA-VALIDATION ValidationEnvelope
  -> CI regression
  -> compliant producer / adapter / consumer / observer

## lon-mirror role

Repository:

https://github.com/Tuttotorna/lon-mirror

Role:

root_reference_observer

Allowed behavior:

- observe validated backbone output
- route measurements through the existing backbone for reference checks
- expose the public root reference path
- link back to the MB-X.01 / L.O.N. ecosystem entry point

Forbidden behavior:

- must not become a validator
- must not become a control plane
- must not become a governance engine
- must not become a decision engine
- must not become a semantic-truth engine
- must not redefine BoundaryCertificate
- must not redefine ValidationEnvelope

## Layer separation

The link is valid only while the ecosystem preserves:

measurement != validation
validation != orchestration
orchestration != decision
decision != measurement
observation != decision
domain adaptation != backbone redefinition

## Registry consequence

The ecosystem registry must continue to record lon-mirror as:

repository: lon-mirror
role: root_reference_observer
status: satellite_compliant
commit: 22a320d
public_root_reference_link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

## Final boundary

This is a public reference link.

It is not a semantic-truth claim.

It is not a governance decision.

It is not a replacement for OMNIA, omnia-limit, or OMNIA-VALIDATION.
