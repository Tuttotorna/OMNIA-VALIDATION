# Temporal Collapse Multi-Source Real GSM-Symbolic Model Output Validator — v12

## Purpose

This document defines the Level 3 v12 direction of OMNIA-VALIDATION.

Level 3 v11 validated real parsed GSM-Symbolic model-output file records mapped into raw ordered structural trajectory events.

Level 3 v12 moves one step further.

The objective is to move from:

```text
single real parsed model-output file validation

to:

multi-source / multi-model real parsed output validation

measurement != inference != decision


---

Core Boundary

v12 must not claim that OMNIA solves GSM-Symbolic.

v12 must not claim semantic truth detection.

v12 must not replace official benchmark scoring.

v12 must not claim production certification.

v12 measures structural warning risk across multiple real parsed GSM-Symbolic model-output source files mapped into raw ordered structural trajectory events.

Correct boundary:

Level 3 v12 maps multiple real parsed GSM-Symbolic model-output source files
into raw ordered structural trajectory events and measures cross-source warning risk.

Incorrect boundary:

Level 3 v12 proves that OMNIA solves GSM-Symbolic across multiple models.


---

Core Transition

The Level 3 progression is:

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
v12 -> multi-source / multi-model real parsed output validation

The v12 transition is from:

real_model_output_file_to_trajectory

to:

multi_source_real_model_output_file_to_trajectory


---

What Changed from v11

v11 used one real parsed model-output source file.

v12 must use multiple source files, multiple providers, multiple model families, or multiple independently parsed output traces.

v11 boundary:

source_record_type: real_model_output_file
mapping_method: real_model_output_file_to_trajectory

v12 target boundary:

source_record_type: multi_source_real_model_output_file
mapping_method: multi_source_real_model_output_file_to_trajectory

v11 limitation:

real parsed model-output file validation does not imply official benchmark scoring

v12 limitation:

multi-source real parsed model-output validation does not imply official benchmark scoring

If the files are reference files, say so directly.

If the providers are reference providers, say so directly.

Boundary honesty is part of the measurement.


---

Core Question

Given multiple real parsed GSM-Symbolic model-output source files, can the Level 3 warning layer classify structural risk regimes while preserving source-file provenance, provider identity, model identity, extraction identity, and cross-source comparability?

Target regimes:

STABLE
DRIFT
CRITICAL
COLLAPSE

Gate actions:

STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP

The gate action is not a final decision.

It is a measurement-derived warning for an external decision layer.


---

What v12 Does Not Claim

v12 does not claim:

GSM-Symbolic solving
semantic truth detection
benchmark correctness replacement
official leaderboard scoring
model cognition detection
universal collapse prediction
production certification
final decision authority
cross-provider superiority proof

Correct claim:

v12 measures structural warning risk across multiple real parsed GSM-Symbolic
model-output source files mapped into raw ordered trajectory events.

Incorrect claim:

v12 proves which model understands GSM-Symbolic.


---

Required Source Boundary

Recommended source independence:

external_source_verified

Recommended independence method:

multi_source_real_model_output_file_mapping

Recommended source record type:

multi_source_real_model_output_file

Recommended mapping method:

multi_source_real_model_output_file_to_trajectory

Recommended boundary:

source: gsm_symbolic_multi_source_real_model_output_v12
source_independence: external_source_verified
independence_method: multi_source_real_model_output_file_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: multi_source_real_model_output_file
mapping_method: multi_source_real_model_output_file_to_trajectory

Alternative valid source record types:

multi_source_real_model_output_file
multi_provider_real_model_output_file
multi_model_real_answer_extraction_log
multi_source_real_benchmark_run_file
multi_source_real_model_response_jsonl
multi_source_real_parsed_output_trace

Alternative valid mapping methods:

multi_source_real_model_output_file_to_trajectory
multi_provider_real_model_output_file_to_trajectory
multi_model_real_answer_extraction_log_to_trajectory
multi_source_real_benchmark_run_file_to_trajectory
multi_source_real_model_response_jsonl_to_trajectory
multi_source_real_parsed_output_trace_to_trajectory

If the data comes from one source file only, it should remain v11.

If the data is bounded construction only, it should remain v10.


---

Required Source Files

Recommended source-output files:

data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_a.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_b.jsonl

Mapped dataset:

data/temporal_collapse_multi_source_real_gsm_symbolic_model_outputs_v12.jsonl

Validator script:

examples/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.py

Result JSON:

results/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.json

Result document:

docs/TEMPORAL_COLLAPSE_MULTI_SOURCE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V12_RESULT.md


---

Required Record Fields

Each v12 event must preserve file identity, provider identity, model-output identity, answer identity, extraction identity, and structural trajectory identity.

Required fields:

trajectory_id
step
source_group_id
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

New v12 fields:

source_group_id
source_file
source_file_hash
provider
cross_source_group
cross_source_role

Optional fields:

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


---

Minimal Event Schema

Minimal event example:

{
  "trajectory_id": "gsm_symbolic_multi_source_output_template_001_provider_a_model_a",
  "step": 1,
  "source_group_id": "provider_a_reference_group",
  "template_id": "gsm_symbolic_template_001",
  "question_id": "gsm_symbolic_template_001_base",
  "variant_type": "base",
  "model_name": "provider_a_model_a",
  "model_version": "provider_a_model_a_v1",
  "provider": "provider_a",
  "run_id": "provider_a_run_001",
  "response_id": "provider_a_response_001",
  "source_file": "data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_a.jsonl",
  "source_file_hash": "sha256:provider_a_source_file_hash_v12",
  "raw_question_hash": "sha256:question_hash_here",
  "raw_output_hash": "sha256:output_hash_here",
  "answer_extraction_method": "final_numeric_answer_extractor_v1",
  "expected_answer": "42",
  "model_final_answer": "42",
  "is_correct": true,
  "signature": "MULTI_SOURCE_OUTPUT_OK_STABLE",
  "cluster": "MULTI_OUT_A_C0",
  "delta": 0.04,
  "iri": 0.01,
  "boundary_distance": 0.94,
  "phase": "STABLE",
  "source": "gsm_symbolic_multi_source_real_model_output_v12",
  "source_independence": "external_source_verified",
  "independence_method": "multi_source_real_model_output_file_mapping",
  "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
  "benchmark_name": "GSM-Symbolic",
  "source_record_type": "multi_source_real_model_output_file",
  "source_record_reference": "data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_a.jsonl#provider_a_response_001",
  "mapping_method": "multi_source_real_model_output_file_to_trajectory",
  "mapping_notes": "multi-source real parsed model-output file record mapped into ordered structural trajectory event",
  "cross_source_group": "template_001_cross_source_group",
  "cross_source_role": "provider_a_member"
}


---

Input Format

Preferred input format:

JSONL

Planned mapped input file:

data/temporal_collapse_multi_source_real_gsm_symbolic_model_outputs_v12.jsonl

Each line must contain one event parsed from a real model-output file, answer-extraction log, or real parsed output trace.


---

Source File Requirement

v12 must include multiple source-file fields.

Required:

source_file
source_file_hash
source_record_reference
source_group_id
provider
model_name
model_version
run_id
response_id

This is the main difference from v11.

v11 used one source file.

v12 must compare multiple source files, providers, models, or source groups.

A v12 result without more than one source file, provider, model family, or source group is structurally weak and should not be called v12.


---

Output Format

Planned output file:

results/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.json

Output should include:

experiment
status
boundary
claim
limitation_note
input_file
trajectory_count
source_count
source_group_count
provider_count
model_count
model_version_count
source_file_count
source_independence_values
independence_method_values
external_source_references
benchmark_names
source_record_types
mapping_methods
source_files
source_file_hashes
providers
model_names
model_versions
answer_extraction_methods
external_source_note
weights
thresholds
aggregate
source_summary
provider_summary
model_summary
cross_source_summary
results

Each trajectory result should include:

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
source_group_id
source_file
source_file_hash
provider
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


---

v12 Warning Signals

v12 preserves the same five visible signals used by v3 through v11:

transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal

Changing the formula at v12 would weaken comparability.


---

Risk Formula v12

The v12 risk score should preserve the v3 through v11 raw trajectory formula:

risk_score =
    0.20 * transition_density
  + 0.20 * drift_progression
  + 0.25 * boundary_proximity
  + 0.25 * collapse_similarity
  + 0.10 * irreversibility_signal

Weights:

{
  "transition_density": 0.2,
  "drift_progression": 0.2,
  "boundary_proximity": 0.25,
  "collapse_similarity": 0.25,
  "irreversibility_signal": 0.1
}

The weights are experimental.

They are not universal.

They remain visible.


---

Classification Thresholds

Initial thresholds:

risk_score < 0.25         -> STABLE
0.25 <= risk_score < 0.50 -> DRIFT
0.50 <= risk_score < 0.75 -> CRITICAL
risk_score >= 0.75        -> COLLAPSE

Gate actions:

STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP

Thresholds are experimental and must remain visible.


---

Correctness Profile

v12 should include a correctness profile for each trajectory:

{
  "event_count": 5,
  "correct_count": 3,
  "incorrect_count": 2,
  "accuracy_rate": 0.6,
  "correctness_changes": 0.25,
  "starts_correct": true,
  "ends_correct": false
}

Important boundary:

correctness_profile is evidence
risk_score is structural warning measurement

Correctness and structural risk may correlate.

They are not the same measurement.


---

Extraction Profile

v12 should include an extraction profile for each trajectory:

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

Extraction failure is evidence.

It is not automatically collapse.


---

Cross-Source Summary

v12 should include a cross-source summary.

The cross-source summary should expose whether risk differs by:

source_file
source_group_id
provider
model_name
model_version
answer_extraction_method
trajectory_family

Suggested fields:

source_file_count
source_group_count
provider_count
model_count
model_version_count
answer_extraction_method_count
highest_risk_source_file
highest_risk_provider
highest_risk_model
highest_risk_trajectory
lowest_risk_source_file
lowest_risk_provider
lowest_risk_model
average_risk_by_provider
average_accuracy_by_provider
average_extraction_by_provider
regime_counts_by_provider


---

Transition Evidence

Each v12 trajectory result should include:

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
broken_signature_count
not_extracted_signature_count
source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
source_record_reference
mapping_method
mapping_notes
source_group_id
source_file
source_file_hash
provider
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

This is required because v12 tests multi-source real parsed model-output file mappings.

A single-source-only v12 result is invalid or should be downgraded to v11.


---

Source Summary

Because v12 involves multiple real parsed output sources, the result must include a source summary.

The source summary should include:

source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
mapping_method
source_group_id
source_file
source_file_hash
provider
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

This exposes whether one source file, model, provider, extraction method, or record class produces systematically higher warning pressure.


---

Minimal Aggregate Result

The aggregate section should include:

aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action
aggregate_accuracy_rate
aggregate_extraction_rate
regime_counts
highest_risk_trajectory
highest_risk_score
source_count
source_group_count
independence_method_count
external_source_reference_count
benchmark_count
source_record_type_count
mapping_method_count
source_file_count
source_file_hash_count
provider_count
model_count
model_version_count
answer_extraction_method_count

The aggregate must not hide individual trajectory results.


---

Reproducibility Requirements

A valid v12 experiment should include:

multiple source-output JSONL files
mapped input JSONL file
validator script
output JSON
visible weights
visible thresholds
per-trajectory evidence
correctness profiles
extraction profiles
source summary
provider summary
model summary
cross-source summary
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
source group id
provider
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


---

Minimum Valid v12 Construction

A minimum valid v12 construction should include:

source: gsm_symbolic_multi_source_real_model_output_v12
source_independence: external_source_verified
independence_method: multi_source_real_model_output_file_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: multi_source_real_model_output_file
mapping_method: multi_source_real_model_output_file_to_trajectory

It should include at least:

2 source files
2 source groups
2 providers or provider labels
2 model families or model labels
5 trajectory families
25+ mapped events

Recommended trajectory families:

multi-source stable trajectory
multi-source drift trajectory
multi-source borderline critical trajectory
multi-source critical trajectory
multi-source collapse-like trajectory

Each trajectory must point to one or more real source-file records.


---

Safe Claim

Safe v12 claim:

OMNIA-VALIDATION Level 3 v12 applies the raw trajectory warning mechanism
to multiple real parsed GSM-Symbolic model-output source files mapped into
raw ordered structural trajectory events.

The validator measures structural warning risk using visible weights,
visible thresholds, source-file references, source-file hashes, provider fields,
model-output fields, answer-extraction fields, correctness profiles,
extraction profiles, mapping methods, source summaries, provider summaries,
cross-source summaries, and inspectable transition evidence.


---

Claims to Avoid

Do not claim:

OMNIA predicts AI collapse universally.

Do not claim:

OMNIA detects semantic truth.

Do not claim:

Level 3 v12 is production-certified.

Do not claim:

The thresholds are universal.

Do not claim:

OMNIA solves GSM-Symbolic.

Do not claim:

Structural warning risk equals benchmark correctness.

Do not claim:

Correct answer means structural stability.

Do not claim:

Wrong answer means structural collapse.

Do not claim:

Extraction failure automatically means collapse.

Do not claim:

A higher-risk provider is semantically worse.

Correct boundary:

Level 3 v12 measures structural warning risk across multiple real parsed
model-output source files mapped into raw ordered trajectory events.


---

Validation Rule

v12 must not weaken the boundary.

If the input comes from multiple real parsed model-output files, the result must state:

source_record_type: multi_source_real_model_output_file
mapping_method: multi_source_real_model_output_file_to_trajectory

If the input comes from multiple real answer-extraction logs, the result must state:

source_record_type: multi_model_real_answer_extraction_log
mapping_method: multi_model_real_answer_extraction_log_to_trajectory

If the input comes from multiple real benchmark run files, the result must state:

source_record_type: multi_source_real_benchmark_run_file
mapping_method: multi_source_real_benchmark_run_file_to_trajectory

If the input is one source file only, the result should remain v11, not v12.

If the input is bounded construction only, the result should remain v10, not v12.

Boundary honesty is part of the result.


---

Planned Files

Concept document:

docs/TEMPORAL_COLLAPSE_MULTI_SOURCE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V12.md

Source-output files:

data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_a.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_b.jsonl

Mapped input data:

data/temporal_collapse_multi_source_real_gsm_symbolic_model_outputs_v12.jsonl

Script:

examples/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.py

Result JSON:

results/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.json

Result document:

docs/TEMPORAL_COLLAPSE_MULTI_SOURCE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V12_RESULT.md


---

Next Step

After this document, the next step is to create the source-output JSONL files:

data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_a.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_b.jsonl

Then create the mapped v12 dataset:

data/temporal_collapse_multi_source_real_gsm_symbolic_model_outputs_v12.jsonl

The v12 dataset must include source-file trace fields:

source_file
source_file_hash
source_record_reference
source_group_id
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

The v12 objective is not to claim benchmark solving.

The v12 objective is to test whether the raw trajectory warning mechanism remains coherent when records come from multiple real parsed model-output source files rather than one source file.