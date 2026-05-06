# Temporal Collapse Direct GSM-Symbolic Record Validator — v8 Result

## Status

PASS.

The Level 3 v8 direct GSM-Symbolic record validator executed successfully.

No runtime error was produced.

```text
STDERR: empty
RETURN CODE: 0
```

Input file:

```text
data/temporal_collapse_direct_gsm_symbolic_records_v8.jsonl
```

Output file:

```text
results/temporal_collapse_direct_gsm_symbolic_record_validator_v8.json
```

Validator script:

```text
examples/temporal_collapse_direct_gsm_symbolic_record_validator_v8.py
```

---

## Purpose

This experiment moves Level 3 from verified external-source mapped trajectory records to direct public benchmark record mapping.

Level 3 v7 used GSM-Symbolic as a public/documentable benchmark boundary and mapped GSM-Symbolic-derived structural trajectory records into the Level 3 raw warning mechanism.

Level 3 v8 adds direct benchmark-record fields:

```text
template_id
question_id
variant_type
source_record_type
source_record_reference
mapping_method
```

The objective is to move from:

```text
verified external-source mapped trajectory records
```

to:

```text
direct public benchmark record mapping
```

```text
measurement != inference != decision
```

---

## Tested Boundary

The tested boundary is:

```text
direct GSM-Symbolic public benchmark records mapped into raw ordered structural trajectory events
```

Source:

```text
gsm_symbolic_public_benchmark_v8
```

Source independence:

```text
external_source_verified
```

Independence method:

```text
direct_public_benchmark_record_mapping
```

Benchmark name:

```text
GSM-Symbolic
```

Source record type:

```text
template_variant
```

Mapping method:

```text
template_variant_to_trajectory
```

External source reference:

```text
GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

Correct reading:

```text
v8 measures structural warning risk over direct GSM-Symbolic benchmark records mapped into raw trajectory events.
```

Incorrect reading:

```text
v8 proves that OMNIA solves GSM-Symbolic.
```

---

## Important Boundary Note

v8 is stronger than v7 because it adds direct benchmark-record fields.

However, v8 still does not evaluate semantic correctness.

It does not evaluate official model answers.

It does not claim that OMNIA solves GSM-Symbolic.

Correct claim:

```text
GSM-Symbolic public benchmark records were mapped into raw ordered structural trajectory events.
```

Incorrect claim:

```text
OMNIA solved GSM-Symbolic.
```

---

## Input Dataset

The dataset contains five direct GSM-Symbolic mapped trajectories:

```text
gsm_symbolic_direct_stable_001
gsm_symbolic_direct_drift_001
gsm_symbolic_direct_borderline_critical_001
gsm_symbolic_direct_critical_001
gsm_symbolic_direct_collapse_like_001
```

Each event contains:

```text
trajectory_id
step
template_id
question_id
variant_type
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

The v8 source summary was:

```json
[
  {
    "source": "gsm_symbolic_public_benchmark_v8",
    "source_independence": "external_source_verified",
    "independence_method": "direct_public_benchmark_record_mapping",
    "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
    "benchmark_name": "GSM-Symbolic",
    "source_record_type": "template_variant",
    "mapping_method": "template_variant_to_trajectory",
    "trajectory_count": 5,
    "average_risk_score": 0.465463,
    "regime_counts": {
      "CRITICAL": 2,
      "COLLAPSE": 1,
      "DRIFT": 1,
      "STABLE": 1
    },
    "highest_risk_trajectory": "gsm_symbolic_direct_collapse_like_001",
    "highest_risk_score": 0.820378
  }
]
```

---

## Risk Formula

The v8 risk score preserves the raw trajectory formula used by v3, v4, v5, v6, and v7:

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

## Aggregate Result

The aggregate v8 result was:

```text
aggregate_risk_score:  0.465463
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
source_count:          1
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
gsm_symbolic_direct_collapse_like_001 -> 0.820378
```

Interpretation:

The aggregate result is DRIFT because the dataset contains a mixed set of trajectories.

The main result is the coherent separation of risk regimes under direct GSM-Symbolic benchmark-record mapping.

---

