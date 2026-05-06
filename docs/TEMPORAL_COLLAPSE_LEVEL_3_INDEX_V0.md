# Temporal Collapse Level 3 Index v0

## Purpose

This document indexes the Level 3 early-warning layer of OMNIA-VALIDATION.

Level 1 detected temporal-collapse signatures.

Level 2 mapped temporal-collapse topology, control-plane behavior, dependency boundaries, and phase regimes.

Level 3 introduces operational early-warning classification.

The purpose is to move from:

```text
after-the-fact collapse mapping
```

to:

```text
pre-collapse structural warning
```

---

## Core Boundary

Level 3 does not predict universal AI collapse.

Level 3 does not detect semantic truth.

Level 3 does not make final decisions.

Level 3 measures structural warning conditions only.

```text
measurement != inference != decision
```

---

## Level 3 Function

Given a trajectory or trajectory-like sequence, Level 3 computes structural warning signals and classifies the trajectory into a risk regime.

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

It is a measurement-derived warning signal for an external decision layer.

---

## Level 3 Progression

Level 3 currently has eleven validation steps:

```text
Level 3 v0
  -> synthetic reference trajectories

Level 3 v1
  -> Level 2-derived result snapshots

Level 3 v2
  -> ordered Level 2 stage trajectory

Level 3 v3
  -> raw ordered reference trajectories

Level 3 v4
  -> external-style raw trajectory validation

Level 3 v5
  -> separate-generator raw trajectory validation

Level 3 v6
  -> declared external-source raw trajectory validation

Level 3 v7
  -> verified external-source raw trajectory validation

Level 3 v8
  -> direct public benchmark record mapping

Level 3 v9
  -> direct answer-trace mapping

Level 3 v10
  -> bounded actual-output-style model-output mapping
```

Current strongest step:

```text
v10 -> bounded actual-output-style GSM-Symbolic model-output mapping
```

Important limitation:

```text
v10 is not an official public GSM-Symbolic model-output benchmark run.
```

---

## Canonical Level 3 Files

```text
docs/TEMPORAL_COLLAPSE_EARLY_WARNING_LEVEL_3_V0.md
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
```

---

## Level 3 v0

### Files

```text
examples/temporal_collapse_early_warning_level_3_v0.py
results/temporal_collapse_early_warning_level_3_v0.json
docs/TEMPORAL_COLLAPSE_EARLY_WARNING_LEVEL_3_V0_RESULT.md
```

### Result

```text
PASS
```

Risk progression:

```text
stable_reference_001    -> 0.0380 -> STABLE   -> PASS
drift_reference_001     -> 0.2830 -> DRIFT    -> WATCH
critical_reference_001  -> 0.5650 -> CRITICAL -> ESCALATE
collapse_reference_001  -> 0.8685 -> COLLAPSE -> STOP
```

Correct interpretation:

```text
v0 validates the minimal early-warning mechanism on synthetic reference trajectories only.
```

---

## Level 3 v1

### Files

```text
examples/temporal_collapse_early_warning_from_level_2_v1.py
results/temporal_collapse_early_warning_from_level_2_v1.json
docs/TEMPORAL_COLLAPSE_EARLY_WARNING_FROM_LEVEL_2_V1_RESULT.md
```

### Result

```text
PASS
```

Aggregate:

```text
aggregate_risk_score:  0.300373
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
```

Strongest local warning:

```text
dependency_boundary_v0 -> CRITICAL -> ESCALATE
```

Correct interpretation:

```text
v1 applies Level 3 warning logic to Level 2-derived result snapshots.
```

Limitation:

```text
v1 is a heuristic bridge, not direct raw trajectory validation.
```

---

## Level 3 v2

### Files

```text
examples/temporal_collapse_trajectory_native_validator_v2.py
results/temporal_collapse_trajectory_native_validator_v2.json
docs/TEMPORAL_COLLAPSE_TRAJECTORY_NATIVE_VALIDATOR_V2_RESULT.md
```

