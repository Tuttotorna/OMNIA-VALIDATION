# OMNIA-VALIDATION — Documentation Index

## Purpose

This index provides a stable entry point for the OMNIA-VALIDATION documentation.

OMNIA-VALIDATION is a structural validation, falsification, perturbation testing, and reproducibility layer for the OMNIA ecosystem.

Core boundary:

```text
measurement != inference != decision
```

---

## Main Repository Files

```text
README.md
pyproject.toml
requirements-dev.txt
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
```

---

## Package Layer

Reusable utilities are located in:

```text
omnia_validation/
```

Current modules:

```text
omnia_validation.hashing
omnia_validation.io
omnia_validation.metrics
omnia_validation.metadata
omnia_validation.schemas
omnia_validation.manifest
omnia_validation.cli
```

Package root:

```text
omnia_validation/__init__.py
```

Package root export policy:

```text
exports only __version__
```

Reason:

```text
submodules may evolve independently
package import should remain stable
helpers should be imported from the module that defines them
```

Correct import pattern:

```python
from omnia_validation.hashing import compute_file_sha256
from omnia_validation.manifest import validate_artifact_manifest
from omnia_validation.schemas import validate_result_envelope
```

Avoid root helper imports:

```python
from omnia_validation import compute_file_sha256
from omnia_validation import validate_artifact_manifest
from omnia_validation import validate_result_envelope
```

Package API reference:

```text
docs/PACKAGE_API.md
```

---

## Tests

The current test suite is located in:

```text
tests/
```

Current test files:

```text
tests/test_hashing.py
tests/test_io.py
tests/test_metrics.py
tests/test_metadata.py
tests/test_cli.py
tests/test_schemas.py
tests/test_existing_results.py
tests/test_enveloped_results.py
tests/test_wrap_legacy_results.py
tests/test_manifest.py
```

`tests/test_manifest.py` validates:

```text
artifact entry structure
artifact role vocabulary
SHA-256 format
optional file existence
optional hash verification
artifact manifest envelope
artifact count consistency
existing artifact hash manifest
```

---

## Continuous Integration

The CI workflow is located in:

```text
.github/workflows/ci.yml
```

It checks:

```text
Python 3.10
Python 3.11
Python 3.12
package installation
ruff
pytest
CLI smoke test
```

---

## Quickstart

Quickstart guide:

```text
docs/QUICKSTART.md
```

This document gives a minimal operational path for new users.

It covers:

```text
clone
install
test
CLI checks
results/
results_enveloped/
legacy wrapper
basic result validation
minimal maintenance loop
```

---

## Running Experiments

Clean execution guide:

```text
docs/RUNNING_EXPERIMENTS.md
```

This document explains how to run OMNIA-VALIDATION experiments from a clean environment.

---

## Maintenance Guide

Maintenance guide:

```text
docs/MAINTENANCE.md
```

This document defines how to maintain the repository without breaking reproducibility, schema validation, historical result preservation, or boundary discipline.

It covers:

```text
commit checks
test commands
result handling
results_enveloped regeneration
legacy wrapper rules
CLI updates
schema updates
documentation updates
token safety
release hygiene
```

---

## Release Policy

Release policy:

```text
docs/RELEASE_POLICY.md
```

This document defines how repository states should be frozen, tagged, archived, and described without overclaiming.

It covers:

```text
release types
version naming
pre-release checks
CI requirements
result artifact rules
legacy normalization rules
Zenodo / DOI interpretation
GitHub release procedure
schema change policy
release notes
non-claim language
release readiness levels
```

Core release boundary:

```text
a release is a checkpoint
not a final truth claim
```

---

## Result Regression Policy

Result regression policy:

```text
docs/RESULT_REGRESSION_POLICY.md
```

This document defines how to classify differences between previous result artifacts and newly generated result artifacts.

It distinguishes:

```text
expected drift
unexpected regression
schema regression
hash regression
payload regression
status regression
boundary regression
documentation regression
scientific boundary change
```

Core regression principle:

```text
a result difference is not automatically an error
a result difference is evidence that must be classified
```

---

## Artifact Hash Manifest Policy

Artifact hash manifest policy:

```text
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
```

This document defines how OMNIA-VALIDATION should handle artifact hashes, hash manifests, source files, datasets, result files, and traceability claims.

It distinguishes:

```text
hash match
hash mismatch
hash presence
artifact traceability
semantic correctness
scientific validation
```

Core hash boundary:

```text
hash match proves artifact byte identity
hash match does not prove semantic truth
hash presence improves traceability
hash presence does not certify scientific correctness
```

Current status:

