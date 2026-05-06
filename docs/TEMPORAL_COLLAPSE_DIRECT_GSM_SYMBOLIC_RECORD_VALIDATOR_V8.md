# Temporal Collapse Direct GSM-Symbolic Record Validator — v8

## Purpose

This document defines the Level 3 v8 direction of OMNIA-VALIDATION.

Level 3 v7 used GSM-Symbolic as a public/documentable benchmark boundary and mapped GSM-Symbolic-derived structural trajectory records into the Level 3 raw warning mechanism.

Level 3 v8 moves one step further.

The objective is to move from:

```text
verified external-source mapped trajectory records
```

to:

```text
direct public benchmark record mapping
```

```text
measurement != inference != decision
```

---

## Core Boundary

v8 must not pretend to be stronger than it is.

A v8 result is valid only if the input records are derived directly from actual GSM-Symbolic files, template variants, model outputs, answer traces, or benchmark records.

Valid v8 source classes include:

```text
actual GSM-Symbolic generated records
official GSM-Symbolic template variants
model outputs over GSM-Symbolic variants
answer correctness traces over symbolic perturbations
public benchmark records transformed into raw trajectory records
```

Invalid v8 source classes include:

```text
handwritten GSM-style trajectories
synthetic GSM-like records with no direct source file
mapped benchmark-inspired examples
internal generator-only records
external-source labels without direct record origin
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
v8 -> direct public benchmark record mapping
```

The v8 transition is from:

```text
GSM-Symbolic-derived mapped trajectory records
```

to:

```text
records derived directly from GSM-Symbolic data or outputs
```

---

## Core Question

Given direct GSM-Symbolic records, can the Level 3 warning layer classify structural risk regimes using the same visible measurement logic used in v3 through v7?

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

## What v8 Does Not Claim

v8 does not claim that OMNIA solves GSM-Symbolic.

v8 does not claim model answer correctness.

v8 does not replace benchmark evaluation.

v8 does not infer semantic truth.

v8 does not make final decisions.

Correct claim:

```text
v8 maps direct GSM-Symbolic benchmark records or answer traces
into raw structural trajectory events and measures warning risk.
```

Incorrect claim:

```text
v8 proves OMNIA solves GSM-Symbolic.
```

---

## Required Source Independence

For v8, the required source independence value remains:

```text
external_source_verified
```

But v8 adds a stronger mapping requirement:

```text
direct_public_benchmark_record_mapping
```

Recommended boundary:

```text
source_independence: external_source_verified
independence_method: direct_public_benchmark_record_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

This is stronger than v7 because v8 should reference actual records, not only mapped GSM-Symbolic-derived structural trajectories.

---

## Required Record Origin

Each v8 trajectory must identify where the record came from.

Required origin fields:

```text
benchmark_name
source_record_type
source_record_reference
mapping_method
```

Allowed `source_record_type` values:

```text
template_variant
generated_question
model_output
answer_trace
correctness_trace
perturbation_trace
```

Allowed `mapping_method` values:

```text
template_variant_to_trajectory
question_variant_to_trajectory
model_output_to_trajectory
answer_trace_to_trajectory
correctness_trace_to_trajectory
perturbation_trace_to_trajectory
```

---

## Direct GSM-Symbolic Raw Trajectory Definition

A v8 raw trajectory is an ordered sequence of structural events derived directly from GSM-Symbolic benchmark records or traces.

Minimal event schema:

```json
{
  "trajectory_id": "gsm_symbolic_direct_template_001",
  "step": 1,
  "template_id": "template_001",
  "question_id": "question_001",
  "variant_type": "base",
  "signature": "GSM_BASE_OK",
  "cluster": "GSM_C0",
  "delta": 0.0,
  "iri": 0.0,
  "boundary_distance": 1.0,
  "phase": "STABLE",
  "source": "gsm_symbolic_public_benchmark_v8",
  "source_independence": "external_source_verified",
  "independence_method": "direct_public_benchmark_record_mapping",
  "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
  "benchmark_name": "GSM-Symbolic",
  "source_record_type": "template_variant",
  "source_record_reference": "template/question/variant identifier",
  "mapping_method": "template_variant_to_trajectory",
  "mapping_notes": "direct GSM-Symbolic record mapped into ordered structural trajectory event"
}
```

Required fields:

```text
trajectory_id
step
template_id
question_id
variant_type
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
benchmark_name
source_record_type
source_record_reference
mapping_method
mapping_notes
```

Optional fields:

```text
model_name
run_id
response_id
expected_answer
model_final_answer
is_correct
score_vector
omega
sei
residual_invariance
transition_label
perturbation_label
raw_question_hash
raw_output_hash
notes
```

---

## Field Meaning

### trajectory_id

Identifier for the direct GSM-Symbolic trajectory.

A trajectory may correspond to:

```text
one template across variants
one question across perturbations
one model answer sequence across variants
one correctness trace across symbolic changes
```

### step

Ordered position of the event inside the trajectory.

The validator must sort events by `step`.

### template_id

Identifier of the GSM-Symbolic template or template-like source unit.

### question_id

Identifier of the generated question or benchmark record.

### variant_type

The perturbation or variant type.

Examples:

```text
base
num_perturbed
clause_augmented
symbolic_variant
irrelevant_clause
difficulty_variant
```

### signature

Structural signature assigned to the event.

Signature changes contribute to transition density.

### cluster

Cluster or regime label assigned to the event.

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

Source label for this v8 experiment.

Recommended:

```text
gsm_symbolic_public_benchmark_v8
```

### source_independence

For v8, this should be:

```text
external_source_verified
```

### independence_method

For v8, this should be:

```text
direct_public_benchmark_record_mapping
```

### external_source_reference

Human-readable source reference.

Recommended:

```text
GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

### benchmark_name

Benchmark name.

Recommended:

```text
GSM-Symbolic
```

### source_record_type

Type of direct record used.

Examples:

```text
template_variant
generated_question
model_output
answer_trace
correctness_trace
perturbation_trace
```

### source_record_reference

Specific source record reference.

Examples:

```text
template_001/base
template_001/num_perturbed
template_001/clause_augmented
question_001/model_output/run_001
```

### mapping_method

How the direct source record was transformed into a structural trajectory event.

Examples:

```text
template_variant_to_trajectory
question_variant_to_trajectory
model_output_to_trajectory
answer_trace_to_trajectory
correctness_trace_to_trajectory
perturbation_trace_to_trajectory
```

### mapping_notes

Short explanation of the transformation.

---

## Input Format

The preferred input format is JSONL.

Each line is one direct GSM-Symbolic-derived event.

Planned input path:

```text
data/temporal_collapse_direct_gsm_symbolic_records_v8.jsonl
```

Example:

```json
{"trajectory_id":"gsm_symbolic_direct_template_001","step":1,"template_id":"template_001","question_id":"question_001","variant_type":"base","signature":"GSM_BASE_OK","cluster":"GSM_C0","delta":0.04,"iri":0.01,"boundary_distance":0.94,"phase":"STABLE","source":"gsm_symbolic_public_benchmark_v8","source_independence":"external_source_verified","independence_method":"direct_public_benchmark_record_mapping","external_source_reference":"GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository","benchmark_name":"GSM-Symbolic","source_record_type":"template_variant","source_record_reference":"template_001/base","mapping_method":"template_variant_to_trajectory","mapping_notes":"direct GSM-Symbolic base variant mapped into structural trajectory event"}
```

---

## Output Format

The v8 validator should emit one JSON result file.

Planned output path:

