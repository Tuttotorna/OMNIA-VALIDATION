# Temporal Collapse Direct GSM-Symbolic Answer Trace Validator — v9 Result

## Status

PASS.

The Level 3 v9 direct GSM-Symbolic answer trace validator executed successfully.

No runtime error was produced.

```text
STDERR: empty
RETURN CODE: 0
```

Input file:

```text
data/temporal_collapse_direct_gsm_symbolic_answer_traces_v9.jsonl
```

Output file:

```text
results/temporal_collapse_direct_gsm_symbolic_answer_trace_validator_v9.json
```

Validator script:

```text
examples/temporal_collapse_direct_gsm_symbolic_answer_trace_validator_v9.py
```

---

## Purpose

This experiment moves Level 3 from direct public benchmark record mapping to direct answer-trace mapping.

Level 3 v8 mapped direct GSM-Symbolic public benchmark record fields into raw ordered structural trajectory events.

Level 3 v9 adds direct answer-trace fields:

```text
model_name
run_id
response_id
expected_answer
model_final_answer
is_correct
correctness_profile
```

The objective is to move from:

```text
direct public benchmark record mapping
```

to:

```text
direct answer-trace / model-output mapping
```

```text
measurement != inference != decision
```

---

## Tested Boundary

The tested boundary is:

```text
direct GSM-Symbolic answer traces mapped into raw ordered structural trajectory events
```

Source:

```text
gsm_symbolic_answer_trace_v9
```

Source independence:

```text
external_source_verified
```

Independence method:

```text
direct_answer_trace_mapping
```

Benchmark name:

```text
GSM-Symbolic
```

Source record type:

```text
answer_trace
```

Mapping method:

```text
answer_trace_to_trajectory
```

External source reference:

```text
GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

Correct reading:

```text
v9 measures structural warning risk over direct GSM-Symbolic answer traces mapped into raw trajectory events.
```

Incorrect reading:

```text
v9 proves that OMNIA solves GSM-Symbolic.
```

---

## Important Boundary Note

v9 is stronger than v8 because it adds answer-trace fields and correctness profiles.

However, v9 still does not evaluate semantic truth.

It does not replace official GSM-Symbolic evaluation.

It does not claim that OMNIA solves GSM-Symbolic.

Correct claim:

```text
GSM-Symbolic answer traces were mapped into raw ordered structural trajectory events.
```

Incorrect claim:

```text
OMNIA solved GSM-Symbolic.
```

Correctness is tracked as evidence.

It is not the final measurement.

---

## Input Dataset

The dataset contains five direct GSM-Symbolic answer-trace trajectories:

```text
gsm_symbolic_answer_trace_stable_001
gsm_symbolic_answer_trace_drift_001
gsm_symbolic_answer_trace_borderline_critical_001
gsm_symbolic_answer_trace_critical_001
gsm_symbolic_answer_trace_collapse_like_001
```

Each event contains:

```text
trajectory_id
step
template_id
question_id
variant_type
model_name
run_id
response_id
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

The v9 source summary was separated by model:

```json
[
  {
    "source": "gsm_symbolic_answer_trace_v9",
    "source_independence": "external_source_verified",
    "independence_method": "direct_answer_trace_mapping",
    "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
    "benchmark_name": "GSM-Symbolic",
    "source_record_type": "answer_trace",
    "mapping_method": "answer_trace_to_trajectory",
    "model_name": "reference_model_a",
    "trajectory_count": 2,
    "average_risk_score": 0.210525,
    "average_accuracy_rate": 0.8,
    "regime_counts": {
      "DRIFT": 1,
      "STABLE": 1
    },
    "highest_risk_trajectory": "gsm_symbolic_answer_trace_drift_001",
    "highest_risk_score": 0.352772
  },
  {
    "source": "gsm_symbolic_answer_trace_v9",
    "source_independence": "external_source_verified",
    "independence_method": "direct_answer_trace_mapping",
    "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
    "benchmark_name": "GSM-Symbolic",
    "source_record_type": "answer_trace",
    "mapping_method": "answer_trace_to_trajectory",
    "model_name": "reference_model_b",
    "trajectory_count": 2,
    "average_risk_score": 0.599856,
    "average_accuracy_rate": 0.3,
    "regime_counts": {
      "CRITICAL": 2
    },
    "highest_risk_trajectory": "gsm_symbolic_answer_trace_critical_001",
    "highest_risk_score": 0.637978
  },
  {
    "source": "gsm_symbolic_answer_trace_v9",
    "source_independence": "external_source_verified",
    "independence_method": "direct_answer_trace_mapping",
    "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
    "benchmark_name": "GSM-Symbolic",
    "source_record_type": "answer_trace",
    "mapping_method": "answer_trace_to_trajectory",
    "model_name": "reference_model_c",
    "trajectory_count": 1,
    "average_risk_score": 0.787044,
    "average_accuracy_rate": 0.2,
    "regime_counts": {
      "COLLAPSE": 1
    },
    "highest_risk_trajectory": "gsm_symbolic_answer_trace_collapse_like_001",
    "highest_risk_score": 0.787044
  }
]
```

---

## Risk Formula

The v9 risk score preserves the raw trajectory formula used by v3 through v8:

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

## Correctness Profile Rule

v9 tracks correctness as evidence.

It does not replace the structural risk score.

Each trajectory includes:

```text
event_count
correct_count
incorrect_count
accuracy_rate
correctness_changes
starts_correct
ends_correct
```

Important boundary:

```text
correctness_profile is evidence
risk_score is structural warning measurement
```

Correctness and structural risk may correlate.

They are not the same measurement.

---

## Aggregate Result

The aggregate v9 result was:

