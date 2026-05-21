# Registry Anchor Role Separation

## Purpose

This document defines the registry-level policy that prevents commit anchors from being confused with semantic or architectural roles.

The policy is simple:

    Commit equality is not role equality.
    Commit divergence is optional.
    Role divergence is mandatory.

## Why this exists

A Git commit hash identifies a repository snapshot.

It does not define the role of that snapshot inside the MB-X.01 / L.O.N. ecosystem.

The same physical hash may legitimately support more than one public surface during a transitional state.

That is allowed only if the registry records different roles for those surfaces.

The registry must never infer role equivalence from hash equivalence.

## Axiomatic Backbone Policy

### 1. A commit hash is not a role.

The cryptographic identity of a snapshot does not define the function of the exposed surface.

### 2. A registry field is not a certificate.

Registry topology belongs to OMNIA-VALIDATION.

BoundaryCertificate validation belongs to omnia-limit.

### 3. A public anchor is not a first-reader anchor.

Public anchors preserve stable historical visibility.

First-reader anchors preserve external readability and navigational entry.

### 4. A first-reader anchor is not a validation anchor.

A reader path is documentation topology.

It is not a validation envelope.

It does not validate.

It does not measure.

It does not orchestrate.

It does not decide.

It does not emit semantic truth.

### 5. A validation anchor is not a measurement anchor.

Measurement is emitted by OMNIA-compatible producers.

Validation of BoundaryCertificate shape belongs to omnia-limit.

Control-plane topology and registry checks belong to OMNIA-VALIDATION.

## Required registry fields for role-bearing anchors

For any repository that declares a first-reader path, the registry must expose:

    first_reader_path_commit
    first_reader_path_link
    first_reader_path_role
    anchor_role_policy

For OMNIA-VALIDATION, the registry must expose:

    registry_control_plane_commit
    registry_role
    first_reader_path_role
    anchor_role_policy

For lon-mirror, the registry must preserve the root reference anchor independently from the public entrypoint and first-reader path anchors:

    commit
    public_root_reference_commit
    public_entrypoint_commit
    latest_public_commit
    first_reader_path_commit
    latest_first_reader_path_commit
    registry_role
    first_reader_path_role
    anchor_role_policy

## Current OMNIA-VALIDATION role mapping

    repository: OMNIA-VALIDATION
    registry_control_plane_commit: 60e4385
    latest_public_commit: 83fa07f
    first_reader_path_commit: 83fa07f
    latest_first_reader_path_commit: 83fa07f
    registry_role: validator_backbone_core
    first_reader_path_role: first_reader_surface
    anchor_role_policy: commit_equality_allowed_role_divergence_required

OMNIA-VALIDATION may temporarily have equal hashes for latest_public_commit and first_reader_path_commit.

That equality is valid because the registry explicitly records different roles.

    same hash != same role

## Current lon-mirror role mapping

    repository: lon-mirror
    commit: 22a320d
    public_root_reference_commit: 22a320d
    public_entrypoint_commit: f74b799
    latest_public_commit: f74b799
    first_reader_path_commit: 4dd5cb5
    latest_first_reader_path_commit: 4dd5cb5
    registry_role: root_reference_observer
    first_reader_path_role: first_reader_surface
    anchor_role_policy: commit_equality_allowed_role_divergence_required

## Boundary statement

This policy belongs to OMNIA-VALIDATION.

It must not be moved into omnia-limit.

omnia-limit validates BoundaryCertificate structure.

OMNIA-VALIDATION validates ecosystem registry topology.

    registry topology != BoundaryCertificate
    commit identity != role identity
    first-reader path != validation
    first-reader path != measurement
    first-reader path != orchestration
    first-reader path != decision

## Public links

    registry anchor role separation: https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/REGISTRY_ANCHOR_ROLE_SEPARATION.md
    OMNIA-VALIDATION first reader path: https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/FIRST_READER_PATH.md
    lon-mirror first reader path: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/FIRST_READER_PATH.md
    lon-mirror public entry point: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/PUBLIC_ENTRYPOINT.md
    lon-mirror root reference link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md
    MB-X.01 / L.O.N. ecosystem entry point: https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/MBX01_LON_ECOSYSTEM_ENTRYPOINT.md
