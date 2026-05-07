# Temporal Collapse Real GSM-Symbolic Model Output Validator — v11

## Purpose

This document defines the Level 3 v11 direction of OMNIA-VALIDATION.

Level 3 v10 validated bounded actual-output-style GSM-Symbolic model-output traces.

Level 3 v11 moves one step further.

The objective is to move from:

```text
bounded actual-output-style model-output mapping
```

to:

```text
real parsed model-output file validation
```

```text
measurement != inference != decision
```

---

## Core Boundary

v11 must not claim that OMNIA solves GSM-Symbolic.

v11 must not claim semantic truth detection.

v11 must not replace official benchmark scoring.

v11 must not claim production certification.

v11 measures structural warning risk over real parsed model-output files mapped into raw ordered structural trajectory events.

Correct boundary:

```text
Level 3 v11 maps real parsed GSM-Symbolic model-output files into raw ordered
structural trajectory events and measures warning risk.
```

Incorrect boundary:

```text
Level 3 v11 proves that OMNIA solves GSM-Symbolic.
```

---

## Core Transition

The Level 3 progression is:

```text
v0  -> synthetic reference trajectories
v1  -> Level 2-derived snapshots
v2  -> ordered Level 2 stage trajectory
v3  -> raw ordered reference trajectories
v4  -> external-style raw trajectory validation
v5  -> separate-generator raw trajectory validation
v6  -> declared external-source raw trajectory validation
v7  -> verified external-source raw trajectory validation
v8  -> direct public benchmark record mapping
v9  -> direct answer-trace mapping
v10 -> bounded actual-output-style model-output mapping
v11 -> real parsed model-output file validation
```

The v11 transition is from:

```text
actual_model_output_to_trajectory
```

to:

```text
real_model_output_file_to_trajectory
```

---

## What Changed from v10

v10 used bounded actual-output-style records.

v11 must use records parsed from a real source file, real model-output file, actual run log, or externally generated output artifact.

v10 boundary:

```text
source_record_type: actual_model_output
mapping_method: actual_model_output_to_trajectory
```

v11 target boundary:

```text
source_record_type: real_model_output_file
mapping_method: real_model_output_file_to_trajectory
```

v10 limitation:

```text
not an official public GSM-Symbolic model-output benchmark run
```

v11 limitation should be more specific:

```text
real parsed model-output file validation does not imply official benchmark scoring
```

If the source file is not official, say it directly.

Boundary honesty is part of the measurement.

---

## Core Question

Given real parsed GSM-Symbolic model-output records, can the Level 3 warning layer classify structural risk regimes using the same visible measurement logic used in v3 through v10?

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

## What v11 Does Not Claim

v11 does not claim:

```text
GSM-Symbolic solving
semantic truth detection
benchmark correctness replacement
official leaderboard scoring
model cognition detection
universal collapse prediction
production certification
final decision authority
```

Correct claim:

```text
v11 measures structural warning risk over real parsed GSM-Symbolic model-output
files mapped into raw ordered trajectory events.
```

Incorrect claim:

```text
v11 proves that OMNIA understands or solves GSM-Symbolic.
```

---

## Required Source Boundary

Recommended source independence:

```text
external_source_verified
```

Recommended independence method:

```text
real_model_output_file_mapping
```

Recommended source record type:

```text
real_model_output_file
```

Recommended mapping method:

```text
real_model_output_file_to_trajectory
```

Recommended boundary:

```text
source: gsm_symbolic_real_model_output_v11
source_independence: external_source_verified
independence_method: real_model_output_file_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: real_model_output_file
mapping_method: real_model_output_file_to_trajectory
```

Alternative valid source record types:

```text
real_model_output_file
real_answer_extraction_log
real_benchmark_run_file
real_model_response_jsonl
real_parsed_output_trace
```

Alternative valid mapping methods:

```text
real_model_output_file_to_trajectory
real_answer_extraction_log_to_trajectory
real_benchmark_run_file_to_trajectory
real_model_response_jsonl_to_trajectory
real_parsed_output_trace_to_trajectory
```

If the file is synthetic or bounded construction, it should remain v10.

