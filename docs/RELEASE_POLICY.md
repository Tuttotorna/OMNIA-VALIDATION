# OMNIA-VALIDATION — Release Policy

## Purpose

This document defines the release policy for OMNIA-VALIDATION.

The goal is to make releases:

```text
traceable
testable
reproducible
schema-aware
honest about limits
safe from overclaiming
```

Core boundary:

```text
measurement != inference != decision
```

OMNIA-VALIDATION releases must not imply semantic truth, production certification, or universal validity.

---

## 1. Release Principle

A release is a frozen repository state.

It should represent:

```text
a reproducible checkpoint
a documented engineering state
a bounded experimental state
a versioned validation layer
```

A release should not be used to exaggerate scientific certainty.

Correct release meaning:

```text
this repository state was tested, documented, and frozen
```

Incorrect release meaning:

```text
this proves OMNIA universally correct
this certifies production safety
this proves semantic truth
this is a final scientific theory
```

---

## 2. Release Types

OMNIA-VALIDATION may use three release types.

```text
engineering release
experiment release
archive release
```

---

### Engineering Release

An engineering release freezes improvements such as:

```text
package utilities
tests
CI
schemas
CLI commands
documentation
maintenance rules
normalization scripts
```

Example:

```text
v0.1.0
```

Use when the repository structure has improved.

---

### Experiment Release

An experiment release freezes a specific validation chain or result family.

Example:

```text
temporal-collapse-level-3-v0
temporal-collapse-topology-v0
```

Use when a specific experimental chain is stable enough to archive.

---

### Archive Release

An archive release freezes the entire repository state for citation, DOI, or long-term record.

Use when:

```text
README is stable
docs are aligned
CI is green
result artifacts are present
release notes are clear
```

---

## 3. Version Naming

Recommended engineering version format:

```text
vMAJOR.MINOR.PATCH
```

Meaning:

```text
MAJOR -> incompatible structural changes
MINOR -> new features, schemas, validators, or result layers
PATCH -> fixes, documentation alignment, small test updates
```

Current repository status is early alpha.

Recommended current style:

```text
v0.x.y
```

until the project has:

```text
stable validator registry
payload-specific schemas
clear runner system
external reproduction
```

---

## 4. Pre-Release Checklist

Before creating a release, run:

```bash
pytest -q
```

Run:

```bash
ruff check omnia_validation tests
```

Run:

```bash
omnia-validation validate-sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Expected output:

```text
PASS
```

Validate the legacy normalization manifest:

```bash
omnia-validation validate-result results_enveloped/legacy_result_envelope_manifest_v0.json
```

Expected output:

```json
{
  "status": "PASS",
  "schema": "result_envelope"
}
```

If result files changed, regenerate enveloped results:

```bash
python examples/wrap_legacy_results_in_envelope.py
pytest -q
```

Then inspect:

```bash
git status --short
git diff --stat
```

Do not release with unexpected uncommitted changes.

---

## 5. Required Green Conditions

A release should require:

```text
CI green
pytest passing
ruff passing
README aligned with docs
docs/INDEX.md aligned with current docs
docs/PROJECT_STATUS.md current
docs/MAINTENANCE.md current
schema docs aligned with code
package API docs aligned with code
legacy normalization docs aligned with behavior
```

The release should not proceed if:

```text
tests fail
CI is red
README links are stale
result schema docs disagree with schemas.py
package API docs disagree with package functions
legacy normalization docs disagree with wrapper behavior
```

---

## 6. Result Artifact Rules

Historical result files remain in:

```text
results/
```

Schema-normalized result copies remain in:

```text
results_enveloped/
```

Do not rewrite historical results before a release just to make them look cleaner.

If historical results need schema compatibility, use:

```text
results_enveloped/
```

Correct release treatment:

```text
results/ preserves historical evidence
results_enveloped/ provides canonical wrappers
```

Incorrect release treatment:

```text
delete old results
hide weak results
rewrite CHECK as PASS
rewrite legacy statuses silently
```

---

## 7. Legacy Result Rules

Legacy normalization is format normalization.

It is not scientific revalidation.

Current wrapper status:

```text
CHECK
```

Reason:

```text
wrapping is normalization
wrapping is not revalidation
```

Before release, ensure:

```text
tests/test_existing_results.py passes
tests/test_enveloped_results.py passes
tests/test_wrap_legacy_results.py passes
```

This protects:

```text
historical result parseability
enveloped result schema compliance
wrapper behavior
legacy status preservation
legacy payload preservation
```

---

## 8. Status Vocabulary

Canonical release-facing statuses remain:

```text
PASS
CHECK
FAIL
```

Release notes should explain these carefully.

Meaning:

```text
PASS  -> tested structural condition survived this validation step
CHECK -> partial instability, ambiguity, boundary condition, or normalization state
FAIL  -> collapse, mismatch, invalid artifact, or validation failure
```

Do not treat:

```text
CHECK
```

as cosmetic weakness.

In OMNIA-VALIDATION, `CHECK` often means:

```text
boundary exposed
instability mapped
manual review required
legacy artifact normalized
```

---

## 9. Release Notes

Every release should include release notes.

Recommended structure:

```text
Summary
What changed
Validation status
Artifacts included
Known limitations
Non-claims
```

Minimal release note template:

```text
## Summary

This release freezes OMNIA-VALIDATION at a tested repository state.

## What changed

- ...

## Validation status

- pytest: PASS
- ruff: PASS
- CI: PASS
- result schema checks: PASS

## Artifacts included

- results/
- results_enveloped/
- docs/
- examples/
- omnia_validation/

