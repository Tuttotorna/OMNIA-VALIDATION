# Temporal Collapse Multi-Source Real GSM-Symbolic Model Output Validator — v12 Result

## Purpose

This document records the result of the Level 3 v12 validator of OMNIA-VALIDATION.

Level 3 v11 validated real parsed GSM-Symbolic model-output file records mapped into raw ordered structural trajectory events.

Level 3 v12 moves one step further.

The objective is to move from:

```text
single-source real parsed model-output file validation

to:

multi-source real parsed model-output file validation

measurement != inference != decision


---

Core Boundary

v12 does not claim that OMNIA solves GSM-Symbolic.

v12 does not infer semantic truth.

v12 does not replace benchmark correctness.

v12 does not certify production readiness.

v12 does not make final decisions.

v12 applies the Level 3 raw trajectory warning mechanism to multi-source real parsed GSM-Symbolic model-output file records mapped into raw ordered structural trajectory events.

Correct boundary:

Level 3 v12 measures structural warning risk over multi-source real parsed
GSM-Symbolic model-output file records mapped into raw ordered trajectory events.

Incorrect boundary:

Level 3 v12 proves that OMNIA solves GSM-Symbolic.


---

Files

Input source files:

data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_a.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_b.jsonl

Mapped dataset:

data/temporal_collapse_multi_source_real_gsm_symbolic_model_outputs_v12.jsonl

Validator:

examples/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.py

Result JSON:

results/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.json

Result document:

docs/TEMPORAL_COLLAPSE_MULTI_SOURCE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V12_RESULT.md


---

Validation Status

PASS

Final status from the validator:

V12 VALIDATION PASSED
RETURN CODE: 0
STDERR: empty
BOUNDARY ASSERTIONS: OK
AGGREGATE ASSERTIONS: OK
RESULTS COUNT: 10
EVENT COUNT: 50


---

Dataset Scope

The v12 mapped dataset contains:

source files:          2
providers:             2
source groups:         2
cross-source groups:   5
trajectories:          10
events:                50
records per provider:  25
events per trajectory: 5

Providers:

provider_a
provider_b

Source files:

data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_a.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_b.jsonl

Source file hashes:

sha256:provider_a_source_file_hash_v12
sha256:provider_b_source_file_hash_v12


---

Boundary Values

The validator preserved the required v12 boundary values:

source_independence:       external_source_verified
independence_method:       multi_source_real_model_output_file_mapping
benchmark_name:            GSM-Symbolic
source_record_type:        multi_source_real_model_output_file
mapping_method:            multi_source_real_model_output_file_to_trajectory
answer_extraction_method:  final_numeric_answer_extractor_v1

External source reference:

GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository

Important limitation:

Multi-source real parsed model-output file validation does not imply official
benchmark scoring, production certification, or semantic truth detection.


---

Level 3 v12 Transition

The Level 3 progression is now:

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

The v12 transition is from:

real_model_output_file_to_trajectory

to:

multi_source_real_model_output_file_to_trajectory


---

Risk Formula

v12 preserves the same raw ordered trajectory warning formula used by the previous Level 3 raw trajectory validators:

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

They are kept visible for inspection.


---

Classification Thresholds

Current thresholds:

risk_score < 0.25         -> STABLE
0.25 <= risk_score < 0.50 -> DRIFT
0.50 <= risk_score < 0.75 -> CRITICAL
risk_score >= 0.75        -> COLLAPSE

Gate actions:

STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP

The gate action is not a final decision.

It is a measurement-derived warning for an external decision layer.


---

Aggregate Result

Aggregate result:

aggregate_risk_score:       0.395512
aggregate_risk_regime:      DRIFT
aggregate_gate_action:      WATCH
aggregate_accuracy_rate:    0.42
aggregate_extraction_rate:  0.90
highest_risk_trajectory:    gsm_symbolic_multi_source_provider_b_collapse_like_001
highest_risk_score:         0.676146
highest_risk_provider:      provider_b

Regime counts:

STABLE   -> 3
DRIFT    -> 4
CRITICAL -> 3
COLLAPSE -> 0

Structural reading:

The aggregate system state is DRIFT.

The correct aggregate gate action is WATCH.

The highest-risk trajectory is provider_b collapse-like trajectory, but it remains
inside CRITICAL under the current visible thresholds.


---

Source Summary

Provider A Source File

source_file:              data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_a.jsonl
source_file_hash:         sha256:provider_a_source_file_hash_v12
provider:                 provider_a
source_group_id:          provider_a_reference_group
trajectory_count:         5
event_count:              25
average_risk_score:       0.362224
average_accuracy_rate:    0.48
average_extraction_rate:  0.92
highest_risk_trajectory:  gsm_symbolic_multi_source_provider_a_collapse_like_001
highest_risk_score:       0.661854

Regime counts:

STABLE   -> 2
DRIFT    -> 2
CRITICAL -> 1

Models:

provider_a_model_alpha
provider_a_model_beta
provider_a_model_gamma

Model versions:

provider_a_model_alpha_v1
provider_a_model_beta_v1
provider_a_model_gamma_v1


---

Provider B Source File

source_file:              data/source_outputs/gsm_symbolic_real_model_outputs_v12_provider_b.jsonl
source_file_hash:         sha256:provider_b_source_file_hash_v12
provider:                 provider_b
source_group_id:          provider_b_reference_group
trajectory_count:         5
event_count:              25
average_risk_score:       0.428800
average_accuracy_rate:    0.36
average_extraction_rate:  0.88
highest_risk_trajectory:  gsm_symbolic_multi_source_provider_b_collapse_like_001
highest_risk_score:       0.676146

Regime counts:

STABLE   -> 1
DRIFT    -> 2
CRITICAL -> 2

Models:

provider_b_model_delta
provider_b_model_epsilon
provider_b_model_zeta

Model versions:

provider_b_model_delta_v1
provider_b_model_epsilon_v1
provider_b_model_zeta_v1


---

Provider Comparison

Provider-level summary:

provider_a -> average risk 0.362224 -> accuracy 0.48 -> extraction 0.92
provider_b -> average risk 0.428800 -> accuracy 0.36 -> extraction 0.88

Structural reading:

provider_b shows higher average structural warning risk than provider_a.

provider_b also shows lower average correctness and lower average extraction rate.

This is evidence only.

It does not prove semantic inferiority.

It indicates higher structural warning pressure under the v12 measurement.


---

Cross-Source Summary

Template 001 Cross-Source Group

cross_source_group:       gsm_symbolic_template_001_cross_source_group
provider_a risk:          0.053975 -> STABLE
provider_b risk:          0.059187 -> STABLE
risk spread:              0.005212
highest risk provider:    provider_b
highest risk trajectory:  gsm_symbolic_multi_source_provider_b_stable_001

Reading:

Both providers remain structurally stable on template 001.


---

Template 002 Cross-Source Group

cross_source_group:       gsm_symbolic_template_002_cross_source_group
provider_a risk:          0.238417 -> STABLE
provider_b risk:          0.362667 -> DRIFT
risk spread:              0.124250
highest risk provider:    provider_b
highest risk trajectory:  gsm_symbolic_multi_source_provider_b_drift_001

Reading:

Template 002 separates the providers structurally.

provider_a remains STABLE.

provider_b enters DRIFT.


---

Template 003 Cross-Source Group

cross_source_group:       gsm_symbolic_template_003_cross_source_group
provider_a risk:          0.399479 -> DRIFT
provider_b risk:          0.469417 -> DRIFT
risk spread:              0.069938
highest risk provider:    provider_b
highest risk trajectory:  gsm_symbolic_multi_source_provider_b_borderline_critical_001

Reading:

Both providers are in DRIFT.

provider_b remains structurally more pressured.


---

Template 004 Cross-Source Group

cross_source_group:       gsm_symbolic_template_004_cross_source_group
provider_a risk:          0.457396 -> DRIFT
provider_b risk:          0.576583 -> CRITICAL
risk spread:              0.119187
highest risk provider:    provider_b
highest risk trajectory:  gsm_symbolic_multi_source_provider_b_critical_001

Reading:

Template 004 separates the providers again.

provider_a remains DRIFT.

provider_b crosses into CRITICAL.


---

Template 005 Cross-Source Group

cross_source_group:       gsm_symbolic_template_005_cross_source_group
provider_a risk:          0.661854 -> CRITICAL
provider_b risk:          0.676146 -> CRITICAL
risk spread:              0.014292
highest risk provider:    provider_b
highest risk trajectory:  gsm_symbolic_multi_source_provider_b_collapse_like_001

Reading:

Both providers reach CRITICAL on template 005.

The spread is small.

The structural pressure is shared across sources.


---

Trajectory Results

Highest Risk

trajectory_id:       gsm_symbolic_multi_source_provider_b_collapse_like_001
provider:            provider_b
risk_score:          0.676146
risk_regime:         CRITICAL
gate_action:         ESCALATE
dominant_axis:       boundary_proximity
accuracy_rate:       0.00
extraction_rate:     0.40

Signals:

transition_density:       0.400000
drift_progression:        0.516666
boundary_proximity:       0.990000
collapse_similarity:      0.589250
irreversibility_signal:   0.980000

Warning flags:

high_drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal

Reading:

This is the strongest v12 warning trajectory.

It is CRITICAL, not COLLAPSE, under the current thresholds.

The main pressure comes from boundary proximity, irreversibility signal,
collapse similarity, and drift progression.


---

Provider A Collapse-Like Trajectory

trajectory_id:       gsm_symbolic_multi_source_provider_a_collapse_like_001
provider:            provider_a
risk_score:          0.661854
risk_regime:         CRITICAL
gate_action:         ESCALATE
dominant_axis:       boundary_proximity
accuracy_rate:       0.20
extraction_rate:     0.60

Reading:

provider_a also reaches CRITICAL on the collapse-like trajectory.

The warning is strong, but still below the COLLAPSE threshold.


---

Provider B Critical Trajectory

trajectory_id:       gsm_symbolic_multi_source_provider_b_critical_001
provider:            provider_b
risk_score:          0.576583
risk_regime:         CRITICAL
gate_action:         ESCALATE
dominant_axis:       boundary_proximity
accuracy_rate:       0.20
extraction_rate:     1.00

Reading:

provider_b crosses into CRITICAL on template 004.

This is a cross-source separation point because provider_a remains DRIFT on
the corresponding trajectory.


---

Provider A Critical Trajectory

trajectory_id:       gsm_symbolic_multi_source_provider_a_critical_001
provider:            provider_a
risk_score:          0.457396
risk_regime:         DRIFT
gate_action:         WATCH
dominant_axis:       boundary_proximity
accuracy_rate:       0.20
extraction_rate:     1.00

Reading:

provider_a shows warning pressure but does not cross the CRITICAL threshold
on template 004.


---

Stable Trajectories

gsm_symbolic_multi_source_provider_a_stable_001 -> 0.053975 -> STABLE -> PASS
gsm_symbolic_multi_source_provider_b_stable_001 -> 0.059187 -> STABLE -> PASS

Reading:

Both providers remain stable on the stable template group.

This matters because the validator does not classify every trajectory as risky.


---

Correctness Profile

Aggregate correctness:

aggregate_accuracy_rate: 0.42

Provider correctness:

provider_a accuracy: 0.48
provider_b accuracy: 0.36

Important boundary:

correctness_profile is evidence
risk_score is structural warning measurement

Correctness and structural risk may correlate.

They are not the same measurement.

Correct answer does not automatically mean structural stability.

Wrong answer does not automatically mean structural collapse.


---

Extraction Profile

Aggregate extraction:

aggregate_extraction_rate: 0.90

Provider extraction:

provider_a extraction: 0.92
provider_b extraction: 0.88

Important boundary:

extraction_profile is evidence
risk_score is structural warning measurement

Extraction failure is evidence.

It is not automatically collapse.


---

What v12 Adds Over v11

v11 validated:

single-source real parsed model-output file mapping

v12 validates:

multi-source real parsed model-output file mapping

v12 adds:

provider comparison
source group comparison
cross-source group comparison
multi-source aggregate
highest-risk provider tracking
source-file count greater than one
provider count greater than one
model count greater than one
model-version count greater than one
cross-source risk spread

This is stronger than v11 because the result is no longer limited to one source file.


---

Structural Reading

v12 shows that the Level 3 raw trajectory warning mechanism remains coherent when applied to two source files, two providers, six model identities, five cross-source template groups, ten trajectories, and fifty ordered events.

The validator separates:

STABLE
DRIFT
CRITICAL

No trajectory reaches COLLAPSE under the current thresholds.

The highest-risk cases are still below 0.75.

Therefore the correct structural reading is:

multi-source DRIFT aggregate
with provider_b showing stronger CRITICAL pressure on the highest-risk groups

not:

system collapse


---

Safe Claim

Safe v12 claim:

OMNIA-VALIDATION Level 3 v12 applies the raw trajectory warning mechanism
to multi-source real parsed GSM-Symbolic model-output file records mapped into
raw ordered structural trajectory events.

The validator preserves source-file references, source-file hashes, provider
identity, model identity, answer-extraction fields, correctness profiles,
extraction profiles, cross-source groups, visible weights, visible thresholds,
and inspectable transition evidence.

The aggregate result is DRIFT with WATCH gate action.

The highest-risk trajectory is provider_b collapse-like trajectory, classified
as CRITICAL under the current thresholds.


---

Claims to Avoid

Do not claim:

OMNIA solves GSM-Symbolic.

Do not claim:

OMNIA detects semantic truth.

Do not claim:

v12 replaces official benchmark scoring.

Do not claim:

v12 is production-certified.

Do not claim:

The thresholds are universal.

Do not claim:

provider_b is semantically worse than provider_a.

Do not claim:

wrong answer means structural collapse.

Do not claim:

correct answer means structural stability.

Do not claim:

extraction failure automatically means collapse.

Correct boundary:

v12 measures structural warning risk over multi-source real parsed model-output
file records mapped into raw ordered trajectory events.


---

Final Verdict

Level 3 v12 PASS

Final structural result:

aggregate_risk_score:       0.395512
aggregate_risk_regime:      DRIFT
aggregate_gate_action:      WATCH
aggregate_accuracy_rate:    0.42
aggregate_extraction_rate:  0.90
highest_risk_trajectory:    gsm_symbolic_multi_source_provider_b_collapse_like_001
highest_risk_score:         0.676146
highest_risk_provider:      provider_b

Correct interpretation:

v12 demonstrates coherent multi-source structural warning measurement over
real parsed GSM-Symbolic model-output file mappings.

Incorrect interpretation:

v12 proves that OMNIA understands or solves GSM-Symbolic.


---

Next Step

The next logical validation step is:

Level 3 v13

Recommended direction:

cross-provider consistency and disagreement analysis

Possible v13 target:

multi-source disagreement-aware structural warning validator

v13 should measure not only per-provider risk, but also cross-provider structural disagreement over the same template groups.

Possible added signals:

cross_source_risk_spread
cross_source_regime_disagreement
cross_source_accuracy_disagreement
cross_source_extraction_disagreement
highest_risk_provider_switch
provider_instability_index

The boundary must remain:

measurement != inference != decision