### Result

```text
PASS
```

Aggregate:

```text
risk_score:    0.357220
risk_regime:   DRIFT
gate_action:   WATCH
dominant_axis: boundary_proximity
```

Ordered stage trajectory:

```text
PASS -> PASS -> PASS -> CHECK -> CHECK -> CHECK -> PASS
```

Correct interpretation:

```text
v2 evaluates the ordered Level 2 stage chain as a trajectory.
```

Limitation:

```text
v2 is trajectory-native relative to Level 2 stages, not raw runtime trajectory validation.
```

---

## Level 3 v3

### Files

```text
docs/TEMPORAL_COLLAPSE_RAW_TRAJECTORY_VALIDATOR_V3.md
data/temporal_collapse_raw_trajectories_v3.jsonl
examples/temporal_collapse_raw_trajectory_validator_v3.py
results/temporal_collapse_raw_trajectory_validator_v3.json
docs/TEMPORAL_COLLAPSE_RAW_TRAJECTORY_VALIDATOR_V3_RESULT.md
```

### Result

```text
PASS
```

Risk progression:

```text
raw_stable_001         -> 0.033417 -> STABLE   -> PASS
raw_drift_001          -> 0.277833 -> DRIFT    -> WATCH
raw_critical_001       -> 0.568722 -> CRITICAL -> ESCALATE
raw_collapse_like_001  -> 0.817056 -> COLLAPSE -> STOP
```

Aggregate:

```text
aggregate_risk_score:  0.424257
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
```

Correct interpretation:

```text
v3 validates the raw ordered trajectory warning mechanism on bounded reference trajectories.
```

---

## Level 3 v4

### Files

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_RAW_TRAJECTORY_VALIDATOR_V4.md
data/temporal_collapse_external_raw_trajectories_v4.jsonl
examples/temporal_collapse_external_raw_trajectory_validator_v4.py
results/temporal_collapse_external_raw_trajectory_validator_v4.json
docs/TEMPORAL_COLLAPSE_EXTERNAL_RAW_TRAJECTORY_VALIDATOR_V4_RESULT.md
```

### Result

```text
PASS
```

Boundary:

```text
source:              external_style_generator_v4
source_independence: not_verified
```

Risk progression:

```text
external_stable_001               -> 0.040583 -> STABLE   -> PASS
external_drift_001                -> 0.321306 -> DRIFT    -> WATCH
external_borderline_critical_001  -> 0.536222 -> CRITICAL -> ESCALATE
external_critical_001             -> 0.619778 -> CRITICAL -> ESCALATE
external_collapse_like_001        -> 0.824306 -> COLLAPSE -> STOP
```

Correct interpretation:

```text
v4 applies raw trajectory warning logic to external-style records.
```

Limitation:

```text
v4 is not verified independent validation.
```

---

## Level 3 v5

### Files

```text
examples/generate_independent_raw_trajectories_v5.py
data/temporal_collapse_verified_independent_raw_trajectories_v5.jsonl
examples/temporal_collapse_verified_independent_raw_trajectory_validator_v5.py
results/temporal_collapse_verified_independent_raw_trajectory_validator_v5.json
docs/TEMPORAL_COLLAPSE_VERIFIED_INDEPENDENT_RAW_TRAJECTORY_VALIDATOR_V5_RESULT.md
```

### Result

```text
PASS
```

Boundary:

```text
source:              independent_generator_script_v5
source_independence: generated_by_independent_script
independence_method: separate_generator_script
```

Risk progression:

```text
independent_stable_001               -> 0.037367 -> STABLE   -> PASS
independent_drift_001                -> 0.285528 -> DRIFT    -> WATCH
independent_borderline_critical_001  -> 0.495100 -> DRIFT    -> WATCH
independent_critical_001             -> 0.595339 -> CRITICAL -> ESCALATE
independent_collapse_like_001        -> 0.808922 -> COLLAPSE -> STOP
```

Aggregate:

```text
aggregate_risk_score:  0.444451
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
```

Correct interpretation:

```text
v5 applies raw trajectory warning logic to records generated by a separate generator script.
```

Limitation:

```text
v5 is stronger than v4, but it is not absolute external validation.
```

---

## Level 3 v6

### Files

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V6.md
data/temporal_collapse_external_source_raw_trajectories_v6.jsonl
examples/temporal_collapse_external_source_raw_trajectory_validator_v6.py
results/temporal_collapse_external_source_raw_trajectory_validator_v6.json
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V6_RESULT.md
```

