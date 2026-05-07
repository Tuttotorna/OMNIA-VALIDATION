# Temporal Collapse Cross-Provider Disagreement Validator — v13

## Purpose

This document defines the Level 3 v13 direction of OMNIA-VALIDATION.

Level 3 v12 validated multi-source real parsed GSM-Symbolic model-output file mappings.

Level 3 v13 moves one step further.

The objective is to move from:

```text
multi-source real parsed model-output file validation

to:

cross-provider disagreement-aware structural warning validation

measurement != inference != decision


---

Core Boundary

v13 must not claim that OMNIA solves GSM-Symbolic.

v13 must not claim semantic truth detection.

v13 must not replace official benchmark scoring.

v13 must not claim production certification.

v13 must not make final decisions.

v13 measures structural warning risk plus cross-provider disagreement pressure over real parsed model-output files mapped into raw ordered trajectory events.

Correct boundary:

Level 3 v13 maps multi-provider real parsed GSM-Symbolic model-output files
into raw ordered structural trajectory events and measures warning risk plus
cross-provider disagreement pressure.

Incorrect boundary:

Level 3 v13 proves which provider is correct.


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
v13 -> cross-provider disagreement-aware structural warning validation

The v13 transition is from:

multi_source_real_model_output_file_to_trajectory

to:

cross_provider_disagreement_to_structural_warning


---

What Changed from v12

v12 measured multi-source structural warning pressure.

v13 must explicitly measure disagreement between providers on the same template group.

v12 tracked:

provider
source_file
source_group_id
cross_source_group
cross_source_risk_spread
highest_risk_provider

v13 adds explicit disagreement fields:

cross_provider_answer_disagreement
cross_provider_correctness_disagreement
cross_provider_extraction_disagreement
cross_provider_regime_disagreement
cross_provider_risk_spread
provider_instability_index
disagreement_pressure

v12 asks:

Do multiple source files preserve coherent structural warning measurement?

v13 asks:

Does disagreement between providers become a measurable structural warning signal?


---

Core Question

Given multiple providers evaluated over comparable GSM-Symbolic template groups, can the Level 3 warning layer measure whether cross-provider disagreement increases structural warning pressure?

Target disagreement classes:

ANSWER_DISAGREEMENT
CORRECTNESS_DISAGREEMENT
EXTRACTION_DISAGREEMENT
REGIME_DISAGREEMENT
RISK_SPREAD
PROVIDER_INSTABILITY

Target regimes remain:

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

It is a measurement-derived warning signal for an external decision layer.


---

What v13 Does Not Claim

v13 does not claim:

GSM-Symbolic solving
semantic truth detection
official benchmark correctness replacement
provider ranking by truth
provider intelligence ranking
production certification
universal collapse prediction
final decision authority

Correct claim:

v13 measures structural warning risk and cross-provider disagreement pressure
over multi-provider real parsed GSM-Symbolic model-output file mappings.

Incorrect claim:

v13 proves which provider understands the problem.


---

Required Source Boundary

Recommended source independence:

external_source_verified

Recommended independence method:

cross_provider_real_model_output_file_mapping

Recommended source record type:

cross_provider_real_model_output_file

Recommended mapping method:

cross_provider_disagreement_to_structural_warning

Recommended boundary:

source: gsm_symbolic_cross_provider_disagreement_v13
source_independence: external_source_verified
independence_method: cross_provider_real_model_output_file_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: cross_provider_real_model_output_file
mapping_method: cross_provider_disagreement_to_structural_warning

Alternative valid source record types:

cross_provider_real_model_output_file
cross_provider_answer_trace
cross_provider_extraction_trace
cross_model_response_jsonl
multi_provider_benchmark_run_file

Alternative valid mapping methods:

cross_provider_disagreement_to_structural_warning
cross_provider_answer_trace_to_structural_warning
cross_provider_extraction_trace_to_structural_warning
cross_model_response_jsonl_to_structural_warning
multi_provider_benchmark_run_file_to_structural_warning

If the file only contains one provider, it is not v13.

If the file has multiple providers but no same-template comparison, it should remain v12.


---

Required Record Fields

Each v13 event should preserve source identity, provider identity, answer identity, extraction identity, trajectory identity, and cross-provider grouping identity.

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
response_id
source_file
source_file_hash
source_group_id
cross_provider_group
cross_provider_role
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

Required cross-provider group fields:

cross_provider_group
cross_provider_role
provider
model_name
model_version
template_id
expected_answer
model_final_answer
is_correct
answer_extraction_method
risk_score
risk_regime
gate_action

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
  "trajectory_id": "gsm_symbolic_cross_provider_provider_a_template_001",
  "step": 1,
  "template_id": "gsm_symbolic_template_001",
  "question_id": "gsm_symbolic_template_001_base",
  "variant_type": "base",
  "provider": "provider_a",
  "model_name": "provider_a_model_alpha",
  "model_version": "provider_a_model_alpha_v1",
  "run_id": "provider_a_run_v13_001",
  "response_id": "provider_a_response_001_01",
  "source_file": "data/source_outputs/gsm_symbolic_real_model_outputs_v13_provider_a.jsonl",
  "source_file_hash": "sha256:provider_a_source_file_hash_v13",
  "source_group_id": "provider_a_reference_group",
  "cross_provider_group": "gsm_symbolic_template_001_cross_provider_group",
  "cross_provider_role": "provider_a_member",
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
  "source": "gsm_symbolic_cross_provider_disagreement_v13",
  "source_independence": "external_source_verified",
  "independence_method": "cross_provider_real_model_output_file_mapping",
  "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
  "benchmark_name": "GSM-Symbolic",
  "source_record_type": "cross_provider_real_model_output_file",
  "source_record_reference": "data/source_outputs/gsm_symbolic_real_model_outputs_v13_provider_a.jsonl#provider_a_response_001_01",
  "mapping_method": "cross_provider_disagreement_to_structural_warning",
  "mapping_notes": "provider record mapped into cross-provider disagreement-aware structural trajectory event"
}


---

Input Format

Preferred input format:

JSONL

Planned input file:

data/temporal_collapse_cross_provider_disagreement_v13.jsonl

Each line must contain one event parsed from a provider-specific real model-output file or answer-extraction trace.

Each event must belong to a cross-provider group.


---

Source File Requirement

v13 must include source-file fields.

Required:

source_file
source_file_hash
source_record_reference
source_group_id
cross_provider_group
cross_provider_role
provider

This is the main difference from v11 and v12.

v11 had one real parsed source file.

v12 had multiple sources and providers.

v13 must explicitly compare providers inside aligned cross-provider groups.

A v13 result without cross_provider_group is structurally incomplete.


---

Output Format

Planned output file:

results/temporal_collapse_cross_provider_disagreement_validator_v13.json

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
external_source_note
weights
thresholds
aggregate
source_summary
provider_summary
source_group_summary
cross_provider_summary
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
source_file
source_file_hash
source_group_id
provider
model_name
model_version
run_id
response_id
template_id
question_id
variant_type
cross_provider_group
cross_provider_role
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

Each cross-provider group summary should include:

cross_provider_group
template_ids
providers
trajectory_ids
provider_risk_scores
provider_risk_regimes
provider_accuracy_rates
provider_extraction_rates
provider_final_answers
provider_correctness_values
provider_extraction_values
cross_provider_risk_spread
cross_provider_regime_disagreement
cross_provider_answer_disagreement
cross_provider_correctness_disagreement
cross_provider_extraction_disagreement
provider_instability_index
disagreement_pressure
highest_risk_provider
highest_risk_trajectory
highest_risk_score


---

v13 Warning Signals

v13 preserves the five visible signals used by v3 through v12:

transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal

v13 adds disagreement signals:

risk_spread_signal
regime_disagreement_signal
answer_disagreement_signal
correctness_disagreement_signal
extraction_disagreement_signal
provider_instability_signal

Changing the base raw trajectory formula would weaken comparability.

The disagreement layer should be additive and visible.


---

Base Risk Formula v13

The base trajectory risk score should preserve the v3 through v12 raw trajectory formula:

base_risk_score =
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

Disagreement Pressure Formula v13

Recommended disagreement pressure:

disagreement_pressure =
    0.25 * risk_spread_signal
  + 0.20 * regime_disagreement_signal
  + 0.20 * answer_disagreement_signal
  + 0.15 * correctness_disagreement_signal
  + 0.10 * extraction_disagreement_signal
  + 0.10 * provider_instability_signal

Recommended disagreement weights:

{
  "risk_spread_signal": 0.25,
  "regime_disagreement_signal": 0.2,
  "answer_disagreement_signal": 0.2,
  "correctness_disagreement_signal": 0.15,
  "extraction_disagreement_signal": 0.1,
  "provider_instability_signal": 0.1
}

The disagreement pressure is not a semantic truth score.

It is a structural disagreement measurement.


---

Combined Risk Formula v13

Recommended combined warning score:

combined_risk_score =
    0.75 * base_risk_score
  + 0.25 * disagreement_pressure

Recommended combined weights:

{
  "base_risk_score": 0.75,
  "disagreement_pressure": 0.25
}

Reason:

base structural risk remains dominant
cross-provider disagreement adds warning pressure

The combined score is experimental.

It is not universal.

It must remain visible.


---

Disagreement Signal Definitions

Risk Spread Signal

risk_spread_signal = max(provider_risk_scores) - min(provider_risk_scores)

Clamped range:

0.0 <= risk_spread_signal <= 1.0


---

Regime Disagreement Signal

regime_disagreement_signal = 0 if all providers share the same risk_regime
regime_disagreement_signal = 1 if at least two providers have different risk_regime values

Example:

provider_a -> DRIFT
provider_b -> CRITICAL

regime_disagreement_signal = 1


---

Answer Disagreement Signal

answer_disagreement_signal = 0 if all extracted model_final_answer values match
answer_disagreement_signal = 1 if extracted model_final_answer values differ

If at least one answer is not_extracted, extraction disagreement should also be measured separately.


---

Correctness Disagreement Signal

correctness_disagreement_signal = 0 if all providers share the same correctness state
correctness_disagreement_signal = 1 if correctness differs across providers

Example:

provider_a -> is_correct true
provider_b -> is_correct false

correctness_disagreement_signal = 1


---

Extraction Disagreement Signal

extraction_disagreement_signal = 0 if all providers share the same extraction state
extraction_disagreement_signal = 1 if extraction state differs across providers

Extraction state:

extracted
not_extracted


---

Provider Instability Signal

Recommended simple form:

provider_instability_signal =
    average of normalized provider-to-provider changes across:
      risk_regime
      correctness
      extraction
      final_answer

Minimal bounded form:

provider_instability_signal =
    mean(
      regime_disagreement_signal,
      answer_disagreement_signal,
      correctness_disagreement_signal,
      extraction_disagreement_signal
    )


---

Classification Thresholds

Initial thresholds for combined risk:

combined_risk_score < 0.25         -> STABLE
0.25 <= combined_risk_score < 0.50 -> DRIFT
0.50 <= combined_risk_score < 0.75 -> CRITICAL
combined_risk_score >= 0.75        -> COLLAPSE

Gate actions:

STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP

Thresholds are experimental and must remain visible.


---

Correctness Profile

v13 should include a correctness profile for each trajectory:

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
disagreement_pressure is structural disagreement measurement

Correctness and structural risk may correlate.

They are not the same measurement.


---

Extraction Profile

v13 should include an extraction profile for each trajectory:

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

Cross-Provider Profile

v13 should include a cross-provider profile for each aligned group:

{
  "cross_provider_group": "gsm_symbolic_template_004_cross_provider_group",
  "providers": [
    "provider_a",
    "provider_b"
  ],
  "provider_risk_scores": {
    "provider_a": 0.457396,
    "provider_b": 0.576583
  },
  "provider_risk_regimes": {
    "provider_a": "DRIFT",
    "provider_b": "CRITICAL"
  },
  "provider_accuracy_rates": {
    "provider_a": 0.2,
    "provider_b": 0.2
  },
  "provider_extraction_rates": {
    "provider_a": 1.0,
    "provider_b": 1.0
  },
  "cross_provider_risk_spread": 0.119187,
  "cross_provider_regime_disagreement": true,
  "cross_provider_answer_disagreement": true,
  "cross_provider_correctness_disagreement": false,
  "cross_provider_extraction_disagreement": false,
  "provider_instability_index": 0.5,
  "disagreement_pressure": 0.424797
}

This profile is central to v13.

Without it, the result remains v12.


---

Transition Evidence

Each v13 trajectory result should include:

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
response_id
template_id
question_id
variant_type
cross_provider_group
cross_provider_role
raw_question_hash
raw_output_hash
answer_extraction_method

This is required because v13 tests provider disagreement over real parsed model-output file mappings.


---

Source Summary

Because v13 involves multiple real parsed output files, the result must include a source summary.

The source summary should include:

source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
mapping_method
source_file
source_file_hash
source_group_ids
providers
model_names
model_versions
answer_extraction_methods
trajectory_count
event_count
average_base_risk_score
average_combined_risk_score
average_disagreement_pressure
average_accuracy_rate
average_extraction_rate
regime_counts
highest_risk_trajectory
highest_risk_score


---

Provider Summary

v13 must include provider summary.

The provider summary should include:

provider
trajectory_count
event_count
average_base_risk_score
average_combined_risk_score
average_accuracy_rate
average_extraction_rate
average_disagreement_pressure
regime_counts
highest_risk_trajectory
highest_risk_score
sources
source_files
source_file_hashes
source_group_ids
model_names
model_versions
answer_extraction_methods
cross_provider_groups
cross_provider_roles


---

Cross-Provider Summary

v13 must include cross-provider summary.

The cross-provider summary should include:

cross_provider_group
template_ids
providers
trajectory_ids
provider_risk_scores
provider_combined_risk_scores
provider_risk_regimes
provider_accuracy_rates
provider_extraction_rates
provider_final_answers
provider_correctness_values
provider_extraction_values
cross_provider_risk_spread
cross_provider_regime_disagreement
cross_provider_answer_disagreement
cross_provider_correctness_disagreement
cross_provider_extraction_disagreement
provider_instability_index
disagreement_pressure
highest_risk_provider
highest_risk_trajectory
highest_risk_score

This exposes whether providers diverge structurally under the same template group.


---

Minimal Aggregate Result

The aggregate section should include:

aggregate_base_risk_score
aggregate_disagreement_pressure
aggregate_combined_risk_score
aggregate_risk_regime
aggregate_gate_action
aggregate_accuracy_rate
aggregate_extraction_rate
regime_counts
highest_risk_trajectory
highest_risk_score
highest_risk_provider
highest_disagreement_group
highest_disagreement_pressure
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
trajectory_count
event_count

The aggregate must not hide individual trajectory results.


---

Reproducibility Requirements

A valid v13 experiment should include:

input JSONL file
validator script
output JSON
visible base weights
visible disagreement weights
visible combined weights
visible thresholds
per-trajectory evidence
correctness profiles
extraction profiles
source summary
provider summary
source-group summary
cross-provider summary
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
cross_provider_group
cross_provider_role
cross_provider_risk_spread
cross_provider_regime_disagreement
cross_provider_answer_disagreement
cross_provider_correctness_disagreement
cross_provider_extraction_disagreement
provider_instability_index
disagreement_pressure


---

Minimum Valid v13 Construction

A minimum valid v13 construction should include:

source: gsm_symbolic_cross_provider_disagreement_v13
source_independence: external_source_verified
independence_method: cross_provider_real_model_output_file_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: cross_provider_real_model_output_file
mapping_method: cross_provider_disagreement_to_structural_warning

It should include at least two providers:

provider_a
provider_b

It should include at least five cross-provider groups:

stable cross-provider group
drift cross-provider group
borderline critical cross-provider group
critical cross-provider group
collapse-like cross-provider group

Each cross-provider group must contain comparable provider trajectories.


---

Safe Claim

Safe v13 claim:

OMNIA-VALIDATION Level 3 v13 applies the raw trajectory warning mechanism
to cross-provider real parsed GSM-Symbolic model-output file records mapped
into raw ordered structural trajectory events.

The validator measures base structural warning risk and cross-provider
disagreement pressure using visible weights, visible thresholds,
source-file references, source-file hashes, provider identities, model-output
fields, answer-extraction fields, correctness profiles, extraction profiles,
cross-provider groups, and inspectable transition evidence.


---

Claims to Avoid

Do not claim:

OMNIA predicts AI collapse universally.

Do not claim:

OMNIA detects semantic truth.

Do not claim:

Level 3 v13 is production-certified.

Do not claim:

The thresholds are universal.

Do not claim:

OMNIA solves GSM-Symbolic.

Do not claim:

Provider disagreement proves which provider is wrong.

Do not claim:

Structural warning risk equals benchmark correctness.

Do not claim:

Correct answer means structural stability.

Do not claim:

Wrong answer means structural collapse.

Do not claim:

Extraction failure automatically means collapse.

Correct boundary:

Level 3 v13 measures structural warning risk and cross-provider disagreement
pressure over real parsed model-output files mapped into raw ordered trajectory
events.


---

Validation Rule

v13 must not weaken the boundary.

If the input comes from multiple provider source files, the result must state:

source_record_type: cross_provider_real_model_output_file
mapping_method: cross_provider_disagreement_to_structural_warning

If the input comes from cross-provider answer traces, the result must state:

source_record_type: cross_provider_answer_trace
mapping_method: cross_provider_answer_trace_to_structural_warning

If the input comes from cross-provider extraction traces, the result must state:

source_record_type: cross_provider_extraction_trace
mapping_method: cross_provider_extraction_trace_to_structural_warning

If the input lacks aligned provider groups, the result should remain v12, not v13.

Boundary honesty is part of the result.


---

Planned Files

Concept document:

docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13.md

Provider source files:

data/source_outputs/gsm_symbolic_real_model_outputs_v13_provider_a.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v13_provider_b.jsonl

Input data:

data/temporal_collapse_cross_provider_disagreement_v13.jsonl

Script:

examples/temporal_collapse_cross_provider_disagreement_validator_v13.py

Result JSON:

results/temporal_collapse_cross_provider_disagreement_validator_v13.json

Result document:

docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13_RESULT.md


---

Next Step

After this document, the next step is to create the cross-provider disagreement JSONL file:

data/temporal_collapse_cross_provider_disagreement_v13.jsonl

The v13 dataset must include cross-provider trace fields:

source_file
source_file_hash
source_group_id
provider
model_name
model_version
run_id
response_id
template_id
question_id
variant_type
expected_answer
model_final_answer
is_correct
answer_extraction_method
cross_provider_group
cross_provider_role
raw_question_hash
raw_output_hash

The v13 objective is not to claim benchmark solving.

The v13 objective is to test whether disagreement between providers becomes a measurable structural warning signal.

measurement != inference != decision