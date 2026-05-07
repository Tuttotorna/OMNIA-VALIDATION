# Temporal Collapse Repeated-Run Cross-Provider Stability Validator — v14

## Purpose

This document defines the Level 3 v14 direction of OMNIA-VALIDATION.

Level 3 v13 measured cross-provider disagreement over real parsed GSM-Symbolic model-output file records.

Level 3 v14 moves one step further.

The objective is to move from:

```text
cross-provider disagreement mapping

to:

repeated-run cross-provider stability validation

measurement != inference != decision


---

Core Boundary

v14 must not claim that OMNIA solves GSM-Symbolic.

v14 must not claim semantic truth detection.

v14 must not replace official benchmark scoring.

v14 must not claim production certification.

v14 must not claim universal provider ranking.

v14 measures whether cross-provider structural disagreement remains stable, weakens, strengthens, or flips across repeated runs.

Correct boundary:

Level 3 v14 maps repeated-run cross-provider GSM-Symbolic model-output records
into raw ordered structural trajectory events and measures cross-run stability.

Incorrect boundary:

Level 3 v14 proves which provider is objectively better.


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
v12 -> multi-source real parsed model-output file validation
v13 -> cross-provider disagreement validation
v14 -> repeated-run cross-provider stability validation

The v14 transition is from:

cross_provider_real_model_output_disagreement_mapping

to:

repeated_run_cross_provider_stability_mapping


---

What Changed from v13

v13 compares providers across matched GSM-Symbolic template groups.

v14 compares repeated runs inside each provider and across providers.

v13 asks:

Do providers disagree structurally on the same template group?

v14 asks:

Does that provider disagreement remain stable across repeated runs?

v13 boundary:

source_record_type: cross_provider_real_model_output_file
mapping_method: cross_provider_real_model_output_file_to_trajectory

v14 target boundary:

source_record_type: repeated_run_cross_provider_real_model_output_file
mapping_method: repeated_run_cross_provider_stability_to_trajectory

v13 limitation:

Cross-provider disagreement validation does not imply official benchmark scoring,
production certification, semantic truth detection, or final decision authority.

v14 limitation:

Repeated-run cross-provider stability validation does not imply official benchmark
scoring, production certification, semantic truth detection, provider ranking, or
final decision authority.


---

Core Question

Given repeated-run cross-provider GSM-Symbolic model-output records, can the Level 3 warning layer measure whether structural risk patterns remain stable across runs?

Target run-stability regimes:

RUN_STABLE
RUN_DRIFT
RUN_UNSTABLE
RUN_COLLAPSE_LIKE

Target structural risk regimes remain:

STABLE
DRIFT
CRITICAL
COLLAPSE

Gate actions remain:

STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP

The gate action is not a final decision.

It is a measurement-derived warning for an external decision layer.


---

What v14 Does Not Claim

v14 does not claim:

GSM-Symbolic solving
semantic truth detection
benchmark correctness replacement
official leaderboard scoring
model cognition detection
provider superiority
provider ranking
universal collapse prediction
production certification
final decision authority

Correct claim:

v14 measures repeated-run structural stability over cross-provider GSM-Symbolic
model-output records mapped into raw ordered trajectory events.

Incorrect claim:

v14 proves that one provider is better than another.


---

Required Source Boundary

Recommended source independence:

external_source_verified

Recommended independence method:

repeated_run_cross_provider_stability_mapping

Recommended source record type:

repeated_run_cross_provider_real_model_output_file

Recommended mapping method:

repeated_run_cross_provider_stability_to_trajectory

Recommended boundary:

source: gsm_symbolic_repeated_run_cross_provider_stability_v14
source_independence: external_source_verified
independence_method: repeated_run_cross_provider_stability_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: repeated_run_cross_provider_real_model_output_file
mapping_method: repeated_run_cross_provider_stability_to_trajectory

Alternative valid source record types:

repeated_run_cross_provider_real_model_output_file
repeated_run_answer_extraction_log
repeated_run_benchmark_output_file
repeated_run_model_response_jsonl
repeated_run_provider_comparison_trace

Alternative valid mapping methods:

repeated_run_cross_provider_stability_to_trajectory
repeated_run_answer_extraction_log_to_trajectory
repeated_run_benchmark_output_file_to_trajectory
repeated_run_model_response_jsonl_to_trajectory
repeated_run_provider_comparison_trace_to_trajectory

If the file contains only one run per provider, it should remain v13.

If the file contains repeated runs but no cross-provider grouping, it should not be called cross-provider v14.

Boundary honesty is part of the measurement.


---

Required Record Fields

Each v14 event must preserve source identity, provider identity, model identity, run identity, repeated-run identity, answer identity, extraction identity, and structural trajectory identity.

Required fields:

trajectory_id
step
template_id
question_id
variant_type
provider
model_name
model_version
run_id
run_index
run_group_id
response_id
source_file
source_file_hash
source_group_id
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
cross_provider_group
cross_provider_role
repeated_run_group
repeated_run_role

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
  "trajectory_id": "gsm_symbolic_repeated_run_provider_a_template_001_run_001",
  "step": 1,
  "template_id": "gsm_symbolic_template_001",
  "question_id": "gsm_symbolic_template_001_base",
  "variant_type": "base",
  "provider": "provider_a",
  "model_name": "provider_a_model_alpha",
  "model_version": "provider_a_model_alpha_v1",
  "run_id": "provider_a_run_v14_001",
  "run_index": 1,
  "run_group_id": "provider_a_template_001_repeated_runs",
  "response_id": "provider_a_run_001_response_001",
  "source_file": "data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl",
  "source_file_hash": "sha256:provider_a_run_001_source_file_hash_v14",
  "source_group_id": "provider_a_repeated_run_group",
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
  "source": "gsm_symbolic_repeated_run_cross_provider_stability_v14",
  "source_independence": "external_source_verified",
  "independence_method": "repeated_run_cross_provider_stability_mapping",
  "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
  "benchmark_name": "GSM-Symbolic",
  "source_record_type": "repeated_run_cross_provider_real_model_output_file",
  "source_record_reference": "data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl#provider_a_run_001_response_001",
  "mapping_method": "repeated_run_cross_provider_stability_to_trajectory",
  "mapping_notes": "repeated-run real parsed model-output file record mapped into ordered structural trajectory event",
  "cross_provider_group": "gsm_symbolic_template_001_cross_provider_group",
  "cross_provider_role": "provider_a_member",
  "repeated_run_group": "provider_a_template_001_repeated_runs",
  "repeated_run_role": "run_001_member"
}


---

Input Format

Preferred input format:

JSONL

Planned input file:

data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl

Each line must contain one event parsed from a repeated-run cross-provider model-output file or repeated answer-extraction log.


---

Source File Requirement

v14 must include repeated-run source-file fields.

Required:

source_file
source_file_hash
source_record_reference
run_id
run_index
run_group_id
repeated_run_group
repeated_run_role
cross_provider_group
cross_provider_role

This is the main difference from v13.

v13 compares providers once.

v14 measures whether provider disagreement remains stable across repeated runs.

A v14 result without repeated-run identifiers is structurally weaker and should not be called v14.


---

Output Format

Planned output file:

results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json

Output should include:

experiment
status
boundary
claim
limitation_note
input_file
trajectory_count
event_count
source_count
source_independence_values
independence_method_values
external_source_references
benchmark_names
source_record_types
mapping_methods
source_files
source_file_hashes
source_group_ids
providers
model_names
model_versions
answer_extraction_methods
cross_provider_groups
cross_provider_roles
repeated_run_groups
repeated_run_roles
external_source_note
weights
thresholds
aggregate
source_summary
provider_summary
source_group_summary
cross_provider_summary
repeated_run_summary
run_stability_summary
results

Each trajectory result should include:

trajectory_id
source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
mapping_method
source_file
source_file_hash
source_group_id
provider
model_name
model_version
run_id
run_index
run_group_id
template_id
cross_provider_group
cross_provider_role
repeated_run_group
repeated_run_role
answer_extraction_method
source_record_reference
mapping_notes
response_id
question_id
variant_type
raw_question_hash
raw_output_hash
expected_answer
model_final_answer
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

v14 Warning Signals

v14 preserves the same five visible structural warning signals used by v3 through v13:

transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal

v14 adds repeated-run stability evidence.

Repeated-run evidence is not a replacement for the risk score.

It is an additional stability layer.


---

Risk Formula v14

The v14 risk score should preserve the v3 through v13 raw trajectory formula:

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

Initial structural thresholds:

risk_score < 0.25         -> STABLE
0.25 <= risk_score < 0.50 -> DRIFT
0.50 <= risk_score < 0.75 -> CRITICAL
risk_score >= 0.75        -> COLLAPSE

Gate actions:

STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP

Repeated-run stability thresholds:

risk_spread < 0.05             -> RUN_STABLE
0.05 <= risk_spread < 0.15     -> RUN_DRIFT
0.15 <= risk_spread < 0.30     -> RUN_UNSTABLE
risk_spread >= 0.30            -> RUN_COLLAPSE_LIKE

These thresholds are experimental.

They are not universal.

They must remain visible.


---

Correctness Profile

v14 should include a correctness profile for each trajectory:

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
run_stability is repeated-run structural evidence

Correctness and structural risk may correlate.

They are not the same measurement.


---

Extraction Profile

v14 should include an extraction profile for each trajectory:

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

Repeated-Run Stability Evidence

Each v14 repeated-run group should include:

repeated_run_group
provider
template_id
run_count
trajectory_ids
run_ids
risk_scores
risk_regimes
accuracy_rates
extraction_rates
risk_score_mean
risk_score_min
risk_score_max
risk_score_spread
accuracy_rate_mean
accuracy_rate_min
accuracy_rate_max
accuracy_rate_spread
extraction_rate_mean
extraction_rate_min
extraction_rate_max
extraction_rate_spread
risk_regime_set
risk_regime_flip
gate_action_set
gate_action_flip
run_stability_regime
highest_risk_run_id
highest_risk_trajectory
highest_risk_score
lowest_risk_run_id
lowest_risk_trajectory
lowest_risk_score

This exposes whether the same provider behaves structurally consistently across repeated runs.


---

Cross-Provider Stability Evidence

Each v14 cross-provider group should include:

cross_provider_group
template_ids
providers
repeated_run_groups
trajectory_ids
provider_risk_scores
provider_risk_regimes
provider_accuracy_rates
provider_extraction_rates
cross_provider_risk_spread
cross_provider_accuracy_spread
cross_provider_extraction_spread
risk_regime_disagreement
accuracy_disagreement
extraction_disagreement
run_stability_regimes
run_stability_disagreement
highest_risk_provider
highest_risk_trajectory
highest_risk_score
lowest_risk_provider
lowest_risk_trajectory
lowest_risk_score

This exposes whether provider disagreement itself remains stable across repeated runs.


---

Transition Evidence

Each v14 trajectory result should include:

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
source_file
source_file_hash
source_group_id
provider
model_name
model_version
run_id
run_index
run_group_id
template_id
cross_provider_group
cross_provider_role
repeated_run_group
repeated_run_role
answer_extraction_method

This is required because v14 tests repeated-run cross-provider stability.

A repeated-run-free v14 result is invalid.


---

Source Summary

Because v14 involves repeated-run cross-provider output files, the result must include a source summary.

The source summary should include:

source_file
trajectory_count
event_count
average_risk_score
average_accuracy_rate
average_extraction_rate
regime_counts
highest_risk_trajectory
highest_risk_score
sources
source_independences
independence_methods
external_source_references
benchmark_names
source_record_types
mapping_methods
source_files
source_file_hashes
source_group_ids
model_names
model_versions
providers
answer_extraction_methods
cross_provider_groups
cross_provider_roles
repeated_run_groups
repeated_run_roles

This exposes whether one source file, provider, model, run, extraction method, or record class produces systematically higher warning pressure.


---

Provider Summary

The provider summary should include:

provider
trajectory_count
event_count
average_risk_score
average_accuracy_rate
average_extraction_rate
regime_counts
highest_risk_trajectory
highest_risk_score
sources
source_independences
independence_methods
external_source_references
benchmark_names
source_record_types
mapping_methods
source_files
source_file_hashes
source_group_ids
model_names
model_versions
providers
answer_extraction_methods
cross_provider_groups
cross_provider_roles
repeated_run_groups
repeated_run_roles
run_stability_regimes

This exposes whether a provider is structurally stable or unstable across repeated runs.

Important boundary:

provider_summary is measurement evidence
provider_summary is not provider ranking


---

Minimal Aggregate Result

The aggregate section should include:

aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action
aggregate_accuracy_rate
aggregate_extraction_rate
aggregate_run_stability_regime
regime_counts
run_stability_regime_counts
highest_risk_trajectory
highest_risk_score
highest_risk_provider
highest_risk_run_id
source_count
independence_method_count
external_source_reference_count
benchmark_count
source_record_type_count
mapping_method_count
source_file_count
source_file_hash_count
source_group_count
provider_count
model_count
model_version_count
answer_extraction_method_count
cross_provider_group_count
repeated_run_group_count
run_group_count
trajectory_count
event_count

The aggregate must not hide individual trajectory results.


---

Reproducibility Requirements

A valid v14 experiment should include:

input JSONL file
validator script
output JSON
visible weights
visible thresholds
visible run-stability thresholds
per-trajectory evidence
correctness profiles
extraction profiles
source summary
provider summary
source-group summary
cross-provider summary
repeated-run summary
run-stability summary
aggregate result
source file references
source file hashes
negative cases
borderline cases
critical cases
collapse-like cases
repeated-run cases
cross-provider disagreement cases
verified source labels
source independence status
independence method
external source reference
benchmark name
source record type
source record reference
mapping method
mapping notes
provider
model name
model version
run id
run index
run group id
response id
raw question hash
raw output hash
answer extraction method
expected answer
model final answer
is_correct


---

Minimum Valid v14 Construction

A minimum valid v14 construction should include:

source: gsm_symbolic_repeated_run_cross_provider_stability_v14
source_independence: external_source_verified
independence_method: repeated_run_cross_provider_stability_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: repeated_run_cross_provider_real_model_output_file
mapping_method: repeated_run_cross_provider_stability_to_trajectory

It should include at least:

2 providers
2 repeated runs per provider
5 matched template groups
10 provider-template trajectory groups
20 repeated-run trajectory groups
50+ ordered events

Minimum trajectory families:

stable repeated-run group
drift repeated-run group
borderline repeated-run group
critical repeated-run group
collapse-like repeated-run group

Each trajectory must point to one or more repeated-run source-file records.


---

Safe Claim

Safe v14 claim:

OMNIA-VALIDATION Level 3 v14 applies the raw trajectory warning mechanism
to repeated-run cross-provider GSM-Symbolic model-output records mapped into
raw ordered structural trajectory events.

The validator measures structural warning risk using visible weights, visible
thresholds, source-file references, source-file hashes, provider identity,
model identity, run identity, repeated-run identity, answer-extraction fields,
correctness profiles, extraction profiles, cross-provider groups, repeated-run
groups, and inspectable transition evidence.


---

Claims to Avoid

Do not claim:

OMNIA predicts AI collapse universally.

Do not claim:

OMNIA detects semantic truth.

Do not claim:

Level 3 v14 is production-certified.

Do not claim:

The thresholds are universal.

Do not claim:

OMNIA solves GSM-Symbolic.

Do not claim:

v14 ranks providers objectively.

Do not claim:

Cross-provider disagreement means one provider is wrong.

Do not claim:

Repeated-run instability means semantic failure.

Do not claim:

Correct answer means structural stability.

Do not claim:

Wrong answer means structural collapse.

Do not claim:

Extraction failure automatically means collapse.

Correct boundary:

Level 3 v14 measures repeated-run structural stability over cross-provider
real parsed model-output records mapped into raw ordered trajectory events.


---

Validation Rule

v14 must not weaken the boundary.

If the input contains repeated-run cross-provider records, the result must state:

source_record_type: repeated_run_cross_provider_real_model_output_file
mapping_method: repeated_run_cross_provider_stability_to_trajectory

If the input contains cross-provider records but only one run, the result should remain v13.

If the input contains repeated runs but only one provider, it should not be called cross-provider v14.

If the input is bounded construction only, the result should remain explicitly bounded.

Boundary honesty is part of the result.


---

Planned Files

Concept document:

docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14.md

Input data:

data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl

Script:

examples/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.py

Result JSON:

results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json

Result document:

docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14_RESULT.md


---

Next Step

After this document, the next step is to create the repeated-run cross-provider JSONL file:

data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl

The v14 dataset must include repeated-run trace fields:

run_id
run_index
run_group_id
repeated_run_group
repeated_run_role
cross_provider_group
cross_provider_role
source_file
source_file_hash
source_record_reference
provider
model_name
model_version
response_id
raw_question_hash
raw_output_hash
answer_extraction_method
expected_answer
model_final_answer
is_correct

The v14 objective is not to claim provider superiority.

The v14 objective is to test whether the raw trajectory warning mechanism remains coherent when cross-provider disagreement is measured across repeated runs rather than a single cross-provider comparison.