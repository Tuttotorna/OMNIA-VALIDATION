# Cross-Gate Real Dataset Proxy Collapse v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Multi-Gate Collapse Confirmation Proxy
```

---

## Purpose

This experiment tests whether arbitration `COLLAPSE` appears when collapse pressure is independently confirmed by multiple structural gates.

Previous real-style proxy tests produced:

```text
mild proxy      → CHECK
stressed proxy  → CHECK
collapse proxy  → PASS
```

The key question here is:

```text
does arbitration COLLAPSE appear only when collapse pressure is confirmed across multiple gate families?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates structural gate agreement under collapse pressure.

---

## Experiment File

```text
examples/cross_gate_real_dataset_proxy_collapse_v0.py
```

Result file:

```text
results/cross_gate_real_dataset_proxy_collapse_v0.json
```

Generated dataset:

```text
data/cross_gate_real_dataset_proxy_collapse_v0.csv
```

Reproduction command:

```text
python examples/cross_gate_real_dataset_proxy_collapse_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

record_count = 20

arbitration COLLAPSE = 5
arbitration ESCALATE = 10
arbitration FLAG = 2
arbitration PASS = 2
arbitration RETRY = 1

high_disagreement_count = 15
medium_disagreement_count = 3
low_disagreement_count = 2

contradiction_count = 9
unanimous_count = 1

multi_gate_collapse_count = 5
collapse_with_projection_count = 4
collapse_with_resistance_count = 3

mean_unique_action_count = 2.7
mean_severity_spread = 3.05
mean_severity_variance = 1.608
```

The experiment passed because final arbitration `COLLAPSE` appeared under multi-gate confirmed collapse pressure.

---

## Arbitration Action Distribution

```text
COLLAPSE = 5
ESCALATE = 10
FLAG = 2
PASS = 2
RETRY = 1
```

This distribution is structurally coherent.

Most records did not collapse.

Many were escalated.

Only records with enough independent collapse pressure reached arbitration `COLLAPSE`.

This supports the intended distinction:

```text
isolated collapse signal  → ESCALATE or FLAG
multi-gate collapse signal → COLLAPSE
```

---

## Source Family Distribution

```text
borderline = 2
collapse = 5
control = 1
effective = 1
logs = 1
mixed = 3
observer = 1
projection = 2
recoverability = 1
sensor = 1
support = 2
```

The dataset contains targeted collapse-pressure families.

This is not a general external benchmark.

It is a controlled real-style proxy designed to test collapse arbitration behavior.

---

## Disagreement Counts

```text
high_disagreement_count = 15
medium_disagreement_count = 3
low_disagreement_count = 2
```

High disagreement dominated the dataset.

This means the collapse cases were not simple uniform failures.

Most records contained strong cross-gate conflict.

---

## Contradiction Count

```text
contradiction_count = 9
```

Nine records produced direct contradiction:

```text
at least one gate = PASS
at least one gate = COLLAPSE
```

This confirms that collapse arbitration occurred in a context of structural conflict, not simple unanimity.

---

## Unanimous Count

```text
unanimous_count = 1
```

The only fully unanimous record was:

```text
clean_control_reference
```

with all gates returning:

```text
PASS
```

This is useful.

It verifies that the gate system can still recognize clean structure when a control record is present.

---

## Multi-Gate Collapse Confirmation

```text
multi_gate_collapse_count = 5
collapse_with_projection_count = 4
collapse_with_resistance_count = 3
```

These are the core validation metrics.

They show that collapse was not merely produced by the effective signal gate alone.

Collapse pressure was also confirmed by:

```text
projection_gate
collapse_gate
```

in multiple records.

---

## Gate Action Distributions

### Effective Signal Gate

```text
PASS = 2
COLLAPSE = 17
RETRY = 1
```

The effective signal gate was strongly collapse-heavy.

This is expected because the dataset was designed to include effective degradation.

But effective degradation alone did not automatically force final `COLLAPSE`.

Several effective-collapse records became:

```text
ESCALATE
FLAG
RETRY
```

instead.

---

### Recoverability Gate

```text
PASS = 4
FLAG = 9
RETRY = 6
COLLAPSE = 1
```

Recoverability was more conservative than the effective signal gate.

Only one record reached recoverability `COLLAPSE`.

This supports the earlier expectation that recoverability does not always collapse immediately under effective signal degradation.

---

### Divergence Gate

```text
PASS = 2
FLAG = 13
RETRY = 3
ESCALATE = 2
```

Divergence mostly detected mismatch through `FLAG`.

It escalated only two records.

This shows that high disagreement is not identical to divergence escalation.

---

### Collapse Gate

```text
PASS = 7
FLAG = 4
RETRY = 6
COLLAPSE = 3
```

The collapse gate contributed independent collapse confirmation in three records.

This is one of the main differences from the previous stressed proxy test.

---

### Projection Gate

```text
PASS = 9
COLLAPSE = 4
FLAG = 4
RETRY = 3
```

Projection collapse appeared in four records.

This is critical.

The previous stressed proxy test failed to produce final arbitration `COLLAPSE` because projection and collapse gates remained too permissive.

Here, projection collapse appeared and helped produce confirmed multi-gate collapse.

---

## Key Record Classes

### Clean control