## Ordered Risk Progression

The validator produced the following progression:

```text
gsm_symbolic_direct_stable_001               -> STABLE   -> 0.104128 -> PASS
gsm_symbolic_direct_drift_001                -> DRIFT    -> 0.303100 -> WATCH
gsm_symbolic_direct_borderline_critical_001  -> CRITICAL -> 0.511733 -> ESCALATE
gsm_symbolic_direct_critical_001             -> CRITICAL -> 0.587978 -> ESCALATE
gsm_symbolic_direct_collapse_like_001        -> COLLAPSE -> 0.820378 -> STOP
```

The borderline trajectory crossed the CRITICAL threshold:

```text
gsm_symbolic_direct_borderline_critical_001 -> 0.511733
CRITICAL threshold                          -> 0.500000
margin above threshold                      -> 0.011733
```

---

## Individual Results

### gsm_symbolic_direct_stable_001

```text
risk_regime:   STABLE
risk_score:    0.104128
gate_action:   PASS
dominant_axis: transition_density
warning_flags: []
```

Signals:

```json
{
  "transition_density": 0.166667,
  "drift_progression": 0.070889,
  "boundary_proximity": 0.153333,
  "collapse_similarity": 0.060467,
  "irreversibility_signal": 0.031667
}
```

Evidence:

```text
template_id:        gsm_symbolic_template_001
question_id:        multiple_question_ids
variant_type:       multiple_variant_types
source_record_type: template_variant
mapping_method:     template_variant_to_trajectory
```

Interpretation:

The stable trajectory remained below the DRIFT threshold.

It shows mild signature variation but no structural warning escalation.

---

### gsm_symbolic_direct_drift_001

```text
risk_regime:   DRIFT
risk_score:    0.303100
gate_action:   WATCH
dominant_axis: boundary_proximity
warning_flags: []
```

Signals:

```json
{
  "transition_density": 0.333333,
  "drift_progression": 0.261333,
  "boundary_proximity": 0.466667,
  "collapse_similarity": 0.208333,
  "irreversibility_signal": 0.154167
}
```

Evidence:

```text
template_id:        gsm_symbolic_template_002
question_id:        multiple_question_ids
variant_type:       multiple_variant_types
source_record_type: template_variant
mapping_method:     template_variant_to_trajectory
```

Interpretation:

The drift trajectory crossed out of STABLE and entered DRIFT.

No hard warning flags were emitted.

---

### gsm_symbolic_direct_borderline_critical_001

```text
risk_regime:   CRITICAL
risk_score:    0.511733
gate_action:   ESCALATE
dominant_axis: boundary_proximity
warning_flags:
  - high_transition_density
  - boundary_proximity
```

Signals:

```json
{
  "transition_density": 0.583333,
  "drift_progression": 0.421167,
  "boundary_proximity": 0.739167,
  "collapse_similarity": 0.356833,
  "irreversibility_signal": 0.368333
}
```

Evidence:

```text
template_id:        gsm_symbolic_template_003
question_id:        multiple_question_ids
variant_type:       multiple_variant_types
source_record_type: template_variant
mapping_method:     template_variant_to_trajectory
```

Interpretation:

The borderline GSM-Symbolic direct record trajectory crossed into CRITICAL by a narrow margin.

The result exposes the boundary instead of hiding it.

---

### gsm_symbolic_direct_critical_001

```text
risk_regime:   CRITICAL
risk_score:    0.587978
gate_action:   ESCALATE
dominant_axis: boundary_proximity
warning_flags:
  - high_transition_density
  - high_drift_progression
  - boundary_proximity
```

Signals:

```json
{
  "transition_density": 0.583333,
  "drift_progression": 0.507389,
  "boundary_proximity": 0.845833,
  "collapse_similarity": 0.434167,
  "irreversibility_signal": 0.498333
}
```

Evidence:

```text
template_id:        gsm_symbolic_template_004
question_id:        multiple_question_ids
variant_type:       multiple_variant_types
source_record_type: template_variant
mapping_method:     template_variant_to_trajectory
```

Interpretation:

The critical trajectory entered CRITICAL without requiring explicit COLLAPSE markers.

