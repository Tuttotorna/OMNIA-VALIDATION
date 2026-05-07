# Temporal Collapse Real GSM-Symbolic Model Output Validator — v11 Result

## Result Status

The v11 validation passed.

```text
V11 VALIDATION PASSED
RETURN CODE: 0
STDERR: empty
BOUNDARY ASSERTIONS: OK
AGGREGATE ASSERTIONS: OK
RESULTS COUNT: 5

Boundary

measurement != inference != decision

v11 measures structural warning risk over real parsed GSM-Symbolic model-output file records mapped into raw ordered structural trajectory events.

It does not claim that OMNIA solves GSM-Symbolic.

It does not infer semantic truth.

It does not replace official benchmark scoring.

It does not provide production certification.

Validated Files

data/source_outputs/gsm_symbolic_real_model_outputs_v11_reference.jsonl
data/temporal_collapse_real_gsm_symbolic_model_outputs_v11.jsonl
examples/temporal_collapse_real_gsm_symbolic_model_output_validator_v11.py
results/temporal_collapse_real_gsm_symbolic_model_output_validator_v11.json

Source File Check

Source file:

data/source_outputs/gsm_symbolic_real_model_outputs_v11_reference.jsonl

Source record count:

25

First source response:

real_response_stable_001_01

Last source response:

real_response_collapse_001_05

Mapped Dataset Check

Mapped dataset:

data/temporal_collapse_real_gsm_symbolic_model_outputs_v11.jsonl

Mapped record count:

25

Trajectory count:

5

Each trajectory contains five ordered steps.

step 1
step 2
step 3
step 4
step 5

Trajectories

gsm_symbolic_real_output_stable_001
gsm_symbolic_real_output_drift_001
gsm_symbolic_real_output_borderline_critical_001
gsm_symbolic_real_output_critical_001
gsm_symbolic_real_output_collapse_like_001

Boundary Assertions

The v11 Colab validation confirmed:

source_independence_values: external_source_verified
independence_method_values: real_model_output_file_mapping
benchmark_names: GSM-Symbolic
source_record_types: real_model_output_file
mapping_methods: real_model_output_file_to_trajectory
source_files: data/source_outputs/gsm_symbolic_real_model_outputs_v11_reference.jsonl
source_file_hashes: sha256:reference_source_file_hash_v11
providers: reference_provider
answer_extraction_methods: final_numeric_answer_extractor_v1

Aggregate Result

aggregate_risk_score: 0.37472
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.48
aggregate_extraction_rate: 0.92

Regime counts:

CRITICAL: 1
DRIFT: 2
STABLE: 2

Highest-risk trajectory:

gsm_symbolic_real_output_collapse_like_001

Highest-risk score:

0.665825

Source Summary

reference_model_a

model_version: reference_model_a_v1
provider: reference_provider
trajectory_count: 2
average_risk_score: 0.151325
average_accuracy_rate: 0.8
average_extraction_rate: 1.0
regime_counts: STABLE=2
highest_risk_trajectory: gsm_symbolic_real_output_drift_001
highest_risk_score: 0.249467

reference_model_b

model_version: reference_model_b_v1
provider: reference_provider
trajectory_count: 2
average_risk_score: 0.452562
average_accuracy_rate: 0.3
average_extraction_rate: 1.0
regime_counts: DRIFT=2
highest_risk_trajectory: gsm_symbolic_real_output_critical_001
highest_risk_score: 0.480217

reference_model_c

model_version: reference_model_c_v1
provider: reference_provider
trajectory_count: 1
average_risk_score: 0.665825
average_accuracy_rate: 0.2
average_extraction_rate: 0.6
regime_counts: CRITICAL=1
highest_risk_trajectory: gsm_symbolic_real_output_collapse_like_001
highest_risk_score: 0.665825

Per-Trajectory Result Summary

gsm_symbolic_real_output_stable_001

risk_regime: STABLE
risk_score: 0.053182
gate_action: PASS
accuracy_rate: 1.0
extraction_rate: 1.0

gsm_symbolic_real_output_drift_001

risk_regime: STABLE
risk_score: 0.249467
gate_action: PASS
accuracy_rate: 0.6
extraction_rate: 1.0

This trajectory remains just below the DRIFT threshold.

gsm_symbolic_real_output_borderline_critical_001

risk_regime: DRIFT
risk_score: 0.424908
gate_action: WATCH
accuracy_rate: 0.4
extraction_rate: 1.0

gsm_symbolic_real_output_critical_001

risk_regime: DRIFT
risk_score: 0.480217
gate_action: WATCH
accuracy_rate: 0.2
extraction_rate: 1.0

This trajectory is close to the CRITICAL threshold but remains classified as DRIFT under the current visible thresholds.

gsm_symbolic_real_output_collapse_like_001

risk_regime: CRITICAL
risk_score: 0.665825
gate_action: ESCALATE
accuracy_rate: 0.2
extraction_rate: 0.6

This is the highest-risk trajectory in v11.

It contains collapse-like evidence, including broken/not-extracted signatures, but its final risk score remains below the COLLAPSE threshold under the current visible weights and thresholds.

Weights

transition_density: 0.2
drift_progression: 0.2
boundary_proximity: 0.25
collapse_similarity: 0.25
irreversibility_signal: 0.1

Thresholds

risk_score < 0.25         -> STABLE
0.25 <= risk_score < 0.50 -> DRIFT
0.50 <= risk_score < 0.75 -> CRITICAL
risk_score >= 0.75        -> COLLAPSE

Interpretation

v11 confirms that the Level 3 Temporal Collapse warning mechanism can process real parsed GSM-Symbolic model-output file records as ordered structural trajectories.

The result is a structural warning measurement.

It is not semantic scoring.

It is not benchmark scoring.

It is not a solver claim.

Safe Claim

OMNIA-VALIDATION Level 3 v11 applies the raw trajectory warning mechanism
to real parsed GSM-Symbolic model-output file records mapped into ordered
structural trajectory events.

The validator reports structural warning risk using visible weights,
visible thresholds, source-file references, source-file hashes, model-output
fields, answer-extraction fields, correctness profiles, extraction profiles,
source summaries, aggregate results, and per-trajectory transition evidence.

Final Status

v11 complete
validated in fresh Colab
result JSON generated
boundary assertions passed
aggregate assertions passed