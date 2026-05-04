# Collapse Confirmation Source Swap v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Collapse Confirmation Source-Swap Robustness
```

---

## Purpose

This experiment tests whether arbitration `COLLAPSE` remains stable when the confirming gate source changes.

The previous stability test showed:

```text
collapse arbitration remains present,
but confirmation-source identity is perturbation-sensitive
```

This experiment asks the next question:

```text
does collapse remain valid when confirmation moves between gates?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates whether collapse confirmation depends on one specific gate or can survive source replacement.

---

## Experiment File

```text
examples/collapse_confirmation_source_swap_v0.py
```

Result file:

```text
results/collapse_confirmation_source_swap_v0.json
```

Generated dataset:

```text
data/collapse_confirmation_source_swap_v0.csv
```

Reproduction command:

```text
python examples/collapse_confirmation_source_swap_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

record_count = 16

COLLAPSE = 9
ESCALATE = 5
PASS = 1
RETRY = 1

multi_source_collapse_count = 9

projection_confirmed_collapse_count = 6
resistance_confirmed_collapse_count = 5
recoverability_confirmed_collapse_count = 1

confirmation_swap_count = 7

projection_only_confirmation_count = 4
resistance_only_confirmation_count = 3
joint_projection_resistance_count = 2

isolated_effective_auto_collapse_count = 0
clean_control_pass_count = 1
```

The experiment passed.

Collapse remained stable while the confirming source changed.

---

## Arbitration Action Distribution

```text
COLLAPSE = 9
ESCALATE = 5
PASS = 1
RETRY = 1
```

This distribution is structurally coherent.

Most collapse-pressure records reached `COLLAPSE`.

Ambiguous records reached `ESCALATE`.

The clean control remained `PASS`.

One partial case remained `RETRY`.

---

## Source Family Distribution

```text
ambiguous = 2
control = 1
divergence_swap = 2
effective_only = 1
projection_swap = 2
recoverability_swap = 2
resistance_swap = 2
source_swap = 2
triple_confirmed = 2
```

The dataset explicitly contains source-swap cases.

It is not a general benchmark.

It is a controlled proxy for testing whether collapse confirmation depends on a fixed confirmation source.

---

## Collapse Count

```text
collapse_count = 9
```

Nine records reached final arbitration `COLLAPSE`.

This confirms that collapse did not disappear when confirmation sources were varied.

---

## Multi-Source Collapse

```text
multi_source_collapse_count = 9
```

Every arbitration `COLLAPSE` record had multi-source confirmation.

This is the central positive result.

The system did not collapse based on a lone effective-signal collapse.

---

## Confirmation Source Families

```text
collapse_gate
effective_signal_gate
projection_gate
recoverability_gate
```

Four different gate families participated in collapse confirmation.

This supports the claim that the architecture is not dependent on one isolated confirming lens.

---

## Source Swap Metrics

```text
confirmation_swap_count = 7

projection_only_confirmation_count = 4
resistance_only_confirmation_count = 3
joint_projection_resistance_count = 2
```

These values show three regimes:

```text
projection-only confirmation
resistance-only confirmation
joint projection/resistance confirmation
```

This is the core source-swap result.

Collapse appears across different confirmation paths.

---

## Projection Confirmation

```text
projection_confirmed_collapse_count = 6
```

Projection confirmed collapse in six records.

This shows that projection stability can act as an independent collapse source.

---

## Resistance Confirmation

```text
resistance_confirmed_collapse_count = 5
```

Collapse resistance confirmed collapse in five records.

This shows that resistance collapse can also independently support arbitration collapse.

---

## Recoverability Confirmation

```text
recoverability_confirmed_collapse_count = 1
```

Recoverability collapse appeared only once.

This is coherent with previous tests.

Recoverability tends to collapse less often than effective signal, projection, or resistance.

---

## Anti-Panic Check

```text
isolated_effective_auto_collapse_count = 0
```

This is one of the strongest checks.

The record:

```text
isolated_effective_collapse
```

produced:

```text
effective_signal_gate = COLLAPSE
arbitration_action = ESCALATE
```

It did not produce automatic `COLLAPSE`.

Correct interpretation:

```text
isolated effective collapse is insufficient for final collapse arbitration
```

---

## Clean Control Check

```text
clean_control_pass_count = 1
```

The clean control remained:

```text
PASS
```

with all gates returning:

```text
PASS
```

This confirms that the dataset does not force universal collapse.

---

## Escalation Recovery

```text
escalation_recovery_count = 5
```

Five ambiguous or single-source collapse cases were routed to `ESCALATE`.

This is important.

It means arbitration separates:

```text
single-source collapse pressure
```

from:

```text
multi-source confirmed collapse
```

---

## Disagreement Metrics

```text
high_disagreement_count = 13
contradiction_count = 10

mean_unique_action_count = 2.875
mean_severity_spread = 3.3125
mean_severity_variance = 1.765000000000
```

The dataset produced strong cross-gate disagreement.

Contradiction was frequent.

This confirms that collapse can be confirmed even in a high-conflict environment.

---

## Gate Action Distributions

### Effective Signal Gate

```text
PASS = 1
COLLAPSE = 14
RETRY = 1
```

The effective signal gate was collapse-heavy.

But it did not alone determine final collapse.

The anti-panic check remained valid.

---

### Projection Gate