```text
manual policy present
artifact hash manifest present
manifest validation helpers present
validate-manifest CLI implemented and tested
repository-wide artifact hash manifest not yet present
```

---

## Artifact Hash Manifest



Deterministic manifest mode:

```bash
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
```

Explicit timestamp mode:

```bash
python examples/build_artifact_hash_manifest_v0.py --created-at 2026-05-07T00:00:00+00:00
```

Manifest generator:

```bash
python examples/build_artifact_hash_manifest_v0.py
```

Validation command:

```bash
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes
```

Current generator scope:

```text
data/source_outputs/
```

Current limitation:

```text
stable timestamp option added
repository-wide artifact coverage still missing
```


validate-manifest CLI command:

```bash
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes
```

Expected output:

```json
{
  "status": "PASS",
  "schema": "artifact_manifest"
}
```


Current artifact hash manifest:

```text
results/artifact_hash_manifest_v0.json
```

Current scope:

```text
data/source_outputs
```

Current source validator:

```text
temporal_collapse_external_source_hash_strengthening_validator_v15
```

Current purpose:

```text
records source-output hashes from Temporal Collapse Level 3 V15
```

Current status:

```text
CHECK
```

Reason:

```text
first artifact hash manifest
real SHA-256 hashes present
manifest validation helpers present
repository-wide artifact coverage not yet present
validate-manifest CLI implemented and tested
```

Validator helpers:

```text
omnia_validation.manifest
```

Tests:

```text
tests/test_manifest.py
```

Policy:

```text
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
```

---

## Validator Authoring Guide

Guide for adding new validators:

```text
docs/VALIDATOR_AUTHORING_GUIDE.md
```

This document defines validator discipline, naming rules, file patterns, result expectations, and non-claim boundaries.

---

## Validator Registry

Validator registry:

```text
docs/VALIDATOR_REGISTRY.md
```

This document provides a structured map of validators and validation-related scripts.

It separates:

```text
schema and package validators
legacy normalization validators
Temporal Collapse Level 3 validators
Temporal Collapse Topology validators
observer and recoverability validators
cross-domain and perturbation validators
structural benchmark validators
future validator families
```

The registry is a navigation and maintenance map.

It does not declare every validator final.

Boundary:

```text
a validator is a controlled structural test
not a truth oracle
```

---

## Result Schema

Common schema for JSON result files:

```text
docs/RESULT_SCHEMA.md
```

This document defines the recommended result envelope, status vocabulary, payload fields, hash traceability fields, trajectory fields, topology fields, and failure/boundary reporting rules.

The schema is partially enforceable through:

```text
omnia_validation.schemas
omnia-validation validate-result <path>
```

---

## Package API

Reusable Python package API reference:

```text
docs/PACKAGE_API.md
```

This document describes:

```text
omnia_validation.hashing
omnia_validation.io
omnia_validation.metrics
omnia_validation.metadata
omnia_validation.schemas
omnia_validation.manifest
omnia_validation.cli
```

It also documents the package root policy:

```text
omnia_validation/__init__.py exports only __version__
helpers should be imported from specific modules
```

---

## Project Status

Current repository status:

```text
docs/PROJECT_STATUS.md
```

This document states what is ready, what is experimental, what is partially consolidated, what is missing, and what is not claimed.

It separates:

```text
ready components
experimental components
partial consolidation
missing engineering work
scientific boundaries
production non-claims
```

---

## Legacy Result Normalization

Legacy result normalization document:

```text
docs/LEGACY_RESULT_NORMALIZATION.md
```

This document explains why the repository contains both:

```text
results/
results_enveloped/
```

Meaning:

```text
results/           -> historical raw result artifacts
results_enveloped/ -> canonical-envelope copies of legacy results
```

The original historical results remain untouched.

The enveloped results are schema-valid wrappers generated by:

```text
examples/wrap_legacy_results_in_envelope.py
```

The manifest is located at:

```text
results_enveloped/legacy_result_envelope_manifest_v0.json
```

Current normalization result:

```text
legacy results wrapped: 97
schema-valid enveloped files: 98
wrapping failures: 0
```

---

## Legacy Status Mapping

Legacy status mapping document:

```text
docs/LEGACY_STATUS_MAPPING.md
```

This document explains how older status values are preserved and handled.

Legacy result files may contain status values such as:

```text
DRIFT
STABLE
CRITICAL
WATCH
passed
stable
collapse-like
v15_external_source_hash_strengthened
```

The current canonical schema allows only:

```text
PASS
CHECK
FAIL
```

Current policy:

