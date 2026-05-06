# Temporal Collapse Raw Trajectory Validator — v3

## Purpose

This document defines the Level 3 v3 direction of OMNIA-VALIDATION.

Level 3 v0 tested synthetic reference trajectories.

Level 3 v1 applied early-warning classification to Level 2-derived result snapshots.

Level 3 v2 evaluated the Level 2 temporal-collapse chain as an ordered stage trajectory.

Level 3 v3 moves to raw ordered trajectory records.

The objective is to stop deriving warning risk from summary files and instead measure warning conditions directly over ordered trajectory events.

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
v3 -> raw ordered trajectory records
```

The v3 transition is from:

```text
stage-summary trajectory warning
```

to:

```text
raw trajectory warning
```

This matters because raw trajectory records preserve event order, local transitions, drift accumulation, and boundary crossings more directly than summary JSON files.

---

## Core Question

Given a raw ordered trajectory, can OMNIA-VALIDATION measure whether the trajectory is entering a structural risk regime?

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

## Raw Trajectory Definition

A raw trajectory is an ordered sequence of structural events.

Each event should preserve temporal or step order.

Minimal event schema:

```json
{
  "trajectory_id": "trajectory_001",
  "step": 1,
  "signature": "S0",
  "cluster": "C0",
  "delta": 0.0,
  "iri": 0.0,
  "boundary_distance": 1.0,
  "phase": "STABLE"
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
```

Optional fields:

```text
source
timestamp
score_vector
omega
sei
residual_invariance
transition_label
observer_label
perturbation_label
notes
```

---

## Field Meaning

### trajectory_id

Identifier for the trajectory being analyzed.

### step

Ordered position of the event.

The v3 validator must sort events by `step`.

### signature

Structural signature observed at that step.

Signature changes contribute to transition density.

### cluster

Cluster or regime label observed at that step.

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

Observed or assigned phase label.

Expected values may include:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
UNKNOWN
```

Phase changes contribute to transition density and regime instability.

---

## Input Format

The preferred input format is JSONL.

Each line is one event.

Example:

```json
{"trajectory_id":"trajectory_001","step":1,"signature":"S0","cluster":"C0","delta":0.05,"iri":0.01,"boundary_distance":0.95,"phase":"STABLE"}
{"trajectory_id":"trajectory_001","step":2,"signature":"S0","cluster":"C0","delta":0.07,"iri":0.02,"boundary_distance":0.90,"phase":"STABLE"}
{"trajectory_id":"trajectory_001","step":3,"signature":"S1","cluster":"C1","delta":0.22,"iri":0.07,"boundary_distance":0.68,"phase":"DRIFT"}
{"trajectory_id":"trajectory_001","step":4,"signature":"S2","cluster":"C1","delta":0.46,"iri":0.18,"boundary_distance":0.42,"phase":"DRIFT"}
```

Planned input path:

```text
data/temporal_collapse_raw_trajectories_v3.jsonl
```

---

## Output Format

The v3 validator should emit one JSON result file.

Planned output path:

```text
results/temporal_collapse_raw_trajectory_validator_v3.json
```

Output should include:

```text
experiment
status
boundary
claim
input_file
trajectory_count
weights
thresholds
aggregate
results
```

Each trajectory result should include:

```text
trajectory_id
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

## v3 Warning Signals

The v3 validator should compute five visible signals.

```text
transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal
```

No hidden interpretation layer should be used.

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

Inputs:

```text
delta
```

Minimal formula:

```text
drift_progression =
    average(
      mean(delta),
      max(delta) - min(delta),
      late_mean(delta) - early_mean(delta)
    )
```

All values should be clamped to `[0, 1]`.

If `late_mean(delta) - early_mean(delta)` is negative, use `0`.

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
```

Collapse-like signs:

```text
phase contains COLLAPSE
high delta
high iri
high boundary proximity
loss of continuity
```

Minimal formula:

```text
collapse_similarity =
    average(
      collapse_phase_ratio,
      max(delta),
      max(iri),
      boundary_proximity
    )
```

Where:

```text
collapse_phase_ratio =
    count(phase == COLLAPSE) / event_count
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

## Risk Formula v3

The v3 risk score should use visible weights:

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

The v3 validator should preserve evidence.

Each trajectory result should include compact transition evidence:

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
```

This makes the warning result inspectable.

A warning without evidence is weak evidence.

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
```

This allows a batch of raw trajectories to be summarized without hiding individual results.

---

## Reproducibility Requirements

A v3 experiment should include:

```text
input JSONL file
script
output JSON
visible weights
visible thresholds
per-trajectory evidence
aggregate result
negative cases
borderline cases
collapse-like cases
```

---

## Safe Claim

Safe v3 claim:

```text
OMNIA-VALIDATION Level 3 v3 defines a raw ordered trajectory validator
for temporal-collapse warning measurement.

It measures structural warning signals directly over ordered trajectory events,
using visible weights, visible thresholds, and inspectable transition evidence.
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
Level 3 v3 is production-certified.
```

Do not claim:

```text
The thresholds are universal.
```

Do not claim:

```text
Raw trajectory warning proves model cognition.
```

Correct boundary:

```text
Level 3 v3 measures structural warning risk over raw ordered trajectory records
inside a bounded validation setup.
```

---

## Planned Files

Concept document:

```text
docs/TEMPORAL_COLLAPSE_RAW_TRAJECTORY_VALIDATOR_V3.md
```

Input data:

```text
data/temporal_collapse_raw_trajectories_v3.jsonl
```

Script:

```text
examples/temporal_collapse_raw_trajectory_validator_v3.py
```

Result JSON:

```text
results/temporal_collapse_raw_trajectory_validator_v3.json
```

Result document:

```text
docs/TEMPORAL_COLLAPSE_RAW_TRAJECTORY_VALIDATOR_V3_RESULT.md
```

---

## Next Step

After this document, the next step is to create the raw JSONL dataset:

```text
data/temporal_collapse_raw_trajectories_v3.jsonl
```

Then create and run the validator script:

```text
examples/temporal_collapse_raw_trajectory_validator_v3.py
```

The v3 test should include at least four trajectory types:

```text
stable raw trajectory
drift raw trajectory
critical raw trajectory
collapse-like raw trajectory
```

This keeps the test bounded, inspectable, and falsifiable.