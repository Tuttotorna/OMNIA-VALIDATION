# Temporal Collapse Actual GSM-Symbolic Model Output Validator — v10 Result

## Status

PASS.

The Level 3 v10 actual GSM-Symbolic model-output validator executed successfully.

No runtime error was produced.

```text
STDERR: empty
RETURN CODE: 0
```

Input file:

```text
data/temporal_collapse_actual_gsm_symbolic_model_outputs_v10.jsonl
```

Output file:

```text
results/temporal_collapse_actual_gsm_symbolic_model_output_validator_v10.json
```

Validator script:

```text
examples/temporal_collapse_actual_gsm_symbolic_model_output_validator_v10.py
```

---

## Purpose

This experiment moves Level 3 from direct answer-trace mapping to bounded actual-output-style model-output trace validation.

Level 3 v9 used:

```text
source_record_type: answer_trace
mapping_method: answer_trace_to_trajectory
```

Level 3 v10 uses:

```text
source_record_type: actual_model_output
mapping_method: actual_model_output_to_trajectory
```

The objective is to test whether the raw trajectory warning mechanism remains coherent when model-output-style records include:

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

```text
measurement != inference != decision
```

---

## Tested Boundary

The tested boundary is:

```text
bounded actual-output-style GSM-Symbolic model-output traces mapped into raw ordered structural trajectory events
```

Source:

```text
gsm_symbolic_actual_model_output_v10
```

Source independence:

```text
external_source_verified
```

Independence method:

```text
actual_model_output_trace_mapping
```

Benchmark name:

```text
GSM-Symbolic
```

Source record type:

```text
actual_model_output
```

Mapping method:

```text
actual_model_output_to_trajectory
```

External source reference:

