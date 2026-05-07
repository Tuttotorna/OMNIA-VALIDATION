# OMNIA-VALIDATION — Result Schema

## Purpose

This document defines the recommended JSON result schema for OMNIA-VALIDATION experiments.

The goal is to make result files:

```text
readable
parseable
comparable
reproducible
auditable
falsifiable
```

Core boundary:

```text
measurement != inference != decision
```

A result file records structural validation behavior.

It does not certify semantic truth.

It does not make final decisions.

---

## 1. Canonical Result Envelope

Every result file should use this top-level structure:

```json
{
  "experiment": "example_validator_v0",
  "status": "PASS",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "boundary": "measurement != inference != decision",
  "payload": {}
}
```

Required top-level fields:

```text
experiment
status
created_at_utc
boundary
payload
```

---

## 2. Field Definitions

### experiment

The validator or experiment name.

Example:

```text
temporal_collapse_external_source_hash_strengthening_validator_v15
```

Rules:

```text
lowercase snake_case
explicit domain
explicit pressure condition
explicit version
```

---

### status

The final validation status.

Allowed values:

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
CHECK is a valid scientific output.
FAIL is a valid scientific output.
```

A result should not be rewritten only to obtain `PASS`.

---

### created_at_utc

The UTC timestamp when the result was generated.

Recommended format:

```text
ISO-8601
```

Example:

```text
2026-05-07T00:00:00+00:00
```

---

### boundary

The epistemic boundary of the result.

Default value:

```text
measurement != inference != decision
```

This field should remain visible in every result file.

---

### payload

The experiment-specific result body.

The payload contains counts, metrics, regimes, failure modes, paths, hashes, summaries, and interpretation boundaries.

It must be a JSON object.

---

## 3. Recommended Base Payload

Every validator payload should include at least:

```json
{
  "record_count": 0,
  "input_path": "data/example_input_v0.jsonl",
  "output_path": "results/example_validator_v0.json",
  "main_signal": "none",
  "decision_reason": "No records were available."
}
```

Recommended fields:

```text
record_count
input_path
output_path
main_signal
decision_reason
```

---

## 4. Common Payload Fields

Use these fields when applicable:

```text
record_count
trajectory_count
event_count
node_count
edge_count
cluster_count
source_file_count
computed_hash_count
real_hash_count
placeholder_hash_count
hash_format_failure_count
hash_mismatch_failure_count
aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action
accuracy_rate
extraction_rate
regime_counts
boundary_conditions
failure_modes
warnings
```

---

## 5. Regime Fields

When a validator classifies structural regimes, use:

```json
{
  "aggregate_risk_score": 0.379255,
  "aggregate_risk_regime": "DRIFT",
  "aggregate_gate_action": "WATCH",
  "regime_counts": {
    "CRITICAL": 4,
    "DRIFT": 10,
    "STABLE": 6
  }
}
```

Recommended regime labels:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
UNKNOWN
```

Recommended gate actions:

```text
PASS
WATCH
RETRY
ESCALATE
BLOCK
```

Interpretation:

```text
STABLE   -> no major structural instability detected in the tested condition
DRIFT    -> measurable instability or structural movement detected
CRITICAL -> high-risk local or aggregate instability detected
COLLAPSE -> structural failure or non-recoverable degradation detected
UNKNOWN  -> insufficient or ambiguous evidence
```

---

## 6. Hash Traceability Fields

For hash-based validators, include:

```json
{
  "source_file_count": 4,
  "computed_hash_count": 4,
  "real_hash_count": 4,
  "placeholder_hash_count": 0,
  "hash_format_failure_count": 0,
  "hash_mismatch_failure_count": 0
}
```

Meaning:

```text
source_file_count              -> number of source artifacts checked
computed_hash_count            -> number of hashes computed by the validator
real_hash_count                -> number of real non-placeholder hashes
placeholder_hash_count         -> number of symbolic placeholder hashes
hash_format_failure_count      -> number of malformed hash values
hash_mismatch_failure_count    -> number of source/hash mismatches
```

Strong traceability condition:

```text
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0
```

---

## 7. Trajectory Fields

For trajectory validators, include:

```json
{
  "trajectory_count": 20,
  "event_count": 100,
  "highest_risk_trajectory": "example_trajectory_001",
  "highest_risk_score": 0.7096,
  "aggregate_risk_score": 0.379255,
  "aggregate_risk_regime": "DRIFT",
  "aggregate_gate_action": "WATCH"
}
```

Recommended fields:

```text
trajectory_count
event_count
highest_risk_trajectory
highest_risk_score
aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action
```

---

## 8. Topology Fields

For topology validators, include:

```json
{
  "node_count": 12,
  "edge_count": 28,
  "cluster_count": 4,
  "centrality_summary": {},
  "control_plane_candidates": [],
  "boundary_conditions": []
}
```

Recommended fields:

```text
node_count
edge_count
cluster_count
centrality_summary
control_plane_candidates
dependency_map
boundary_conditions
phase_regions
```

