# OMNIA-VALIDATION v0.2.0 — Artifact Traceability and Result Regression

Release tag:

```text
v0.2.0
```

Core boundary:

```text
measurement != inference != decision
```

---

## Summary

OMNIA-VALIDATION v0.2.0 marks the transition from a mainly documentation-and-experiment repository into an executable validation layer with artifact traceability and result-regression classification.

This release does not claim semantic truth detection, production safety certification, or final scientific correctness.

It provides reproducible structural checks.

---

## Main Additions

### Artifact Manifest Generation

Added a manifest generator:

```text
examples/build_artifact_hash_manifest_v0.py
```

Current command:

```bash
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
```

Current scope:

```text
data/source_outputs/
```

Current output:

```text
results/artifact_hash_manifest_v0.json
```

The generator computes SHA-256 hashes, records artifact paths, records byte sizes, and supports deterministic timestamps.

---

### Artifact Manifest Validation

Added manifest validation helpers:

```text
omnia_validation.manifest
```

Added CLI support:

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
hash match means artifact byte identity is preserved
hash match does not prove semantic truth
hash traceability does not certify production safety
```

---

### Result Regression Automation

Added result-regression classification:

```text
omnia_validation.regression
examples/compare_result_regression_v0.py
```

Added CLI support:

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

---

### Documentation Cleanup

Cleaned and shortened:

```text
README.md
docs/INDEX.md
```

The README now presents the operational chains directly.

The documentation index now acts as a navigation layer instead of a second long README.

---

## Current Operational Chains

### 1. Build manifest

```bash
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
```

### 2. Validate manifest

```bash
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes
```

### 3. Compare results

```bash
omnia-validation compare-results \
  --previous results/artifact_hash_manifest_v0.json \
  --current results/artifact_hash_manifest_v0.json
```

---

## Test Status At Release

Release validation commands:

```bash
ruff check omnia_validation tests
pytest -q
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes
omnia-validation compare-results --previous results/artifact_hash_manifest_v0.json --current results/artifact_hash_manifest_v0.json
```

Expected state:

```text
ruff: pass
pytest: pass
validate-manifest: PASS
compare-results: NO_REGRESSION
```

---

## Known Limitations

This release is not v1.0.0.

Known limitations remain:

```text
payload-specific schemas are still incomplete
full per-file validator registry is still incomplete
full experiment-chain CI is still missing
repository-wide artifact manifest is still missing
release-grade baseline manifests are still missing
external reproduction is still needed
production certification is not claimed
```

---

## Non-Claims

This release does not claim:

```text
semantic truth detection
universal correctness
model intelligence certification
production safety certification
decision authority
scientific finality
```

Final boundary:

```text
measurement != inference != decision
```

