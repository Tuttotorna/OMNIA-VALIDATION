# Cross-Gate Disagreement Stability v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Cross-Gate Conflict Stability
```

---

## Purpose

The previous experiment showed that cross-gate disagreement exists.

This experiment asks a stronger question:

does cross-gate disagreement remain stable across populations?

Core boundary:

```text
measurement != inference != decision
```

This experiment evaluates stability of:

- disagreement regimes
- contradiction regimes
- arbitration behavior
- severity spread
- signal variance

across many random seeds.

---

## Experiment File

```text
examples/cross_gate_disagreement_stability_v0.py
```

Result file:

```text
results/cross_gate_disagreement_stability_v0.json
```

Reproduction command:

```text
python examples/cross_gate_disagreement_stability_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

seed_count = 20
systems_per_seed = 1500
total_system_count = 30000

pass_seed_count = 20
check_seed_count = 0
```

All tested seeds passed.

The disagreement structure remained stable across:

```text
30000 synthetic external-style systems
```

---

## High Disagreement Stability

```text
high_disagreement_count:

mean = 863.7
min = 841
max = 902
```

High disagreement remained dominant across all seeds.

This is structurally important.

The disagreement regime is not an isolated random artifact.

---

## Medium And Low Disagreement Stability

```text
medium_disagreement_count:

mean = 619.9
min = 580
max = 645
```

```text
low_disagreement_count:

mean = 16.4
min = 10
max = 25
```

Low disagreement remained rare.

Most systems consistently fell into:

- medium disagreement
- high disagreement

rather than low disagreement.

---

## Contradiction Stability

```text
contradiction_count:

mean = 550.55
min = 523
max = 570
```

Contradiction remained structurally persistent.

This means many systems continued to produce:

```text
PASS
```

from at least one gate while simultaneously producing:

```text
COLLAPSE
```

from another gate.

This is the strongest possible gate conflict.

---

## Unanimity Stability

```text
unanimous_count:

mean = 0.1
min = 0
max = 1
```

Almost no systems produced full agreement across all gates.

This confirms:

```text
the gate family is non-redundant
```

---

## Unique Action Stability

```text
mean_unique_action_count:

mean = 3.050433333333
min = 3.026666666667
max = 3.082000000000
```

Most systems consistently triggered:

```text
~3 distinct gate actions simultaneously
```

This strongly supports:

```text
multi-signal conflict persistence
```

---

## Severity Spread Stability

```text
mean_severity_spread:

mean = 2.931833333333
min = 2.903333333333
max = 2.969333333333
```

Severity spread remained highly stable.

The variation across seeds was very small.

This suggests that arbitration conflict intensity is not random drift.

---

## Severity Variance Stability

```text
mean_severity_variance:

mean = 1.373397333333
min = 1.354346666667
max = 1.394240000000
```

Variance also remained stable across populations.

This confirms that:

```text
cross-gate conflict geometry persists across seeds
```

---

## Arbitration Stability

### PASS Rate

```text
pass_rate:

mean = 0.102333333333
min = 0.082000000000
max = 0.123333333333
```

### RETRY Rate

```text
retry_rate:

mean = 0.317166666667
min = 0.298000000000
max = 0.337333333333
```

### FLAG Rate

```text
flag_rate:

mean = 0.001400000000
min = 0.000000000000
max = 0.003333333333
```

### ESCALATE Rate

```text
escalate_rate:

mean = 0.438266666667
min = 0.424000000000
max = 0.452000000000
```

### COLLAPSE Rate

```text
collapse_rate:

mean = 0.140833333333
min = 0.132000000000
max = 0.158000000000
```

The dominant arbitration action remained:

```text
ESCALATE
```

This is coherent.

When multiple gates disagree strongly, escalation dominates.

---

## Important Finding

The most important result is:

```text
cross-gate disagreement is stable across seeds
```

Key persistent facts:

```text
high disagreement remains dominant
contradictions remain frequent
unanimity remains near-zero
~3 simultaneous actions remain typical
ESCALATE remains dominant
```

This supports the idea that:

```text
structural arbitration is necessary
```

rather than:

```text
single-threshold gating
```

---

## Interpretation

The experiment suggests that structural signals naturally produce:

- conflicting evaluations
- conflicting severities
- conflicting intervention actions

These conflicts persist even when populations change.

Therefore:

```text
multi-gate disagreement is not random instability
```

It appears to be a stable structural property of the tested signal family.

---

## What This Confirms

This experiment supports:

- disagreement persistence across seeds
- contradiction persistence across seeds
- arbitration stability
- non-redundant gate behavior
- stable escalation regimes
- stable conflict geometry
- stable severity spread

---

## What This Does Not Prove

This experiment does not prove:

- the arbitration rule is optimal
- the severity mapping is correct
- the gates represent real systems
- the synthetic generator is realistic
- OMNIA correctness
- semantic correctness
- real-world reliability

It only shows stability of measured disagreement behavior.

---

## Boundary Statement

This experiment does not evaluate:

- truth
- meaning
- intelligence
- semantics
- causality
- cognition
- real-world correctness

It evaluates:

```text
stability of cross-gate structural disagreement
```

---

## Limitations

This is not the full OMNIA engine.

The generators remain synthetic.

Only one arbitration framework was used.

Only one severity mapping was used.

No external real-world datasets were used.

No semantic evaluation exists.

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Cross-Gate Conflict Stability
```

Reason:

- 20 independent seeds
- 30000 systems tested
- stable disagreement structure
- stable contradiction structure
- stable arbitration rates
- stable spread metrics
- stable variance metrics
- reproducible outputs

Not yet Level 3 because:

- no external dataset
- no real deployment
- arbitration remains hand-defined
- synthetic generators remain simplified

---

## Relation To Previous Results

Validation path:

```text
Effective Observer Count v0
→ raw_count != effective_count

Recoverability Effective Observer v0
→ flawed recoverability proxy exposed

Recoverability Effective Observer v1
→ proxy corrected

Correlation Analysis v0
→ effective_count beats raw_count on one seed

Correlation Stability v0
→ effective_count beats raw_count across 20 seeds

Correlation Adversarial v0
→ effective_count boundary exposed

Recoverability Gate v0
→ adversarial boundary cases detected

Recoverability Gate Stability v0
→ threshold stability verified

Recoverability Gate Adversarial v0
→ gate resists adversarial probes

Recoverability Gate Randomized v0
→ coherent randomized behavior

Recoverability Gate Randomized Stability v0
→ stable randomized behavior

Recoverability Gate External Proxy v0
→ external-style shift exposes bias

Cross-Gate Disagreement Analysis v0
→ signal conflict regimes measured

Cross-Gate Disagreement Stability v0
→ signal conflict remains stable across populations
```

---

## Required Next Step

Recommended next file:

```text
examples/cross_gate_real_dataset_proxy_v0.py
```

Purpose:

```text
test disagreement behavior on externally sourced
non-synthetic structural datasets
```

Main question:

```text
does cross-gate disagreement persist outside synthetic generators?
```

---

## Final Result

```text
PASS — cross-gate disagreement remained stable across seeds.
```

Correct final conclusion:

```text
the disagreement structure is persistent,
the gates remain non-redundant,
and structural arbitration remains justified across populations.
```