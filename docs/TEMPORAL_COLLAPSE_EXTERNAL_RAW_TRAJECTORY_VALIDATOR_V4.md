# Temporal Collapse External Raw Trajectory Validator — v4

## Purpose

This document defines the Level 3 v4 direction of OMNIA-VALIDATION.

Level 3 v0 tested synthetic reference trajectories.

Level 3 v1 applied early-warning classification to Level 2-derived result snapshots.

Level 3 v2 evaluated the Level 2 temporal-collapse chain as an ordered stage trajectory.

Level 3 v3 measured warning risk directly over bounded raw ordered trajectory records.

Level 3 v4 moves from internal raw reference trajectories to external or independently generated raw trajectory records.

```text
measurement != inference != decision
```

---

## Core Transition

The Level 3 progression is:

```text
v0 -> synthetic reference trajectories
v1 -> Level 2-derived snapshots
v2 -> ordered Level 2 stage trajectory
v3 -> raw ordered reference trajectories
v4 -> external raw trajectory validation
```

The v4 transition is from:

```text
raw reference trajectory warning
```

to:

```text
external raw trajectory validation
```

This matters because v3 validated the warning mechanism on controlled reference trajectories.

v4 asks whether the same mechanism remains meaningful when the raw trajectories are not constructed only as internal reference cases.

---

## Core Question

Given external or independently generated raw ordered trajectories, can the Level 3 warning layer classify structural risk regimes using the same visible measurement logic?

Target regimes:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
```

Gate actions:

```text
STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP
```

The gate action is not a final decision.

It is a measurement-derived warning for an external decision layer.

---

## Definition of External Raw Trajectory

An external raw trajectory is an ordered sequence of structural events not created only as a synthetic internal reference case.

Examples may include:

```text
model-output perturbation traces
reasoning-step instability traces
token-level structural drift traces
multi-run answer trajectories
stress-test trajectories
observer-variant trajectories
threshold-sweep trajectories
representation-change trajectories
```

A v4 trajectory does not need to be produced by a live production system.

But it must be external to the v3 reference dataset.

---

## Required Raw Event Schema

Each event should preserve temporal or step order.

Minimal event schema:

```json
{
  "trajectory_id": "external_trajectory_001",
  "step": 1,
  "signature": "S0",
  "cluster": "C0",
  "delta": 0.0,
  "iri": 0.0,
  "boundary_distance": 1.0,
  "phase": "STABLE",
  "source": "external_or_independent_generator"
}
```

Required fields:

```text
trajectory_id
step
signature
cluster
delta
iri
boundary_distance
phase
source
```

Optional fields:

```text
timestamp
score_vector
omega
sei
residual_invariance
transition_label
observer_label
perturbation_label
model_name
prompt_id
run_id
variant_id
notes
```

---

## Field Meaning

### trajectory_id

Identifier for the external trajectory being analyzed.

### step

Ordered position of the event.

The validator must sort events by `step`.

### signature

Structural signature observed at that event.

Signature changes contribute to transition density.

### cluster

Cluster or regime label observed at that event.

Cluster changes contribute to transition density and drift.

### delta

Structural change or instability signal.

Higher values increase drift and collapse pressure.

### iri

Irreversibility signal.

Higher values indicate non-recoverable structural loss.

### boundary_distance

Distance from a known or estimated structural boundary.

Lower values mean higher boundary proximity.

The validator should convert it as:

```text
boundary_proximity = 1 - boundary_distance
```

after clamping to `[0, 1]`.

### phase

Observed or assigned structural phase.

Expected values may include:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
UNKNOWN
```

### source

Identifier for the source of the trajectory.

The source field is required in v4 because the core purpose is external or independently generated validation.

---

## Input Format

The preferred input format is JSONL.

Each line is one event.

Planned input path:

```text
data/temporal_collapse_external_raw_trajectories_v4.jsonl
```

Example:

```json
{"trajectory_id":"external_trajectory_001","step":1,"signature":"S0","cluster":"C0","delta":0.06,"iri":0.01,"boundary_distance":0.92,"phase":"STABLE","source":"independent_generator_v1"}
{"trajectory_id":"external_trajectory_001","step":2,"signature":"S0","cluster":"C0","delta":0.11,"iri":0.03,"boundary_distance":0.84,"phase":"STABLE","source":"independent_generator_v1"}
{"trajectory_id":"external_trajectory_001","step":3,"signature":"S1","cluster":"C1","delta":0.29,"iri":0.09,"boundary_distance":0.61,"phase":"DRIFT","source":"independent_generator_v1"}
{"trajectory_id":"external_trajectory_001","step":4,"signature":"S2","cluster":"C1","delta":0.41,"iri":0.16,"boundary_distance":0.47,"phase":"DRIFT","source":"independent_generator_v1"}
```

---

## Output Format

The v4 validator should emit one JSON result file.

Planned output path:

```text
results/temporal_collapse_external_raw_trajectory_validator_v4.json
```

Output should include:

```text
experiment
status
boundary
claim
input_file
trajectory_count
source_count
weights
thresholds
aggregate
source_summary
results
```

Each trajectory result should include:

```text
trajectory_id
source
event_count
risk_regime
risk_score
gate_action
dominant_axis
warning_flags
signals
transition_evidence
```

---

## v4 Warning Signals

The v4 validator should compute the same five visible signals used by v3:

```text
transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal
```

The purpose is to test whether the v3 mechanism remains meaningful outside the internal reference set.

Changing the formula too early would weaken the validation.

---

## Signal 1 — transition_density

Measures how often structural labels change across the ordered trajectory.

Inputs:

```text
signature
cluster
phase
```

Minimal formula:

```text
transition_density =
    average(
      normalized_change_count(signature),
      normalized_change_count(cluster),
      normalized_change_count(phase)
    )
```

Where:

```text
normalized_change_count(values) =
    number_of_changes / number_of_possible_transitions
```

---

## Signal 2 — drift_progression

Measures whether instability increases over the ordered trajectory.

Input:

```text
delta
```

Minimal formula:

```text
drift_progression =
    average(
      mean(delta),
      max(delta) - min(delta),
      max(0, late_mean(delta) - early_mean(delta))
    )
```

All values should be clamped to `[0, 1]`.

---

## Signal 3 — boundary_proximity

Measures how close the trajectory comes to a boundary.

Input:

```text
boundary_distance
```

Convert each event:

```text
event_boundary_proximity = 1 - boundary_distance
```

Minimal formula:

```text
boundary_proximity =
    average(
      max(event_boundary_proximity),
      late_mean(event_boundary_proximity)
    )
```

All values should be clamped to `[0, 1]`.

---

## Signal 4 — collapse_similarity

Measures whether the trajectory resembles collapse-like behavior.

Inputs:

```text
phase
delta
iri
boundary_proximity
signature
```

Collapse-like signs:

```text
phase contains COLLAPSE
high delta
high iri
high boundary proximity
broken signature markers
loss of continuity
```

Minimal formula:

```text
collapse_similarity =
    average(
      collapse_phase_ratio,
      max(delta),
      max(iri),
      boundary_proximity,
      broken_marker
    )
```

Where:

```text
collapse_phase_ratio =
    count(phase == COLLAPSE) / event_count
```

And:

```text
broken_marker = 1
```

if signature contains one of:

```text
BROKEN
FAIL
NULL
COLLAPSE
```

Otherwise:

```text
broken_marker = 0
```

---

## Signal 5 — irreversibility_signal

Measures structural loss or non-recoverable degradation.

Input:

```text
iri
```

Minimal formula:

```text
irreversibility_signal =
    average(
      max(iri),
      late_mean(iri)
    )
```

All values should be clamped to `[0, 1]`.

---

## Risk Formula v4

The v4 risk score should preserve the v3 raw trajectory formula:

```text
risk_score =
    0.20 * transition_density
  + 0.20 * drift_progression
  + 0.25 * boundary_proximity
  + 0.25 * collapse_similarity
  + 0.10 * irreversibility_signal
```

Weights:

```json
{
  "transition_density": 0.2,
  "drift_progression": 0.2,
  "boundary_proximity": 0.25,
  "collapse_similarity": 0.25,
  "irreversibility_signal": 0.1
}
```

