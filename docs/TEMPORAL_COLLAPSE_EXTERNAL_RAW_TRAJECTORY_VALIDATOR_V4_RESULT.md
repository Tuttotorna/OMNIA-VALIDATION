# Temporal Collapse External Raw Trajectory Validator — v4 Result

## Status

PASS.

The Level 3 v4 external raw trajectory validator executed successfully.

The script read the external-style raw JSONL trajectory dataset.

No runtime error was produced.

```text
STDERR: empty
RETURN CODE: 0
```

Input file:

```text
data/temporal_collapse_external_raw_trajectories_v4.jsonl
```

Output file:

```text
results/temporal_collapse_external_raw_trajectory_validator_v4.json
```

---

## Purpose

This experiment moves Level 3 from internal raw reference trajectories to external-style raw ordered trajectory records.

Level 3 v3 validated the raw trajectory warning mechanism over bounded internal reference trajectories.

Level 3 v4 applies the same raw trajectory warning mechanism to external-style trajectories with explicit source labels and source-independence tracking.

The objective is to move from:

```text
raw reference trajectory warning
```

to:

```text
external-style raw trajectory validation
```

```text
measurement != inference != decision
```

---

## Tested Boundary

This v4 result is bounded.

The tested boundary is:

```text
external-style raw ordered trajectory records
```

Source:

```text
external_style_generator_v4
```

Source independence:

```text
not_verified
```

This is important.

A source label alone does not prove independence.

Therefore this result must be read as:

```text
external-style validation
```

Not as:

```text
verified independent validation
```

---

## Input Dataset

The dataset contains five external-style raw trajectories:

```text
external_stable_001
external_drift_001
external_borderline_critical_001
external_critical_001
external_collapse_like_001
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
```

The validator groups events by `trajectory_id` and sorts each trajectory by `step`.

---

## Source Summary

The v4 source summary was:

```json
[
  {
    "source": "external_style_generator_v4",
    "source_independence": "not_verified",
    "trajectory_count": 5,
    "average_risk_score": 0.468439,
    "regime_counts": {
      "CRITICAL": 2,
      "COLLAPSE": 1,
      "DRIFT": 1,
      "STABLE": 1
    },
    "highest_risk_trajectory": "external_collapse_like_001",
    "highest_risk_score": 0.824306
  }
]
```

Interpretation:

All trajectories came from one external-style source.

The source independence was explicitly marked as not verified.

This preserves the correct epistemic boundary.

---

## Risk Formula

The v4 risk score preserves the v3 raw trajectory formula:

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

The aggregate v4 result was:

```text
aggregate_risk_score:  0.468439
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
external_collapse_like_001 -> 0.824306
```

Interpretation:

The aggregate result is DRIFT because the dataset contains a mixed set of trajectories.

The main result is not the aggregate score alone.

The main result is that the validator separated external-style trajectories into the expected structural regimes while preserving source-independence limits.

---

## Ordered Risk Progression

The validator produced the following progression:

```text
external_stable_001               -> STABLE    -> 0.040583 -> PASS
external_drift_001                -> DRIFT     -> 0.321306 -> WATCH
external_borderline_critical_001  -> CRITICAL  -> 0.536222 -> ESCALATE
external_critical_001             -> CRITICAL  -> 0.619778 -> ESCALATE
external_collapse_like_001        -> COLLAPSE  -> 0.824306 -> STOP
```

This progression is coherent.

The external-style stable trajectory remained STABLE.

The external-style drift trajectory entered DRIFT.

The borderline critical and critical trajectories entered CRITICAL.

The collapse-like trajectory entered COLLAPSE.

---

## Individual Results

### external_stable_001

```text
source:              external_style_generator_v4
source_independence: not_verified
risk_regime:         STABLE
risk_score:          0.040583
gate_action:         PASS
dominant_axis:       boundary_proximity
warning_flags:       []
```

Signals:

```json
{
  "transition_density": 0.0,
  "drift_progression": 0.026667,
  "boundary_proximity": 0.0975,
  "collapse_similarity": 0.0355,
  "irreversibility_signal": 0.02
}
```

Evidence:

```json
{
  "signature_changes": 0.0,
  "cluster_changes": 0.0,
  "phase_changes": 0.0,
  "delta_early_mean": 0.045,
  "delta_late_mean": 0.055,
  "iri_early_mean": 0.01,
  "iri_late_mean": 0.02,
  "min_boundary_distance": 0.9,
  "max_boundary_proximity": 0.1,
  "collapse_phase_count": 0,
  "source": "external_style_generator_v4",
  "source_independence": "not_verified"
}
```

Interpretation:

The stable trajectory remained structurally consistent.

No warning flags were emitted.

---

### external_drift_001

```text
source:              external_style_generator_v4
source_independence: not_verified
risk_regime:         DRIFT
risk_score:          0.321306
gate_action:         WATCH
dominant_axis:       boundary_proximity
warning_flags:       []
```

Signals:

```json
{
  "transition_density": 0.444444,
  "drift_progression": 0.238333,
  "boundary_proximity": 0.4725,
  "collapse_similarity": 0.2045,
  "irreversibility_signal": 0.155
}
```

Evidence:

```json
{
  "signature_changes": 0.666667,
  "cluster_changes": 0.333333,
  "phase_changes": 0.333333,
  "delta_early_mean": 0.125,
  "delta_late_mean": 0.325,
  "iri_early_mean": 0.045,
  "iri_late_mean": 0.14,
  "min_boundary_distance": 0.5,
  "max_boundary_proximity": 0.5,
  "collapse_phase_count": 0,
  "source": "external_style_generator_v4",
  "source_independence": "not_verified"
}
```

