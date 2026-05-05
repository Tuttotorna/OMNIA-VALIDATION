# Temporal Collapse Topology Window Sensitivity v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Window Sensitivity
```

---

## Purpose

This experiment tests whether temporal collapse topology classification remains coherent when the temporal windows change.

Previous experiments established:

```text
temporal topology classification
topology stability under perturbation
threshold boundary consistency
```

However, those tests used fixed temporal windows.

This experiment varies:

```text
confirmation_window
persistence_window
```

Core question:

```text
does the temporal topology boundary map remain coherent
when confirmation and persistence windows change?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates temporal-window sensitivity of topology classification.

---

## Experiment File

```text
examples/temporal_collapse_topology_window_sensitivity_v0.py
```

Result file:

```text
results/temporal_collapse_topology_window_sensitivity_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_window_sensitivity_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

case_count = 63

pass_case_count = 63
check_case_count = 0
pass_rate = 1.0

confirmation_windows = [2, 3, 4]
persistence_windows = [2, 3, 4]

global_persistence_thresholds = [4, 5, 6, 7, 8]

mean_fragmentation_index = 0.3
max_fragmentation_index = 0.8

mean_max_temporal_collapse_run_length = 3
mean_local_confirmation_count = 1.2698412698412698
```

The experiment passed.

All 63 cases were classified correctly across all tested confirmation and persistence window pairs.

---

## Supported Classes

```text
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
CLEAN_PASS
```

All supported classes remained coherent under tested window perturbations.

---

## Window Grid

Tested confirmation windows:

```text
2
3
4
```

Tested persistence windows:

```text
2
3
4
```

Tested window pairs:

```text
cw2_pw2
cw2_pw3
cw2_pw4

cw3_pw2
cw3_pw3
cw3_pw4

cw4_pw2
cw4_pw3
cw4_pw4
```

Each pair produced:

```text
case_count = 7
pass_count = 7
check_count = 0
pass_rate = 1.0
```

---

## Threshold Rule

The global persistence threshold is:

```text
global_persistence_threshold =
confirmation_window + persistence_window
```

Across this experiment the observed thresholds were:

```text
4
5
6
7
8
```

All threshold shifts behaved coherently.

This means the topology rule scales with window size instead of breaking under window variation.

---

## Main Finding

The central result is:

```text
pass_rate = 1.0
```

and:

```text
63 / 63 cases passed
```

This confirms that the topology boundary map remained coherent under temporal-window perturbation.

The classification did not depend on one fixed parameter setting.

---

## Structural Meaning

This is the important step after threshold-boundary validation.

The previous boundary map showed:

```text
max_run = 1
-> spike / oscillation

max_run >= confirmation_window
-> local confirmation

max_run >= confirmation_window + persistence_window
-> global persistence
```

This experiment shows that those transitions move predictably when the windows change.

So the topology is not fixed to `cw=2`, `pw=2`.

It is parameterized coherently.

---

## Case Type Summary

### clean

```text
cases = 9
pass = 9
check = 0
rate = 1.0
```

Interpretation:

```text
clean trajectories remain CLEAN_PASS under all window pairs
```

---

### spike_below_confirmation

```text
cases = 9
pass = 9
check = 0
rate = 1.0
```

Interpretation:

```text
collapse runs below confirmation_window remain SPIKE_FILTERED
```

For example:

```text
cw = 4
max_run = 3
-> SPIKE_FILTERED
```

This confirms that spike filtering scales with the confirmation window.

---

### single_local_threshold

```text
cases = 9
pass = 9
check = 0
rate = 1.0
```

Interpretation:

```text
runs exactly at confirmation_window become FRAGMENTED_LOCAL_COLLAPSE
```

Examples:

```text
cw = 2
max_run = 2
-> FRAGMENTED_LOCAL_COLLAPSE

cw = 3
max_run = 3
-> FRAGMENTED_LOCAL_COLLAPSE

cw = 4
max_run = 4
-> FRAGMENTED_LOCAL_COLLAPSE
```

Local confirmation boundary shifts correctly.

---

### single_global_threshold

```text
cases = 9
pass = 9
check = 0
rate = 1.0
```

Interpretation:

```text
runs exactly at confirmation_window + persistence_window
become GLOBAL_PERSISTENT_COLLAPSE
```

Examples:

```text
cw = 2, pw = 2, threshold = 4
max_run = 4
-> GLOBAL_PERSISTENT_COLLAPSE

cw = 3, pw = 4, threshold = 7
max_run = 7
-> GLOBAL_PERSISTENT_COLLAPSE

cw = 4, pw = 4, threshold = 8
max_run = 8
-> GLOBAL_PERSISTENT_COLLAPSE
```

Global persistence boundary shifts correctly.

---

### oscillation_below_confirmation

```text
cases = 9
pass = 9
check = 0
rate = 1.0
```

Interpretation:

```text
oscillating one-frame collapse remains OSCILLATING_NONPERSISTENT
```

This remains true even as confirmation_window increases.

---

### fragmentation_at_confirmation

```text
cases = 9
pass = 9
check = 0
rate = 1.0
```

Interpretation:

```text
repeated runs at confirmation_window become FRAGMENTED_LOCAL_COLLAPSE
```

The system distinguishes:

```text
repeated below-confirmation instability
```

from:

```text
repeated locally confirmed collapse
```

under all tested window pairs.

---

### recovery_relapse_global

```text
cases = 9
pass = 9
check = 0
rate = 1.0
```

Interpretation:

```text
local collapse followed by global collapse remains RECOVERY_RELAPSE_COLLAPSE
```

This remains coherent as global threshold shifts from 4 to 8.

---

## Window Pair Summary

### cw2_pw2

```text
threshold = 4
cases = 7
pass = 7
check = 0
rate = 1.0
```

