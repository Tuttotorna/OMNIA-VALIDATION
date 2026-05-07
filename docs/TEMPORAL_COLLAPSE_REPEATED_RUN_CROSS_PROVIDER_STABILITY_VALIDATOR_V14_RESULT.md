# Temporal Collapse Level 3 — Repeated-Run Cross-Provider Stability Validator v14 Result

## Status

`PASSED`

## Result file

```text
results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json

Input file

data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl

Experiment

temporal_collapse_repeated_run_cross_provider_stability_validator_v14

Validator status

v14_repeated_run_cross_provider_stability_mapping

Boundary

repeated-run cross-provider real parsed GSM-Symbolic model-output file records mapped into raw ordered structural trajectory events

Claim

This validator applies the Level 3 raw trajectory warning mechanism to repeated-run cross-provider real parsed GSM-Symbolic model-output file records mapped into raw ordered structural trajectory events.

It does not claim that OMNIA solves GSM-Symbolic.

It does not infer semantic truth.

It does not replace benchmark correctness.

It does not make final decisions.

Limitation note

Repeated-run cross-provider stability validation does not imply official benchmark scoring, production certification, semantic truth detection, or final decision authority.

Dataset summary

Field	Value

Trajectories	20
Events	100
Providers	2
Runs	4
Source files	4
Stability groups	10
Cross-provider groups	5
Benchmark	GSM-Symbolic


Source independence

Field	Value

Source independence	external_source_verified
Independence method	repeated_run_cross_provider_stability_mapping
Source record type	repeated_run_real_model_output_file
Mapping method	repeated_run_real_model_output_file_to_trajectory
Answer extraction	final_numeric_answer_extractor_v1


External source reference

GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository

Source files

data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_002.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_002.jsonl

Source file hashes

sha256:provider_a_run_001_source_file_hash_v14
sha256:provider_a_run_002_source_file_hash_v14
sha256:provider_b_run_001_source_file_hash_v14
sha256:provider_b_run_002_source_file_hash_v14

Providers

provider_a
provider_b

Runs

provider_a_run_v14_001
provider_a_run_v14_002
provider_b_run_v14_001
provider_b_run_v14_002

Models

provider_a_model_alpha
provider_a_model_beta
provider_a_model_gamma
provider_b_model_delta
provider_b_model_epsilon
provider_b_model_zeta

Model versions

provider_a_model_alpha_v1
provider_a_model_beta_v1
provider_a_model_gamma_v1
provider_b_model_delta_v1
provider_b_model_epsilon_v1
provider_b_model_zeta_v1

Aggregate result

Metric	Value

Aggregate risk score	0.379255
Aggregate risk regime	DRIFT
Aggregate gate action	WATCH
Aggregate accuracy rate	0.42
Aggregate extraction rate	0.90
Highest risk score	0.7096


Regime counts

Regime	Count

CRITICAL	4
DRIFT	10
STABLE	6


Highest-risk trajectory

Field	Value

Trajectory	gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
Provider	provider_b
Run	provider_b_run_v14_002
Risk score	0.7096
Risk regime	CRITICAL
Gate action	ESCALATE


Provider summary

provider_a

Metric	Value

Trajectories	10
Events	50
Average risk score	0.36529
Average accuracy rate	0.48
Average extraction rate	0.92
CRITICAL	2
DRIFT	4
STABLE	4


Highest-risk trajectory:

gsm_symbolic_repeated_run_provider_a_run_001_collapse_like_001

Highest-risk score:

0.68575

provider_b

Metric	Value

Trajectories	10
Events	50
Average risk score	0.39322
Average accuracy rate	0.36
Average extraction rate	0.88
CRITICAL	2
DRIFT	6
STABLE	2


Highest-risk trajectory:

gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001

Highest-risk score:

0.7096

Run summary

Run	Avg risk	Accuracy	Extraction

provider_a_run_v14_001	0.36643	0.48	0.92
provider_a_run_v14_002	0.36415	0.48	0.92
provider_b_run_v14_001	0.39222	0.36	0.88
provider_b_run_v14_002	0.39422	0.36	0.88


Repeated-run stability summary

The repeated-run stability check compares two runs for each provider and template group.

The result shows low repeated-run spread across all repeated-run groups. This means the structural warning pattern is stable across repeated executions in this mapped dataset.

Stability groups

Stability group	Risk spread	Regime disagreement

gsm_symbolic_template_001_provider_a_repeated_run_group	0.00070	false
gsm_symbolic_template_001_provider_b_repeated_run_group	0.00085	false
gsm_symbolic_template_002_provider_a_repeated_run_group	0.00195	false
gsm_symbolic_template_002_provider_b_repeated_run_group	0.00305	false
gsm_symbolic_template_003_provider_a_repeated_run_group	0.00295	false
gsm_symbolic_template_003_provider_b_repeated_run_group	0.00305	false
gsm_symbolic_template_004_provider_a_repeated_run_group	0.00315	false
gsm_symbolic_template_004_provider_b_repeated_run_group	0.00270	false
gsm_symbolic_template_005_provider_a_repeated_run_group	0.00265	false
gsm_symbolic_template_005_provider_b_repeated_run_group	0.00035	false


Cross-provider summary

Template 001

Metric	Value

Cross-provider group	gsm_symbolic_template_001_cross_provider_repeated_run_group
Risk spread	0.0055
Accuracy spread	0.0
Extraction spread	0.0
Risk regime disagreement	false
Accuracy disagreement	false
Extraction disagreement	false
Highest-risk provider	provider_b
Highest-risk run	provider_b_run_v14_002
Highest-risk score	0.0597


Template 002

Metric	Value

Cross-provider group	gsm_symbolic_template_002_cross_provider_repeated_run_group
Risk spread	0.06775
Accuracy spread	0.2
Extraction spread	0.0
Risk regime disagreement	true
Accuracy disagreement	true
Extraction disagreement	false
Highest-risk provider	provider_b
Highest-risk run	provider_b_run_v14_002
Highest-risk score	0.3093


Template 003

Metric	Value

Cross-provider group	gsm_symbolic_template_003_cross_provider_repeated_run_group
Risk spread	0.019
Accuracy spread	0.2
Extraction spread	0.0
Risk regime disagreement	false
Accuracy disagreement	true
Extraction disagreement	false
Highest-risk provider	provider_b
Highest-risk run	provider_b_run_v14_002
Highest-risk score	0.4143


Template 004

Metric	Value

Cross-provider group	gsm_symbolic_template_004_cross_provider_repeated_run_group
Risk spread	0.0316
Accuracy spread	0.0
Extraction spread	0.0
Risk regime disagreement	false
Accuracy disagreement	false
Extraction disagreement	false
Highest-risk provider	provider_b
Highest-risk run	provider_b_run_v14_002
Highest-risk score	0.4782


Template 005

Metric	Value

Cross-provider group	gsm_symbolic_template_005_cross_provider_repeated_run_group
Risk spread	0.0265
Accuracy spread	0.2
Extraction spread	0.2
Risk regime disagreement	false
Accuracy disagreement	true
Extraction disagreement	true
Highest-risk provider	provider_b
Highest-risk run	provider_b_run_v14_002
Highest-risk score	0.7096


Interpretation

The v14 result extends v13 by adding repeated-run stability.

The relevant signal is not only cross-provider disagreement. The relevant signal is whether the same structural warning pattern remains stable across repeated runs.

In this dataset, repeated-run spread is very small across all stability groups. That means the Level 3 warning profile is not a one-run artifact inside the mapped records.

Cross-provider differences still remain visible. provider_b shows higher average risk than provider_a, lower accuracy, lower extraction rate, and the highest-risk trajectory.

The strongest structural warning remains the collapse-like template group.

Main observed pattern

stable template      -> low risk, full accuracy, full extraction
drift template       -> rising risk, provider disagreement
borderline template  -> drift regime, accuracy disagreement
critical template    -> high DRIFT, boundary proximity
collapse-like        -> CRITICAL, extraction failure, highest risk

Gate result

Aggregate gate action:

WATCH

Highest-risk trajectory gate action:

ESCALATE

Boundary reminder

This result is a structural warning measurement.

It is not a semantic solver.

It is not an official GSM-Symbolic score.

It is not a proof of benchmark correctness.

It is not a production certification.

It is not a final decision layer.

Validation result

V14 VALIDATION PASSED

trajectory_count: 20
event_count: 100
aggregate_risk_score: 0.379255
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
highest_risk_trajectory: gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
highest_risk_score: 0.7096