# Cross-Gate Real Dataset Proxy Stressed v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Stressed Real-Style Cross-Gate Proxy Evaluation
```

---

## Purpose

This experiment evaluates cross-gate disagreement using a stressed real-style proxy dataset.

The previous proxy dataset produced measurable disagreement, but the conflict intensity remained relatively weak.

This stressed version introduces records designed to increase:

```text
projection instability
collapse pressure
effective signal degradation
observer shift
redundancy masking
surface/deep disagreement
distributed inconsistency
structural ambiguity
```

The experiment asks:

```text
can stressed real-style records produce measurable multi-gate conflict?
```

Core boundary:

```text
measurement != inference != decision
```

This experiment does not evaluate semantic truth.

It evaluates structural disagreement between gate families.

---

## Experiment File

```text
examples/cross_gate_real_dataset_proxy_stressed_v0.py
```

Result file:

```text
results/cross_gate_real_dataset_proxy_stressed_v0.json
```

Generated dataset:

```text
data/cross_gate_real_dataset_proxy_stressed_v0.csv
```

Reproduction command:

```text
python examples/cross_gate_real_dataset_proxy_stressed_v0.py
```

---

## Summary Result

```text
Status: CHECK
Version: 0.1.0

record_count = 20

high_disagreement_count = 6
medium_disagreement_count = 9
low_disagreement_count = 5

contradiction_count = 4
unanimous_count = 0

mean_unique_action_count = 2.65
mean_severity_spread = 2.25
mean_severity_variance = 0.980000000000
```

The stressed dataset successfully increased cross-gate disagreement compared to the previous proxy dataset.

However:

```text
final arbitration COLLAPSE did not occur
```

The result therefore remains:

```text
CHECK
```

not:

```text
PASS
```

---

## Arbitration Action Distribution

```text
ESCALATE = 6
PASS = 6
RETRY = 8
COLLAPSE = 0
FLAG = 0
```

Important observation:

```text
ESCALATE increased substantially
```

compared to the earlier real-style proxy dataset.

This confirms that the stressed records successfully generated stronger structural conflict.

However:

```text
no arbitration COLLAPSE occurred
```

This means the gate family detected instability and disagreement, but not sufficiently confirmed multi-gate collapse.

---

## Source Family Distribution

```text
docs = 2
logs = 3
research = 4
sensor = 4
software = 4
support = 3
```

The stressed dataset spans multiple proxy domains.

The strongest disagreement emerged in:

```text
logs
sensor
support
```

This is structurally coherent because those domains naturally contain:

```text
redundancy
projection drift
distributed inconsistency
partial observability
surface/deep mismatch
```

---

## Disagreement Counts

```text
high_disagreement_count = 6
medium_disagreement_count = 9
low_disagreement_count = 5
```

Compared to the earlier proxy dataset:

```text
previous proxy:
high_disagreement_count = 1

stressed proxy:
high_disagreement_count = 6
```

The stressed dataset clearly increased measurable disagreement.

This confirms the stress construction worked.

---

## Contradiction Count

```text
contradiction_count = 4
```

Contradictions occur when at least one gate emits:

```text
PASS
```

while another emits:

```text
COLLAPSE
```

This is the strongest form of gate disagreement.

The presence of contradiction confirms:

```text
the gate family is non-redundant
```

and:

```text
different structural lenses react differently to the same record
```

---

## Unanimous Count

```text
unanimous_count = 0
```

No record produced complete agreement across all gates.

This is consistent with previous cross-gate experiments.

The gate family continues to behave as:

```text
multiple partially independent structural observers
```

rather than:

```text
one duplicated signal
```

---

## Mean Disagreement Metrics

```text
mean_unique_action_count = 2.65
mean_severity_spread = 2.25
mean_severity_variance = 0.980000000000
```

Interpretation:

```text
the average record triggered multiple distinct structural reactions
```

The disagreement intensity is significantly higher than the earlier proxy dataset, but still lower than the large synthetic external-style populations.

---

## Mean Spread By Family

```text
docs = 1.5
logs = 3.666666666667
research = 1.75
sensor = 2.75
software = 1.5
support = 2.333333333333
```

Highest disagreement:

```text
logs
sensor
support
```

Lowest disagreement:

```text
docs
software
```

This is coherent.

Static or cleaner structures naturally generate less conflict.

Distributed, noisy, or unstable structures generate more disagreement.

---

## Mean Variance By Family

```text
docs = 0.480000000000
logs = 1.893333333333
research = 0.680000000000
sensor = 1.240000000000
software = 0.560000000000
support = 1.013333333333
```

Logs produced the strongest variance.

This means:

```text
different gates strongly disagree on unstable repetitive event structures
```

This pattern matches previous disagreement experiments.

---

## Gate Action Distributions

### Collapse Gate

```text
PASS = 18
RETRY = 2
COLLAPSE = 0
```

The collapse gate remained permissive.

This is the primary reason the arbitration layer never emitted:

```text
COLLAPSE
```

Even under stressed conditions, collapse resistance was not jointly weak enough.

---

### Divergence Gate

```text
FLAG = 15
RETRY = 4
ESCALATE = 1
```

The divergence gate remained highly sensitive.

It detected disagreement in almost every record.

This confirms:

```text
structural mismatch persists even when collapse is not confirmed
```

---

### Effective Signal Gate

```text
PASS = 4
COLLAPSE = 5
RETRY = 7
FLAG = 4
```

The effective signal gate produced the strongest collapse behavior.

This is important.

The main instability source in this dataset is:

```text
effective structural degradation
```

not:

```text
joint multi-gate collapse
```

---

### Projection Gate

```text
PASS = 14
RETRY = 5
FLAG = 1
COLLAPSE = 0
```

Projection instability increased compared to the earlier proxy dataset.

However, it still remained relatively permissive.

Projection collapse was not confirmed.

---

### Recoverability Gate

```text
PASS = 9
FLAG = 11
COLLAPSE = 0
RETRY = 0
```

Recoverability split almost evenly between:

```text
PASS
```

and:

```text
FLAG
```

It did not collapse.

This means the records often retained partial recoverable structure despite instability.

---

## Important Finding

The stressed proxy dataset successfully increased structural disagreement.

However, collapse pressure remained asymmetric.

Key asymmetry:

```text
effective_signal_gate COLLAPSE = 5
collapse_gate COLLAPSE = 0
projection_gate COLLAPSE = 0
recoverability_gate COLLAPSE = 0
```

Interpretation:

```text
effective degradation alone is insufficient
for confirmed arbitration collapse
```

The arbitration layer requires stronger independent confirmation.

That confirmation did not occur.

---

## Main Interpretation

This experiment produced:

```text
more disagreement
more escalation
more contradiction
higher spread
higher variance
```

than the earlier real-style proxy dataset.

But:

```text
the collapse signal remained isolated
primarily inside the effective signal gate
```

Therefore:

```text
the system detected instability,
but not sufficiently confirmed structural collapse
```

This is exactly why the final result is:

```text
CHECK
```

rather than:

```text
PASS
```

---

## What This Confirms

This experiment supports:

```text
stressed proxy datasets increase cross-gate disagreement

