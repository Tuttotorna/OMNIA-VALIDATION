# OMNIA-VALIDATION

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20083830.svg)](https://doi.org/10.5281/zenodo.20083830)

**OMNIA-VALIDATION** is the validation, falsification, artifact traceability, reproducibility, and result-regression layer for the OMNIA ecosystem.

It exists to pressure-test structural measurement claims.

Its purpose is not to defend OMNIA.

Its purpose is to expose what survives controlled validation and what collapses under perturbation, falsification, threshold changes, observer variation, artifact checks, and reproducibility checks.

```text
measurement != inference != decision
```

OMNIA-VALIDATION is not a truth oracle.

OMNIA-VALIDATION is not a semantic judge.

OMNIA-VALIDATION does not make final decisions.

Decision remains external.

---

## What this repository is

OMNIA-VALIDATION is a research-first validation layer.

It turns part of the OMNIA ecosystem from narrative claim into executable checks.

Current operational focus:

```text
artifact traceability
manifest generation
manifest validation
result regression
classification schema checking
hash checking
testable reproducibility
failure exposure
validation limits
```

Correct reading:

```text
less trust the claim
more run the check
```

---

## What this repository is not

OMNIA-VALIDATION is not:

- a proof that OMNIA is universally correct
- a semantic correctness evaluator
- a truth oracle
- a production safety certificate
- a replacement for external review
- a replacement for domain expertise
- a final decision layer

Validation evidence is structural evidence.

Structural evidence is not final truth.

---

## OMNIA Silent Failure validation bridge

OMNIA-VALIDATION includes a bridge document for the OMNIA Silent Failure Gate demo:

- [`docs/OMNIA_SILENT_FAILURE_VALIDATION_BRIDGE.md`](docs/OMNIA_SILENT_FAILURE_VALIDATION_BRIDGE.md)
- [`examples/validate_omnia_silent_failure_pattern.py`](examples/validate_omnia_silent_failure_pattern.py)

The bridge defines how OMNIA-VALIDATION should treat the minimal OMNIA demo as a reproducible, inspectable, and falsifiable validation target.

The source OMNIA demo is:

```text
OMNIA/examples/silent_failure_gate_demo.py
```

The minimal pattern to validate is:

```text
stable_output    -> Surface PASS -> OMNIA GO
fragile_output   -> Surface PASS -> OMNIA RISK
collapsed_output -> Surface FAIL -> OMNIA STOP
```

The central validation target is:

```text
fragile_output -> Surface PASS -> OMNIA RISK
```

This is the silent failure pattern.

It shows that an output can pass a surface check while still being structurally fragile under controlled perturbation.

Correct relationship:

```text
OMNIA            = structural measurement
OMNIA-VALIDATION = traceability / reproducibility / falsification
```

Boundary:

```text
measurement != inference != decision
```

This bridge does not claim that OMNIA-VALIDATION proves semantic truth.

It only defines how the OMNIA Silent Failure Gate result can become a validation artifact.

---

## Executable Silent Failure validation

OMNIA-VALIDATION includes an executable validator for the OMNIA Silent Failure Gate pattern:

- [`examples/validate_omnia_silent_failure_pattern.py`](examples/validate_omnia_silent_failure_pattern.py)

Run:

```bash
python examples/validate_omnia_silent_failure_pattern.py
```

The validator checks the minimal OMNIA pattern:

```text
stable_output    -> Surface PASS -> OMNIA GO
fragile_output   -> Surface PASS -> OMNIA RISK
collapsed_output -> Surface FAIL -> OMNIA STOP
```

It writes the validation artifact to:

```text
results/omnia_silent_failure_validation_result.json
```

The central validation target is:

```text
fragile_output -> Surface PASS -> OMNIA RISK
```

The validator checks structural pattern reproduction.

It does not validate semantic truth.

Boundary:

```text
measurement != inference != decision
```

---

## Operational chains

The repository currently has three main executable chains.

### 1. Artifact manifest generation

```text
data/source_outputs/
  -> examples/build_artifact_hash_manifest_v0.py
  -> results/artifact_hash_manifest_v0.json
```

Stable command:

```bash
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
```

### 2. Artifact manifest validation

```text
results/artifact_hash_manifest_v0.json
  -> omnia-validation validate-manifest ... --verify-hashes
  -> PASS / FAIL
```

Command:

```bash
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes
```

### 3. Result regression classification

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

---

## Quickstart

Clone, install, and test:

```bash
git clone https://github.com/Tuttotorna/OMNIA-VALIDATION.git
cd OMNIA-VALIDATION
python -m pip install --upgrade pip
python -m pip install -e .
python -m pytest -q
```

Expected clean status:

```text
254 passed
```

Run current operational checks:

```bash
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes

omnia-validation compare-results \
  --previous results/artifact_hash_manifest_v0.json \
  --current results/artifact_hash_manifest_v0.json
```

Reviewer guide:

- [`docs/REVIEWER_GUIDE.md`](docs/REVIEWER_GUIDE.md)
- [`docs/OMNIA_SILENT_FAILURE_VALIDATION_BRIDGE.md`](docs/OMNIA_SILENT_FAILURE_VALIDATION_BRIDGE.md)

Full quickstart:

- [`docs/QUICKSTART.md`](docs/QUICKSTART.md)

---

## Package layer

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

CLI commands:

```bash
omnia-validation validate-sha256 <sha256>
omnia-validation hash-file <path>
omnia-validation validate-json <path>
omnia-validation validate-result <path>
omnia-validation validate-manifest <path> --verify-hashes
omnia-validation compare-results --previous <path> --current <path>
```

Package API:

- [`docs/PACKAGE_API.md`](docs/PACKAGE_API.md)

---

## Validation scope

OMNIA-VALIDATION currently validates structural behavior through:

- artifact identity checks
- hash preservation
- schema validation
- result-envelope validation
- regression classification
- reproducibility baselines
- perturbation experiments
- temporal-collapse experiments
- topology and transition experiments
- cross-provider / cross-source traceability

Validation scope is documented in:

- [`docs/VALIDATION_SCOPE.md`](docs/VALIDATION_SCOPE.md)

---

## Results and evidence

The repository contains:

```text
data/      input datasets and source outputs
results/   raw result artifacts
docs/      result reports and validation notes
examples/  reproducible scripts
tests/     package and regression tests
```

Result index:

- [`docs/RESULTS_INDEX.md`](docs/RESULTS_INDEX.md)

Failure and limit cases:

- [`docs/FAILURE_CASES.md`](docs/FAILURE_CASES.md)

Repository status:

- [`docs/REPOSITORY_STATUS.md`](docs/REPOSITORY_STATUS.md)

---

## Relationship to OMNIA

OMNIA is the structural measurement core.

OMNIA-VALIDATION is the evidence and validation layer.

```text
OMNIA            = measure structural behavior
OMNIA-VALIDATION = test evidence, failures, limits, reproducibility
Decision          = external layer
```

Validation does not collapse measurement into decision.

---

## Citation

If you reference this repository, use the archived Zenodo record:

```text
DOI: 10.5281/zenodo.20083830
https://doi.org/10.5281/zenodo.20083830
```

Citation metadata is available in:

- [`CITATION.cff`](CITATION.cff)

---

## Summary

OMNIA-VALIDATION is the repository where OMNIA claims are pressure-tested.

It records evidence, limits, reproducibility checks, failures, and result regressions.

Its central rule is:

```text
validation evidence != semantic truth
measurement != inference != decision
```
