# DOI Ownership Audit

## Status

audit_status: pending_strict_ownership_verification
target_repository: Tuttotorna/OMNIA-VALIDATION
reference_repository: Tuttotorna/OMNIA
release_tag: v2026.05.21
release_commit: fbcbb4f
previous_target_doi: 10.5281/zenodo.20322696
reference_doi: 10.5281/zenodo.20322696
resolved_target_doi: pending
resolved_target_zenodo_record: pending

## Finding

The ecosystem DOI audit detected a cross-repository DOI collision.

duplicate_doi: 10.5281/zenodo.20322696
affected_repository_1: Tuttotorna/OMNIA
affected_repository_2: Tuttotorna/OMNIA-VALIDATION

The collision is structurally invalid because OMNIA and OMNIA-VALIDATION are distinct repositories.

## Corrective rule

repo_name substring match is forbidden for DOI ownership
OMNIA != OMNIA-VALIDATION
a DOI must bind to exact repository identity or remain pending

## Applied correction

OMNIA-VALIDATION no longer accepts the OMNIA DOI as its own release DOI.

If a strict Zenodo record was found for OMNIA-VALIDATION, the exact DOI was registered.

If no strict Zenodo record was found, the DOI was set to pending and the dynamic Zenodo badge was preserved.

## Boundary

DOI ownership != substring match
DOI ownership != measurement
DOI ownership != validation
DOI ownership != orchestration
DOI ownership != decision
