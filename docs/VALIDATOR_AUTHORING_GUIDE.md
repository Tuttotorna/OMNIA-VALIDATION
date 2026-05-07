# OMNIA-VALIDATION — Validator Authoring Guide

## Purpose

This guide explains how to add new validators to OMNIA-VALIDATION.

A validator is a bounded experiment that pressure-tests a structural measurement under controlled conditions.

Core boundary:

```text
measurement != inference != decision
```

A validator does not prove semantic truth.

A validator does not make final decisions.

A validator exposes structural behavior.

---

## 1. What A Validator Is

A validator is a reproducible experiment with:

```text
bounded input
explicit transformation
visible parameters
deterministic or documented execution
structured output
clear pass/check/fail logic
documented boundary
```

A validator should answer one question:

```text
What happens to the measured structure under this controlled condition?
```

---

## 2. What A Validator Is Not

A validator is not:

```text
a semantic truth detector
a correctness oracle
a production-safety certificate
a benchmark leaderboard
a final proof
a narrative justification
```

It must not claim more than it measures.

---

## 3. Required File Pattern

A new validator should usually include:

```text
examples/<validator_name>.py
data/<input_dataset>.jsonl
results/<validator_name>.json
docs/<VALIDATOR_NAME>.md
docs/<VALIDATOR_NAME>_RESULT.md
```

Example:

```text
examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py
data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15.md
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15_RESULT.md
```

---

## 4. Naming Convention

Use explicit names.

Good:

```text
temporal_collapse_cross_provider_disagreement_validator_v13.py
temporal_collapse_repeated_run_cross_provider_stability_validator_v14.py
temporal_collapse_external_source_hash_strengthening_validator_v15.py
```

Weak:

```text
test.py
experiment.py
run.py
new_validator.py
```

The name should expose:

```text
domain
pressure condition
measured behavior
version
```

---

## 5. Minimal Validator Structure

A validator script should contain:

```text
configuration
input loading
validation logic
result construction
result writing
summary printing
```

Recommended skeleton:

```python
from __future__ import annotations

from pathlib import Path

from omnia_validation.io import read_jsonl, write_json
from omnia_validation.metadata import result_envelope

VALIDATOR_NAME = "example_validator_v0"

INPUT_PATH = Path("data/example_input_v0.jsonl")
RESULT_PATH = Path("results/example_validator_v0.json")


def validate(records: list[dict]) -> dict:
    """Run structural validation logic."""
    total = len(records)

    return {
        "record_count": total,
        "status": "PASS" if total > 0 else "FAIL",
    }


def main() -> int:
    records = read_jsonl(INPUT_PATH)
    payload = validate(records)

    result = result_envelope(
        experiment=VALIDATOR_NAME,
        status=payload["status"],
        payload=payload,
    )

    write_json(RESULT_PATH, result)

    print(f"{VALIDATOR_NAME}: {payload['status']}")
    print(f"result: {RESULT_PATH}")

    return 0 if payload["status"] in {"PASS", "CHECK"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

---

## 6. Result Status Logic

Use this status vocabulary:

```text
PASS
CHECK
FAIL
```

Meaning:

```text
PASS  -> the tested structural condition survived this validation step
CHECK -> partial instability, ambiguity, or boundary condition detected
FAIL  -> collapse, mismatch, invalid artifact, or validation failure detected
```

Important:

```text
CHECK is not cosmetic.
FAIL is not shameful.
```

A `CHECK` or `FAIL` can be scientifically valuable if it exposes a real boundary.

---

## 7. Recommended Result Schema

Every result file should include:

```text
experiment
status
created_at_utc
boundary
payload
```

Recommended envelope:

```json
{
  "experiment": "example_validator_v0",
  "status": "PASS",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "boundary": "measurement != inference != decision",
  "payload": {
    "record_count": 10
  }
}
```

The `payload` should contain experiment-specific fields.

---

## 8. Required Result Fields

At minimum, the payload should include:

```text
record_count
input_path
output_path
main_metric_or_signal
decision_reason
```

For hash-based validators, include:

```text
source_file_count
computed_hash_count
real_hash_count
placeholder_hash_count
hash_format_failure_count
hash_mismatch_failure_count
```

For trajectory validators, include:

```text
trajectory_count
event_count
regime_counts
highest_risk_trajectory
aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action
```

For topology validators, include:

```text
node_count
edge_count
cluster_count
centrality_summary
control_plane_candidates
boundary_conditions
```

---

## 9. Input Dataset Rules

Input datasets should be bounded.

Good:

```text
small enough to inspect
large enough to expose the tested behavior
stored as JSON or JSONL
stable across reruns
documented
```

Avoid:

```text
hidden online dependency
unbounded external API calls
silent random generation
undocumented filtering
implicit manual edits
```

If randomness is required, define:

```text
seed
distribution
sample size
generation rule
```

---

## 10. Reproducibility Rules

A validator should be runnable from a clean clone.

Required:

```bash
python -m pip install -e ".[dev]"
python examples/<validator_name>.py
```

Then verify:

```bash
omnia-validation validate-json results/<validator_name>.json
```

Before committing:

```bash
pytest -q
ruff check omnia_validation tests
```

---

## 11. Documentation Rules

Each validator should have a documentation file explaining:

```text
purpose
input data
pressure condition
measured signal
status logic
known boundary
non-claims
reproduction command
result file
```

Recommended document structure:

```md
# <Validator Name>

