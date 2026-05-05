# Temporal Collapse Regime Reset v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Reset-Aware Dynamic Horizon
```

---

## Purpose

This experiment tests whether reset-aware temporal horizon logic can restore predictability under non-stationary collapse regimes.

The previous experiment showed that the corrected static rule:

```text
critical_horizon =
first_raw_collapse +
confirmation_window +
persistence_window - 2
```

fails when an early collapse is followed by recovery and later relapse.

This experiment replaces the static anchor:

```text
first_raw_collapse
```

with a dynamic anchor:

```text
valid_regime_start
```

Core question:

```text
can the horizon rule be restored
by computing it from the first valid collapse regime
instead of the first raw collapse frame?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates reset-aware dynamic temporal collapse observability.

---

## Experiment File

```text
examples/temporal_collapse_regime_reset_v0.py
```

Result file:

```text
results/temporal_collapse_regime_reset_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_regime_reset_v0.py
```

---

## Summary Result

```text
Status: CHECK
Version: 0.1.0

trajectory_count = 8
trajectory_length = 16

confirmation_window = 2
persistence_window = 2
reset_window = 2

pass_trajectory_count = 7
check_trajectory_count = 1

observable_persistence_count = 5

mean_dynamic_horizon_error = 0
max_abs_dynamic_horizon_error = 0

mean_persistence_reset_count = 0.75
max_persistence_reset_count = 4

mean_horizon_fragmentation = 1
max_horizon_fragmentation = 2
```

The result is CHECK.

The important point is that the horizon prediction error is zero.

The CHECK comes from fragmented persistence classification, not from horizon prediction failure.

---

## Dynamic Rule

The dynamic rule is:

```text
dynamic_critical_horizon =
valid_regime_start +
confirmation_window +
persistence_window - 2
```

The reset rule is:

```text
a regime is reset when raw_action is not COLLAPSE
for reset_window consecutive frames before persistence
```

With this experiment:

```text
confirmation_window = 2
persistence_window = 2
reset_window = 2
```

---

## Main Finding

The central result is:

```text
mean_dynamic_horizon_error = 0
max_abs_dynamic_horizon_error = 0
```

This means the reset-aware dynamic rule restored exact horizon predictability for all observable persistent regimes.

The previous `recovery_then_relapse` failure was resolved.

---

## Why The Result Is Still CHECK

The global result remains CHECK because one trajectory was classified as unresolved:

```text
fragmented_persistence
```

That trajectory produced repeated local collapse confirmations, but never produced global persistent collapse.

This is not a horizon error.

It is a classification boundary.

The system now needs to distinguish:

```text
persistent global collapse
```

from:

```text
fragmented local collapse
```

---

## Tested Dynamic Families

The experiment tested eight dynamic families:

```text
clean_monotonic
drifting_onset
instant_spike_recovery
oscillating_collapse
recovery_then_relapse
fragmented_persistence
dual_regime_collapse
delayed_secondary_collapse
```

These include monotonic collapse, delayed onset, spikes, oscillation, recovery, relapse, fragmentation, and dual-regime collapse.

---

## Trajectory Results

### clean_monotonic

```text
status = PASS

raw_first = 4
temporal_first = 5

observed = 6
matched = 6
error = 0

regimes = [4]
horizons = [6]

fragments = 1
resets = 0
```

Raw sequence:

```text
PASS -> PASS -> RETRY -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> PASS -> RETRY -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
clean monotonic collapse remains exactly predictable
```

---

### drifting_onset

```text
status = PASS

raw_first = 6
temporal_first = 7

observed = 8
matched = 8
error = 0

regimes = [6]
horizons = [8]

fragments = 1
resets = 0
```

Raw sequence:

```text
PASS -> PASS -> PASS -> RETRY -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> PASS -> PASS -> RETRY -> ESCALATE -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
delayed collapse onset remains exactly predictable
```

---

### instant_spike_recovery

```text
status = PASS

raw_first = 1
temporal_first = None

observed = None
matched = None
error = None

regimes = []
horizons = []

fragments = 0
resets = 0
```

Raw sequence:

```text
PASS -> COLLAPSE -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS
```

Temporal sequence:

```text
PASS -> ESCALATE -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS
```

Interpretation:

```text
single-frame collapse spike remains filtered
```

The spike does not create a valid regime.

---

### oscillating_collapse

```text
status = PASS

raw_first = 2
temporal_first = None

observed = None
matched = None
error = None

regimes = []
horizons = []

fragments = 0
resets = 0
```

Raw sequence:

```text
PASS -> ESCALATE -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS
```

Temporal sequence:

```text
PASS -> ESCALATE -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS
```

Interpretation:

```text
oscillating collapse does not become persistent collapse
```

Repeated isolated collapse frames are not enough.