### Result

```text
PASS
```

Boundary:

```text
source:              benchmark_prompt_perturbation_v6
source_independence: external_source_declared
independence_method: prompt_perturbation_trace
```

Risk progression:

```text
external_source_stable_001               -> 0.040000 -> STABLE   -> PASS
external_source_drift_001                -> 0.294956 -> DRIFT    -> WATCH
external_source_borderline_critical_001  -> 0.503233 -> CRITICAL -> ESCALATE
external_source_critical_001             -> 0.606739 -> CRITICAL -> ESCALATE
external_source_collapse_like_001        -> 0.813406 -> COLLAPSE -> STOP
```

Aggregate:

```text
aggregate_risk_score:  0.451667
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
```

Correct interpretation:

```text
v6 applies raw trajectory warning logic to declared external-source records.
```

Limitation:

```text
v6 is external_source_declared, not external_source_verified.
```

---

## Level 3 v7

### Files

```text
docs/TEMPORAL_COLLAPSE_VERIFIED_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V7.md
data/temporal_collapse_verified_external_source_raw_trajectories_v7.jsonl
examples/temporal_collapse_verified_external_source_raw_trajectory_validator_v7.py
results/temporal_collapse_verified_external_source_raw_trajectory_validator_v7.json
docs/TEMPORAL_COLLAPSE_VERIFIED_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V7_RESULT.md
```

### Result

```text
PASS
```

Boundary:

```text
source:                    gsm_symbolic_public_benchmark_v7
source_independence:       external_source_verified
independence_method:       public_benchmark_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

Risk progression:

```text
gsm_symbolic_stable_001               -> 0.106344 -> STABLE   -> PASS
gsm_symbolic_drift_001                -> 0.306183 -> DRIFT    -> WATCH
gsm_symbolic_borderline_critical_001  -> 0.508467 -> CRITICAL -> ESCALATE
gsm_symbolic_critical_001             -> 0.584711 -> CRITICAL -> ESCALATE
gsm_symbolic_collapse_like_001        -> 0.817794 -> COLLAPSE -> STOP
```

Aggregate:

```text
aggregate_risk_score:  0.464700
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
```

Correct interpretation:

```text
v7 maps GSM-Symbolic-derived verified external-source raw trajectory records into Level 3 warning logic.
```

Limitation:

```text
v7 does not claim that OMNIA solves GSM-Symbolic.
```

---

## Level 3 v8

### Files

```text
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_RECORD_VALIDATOR_V8.md
data/temporal_collapse_direct_gsm_symbolic_records_v8.jsonl
examples/temporal_collapse_direct_gsm_symbolic_record_validator_v8.py
results/temporal_collapse_direct_gsm_symbolic_record_validator_v8.json
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_RECORD_VALIDATOR_V8_RESULT.md
```

### Result

```text
PASS
```

Boundary:

```text
source:                    gsm_symbolic_public_benchmark_v8
source_independence:       external_source_verified
independence_method:       direct_public_benchmark_record_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name:            GSM-Symbolic
source_record_type:        template_variant
mapping_method:            template_variant_to_trajectory
```

Risk progression:

```text
gsm_symbolic_direct_stable_001               -> 0.104128 -> STABLE   -> PASS
gsm_symbolic_direct_drift_001                -> 0.303100 -> DRIFT    -> WATCH
gsm_symbolic_direct_borderline_critical_001  -> 0.511733 -> CRITICAL -> ESCALATE
gsm_symbolic_direct_critical_001             -> 0.587978 -> CRITICAL -> ESCALATE
gsm_symbolic_direct_collapse_like_001        -> 0.820378 -> COLLAPSE -> STOP
```

Aggregate:

```text
aggregate_risk_score:  0.465463
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
```

Correct interpretation:

```text
v8 maps direct GSM-Symbolic public benchmark record fields into raw ordered structural trajectory events.
```

Limitation:

```text
v8 does not claim GSM-Symbolic solving and does not evaluate semantic correctness.
```

Technical note:

```text
The earlier v8 output contained the label multiple_mapping_notess.

