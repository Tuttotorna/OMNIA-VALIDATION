# First Reader Path

## Purpose

This is the shortest public path for a reader who arrives with no prior context.

Read this first if you want to understand what the MB-X.01 / L.O.N. ecosystem is without entering the technical documents immediately.

## Thirty-second version

MB-X.01 is a multi-repository structural-validation ecosystem.

L.O.N. means Logical Origin Node.

OMNIA measures structural behavior.

omnia-limit validates the boundary certificate.

OMNIA-VALIDATION validates the control-plane envelope and protects the public registry.

OMNIAMIND may orchestrate.

Satellites adapt, observe, or consume.

lon-mirror is the root reference observer.

No layer is allowed to silently become another layer.

## One-line backbone

OMNIA measurement -> BoundaryCertificate -> omnia-limit validate_certificate() -> OMNIA-VALIDATION ValidationEnvelope -> CI regression -> compliant producer / adapter / consumer / observer

## What to open first

1. MB-X.01 / L.O.N. ecosystem entry point:
   https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/MBX01_LON_ECOSYSTEM_ENTRYPOINT.md

2. Ecosystem map:
   https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/ECOSYSTEM_MAP.md

3. Ecosystem status:
   https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/ECOSYSTEM_STATUS.md

4. Backbone compliance registry:
   https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/ECOSYSTEM_BACKBONE_COMPLIANCE_REGISTRY.md

5. lon-mirror public entry point:
   https://github.com/Tuttotorna/lon-mirror/blob/main/docs/PUBLIC_ENTRYPOINT.md

6. lon-mirror root reference link:
   https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

## Boundary rule

measurement != validation
validation != orchestration
orchestration != decision
decision != measurement
observation != decision
domain adaptation != backbone redefinition

## What this ecosystem does not claim

It does not claim semantic truth.

It does not claim final mathematical truth.

It does not claim final physical truth.

It does not claim consciousness.

It does not claim agency.

It does not make governance decisions.

It does not decide what the world means.

## Current public anchors

OMNIA-VALIDATION commit at patch time:
2e7e63c

lon-mirror commit at patch time:
f74b799

## Minimal mental model

OMNIA measures.
omnia-limit validates the boundary certificate.
OMNIA-VALIDATION validates the control-plane envelope.
OMNIAMIND orchestrates.
Satellites adapt, observe, or consume.
lon-mirror acts as root reference observer.
No satellite owns the backbone.
No layer silently replaces another layer.

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
