# DOI Ownership Audit

## Status

audit_status: resolved
target_repository: Tuttotorna/OMNIA-VALIDATION
release_tag: v2026.05.21
release_commit: fbcbb4f
resolved_target_doi: 10.5281/zenodo.20322696
resolved_target_zenodo_record: https://zenodo.org/records/20322696
ownership_status: strict_exact_repository_match

## Correct mapping

Tuttotorna/OMNIA: 10.5281/zenodo.20322683
Tuttotorna/OMNIA-VALIDATION: 10.5281/zenodo.20322696

## Local repository mapping

this_repository: Tuttotorna/OMNIA-VALIDATION
this_repository_doi: 10.5281/zenodo.20322696
other_repository: Tuttotorna/OMNIA
other_repository_doi: 10.5281/zenodo.20322683

## Finding

The previous audit path allowed a repository-name collision between OMNIA and OMNIA-VALIDATION.

That collision is invalid because OMNIA and OMNIA-VALIDATION are distinct repositories with distinct Zenodo DOI records.

## Corrective rule

exact repository identity is required for DOI ownership
repo_name substring match is forbidden for DOI ownership
OMNIA != OMNIA-VALIDATION
OMNIA DOI != OMNIA-VALIDATION DOI

## Boundary

DOI ownership != substring match
DOI ownership != measurement
DOI ownership != validation
DOI ownership != orchestration
DOI ownership != decision
