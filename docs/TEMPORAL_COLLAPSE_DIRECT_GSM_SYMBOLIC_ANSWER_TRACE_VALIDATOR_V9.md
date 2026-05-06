# Temporal Collapse Direct GSM-Symbolic Answer Trace Validator — v9

## Purpose

This document defines the Level 3 v9 direction of OMNIA-VALIDATION.

Level 3 v8 mapped direct GSM-Symbolic public benchmark record fields into raw ordered structural trajectory events.

Level 3 v9 moves one step further.

The objective is to move from:

```text
direct public benchmark record mapping
```

to:

```text
direct answer-trace / model-output mapping
```

```text
measurement != inference != decision
```

---

## Core Boundary

v9 must not claim that OMNIA solves GSM-Symbolic.

v9 must not claim semantic correctness.

v9 must not claim benchmark superiority.

v9 must not replace official benchmark evaluation.

v9 measures structural warning risk over ordered answer traces or model-output traces.

Correct boundary:

```text
Level 3 v9 maps GSM-Symbolic answer traces or model-output traces
into raw ordered structural trajectory events and measures warning risk.
```

Incorrect boundary:

```text
Level 3 v9 proves that OMNIA solves GSM-Symbolic.
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
v9 -> direct answer-trace / model-output mapping
```

The v9 transition is from:

```text
template_variant_to_trajectory
```

to:

```text
answer_trace_to_trajectory
model_output_to_trajectory
correctness_trace_to_trajectory
```

---

## Core Question

Given GSM-Symbolic answer traces or model-output traces, can the Level 3 warning layer classify structural risk regimes using the same visible measurement logic used in v3 through v8?

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

## What v9 Does Not Claim

v9 does not claim:

```text
GSM-Symbolic solving
semantic truth detection
benchmark correctness replacement
model cognition detection
universal collapse prediction
production certification
final decision authority
```

Correct claim:

```text
v9 measures structural warning risk over GSM-Symbolic answer traces
or model-output traces mapped into raw ordered trajectory events.
```

Incorrect claim:

```text
v9 proves that OMNIA understands or solves GSM-Symbolic.
```

---

## Required Source Boundary

For v9, the required source independence value remains:

```text
external_source_verified
```

Recommended boundary:

```text
source: gsm_symbolic_answer_trace_v9
source_independence: external_source_verified
independence_method: direct_answer_trace_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: answer_trace
mapping_method: answer_trace_to_trajectory
```

Alternative valid source record types:

```text
model_output
correctness_trace
answer_trace
```

Alternative valid mapping methods:

```text
model_output_to_trajectory
answer_trace_to_trajectory
correctness_trace_to_trajectory
```

---

## Required Record Fields

Each v9 event must preserve benchmark identity, model-output identity, answer identity, and structural trajectory identity.

Required fields:

```text
trajectory_id
step
template_id
question_id
variant_type
model_name
run_id
response_id
expected_answer
model_final_answer
is_correct
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
raw_question_hash
raw_output_hash
model_raw_output
answer_extraction_method
score_vector
omega
sei
residual_invariance
transition_label
perturbation_label
failure_label
notes
```

---

## Direct Answer-Trace Event Schema

Minimal event example:

```json
{
  "trajectory_id": "gsm_symbolic_answer_trace_template_001_model_a",
  "step": 1,
  "template_id": "gsm_symbolic_template_001",
  "question_id": "gsm_symbolic_template_001_base",
  "variant_type": "base",
  "model_name": "model_a",
  "run_id": "run_001",
  "response_id": "response_001",
  "expected_answer": "42",
  "model_final_answer": "42",
  "is_correct": true,
  "signature": "ANSWER_OK_STABLE",
  "cluster": "ANS_C0",
  "delta": 0.04,
  "iri": 0.01,
  "boundary_distance": 0.94,
  "phase": "STABLE",
  "source": "gsm_symbolic_answer_trace_v9",
  "source_independence": "external_source_verified",
  "independence_method": "direct_answer_trace_mapping",
  "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
  "benchmark_name": "GSM-Symbolic",
  "source_record_type": "answer_trace",
  "source_record_reference": "gsm_symbolic_template_001/base/model_a/run_001",
  "mapping_method": "answer_trace_to_trajectory",
  "mapping_notes": "direct answer trace mapped into ordered structural trajectory event"
}
```

