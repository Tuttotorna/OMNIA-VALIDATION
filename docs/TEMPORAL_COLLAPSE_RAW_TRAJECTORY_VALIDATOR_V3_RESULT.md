# Temporal Collapse Raw Trajectory Validator — v3 Result

## Status

PASS.

The Level 3 v3 raw trajectory validator executed successfully.

The script created and read the raw JSONL trajectory dataset.

No runtime error was produced.

```text
STDERR: empty
RETURN CODE: 0
```

Input file:

```text
data/temporal_collapse_raw_trajectories_v3.jsonl
```

Output file:

```text
results/temporal_collapse_raw_trajectory_validator_v3.json
```

---

## Purpose

This experiment moves Level 3 from ordered stage summaries to raw ordered trajectory records.

Level 3 v0 tested synthetic reference trajectories.

Level 3 v1 applied warning measurement to Level 2-derived result snapshots.

Level 3 v2 evaluated the Level 2 temporal-collapse chain as an ordered stage trajectory.

Level 3 v3 reads raw ordered trajectory events directly.

The objective is to move from:

```text
stage-summary trajectory warning
```

to:

```text
raw trajectory warning
```

```text
measurement != inference != decision
```

---

## Tested Boundary

This v3 result is bounded.

The tested boundary is:

```text
raw ordered trajectory records in JSONL format
```

The dataset contains four bounded reference trajectories:

```text
raw_stable_001
raw_drift_001
raw_critical_001
raw_collapse_like_001
```

This is not universal collapse prediction.

This is not semantic truth detection.

This is not production certification.

It is a raw ordered trajectory warning measurement over a bounded reference dataset.

---

## Input Schema

Each raw trajectory event contains:

```text
trajectory_id
step
signature
cluster
delta
iri
boundary_distance
phase
```

The validator groups events by `trajectory_id` and sorts each trajectory by `step`.

The measured trajectory structure is therefore ordered.

---

## Risk Formula

The v3 risk score is computed from five visible signals:

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

The aggregate v3 result was:

```text
aggregate_risk_score:  0.424257
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
```

Regime counts:

```text
STABLE   -> 1
DRIFT    -> 1
CRITICAL -> 1
COLLAPSE -> 1
```

Highest-risk trajectory:

```text
raw_collapse_like_001 -> 0.817056
```

Interpretation:

The aggregate result is DRIFT because the dataset intentionally contains one trajectory from each regime.

The aggregate is not the main scientific result.

The main result is that the validator separated all four bounded reference trajectories into the expected structural regimes.

---

## Ordered Risk Progression

The validator produced the following ordered progression:

```text
raw_stable_001         -> STABLE    -> 0.033417 -> PASS
raw_drift_001          -> DRIFT     -> 0.277833 -> WATCH
raw_critical_001       -> CRITICAL  -> 0.568722 -> ESCALATE
raw_collapse_like_001  -> COLLAPSE  -> 0.817056 -> STOP
```

Risk score progression:

```text
0.033417 -> 0.277833 -> 0.568722 -> 0.817056
```

This is the central v3 result.

The raw trajectory validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes using ordered event records.

---

## Individual Results

### raw_stable_001

```text
risk_regime:   STABLE
risk_score:    0.033417
gate_action:   PASS
dominant_axis: boundary_proximity
warning_flags: []
```

Signals:

```json
{
  "transition_density": 0.0,
  "drift_progression": 0.023333,
  "boundary_proximity": 0.0775,
  "collapse_similarity": 0.0295,
  "irreversibility_signal": 0.02
}
```

Evidence:

```json
{
  "signature_changes": 0.0,
  "cluster_changes": 0.0,
  "phase_changes": 0.0,
  "delta_early_mean": 0.035,
  "delta_late_mean": 0.045,
  "iri_early_mean": 0.01,
  "iri_late_mean": 0.02,
  "min_boundary_distance": 0.92,
  "max_boundary_proximity": 0.08,
  "collapse_phase_count": 0
}
```

Interpretation:

The stable trajectory remained structurally consistent.

No transition pressure, collapse phase, or relevant boundary pressure was detected.

---

### raw_drift_001

```text
risk_regime:   DRIFT
risk_score:    0.277833
gate_action:   WATCH
dominant_axis: boundary_proximity
warning_flags: []
```

Signals:

```json
{
  "transition_density": 0.333333,
  "drift_progression": 0.215833,
  "boundary_proximity": 0.4325,
  "collapse_similarity": 0.1845,
  "irreversibility_signal": 0.1375
}
```