If the file contains real outputs but not official benchmark outputs, the result must say so.

---

## Required Record Fields

Each v11 event must preserve file identity, model-output identity, answer identity, extraction identity, and structural trajectory identity.

Required fields:

```text
trajectory_id
step
template_id
question_id
variant_type
model_name
model_version
provider
run_id
response_id
source_file
source_file_hash
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
parser_version
extractor_version
source_line_number
notes
```

---

## Minimal Event Schema

Minimal event example:

```json
{
  "trajectory_id": "gsm_symbolic_real_output_template_001_model_a",
  "step": 1,
  "template_id": "gsm_symbolic_template_001",
  "question_id": "gsm_symbolic_template_001_base",
  "variant_type": "base",
  "model_name": "model_a",
  "model_version": "model_a_version_001",
  "provider": "provider_name",
  "run_id": "run_001",
  "response_id": "response_001",
  "source_file": "data/source_outputs/model_a_gsm_symbolic_outputs.jsonl",
  "source_file_hash": "sha256:source_file_hash_here",
  "raw_question_hash": "sha256:question_hash_here",
  "raw_output_hash": "sha256:output_hash_here",
  "answer_extraction_method": "final_numeric_answer_extractor_v1",
  "expected_answer": "42",
  "model_final_answer": "42",
  "is_correct": true,
  "signature": "REAL_OUTPUT_OK_STABLE",
  "cluster": "REAL_OUT_C0",
  "delta": 0.04,
  "iri": 0.01,
  "boundary_distance": 0.94,
  "phase": "STABLE",
  "source": "gsm_symbolic_real_model_output_v11",
  "source_independence": "external_source_verified",
  "independence_method": "real_model_output_file_mapping",
  "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
  "benchmark_name": "GSM-Symbolic",
  "source_record_type": "real_model_output_file",
  "source_record_reference": "data/source_outputs/model_a_gsm_symbolic_outputs.jsonl#response_001",
  "mapping_method": "real_model_output_file_to_trajectory",
  "mapping_notes": "real parsed model-output file record mapped into ordered structural trajectory event"
}
```

---

## Input Format

Preferred input format:

```text
JSONL
```

Planned input file:

```text
data/temporal_collapse_real_gsm_symbolic_model_outputs_v11.jsonl
```

Each line must contain one event parsed from a real model-output file or real answer-extraction log.

---

## Source File Requirement

v11 must include source-file fields.

Required:

```text
source_file
source_file_hash
source_record_reference
```

This is the main difference from v10.

v10 had output-style fields.

v11 must point to an actual parsed source file or run artifact.

A v11 result without `source_file` and `source_file_hash` is structurally weaker and should not be called v11.

---

## Output Format

Planned output file:

```text
results/temporal_collapse_real_gsm_symbolic_model_output_validator_v11.json
```

Output should include:

