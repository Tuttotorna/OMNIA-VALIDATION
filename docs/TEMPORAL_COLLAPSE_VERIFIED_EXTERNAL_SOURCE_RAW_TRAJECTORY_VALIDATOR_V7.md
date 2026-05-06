# Temporal Collapse Verified External-Source Raw Trajectory Validator — v7

## Purpose

This document defines the Level 3 v7 direction of OMNIA-VALIDATION.

Level 3 v6 validated the raw trajectory warning mechanism over declared external-source raw ordered trajectory records.

The v6 source boundary was:

```text
source_independence: external_source_declared
independence_method: prompt_perturbation_trace
```

v6 was stronger than v5, but it was not externally verified.

Level 3 v7 moves from:

```text
external_source_declared
```

to:

```text
external_source_verified
```

```text
measurement != inference != decision
```

---

## Core Boundary

v7 must not be fake.

A v7 result is valid only if the input records are derived from a source that can be independently documented.

Valid v7 source classes include:

```text
public benchmark-derived trace
external model output trace
multi-run prompt perturbation output from another system
public dataset transformed into raw trajectory records
real perturbation log
externally generated reasoning trace
```

Invalid v7 source classes include:

```text
handwritten internal reference trajectories
external-style synthetic records
internal generator-only records
declared external-source records with no external source evidence
```

---

## Core Transition

The Level 3 progression is:

```text
v0 -> synthetic reference trajectories
v1 -> Level 2-derived snapshots
v2 -> ordered Level 2 stage trajectory
v3 -> raw ordered reference trajectories
v4 -> external-style raw trajectory validation
v5 -> separate-generator raw trajectory validation
v6 -> declared external-source raw trajectory validation
v7 -> verified external-source raw trajectory validation
```

The v7 transition is from:

```text
declared external-source validation
```

to:

```text
verified external-source validation
```

---

## Core Question

Given raw ordered trajectory records derived from a documented external source, can the Level 3 warning layer classify structural risk regimes using the same visible measurement logic used in v3, v4, v5, and v6?

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

## Required Source Independence

For v7, the required source independence value is:

```text
external_source_verified
```

This value must not be used unless the source is externally documented.

Acceptable evidence may include:

```text
public benchmark name
public dataset name
external model output batch
external trace source
external file origin
external generation method
external-source URL or citation
reproducible transformation notes
```

If this evidence is absent, the correct label is not:

```text
external_source_verified
```

The correct label remains:

```text
external_source_declared
```

---

## Source Independence Levels

v7 recognizes the same independence levels as v6, but only one qualifies as v7-complete:

```text
not_verified
generated_by_independent_script
external_source_declared
external_source_verified
```

Meaning:

```text
not_verified
```

The source is named, but independence is not verified.

```text
generated_by_independent_script
```

The source was produced by a separate internal generator script.

```text
external_source_declared
```

The source is declared as external to the internal generator chain, but not independently documented.

```text
external_source_verified
```

The source is externally produced or publicly documented strongly enough to support verified external-source status.

Only this final level is valid for v7.

---

## Recommended v7 Boundary

The first practical v7 boundary should be:

```text
source_independence: external_source_verified
independence_method: public_benchmark_mapping
```

or:

```text
source_independence: external_source_verified
independence_method: external_model_output_mapping
```

The exact method depends on the chosen source.

Correct v7 wording:

```text
verified external-source raw trajectory validation
```

Incorrect v7 wording:

```text
universal collapse prediction
```

---

## External Raw Trajectory Definition

A v7 raw trajectory is an ordered sequence of structural events derived from a verified external source.

Each event must preserve step order.

Minimal event schema:

```json
{
  "trajectory_id": "verified_external_source_trajectory_001",
  "step": 1,
  "signature": "S0",
  "cluster": "C0",
  "delta": 0.0,
  "iri": 0.0,
  "boundary_distance": 1.0,
  "phase": "STABLE",
  "source": "verified_external_source_name",
  "source_independence": "external_source_verified",
  "independence_method": "public_benchmark_mapping",
  "external_source_reference": "documented external source",
  "mapping_notes": "how the source was transformed into trajectory events"
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
source_independence
independence_method
external_source_reference
mapping_notes
```

Optional fields:

```text
timestamp
model_name
benchmark_name
dataset_name
prompt_id
run_id
variant_id
question_id
response_id
score_vector
omega
sei
residual_invariance
transition_label
observer_label
perturbation_label
source_url
source_citation
notes
```

---

## Field Meaning

### trajectory_id

Identifier for the verified external-source trajectory.

### step

Ordered position of the event.

The validator must sort events by `step`.

### signature

Structural signature observed at that event.

Signature changes contribute to transition density.

### cluster

Cluster or regime label observed at that event.

Cluster changes contribute to transition density.

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

Expected values:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
UNKNOWN
```

### source

Verified external source label.

Examples:

```text
public_benchmark_trace_v7
external_model_batch_v7
documented_prompt_perturbation_trace_v7
```

### source_independence

For v7-complete validation, this must be:

```text
external_source_verified
```

### independence_method

How the verified external-source boundary was obtained.

Examples:

```text
public_benchmark_mapping
external_model_output_mapping
public_dataset_mapping
documented_trace_mapping
```

### external_source_reference

Human-readable reference to the source origin.

Examples:

```text
public benchmark dataset
external model output batch
documented perturbation trace
public dataset transformed into trajectory records
```

### mapping_notes

Short explanation of how the external data was transformed into raw trajectory events.

---

## Input Format

The preferred input format is JSONL.

Each line is one event.

Planned input path:

```text
data/temporal_collapse_verified_external_source_raw_trajectories_v7.jsonl
```

Example:

```json
{"trajectory_id":"verified_external_source_stable_001","step":1,"signature":"VS0","cluster":"VC0","delta":0.04,"iri":0.01,"boundary_distance":0.94,"phase":"STABLE","source":"public_benchmark_trace_v7","source_independence":"external_source_verified","independence_method":"public_benchmark_mapping","external_source_reference":"public benchmark-derived trace","mapping_notes":"mapped perturbation progression into ordered structural events"}
```

---

## Output Format

The v7 validator should emit one JSON result file.

Planned output path:

```text
results/temporal_collapse_verified_external_source_raw_trajectory_validator_v7.json
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
source_independence_values
independence_method_values
external_source_references
external_source_note
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
source_independence
independence_method
external_source_reference
mapping_notes
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