---

## Event Meaning

### trajectory_id

Identifier for one answer trace trajectory.

A trajectory may correspond to:

```text
one template across variants for one model
one generated question across perturbations for one model
one model-output trace across variant types
one correctness trace across symbolic changes
```

### step

Ordered position of the event inside the trajectory.

The validator must sort by `step`.

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

### model_name

Name or label of the model that produced the answer.

### run_id

Identifier of the run.

### response_id

Identifier of the model response.

### expected_answer

Benchmark expected answer.

This is included for traceability.

### model_final_answer

Extracted final model answer.

This is included for traceability.

### is_correct

Boolean correctness flag.

Important: `is_correct` is evidence, not the final measurement.

The validator may use correctness transitions as structural input, but the output remains a structural warning measurement.

### signature

Structural signature assigned to the event.

Examples:

```text
ANSWER_OK_STABLE
ANSWER_OK_VAR
ANSWER_FAIL_DRIFT
ANSWER_FAIL_CRITICAL
ANSWER_BROKEN
```

### cluster

Cluster or regime label assigned to the event.

Examples:

```text
ANS_C0
ANS_C1
ANS_C2
ANS_C9
```

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

---

## Input Format

Preferred input format:

```text
JSONL
```

Planned input file:

```text
data/temporal_collapse_direct_gsm_symbolic_answer_traces_v9.jsonl
```

Each line must contain one direct answer-trace event.

---

## Output Format

Planned output file:

```text
results/temporal_collapse_direct_gsm_symbolic_answer_trace_validator_v9.json
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
model_names
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
model_name
run_id
template_id
question_id
variant_type
correctness_profile
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

## v9 Warning Signals

v9 preserves the same five visible signals used by v3 through v8:

```text
transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal
```

Changing the formula at v9 would weaken comparability.

---

## Signal 1 — transition_density

Measures how often structural labels change across the ordered answer trace.

Inputs:

```text
signature
cluster
phase
is_correct
```

Base formula:

```text
transition_density =
    average(
      normalized_change_count(signature),
      normalized_change_count(cluster),
      normalized_change_count(phase)
    )
```

Optional v9 extension:

```text
correctness_change_rate =
    normalized_change_count(is_correct)
```

If included, it must be explicitly reported.

The default v9 validator should keep the raw v3-v8 formula unchanged and report correctness changes as transition evidence.

---

## Signal 2 — drift_progression

Measures whether instability increases over the ordered answer trace.

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

Measures how close the answer trace comes to a structural boundary.

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

Measures whether the answer trace resembles collapse-like behavior.

Inputs:

```text
phase
delta
iri
boundary_proximity
signature
is_correct
```

Base formula:

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

Correctness failure can be reported as evidence.

It should not silently replace the structural signal.

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

## Risk Formula v9

The v9 risk score should preserve the v3/v4/v5/v6/v7/v8 raw trajectory formula:

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

Each v9 trajectory result should include:

```text
signature_changes
cluster_changes
phase_changes
correctness_changes
correct_count
incorrect_count
accuracy_rate
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
model_name
run_id
template_id
question_id
variant_type
```

This is required because v9 tests answer-trace or model-output mappings.

A record-free v9 result is invalid.

---

## Correctness Profile

v9 should include a correctness profile for each trajectory:

```json
{
  "event_count": 5,
  "correct_count": 3,
  "incorrect_count": 2,
  "accuracy_rate": 0.6,
  "correctness_changes": 2,
  "starts_correct": true,
  "ends_correct": false
}
```

Important boundary:

```text
correctness_profile is evidence.

