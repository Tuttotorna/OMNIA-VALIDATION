# Temporal Collapse Actual GSM-Symbolic Model Output Validator — v10

## Purpose

This document defines the Level 3 v10 direction of OMNIA-VALIDATION.

Level 3 v9 mapped direct GSM-Symbolic answer traces into raw ordered structural trajectory events.

Level 3 v10 moves one step further.

The objective is to move from:

```text
direct answer-trace mapping
```

to:

```text
actual model-output / parsed benchmark trace validation
```

```text
measurement != inference != decision
```

---

## Core Boundary

v10 must not claim that OMNIA solves GSM-Symbolic.

v10 must not claim semantic truth detection.

v10 must not replace official benchmark scoring.

v10 must not claim production certification.

v10 measures structural warning risk over actual model-output traces, parsed benchmark traces, or answer-extraction traces mapped into raw ordered structural events.

Correct boundary:

```text
Level 3 v10 maps actual GSM-Symbolic model-output traces or parsed benchmark
records into raw ordered structural trajectory events and measures warning risk.
```

Incorrect boundary:

```text
Level 3 v10 proves that OMNIA solves GSM-Symbolic.
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
v9 -> direct answer-trace mapping
v10 -> actual model-output / parsed benchmark trace validation
```

The v10 transition is from:

```text
answer_trace_to_trajectory
```

to:

```text
actual_model_output_to_trajectory
parsed_benchmark_trace_to_trajectory
answer_extraction_trace_to_trajectory
```

---

## Core Question

Given actual GSM-Symbolic model outputs, parsed benchmark records, or answer-extraction traces, can the Level 3 warning layer classify structural risk regimes using the same visible measurement logic used in v3 through v9?

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

## What v10 Does Not Claim

v10 does not claim:

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
v10 measures structural warning risk over actual model-output traces,
parsed benchmark traces, or answer-extraction traces mapped into raw ordered
trajectory events.
```

Incorrect claim:

```text
v10 proves that OMNIA understands or solves GSM-Symbolic.
```

---

## Required Source Boundary

For v10, the source boundary should be stronger than v9.

Recommended source independence:

```text
external_source_verified
```

Recommended independence method:

```text
actual_model_output_trace_mapping
```

Alternative valid independence methods:

```text
parsed_public_benchmark_trace_mapping
answer_extraction_trace_mapping
actual_model_output_trace_mapping
```

Recommended boundary:

```text
source: gsm_symbolic_actual_model_output_v10
source_independence: external_source_verified
independence_method: actual_model_output_trace_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: actual_model_output
mapping_method: actual_model_output_to_trajectory
```

Alternative valid source record types:

```text
actual_model_output
parsed_benchmark_record
answer_extraction_trace
correctness_trace
```

Alternative valid mapping methods:

```text
actual_model_output_to_trajectory
parsed_benchmark_trace_to_trajectory
answer_extraction_trace_to_trajectory
correctness_trace_to_trajectory
```

If actual model outputs are not present, the result should not be called actual model-output validation.

Boundary honesty is part of the measurement.

---

## Required Record Fields

Each v10 event must preserve benchmark identity, model-output identity, answer identity, extraction identity, and structural trajectory identity.

Required fields:

```text
trajectory_id
step
template_id
question_id
variant_type
model_name
model_version
run_id
response_id
raw_question_hash
raw_output_hash
answer_extraction_method
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
raw_question
model_raw_output
prompt_id
prompt_hash
temperature
seed
provider
response_latency_ms
token_count_input
token_count_output
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

## Direct Actual Model-Output Event Schema

Minimal event example:

```json
{
  "trajectory_id": "gsm_symbolic_actual_output_template_001_model_a",
  "step": 1,
  "template_id": "gsm_symbolic_template_001",
  "question_id": "gsm_symbolic_template_001_base",
  "variant_type": "base",
  "model_name": "model_a",
  "model_version": "model_a_version_001",
  "run_id": "run_001",
  "response_id": "response_001",
  "raw_question_hash": "sha256:question_hash_here",
  "raw_output_hash": "sha256:output_hash_here",
  "answer_extraction_method": "final_numeric_answer_extractor_v1",
  "expected_answer": "42",
  "model_final_answer": "42",
  "is_correct": true,
  "signature": "OUTPUT_OK_STABLE",
  "cluster": "OUT_C0",
  "delta": 0.04,
  "iri": 0.01,
  "boundary_distance": 0.94,
  "phase": "STABLE",
  "source": "gsm_symbolic_actual_model_output_v10",
  "source_independence": "external_source_verified",
  "independence_method": "actual_model_output_trace_mapping",
  "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
  "benchmark_name": "GSM-Symbolic",
  "source_record_type": "actual_model_output",
  "source_record_reference": "gsm_symbolic_template_001/base/model_a/run_001/response_001",
  "mapping_method": "actual_model_output_to_trajectory",
  "mapping_notes": "actual model output trace mapped into ordered structural trajectory event"
}
```