logs and sensors produce stronger instability

effective degradation can collapse independently

cross-gate contradiction exists

ESCALATE increases under stress

gate families remain non-redundant

structural disagreement remains measurable
```

---

## What This Does Not Prove

This experiment does not prove:

```text
real-world validity

semantic correctness

truth detection

optimal arbitration

general collapse theory

real observer behavior

full OMNIA correctness
```

It only evaluates stressed proxy structural disagreement.

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

It evaluates disagreement between structural gate families.

---

## Limitations

```text
Only 20 records were tested.

The dataset is synthetic real-style proxy data.

The arbitration rule is hand-defined.

The severity mapping is hand-defined.

No external benchmark is used.

No semantic evaluation exists.

No real-world ground truth exists.

The dataset is intentionally stressed.

The collapse gate remained permissive.
```

---

## Result Classification

Recommended classification:

```text
CHECK
```

Evidence level:

```text
Level 2 — Stressed Real-Style Cross-Gate Proxy Evaluation
```

Reason:

```text
defined stressed dataset
defined structural metrics
defined gate family
defined arbitration logic
defined disagreement metrics
defined reproduction command
saved JSON result
increased disagreement verified
increased escalation verified
contradictions verified
but arbitration collapse absent
```

This is a useful boundary result.

Not a failed experiment.

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
→ effective_count beats raw_count

Correlation Stability v0
→ correlation stability verified

Correlation Adversarial v0
→ adversarial boundary exposed

Recoverability Gate v0
→ multi-signal gate detects instability

Recoverability Gate Stability v0
→ threshold stability verified

Recoverability Gate Adversarial v0
→ adversarial resistance improved

Recoverability Gate Randomized v0
→ coherent randomized behavior

Recoverability Gate Randomized Stability v0
→ stable randomized behavior

Recoverability Gate External Proxy v0
→ external-style shift exposes mismatch

Cross-Gate Disagreement Analysis v0
→ signal conflict regimes measured

Cross-Gate Disagreement Stability v0
→ conflict remains stable across populations

Cross-Gate Real Dataset Proxy v0
→ mild proxy dataset under-stressed

Cross-Gate Real Dataset Proxy Stressed v0
→ stronger disagreement achieved without confirmed collapse
```

---

## Required Next Step

Recommended next experiment:

```text
examples/cross_gate_real_dataset_proxy_collapse_v0.py
```

Purpose:

```text
construct records where collapse pressure
is confirmed simultaneously by multiple gates
```

Required structural conditions:

```text
low collapse resistance
low projection stability
low normalized effective signal
high divergence
low recoverability
high redundancy masking
family imbalance
distributed instability
```

Main question:

```text
does arbitration COLLAPSE appear
when collapse is independently confirmed
across multiple gate families?
```

---

## Final Result

```text
CHECK — stressed real-dataset proxy did not expose enough conflict.
```

Correct final conclusion:

```text
the stressed proxy successfully increased disagreement,
but multi-gate confirmed collapse was still not reached.
```