---

### recovery_then_relapse

```text
status = PASS

raw_first = 2
temporal_first = 3

observed = 10
matched = 10
error = 0

regimes = [2, 8]
horizons = [4, 10]

fragments = 2
resets = 1
```

Raw sequence:

```text
PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> PASS -> RETRY -> PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> PASS -> RETRY -> PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
reset-aware logic fixes recovery-then-relapse
```

The old static rule failed here.

The reset-aware rule finds two regimes:

```text
regime 1 starts at 2
regime 2 starts at 8
```

The first regime is invalidated by recovery.

The second regime becomes the valid persistent collapse regime.

Observed persistent collapse:

```text
10
```

Matched dynamic horizon:

```text
10
```

Error:

```text
0
```

This is the most important positive result.

---

### fragmented_persistence

```text
status = CHECK

raw_first = 2
temporal_first = 3

observed = None
matched = None
error = None

regimes = [2]
horizons = [4]

fragments = 1
resets = 4
```

Raw sequence:

```text
PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> PASS -> ESCALATE -> COLLAPSE -> PASS -> ESCALATE -> COLLAPSE -> PASS -> ESCALATE -> COLLAPSE -> PASS -> ESCALATE -> COLLAPSE
```

Interpretation:

```text
fragmented collapse produces repeated local confirmations
but no global persistent collapse
```

This is why the experiment remains CHECK.

The problem is not horizon prediction.

The problem is classification.

This trajectory needs a separate fragmentation classifier.

---

### dual_regime_collapse

```text
status = PASS

raw_first = 3
temporal_first = 4

observed = 5
matched = 5
error = 0

regimes = [3, 9]
horizons = [5, 11]

fragments = 2
resets = 1
```

Raw sequence:

```text
PASS -> PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> PASS -> PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> PASS -> PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
dual-regime collapse remains predictable
```

The first valid regime already becomes persistent.

The second regime is also detected but not needed for first persistent horizon matching.

---

### delayed_secondary_collapse

```text
status = PASS

raw_first = 3
temporal_first = 10

observed = 11
matched = 11
error = 0

regimes = [9]
horizons = [11]

fragments = 1
resets = 0
```

Raw sequence:

```text
PASS -> PASS -> ESCALATE -> COLLAPSE -> PASS -> PASS -> PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> PASS -> ESCALATE -> ESCALATE -> PASS -> PASS -> PASS -> ESCALATE -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
delayed secondary collapse remains predictable
```

The insufficient early collapse does not create a regime.

The later valid collapse regime becomes the correct anchor.

---

## Core Result

The reset-aware rule restored the horizon error:

```text
mean_dynamic_horizon_error = 0
max_abs_dynamic_horizon_error = 0
```

This means:

```text
dynamic reset logic solved horizon drift
```

The remaining CHECK is not caused by timing error.

It is caused by unresolved collapse topology.

---

## Fragmentation Boundary

The fragmented trajectory shows that collapse can be locally confirmed many times without becoming globally persistent.

This creates a new structural distinction:

```text
persistent collapse
```

versus:

```text
fragmented local collapse
```

The current reset-aware horizon can predict regimes, but it does not yet classify fragmentation topology.

---

## What Was Fixed

This experiment fixed the previous failure:

```text
recovery_then_relapse
```

Previous dynamic horizon result:

```text
predicted = 4
observed = 10
error = 6
```

Reset-aware result:

```text
regimes = [2, 8]
horizons = [4, 10]
observed = 10
matched = 10
error = 0
```

So the horizon rule is restored when regime resets are recognized.

---

## What Remains Open

The remaining open problem is:

```text
fragmentation classification
```

The fragmented trajectory does not show persistent global collapse.

It shows repeated local collapse fragments.

This requires a new classification layer.

---

## Structural Interpretation

The system now separates three temporal cases:

```text
1. coherent persistent collapse
2. recovered collapse with relapse
3. fragmented local collapse
```

The reset-aware horizon solves case 2.

It does not yet classify case 3.

This is the correct next boundary.

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO.

It shows that temporal collapse cannot be measured only as event timing.

It must also be measured as regime topology.

OMNIATEMPO therefore needs both:

```text
critical horizon timing
```

and:

```text
collapse topology classification
```

---

## Relation To TDelta

This experiment refines the TDelta path.

A simple first divergence time is insufficient.

The system may:

```text
collapse
recover
relapse
fragment
```

So TDelta-like measurement must become regime-aware:

```text
TΔ_first
TΔ_valid
TΔ_persistent
TΔ_reset
TΔ_fragmented
```

The reset-aware horizon is a step toward this.

---

## What This Confirms

This experiment supports:

```text
reset-aware horizon logic
dynamic critical horizon rule
zero dynamic horizon error
recovery-then-relapse repair
delayed onset prediction
secondary collapse prediction
spike filtering
oscillation filtering
fragmentation boundary detection
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal dynamic reset law
full fragmentation classification
real-world temporal reliability
semantic correctness
causal correctness
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates reset-aware horizon prediction and exposes the next classification boundary.

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
reset-aware dynamic temporal collapse horizon behavior
```

---

## Limitations

```text
Only 8 dynamic trajectory families were tested.

Trajectory length is fixed at 16.

Confirmation window is fixed at 2.

Persistence window is fixed at 2.

Reset window is fixed at 2.

Trajectories are synthetic.

Fragmentation classification is not yet formalized.

No external temporal dataset was used.

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
Level 2 — Reset-Aware Dynamic Horizon
```

Reason:

```text
8 dynamic trajectories tested

7 trajectories passed

1 trajectory exposed fragmentation boundary

dynamic horizon error = 0

recovery-then-relapse repaired

reset-aware rule matched all observable persistent regimes

fragmented persistence requires separate classification
```

This is not a failed result.

It is a successful horizon repair plus a new boundary diagnosis.

---

## Relation To Previous Results

Validation path:

```text
Effective Observer Count v0
-> raw_count != effective_count

Recoverability Effective Observer v0
-> flawed recoverability proxy exposed

Recoverability Effective Observer v1
-> proxy corrected

Correlation Analysis v0
-> effective_count beats raw_count

Correlation Stability v0
-> correlation stability verified

Correlation Adversarial v0
-> adversarial boundary exposed

Recoverability Gate v0
-> multi-signal gate detects instability

Recoverability Gate Stability v0
-> threshold stability verified

Recoverability Gate Adversarial v0
-> adversarial resistance improved

Recoverability Gate Randomized v0
-> coherent randomized behavior

Recoverability Gate Randomized Stability v0
-> stable randomized behavior

Recoverability Gate External Proxy v0
-> external-style shift exposes mismatch

Cross-Gate Disagreement Analysis v0
-> signal conflict regimes measured

Cross-Gate Disagreement Stability v0
-> conflict remains stable across populations

Cross-Gate Real Dataset Proxy v0
-> mild proxy dataset under-stressed

Cross-Gate Real Dataset Proxy Stressed v0
-> stronger disagreement achieved without confirmed collapse

Cross-Gate Real Dataset Proxy Collapse v0
-> arbitration COLLAPSE appears under multi-gate confirmed pressure

Collapse Confirmation Stability v0
-> collapse remains present but confirmation-source identity is perturbation-sensitive

Collapse Confirmation Source Swap v0
-> collapse remains stable when confirmation source changes

Temporal Collapse Degradation v0
-> temporal degradation is measurable but single-frame collapse requires confirmation

Temporal Collapse Confirmation v0
-> transient collapse is filtered but persistence requires longer trajectories

Temporal Collapse Persistence v0
-> persistent collapse confirmed while transient collapse is filtered

Temporal Collapse Persistence Stability v0
-> persistence stable under mild window variation but scale-sensitive under strict windows

Temporal Collapse Phase Diagram v0
-> temporal observability boundary mapped across trajectory length and window space

Temporal Collapse Critical Horizon v0
-> first horizon law exposed systematic offset

Temporal Collapse Critical Horizon Corrected v0
-> corrected horizon law matches all observable clean-regime pairs

Temporal Collapse Dynamic Horizon v0
-> recovery and relapse expose need for reset-aware horizon logic

Temporal Collapse Regime Reset v0
-> reset-aware horizon restores zero-error prediction but exposes fragmentation classification boundary
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_fragmentation_classification_v0.py
```

Purpose:

```text
distinguish persistent global collapse from fragmented local collapse
```

Main question:

```text
can local collapse fragments be classified
without falsely promoting them to global persistence?
```

Required classes:

```text
GLOBAL_PERSISTENT_COLLAPSE

RECOVERY_RELAPSE_COLLAPSE

FRAGMENTED_LOCAL_COLLAPSE

OSCILLATING_NONPERSISTENT

SPIKE_FILTERED

CLEAN_PASS
```

Required measurements:

```text
collapse_run_count
temporal_collapse_run_count
max_temporal_collapse_run_length
persistence_reset_count
fragmentation_index
global_persistence_detected
local_confirmation_count
```

Expected result:

```text
fragmented_persistence becomes classified as FRAGMENTED_LOCAL_COLLAPSE
instead of CHECK
```

---

## Final Result

```text
CHECK — reset-aware dynamic horizon did not fully restore predictability.
```

More precise conclusion:

```text
reset-aware dynamic horizon restored zero-error prediction
for observable persistent regimes,
but fragmented local collapse requires separate topology classification.
```