This is a harmless formatting issue caused by pluralizing mapping_notes by appending s.

The intended clean label is multiple_mapping_notes.

The measurement result is not affected.
```

---

## Level 3 v9

### Files

```text
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_ANSWER_TRACE_VALIDATOR_V9.md
data/temporal_collapse_direct_gsm_symbolic_answer_traces_v9.jsonl
examples/temporal_collapse_direct_gsm_symbolic_answer_trace_validator_v9.py
results/temporal_collapse_direct_gsm_symbolic_answer_trace_validator_v9.json
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_ANSWER_TRACE_VALIDATOR_V9_RESULT.md
```

### Result

```text
PASS
```

Boundary:

```text
source:                    gsm_symbolic_answer_trace_v9
source_independence:       external_source_verified
independence_method:       direct_answer_trace_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name:            GSM-Symbolic
source_record_type:        answer_trace
mapping_method:            answer_trace_to_trajectory
```

Risk progression:

```text
gsm_symbolic_answer_trace_stable_001               -> 0.068278 -> STABLE   -> PASS
gsm_symbolic_answer_trace_drift_001                -> 0.352772 -> DRIFT    -> WATCH
gsm_symbolic_answer_trace_borderline_critical_001  -> 0.561733 -> CRITICAL -> ESCALATE
gsm_symbolic_answer_trace_critical_001             -> 0.637978 -> CRITICAL -> ESCALATE
gsm_symbolic_answer_trace_collapse_like_001        -> 0.787044 -> COLLAPSE -> STOP
```

Aggregate:

```text
aggregate_risk_score:    0.481561
aggregate_risk_regime:   DRIFT
aggregate_gate_action:   WATCH
aggregate_accuracy_rate: 0.480000
```

Correct interpretation:

```text
v9 maps direct GSM-Symbolic answer traces into raw ordered structural trajectory events.
```

Limitation:

```text
v9 does not claim GSM-Symbolic solving, does not infer semantic truth, and does not replace benchmark correctness.
```

Important rule:

```text
is_correct is evidence
risk_score remains structural warning measurement
```

---

## Level 3 v10

### Files

```text
docs/TEMPORAL_COLLAPSE_ACTUAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V10.md
data/temporal_collapse_actual_gsm_symbolic_model_outputs_v10.jsonl
examples/temporal_collapse_actual_gsm_symbolic_model_output_validator_v10.py
results/temporal_collapse_actual_gsm_symbolic_model_output_validator_v10.json
docs/TEMPORAL_COLLAPSE_ACTUAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V10_RESULT.md
```

### Result

```text
PASS
```

Boundary:

```text
source:                    gsm_symbolic_actual_model_output_v10
source_independence:       external_source_verified
independence_method:       actual_model_output_trace_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name:            GSM-Symbolic
source_record_type:        actual_model_output
mapping_method:            actual_model_output_to_trajectory
```

Mandatory limitation:

```text
These are bounded actual-output-style records for validator construction,
not an official public GSM-Symbolic model-output benchmark run.
```

Risk progression:

```text
gsm_symbolic_actual_output_stable_001               -> 0.068278 -> STABLE   -> PASS
gsm_symbolic_actual_output_drift_001                -> 0.352772 -> DRIFT    -> WATCH
gsm_symbolic_actual_output_borderline_critical_001  -> 0.561733 -> CRITICAL -> ESCALATE
gsm_symbolic_actual_output_critical_001             -> 0.637978 -> CRITICAL -> ESCALATE
gsm_symbolic_actual_output_collapse_like_001        -> 0.787044 -> COLLAPSE -> STOP
```

Aggregate:

```text
aggregate_risk_score:       0.481561
aggregate_risk_regime:      DRIFT
aggregate_gate_action:      WATCH
aggregate_accuracy_rate:    0.480000
aggregate_extraction_rate:  0.920000
```

Regime counts:

```text
STABLE   -> 1
DRIFT    -> 1
CRITICAL -> 2
COLLAPSE -> 1
```

Highest-risk trajectory:

```text
gsm_symbolic_actual_output_collapse_like_001 -> 0.787044 -> COLLAPSE -> STOP
```

Tracked model-output-style fields:

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
correctness_profile
extraction_profile
```

