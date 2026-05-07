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
schema-checkable
```

Core boundary:

```text
measurement != inference != decision
```

A result file records structural validation behavior.

It does not certify semantic truth.

It does not make final decisions.

---

## 1. Schema Validation Module

The result schema is now partially enforceable through the package module:

```text
omnia_validation.schemas
```

Source file:

```text
omnia_validation/schemas.py
```

Current schema helpers:

```text
validate_result_envelope
is_valid_result_envelope
require_valid_result_envelope
```

Current schema constants:

```text
ALLOWED_RESULT_STATUSES
REQUIRED_RESULT_FIELDS
DEFAULT_BOUNDARY
```

Important limitation:

```text
The current schema validator checks the canonical top-level envelope only.
It does not yet validate every possible payload field.
```

This means the current code checks:

```text
experiment
status
created_at_utc
boundary
payload
```

It does not yet fully enforce:

```text
trajectory payload fields
topology payload fields
hash payload fields
regime payload fields
failure mode vocabulary
```

Those may be added in later schema versions.

---

## 2. Canonical Result Envelope

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

These fields are defined in code as:

```python
REQUIRED_RESULT_FIELDS = frozenset(
    {
        "experiment",
        "status",
        "created_at_utc",
        "boundary",
        "payload",
    }
)
```

---

## 3. Field Definitions

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
non-empty string
```

The current schema validator checks that:

```text
experiment is present
experiment is a string
experiment is not empty
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

These are defined in code as:

```python
ALLOWED_RESULT_STATUSES = frozenset({"PASS", "CHECK", "FAIL"})
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

The current schema validator checks that:

```text
status is present
status is a string
status is one of PASS, CHECK, FAIL
```

---

### created_at_utc

The UTC timestamp when the result was generated.

Recommended format:

```text
ISO-8601 UTC
```

Accepted examples:

```text
2026-05-07T00:00:00+00:00
2026-05-07T00:00:00Z
```

The current schema validator checks that:

```text
created_at_utc is present
created_at_utc is a string
created_at_utc is not empty
created_at_utc contains +00:00 or ends with Z
```

---

### boundary

The epistemic boundary of the result.

Default value:

```text
measurement != inference != decision
```

This is defined in code as:

```python
DEFAULT_BOUNDARY = "measurement != inference != decision"
```

This field should remain visible in every result file.

The current schema validator checks that:

```text
boundary is present
boundary is a string
boundary equals measurement != inference != decision
```

---

### payload

The experiment-specific result body.

The payload contains counts, metrics, regimes, failure modes, paths, hashes, summaries, and interpretation boundaries.

It must be a JSON object.

The current schema validator checks that:

```text
payload is present
payload is a mapping/object
```

---

## 4. Validating A Result Envelope

Basic validation:

```python
from omnia_validation.schemas import validate_result_envelope

errors = validate_result_envelope(result)

if errors:
    print(errors)
else:
    print("PASS")
```

Boolean validation:

```python
from omnia_validation.schemas import is_valid_result_envelope

if is_valid_result_envelope(result):
    print("valid")
else:
    print("invalid")
```

Strict validation:

```python
from omnia_validation.schemas import require_valid_result_envelope

require_valid_result_envelope(result)
```

If the result is invalid, `require_valid_result_envelope` raises:

```text
ValueError
```

---

## 5. Recommended Validator Usage

A validator should build the result, validate it, then write it.

Recommended pattern:

```python
from omnia_validation.io import write_json
from omnia_validation.metadata import result_envelope
from omnia_validation.schemas import require_valid_result_envelope

payload = {
    "record_count": 10,
    "input_path": "data/example_input_v0.jsonl",
    "output_path": "results/example_validator_v0.json",
    "main_signal": "record_presence",
    "decision_reason": "Input records were valid.",
}

result = result_envelope(
    experiment="example_validator_v0",
    status="PASS",
    payload=payload,
)

require_valid_result_envelope(result)
write_json("results/example_validator_v0.json", result)
```

This makes result generation fail early if the top-level envelope is invalid.

---

## 6. Recommended Base Payload

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

Current enforcement status:

```text
recommended
not yet automatically enforced
```

---

## 7. Common Payload Fields

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

Current enforcement status:

```text
recommended
not yet automatically enforced
```

---

## 8. Regime Fields

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

Current enforcement status:

```text
recommended
not yet automatically enforced
```

---

## 9. Hash Traceability Fields

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

Current enforcement status:

```text
recommended
not yet automatically enforced
```

---

## 10. Trajectory Fields

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

Current enforcement status:

```text
recommended
not yet automatically enforced
```