```text
PASS = 8
COLLAPSE = 6
FLAG = 2
```

Projection confirmed collapse in multiple source-swap records.

This supports projection as a strong independent confirmation source.

---

### Collapse Gate

```text
PASS = 6
FLAG = 3
RETRY = 2
COLLAPSE = 5
```

Collapse resistance also confirmed collapse in multiple records.

This supports resistance as another independent source.

---

### Recoverability Gate

```text
PASS = 1
FLAG = 10
RETRY = 4
COLLAPSE = 1
```

Recoverability mostly stayed in `FLAG` or `RETRY`.

It only collapsed once.

This supports the earlier observation:

```text
recoverability is harder to collapse
```

---

### Divergence Gate

```text
PASS = 2
FLAG = 11
ESCALATE = 2
RETRY = 1
```

Divergence mostly flagged disagreement.

It escalated only two records.

This confirms that divergence is a conflict-sensitive signal, not simply a collapse detector.

---

## Key Record Classes

### Clean control

```text
clean_control_reference
arbitration = PASS
confirmation_sources = none
all gates = PASS
```

This verifies that clean structure remains passable.

---

### Isolated effective collapse

```text
isolated_effective_collapse
arbitration = ESCALATE
confirmation_sources = effective_signal_gate
```

This verifies anti-panic behavior.

Single-source effective collapse did not force final `COLLAPSE`.

---

### Projection-only confirmation

Examples:

```text
projection_strong_resistance_weak
projection_collapse_resistance_flag
divergence_dominant_projection_weak
resistance_relief_projection_takeover
```

These records reached `COLLAPSE` through projection confirmation without collapse-gate collapse.

This proves that projection can substitute for resistance confirmation.

---

### Resistance-only confirmation

Examples:

```text
recoverability_weak_resistance_strong
divergence_dominant_resistance_weak
projection_relief_resistance_takeover
```

These records reached `COLLAPSE` through collapse-gate confirmation without projection collapse.

This proves that resistance can substitute for projection confirmation.

---

### Joint confirmation

Examples:

```text
triple_confirmed_collapse
quad_confirmed_collapse
```

These records reached collapse through joint confirmation.

They verify the expected strong-collapse regime.

---

## Important Finding

The important finding is:

```text
collapse confirmation is source-swappable
```

Collapse does not require one fixed confirming gate.

It can be confirmed by different combinations of structural gates:

```text
effective + projection
effective + resistance
effective + projection + resistance
effective + recoverability + projection + resistance
```

This supports a stronger architecture:

```text
multi-source arbitration
```

rather than:

```text
single-gate dependency
```

---

## Main Interpretation

The previous perturbation stability test showed partial instability:

```text
projection relief removed projection confirmation
collapse relief removed resistance confirmation
```

This test shows that this is not necessarily a failure.

If one confirmation source weakens, another can take over.

Correct interpretation:

```text
confirmation-source identity may change,
while collapse arbitration remains structurally valid
```

This is stronger than requiring the same gate to confirm collapse in every condition.

---

## What This Confirms

This experiment supports:

```text
collapse confirmation can survive source replacement

projection confirmation can support collapse independently

resistance confirmation can support collapse independently

joint confirmation remains available

isolated effective collapse does not trigger automatic collapse

clean control remains passable

ambiguous single-source cases escalate

collapse arbitration is multi-source, not single-gate dependent
```

---

## What This Does Not Prove

This experiment does not prove:

```text
real-world collapse validity

semantic correctness

causal correctness

universal arbitration optimality

full OMNIA correctness

external benchmark performance

general deployment readiness
```

It only tests source-swap behavior on a controlled proxy dataset.

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
source-swap robustness of multi-gate collapse confirmation
```

---

## Limitations

```text
Only 16 records were tested.

The dataset is generated by the script.

The source-swap cases are constructed.

The arbitration rule is hand-defined.

The severity mapping is hand-defined.

No external real-world dataset was used.

No semantic ground truth exists.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Collapse Confirmation Source-Swap Robustness
```

Reason:

```text
defined source-swap dataset
defined gate family
defined confirmation metrics
defined arbitration rule
defined reproduction command
saved JSON result

COLLAPSE appeared through projection-only confirmation
COLLAPSE appeared through resistance-only confirmation
COLLAPSE appeared through joint confirmation
isolated effective collapse did not auto-collapse
clean control remained PASS
ambiguous cases escalated
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

Collapse Confirmation Stability v0
→ collapse remains present, but confirmation-source identity is perturbation-sensitive

Collapse Confirmation Source Swap v0
→ collapse remains stable when confirmation source changes
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_degradation_v0.py
```

Purpose:

```text
test whether collapse emerges over time
through gradual degradation rather than static snapshots
```

Main question:

```text
does a structure move through PASS → RETRY → ESCALATE → COLLAPSE
as degradation accumulates?
```

Required checks:

```text
temporal_order_consistency
collapse_onset_step
escalation_before_collapse
no_instant_panic_from_single_gate
control_trajectory_remains_pass
multi-gate_confirmation_before_collapse
```

---

## Final Result

```text
PASS — collapse confirmation remained stable under source swap.
```

Correct final conclusion:

```text
arbitration COLLAPSE is not dependent on one fixed confirmation gate;
it remains valid when collapse confirmation shifts between independent structural sources.
```