---

## Event Meaning

### trajectory_id

Identifier for one actual model-output trajectory.

A trajectory may correspond to:

```text
one template across variants for one model
one generated question across perturbations for one model
one parsed benchmark trace across variant types
one model-output trace across perturbations
one answer-extraction trace across symbolic changes
```

### step

Ordered position of the event inside the trajectory.

The validator must sort by `step`.

### template_id

Identifier of the GSM-Symbolic template or source template family.

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

Name or label of the model that produced the output.

### model_version

Version or stable label of the model.

If unknown, use:

```text
unknown
```

### run_id

Identifier of the run.

### response_id

Identifier of the model response.

### raw_question_hash

Hash of the raw question text.

This preserves traceability without forcing long raw text into the core result.

### raw_output_hash

Hash of the raw model output.

This preserves traceability without forcing long raw outputs into the core result.

### answer_extraction_method

Method used to extract the final answer.

Examples:

```text
manual_extraction
final_numeric_answer_extractor_v1
regex_final_number
provided_answer_field
```

### expected_answer

Benchmark expected answer.

This is evidence.

### model_final_answer

Extracted final model answer.

This is evidence.

### is_correct

Boolean correctness flag.

Important:

```text
is_correct is evidence
risk_score is structural warning measurement
```

Correctness transitions may be reported as evidence.

They must not silently replace structural warning signals.

### signature

Structural signature assigned to the event.

Examples:

```text
OUTPUT_OK_STABLE
OUTPUT_OK_VAR
OUTPUT_FAIL_DRIFT
OUTPUT_FAIL_CRITICAL
OUTPUT_BROKEN
```

### cluster

Cluster or regime label assigned to the event.

Examples:

```text
OUT_C0
OUT_C1
OUT_C2
OUT_C9
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
data/temporal_collapse_actual_gsm_symbolic_model_outputs_v10.jsonl
```

Each line must contain one actual model-output or parsed benchmark trace event.

---

## Output Format

Planned output file:

```text
results/temporal_collapse_actual_gsm_symbolic_model_output_validator_v10.json
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
model_versions
answer_extraction_methods
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
model_version
run_id
response_id
template_id
question_id
variant_type
answer_extraction_method
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

## v10 Warning Signals

v10 preserves the same five visible signals used by v3 through v9:

```text
transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal
```

Changing the formula at v10 would weaken comparability.

---

## Signal 1 — transition_density

Measures how often structural labels change across the ordered model-output trace.

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

v10 may report correctness changes as evidence:

```text
correctness_change_rate =
    normalized_change_count(is_correct)
```

Default rule:

```text
correctness_change_rate is evidence
not a hidden replacement for transition_density
```

---

## Signal 2 — drift_progression

Measures whether instability increases over the ordered model-output trace.

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

Measures how close the model-output trace comes to a structural boundary.

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

Measures whether the model-output trace resembles collapse-like behavior.

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
NOT_EXTRACTED
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

## Risk Formula v10

The v10 risk score should preserve the v3/v4/v5/v6/v7/v8/v9 raw trajectory formula:

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

## Correctness Profile

v10 should include a correctness profile for each trajectory:

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
correctness_profile is evidence
risk_score is structural warning measurement
```

Correctness and structural risk may correlate.

They are not the same measurement.

---

## Extraction Profile

Because v10 involves actual model outputs, the validator should track extraction quality.

Recommended extraction profile:

```json
{
  "event_count": 5,
  "extracted_count": 4,
  "not_extracted_count": 1,
  "extraction_rate": 0.8,
  "answer_extraction_methods": [
    "final_numeric_answer_extractor_v1"
  ]
}
```

Extraction failure is evidence.

It is not automatically collapse.

---

## Transition Evidence

Each v10 trajectory result should include:

