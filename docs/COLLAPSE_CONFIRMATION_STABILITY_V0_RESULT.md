# Collapse Confirmation Stability v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Perturbation Stability of Multi-Gate Collapse Confirmation
```

---

## Purpose

This experiment tests whether multi-gate collapse confirmation remains stable under controlled perturbations.

The previous experiment showed that arbitration `COLLAPSE` appears when collapse pressure is independently confirmed by multiple gate families.

This experiment asks a stronger question:

```text
does confirmed collapse survive perturbation?
```

Core boundary:

```text
measurement != arbitration != decision
```

This test does not evaluate semantic truth.

It evaluates stability of collapse confirmation under structural perturbation.

---

## Experiment File

```text
examples/collapse_confirmation_stability_v0.py
```

Result file:

```text
results/collapse_confirmation_stability_v0.json
```

Generated dataset:

```text
data/collapse_confirmation_stability_v0.csv
```

Reproduction command:

```text
python examples/collapse_confirmation_stability_v0.py
```

---

## Summary Result

```text
Status: CHECK
Version: 0.1.0

config_count = 9
record_count_per_config = 20
total_evaluated_records = 180

pass_config_count = 7
check_config_count = 2
```

The result is `CHECK`, not because collapse disappeared, but because two perturbations removed one specific confirmation source.

Core finding:

```text
collapse arbitration remains present
but confirmation-source identity is perturbation-sensitive
```

---

## Global Collapse Stability

```text
mean_collapse_count = 5.777777777778
min_collapse_count = 3
max_collapse_count = 9
```

Arbitration `COLLAPSE` remained present in every perturbation.

Even the weakest configuration still produced:

```text
collapse_count = 3
```

This means collapse detection itself did not disappear.

---

## Multi-Gate Collapse Stability

```text
mean_multi_gate_collapse_count = 5.777777777778
min_multi_gate_collapse_count = 3
max_multi_gate_collapse_count = 9
```

Multi-gate collapse also remained present in every perturbation.

This is an important positive result.

It shows that collapse confirmation is not a single-threshold accident.

---

## Projection Confirmation Stability

```text
mean_projection_confirmed_count = 4.111111111111
min_projection_confirmed_count = 0
```

Projection-confirmed collapse failed under:

```text
projection_relief
```

This is expected.

That perturbation explicitly reduces projection loss.

Therefore the projection gate stopped confirming collapse.

This is why the run did not receive a global `PASS`.

---

## Resistance Confirmation Stability

```text
mean_resistance_confirmed_count = 3.111111111111
min_resistance_confirmed_count = 0
```

Collapse-resistance-confirmed collapse failed under:

```text
collapse_relief
```

This is also expected.

That perturbation explicitly reduces failure and instability pressure.

Therefore the collapse-resistance gate stopped confirming collapse.

This is the second reason for global `CHECK`.

---

## Anti-Panic Check

```text
max_isolated_effective_auto_collapse_count = 0
```

This is one of the strongest results.

It means isolated effective collapse never became automatic arbitration collapse under any perturbation.

Correct interpretation:

```text
effective degradation alone still does not force COLLAPSE
```

This protects the architecture from threshold panic.

---

## Control Stability

```text
min_clean_control_pass_count = 1
```

The clean control remained `PASS` in every perturbation.

This confirms that the perturbations did not make the system collapse everything.

Correct interpretation:

```text
the arbitration layer remains selective
```

---

## Escalation Stability

```text
mean_escalate_count = 9.777777777778
min_escalate_count = 8
```

Escalation remained common in every perturbation.

This means ambiguous or partially confirmed collapse pressure continued to produce:

```text
ESCALATE
```

rather than automatic `COLLAPSE`.

This is structurally desirable.

---

## Disagreement Stability

```text
mean_high_disagreement_count = 15
min_high_disagreement_count = 13
```

High disagreement remained present in every perturbation.

The signal family remains non-redundant under perturbation.

---

## Contradiction Stability

```text
mean_contradiction_count = 8.222222222222
min_contradiction_count = 6
```

Contradictions remained present in every perturbation.

This means that even perturbed collapse-pressure records continue to produce:

```text
PASS / COLLAPSE conflict across gates
```

---

## Severity Spread Stability

```text
mean_severity_spread = 3.044444444444
min_mean_severity_spread = 2.8
```

Severity spread remained high across all perturbations.

This confirms that the dataset stayed structurally conflicted.

---

## Config Summary

### Baseline

```text
status = PASS
collapse = 5
multi_gate_collapse = 5
projection = 4
resistance = 3
isolated_auto = 0
control_pass = 1
high_disagreement = 15
contradiction = 9
mean_spread = 3.05
```

Baseline confirms the previous collapse-proxy result.

---

### Mild Relief

```text
status = PASS
collapse = 3
multi_gate_collapse = 3
projection = 3
resistance = 3
isolated_auto = 0
control_pass = 1
high_disagreement = 14
contradiction = 8
mean_spread = 2.95
```

Mild relief reduced collapse intensity, but did not destroy confirmation.

---

### Mild Stress

```text
status = PASS
collapse = 8
multi_gate_collapse = 8
projection = 6
resistance = 3
isolated_auto = 0
control_pass = 1
high_disagreement = 15
contradiction = 9
mean_spread = 3.15
```

Mild stress increased collapse count.

This is coherent.

---

### Projection Relief

```text
status = CHECK
collapse = 3
multi_gate_collapse = 3
projection = 0
resistance = 3
isolated_auto = 0
control_pass = 1
high_disagreement = 15
contradiction = 6
mean_spread = 2.90
```

Projection relief removed projection-confirmed collapse.

Important:

```text
collapse still remained present
```

The `CHECK` is caused by loss of projection confirmation, not loss of collapse.

---

### Projection Stress

```text
status = PASS
collapse = 9
multi_gate_collapse = 9
projection = 8
resistance = 3
isolated_auto = 0
control_pass = 1
high_disagreement = 15
contradiction = 8
mean_spread = 3.05
```

Projection stress strongly increased projection-confirmed collapse.

This is coherent.

---

### Collapse Relief

```text
status = CHECK
collapse = 4
multi_gate_collapse = 4
projection = 4
resistance = 0
isolated_auto = 0
control_pass = 1
high_disagreement = 16
contradiction = 9
mean_spread = 3.10
```

Collapse relief removed resistance-confirmed collapse.

Important:

```text
collapse still remained present
```

The `CHECK` is caused by loss of collapse-resistance confirmation.

---

### Collapse Stress

```text
status = PASS
collapse = 9
multi_gate_collapse = 9
projection = 4
resistance = 7
isolated_auto = 0
control_pass = 1
high_disagreement = 15
contradiction = 9
mean_spread = 3.10
```

Collapse stress strongly increased resistance-confirmed collapse.

This is coherent.

---

### Redundancy Relief

```text
status = PASS
collapse = 5
multi_gate_collapse = 5
projection = 4
resistance = 3
isolated_auto = 0
control_pass = 1
high_disagreement = 13
contradiction = 7
mean_spread = 2.80
```

Redundancy relief reduced some disagreement intensity but preserved collapse confirmation.

---

### Redundancy Stress

```text
status = PASS
collapse = 6
multi_gate_collapse = 6
projection = 4
resistance = 3
isolated_auto = 0
control_pass = 1
high_disagreement = 17
contradiction = 9
mean_spread = 3.30
```

Redundancy stress increased disagreement intensity.

This is coherent.

---

## Important Finding

The experiment did not prove full confirmation-source stability.

It did prove something more precise:

```text
collapse arbitration is stable,
but confirmation source identity is perturbation-sensitive
```

Projection relief removes projection confirmation.

Collapse relief removes resistance confirmation.

This is expected behavior, not a logical failure.

The global `CHECK` is therefore informative.

---

## Main Interpretation

The test shows three things at once:

```text
1. collapse does not disappear under perturbation