```text
aggregate_risk_score:    0.481561
aggregate_risk_regime:   DRIFT
aggregate_gate_action:   WATCH
aggregate_accuracy_rate: 0.480000
source_count:            1
model_count:             3
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
gsm_symbolic_answer_trace_collapse_like_001 -> 0.787044
```

Interpretation:

The aggregate result is DRIFT because the dataset contains a mixed set of trajectories.

The important result is that the answer-trace validator separated the five ordered traces into distinct risk regimes while preserving correctness evidence.

---

## Ordered Risk Progression

The validator produced the following progression:

```text
gsm_symbolic_answer_trace_stable_001               -> STABLE   -> 0.068278 -> PASS
gsm_symbolic_answer_trace_drift_001                -> DRIFT    -> 0.352772 -> WATCH
gsm_symbolic_answer_trace_borderline_critical_001  -> CRITICAL -> 0.561733 -> ESCALATE
gsm_symbolic_answer_trace_critical_001             -> CRITICAL -> 0.637978 -> ESCALATE
gsm_symbolic_answer_trace_collapse_like_001        -> COLLAPSE -> 0.787044 -> STOP
```

The borderline trajectory crossed the CRITICAL threshold:

```text
gsm_symbolic_answer_trace_borderline_critical_001 -> 0.561733
CRITICAL threshold                                -> 0.500000
margin above threshold                            -> 0.061733
```

---

## Accuracy Profile

The aggregate accuracy rate was:

```text
0.480000
```

Per trajectory:

```text
gsm_symbolic_answer_trace_stable_001               -> accuracy 1.000000
gsm_symbolic_answer_trace_drift_001                -> accuracy 0.600000
gsm_symbolic_answer_trace_borderline_critical_001  -> accuracy 0.400000
gsm_symbolic_answer_trace_critical_001             -> accuracy 0.200000
gsm_symbolic_answer_trace_collapse_like_001        -> accuracy 0.200000
```

The accuracy profile declines as structural risk rises in this bounded v9 dataset.

Correct reading:

```text
in this bounded dataset, structural risk and answer failure trend together
```

Incorrect reading:

```text
structural risk is identical to benchmark correctness
```

---

## Individual Results

### gsm_symbolic_answer_trace_stable_001

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

The stable answer trace remained below the DRIFT threshold.

Correctness stayed stable across all events.

---

### gsm_symbolic_answer_trace_drift_001

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

The drift answer trace crossed out of STABLE and entered DRIFT.

Correctness degraded but did not define the risk score.

---

### gsm_symbolic_answer_trace_borderline_critical_001

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

The borderline answer trace entered CRITICAL.

The transition and boundary signals are visible.

Correctness degradation is preserved as evidence, not silently converted into the risk score.

---

### gsm_symbolic_answer_trace_critical_001

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

The critical answer trace entered CRITICAL without requiring explicit COLLAPSE phase count.

The high structural pressure is visible through transition density, drift progression, boundary proximity, and collapse similarity.

---

### gsm_symbolic_answer_trace_collapse_like_001

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

The collapse-like answer trace entered COLLAPSE.

All warning flags were activated.

The highest-risk trajectory was correctly identified as:

```text
gsm_symbolic_answer_trace_collapse_like_001
```

---

## Structural Reading

The v9 result extends v8 by adding answer-trace and correctness fields.

v8 used:

```text
source_independence: external_source_verified
independence_method: direct_public_benchmark_record_mapping
benchmark_name: GSM-Symbolic
source_record_type: template_variant
mapping_method: template_variant_to_trajectory
```

v9 uses:

```text
source_independence: external_source_verified
independence_method: direct_answer_trace_mapping
benchmark_name: GSM-Symbolic
source_record_type: answer_trace
mapping_method: answer_trace_to_trajectory
```

This is a stronger answer-trace boundary step.

The correct structural reading is:

```text
the raw trajectory warning mechanism remains coherent over direct GSM-Symbolic answer-trace mappings
```

not:

```text
OMNIA solves GSM-Symbolic
```

---

## Main Finding

Safe claim:

```text
OMNIA-VALIDATION Level 3 v9 applied the raw trajectory warning mechanism
to direct GSM-Symbolic answer traces mapped into raw ordered structural events.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
tracked correctness profiles, and preserved model/source/benchmark boundaries.
```

---

## Important Limitation

This v9 result is still bounded.

It maps answer traces into raw trajectory events.

It does not directly evaluate official GSM-Symbolic benchmark runs.

It does not prove semantic correctness.

It does not claim benchmark solving.

Correct interpretation:

```text
Level 3 v9 validates the raw trajectory warning mechanism
on direct GSM-Symbolic answer-trace mappings.
```

Not:

```text
Level 3 v9 proves OMNIA solves GSM-Symbolic.
```

---

## What This Result Does Not Claim

This result does not claim:

```text
universal AI collapse prediction
semantic truth detection
GSM-Symbolic solving
official benchmark correctness scoring
domain-independent validity
production-level certification
final decision authority
model cognition detection
live runtime validation
correctness equals structural stability
wrong answer equals structural collapse
```

The result is valid only inside the tested v9 construction.

---

## Conclusion

Level 3 v9 passes as a direct answer-trace mapping step.

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

The strongest trajectory was:

```text
gsm_symbolic_answer_trace_collapse_like_001 -> COLLAPSE -> STOP
```

The decisive boundary condition is:

```text
source_independence: external_source_verified
independence_method: direct_answer_trace_mapping
benchmark_name: GSM-Symbolic
source_record_type: answer_trace
mapping_method: answer_trace_to_trajectory
```

Therefore, v9 is stronger than v8 as an answer-trace mapping step.

The next step is to replace reference answer traces with actual model outputs, real answer extraction records, or parsed benchmark files from source.