Evidence:

```json
{
  "signature_changes": 0.333333,
  "cluster_changes": 0.333333,
  "phase_changes": 0.333333,
  "delta_early_mean": 0.11,
  "delta_late_mean": 0.295,
  "iri_early_mean": 0.045,
  "iri_late_mean": 0.125,
  "min_boundary_distance": 0.55,
  "max_boundary_proximity": 0.45,
  "collapse_phase_count": 0
}
```

Interpretation:

The drift trajectory crossed out of STABLE but remained below CRITICAL.

The score was driven by moderate transition density and increasing late delta.

No hard warning flag was emitted.

---

### raw_critical_001

```text
risk_regime:   CRITICAL
risk_score:    0.568722
gate_action:   ESCALATE
dominant_axis: transition_density
warning_flags:
  - high_transition_density
  - boundary_proximity
```

Signals:

```json
{
  "transition_density": 0.777778,
  "drift_progression": 0.440833,
  "boundary_proximity": 0.77,
  "collapse_similarity": 0.374,
  "irreversibility_signal": 0.39
}
```

Evidence:

```json
{
  "signature_changes": 1.0,
  "cluster_changes": 0.666667,
  "phase_changes": 0.666667,
  "delta_early_mean": 0.24,
  "delta_late_mean": 0.615,
  "iri_early_mean": 0.12,
  "iri_late_mean": 0.36,
  "min_boundary_distance": 0.2,
  "max_boundary_proximity": 0.8,
  "collapse_phase_count": 0
}
```

Interpretation:

The critical trajectory entered a high-risk regime without requiring collapse-phase markers.

High transition density and boundary proximity were sufficient to trigger ESCALATE.

This is important because v3 can detect critical pre-collapse deformation before explicit collapse appears.

---

### raw_collapse_like_001

```text
risk_regime:   COLLAPSE
risk_score:    0.817056
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
  "transition_density": 0.777778,
  "drift_progression": 0.635,
  "boundary_proximity": 0.94,
  "collapse_similarity": 0.86,
  "irreversibility_signal": 0.845
}
```

Evidence:

```json
{
  "signature_changes": 1.0,
  "cluster_changes": 0.666667,
  "phase_changes": 0.666667,
  "delta_early_mean": 0.37,
  "delta_late_mean": 0.9,
  "iri_early_mean": 0.24,
  "iri_late_mean": 0.79,
  "min_boundary_distance": 0.04,
  "max_boundary_proximity": 0.96,
  "collapse_phase_count": 2
}
```

Interpretation:

The collapse-like trajectory reached the COLLAPSE regime.

All warning flags were activated.

The validator detected high transition density, high drift progression, strong boundary proximity, high collapse similarity, and high irreversibility signal.

---

## Structural Reading

The v3 result confirms the Level 3 progression:

```text
v0 -> synthetic warning
v1 -> Level 2-derived snapshot warning
v2 -> ordered stage-chain warning
v3 -> raw ordered trajectory warning
```

The v3 validator is stronger than v0, v1, and v2 because it reads ordered events directly.

It preserves:

```text
step order
signature transitions
cluster transitions
phase transitions
delta progression
iri progression
boundary proximity
collapse-phase count
```

The output is not only a score.

It is:

```text
score + regime + gate action + transition evidence
```

This makes the result inspectable and falsifiable.

---

## Main Finding

Safe claim:

```text
OMNIA-VALIDATION Level 3 v3 validated raw ordered trajectory warning
over four bounded reference trajectories.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes
using visible structural signals, explicit thresholds, and inspectable
transition evidence.
```

---

## Important Limitation

This v3 result is still bounded.

The raw trajectories are controlled reference trajectories.

They are not yet external model logs, live runtime traces, or independently sourced trajectory datasets.

Correct interpretation:

```text
Level 3 v3 validates the raw ordered trajectory warning mechanism
on bounded reference trajectories.
```

Not:

```text
Level 3 v3 proves universal AI collapse prediction.
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
live runtime validation
```

The result is valid only inside the tested v3 construction.

---

## Conclusion

Level 3 v3 passes as a raw ordered trajectory validator over bounded reference trajectories.

The validator correctly separated the four target regimes:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
```

The key result is the monotonic risk progression:

```text
0.033417 -> 0.277833 -> 0.568722 -> 0.817056
```

This is the first Level 3 result where the warning layer operates directly over raw ordered trajectory records instead of synthetic summaries, Level 2 snapshots, or ordered stage summaries.

The next step is to test v3 against external or independently generated raw trajectory records.