The weights are experimental.

They are not universal.

They remain visible.

---

## Classification Thresholds

Initial thresholds:

```text
risk_score < 0.25         -> STABLE
0.25 <= risk_score < 0.50 -> DRIFT
0.50 <= risk_score < 0.75 -> CRITICAL
risk_score >= 0.75        -> COLLAPSE
```

Gate actions:

```text
STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP
```

Thresholds are experimental and must remain visible.

---

## Transition Evidence

The v4 validator should preserve evidence for each trajectory.

Each trajectory result should include:

```text
signature_changes
cluster_changes
phase_changes
delta_early_mean
delta_late_mean
iri_early_mean
iri_late_mean
min_boundary_distance
max_boundary_proximity
collapse_phase_count
source
```

This is required because v4 tests externality.

A source-free external validation is weak evidence.

---

## Source Summary

Because v4 involves external or independently generated trajectories, the result should include a source summary.

The source summary should include:

```text
source
trajectory_count
average_risk_score
regime_counts
highest_risk_trajectory
highest_risk_score
```

This allows the validator to expose whether one source produces systematically higher risk than another.

---

## Minimal Aggregate Result

The aggregate section should include:

```text
aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action
regime_counts
highest_risk_trajectory
highest_risk_score
source_count
```

The aggregate must not hide individual trajectory results.

---

## Reproducibility Requirements

A v4 experiment should include:

```text
input JSONL file
script
output JSON
visible weights
visible thresholds
per-trajectory evidence
source summary
aggregate result
negative cases
borderline cases
collapse-like cases
external or independently generated source labels
```

---

## Safe Claim

Safe v4 claim:

```text
OMNIA-VALIDATION Level 3 v4 defines external raw trajectory validation
for temporal-collapse warning measurement.

It applies the v3 raw trajectory warning mechanism to external or
independently generated ordered trajectory records using visible weights,
visible thresholds, source labels, and inspectable transition evidence.
```

---

## Claims to Avoid

Do not claim:

```text
OMNIA predicts AI collapse universally.
```

Do not claim:

```text
OMNIA detects semantic truth.
```

Do not claim:

```text
Level 3 v4 is production-certified.
```

Do not claim:

```text
The thresholds are universal.
```

Do not claim:

```text
External raw trajectory validation proves model cognition.
```

Do not claim:

```text
A source label alone makes the data independent.
```

Correct boundary:

```text
Level 3 v4 measures structural warning risk over external or independently
generated raw ordered trajectory records inside a bounded validation setup.
```

---

## Validation Rule

v4 should not weaken the boundary.

A valid v4 result must say exactly what the input data is.

If the trajectories are generated by an internal script, the result must say:

```text
internally generated external-style trajectories
```

If the trajectories are generated by another model, system, script, benchmark, or source, the result must name the source.

If independence cannot be verified, the result must state:

```text
source independence not verified
```

This is not a weakness.

It is boundary honesty.

---

## Planned Files

Concept document:

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_RAW_TRAJECTORY_VALIDATOR_V4.md
```

Input data:

```text
data/temporal_collapse_external_raw_trajectories_v4.jsonl
```

Script:

```text
examples/temporal_collapse_external_raw_trajectory_validator_v4.py
```

Result JSON:

```text
results/temporal_collapse_external_raw_trajectory_validator_v4.json
```

Result document:

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_RAW_TRAJECTORY_VALIDATOR_V4_RESULT.md
```

---

## Next Step

After this document, the next step is to create the external raw JSONL dataset:

```text
data/temporal_collapse_external_raw_trajectories_v4.jsonl
```

Then create and run the validator script:

```text
examples/temporal_collapse_external_raw_trajectory_validator_v4.py
```

The v4 test should include at least four trajectory types:

```text
external stable trajectory
external drift trajectory
external critical trajectory
external collapse-like trajectory
```

The result must preserve source labels.

The v4 objective is not to claim universal validity.

The v4 objective is to test whether the v3 raw trajectory warning mechanism remains coherent beyond the internal v3 reference dataset.