---

## 9. Failure and Boundary Fields

When instability is detected, do not hide it.

Use:

```json
{
  "failure_modes": [
    "threshold_instability",
    "representation_dependence"
  ],
  "boundary_conditions": [
    "control_plane_not_universally_invariant"
  ],
  "warnings": [
    "CHECK result indicates partial robustness only."
  ]
}
```

Recommended failure mode labels:

```text
threshold_instability
representation_dependence
observer_sensitivity
metric_degeneracy
hash_mismatch
invalid_artifact
dependency_boundary
structural_collapse
semantic_structural_divergence
```

---

## 10. Input and Output Paths

Always use relative repository paths.

Good:

```text
data/example_input_v0.jsonl
results/example_validator_v0.json
docs/EXAMPLE_VALIDATOR_V0_RESULT.md
```

Avoid:

```text
/home/user/project/data/example_input_v0.jsonl
C:\Users\name\project\data\example_input_v0.jsonl
```

Reason:

```text
relative paths survive across machines
absolute paths leak environment-specific details
```

---

## 11. JSON Formatting Rules

Result files should be written with:

```text
UTF-8 encoding
two-space indentation
sorted keys when practical
final newline
valid JSON object at top level
```

Preferred writer:

```python
from omnia_validation.io import write_json

write_json("results/example_validator_v0.json", result)
```

---

## 12. JSONL Rules

Use JSONL for datasets and source-output records.

Rules:

```text
one JSON object per line
no trailing commas
blank lines allowed only if reader supports them
stable field names
bounded record count
```

Validate JSONL files with:

```bash
omnia-validation validate-json data/example_input_v0.jsonl
```

---

## 13. Status Selection Rule

Use `PASS` only when the tested structural condition survives the validation step.

Use `CHECK` when:

```text
partial instability exists
boundary condition exists
evidence is mixed
robustness is incomplete
threshold sensitivity is detected
```

Use `FAIL` when:

```text
artifact is invalid
required source is missing
hash mismatch occurs
metric collapses
result cannot be reproduced
structural condition fails the validator
```

---

## 14. Interpretation Rule

A result should include enough information to answer:

```text
What was tested?
What input was used?
What condition was applied?
What was measured?
What survived?
What drifted?
What collapsed?
What boundary was exposed?
```

A result should not claim:

```text
semantic truth
model intelligence
universal validity
production safety
final correctness
```

---

## 15. Minimal Complete Example

```json
{
  "boundary": "measurement != inference != decision",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "experiment": "example_validator_v0",
  "payload": {
    "decision_reason": "Input records were valid and the tested structural condition survived.",
    "input_path": "data/example_input_v0.jsonl",
    "main_signal": "record_presence",
    "output_path": "results/example_validator_v0.json",
    "record_count": 10
  },
  "status": "PASS"
}
```

---

## 16. Hash Validator Example

```json
{
  "boundary": "measurement != inference != decision",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "experiment": "external_source_hash_strengthening_validator_v0",
  "payload": {
    "computed_hash_count": 4,
    "decision_reason": "All source files produced real SHA-256 hashes with no placeholder or mismatch failures.",
    "hash_format_failure_count": 0,
    "hash_mismatch_failure_count": 0,
    "placeholder_hash_count": 0,
    "real_hash_count": 4,
    "source_file_count": 4
  },
  "status": "PASS"
}
```

---

## 17. CHECK Example

```json
{
  "boundary": "measurement != inference != decision",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "experiment": "control_plane_robustness_validator_v0",
  "payload": {
    "boundary_conditions": [
      "control_plane_not_universally_invariant"
    ],
    "decision_reason": "The control plane survived some perturbations but drifted under threshold-axis variation.",
    "failure_modes": [
      "threshold_instability"
    ],
    "main_signal": "partial_control_plane_robustness"
  },
  "status": "CHECK"
}
```

---

## 18. FAIL Example

```json
{
  "boundary": "measurement != inference != decision",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "experiment": "artifact_integrity_validator_v0",
  "payload": {
    "decision_reason": "Required source file was missing.",
    "failure_modes": [
      "invalid_artifact"
    ],
    "input_path": "data/missing_input_v0.jsonl",
    "main_signal": "missing_source_file"
  },
  "status": "FAIL"
}
```

---

## 19. Schema Checklist

Before committing a result file, verify:

```text
Top-level object is valid JSON.
experiment is present.
status is PASS, CHECK, or FAIL.
created_at_utc is present.
boundary is present.
payload is an object.
input/output paths are relative.
failure or boundary conditions are not hidden.
claims stay inside the tested construction.
```

Use:

```bash
omnia-validation validate-json results/<result_file>.json
```

---

## 20. Non-Goal

This schema does not define semantic truth.

It does not define intelligence.

It does not certify production safety.

It defines a reproducible structure for reporting structural validation behavior.

Final boundary:

```text
measurement != inference != decision
```