## Purpose

## Input

## Method

## Status Logic

## Result

## Boundary

## Reproduction

## Non-Claims
```

---

## 12. Result Report Rules

Each result report should explain what happened, not what one wishes happened.

Include:

```text
actual status
main counts
main metric values
detected instability
detected boundary
interpretation limits
```

Do not hide:

```text
weak correlation
partial drift
threshold instability
unexpected collapse
negative result
```

Negative evidence is valid evidence when it is reproducible.

---

## 13. Boundary Language

Every validator should preserve this boundary:

```text
measurement != inference != decision
```

Use precise claim language.

Good:

```text
This validator detected structural drift under repeated-run variation.
```

Weak:

```text
This proves the model is unreliable.
```

Good:

```text
This result exposes a boundary condition in this tested construction.
```

Weak:

```text
This proves universal instability.
```

---

## 14. Versioning Rule

Use versions when the validator logic changes:

```text
v0
v1
v2
```

Use a new version when changing:

```text
input construction
metric definition
threshold logic
status logic
aggregation method
hash method
trajectory extraction rule
```

Do not create a new version only for:

```text
typo fixes
formatting cleanup
documentation clarification
```

---

## 15. When To Use Package Utilities

Use the package layer for reusable operations:

```text
omnia_validation.hashing
omnia_validation.io
omnia_validation.metrics
omnia_validation.metadata
```

Examples:

```python
from omnia_validation.hashing import sha256_file
from omnia_validation.io import read_jsonl, write_json
from omnia_validation.metadata import result_envelope
from omnia_validation.metrics import shannon_entropy
```

This reduces duplicated logic across experimental scripts.

---

## 16. Validator Quality Checklist

Before adding a validator, check:

```text
Does it have bounded input?
Does it have explicit pressure condition?
Does it write structured output?
Does it preserve negative results?
Does it avoid semantic overclaiming?
Does it use PASS/CHECK/FAIL consistently?
Can it run from a clean clone?
Is the result file parseable JSON?
Is the documentation clear?
Does the claim stay inside the tested construction?
```

---

## 17. Pull Request Checklist

Before opening a pull request:

```bash
pytest -q
ruff check omnia_validation tests
```

Also verify any generated artifact:

```bash
omnia-validation validate-json results/<validator_name>.json
```

If the validator uses JSONL:

```bash
omnia-validation validate-json data/<input_dataset>.jsonl
```

---

## 18. Non-Goal

This guide does not define a universal scientific method.

It defines repository discipline for structural validation experiments.

Final boundary:

```text
measurement != inference != decision
```