```text
clean_control_reference
arbitration = PASS
all gates = PASS
```

This verifies the control case.

The system does not collapse everything by construction.

---

### Isolated effective collapse

```text
effective_only_collapse
arbitration = ESCALATE
effective_signal_gate = COLLAPSE
collapse_gate = PASS
projection_gate = PASS
```

This is a crucial negative control.

A single effective collapse did not force final `COLLAPSE`.

Correct interpretation:

```text
effective collapse alone is insufficient
```

---

### Projection-confirmed collapse

```text
projection_confirmed_collapse
arbitration = COLLAPSE
effective_signal_gate = COLLAPSE
projection_gate = COLLAPSE
```

This shows collapse when projection also confirms failure.

---

### Hard collapse

```text
hard_collapse_low_everything
arbitration = COLLAPSE
effective_signal_gate = COLLAPSE
recoverability_gate = COLLAPSE
collapse_gate = COLLAPSE
projection_gate = COLLAPSE
```

This is the trivial hard-collapse reference.

It confirms that the system can collapse when almost everything fails.

---

### Non-trivial multi-gate collapse

```text
multi_gate_confirmed_collapse
arbitration = COLLAPSE
effective_signal_gate = COLLAPSE
recoverability_gate = RETRY
divergence_gate = RETRY
collapse_gate = COLLAPSE
projection_gate = COLLAPSE
```

This is the more important case.

It is not full unanimous collapse.

Recoverability and divergence do not collapse.

Yet arbitration still emits `COLLAPSE` because collapse is independently confirmed by multiple structural gates.

This is the strongest result of the experiment.

---

## Important Finding

The central finding is:

```text
COLLAPSE appears only when collapse pressure is independently confirmed.
```

The earlier stressed proxy test produced:

```text
effective_signal_gate COLLAPSE = 5
arbitration COLLAPSE = 0
```

This collapse proxy produced:

```text
effective_signal_gate COLLAPSE = 17
collapse_gate COLLAPSE = 3
projection_gate COLLAPSE = 4
arbitration COLLAPSE = 5
```

The difference is not just stronger effective degradation.

The difference is independent confirmation.

---

## Interpretation

This experiment closes a key architectural loop.

It shows three regimes:

```text
mild proxy:
  disagreement exists, but weak

stressed proxy:
  effective degradation appears, but collapse is not confirmed

collapse proxy:
  multi-gate confirmation appears, and arbitration COLLAPSE appears
```

This supports the architecture’s separation between:

```text
weak information
```

and:

```text
confirmed structural collapse
```

It also supports the separation between:

```text
measurement
arbitration
decision
```

---

## What This Confirms

This experiment supports:

```text
isolated effective collapse does not force arbitration COLLAPSE

multi-gate confirmed collapse produces arbitration COLLAPSE

projection collapse is a strong confirmation signal

collapse resistance contributes independent confirmation

recoverability can remain non-collapsed while arbitration collapses

high disagreement can coexist with final collapse

structural arbitration is not simple single-threshold gating
```

---

## What This Does Not Prove

This experiment does not prove:

```text
real-world collapse detection

semantic truth

causal truth

observer optimality

threshold optimality

universal arbitration correctness

full OMNIA correctness
```

It only tests a controlled real-style proxy dataset.

---

## Boundary Statement

This experiment does not evaluate:

```text
truth
meaning
semantic correctness
intelligence
causality
real-world reliability
full OMNIA correctness
```

It evaluates:

```text
multi-gate structural collapse confirmation
```

---

## Limitations

```text
Only 20 records were tested.

The dataset is generated by the script.

The dataset is real-style proxy data, not a true external benchmark.

The arbitration rule is hand-defined.

The severity mapping is hand-defined.

The collapse cases are intentionally constructed.

No semantic ground truth exists.

No external real-world dataset is used.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Multi-Gate Collapse Confirmation Proxy
```

Reason:

```text
defined collapse-pressure dataset
defined gate family
defined arbitration logic
defined confirmation metrics
defined reproduction command
saved JSON result
arbitration COLLAPSE appeared
multi-gate collapse appeared
projection-confirmed collapse appeared
collapse-resistance-confirmed collapse appeared
isolated effective collapse did not force collapse
```

Not yet Level 3 because the dataset is constructed and not externally validated.

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

Cross-Gate Real Dataset Proxy Collapse v0
→ arbitration COLLAPSE appears under multi-gate confirmed pressure
```

---

## Required Next Step

Recommended next experiment:

```text
examples/collapse_confirmation_stability_v0.py
```

Purpose:

```text
test whether collapse confirmation remains stable
under perturbations of the collapse proxy dataset
```

Main question:

```text
does multi-gate collapse confirmation persist
when collapse-pressure records are slightly perturbed?
```

Required checks:

```text
arbitration COLLAPSE count remains nonzero
multi_gate_collapse_count remains nonzero
projection-confirmed collapse remains present
collapse-resistance-confirmed collapse remains present
isolated effective collapse does not become automatic COLLAPSE
```

---

## Final Result

```text
PASS — collapse appeared under multi-gate confirmed pressure.
```

Correct final conclusion:

```text
arbitration COLLAPSE is not triggered by isolated effective degradation;
it appears when collapse pressure is independently confirmed across multiple gates.
```