```text
GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

---

## Mandatory Limitation

The v10 result includes this limitation:

```text
These are bounded actual-output-style records for validator construction,
not an official public GSM-Symbolic model-output benchmark run.
```

Correct reading:

```text
v10 measures structural warning risk over bounded actual-output-style GSM-Symbolic traces.
```

Incorrect reading:

```text
v10 is an official public GSM-Symbolic model-output benchmark run.
```

---

## Important Boundary Note

v10 is stronger than v9 as a validator-construction step because it adds model-output-style fields and extraction profiles.

However, v10 still does not prove benchmark solving.

It does not infer semantic truth.

It does not replace benchmark correctness.

Correctness and extraction are tracked as evidence.

They are not the final measurement.

Correct claim:

```text
actual-output-style traces were mapped into raw ordered structural trajectory events
```

Incorrect claim:

```text
OMNIA solved GSM-Symbolic
```

---

## Input Dataset

The dataset contains five bounded actual-output-style GSM-Symbolic trajectories:

```text
gsm_symbolic_actual_output_stable_001
gsm_symbolic_actual_output_drift_001
gsm_symbolic_actual_output_borderline_critical_001
gsm_symbolic_actual_output_critical_001
gsm_symbolic_actual_output_collapse_like_001
```

Each event contains:

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

The validator groups events by `trajectory_id` and sorts each trajectory by `step`.

---

## Source Summary

The v10 source summary was separated by model, model version, and extraction method:

```json
[
  {
    "source": "gsm_symbolic_actual_model_output_v10",
    "source_independence": "external_source_verified",
    "independence_method": "actual_model_output_trace_mapping",
    "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
    "benchmark_name": "GSM-Symbolic",
    "source_record_type": "actual_model_output",
    "mapping_method": "actual_model_output_to_trajectory",
    "model_name": "reference_model_a",
    "model_version": "reference_model_a_v1",
    "answer_extraction_method": "final_numeric_answer_extractor_v1",
    "trajectory_count": 2,
    "average_risk_score": 0.210525,
    "average_accuracy_rate": 0.8,
    "average_extraction_rate": 1.0,
    "regime_counts": {
      "DRIFT": 1,
      "STABLE": 1
    },
    "highest_risk_trajectory": "gsm_symbolic_actual_output_drift_001",
    "highest_risk_score": 0.352772
  },
  {
    "source": "gsm_symbolic_actual_model_output_v10",
    "source_independence": "external_source_verified",
    "independence_method": "actual_model_output_trace_mapping",
    "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
    "benchmark_name": "GSM-Symbolic",
    "source_record_type": "actual_model_output",
    "mapping_method": "actual_model_output_to_trajectory",
    "model_name": "reference_model_b",
    "model_version": "reference_model_b_v1",
    "answer_extraction_method": "final_numeric_answer_extractor_v1",
    "trajectory_count": 2,
    "average_risk_score": 0.599856,
    "average_accuracy_rate": 0.3,
    "average_extraction_rate": 1.0,
    "regime_counts": {
      "CRITICAL": 2
    },
    "highest_risk_trajectory": "gsm_symbolic_actual_output_critical_001",
    "highest_risk_score": 0.637978
  },
  {
    "source": "gsm_symbolic_actual_model_output_v10",
    "source_independence": "external_source_verified",
    "independence_method": "actual_model_output_trace_mapping",
    "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
    "benchmark_name": "GSM-Symbolic",
    "source_record_type": "actual_model_output",
    "mapping_method": "actual_model_output_to_trajectory",
    "model_name": "reference_model_c",
    "model_version": "reference_model_c_v1",
    "answer_extraction_method": "final_numeric_answer_extractor_v1",
    "trajectory_count": 1,
    "average_risk_score": 0.787044,
    "average_accuracy_rate": 0.2,
    "average_extraction_rate": 0.6,
    "regime_counts": {
      "COLLAPSE": 1
    },
    "highest_risk_trajectory": "gsm_symbolic_actual_output_collapse_like_001",
    "highest_risk_score": 0.787044
  }
]
```

---

## Risk Formula

The v10 risk score preserves the raw trajectory formula used by v3 through v9:

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

Thresholds:

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

All weights and thresholds are visible.

No hidden interpretation layer is used.

---

## Correctness and Extraction Rule

v10 tracks correctness and extraction as evidence.

They do not replace the structural risk score.

Each trajectory includes:

```text
correctness_profile
extraction_profile
```

Important boundary:

```text
correctness_profile is evidence
extraction_profile is evidence
risk_score is structural warning measurement
```

Correctness, extraction, and structural risk may correlate.

They are not the same measurement.

---

## Aggregate Result

The aggregate v10 result was:

```text
aggregate_risk_score:       0.481561
aggregate_risk_regime:      DRIFT
aggregate_gate_action:      WATCH
aggregate_accuracy_rate:    0.480000
aggregate_extraction_rate:  0.920000
source_count:               1
model_count:                3
model_version_count:        3
answer_extraction_method_count: 1
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
gsm_symbolic_actual_output_collapse_like_001 -> 0.787044
```

Interpretation:

The aggregate result is DRIFT because the dataset contains mixed trajectories.

The important result is that the actual-output-style validator separated the five ordered traces into distinct risk regimes while preserving correctness, extraction, model, version, source, and benchmark boundaries.

---

## Ordered Risk Progression

The validator produced the following progression:

```text
gsm_symbolic_actual_output_stable_001               -> STABLE   -> 0.068278 -> PASS
gsm_symbolic_actual_output_drift_001                -> DRIFT    -> 0.352772 -> WATCH
gsm_symbolic_actual_output_borderline_critical_001  -> CRITICAL -> 0.561733 -> ESCALATE
gsm_symbolic_actual_output_critical_001             -> CRITICAL -> 0.637978 -> ESCALATE
gsm_symbolic_actual_output_collapse_like_001        -> COLLAPSE -> 0.787044 -> STOP
```

The borderline trajectory crossed the CRITICAL threshold:

```text
gsm_symbolic_actual_output_borderline_critical_001 -> 0.561733
CRITICAL threshold                                 -> 0.500000
margin above threshold                             -> 0.061733
```

---

## Accuracy Profile

The aggregate accuracy rate was:

```text
0.480000
```

Per trajectory:

```text
gsm_symbolic_actual_output_stable_001               -> accuracy 1.000000
gsm_symbolic_actual_output_drift_001                -> accuracy 0.600000
gsm_symbolic_actual_output_borderline_critical_001  -> accuracy 0.400000
gsm_symbolic_actual_output_critical_001             -> accuracy 0.200000
gsm_symbolic_actual_output_collapse_like_001        -> accuracy 0.200000
```

Correct reading:

```text
in this bounded dataset, structural risk and answer failure trend together
```

Incorrect reading:

```text
structural risk is identical to benchmark correctness
```

---

## Extraction Profile

The aggregate extraction rate was:

```text
0.920000
```

Per trajectory:

```text
gsm_symbolic_actual_output_stable_001               -> extraction 1.000000
gsm_symbolic_actual_output_drift_001                -> extraction 1.000000
gsm_symbolic_actual_output_borderline_critical_001  -> extraction 1.000000
gsm_symbolic_actual_output_critical_001             -> extraction 1.000000
gsm_symbolic_actual_output_collapse_like_001        -> extraction 0.600000
```

The collapse-like trajectory includes two `not_extracted` model-final-answer events.

Correct reading:

```text
extraction failure is evidence
```

Incorrect reading:

```text
extraction failure automatically means semantic collapse
```

---

## Individual Results

### gsm_symbolic_actual_output_stable_001

```text
risk_regime:   STABLE
risk_score:    0.068278
gate_action:   PASS
dominant_axis: boundary_proximity
warning_flags: []
```

Correctness profile:

```json
{
  "event_count": 5,
  "correct_count": 5,
  "incorrect_count": 0,
  "accuracy_rate": 1.0,
  "correctness_changes": 0.0,
  "starts_correct": true,
  "ends_correct": true
}
```

Extraction profile:

```json
{
  "event_count": 5,
  "extracted_count": 5,
  "not_extracted_count": 0,
  "extraction_rate": 1.0,
  "extraction_changes": 0.0,
  "starts_extracted": true,
  "ends_extracted": true,
  "answer_extraction_methods": [
    "final_numeric_answer_extractor_v1"
  ]
}
```

Signals:

```json
{
  "transition_density": 0.0,
  "drift_progression": 0.067056,
  "boundary_proximity": 0.148333,
  "collapse_similarity": 0.058467,
  "irreversibility_signal": 0.031667
}
```

Interpretation:

The stable actual-output-style trace remained below the DRIFT threshold.

Correctness and extraction stayed stable across all events.

---

### gsm_symbolic_actual_output_drift_001

```text
risk_regime:   DRIFT
risk_score:    0.352772
gate_action:   WATCH
dominant_axis: boundary_proximity
warning_flags: []
```

Correctness profile:

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

Extraction profile:

```json
{
  "event_count": 5,
  "extracted_count": 5,
  "not_extracted_count": 0,
  "extraction_rate": 1.0,
  "extraction_changes": 0.0,
  "starts_extracted": true,
  "ends_extracted": true,
  "answer_extraction_methods": [
    "final_numeric_answer_extractor_v1"
  ]
}
```

Signals:

```json
{
  "transition_density": 0.333333,
  "drift_progression": 0.260944,
  "boundary_proximity": 0.465833,
  "collapse_similarity": 0.408167,
  "irreversibility_signal": 0.154167
}
```

Interpretation:

The drift trace crossed out of STABLE and entered DRIFT.

Correctness degraded late, while extraction remained stable.

---

### gsm_symbolic_actual_output_borderline_critical_001

```text
risk_regime:   CRITICAL
risk_score:    0.561733
gate_action:   ESCALATE
dominant_axis: boundary_proximity
warning_flags:
  - high_transition_density
  - boundary_proximity