Interpretation:

The drift trajectory crossed out of STABLE and entered DRIFT.

The score was driven by moderate transition density, increasing delta, and boundary proximity.

No hard warning flag was emitted.

---

### external_borderline_critical_001

```text
source:              external_style_generator_v4
source_independence: not_verified
risk_regime:         CRITICAL
risk_score:          0.536222
gate_action:         ESCALATE
dominant_axis:       transition_density
warning_flags:
  - high_transition_density
  - boundary_proximity
```

Signals:

```json
{
  "transition_density": 0.777778,
  "drift_progression": 0.393333,
  "boundary_proximity": 0.73,
  "collapse_similarity": 0.342,
  "irreversibility_signal": 0.34
}
```

Evidence:

```json
{
  "signature_changes": 1.0,
  "cluster_changes": 0.666667,
  "phase_changes": 0.666667,
  "delta_early_mean": 0.215,
  "delta_late_mean": 0.545,
  "iri_early_mean": 0.105,
  "iri_late_mean": 0.31,
  "min_boundary_distance": 0.24,
  "max_boundary_proximity": 0.76,
  "collapse_phase_count": 0,
  "source": "external_style_generator_v4",
  "source_independence": "not_verified"
}
```

Interpretation:

The borderline critical trajectory entered CRITICAL.

The validator emitted ESCALATE without requiring explicit COLLAPSE phase markers.

This is useful because it shows pre-collapse boundary pressure.

---

### external_critical_001

```text
source:              external_style_generator_v4
source_independence: not_verified
risk_regime:         CRITICAL
risk_score:          0.619778
gate_action:         ESCALATE
dominant_axis:       transition_density
warning_flags:
  - high_transition_density
  - boundary_proximity
```

Signals:

```json
{
  "transition_density": 0.888889,
  "drift_progression": 0.4625,
  "boundary_proximity": 0.8125,
  "collapse_similarity": 0.4045,
  "irreversibility_signal": 0.4525
}
```

Evidence:

```json
{
  "signature_changes": 1.0,
  "cluster_changes": 1.0,
  "phase_changes": 0.666667,
  "delta_early_mean": 0.27,
  "delta_late_mean": 0.655,
  "iri_early_mean": 0.135,
  "iri_late_mean": 0.415,
  "min_boundary_distance": 0.16,
  "max_boundary_proximity": 0.84,
  "collapse_phase_count": 0,
  "source": "external_style_generator_v4",
  "source_independence": "not_verified"
}
```

Interpretation:

The critical trajectory entered a high-risk structural regime.

The warning layer detected strong transition pressure and boundary proximity.

No explicit collapse phase was required.

---

### external_collapse_like_001

```text
source:              external_style_generator_v4
source_independence: not_verified
risk_regime:         COLLAPSE
risk_score:          0.824306
gate_action:         STOP
dominant_axis:       boundary_proximity
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
  "transition_density": 0.777778,
  "drift_progression": 0.635,
  "boundary_proximity": 0.9525,
  "collapse_similarity": 0.8685,
  "irreversibility_signal": 0.865
}
```

Evidence:

```json
{
  "signature_changes": 1.0,
  "cluster_changes": 0.666667,
  "phase_changes": 0.666667,
  "delta_early_mean": 0.395,
  "delta_late_mean": 0.915,
  "iri_early_mean": 0.245,
  "iri_late_mean": 0.81,
  "min_boundary_distance": 0.03,
  "max_boundary_proximity": 0.97,
  "collapse_phase_count": 2,
  "source": "external_style_generator_v4",
  "source_independence": "not_verified"
}
```

Interpretation:

The collapse-like trajectory entered COLLAPSE.

All warning flags were activated.

The highest-risk trajectory was correctly identified as `external_collapse_like_001`.

---

## Structural Reading

The v4 result extends v3 in one important direction.

v3 showed that the raw trajectory warning mechanism works on bounded internal reference trajectories.

v4 shows that the same mechanism remains coherent on external-style raw ordered trajectory records.

However, v4 does not prove independent validation because source independence is explicitly marked:

```text
not_verified
```

The structural result is therefore:

```text
mechanism coherent beyond v3 reference dataset
```

not:

```text
independently verified universal behavior
```

---

## Main Finding

Safe claim:

```text
OMNIA-VALIDATION Level 3 v4 applied the v3 raw trajectory warning mechanism
to external-style raw ordered trajectory records.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE-like regimes,
while explicitly marking source independence as not verified.
```

---

## Important Limitation

This v4 result is still bounded.

The trajectories are external-style records generated for validation.

Their source independence is not verified.

Correct interpretation:

```text
Level 3 v4 validates the raw trajectory warning mechanism
on external-style raw ordered trajectory records with source independence
explicitly marked as not verified.
```

Not:

```text
Level 3 v4 proves independent external validation.
```

---

## What This Result Does Not Claim

This result does not claim:

```text
universal AI collapse prediction
semantic truth detection
domain-independent validity
production-level certification
final decision authority
model cognition detection
verified source independence
live runtime validation
```

The result is valid only inside the tested v4 construction.

---

## Conclusion

Level 3 v4 passes as an external-style raw trajectory validation step.

The validator produced a coherent regime separation:

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
external_collapse_like_001 -> COLLAPSE -> STOP
```

The decisive boundary condition is preserved:

```text
source_independence: not_verified
```

Therefore, v4 is a successful external-style validation, not yet a verified independent validation.

The next step is to test the validator on genuinely independent raw trajectory records from another generator, model, benchmark, or externally produced trace source.