Model summary:

```text
reference_model_a_v1 -> 2 trajectories -> average risk 0.210525 -> average accuracy 0.800000 -> extraction 1.000000
reference_model_b_v1 -> 2 trajectories -> average risk 0.599856 -> average accuracy 0.300000 -> extraction 1.000000
reference_model_c_v1 -> 1 trajectory   -> average risk 0.787044 -> average accuracy 0.200000 -> extraction 0.600000
```

Correct interpretation:

```text
v10 maps bounded actual-output-style GSM-Symbolic model-output traces into raw ordered structural trajectory events.
```

Limitation:

```text
v10 is not an official public GSM-Symbolic model-output benchmark run.
```

Important rule:

```text
correctness_profile is evidence
extraction_profile is evidence
risk_score remains structural warning measurement
```

v10 does not claim:

```text
GSM-Symbolic solving
semantic truth detection
official benchmark correctness scoring
production certification
model cognition detection
universal collapse prediction
```

---

## Risk Formula v0/v1

Level 3 v0 and v1 use:

```text
risk_score =
    0.20 * transition_density
  + 0.20 * drift_score
  + 0.25 * boundary_proximity
  + 0.25 * collapse_similarity
  + 0.10 * irreversibility_signal
```

---

## Risk Formula v2

Level 3 v2 uses:

```text
risk_score =
    0.20 * transition_density
  + 0.20 * drift_progression
  + 0.25 * boundary_proximity
  + 0.25 * collapse_similarity
  + 0.10 * irreversibility_proxy
```

---

## Risk Formula v3/v4/v5/v6/v7/v8/v9/v10

Level 3 v3 through v10 use the raw ordered trajectory variant:

```text
risk_score =
    0.20 * transition_density
  + 0.20 * drift_progression
  + 0.25 * boundary_proximity
  + 0.25 * collapse_similarity
  + 0.10 * irreversibility_signal
```

The raw trajectory formula measures over ordered event fields:

```text
signature transitions
cluster transitions
phase transitions
delta progression
iri progression
boundary distance
collapse phase count
broken signature markers
```

v9 additionally tracks:

```text
direct answer-trace mapping
model_name
run_id
response_id
expected_answer
model_final_answer
is_correct
correctness_profile
aggregate_accuracy_rate
```

v10 additionally tracks:

```text
bounded actual-output-style mapping
model_version
raw_question_hash
raw_output_hash
answer_extraction_method
extraction_profile
aggregate_extraction_rate
model_versions
answer_extraction_methods
```

Important boundary:

```text
is_correct is evidence
extraction_profile is evidence
risk_score remains structural warning measurement
```

---

## Classification Thresholds

Current thresholds:

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

These thresholds are experimental.

They are not universal.