```

Correctness profile:

```json
{
  "event_count": 5,
  "correct_count": 2,
  "incorrect_count": 3,
  "accuracy_rate": 0.4,
  "correctness_changes": 0.25,
  "starts_correct": true,
  "ends_correct": false
}
```

Extraction profile:

```json
{
  "event_count": 5,
  "extracted_count": 5,
  "not_extracted_count": 0,
  "extraction_rate": 1.0,
  "extraction_changes": 0.0,
  "starts_extracted": true,
  "ends_extracted": true,
  "answer_extraction_methods": [
    "final_numeric_answer_extractor_v1"
  ]
}
```

Signals:

```json
{
  "transition_density": 0.583333,
  "drift_progression": 0.421167,
  "boundary_proximity": 0.739167,
  "collapse_similarity": 0.556833,
  "irreversibility_signal": 0.368333
}
```

Interpretation:

The borderline actual-output-style trace entered CRITICAL.

The transition and boundary signals are visible.

Correctness degradation is preserved as evidence.

---

### gsm_symbolic_actual_output_critical_001

```text
risk_regime:   CRITICAL
risk_score:    0.637978
gate_action:   ESCALATE
dominant_axis: boundary_proximity
warning_flags:
  - high_transition_density
  - high_drift_progression
  - boundary_proximity
  - collapse_similarity
```

Correctness profile:

```json
{
  "event_count": 5,
  "correct_count": 1,
  "incorrect_count": 4,
  "accuracy_rate": 0.2,
  "correctness_changes": 0.25,
  "starts_correct": true,
  "ends_correct": false
}
```

Extraction profile:

```json
{
  "event_count": 5,
  "extracted_count": 5,
  "not_extracted_count": 0,
  "extraction_rate": 1.0,
  "extraction_changes": 0.0,
  "starts_extracted": true,
  "ends_extracted": true,
  "answer_extraction_methods": [
    "final_numeric_answer_extractor_v1"
  ]
}
```

Signals:

```json
{
  "transition_density": 0.583333,
  "drift_progression": 0.507389,
  "boundary_proximity": 0.845833,
  "collapse_similarity": 0.634167,
  "irreversibility_signal": 0.498333
}
```

Interpretation:

The critical trace entered CRITICAL without explicit collapse-phase count.

The high structural pressure is visible through transition density, drift progression, boundary proximity, and collapse similarity.

---

### gsm_symbolic_actual_output_collapse_like_001

```text
risk_regime:   COLLAPSE
risk_score:    0.787044
gate_action:   STOP
dominant_axis: boundary_proximity
warning_flags:
  - high_transition_density
  - high_drift_progression
  - boundary_proximity
  - collapse_similarity
  - irreversibility_signal