```text
legacy status values are preserved inside payload.legacy_status
legacy wrapped files use canonical status CHECK
automatic scientific reinterpretation is not applied
```

This prevents format normalization from being falsely presented as scientific revalidation.

---

## Consolidation Roadmap

The engineering consolidation roadmap is located in:

```text
docs/CONSOLIDATION_ROADMAP_V0.md
```

This document defines the path from research-script archive toward a reproducible, installable, testable validation layer.

---

## Code Of Conduct

Code of conduct:

```text
CODE_OF_CONDUCT.md
```

This document defines expected conduct for contributors, reviewers, maintainers, and users.

It supports:

```text
precise criticism
evidence-based review
boundary discipline
credential safety
non-abusive technical disagreement
negative-result preservation
```

It does not require agreement with OMNIA-VALIDATION claims.

Critical review is welcome when it remains specific, reproducible, and non-abusive.

---

## Contribution And Security

Contribution guide:

```text
CONTRIBUTING.md
```

Security policy:

```text
SECURITY.md
```

GitHub issue templates:

```text
.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/validation_result_review.md
.github/ISSUE_TEMPLATE/documentation_issue.md
```

Pull request template:

```text
.github/pull_request_template.md
```

---

## Temporal Collapse Topology

Canonical entry point:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_INDEX_V0.md
```

Main chain document:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_EXPERIMENT_CHAIN_V0.md
```

Final phase result:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_BOUNDARY_PHASE_DIAGRAM_V0_RESULT.md
```

Registry entry:

```text
docs/VALIDATOR_REGISTRY.md
```

Regression policy:

```text
docs/RESULT_REGRESSION_POLICY.md
```

Hash manifest policy:

```text
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
```

Artifact hash manifest:

```text
results/artifact_hash_manifest_v0.json
```

---

## Temporal Collapse Level 3

Canonical entry point:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
```