They are valid only inside the tested construction unless expanded by later validation.

---

## Structural Path

Logical dependency:

```text
temporal-collapse signatures
  -> cluster structure
  -> directed graph topology
  -> centrality behavior
  -> control-plane behavior
  -> robustness CHECK
  -> dependency map
  -> boundary map
  -> phase diagram
  -> early-warning classification
  -> raw trajectory warning
  -> external-style raw trajectory validation
  -> separate-generator raw trajectory validation
  -> declared external-source raw trajectory validation
  -> verified external-source raw trajectory validation
  -> direct public benchmark record mapping
  -> direct answer-trace mapping
  -> bounded actual-output-style model-output mapping
```

The Level 3 warning layer exists because Level 2 mapped structural boundaries.

Without the Level 2 boundary map, Level 3 would only be arbitrary scoring.

With the Level 2 boundary map, Level 3 becomes bounded structural navigation.

---

## Structural Reading Across v0 to v10

### v0

```text
synthetic reference trajectories
  -> STABLE / DRIFT / CRITICAL / COLLAPSE separated
```

### v1

```text
Level 2-derived snapshots
  -> aggregate DRIFT
  -> dependency_boundary CRITICAL
```

### v2

```text
ordered Level 2 stage trajectory
  -> DRIFT
  -> WATCH
  -> boundary_proximity dominant
```

### v3

```text
raw ordered reference trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE separated
```

### v4

```text
external-style raw trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE-like regimes separated
  -> source_independence: not_verified
```

### v5

```text
separate-generator raw trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> independence_method: separate_generator_script
```

### v6

```text
declared external-source raw trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> source_independence: external_source_declared
```

### v7

```text
GSM-Symbolic-derived verified external-source raw trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> source_independence: external_source_verified
  -> independence_method: public_benchmark_mapping
```

### v8

```text
direct GSM-Symbolic public benchmark record mappings
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> source_record_type: template_variant
  -> mapping_method: template_variant_to_trajectory
```

### v9

```text
direct GSM-Symbolic answer-trace mappings
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> source_record_type: answer_trace
  -> mapping_method: answer_trace_to_trajectory
```

### v10

```text
bounded actual-output-style GSM-Symbolic model-output mappings
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> source_record_type: actual_model_output
  -> mapping_method: actual_model_output_to_trajectory
```

v10 adds:

```text
model_version
raw_question_hash
raw_output_hash
answer_extraction_method
extraction_profile
aggregate_extraction_rate
```

v10 decisive boundary:

```text
source_independence: external_source_verified
independence_method: actual_model_output_trace_mapping
benchmark_name: GSM-Symbolic
source_record_type: actual_model_output
mapping_method: actual_model_output_to_trajectory
```

v10 mandatory limitation:

```text
bounded actual-output-style records for validator construction,
not an official public GSM-Symbolic model-output benchmark run
```

---

## Current Structural Verdict

Safe verdict:

```text
Level 3 has moved from synthetic warning,
to Level 2-derived warning,
to ordered stage-trajectory warning,
to raw ordered trajectory warning,
to external-style raw trajectory validation,
to separate-generator raw trajectory validation,
to declared external-source raw trajectory validation,
to verified external-source raw trajectory validation,
to direct public benchmark record mapping,
to direct answer-trace mapping,
to bounded actual-output-style model-output mapping.
```

Current strongest result:

```text
Level 3 v10
```

Current strongest boundary:

```text
bounded actual-output-style GSM-Symbolic model-output traces
mapped into raw ordered structural trajectory events
```

Current strongest result values:

```text
aggregate_risk_score:       0.481561
aggregate_risk_regime:      DRIFT
aggregate_gate_action:      WATCH
aggregate_accuracy_rate:    0.480000
aggregate_extraction_rate:  0.920000
highest_risk:               gsm_symbolic_actual_output_collapse_like_001
highest_score:              0.787044
```

