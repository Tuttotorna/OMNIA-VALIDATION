# Temporal Collapse Verified External-Source Raw Trajectory Validator — v7 Result

## Status

PASS.

The Level 3 v7 verified external-source raw trajectory validator executed successfully.

No runtime error was produced.

```text
STDERR: empty
RETURN CODE: 0
```

Input file:

```text
data/temporal_collapse_verified_external_source_raw_trajectories_v7.jsonl
```

Output file:

```text
results/temporal_collapse_verified_external_source_raw_trajectory_validator_v7.json
```

Validator script:

```text
examples/temporal_collapse_verified_external_source_raw_trajectory_validator_v7.py
```

---

## Purpose

This experiment moves Level 3 from declared external-source validation to verified external-source validation.

Level 3 v6 used:

```text
source_independence: external_source_declared
independence_method: prompt_perturbation_trace
```

Level 3 v7 uses:

```text
source_independence: external_source_verified
independence_method: public_benchmark_mapping
```

The source boundary is:

```text
GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

This does not claim that OMNIA solves GSM-Symbolic.

It only uses GSM-Symbolic as a public/documentable benchmark source from which raw ordered trajectory records are mapped.

```text
measurement != inference != decision
```

---

## Tested Boundary

The tested boundary is:

```text
verified external-source raw ordered trajectory records mapped from GSM-Symbolic
```

Source:

```text
gsm_symbolic_public_benchmark_v7
```

Source independence:

```text
external_source_verified
```

Independence method:

```text
public_benchmark_mapping
```

External source reference:

```text
GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

Correct reading:

```text
v7 validates the raw trajectory warning mechanism on GSM-Symbolic-derived structural trajectory records.
```

Incorrect reading:

```text
v7 proves that OMNIA solves GSM-Symbolic.
```

---

## Important Boundary Note

The v7 boundary is stronger than v6 because it names a public/documentable benchmark source.

However, this v7 dataset is still a mapped structural trajectory construction.

The correct claim is:

```text
GSM-Symbolic was used as a public-source reference boundary
for constructing raw ordered structural trajectory records.
```

The incorrect claim is:

```text
OMNIA directly evaluated official GSM-Symbolic model answers.
```

That direct evaluation would require actual GSM-Symbolic records, model outputs, and answer correctness traces.

---

## Input Dataset

The dataset contains five GSM-Symbolic-derived structural trajectories:

```text
gsm_symbolic_stable_001
gsm_symbolic_drift_001
gsm_symbolic_borderline_critical_001
gsm_symbolic_critical_001
gsm_symbolic_collapse_like_001
```

Each event contains:

```text
trajectory_id
step
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
mapping_notes
```

The validator groups events by `trajectory_id` and sorts each trajectory by `step`.

---

## Source Summary

The v7 source summary was:

```json
[
  {
    "source": "gsm_symbolic_public_benchmark_v7",
    "source_independence": "external_source_verified",
    "independence_method": "public_benchmark_mapping",
    "external_source_reference": "GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository",
    "trajectory_count": 5,
    "average_risk_score": 0.4647,
    "regime_counts": {
      "CRITICAL": 2,
      "COLLAPSE": 1,
      "DRIFT": 1,
      "STABLE": 1
    },
    "highest_risk_trajectory": "gsm_symbolic_collapse_like_001",
    "highest_risk_score": 0.817794
  }
]
```

---

## Risk Formula

The v7 risk score preserves the raw trajectory formula used by v3, v4, v5, and v6:

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

The aggregate v7 result was:

```text
aggregate_risk_score:  0.464700
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
gsm_symbolic_collapse_like_001 -> 0.817794
```

Interpretation:

The aggregate result is DRIFT because the dataset contains a mixed set of trajectories.

The main result is the coherent separation of risk regimes under a verified external-source benchmark boundary.

---

## Ordered Risk Progression

The validator produced the following progression:

```text
gsm_symbolic_stable_001               -> STABLE   -> 0.106344 -> PASS
gsm_symbolic_drift_001                -> DRIFT    -> 0.306183 -> WATCH
gsm_symbolic_borderline_critical_001  -> CRITICAL -> 0.508467 -> ESCALATE
gsm_symbolic_critical_001             -> CRITICAL -> 0.584711 -> ESCALATE
gsm_symbolic_collapse_like_001        -> COLLAPSE -> 0.817794 -> STOP
```

The borderline trajectory crossed the CRITICAL threshold:

```text
gsm_symbolic_borderline_critical_001 -> 0.508467
CRITICAL threshold                   -> 0.500000
margin above threshold               -> 0.008467
```

---

## Individual Results

### gsm_symbolic_stable_001

```text
risk_regime:   STABLE
risk_score:    0.106344
gate_action:   PASS
dominant_axis: transition_density
warning_flags: []
```