---

### cw2_pw3

```text
threshold = 5
cases = 7
pass = 7
check = 0
rate = 1.0
```

---

### cw2_pw4

```text
threshold = 6
cases = 7
pass = 7
check = 0
rate = 1.0
```

---

### cw3_pw2

```text
threshold = 5
cases = 7
pass = 7
check = 0
rate = 1.0
```

---

### cw3_pw3

```text
threshold = 6
cases = 7
pass = 7
check = 0
rate = 1.0
```

---

### cw3_pw4

```text
threshold = 7
cases = 7
pass = 7
check = 0
rate = 1.0
```

---

### cw4_pw2

```text
threshold = 6
cases = 7
pass = 7
check = 0
rate = 1.0
```

---

### cw4_pw3

```text
threshold = 7
cases = 7
pass = 7
check = 0
rate = 1.0
```

---

### cw4_pw4

```text
threshold = 8
cases = 7
pass = 7
check = 0
rate = 1.0
```

Every window pair passed fully.

---

## Boundary Behavior Under Window Perturbation

The experiment confirms these moving boundaries:

```text
max_run < confirmation_window
-> SPIKE_FILTERED or OSCILLATING_NONPERSISTENT

max_run >= confirmation_window
and max_run < confirmation_window + persistence_window
-> FRAGMENTED_LOCAL_COLLAPSE

max_run >= confirmation_window + persistence_window
and collapse_run_count = 1
-> GLOBAL_PERSISTENT_COLLAPSE

max_run >= confirmation_window + persistence_window
and collapse_run_count > 1
-> RECOVERY_RELAPSE_COLLAPSE
```

This is the operational window-sensitive topology map.

---

## Main Structural Result

The topology classifier is not merely stable under fixed windows.

It remains coherent as the temporal windows shift.

That means the taxonomy is parameterized by:

```text
confirmation_window
persistence_window
```

but not arbitrarily dependent on them.

The boundaries move according to a simple structural law:

```text
global_persistence_threshold =
confirmation_window + persistence_window
```

---

## Relation To Threshold Boundary v0

Threshold Boundary v0 validated exact boundaries for:

```text
confirmation_window = 2
persistence_window = 2
```

Window Sensitivity v0 generalizes that result across:

```text
confirmation_window = 2, 3, 4
persistence_window = 2, 3, 4
```

So the validation sequence is:

```text
boundary consistency at fixed windows
->
boundary consistency under window perturbation
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO.

It shows that temporal topology is not just a fixed label.

It is a window-sensitive structural classification that scales coherently with observation requirements.

This supports the idea that temporal collapse must be measured relative to an observation protocol.

But the protocol must deform the boundaries predictably.

Here, it does.

---

## Relation To TDelta

This experiment also strengthens future TDelta work.

A TDelta value depends on the temporal confirmation and persistence protocol.

This result shows that the protocol can be varied without destroying classification coherence.

That is necessary before defining robust TDelta-like temporal indices.

---

## What This Confirms

This experiment supports:

```text
window-sensitive topology coherence
confirmation-window scaling
persistence-window scaling
global-threshold scaling
spike filtering under larger confirmation windows
local confirmation under larger confirmation windows
global persistence under larger persistence windows
recovery-relapse distinction under shifted thresholds
fragmentation stability under shifted thresholds
oscillation stability under shifted thresholds
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal optimal windows
real-world temporal reliability
semantic correctness
causal correctness
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates controlled synthetic window sensitivity.

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
temporal collapse topology sensitivity
under confirmation-window and persistence-window perturbation
```

---

## Limitations

```text
Only confirmation_window values 2, 3, 4 were tested.

Only persistence_window values 2, 3, 4 were tested.

Only 63 synthetic cases were tested.

Case generation was controlled and deterministic.

No noisy probabilistic trajectories were used.

No external temporal dataset was used.

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
Level 2 — Temporal Topology Window Sensitivity
```

Reason:

```text
63 cases tested

63 / 63 cases passed

7 / 7 case types passed under all window pairs

9 / 9 window pairs had pass_rate = 1.0

global persistence threshold shifted correctly from 4 to 8

classification remained coherent under confirmation and persistence window perturbation
```

This is a successful controlled window-sensitivity experiment.

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

Temporal Collapse Fragmentation Classification v0
-> fragmented local collapse becomes an explicit temporal topology class

Temporal Collapse Topology Stability v0
-> temporal collapse topology classification remains invariant under controlled perturbations

Temporal Collapse Topology Threshold Boundary v0
-> class transition boundaries remain consistent across tested threshold cases

Temporal Collapse Topology Window Sensitivity v0
-> topology boundaries remain coherent under confirmation-window and persistence-window perturbation
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_noise_robustness_v0.py
```

Purpose:

```text
test whether the topology classifier remains stable
under controlled noise injection
```

Main question:

```text
does temporal topology classification survive sparse noisy frame flips?
```

Required perturbations:

```text
PASS -> COLLAPSE noise
COLLAPSE -> PASS dropout
ESCALATE insertion
single-frame false spikes
single-frame missing collapse
mixed local dropout
```

Required checks:

```text
global persistence should remain global under sparse dropout

fragmentation should not become global from one noisy spike

oscillation should not become fragmentation unless local confirmation appears

spike should remain filtered

clean pass should tolerate sparse nonpersistent spikes

recovery-relapse should remain distinct under small noise
```

Expected output:

```text
noise robustness matrix
class-wise robustness rates
noise-induced boundary failures
```

---

## Final Result

```text
PASS — topology window sensitivity remained coherent across confirmation and persistence window perturbations.
```

Correct final conclusion:

```text
the temporal collapse topology map scales coherently with confirmation and persistence window changes.
```