```

Correctness profile:

```json
{
  "event_count": 5,
  "correct_count": 1,
  "incorrect_count": 4,
  "accuracy_rate": 0.2,
  "correctness_changes": 0.25,
  "starts_correct": true,
  "ends_correct": false
}
```

Extraction profile:

```json
{
  "event_count": 5,
  "extracted_count": 3,
  "not_extracted_count": 2,
  "extraction_rate": 0.6,
  "extraction_changes": 0.25,
  "starts_extracted": true,
  "ends_extracted": false,
  "answer_extraction_methods": [
    "final_numeric_answer_extractor_v1"
  ]
}
```

Signals:

```json
{
  "transition_density": 0.583333,
  "drift_progression": 0.649389,
  "boundary_proximity": 0.954167,
  "collapse_similarity": 0.858833,
  "irreversibility_signal": 0.8725
}
```

Interpretation:

The collapse-like actual-output-style trace entered COLLAPSE.

All warning flags were activated.

The highest-risk trajectory was correctly identified as:

```text
gsm_symbolic_actual_output_collapse_like_001
```

This trajectory also contains extraction degradation:

```text
extraction_rate: 0.600000
not_extracted_count: 2
```

Extraction failure is evidence, not automatic semantic judgment.

---

## Structural Reading

The v10 result extends v9 by adding actual-output-style fields and extraction profiles.

v9 used:

```text
source_independence: external_source_verified
independence_method: direct_answer_trace_mapping
benchmark_name: GSM-Symbolic
source_record_type: answer_trace
mapping_method: answer_trace_to_trajectory
```

v10 uses:

```text
source_independence: external_source_verified
independence_method: actual_model_output_trace_mapping
benchmark_name: GSM-Symbolic
source_record_type: actual_model_output
mapping_method: actual_model_output_to_trajectory
```

This is a stronger model-output-style boundary step.

The correct structural reading is:

```text
the raw trajectory warning mechanism remains coherent over bounded
actual-output-style GSM-Symbolic model-output mappings
```

not:

```text
OMNIA solves GSM-Symbolic
```

---

## Main Finding

Safe claim:

```text
OMNIA-VALIDATION Level 3 v10 applied the raw trajectory warning mechanism
to bounded actual-output-style GSM-Symbolic model-output traces mapped into
raw ordered structural events.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
tracked correctness profiles, tracked extraction profiles, and preserved
model/source/benchmark boundaries.
```

---

## Important Limitation

This v10 result is still bounded.

It uses actual-output-style records for validator construction.

It is not an official public GSM-Symbolic model-output benchmark run.

It does not prove semantic correctness.

It does not claim benchmark solving.

Correct interpretation:

```text
Level 3 v10 validates the raw trajectory warning mechanism
on bounded actual-output-style GSM-Symbolic model-output mappings.
```

Not:

```text
Level 3 v10 proves OMNIA solves GSM-Symbolic.
```

---

## What This Result Does Not Claim

This result does not claim:

```text
universal AI collapse prediction
semantic truth detection
GSM-Symbolic solving
official benchmark correctness scoring
official public model-output benchmark run
domain-independent validity
production-level certification
final decision authority
model cognition detection
live runtime validation
correctness equals structural stability
wrong answer equals structural collapse
extraction failure automatically equals semantic collapse
```

The result is valid only inside the tested v10 construction.

---

## Conclusion

Level 3 v10 passes as a bounded actual-output-style model-output mapping step.

The validator produced coherent regime separation:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
```

The aggregate result was:

```text
DRIFT
WATCH
```

The aggregate accuracy rate was:

```text
0.480000
```

The aggregate extraction rate was:

```text
0.920000
```

The strongest trajectory was:

```text
gsm_symbolic_actual_output_collapse_like_001 -> COLLAPSE -> STOP
```

The decisive boundary condition is:

```text
source_independence: external_source_verified
independence_method: actual_model_output_trace_mapping
benchmark_name: GSM-Symbolic
source_record_type: actual_model_output
mapping_method: actual_model_output_to_trajectory
```

Therefore, v10 is stronger than v9 as a bounded actual-output-style mapping step.

The next step is to replace bounded actual-output-style records with real parsed output files, live model outputs, or public benchmark output traces.