## Known limitations

- ...

## Non-claims

This release does not certify semantic truth, production safety, or universal validity.

Boundary:

measurement != inference != decision
```

---

## 10. Zenodo And DOI Policy

Zenodo may archive GitHub releases and assign a DOI.

A DOI should identify a frozen repository state.

It should not imply:

```text
peer review
scientific finality
production readiness
universal validation
```

Correct DOI interpretation:

```text
this repository version is archived and citable
```

Incorrect DOI interpretation:

```text
this repository version is scientifically proven
```

Before triggering Zenodo archiving, ensure:

```text
release notes are accurate
README is current
CI is green
docs are aligned
known limitations are visible
```

---

## 11. GitHub Release Procedure

Recommended release procedure:

```bash
git status --short
pytest -q
ruff check omnia_validation tests
```

If clean and green, create a tag:

```bash
git tag v0.x.y
```

Push the tag:

```bash
git push origin v0.x.y
```

Then create a GitHub release from that tag.

Release notes should include:

```text
boundary statement
test status
schema status
known limitations
non-claims
```

---

## 12. Package Release Policy

The package layer is currently minimal.

It is not yet intended as a mature production package.

Before publishing to a package registry, the project should have:

```text
stable API
clear versioning
payload-specific schemas
runner discipline
more integration tests
release notes
maintenance process
```

Until then, recommended usage remains:

```bash
python -m pip install -e ".[dev]"
```

from the repository.

---

## 13. Breaking Change Policy

Breaking changes include:

```text
changing canonical result envelope fields
renaming package modules
removing public functions
changing CLI command behavior
changing wrapper semantics
changing status vocabulary
```

Before introducing breaking changes:

```text
document the change
update tests
update docs
update README
explain migration path
preserve legacy artifacts
```

Breaking changes should not silently alter historical evidence.

---

## 14. Schema Change Policy

Schema changes must update:

```text
omnia_validation/schemas.py
tests/test_schemas.py
tests/test_cli.py
docs/RESULT_SCHEMA.md
docs/PACKAGE_API.md
docs/PROJECT_STATUS.md
```

If the change affects enveloped results, also update:

```text
tests/test_enveloped_results.py
docs/LEGACY_RESULT_NORMALIZATION.md
docs/LEGACY_STATUS_MAPPING.md
```

Be explicit about whether new schema rules apply to:

```text
new results only
results_enveloped/
specific payload families
all result files
```

Do not silently apply stricter rules to historical artifacts.

---

## 15. Documentation Release Rules

Before release, check:

```text
README.md
docs/INDEX.md
docs/PROJECT_STATUS.md
docs/MAINTENANCE.md
docs/RUNNING_EXPERIMENTS.md
docs/RESULT_SCHEMA.md
docs/PACKAGE_API.md
docs/LEGACY_RESULT_NORMALIZATION.md
docs/LEGACY_STATUS_MAPPING.md
```

Documentation must match the actual repository state.

If a file is mentioned in README or docs/INDEX.md, it should exist.

If a command is documented, it should run.

If a status is claimed, it should be backed by tests or documented as experimental.

---

## 16. Experimental Result Release Rules

When releasing an experimental chain, include:

```text
input files
scripts
result files
result docs
known limitations
reproduction order
boundary statement
```

Do not release only the positive interpretation.

Preserve:

```text
CHECK results
DRIFT regimes
CRITICAL local behavior
failed assumptions
negative findings
boundary conditions
```

These are part of the scientific value.

---

## 17. Non-Claim Language

Every release should preserve this boundary:

```text
measurement != inference != decision
```

A release must not claim:

```text
semantic truth detection
model intelligence certification
production safety certification
universal validity
mathematical completeness
final correctness
domain-independent guarantees
```

Use cautious language:

```text
measures structural behavior
tests reproducibility
exposes boundary conditions
preserves negative evidence
supports falsification
```

Avoid overclaiming language:

```text
measures structural stability
audits AI-output structure safety
certifies models
guarantees correctness
universal detector
```

---

## 18. Release Readiness Levels

Recommended internal labels:

```text
alpha
beta
candidate
archived
```

Meaning:

```text
alpha     -> research-ready, unstable interfaces
beta      -> broader testing, clearer schemas
candidate -> release candidate, docs aligned, CI green
archived  -> frozen and citable
```

Current recommended level:

```text
alpha
```

Reason:

```text
package layer exists
CI is green
schema validator exists
legacy normalization exists
but payload-specific schemas and full runner discipline are not complete
```

---

## 19. Emergency Fix Release

Use a patch release when fixing:

```text
broken tests
broken CI
invalid schema docs
broken CLI behavior
incorrect README links
dangerous overclaiming language
credential exposure
```

If credential exposure occurs:

```text
revoke credential immediately
remove exposed secret from repository
rotate affected token
document fix if appropriate
```

Do not wait for a normal release cycle.

---

## 20. Release Checklist

Before release:

```text
pytest -q
ruff check omnia_validation tests
omnia-validation validate-result results_enveloped/legacy_result_envelope_manifest_v0.json
git status --short
README.md checked
docs/INDEX.md checked
docs/PROJECT_STATUS.md checked
docs/MAINTENANCE.md checked
release notes drafted
known limitations included
non-claims included
```

If any item fails, do not release.

---

## 21. Non-Goal

This policy does not make OMNIA-VALIDATION production-ready.

It defines how to freeze repository states honestly.

A release is a checkpoint.

It is not a final truth claim.

Final boundary:

```text
measurement != inference != decision
```