---

## 11. Topology Fields

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

Current enforcement status:

```text
recommended
not yet automatically enforced
```

---

## 12. Failure and Boundary Fields

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

Current enforcement status:

```text
recommended
not yet automatically enforced
```

---

## 13. Input and Output Paths

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

Current enforcement status:

```text
recommended
not yet automatically enforced
```

---

## 14. JSON Formatting Rules

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

The helper `write_json` currently uses:

```text
UTF-8
ensure_ascii=False
sort_keys=True
final newline
```

---

## 15. JSONL Rules

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

The current JSONL reader checks that each non-empty line is a JSON object.

---

## 16. Status Selection Rule

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

The current schema validator enforces only that the status value is one of:

```text
PASS
CHECK
FAIL
```

It does not infer whether the selected status is scientifically correct.

---

## 17. Interpretation Rule

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

## 18. Minimal Complete Example

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

This example passes the current envelope validator.

---

## 19. Hash Validator Example

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

This example passes the current envelope validator.

The specific hash payload fields are recommended but not yet enforced.

---

## 20. CHECK Example

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

This example passes the current envelope validator.

A `CHECK` result should not be rewritten as `PASS` unless the underlying measurement logic changes and justifies it.

---

## 21. FAIL Example

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

This example passes the current envelope validator because the envelope is structurally valid.

The scientific failure is represented in:

```text
status
payload.decision_reason
payload.failure_modes
```

---

## 22. Invalid Envelope Examples

### Missing required field

```json
{
  "experiment": "example_validator_v0",
  "status": "PASS"
}
```

Expected schema errors:

```text
missing required field: boundary
missing required field: created_at_utc
missing required field: payload
```

---

### Invalid status

```json
{
  "boundary": "measurement != inference != decision",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "experiment": "example_validator_v0",
  "payload": {},
  "status": "UNKNOWN"
}
```

Expected schema error:

```text
status must be one of: CHECK, FAIL, PASS
```

---

### Wrong boundary

```json
{
  "boundary": "measurement == decision",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "experiment": "example_validator_v0",
  "payload": {},
  "status": "PASS"
}
```

Expected schema error:

```text
boundary should be: measurement != inference != decision
```

---

### Non-object payload

```json
{
  "boundary": "measurement != inference != decision",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "experiment": "example_validator_v0",
  "payload": [],
  "status": "PASS"
}
```

Expected schema error:

```text
payload must be a mapping/object
```

---

## 23. Schema Checklist

Before committing a result file, verify:

```text
Top-level object is valid JSON.
experiment is present.
experiment is a non-empty string.
status is PASS, CHECK, or FAIL.
created_at_utc is present.
created_at_utc is UTC-like.
boundary is present.
boundary equals measurement != inference != decision.
payload is an object.
input/output paths are relative.
failure or boundary conditions are not hidden.
claims stay inside the tested construction.
```

Use:

```bash
omnia-validation validate-json results/<result_file>.json
```

Then, from Python:

```python
from omnia_validation.io import read_json
from omnia_validation.schemas import require_valid_result_envelope

result = read_json("results/<result_file>.json")
require_valid_result_envelope(result)
```

---

## 24. Current Automated Tests

Schema tests are located in:

```text
tests/test_schemas.py
```

They currently verify:

```text
schema constants
valid envelope acceptance
missing field detection
invalid status detection
empty experiment detection
non-UTC timestamp detection
Z-suffix timestamp acceptance
wrong boundary detection
non-object payload detection
non-mapping result detection
strict validation failure raising
```

Run:

```bash
pytest -q
```

---

## 25. Current Limits

The current schema layer is intentionally minimal.

It does not yet enforce:

```text
payload-specific schemas
hash-validator payload rules
trajectory-validator payload rules
topology-validator payload rules
allowed failure mode vocabulary
allowed regime vocabulary
relative path validation
numeric range validation
cross-file artifact existence
hash manifest validation
```

These should be future extensions.

---

## 26. Future Schema Extensions

Possible future modules or functions:

```text
validate_hash_payload
validate_trajectory_payload
validate_topology_payload
validate_relative_paths
validate_failure_modes
validate_regime_fields
validate_result_file
validate_result_directory
```

Possible future package module:

```text
omnia_validation.schemas
```

Already present:

```text
validate_result_envelope
is_valid_result_envelope
require_valid_result_envelope
```

---

## 27. Non-Goal

This schema does not define semantic truth.

It does not define intelligence.

It does not certify production safety.

It defines a reproducible structure for reporting structural validation behavior.

Final boundary:

```text
measurement != inference != decision
```