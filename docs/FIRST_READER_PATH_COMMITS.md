# First Reader Path Commit Registration

## Status

The public first-reader path is now registered as an explicit public orientation layer.

This document records the current first-reader path commits for both public entry repositories.

## Registered commits

OMNIA-VALIDATION:
  repository: OMNIA-VALIDATION
  first_reader_path_commit: 83fa07f
  first_reader_path_link: https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/FIRST_READER_PATH.md
  latest_public_commit: 83fa07f
  latest_public_artifact: docs/FIRST_READER_PATH.md

lon-mirror:
  repository: lon-mirror
  registry_commit: 22a320d
  public_entrypoint_commit: f74b799
  latest_public_commit: f74b799
  latest_public_artifact: docs/PUBLIC_ENTRYPOINT.md
  first_reader_path_commit: 4dd5cb5
  latest_first_reader_path_commit: 4dd5cb5
  first_reader_path_link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/FIRST_READER_PATH.md

## Compatibility rule

For lon-mirror, latest_public_commit remains the public entry point commit.

That preserves the existing public entry point registration test.

The newer first-reader path commit is stored separately as first_reader_path_commit and latest_first_reader_path_commit.

## Public circuit

OMNIA-VALIDATION FIRST_READER_PATH
  -> MB-X.01 / L.O.N. ecosystem entry point
  -> ecosystem map
  -> ecosystem status
  -> backbone compliance registry
  -> lon-mirror PUBLIC_ENTRYPOINT
  -> lon-mirror FIRST_READER_PATH

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

## First-reader boundary

first-reader path != validation
first-reader path != measurement
first-reader path != orchestration
first-reader path != decision

The first-reader path is public orientation only.

It does not validate.
It does not measure.
It does not orchestrate.
It does not decide.
It does not emit semantic truth.
It does not replace the registry.
It does not redefine the BoundaryCertificate.
It does not redefine the ValidationEnvelope.

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