## v7 Warning Signals

The v7 validator must preserve the same five visible signals used by v3, v4, v5, and v6:

```text
transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal
```

Changing the formula at v7 would weaken comparability.

---

## Signal 1 — transition_density

Measures how often structural labels change across the ordered trajectory.

Inputs:

```text
signature
cluster
phase
```

Formula:

```text
transition_density =
    average(
      normalized_change_count(signature),
      normalized_change_count(cluster),
      normalized_change_count(phase)
    )
```

---

## Signal 2 — drift_progression

Measures whether instability increases over the ordered trajectory.

Input:

```text
delta
```

Formula:

```text
drift_progression =
    average(
      mean(delta),
      max(delta) - min(delta),
      max(0, late_mean(delta) - early_mean(delta))
    )
```

All values are clamped to `[0, 1]`.

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

Formula:

```text
boundary_proximity =
    average(
      max(event_boundary_proximity),
      late_mean(event_boundary_proximity)
    )
```

All values are clamped to `[0, 1]`.

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

Formula:

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

Formula:

```text
irreversibility_signal =
    average(
      max(iri),
      late_mean(iri)
    )
```

All values are clamped to `[0, 1]`.

---

## Risk Formula v7

The v7 risk score should preserve the v3/v4/v5/v6 raw trajectory formula:

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

The v7 validator should preserve evidence for each trajectory.

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
source_independence
independence_method
external_source_reference
mapping_notes
```

This is required because v7 tests verified source-boundary strength.

A source-free v7 result is invalid.

---

## Source Summary

Because v7 involves verified external-source trajectories, the result must include a source summary.

The source summary should include:

```text
source
source_independence
independence_method
external_source_reference
trajectory_count
average_risk_score
regime_counts
highest_risk_trajectory
highest_risk_score
```

This exposes whether one external source produces systematically higher or lower warning pressure.

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
independence_method_count
external_source_reference_count
```

The aggregate must not hide individual trajectory results.

---

## Reproducibility Requirements

A v7 experiment should include:

```text
input JSONL file
validator script
output JSON
visible weights
visible thresholds
per-trajectory evidence
source summary
aggregate result
negative cases
borderline cases
critical cases
collapse-like cases
verified source labels
source independence status
independence method
external source reference
mapping notes
```

---

## Minimum Valid v7 Construction

A minimum valid v7 construction should include:

```text
source: public_benchmark_trace_v7
source_independence: external_source_verified
independence_method: public_benchmark_mapping
external_source_reference: documented public benchmark-derived trace
```

or equivalent.

It must include at least five trajectory types:

```text
verified external-source stable trajectory
verified external-source drift trajectory
verified external-source borderline critical trajectory
verified external-source critical trajectory
verified external-source collapse-like trajectory
```

---

## Safe Claim

Safe v7 claim:

```text
OMNIA-VALIDATION Level 3 v7 applies the raw trajectory warning mechanism
to verified external-source raw ordered trajectory records.

The validator measures structural warning risk using visible weights,
visible thresholds, source labels, independence method labels, external-source
references, and inspectable transition evidence.
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
Level 3 v7 is production-certified.
```

Do not claim:

```text
The thresholds are universal.
```

Do not claim:

```text
External-source validation proves model cognition.
```

Do not claim:

```text
A hand-written dataset is external_source_verified.
```

Correct boundary:

```text
Level 3 v7 measures structural warning risk over verified external-source
raw ordered trajectory records inside a bounded validation setup.
```

---

## Validation Rule

v7 must not weaken the boundary.

A valid v7 result must name the external source.

If the trajectories are derived from a public benchmark, the result must name the benchmark or dataset class.

If the trajectories are derived from model outputs, the result must state the output-generation method.

If the trajectories are derived from a public dataset, the result must state the dataset class and mapping method.

If source independence cannot be externally documented, the result must not use:

```text
external_source_verified
```

Boundary honesty is part of the result.

---

## Planned Files

Concept document:

```text
docs/TEMPORAL_COLLAPSE_VERIFIED_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V7.md
```

Input data:

```text
data/temporal_collapse_verified_external_source_raw_trajectories_v7.jsonl
```

Script:

```text
examples/temporal_collapse_verified_external_source_raw_trajectory_validator_v7.py
```

Result JSON:

```text
results/temporal_collapse_verified_external_source_raw_trajectory_validator_v7.json
```

Result document:

```text
docs/TEMPORAL_COLLAPSE_VERIFIED_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V7_RESULT.md
```

---

## Next Step

After this document, the next step is to choose the actual verified external source.

Without a genuine documented external source, v7 should not proceed.

The correct next action is:

```text
select external source
```

Then create:

```text
data/temporal_collapse_verified_external_source_raw_trajectories_v7.jsonl
```

Only after that should the validator be run.

The v7 objective is not to claim universal validity.

The v7 objective is to test whether the raw trajectory warning mechanism remains coherent under a verified external-source boundary.