Signals:

```json
{
  "transition_density": 0.166667,
  "drift_progression": 0.072556,
  "boundary_proximity": 0.158333,
  "collapse_similarity": 0.062667,
  "irreversibility_signal": 0.0325
}
```

Interpretation:

The stable trajectory remained below the DRIFT threshold.

It shows mild signature variation but no structural warning escalation.

---

### gsm_symbolic_drift_001

```text
risk_regime:   DRIFT
risk_score:    0.306183
gate_action:   WATCH
dominant_axis: boundary_proximity
warning_flags: []
```

Signals:

```json
{
  "transition_density": 0.333333,
  "drift_progression": 0.263,
  "boundary_proximity": 0.475,
  "collapse_similarity": 0.211,
  "irreversibility_signal": 0.154167
}
```

Interpretation:

The drift trajectory crossed out of STABLE and entered DRIFT.

No hard warning flags were emitted.

---

### gsm_symbolic_borderline_critical_001

```text
risk_regime:   CRITICAL
risk_score:    0.508467
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
  "drift_progression": 0.417333,
  "boundary_proximity": 0.734167,
  "collapse_similarity": 0.353833,
  "irreversibility_signal": 0.363333
}
```

Interpretation:

The borderline GSM-Symbolic trajectory crossed into CRITICAL by a narrow margin.

The result exposes the boundary instead of hiding it.

---

### gsm_symbolic_critical_001

```text
risk_regime:   CRITICAL
risk_score:    0.584711
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
  "drift_progression": 0.503556,
  "boundary_proximity": 0.840833,
  "collapse_similarity": 0.431167,
  "irreversibility_signal": 0.493333
}
```

Interpretation:

The critical trajectory entered CRITICAL without requiring explicit COLLAPSE markers.

The validator emitted ESCALATE due to combined transition pressure, drift progression, and boundary proximity.

---

### gsm_symbolic_collapse_like_001

```text
risk_regime:   COLLAPSE
risk_score:    0.817794
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
  "drift_progression": 0.648222,
  "boundary_proximity": 0.9505,
  "collapse_similarity": 0.8561,
  "irreversibility_signal": 0.865
}
```

Interpretation:

The collapse-like GSM-Symbolic trajectory entered COLLAPSE.

All warning flags were activated.

The highest-risk trajectory was correctly identified as:

```text
gsm_symbolic_collapse_like_001
```

---

## Structural Reading

The v7 result extends v6 by using a public/documentable benchmark boundary.

v6 used:

```text
source_independence: external_source_declared
independence_method: prompt_perturbation_trace
```

v7 uses:

```text
source_independence: external_source_verified
independence_method: public_benchmark_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

This is a stronger source-boundary step.

The correct structural reading is:

```text
the raw trajectory warning mechanism remains coherent over GSM-Symbolic-derived structural trajectory records
```

not:

```text
OMNIA solves GSM-Symbolic
```

---

## Main Finding

Safe claim:

```text
OMNIA-VALIDATION Level 3 v7 applied the raw trajectory warning mechanism
to GSM-Symbolic-derived verified external-source raw ordered trajectory records.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
with the borderline trajectory crossing the CRITICAL threshold by a narrow margin.
```

---

## Important Limitation

This v7 result is still bounded.

It maps GSM-Symbolic-style benchmark perturbation structure into raw trajectory records.

It does not directly evaluate official GSM-Symbolic answer files.

It does not test model correctness.

It does not claim semantic solving.

Correct interpretation:

```text
Level 3 v7 validates the raw trajectory warning mechanism
on GSM-Symbolic-derived structural trajectory records.
```

Not:

```text
Level 3 v7 proves OMNIA solves GSM-Symbolic.
```

---

## What This Result Does Not Claim

This result does not claim:

```text
universal AI collapse prediction
semantic truth detection
GSM-Symbolic solving
model answer correctness
domain-independent validity
production-level certification
final decision authority
model cognition detection
live runtime validation
```

The result is valid only inside the tested v7 construction.

---

## Conclusion

Level 3 v7 passes as a verified external-source raw trajectory validation step.

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
gsm_symbolic_collapse_like_001 -> COLLAPSE -> STOP
```

The borderline trajectory crossed into CRITICAL by a narrow margin:

```text
gsm_symbolic_borderline_critical_001 -> 0.508467 -> CRITICAL
```

The decisive boundary condition is:

```text
source_independence: external_source_verified
independence_method: public_benchmark_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

Therefore, v7 is stronger than v6 as a verified public-source boundary.

The next step is to replace mapped GSM-Symbolic-style trajectory records with records derived directly from actual GSM-Symbolic files, model outputs, or answer perturbation traces.