2. isolated effective collapse still does not become automatic collapse

3. the specific gate family confirming collapse can change under perturbation
```

That is a strong structural result.

It means the arbitration system is not simply panic-triggered.

It also means collapse confirmation is not fully invariant to targeted relief perturbations.

---

## What This Confirms

This experiment supports:

```text
arbitration COLLAPSE remains nonzero under all perturbations

multi-gate collapse remains nonzero under all perturbations

clean control remains PASS under all perturbations

isolated effective collapse never becomes automatic COLLAPSE

high disagreement remains present

contradiction remains present

ESCALATE remains common for ambiguous cases

projection stress increases projection confirmation

collapse stress increases resistance confirmation
```

---

## What This Does Not Confirm

This experiment does not confirm:

```text
full confirmation-source invariance

projection confirmation under projection relief

resistance confirmation under collapse relief

universal perturbation stability

real-world collapse validity

semantic correctness

full OMNIA correctness
```

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
perturbation stability of multi-gate collapse confirmation
```

---

## Limitations

```text
Only 9 perturbation configurations were tested.

Only 20 records per configuration were used.

The dataset is generated by the script.

The perturbations are hand-defined.

The arbitration rule is hand-defined.

The severity mapping is hand-defined.

No real external dataset was used.

No semantic ground truth exists.
```

---

## Result Classification

Recommended classification:

```text
CHECK
```

Evidence level:

```text
Level 2 — Perturbation Stability of Multi-Gate Collapse Confirmation
```

Reason:

```text
defined perturbation configs
defined collapse proxy dataset
defined confirmation metrics
defined arbitration logic
defined reproduction command
saved JSON result

7 / 9 perturbation configs passed
collapse remained present in all configs
multi-gate collapse remained present in all configs
isolated effective collapse never became automatic collapse
clean control stayed PASS in all configs

but projection confirmation dropped to zero under projection relief
and resistance confirmation dropped to zero under collapse relief
```

This is not a failed experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/collapse_confirmation_source_swap_v0.py
```

Purpose:

```text
test whether collapse confirmation can remain stable
when the confirming gate family changes
```

Main question:

```text
can arbitration COLLAPSE remain stable
even when projection confirmation is replaced by resistance confirmation,
or resistance confirmation is replaced by projection confirmation?
```

Required checks:

```text
collapse_count remains nonzero
multi_gate_collapse_count remains nonzero
at least one independent confirmation source remains present
isolated effective collapse remains non-automatic
clean control remains PASS
ESCALATE remains common for ambiguous cases
```

---

## Final Result

```text
CHECK — multi-gate collapse confirmation showed partial instability under targeted perturbation.
```

Correct final conclusion:

```text
collapse arbitration remains stable,
but the identity of the confirming gate family changes under perturbation.
```