```text
signature_changes
cluster_changes
phase_changes
correctness_changes
correct_count
incorrect_count
accuracy_rate
extracted_count
not_extracted_count
extraction_rate
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
model_version
run_id
response_id
template_id
question_id
variant_type
raw_question_hash
raw_output_hash
answer_extraction_method
```

This is required because v10 tests actual model-output or parsed benchmark trace mappings.

A trace-free v10 result is invalid.

---

## Source Summary

Because v10 involves actual model-output or parsed benchmark records, the result must include a source summary.

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
model_version
answer_extraction_method
trajectory_count
average_risk_score
average_accuracy_rate
average_extraction_rate
regime_counts
highest_risk_trajectory
highest_risk_score
```

This exposes whether one model, version, source, extraction method, or record class produces systematically higher warning pressure.

---

## Minimal Aggregate Result

The aggregate section should include:

```text
aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action
aggregate_accuracy_rate
aggregate_extraction_rate
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
model_version_count
answer_extraction_method_count
```

The aggregate must not hide individual trajectory results.

---

## Reproducibility Requirements

A valid v10 experiment should include:

```text
input JSONL file
validator script
output JSON
visible weights
visible thresholds
per-trajectory evidence
correctness profiles
extraction profiles
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
model version
run id
response id
raw question hash
raw output hash
answer extraction method
expected answer
model final answer
is_correct
```

---

## Minimum Valid v10 Construction

A minimum valid v10 construction should include:

```text
source: gsm_symbolic_actual_model_output_v10
source_independence: external_source_verified
independence_method: actual_model_output_trace_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: actual_model_output
mapping_method: actual_model_output_to_trajectory
```

It should include at least five trajectory types:

```text
actual model-output stable trajectory
actual model-output drift trajectory
actual model-output borderline critical trajectory
actual model-output critical trajectory
actual model-output collapse-like trajectory
```

---

## Safe Claim

Safe v10 claim:

```text
OMNIA-VALIDATION Level 3 v10 applies the raw trajectory warning mechanism
to actual GSM-Symbolic model-output traces, parsed benchmark traces, or
answer-extraction traces mapped into raw ordered structural trajectory events.

The validator measures structural warning risk using visible weights,
visible thresholds, source labels, benchmark references, model-output fields,
answer-extraction fields, answer-correctness fields, extraction profiles,
correctness profiles, mapping methods, and inspectable transition evidence.
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
Level 3 v10 is production-certified.
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

Do not claim:

```text
Extraction failure automatically means collapse.
```

Correct boundary:

```text
Level 3 v10 measures structural warning risk over actual model-output,
parsed benchmark, or answer-extraction traces mapped into raw ordered
trajectory events.
```

---

## Validation Rule

v10 must not weaken the boundary.

If the input comes from actual model outputs, the result must state:

```text
source_record_type: actual_model_output
mapping_method: actual_model_output_to_trajectory
```

If the input comes from parsed benchmark records, the result must state:

```text
source_record_type: parsed_benchmark_record
mapping_method: parsed_benchmark_trace_to_trajectory
```

If the input comes from answer extraction traces, the result must state:

```text
source_record_type: answer_extraction_trace
mapping_method: answer_extraction_trace_to_trajectory
```

If actual model-output records cannot be identified, the result should remain v9, not v10.

Boundary honesty is part of the result.

---

## Planned Files

Concept document:

```text
docs/TEMPORAL_COLLAPSE_ACTUAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V10.md
```

Input data:

```text
data/temporal_collapse_actual_gsm_symbolic_model_outputs_v10.jsonl
```

Script:

```text
examples/temporal_collapse_actual_gsm_symbolic_model_output_validator_v10.py
```

Result JSON:

```text
results/temporal_collapse_actual_gsm_symbolic_model_output_validator_v10.json
```

Result document:

```text
docs/TEMPORAL_COLLAPSE_ACTUAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V10_RESULT.md
```

---

## Next Step

After this document, the next step is to create the actual GSM-Symbolic model-output JSONL file:

```text
data/temporal_collapse_actual_gsm_symbolic_model_outputs_v10.jsonl
```

The v10 dataset must include actual-output trace fields:

```text
model_name
model_version
run_id
response_id
raw_question_hash
raw_output_hash
answer_extraction_method
expected_answer
model_final_answer
is_correct
```

Only after that should the validator be run.

The v10 objective is not to claim benchmark solving.

The v10 objective is to test whether the raw trajectory warning mechanism remains coherent when actual GSM-Symbolic model-output traces, parsed benchmark traces, or answer-extraction traces are mapped directly into ordered structural events.