Correct interpretation:

```text
v10 demonstrates coherent structural regime separation over bounded
actual-output-style GSM-Symbolic model-output mappings.
```

Incorrect interpretation:

```text
v10 proves that OMNIA solves GSM-Symbolic.
```

---

## Safe Claim

```text
OMNIA-VALIDATION Level 3 v10 applied the raw trajectory warning mechanism
to bounded actual-output-style GSM-Symbolic model-output traces mapped into
raw ordered structural events.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
tracked correctness profiles, tracked extraction profiles, and preserved
model/source/benchmark boundaries.

The result is bounded, reproducible, and falsifiable.

It is not an official public GSM-Symbolic model-output benchmark run.
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
Level 3 is production-certified.
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
v10 is an official public GSM-Symbolic model-output benchmark run.
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
Extraction failure automatically means semantic collapse.
```

Correct boundary:

```text
Level 3 v10 measures structural warning risk over bounded actual-output-style
GSM-Symbolic model-output traces mapped into raw ordered trajectory events.
```

---

## Current Level 3 Status

```text
Level 3 v0
  -> synthetic early-warning prototype
  -> PASS

Level 3 v1
  -> Level 2-derived bridge
  -> PASS
  -> aggregate DRIFT

Level 3 v2
  -> ordered Level 2 stage trajectory
  -> PASS
  -> trajectory DRIFT

Level 3 v3
  -> raw ordered reference trajectories
  -> PASS
  -> STABLE / DRIFT / CRITICAL / COLLAPSE separated

Level 3 v4
  -> external-style raw trajectory validation
  -> PASS
  -> source independence: not_verified

Level 3 v5
  -> separate-generator raw trajectory validation
  -> PASS
  -> independence method: separate_generator_script

Level 3 v6
  -> declared external-source raw trajectory validation
  -> PASS
  -> source independence: external_source_declared

Level 3 v7
  -> verified external-source raw trajectory validation
  -> PASS
  -> source independence: external_source_verified
  -> independence method: public_benchmark_mapping

Level 3 v8
  -> direct public benchmark record mapping
  -> PASS
  -> source record type: template_variant
  -> mapping method: template_variant_to_trajectory

Level 3 v9
  -> direct answer-trace mapping
  -> PASS
  -> source record type: answer_trace
  -> mapping method: answer_trace_to_trajectory

Level 3 v10
  -> bounded actual-output-style model-output mapping
  -> PASS
  -> source record type: actual_model_output
  -> mapping method: actual_model_output_to_trajectory
  -> aggregate accuracy rate: 0.480000
  -> aggregate extraction rate: 0.920000
  -> not an official public GSM-Symbolic model-output benchmark run
```

---

## Next Step

The next validation step is to move from bounded actual-output-style records to real parsed output files, live model outputs, or public benchmark output traces.

Target direction:

```text
Level 3 v11
  -> real parsed model-output file validation
```

Possible v11 source classes:

```text
real model outputs over GSM-Symbolic variants
public benchmark output traces
parsed generated answer files
answer extraction logs from actual runs
multi-model output comparisons
```

Target files:

```text
docs/TEMPORAL_COLLAPSE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V11.md
data/temporal_collapse_real_gsm_symbolic_model_outputs_v11.jsonl
examples/temporal_collapse_real_gsm_symbolic_model_output_validator_v11.py
results/temporal_collapse_real_gsm_symbolic_model_output_validator_v11.json
docs/TEMPORAL_COLLAPSE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V11_RESULT.md
```

v11 should preserve:

```text
raw_question_hash
raw_output_hash
model_name
model_version
provider
run_id
response_id
answer_extraction_method
expected_answer
model_final_answer
is_correct
source_record_reference
source file reference
mapping method
source independence status
external source reference
```

The v11 objective is to test whether the raw trajectory warning mechanism remains coherent when the records come from real parsed model-output files rather than bounded actual-output-style construction.