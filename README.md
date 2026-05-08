# OMNIA-VALIDATION

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20068812.svg)](https://doi.org/10.5281/zenodo.20068812)

Structural validation, falsification, perturbation testing, reproducibility, artifact traceability, and result-regression layer for the OMNIA ecosystem.

OMNIA-VALIDATION exists to pressure-test structural measurements.

Its purpose is not to defend OMNIA.

Its purpose is to expose what survives controlled validation, and what collapses under perturbation, falsification, threshold changes, observer variation, artifact checks, and reproducibility checks.

```text
measurement != inference != decision
```

---

## What This Repository Is

OMNIA-VALIDATION is a research-first validation layer.

It turns part of the OMNIA ecosystem from narrative claim into executable checks.

Current operational focus:

```text
artifact traceability
manifest generation
manifest validation
result regression classification
schema checking
hash checking
testable reproducibility
```

Correct reading:

```text
less trust the claim
more run the check
```

---

## What Is Operational Now

The repository currently has three executable chains.

### 1. Artifact Manifest Generation

```text
data/source_outputs/
  -> examples/build_artifact_hash_manifest_v0.py
  -> results/artifact_hash_manifest_v0.json
```

Stable generation command:

```bash
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
```

Current manifest scope:

```text
data/source_outputs/
```

Current manifest file:

```text
results/artifact_hash_manifest_v0.json
```

---

### 2. Artifact Manifest Validation

```text
results/artifact_hash_manifest_v0.json
  -> omnia-validation validate-manifest ... --verify-hashes
  -> PASS / FAIL
```

Command:

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

Correct interpretation:

```text
hash match    -> artifact byte identity preserved
hash mismatch -> artifact identity changed or path/content problem exists
hash present  -> traceability improved
```

Incorrect interpretation:

```text
hash match proves semantic truth
hash presence proves scientific correctness
hash traceability certifies production safety
```

---

### 3. Result Regression Classification

```text
previous result + current result
  -> omnia-validation compare-results
  -> NO_REGRESSION / EXPECTED_DRIFT / HASH_REGRESSION / ...
```

Command:

```bash
omnia-validation compare-results \
  --previous results/artifact_hash_manifest_v0.json \
  --current results/artifact_hash_manifest_v0.json
```

Expected identical-artifact output:

```json
{
  "status": "PASS",
  "schema": "result_regression_comparison",
  "classification": "NO_REGRESSION"
}
```

Current classifications:

```text
NO_REGRESSION
EXPECTED_DRIFT
SCHEMA_REGRESSION
STATUS_REGRESSION
BOUNDARY_REGRESSION
PAYLOAD_REGRESSION
HASH_REGRESSION
```

Boundary:

```text
regression classification is structural evidence
regression classification is not semantic truth
regression classification does not replace external review
```

---

## Quickstart

Clone, install, test:

```bash
git clone https://github.com/Tuttotorna/OMNIA-VALIDATION.git
cd OMNIA-VALIDATION
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest -q
ruff check omnia_validation tests
```

Run the current operational checks:

```bash
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes
omnia-validation compare-results \
  --previous results/artifact_hash_manifest_v0.json \
  --current results/artifact_hash_manifest_v0.json
```

Full quickstart:

```text
docs/QUICKSTART.md
```

---

## Package Layer

Installable package:

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
omnia_validation.regression
omnia_validation.cli
```

Package root policy:

```text
omnia_validation/__init__.py exports only __version__
```

Use module-specific imports:

```python
from omnia_validation.hashing import compute_file_sha256
from omnia_validation.manifest import validate_artifact_manifest
from omnia_validation.regression import compare_result_files
from omnia_validation.schemas import validate_result_envelope
```

Avoid root helper imports:

```python
from omnia_validation import compute_file_sha256
from omnia_validation import validate_artifact_manifest
from omnia_validation import compare_result_files
```

Package API:

```text
docs/PACKAGE_API.md
```

---

## CLI Commands

Current CLI:

```bash
omnia-validation validate-sha256 <sha256>
omnia-validation hash-file <path>
omnia-validation validate-json <path>
omnia-validation validate-result <path>
omnia-validation validate-manifest <path> --verify-hashes
omnia-validation compare-results --previous <path> --current <path>
```

Command meaning:

```text
validate-sha256   -> check SHA-256 hexadecimal format
hash-file         -> compute SHA-256 for a file
validate-json     -> check JSON / JSONL parseability
validate-result   -> check canonical result envelope
validate-manifest -> check artifact manifest and optional hash matches
compare-results   -> classify structural differences between result artifacts
```

---

## Current Status

Current engineering status:

```text
research-first
experimental
CI-enabled
installable package layer present
artifact manifest generator present
manifest validator present
validate-manifest CLI present
result regression module present
compare-results CLI present
tests present
documentation aligned
not production-certified
```

Current tested components include:

```text
hash utilities
JSON / JSONL utilities
schema validation
artifact manifest validation
manifest generator
validate-manifest CLI
result regression classifier
compare-results CLI
legacy result wrapping
existing result parseability
```

Current project status:

```text
docs/PROJECT_STATUS.md
```

---

## What This Repository Does Not Claim

OMNIA-VALIDATION does not claim:

```text
semantic truth detection
universal validity
universal invariance
model intelligence certification
production safety certification
mathematical completeness
scientific finality
decision authority
```

Structural stability is not semantic correctness.

Structural instability is not semantic incorrectness.

Hash identity is not scientific truth.

Regression classification is not final interpretation.

Final boundary:

```text
measurement != inference != decision
```

---

## Documentation Index

Main index:

```text
docs/INDEX.md
```

Core engineering docs:

```text
docs/QUICKSTART.md
docs/RUNNING_EXPERIMENTS.md
docs/VALIDATOR_AUTHORING_GUIDE.md
docs/VALIDATOR_REGISTRY.md
docs/RESULT_SCHEMA.md
docs/RESULT_REGRESSION_POLICY.md
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
docs/PACKAGE_API.md
docs/PROJECT_STATUS.md
docs/MAINTENANCE.md
docs/RELEASE_POLICY.md
docs/LEGACY_RESULT_NORMALIZATION.md
docs/LEGACY_STATUS_MAPPING.md
docs/CONSOLIDATION_ROADMAP_V0.md
```

Contribution and governance:

```text
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
```

---

## Repository Structure

Important directories:

```text
docs/              -> technical documentation and result reports
examples/          -> runnable validation scripts
results/           -> historical and generated JSON result files
results_enveloped/ -> schema-normalized copies of legacy results
data/              -> bounded datasets and source-output records
omnia_validation/  -> reusable Python package utilities
tests/             -> pytest suite
.github/workflows/ -> CI workflow
```

---

## Why This Exists

Without validation pressure:

```text
metrics drift into narrative
thresholds become arbitrary
frameworks become unfalsifiable
failures disappear from visibility
structural claims become too easy to overstate
```

OMNIA-VALIDATION exists to make structural claims harder to fake and easier to test.

Core principle:

```text
a framework becomes more trustworthy when its failure boundaries become measurable
```

---

## Author

Author: Brighindi Massimiliano

Contact: brighissimo@gmail.com