```text
results/temporal_collapse_direct_gsm_symbolic_record_validator_v8.json
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
benchmark_names
source_record_types
mapping_methods
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
benchmark_name
source_record_type
source_record_reference
mapping_method
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

## v8 Warning Signals

The v8 validator must preserve the same five visible signals used by v3, v4, v5, v6, and v7:

```text
transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal
```

Changing the formula at v8 would weaken comparability.

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

## Risk Formula v8

The v8 risk score should preserve the v3/v4/v5/v6/v7 raw trajectory formula:

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

The v8 validator should preserve evidence for each trajectory.

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
benchmark_name
source_record_type
source_record_reference
mapping_method
mapping_notes
```

This is required because v8 tests direct public benchmark mapping.

A record-free v8 result is invalid.

---

## Source Summary

Because v8 involves direct public benchmark records, the result must include a source summary.

The source summary should include:

```text
source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
mapping_method
trajectory_count
average_risk_score
regime_counts
highest_risk_trajectory
highest_risk_score
```

This exposes whether one source or record class produces systematically higher or lower warning pressure.

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
benchmark_count
source_record_type_count
mapping_method_count
```

The aggregate must not hide individual trajectory results.

---

## Reproducibility Requirements

A v8 experiment should include:

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
benchmark name
source record type
source record reference
mapping method
mapping notes
```

---

## Minimum Valid v8 Construction

A minimum valid v8 construction should include records such as:

```text
source: gsm_symbolic_public_benchmark_v8
source_independence: external_source_verified
independence_method: direct_public_benchmark_record_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: template_variant
mapping_method: template_variant_to_trajectory
```

It should include at least five trajectory types:

```text
direct GSM-Symbolic stable trajectory
direct GSM-Symbolic drift trajectory
direct GSM-Symbolic borderline critical trajectory
direct GSM-Symbolic critical trajectory
direct GSM-Symbolic collapse-like trajectory
```

---

## Safe Claim

Safe v8 claim:

```text
OMNIA-VALIDATION Level 3 v8 applies the raw trajectory warning mechanism
to direct GSM-Symbolic public benchmark records mapped into raw ordered
structural trajectory events.

The validator measures structural warning risk using visible weights,
visible thresholds, source labels, benchmark references, source-record fields,
mapping methods, and inspectable transition evidence.
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
Level 3 v8 is production-certified.
```

Do not claim:

```text
The thresholds are universal.
```

Do not claim:

```text
OMNIA solves GSM-Symbolic.
```

Do not claim:

```text
Structural warning risk equals benchmark correctness.
```

Correct boundary:

```text
Level 3 v8 measures structural warning risk over direct GSM-Symbolic
benchmark records mapped into raw ordered trajectory events.
```

---

## Validation Rule

v8 must not weaken the boundary.

A valid v8 result must name the source record class.

If the input comes from template variants, the result must state:

```text
template_variant
```

If the input comes from generated questions, the result must state:

```text
generated_question
```

If the input comes from model answers, the result must state:

```text
model_output
```

If the input comes from correctness traces, the result must state:

```text
correctness_trace
```

If direct source records cannot be identified, the result should remain v7, not v8.

Boundary honesty is part of the result.

---

## Planned Files

Concept document:

```text
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_RECORD_VALIDATOR_V8.md
```

Input data:

```text
data/temporal_collapse_direct_gsm_symbolic_records_v8.jsonl
```

Script:

```text
examples/temporal_collapse_direct_gsm_symbolic_record_validator_v8.py
```

Result JSON:

```text
results/temporal_collapse_direct_gsm_symbolic_record_validator_v8.json
```

Result document:

```text
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_RECORD_VALIDATOR_V8_RESULT.md
```

---

## Next Step

After this document, the next step is to create the direct GSM-Symbolic record JSONL file:

```text
data/temporal_collapse_direct_gsm_symbolic_records_v8.jsonl
```

The v8 dataset must include direct record fields:

```text
template_id
question_id
variant_type
benchmark_name
source_record_type
source_record_reference
mapping_method
```

Only after that should the validator be run.

The v8 objective is not to claim benchmark solving.

The v8 objective is to test whether the raw trajectory warning mechanism remains coherent when GSM-Symbolic public benchmark records are mapped directly into ordered structural events.