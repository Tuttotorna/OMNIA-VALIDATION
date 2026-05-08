# OMNIA-VALIDATION — Reviewer Guide

This guide is for external reviewers, readers, researchers, engineers, and skeptics who want to verify the current operational claims of OMNIA-VALIDATION.

It is not a trust document.

It is an execution guide.

Core boundary:

```text
measurement != inference != decision
```

---

## What This Guide Verifies

This guide verifies the executable v0.2.0 operational layer:

```text
package installation
unit tests
artifact manifest generation
artifact manifest validation
result regression classification
```

It does not verify semantic truth.

It does not certify production safety.

It does not prove universal correctness.

---

## Repository

```text
https://github.com/Tuttotorna/OMNIA-VALIDATION
```

Release:

```text
https://github.com/Tuttotorna/OMNIA-VALIDATION/releases/tag/v0.2.0
```

DOI:

```text
https://doi.org/10.5281/zenodo.20083830
```

---

## Minimal Verification Path

Run:

```bash
git clone https://github.com/Tuttotorna/OMNIA-VALIDATION.git
cd OMNIA-VALIDATION
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest -q
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes
omnia-validation compare-results \
  --previous results/artifact_hash_manifest_v0.json \
  --current results/artifact_hash_manifest_v0.json
```

Expected high-level result:

```text
pytest: passed
validate-manifest: PASS
compare-results: NO_REGRESSION
```

---

## One-Cell Colab Verification

Use this cell in a fresh Colab session:

```python
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/Tuttotorna/OMNIA-VALIDATION.git"
REPO_DIR = Path("/content/OMNIA-VALIDATION")

def run(cmd, cwd=None):
    print("\n" + "=" * 100)
    print("RUN:", " ".join(cmd))
    print("=" * 100)
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    if result.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(cmd)}")
    return result

if REPO_DIR.exists():
    run(["rm", "-rf", str(REPO_DIR)])

run(["git", "clone", REPO_URL, str(REPO_DIR)], cwd="/content")
run(["python", "-m", "pip", "install", "--upgrade", "pip"], cwd=REPO_DIR)
run(["python", "-m", "pip", "install", "-e", ".[dev]"], cwd=REPO_DIR)
run(["pytest", "-q"], cwd=REPO_DIR)
run(["python", "examples/build_artifact_hash_manifest_v0.py", "--stable-timestamp"], cwd=REPO_DIR)
run(["omnia-validation", "validate-manifest", "results/artifact_hash_manifest_v0.json", "--verify-hashes"], cwd=REPO_DIR)
run([
    "omnia-validation",
    "compare-results",
    "--previous",
    "results/artifact_hash_manifest_v0.json",
    "--current",
    "results/artifact_hash_manifest_v0.json",
], cwd=REPO_DIR)

print("\nVERIFICATION COMPLETE")
```

---

## Operational Chain 1 — Artifact Manifest Generation

Command:

```bash
python examples/build_artifact_hash_manifest_v0.py --stable-timestamp
```

Expected behavior:

```text
scans data/source_outputs/
computes SHA-256 hashes
records artifact paths
records size_bytes
writes results/artifact_hash_manifest_v0.json
uses deterministic timestamp
```

Expected stable timestamp:

```text
2026-05-07T00:00:00+00:00
```

Correct interpretation:

```text
the manifest records byte-level artifact identity signals
the manifest improves traceability
```

Incorrect interpretation:

```text
the manifest proves semantic truth
the manifest proves scientific correctness
the manifest certifies production safety
```

---

## Operational Chain 2 — Artifact Manifest Validation

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

Meaning:

```text
manifest structure is valid
recorded SHA-256 hashes match current file bytes
```

Boundary:

```text
hash match -> artifact byte identity preserved
hash match != semantic truth
```

---

## Operational Chain 3 — Result Regression Classification

Command:

```bash
omnia-validation compare-results \
  --previous results/artifact_hash_manifest_v0.json \
  --current results/artifact_hash_manifest_v0.json
```

Expected output:

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

Meaning:

```text
result differences are classified structural evidence
result differences are not automatically errors
NO_REGRESSION means compared artifacts are structurally identical
```

Boundary:

```text
regression classification != semantic correctness
regression classification != final interpretation
```

---

## How To Try To Break It

A reviewer can test failure behavior by modifying artifacts locally.

Examples:

```text
edit a file in data/source_outputs/
change a recorded sha256 value in results/artifact_hash_manifest_v0.json
delete a required result field
change the boundary string
compare two intentionally different result files
```

Expected outcomes:

```text
validate-manifest should fail on hash mismatch
compare-results should classify structural differences
schema validation should fail on invalid result envelopes
```

This is intentional.

The goal is not to hide failures.

The goal is to make failures classifiable.

---

## What PASS Means

A PASS result means:

```text
the tested structural condition passed under the specified check
```

A PASS result does not mean:

```text
semantic truth
scientific finality
production safety
universal correctness
```

---

## What NO_REGRESSION Means

`NO_REGRESSION` means:

```text
the compared result artifacts are structurally identical under the current comparison layer
```

`NO_REGRESSION` does not mean:

```text
the result is semantically true
the experiment is scientifically final
external review is unnecessary
```

---

## Current Limitations

Known limitations:

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

## Reviewer Summary

A reviewer should be able to verify:

```text
the package installs
the tests pass
the manifest can be generated
the manifest validates
identical results classify as NO_REGRESSION
```

That is the current executable claim.

Final boundary:

```text
measurement != inference != decision
```
