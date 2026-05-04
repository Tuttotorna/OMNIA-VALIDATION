# Cross-Gate Real Dataset Proxy v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Real-Style Proxy Dataset Test
```

---

## Purpose

This experiment tests cross-gate disagreement on a small real-style proxy dataset.

Previous experiments showed that cross-gate disagreement exists and remains stable across synthetic external-style populations.

This test asks whether similar disagreement appears in a more dataset-like proxy table.

Core boundary:

```text
measurement != inference != decision
```

The goal is not to force a `PASS`.

The goal is to measure whether the dataset produces enough structural conflict to validate cross-gate disagreement outside the randomized generator.

---

## Experiment File

```text
examples/cross_gate_real_dataset_proxy_v0.py
```

Result file:

```text
results/cross_gate_real_dataset_proxy_v0.json
```

Generated dataset:

```text
data/cross_gate_real_dataset_proxy_v0.csv
```

Reproduction command:

```text
python examples/cross_gate_real_dataset_proxy_v0.py
```

---

## Summary Result

```text
Status: CHECK
Version: 0.1.0

record_count = 16

high_disagreement_count = 1
medium_disagreement_count = 11
low_disagreement_count = 4

contradiction_count = 1
unanimous_count = 0

mean_unique_action_count = 2.5625
mean_severity_spread = 1.875
mean_severity_variance = 0.65
```

The dataset exposed some cross-gate disagreement, but not enough to satisfy the stronger conflict criteria.

---

## Arbitration Action Distribution

```text
ESCALATE = 1
PASS = 8
RETRY = 7
COLLAPSE = 0
FLAG = 0
```

The arbitration distribution is mild.

Most records were classified as:

```text
PASS
```

or:

```text
RETRY
```

Only one record escalated.

No record collapsed.

This means the proxy dataset is not sufficiently stress-heavy.

---

## Source Family Distribution

```text
docs = 2
logs = 2
research = 4
sensor = 2
software = 3
support = 3
```

The dataset includes multiple source families, but it is still small.

The test is useful as a proxy, not as an external benchmark.

---

## Disagreement Counts

```text
high_disagreement_count = 1
medium_disagreement_count = 11
low_disagreement_count = 4
```

Most records produced medium disagreement.

Only one produced high disagreement.

This is why the run correctly returned:

```text
CHECK
```

---

## Contradiction Count

```text
contradiction_count = 1
```

Only one record produced a direct conflict where one gate emitted `PASS` while another emitted `COLLAPSE`.

That is enough to show cross-gate disagreement exists, but not enough to show strong real-dataset conflict.

---

## Unanimous Count

```text
unanimous_count = 0
```

No record produced full agreement across all gates.

This is still useful.

It confirms that even in a mild dataset, the gates do not collapse into one identical signal.

---

## Mean Disagreement Metrics

```text
mean_unique_action_count = 2.5625
mean_severity_spread = 1.875
mean_severity_variance = 0.65
```

The signal family remains non-redundant, but the disagreement intensity is weaker than in the synthetic external-style population.

---

## Mean Spread By Family

```text
docs = 1.5
logs = 3.0
research = 1.75
sensor = 1.5
software = 1.666666666667
support = 2.0
```

The strongest spread appeared in:

```text
logs
```

This is coherent because the log records included anomaly and incident-style examples.

---

## Mean Variance By Family

```text
docs = 0.480000000000
logs = 1.160000000000
research = 0.640000000000
sensor = 0.360000000000
software = 0.533333333333
support = 0.746666666667
```

Again, logs produced the strongest disagreement variance.

---

## Gate Action Distributions

### Collapse Gate

```text
PASS = 16
```

The collapse gate passed all records.

This explains why there were no final `COLLAPSE` arbitration results.

The dataset does not contain enough collapse-pressure records.

### Divergence Gate

```text
FLAG = 12
RETRY = 4
```

The divergence gate was the most sensitive signal.

It found structural mismatch in most records.

### Effective Signal Gate

```text
PASS = 7
RETRY = 7
FLAG = 1
COLLAPSE = 1
```

The effective signal gate produced the broadest range of actions.

It is the only gate that emitted a `COLLAPSE`.

### Projection Gate

```text
PASS = 13
RETRY = 3
```

Projection stability was mostly permissive.

### Recoverability Gate

```text
PASS = 8
FLAG = 8
```

Recoverability split the dataset evenly between pass and flag.

---

## Important Finding

This run is scientifically useful because it did not simply produce another artificial `PASS`.

It found a limitation:

```text
the real-style proxy dataset is under-stressed
```

The dataset is too mild to reproduce the strong conflict regimes seen in the external randomized generator.

Correct interpretation:

```text
CHECK does not invalidate the gate family.
CHECK diagnoses the dataset.
```

---

## Main Interpretation

The result shows:

```text
cross-gate disagreement exists
```

but:

```text
the dataset is too small and too mild
to validate strong disagreement persistence
```

The correct next move is not threshold tuning.

The correct next move is a stronger real-style proxy dataset.

---

## What This Confirms

This experiment supports:

```text
the gate family remains non-redundant

unanimous agreement remains absent

divergence gate remains sensitive

effective signal gate detects the strongest weakness

log-like records produce the strongest spread

small real-style proxy datasets can diagnose whether enough stress exists
```

---

## What This Does Not Prove

This experiment does not prove:

```text
real-world generalization

external benchmark validity

arbitration correctness

threshold optimality

full OMNIA correctness

semantic correctness

recoverability truth
```

It only tests a small real-style proxy dataset.

---

## Boundary Statement

This experiment does not evaluate:

```text
truth
meaning
semantic correctness
intelligence
causality
observer optimality
real-world reliability
full OMNIA correctness
```

It evaluates cross-gate disagreement on a small structured proxy dataset.

---

## Limitations

```text
Only 16 records were tested.

The dataset is generated by the script.

The dataset is real-style, not truly external.

The records are proxy examples.

The collapse gate passed all records.

No true real-world ground truth exists.

No semantic truth is evaluated.

The arbitration rule is hand-defined.
```

---

## Result Classification

Recommended classification:

```text
CHECK
```

Evidence level:

```text
Level 2 — Real-Style Proxy Dataset Test
```

Reason:

```text
defined dataset format
defined feature derivation
defined gate actions
defined arbitration rule
defined reproduction command
saved JSON result
measurable disagreement found
but strong conflict criteria not satisfied
```

This is not a failed validation.

It is a boundary diagnosis.

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

Cross-Gate Real Dataset Proxy v0
→ small real-style proxy dataset is under-stressed
```

---

## Required Next Step

Recommended next file:

```text
examples/cross_gate_real_dataset_proxy_stressed_v0.py
```

Purpose:

```text
construct a stronger real-style proxy dataset
with explicit collapse-pressure,
projection-loss,
redundancy,
instability,
and contradiction records
```

Main question:

```text
does cross-gate disagreement reappear strongly
when the real-style proxy dataset contains enough structural stress?
```

---

## Final Result

```text
CHECK — real-dataset proxy did not expose enough cross-gate conflict.
```

Correct final conclusion:

```text
the gate family remains non-redundant,
but the v0 real-style proxy dataset is too mild
to validate strong cross-gate disagreement.
```