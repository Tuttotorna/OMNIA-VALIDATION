# lon-mirror Public Entry Point Registration

## Status

`lon-mirror` now exposes a public first-reader entry point.

This document registers that public entry point inside `OMNIA-VALIDATION`, so the central ecosystem control-plane documentation points back to the current `lon-mirror` public doorway.

## Registered repository

repository: lon-mirror
role: root_reference_observer
status: satellite_compliant
registry_commit: 22a320d
public_entrypoint_commit: f74b799
public_root_reference_commit: 22a320d

## Public links

lon-mirror public entry point:
https://github.com/Tuttotorna/lon-mirror/blob/main/docs/PUBLIC_ENTRYPOINT.md

lon-mirror root reference link:
https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

OMNIA-VALIDATION MB-X.01 / L.O.N. ecosystem entry point:
https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/MBX01_LON_ECOSYSTEM_ENTRYPOINT.md

## Canonical backbone

OMNIA measurement
  -> BoundaryCertificate
  -> omnia-limit validate_certificate()
  -> OMNIA-VALIDATION ValidationEnvelope
  -> CI regression
  -> compliant producer / adapter / consumer / observer

## Layer separation

measurement != validation
validation != orchestration
orchestration != decision
decision != measurement
observation != decision
domain adaptation != backbone redefinition

## Boundary

This registration does not give `lon-mirror` new authority.

`lon-mirror` remains a bounded root reference observer.

It must not become:

validator
control plane
governance engine
decision engine
semantic-truth engine
measurement replacement
BoundaryCertificate redefinition
ValidationEnvelope redefinition

## Closed public path

OMNIA-VALIDATION
  -> MB-X.01 / L.O.N. ecosystem entry point
  -> ecosystem map
  -> ecosystem status
  -> backbone compliance registry
  -> lon-mirror root reference observer
  -> lon-mirror public entry point