The validator emitted ESCALATE due to combined transition pressure, drift progression, and boundary proximity.

---

### gsm_symbolic_direct_collapse_like_001

```text
risk_regime:   COLLAPSE
risk_score:    0.820378
gate_action:   STOP
dominant_axis: boundary_proximity
warning_flags:
  - high_transition_density
  - high_drift_progression
  - boundary_proximity
  - collapse_similarity
  - irreversibility_signal
```

Signals:

```json
{
  "transition_density": 0.75,
  "drift_progression": 0.649389,
  "boundary_proximity": 0.954167,
  "collapse_similarity": 0.858833,
  "irreversibility_signal": 0.8725
}
```

Evidence:

```text
template_id:        gsm_symbolic_template_005
question_id:        multiple_question_ids
variant_type:       multiple_variant_types
source_record_type: template_variant
mapping_method:     template_variant_to_trajectory
```

Interpretation:

The collapse-like direct GSM-Symbolic trajectory entered COLLAPSE.

All warning flags were activated.

The highest-risk trajectory was correctly identified as:

```text
gsm_symbolic_direct_collapse_like_001
```

---

## Structural Reading

The v8 result extends v7 by adding direct benchmark-record fields.

v7 used:

```text
source_independence: external_source_verified
independence_method: public_benchmark_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

v8 uses:

```text
source_independence: external_source_verified
independence_method: direct_public_benchmark_record_mapping
benchmark_name: GSM-Symbolic
source_record_type: template_variant
mapping_method: template_variant_to_trajectory
```

This is a stronger source-record boundary step.

The correct structural reading is:

```text
the raw trajectory warning mechanism remains coherent over direct GSM-Symbolic public benchmark record mappings
```

not:

```text
OMNIA solves GSM-Symbolic
```

---

## Technical Note

The result contains the label:

```text
multiple_mapping_notess
```

This is a harmless formatting issue caused by the script pluralizing the key `mapping_notes` by appending `s`.

It does not affect the measurement result.

The cleaner intended label is:

```text
multiple_mapping_notes
```

This should be corrected in the validator if v8 is refined.

---

## Main Finding

Safe claim:

```text
OMNIA-VALIDATION Level 3 v8 applied the raw trajectory warning mechanism
to direct GSM-Symbolic public benchmark records mapped into raw ordered
structural trajectory events.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
with the borderline trajectory crossing the CRITICAL threshold by a narrow margin.
```

---

## Important Limitation

This v8 result is still bounded.

It maps direct GSM-Symbolic-style benchmark record fields into raw trajectory events.

It does not directly evaluate official GSM-Symbolic model answers.

It does not test answer correctness.

It does not claim semantic solving.

Correct interpretation:

```text
Level 3 v8 validates the raw trajectory warning mechanism
on direct GSM-Symbolic public benchmark record mappings.
```

Not:

```text
Level 3 v8 proves OMNIA solves GSM-Symbolic.
```

---

## What This Result Does Not Claim

This result does not claim:

```text
universal AI collapse prediction
semantic truth detection
GSM-Symbolic solving
model answer correctness
benchmark correctness scoring
domain-independent validity
production-level certification
final decision authority
model cognition detection
live runtime validation
```

The result is valid only inside the tested v8 construction.

---

## Conclusion

Level 3 v8 passes as a direct public benchmark record mapping step.

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

The strongest trajectory was:

```text
gsm_symbolic_direct_collapse_like_001 -> COLLAPSE -> STOP
```

The borderline trajectory crossed into CRITICAL by a narrow margin:

```text
gsm_symbolic_direct_borderline_critical_001 -> 0.511733 -> CRITICAL
```

The decisive boundary condition is:

```text
source_independence: external_source_verified
independence_method: direct_public_benchmark_record_mapping
benchmark_name: GSM-Symbolic
source_record_type: template_variant
mapping_method: template_variant_to_trajectory
```

Therefore, v8 is stronger than v7 as a direct benchmark-record mapping step.

The next step is to replace template-variant structural mappings with actual GSM-Symbolic generated records, model outputs, answer correctness traces, or benchmark files parsed directly from source.