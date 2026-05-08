# OMNIA-VALIDATION — Documentation Index

This document is the navigation index for OMNIA-VALIDATION.

OMNIA-VALIDATION is a structural validation, falsification, perturbation testing, reproducibility, artifact traceability, and result-regression layer for the OMNIA ecosystem.

Core boundary:

```text
measurement != inference != decision
```

---

## Operational Chains

The repository currently exposes three executable chains.

### 1. Artifact Manifest Generation

```text
data/source_outputs/
  -> examples/build_artifact_hash_manifest_v0.py
  -> results/artifact_hash_manifest_v0.json
```

Command:

```bash
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
```

Purpose:

```text
scan data/source_outputs/
compute SHA-256
record size_bytes
write artifact_hash_manifest_v0.json
use deterministic timestamp when requested
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

---

## Main Entry Points

```text
README.md                       -> short operational overview
docs/INDEX.md                   -> documentation navigation
docs/QUICKSTART.md              -> first-run guide
docs/PROJECT_STATUS.md          -> current engineering/research status
docs/PACKAGE_API.md             -> Python package and CLI API
docs/RESULT_SCHEMA.md           -> canonical result envelope
docs/RESULT_REGRESSION_POLICY.md -> result difference policy
docs/ARTIFACT_HASH_MANIFEST_POLICY.md -> hash/manifest policy
```

---

## Engineering Documentation

```text
docs/QUICKSTART.md
docs/RUNNING_EXPERIMENTS.md
docs/MAINTENANCE.md
docs/RELEASE_POLICY.md
docs/CONSOLIDATION_ROADMAP_V0.md
```

Purpose:

```text
clone
install
test
run experiments
maintain results
prepare releases
continue consolidation
```

---

## Validation Documentation

```text
docs/VALIDATOR_AUTHORING_GUIDE.md
docs/VALIDATOR_REGISTRY.md
docs/RESULT_SCHEMA.md
docs/RESULT_REGRESSION_POLICY.md
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
docs/LEGACY_RESULT_NORMALIZATION.md
docs/LEGACY_STATUS_MAPPING.md
```

Purpose:

```text
define validator discipline
map validator families
define canonical result envelopes
classify result differences
define artifact hash traceability
preserve legacy result history
preserve legacy status values
```

---

## Package Modules

Python package:

```text
omnia_validation/
```

Current modules:

```text
omnia_validation.hashing      -> SHA-256 helpers
omnia_validation.io           -> JSON / JSONL helpers
omnia_validation.metrics      -> simple structural metrics
omnia_validation.metadata     -> metadata helpers
omnia_validation.schemas      -> result-envelope validation
omnia_validation.manifest     -> artifact manifest validation
omnia_validation.regression   -> result regression classification
omnia_validation.cli          -> command-line interface
```

Package root policy:

```text
omnia_validation/__init__.py exports only __version__
helpers should be imported from the module that defines them
```

API reference:

```text
docs/PACKAGE_API.md
```

---

## CLI Commands

```bash
omnia-validation validate-sha256 <sha256>
omnia-validation hash-file <path>
omnia-validation validate-json <path>
omnia-validation validate-result <path>
omnia-validation validate-manifest <path> --verify-hashes
omnia-validation compare-results --previous <path> --current <path>
```

Meaning:

```text
validate-sha256   -> check SHA-256 format
hash-file         -> compute file SHA-256
validate-json     -> check JSON / JSONL parseability
validate-result   -> check canonical result envelope
validate-manifest -> check artifact manifest and optional hash matches
compare-results   -> classify structural differences between result artifacts
```

---

## Tests

Test suite:

```text
tests/
```

Important test families:

```text
tests/test_hashing.py
tests/test_io.py
tests/test_metrics.py
tests/test_metadata.py
tests/test_cli.py
tests/test_cli_manifest.py
tests/test_cli_regression.py
tests/test_schemas.py
tests/test_manifest.py
tests/test_regression.py
tests/test_build_artifact_hash_manifest.py
tests/test_existing_results.py
tests/test_enveloped_results.py
tests/test_wrap_legacy_results.py
```

Run:

```bash
pytest -q
ruff check omnia_validation tests
```

---

## Result Directories

```text
results/           -> historical and generated JSON result files
results_enveloped/ -> canonical-envelope wrappers for legacy results
data/              -> bounded datasets and source-output records
examples/          -> runnable scripts
docs/              -> documentation and result reports
```

Important current result:

```text
results/artifact_hash_manifest_v0.json
```

Legacy normalization:

```text
results/ preserves historical artifacts
results_enveloped/ provides schema-valid wrappers
wrapping is format normalization, not scientific revalidation
```

---

## Temporal Collapse Documentation

Level 3 entry point:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
```

Topology entry point:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_INDEX_V0.md
```

Useful related docs:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_FINAL_SUMMARY_V0.md
docs/TEMPORAL_COLLAPSE_TOPOLOGY_EXPERIMENT_CHAIN_V0.md
docs/TEMPORAL_COLLAPSE_TOPOLOGY_BOUNDARY_PHASE_DIAGRAM_V0_RESULT.md
```

---

## Current Status

Current status document:

```text
docs/PROJECT_STATUS.md
```

Current engineering state:

```text
CI-enabled
installable package layer present
manifest generator present
validate-manifest CLI present
result regression module present
compare-results CLI present
tests present
not production-certified
```

---

## Current Limitations

Known remaining limitations:

```text
payload-specific schemas are still incomplete
full per-file validator registry is still incomplete
full experiment-chain CI is still missing
repository-wide artifact manifest is still missing
release-grade baseline manifests are still missing
external reproduction is still needed
```

---

## Reading Order

Recommended order for new readers:

```text
README.md
docs/INDEX.md
docs/QUICKSTART.md
docs/PROJECT_STATUS.md
docs/PACKAGE_API.md
docs/RESULT_SCHEMA.md
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
docs/RESULT_REGRESSION_POLICY.md
docs/VALIDATOR_AUTHORING_GUIDE.md
docs/VALIDATOR_REGISTRY.md
docs/LEGACY_RESULT_NORMALIZATION.md
docs/LEGACY_STATUS_MAPPING.md
docs/CONSOLIDATION_ROADMAP_V0.md
```

---

## Contribution And Governance

```text
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
.github/ISSUE_TEMPLATE/
.github/pull_request_template.md
```

---

## Non-Goal

OMNIA-VALIDATION does not claim:

```text
semantic truth detection
universal correctness
model intelligence certification
production safety certification
decision authority
```

Final boundary:

```text
measurement != inference != decision
```