```text
experiment
status
boundary
claim
limitation_note
input_file
trajectory_count
source_count
source_independence_values
independence_method_values
external_source_references
benchmark_names
source_record_types
mapping_methods
source_files
source_file_hashes
model_names
model_versions
providers
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
source_file
source_file_hash
model_name
model_version
provider
run_id
response_id
template_id
question_id
variant_type
raw_question_hash
raw_output_hash
answer_extraction_method
correctness_profile
extraction_profile
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

## v11 Warning Signals

v11 preserves the same five visible signals used by v3 through v10:

```text
transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal
```

Changing the formula at v11 would weaken comparability.

---

## Risk Formula v11

The v11 risk score should preserve the v3 through v10 raw trajectory formula:

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

v11 should include a correctness profile for each trajectory:

```json
{
  "event_count": 5,
  "correct_count": 3,
  "incorrect_count": 2,
  "accuracy_rate": 0.6,
  "correctness_changes": 0.25,
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

v11 should include an extraction profile for each trajectory:

```json
{
  "event_count": 5,
  "extracted_count": 4,
  "not_extracted_count": 1,
  "extraction_rate": 0.8,
  "extraction_changes": 0.25,
  "starts_extracted": true,
  "ends_extracted": false,
  "answer_extraction_methods": [
    "final_numeric_answer_extractor_v1"
  ]
}
```

Extraction failure is evidence.

It is not automatically collapse.

---

## Transition Evidence

Each v11 trajectory result should include:

```text
signature_changes
cluster_changes
phase_changes
correctness_changes
extraction_changes
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
source_file
source_file_hash
model_name
model_version
provider
run_id
response_id
template_id
question_id
variant_type
raw_question_hash
raw_output_hash
answer_extraction_method
```

This is required because v11 tests real parsed model-output file mappings.

A source-file-free v11 result is invalid.

---

## Source Summary

Because v11 involves real parsed output files, the result must include a source summary.

The source summary should include:

```text
source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
mapping_method
source_file
source_file_hash
model_name
model_version
provider
answer_extraction_method
trajectory_count
average_risk_score
average_accuracy_rate
average_extraction_rate
regime_counts
highest_risk_trajectory
highest_risk_score
```

This exposes whether one source file, model, provider, extraction method, or record class produces systematically higher warning pressure.

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
source_file_count
source_file_hash_count
model_count
model_version_count
provider_count
answer_extraction_method_count
```

The aggregate must not hide individual trajectory results.

---

## Reproducibility Requirements

A valid v11 experiment should include:

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
source file references
source file hashes
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
provider
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

## Minimum Valid v11 Construction

A minimum valid v11 construction should include:

```text
source: gsm_symbolic_real_model_output_v11
source_independence: external_source_verified
independence_method: real_model_output_file_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: real_model_output_file
mapping_method: real_model_output_file_to_trajectory
```

It should include at least five trajectory types:

```text
real model-output stable trajectory
real model-output drift trajectory
real model-output borderline critical trajectory
real model-output critical trajectory
real model-output collapse-like trajectory
```

Each trajectory must point to one or more real source-file records.

---

## Safe Claim

Safe v11 claim:

```text
OMNIA-VALIDATION Level 3 v11 applies the raw trajectory warning mechanism
to real parsed GSM-Symbolic model-output files mapped into raw ordered
structural trajectory events.

The validator measures structural warning risk using visible weights,
visible thresholds, source-file references, source-file hashes, model-output
fields, answer-extraction fields, correctness profiles, extraction profiles,
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
Level 3 v11 is production-certified.
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
Level 3 v11 measures structural warning risk over real parsed model-output files
mapped into raw ordered trajectory events.
```

---

## Validation Rule

v11 must not weaken the boundary.

If the input comes from a real parsed model-output file, the result must state:

```text
source_record_type: real_model_output_file
mapping_method: real_model_output_file_to_trajectory
```

If the input comes from a real answer-extraction log, the result must state:

```text
source_record_type: real_answer_extraction_log
mapping_method: real_answer_extraction_log_to_trajectory
```

If the input comes from a real benchmark run file, the result must state:

```text
source_record_type: real_benchmark_run_file
mapping_method: real_benchmark_run_file_to_trajectory
```

If the input is bounded construction only, the result should remain v10, not v11.

Boundary honesty is part of the result.

---

## Planned Files

Concept document:

```text
docs/TEMPORAL_COLLAPSE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V11.md
```

Input data:

```text
data/temporal_collapse_real_gsm_symbolic_model_outputs_v11.jsonl
```

Script:

```text
examples/temporal_collapse_real_gsm_symbolic_model_output_validator_v11.py
```

Result JSON:

```text
results/temporal_collapse_real_gsm_symbolic_model_output_validator_v11.json
```

Result document:

```text
docs/TEMPORAL_COLLAPSE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V11_RESULT.md
```

---

## Next Step

After this document, the next step is to create the real parsed model-output JSONL file:

```text
data/temporal_collapse_real_gsm_symbolic_model_outputs_v11.jsonl
```

The v11 dataset must include source-file trace fields:

```text
source_file
source_file_hash
source_record_reference
provider
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

The v11 objective is not to claim benchmark solving.

The v11 objective is to test whether the raw trajectory warning mechanism remains coherent when records come from real parsed model-output files rather than bounded actual-output-style construction.