risk_score is still a structural warning score.
```

Correctness and structural risk may correlate, but they are not the same measurement.

---

## Source Summary

Because v9 involves model-output or answer-trace records, the result must include a source summary.

The source summary should include:

```text
source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
mapping_method
model_name
trajectory_count
average_risk_score
average_accuracy_rate
regime_counts
highest_risk_trajectory
highest_risk_score
```

This exposes whether one model, source, or record class produces systematically higher or lower warning pressure.

---

## Minimal Aggregate Result

The aggregate section should include:

```text
aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action
aggregate_accuracy_rate
regime_counts
highest_risk_trajectory
highest_risk_score
source_count
independence_method_count
external_source_reference_count
benchmark_count
source_record_type_count
mapping_method_count
model_count
```

The aggregate must not hide individual trajectory results.

---

## Reproducibility Requirements

A v9 experiment should include:

```text
input JSONL file
validator script
output JSON
visible weights
visible thresholds
per-trajectory evidence
correctness profiles
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
model name
run id
response id
expected answer
model final answer
is_correct
```

---

## Minimum Valid v9 Construction

A minimum valid v9 construction should include:

```text
source: gsm_symbolic_answer_trace_v9
source_independence: external_source_verified
independence_method: direct_answer_trace_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: answer_trace
mapping_method: answer_trace_to_trajectory
```

It should include at least five trajectory types:

```text
direct answer-trace stable trajectory
direct answer-trace drift trajectory
direct answer-trace borderline critical trajectory
direct answer-trace critical trajectory
direct answer-trace collapse-like trajectory
```

---

## Safe Claim

Safe v9 claim:

```text
OMNIA-VALIDATION Level 3 v9 applies the raw trajectory warning mechanism
to GSM-Symbolic answer traces or model-output traces mapped into raw ordered
structural trajectory events.

The validator measures structural warning risk using visible weights,
visible thresholds, source labels, benchmark references, model-output fields,
answer-correctness fields, mapping methods, correctness profiles, and
inspectable transition evidence.
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
Level 3 v9 is production-certified.
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

Do not claim:

```text
Correct answer means structural stability.
```

Do not claim:

```text
Wrong answer means structural collapse.
```

Correct boundary:

```text
Level 3 v9 measures structural warning risk over GSM-Symbolic answer traces
or model-output traces mapped into raw ordered trajectory events.
```

---

## Validation Rule

v9 must not weaken the boundary.

If the input comes from model outputs, the result must state:

```text
source_record_type: model_output
mapping_method: model_output_to_trajectory
```

If the input comes from answer traces, the result must state:

```text
source_record_type: answer_trace
mapping_method: answer_trace_to_trajectory
```

If the input comes from correctness traces, the result must state:

```text
source_record_type: correctness_trace
mapping_method: correctness_trace_to_trajectory
```

If direct answer or model-output records cannot be identified, the result should remain v8, not v9.

Boundary honesty is part of the result.

---

## Planned Files

Concept document:

```text
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_ANSWER_TRACE_VALIDATOR_V9.md
```

Input data:

```text
data/temporal_collapse_direct_gsm_symbolic_answer_traces_v9.jsonl
```

Script:

```text
examples/temporal_collapse_direct_gsm_symbolic_answer_trace_validator_v9.py
```

Result JSON:

```text
results/temporal_collapse_direct_gsm_symbolic_answer_trace_validator_v9.json
```

Result document:

```text
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_ANSWER_TRACE_VALIDATOR_V9_RESULT.md
```

---

## Next Step

After this document, the next step is to create the direct GSM-Symbolic answer-trace JSONL file:

```text
data/temporal_collapse_direct_gsm_symbolic_answer_traces_v9.jsonl
```

The v9 dataset must include answer-trace fields:

```text
model_name
run_id
response_id
expected_answer
model_final_answer
is_correct
```

Only after that should the validator be run.

The v9 objective is not to claim benchmark solving.

The v9 objective is to test whether the raw trajectory warning mechanism remains coherent when GSM-Symbolic answer traces or model-output traces are mapped directly into ordered structural events.