Human-readable summary:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_FINAL_SUMMARY_V0.md
```

Current chain:

```text
V13 -> V14 -> V15
```

Registry entry:

```text
docs/VALIDATOR_REGISTRY.md
```

Regression policy:

```text
docs/RESULT_REGRESSION_POLICY.md
```

Hash manifest policy:

```text
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
```

Artifact hash manifest:

```text
results/artifact_hash_manifest_v0.json
```

---

## Result Directories

Experimental artifacts are organized under:

```text
data/
examples/
results/
results_enveloped/
docs/
```

Current important directories:

```text
docs/              -> technical documentation and result reports
examples/          -> runnable validation scripts
results/           -> historical generated JSON result files
results_enveloped/ -> schema-normalized copies of legacy result files
data/              -> bounded datasets and source-output records
omnia_validation/  -> reusable Python package utilities
tests/             -> pytest suite
.github/workflows/ -> CI workflow
```

---

## Reading Order

Suggested reading order for new visitors:

```text
README.md
docs/INDEX.md
docs/QUICKSTART.md
docs/PROJECT_STATUS.md
docs/MAINTENANCE.md
docs/RELEASE_POLICY.md
docs/RESULT_REGRESSION_POLICY.md
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
docs/RUNNING_EXPERIMENTS.md
docs/VALIDATOR_AUTHORING_GUIDE.md
docs/VALIDATOR_REGISTRY.md
docs/RESULT_SCHEMA.md
docs/PACKAGE_API.md
docs/LEGACY_RESULT_NORMALIZATION.md
docs/LEGACY_STATUS_MAPPING.md
docs/CONSOLIDATION_ROADMAP_V0.md
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
docs/TEMPORAL_COLLAPSE_TOPOLOGY_INDEX_V0.md
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
```

---

## Engineering Documents

Current engineering/consolidation documents:

```text
docs/PROJECT_STATUS.md
docs/QUICKSTART.md
docs/MAINTENANCE.md
docs/RELEASE_POLICY.md
docs/RESULT_REGRESSION_POLICY.md
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
docs/RUNNING_EXPERIMENTS.md
docs/VALIDATOR_AUTHORING_GUIDE.md
docs/VALIDATOR_REGISTRY.md
docs/RESULT_SCHEMA.md
docs/PACKAGE_API.md
docs/LEGACY_RESULT_NORMALIZATION.md
docs/LEGACY_STATUS_MAPPING.md
docs/CONSOLIDATION_ROADMAP_V0.md
```

Purpose:

```text
declare current project state
provide a minimal first-run path
define maintenance discipline
define release discipline
define result regression discipline
define artifact hash manifest discipline
make experiments runnable
make validators authorable
map validators and validator families
make result files comparable
make package utilities documented
explain package root import policy
explain legacy result normalization
explain legacy status preservation
make repository structure maintainable
```

---

## Current Engineering State

The repository currently includes:

```text
installable package layer
basic unit tests
green CI
quickstart guide
maintenance guide
release policy
result regression policy
artifact hash manifest policy
artifact hash manifest
manifest validation helpers
manifest tests
clean execution guide
validator authoring guide
validator registry
common result schema
schema validator
validate-result CLI command
package API documentation
project status document
legacy result normalization layer
legacy status mapping policy
contribution guide
security policy
code of conduct
issue templates
pull request template
consolidation roadmap
```

Still missing:

```text
payload-specific schema validators
full per-file validator registry
automated result regression tests
experiment-chain CI
repository-wide artifact hash manifest
validate-manifest CLI command
manifest generator
```

---

## Legacy Result Policy

The repository preserves historical result artifacts in:

```text
results/
```

These files may not follow the current canonical envelope.

Schema-normalized copies are stored in:

```text
results_enveloped/
```

Correct interpretation:

```text
results/ preserves history.
results_enveloped/ provides schema-valid wrappers.
```

Incorrect interpretation:

```text
results_enveloped/ scientifically revalidates every legacy experiment.
results/ should be deleted.
```

Legacy normalization is format normalization.

It is not semantic validation.

It is not scientific revalidation.

---

## Legacy Status Policy

Legacy statuses are historical values.

They are preserved, not erased.

They are stored in enveloped copies at:

```text
payload.legacy_status
```

Wrapper status remains:

```text
CHECK
```

Reason:

```text
wrapping is normalization
wrapping is not revalidation
```

A future validator-specific mapping may map some legacy statuses to `PASS`, `CHECK`, or `FAIL`, but only with explicit documented logic.

---

## Maintenance Policy

Maintenance must preserve evidence while improving reproducibility.

Before pushing changes, run:

```bash
pytest -q
ruff check omnia_validation tests
```

When result files change, validate them and regenerate enveloped results if needed:

```bash
omnia-validation validate-json results/<result_file>.json
python examples/wrap_legacy_results_in_envelope.py
pytest -q
```

Maintenance must not:

```text
rewrite old results silently
delete negative results
convert CHECK to PASS without revalidation
hide failures
remove boundary statements
treat normalization as scientific proof
```

Full policy:

```text
docs/MAINTENANCE.md
```

---

## Release Policy

A release is a frozen repository state.

It should mean:

```text
this repository state was tested, documented, and frozen
```

It must not mean:

```text
this proves semantic truth
this certifies production safety
this proves universal validity
```

Before release, the project should have:

```text
CI green
pytest passing
ruff passing
README aligned
docs aligned
result schema checks passing
known limitations visible
non-claims explicit
```

Full policy:

```text
docs/RELEASE_POLICY.md
```

---

## Result Regression Policy

A result change is evidence to classify.

It is not automatically an error.

Regression review should distinguish:

```text
expected drift
unexpected regression
schema regression
hash regression
payload regression
status regression
boundary regression
documentation regression
scientific boundary change
```

Full policy:

```text
docs/RESULT_REGRESSION_POLICY.md
```

---

## Artifact Hash Policy

Hashes support artifact traceability.

They do not prove semantic truth.

Correct interpretation:

```text
hash match    -> artifact byte identity preserved
hash mismatch -> artifact identity changed or path/content problem exists
hash present  -> traceability improved
hash absent   -> traceability weaker
```

Incorrect interpretation:

```text
hash match proves semantic correctness
hash presence certifies scientific validity
hash manifest replaces independent reproduction
```

Full policy:

```text
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
```

Current manifest:

```text
results/artifact_hash_manifest_v0.json
```

Current validation module:

```text
omnia_validation.manifest
```

Current tests:

```text
tests/test_manifest.py
```

---

## Conduct Policy

The repository accepts direct technical criticism.

The criticism must remain:

```text
specific
evidence-based
non-abusive
reproducible when possible
focused on artifacts, claims, methods, or documentation
```

The conduct policy is located at:

```text
CODE_OF_CONDUCT.md
```

---

## Validator Policy

Validators are controlled structural tests.

They are not truth oracles.

A validator should expose:

```text
stability
drift
collapse
ambiguity
boundary conditions
artifact invalidity
```

A validator should not claim:

```text
semantic truth
model intelligence
production safety
universal validity
final correctness
```

The validator registry is located at:

```text
docs/VALIDATOR_REGISTRY.md
```

---

## Non-Goal

This repository does not claim to detect semantic truth, intelligence, consciousness, or final correctness.

It measures structural behavior under controlled validation pressure.

```text
measurement != inference != decision
```