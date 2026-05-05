# Temporal Collapse Fragmentation Classification v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Collapse Topology Classification
```

---

## Purpose

This experiment tests whether temporal collapse trajectories can be classified by topology.

Previous experiments measured collapse timing, persistence, horizon prediction, and reset-aware regime behavior.

The remaining unresolved case was:

```text
fragmented_persistence
```

It produced repeated local collapse confirmations but no global persistent collapse.

This experiment turns that ambiguity into an explicit structural class:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

Core question:

```text
can local collapse fragments be classified
without falsely promoting them to global persistence?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates temporal collapse topology.

---

## Experiment File

```text
examples/temporal_collapse_fragmentation_classification_v0.py
```

Result file:

```text
results/temporal_collapse_fragmentation_classification_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_fragmentation_classification_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

trajectory_count = 6

pass_trajectory_count = 6
check_trajectory_count = 0

confirmation_window = 2
persistence_window = 2
reset_window = 2
```

Supported classes:

```text
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
CLEAN_PASS
```

The experiment passed.

All six temporal collapse topologies were correctly separated.

---

## Main Finding

The central result is:

```text
fragmented_local_collapse
->
FRAGMENTED_LOCAL_COLLAPSE
```

This closes the boundary left open by the reset-aware regime experiment.

Fragmentation is no longer an ambiguous CHECK condition.

It is now a measurable temporal topology.

---

## Structural Shift

The system moved from:

```text
collapse / no collapse
```

to:

```text
collapse topology classification
```

This is an important OMNIATEMPO transition.

The system now distinguishes:

```text
global persistence
recovery-relapse persistence
fragmented local collapse
oscillation without persistence
single-frame spike
clean pass
```

---

## Classification Logic

The classifier measures:

```text
collapse_run_count
max_temporal_collapse_run_length
temporal_collapse_run_count
persistence_reset_count
fragmentation_index
global_persistence_detected
local_confirmation_count
collapse_runs
```

Then it assigns one of six classes.

---

## Class Definitions

### CLEAN_PASS

Definition:

```text
no collapse run exists
```

Meaning:

```text
the trajectory remains structurally clean
```

---

### SPIKE_FILTERED

Definition:

```text
one collapse run exists
and its maximum length is 1
```

Meaning:

```text
a single-frame collapse spike occurred
but it did not become local or global persistence
```

---

### GLOBAL_PERSISTENT_COLLAPSE

Definition:

```text
global persistence is detected
and no reset occurs
```

Meaning:

```text
collapse becomes continuous and globally persistent
```

---

### RECOVERY_RELAPSE_COLLAPSE

Definition:

```text
global persistence is detected
and at least one reset occurs
```

Meaning:

```text
collapse appears,
recovery interrupts it,
then relapse produces persistent collapse
```

---

### FRAGMENTED_LOCAL_COLLAPSE

Definition:

```text
local confirmation exists
but global persistence is not detected
```

Meaning:

```text
collapse appears in repeated local fragments
without becoming globally persistent
```

---

### OSCILLATING_NONPERSISTENT

Definition:

```text
collapse events exist
but no local confirmation exists
```

Meaning:

```text
collapse oscillates in isolated frames
without persistence
```

---

## Trajectory Results

### clean_pass

```text
status = PASS
class = CLEAN_PASS

collapse_run_count = 0
max_temporal_collapse_run_length = 0
local_confirmation_count = 0
global_persistence_detected = False
persistence_reset_count = 0
fragmentation_index = 0.0
```

Raw sequence:

```text
PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS
```

Interpretation:

```text
no collapse topology is present
```

The classifier correctly identifies a clean trajectory.

---

### global_persistent_collapse

```text
status = PASS
class = GLOBAL_PERSISTENT_COLLAPSE

collapse_run_count = 1
max_temporal_collapse_run_length = 12
local_confirmation_count = 1
global_persistence_detected = True
persistence_reset_count = 0
fragmentation_index = 0.0
```

Collapse runs:

```text
[4, 15]
```

Raw sequence:

```text
PASS -> PASS -> RETRY -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
single uninterrupted collapse regime
```

The classifier correctly detects global persistent collapse.

---

### recovery_relapse_collapse

```text
status = PASS
class = RECOVERY_RELAPSE_COLLAPSE

collapse_run_count = 2
max_temporal_collapse_run_length = 8
local_confirmation_count = 2
global_persistence_detected = True
persistence_reset_count = 1
fragmentation_index = 0.5
```

Collapse runs:

```text
[2, 3]
[8, 15]
```

Raw sequence:

```text
PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> PASS -> RETRY -> PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
early collapse is interrupted,
then later relapse becomes globally persistent
```

The classifier correctly distinguishes this from simple global collapse.

---

### fragmented_local_collapse

```text
status = PASS
class = FRAGMENTED_LOCAL_COLLAPSE

collapse_run_count = 5
max_temporal_collapse_run_length = 2
local_confirmation_count = 5
global_persistence_detected = False
persistence_reset_count = 4
fragmentation_index = 0.8
```

Collapse runs:

```text
[2, 3]
[5, 6]
[8, 9]
[11, 12]
[14, 15]
```

Raw sequence:

```text
PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
repeated local confirmations exist,
but no global persistent collapse exists
```

This is the key success case.

The previous CHECK boundary is now classified explicitly.

---

### oscillating_nonpersistent

```text
status = PASS
class = OSCILLATING_NONPERSISTENT

collapse_run_count = 7
max_temporal_collapse_run_length = 1
local_confirmation_count = 0
global_persistence_detected = False
persistence_reset_count = 6
fragmentation_index = 0.8571
```

Collapse runs:

```text
[2, 2]
[4, 4]
[6, 6]
[8, 8]
[10, 10]
[12, 12]
[14, 14]
```

Raw sequence:

```text
PASS -> ESCALATE -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS
```

Interpretation:

```text
many isolated collapse events exist,
but none reach local confirmation
```

The classifier correctly separates oscillation from fragmentation.

---

### spike_filtered

```text
status = PASS
class = SPIKE_FILTERED

collapse_run_count = 1
max_temporal_collapse_run_length = 1
local_confirmation_count = 0
global_persistence_detected = False
persistence_reset_count = 0
fragmentation_index = 0.0
```

Collapse runs:

```text
[1, 1]
```

Raw sequence:

```text
PASS -> COLLAPSE -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS
```

Interpretation:

```text
a single-frame collapse spike is isolated
```

The classifier correctly separates spike from oscillation and fragmentation.

---

## Topology Metrics

### Collapse Run Count

```text
collapse_run_count
```

Measures how many collapse intervals exist.

This separates:

```text
single persistent regime
```

from:

```text
multiple fragmented regimes
```

---

### Maximum Collapse Run Length

```text
max_temporal_collapse_run_length
```

Measures the longest collapse interval.

This separates:

```text
single-frame spikes
```

from:

```text
local confirmation
```

and:

```text
global persistence
```

---

### Local Confirmation Count

```text
local_confirmation_count
```

Counts collapse runs long enough to satisfy the confirmation window.

This separates:

```text
oscillation
```

from:

```text
fragmentation
```

---

### Global Persistence Detection

```text
global_persistence_detected
```

Detects whether collapse persists long enough to become a global collapse regime.

This separates:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

from:

```text
GLOBAL_PERSISTENT_COLLAPSE
```

and:

```text
RECOVERY_RELAPSE_COLLAPSE
```

---

### Persistence Reset Count

```text
persistence_reset_count
```

Counts interruptions between collapse runs.

This separates:

```text
single global collapse
```

from:

```text
recovery-relapse collapse
```

and:

```text
fragmented local collapse
```

---

### Fragmentation Index

```text
fragmentation_index
```

A simple ratio:

```text
persistence_reset_count / collapse_run_count
```

High values indicate repeated interrupted collapse.

Examples:

```text
fragmented_local_collapse = 0.8
oscillating_nonpersistent = 0.8571
recovery_relapse_collapse = 0.5
global_persistent_collapse = 0.0
```

The index alone is not sufficient.

It must be interpreted with:

```text
local_confirmation_count
global_persistence_detected
max_temporal_collapse_run_length
```

---

## Main Structural Result

The experiment establishes a temporal collapse taxonomy:

```text
CLEAN_PASS
SPIKE_FILTERED
OSCILLATING_NONPERSISTENT
FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
```

This is not just detection.

It is classification of temporal collapse shape.

---

## Why This Matters

The previous reset-aware experiment had one unresolved case:

```text
fragmented_persistence
```

That case was not a failure of horizon timing.

It was a missing class.

This experiment adds the missing class and resolves the ambiguity.

---

## Relation To Regime Reset v0

Regime Reset v0 showed:

```text
mean_dynamic_horizon_error = 0
max_abs_dynamic_horizon_error = 0
```

but still returned CHECK because fragmented persistence was structurally unresolved.

Fragmentation Classification v0 resolves that boundary:

```text
fragmented_local_collapse
->
FRAGMENTED_LOCAL_COLLAPSE
```

So the remaining ambiguity becomes a named topology.

---

## Relation To OMNIATEMPO

This experiment is a major OMNIATEMPO step.

It shows that temporal collapse must be measured as:

```text
event
run
regime
fragmentation
persistence
recovery
relapse
```

not merely as:

```text
COLLAPSE / PASS
```

This is the beginning of temporal structural taxonomy.

---

## Relation To TDelta

This experiment supports a richer TDelta direction.

A single divergence time is not enough.

Different temporal topologies require different timing concepts:

```text
TΔ_spike
TΔ_local
TΔ_global
TΔ_fragmented
TΔ_relapse
TΔ_persistent
```

Fragmentation classification makes those future distinctions possible.

---

## What This Confirms

This experiment supports:

```text
collapse topology classification
clean pass detection
spike filtering
oscillation separation
fragmented local collapse classification
recovery-relapse classification
global persistent collapse classification
local confirmation measurement
global persistence measurement
fragmentation index measurement
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal collapse topology taxonomy
real-world temporal reliability
semantic correctness
causal correctness
optimal fragmentation index
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates a controlled synthetic topology classifier.

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
temporal collapse topology classification
```

---

## Limitations

```text
Only 6 topology classes were tested.

Only synthetic trajectories were used.

Trajectory length is fixed at 16.

Confirmation window is fixed at 2.

Persistence window is fixed at 2.

Reset window is fixed at 2.

Fragmentation index is simple and provisional.

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
Level 2 — Temporal Collapse Topology Classification
```

Reason:

```text
6 trajectory classes tested

6 / 6 correctly classified

fragmented local collapse separated from global persistence

oscillation separated from fragmentation

spike separated from oscillation

recovery-relapse separated from global persistence

clean pass detected correctly
```

This is a successful controlled topology classification experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_stability_v0.py
```

Purpose:

```text
test whether topology classification remains stable
under perturbations of run length, reset gaps, and collapse density
```

Main question:

```text
does the temporal collapse taxonomy remain stable
when trajectory parameters vary?
```

Required perturbations:

```text
different trajectory lengths
different collapse run lengths
different recovery gap lengths
different fragmentation densities
different oscillation frequencies
different spike positions
```

Required checks:

```text
GLOBAL_PERSISTENT_COLLAPSE remains stable

RECOVERY_RELAPSE_COLLAPSE remains stable

FRAGMENTED_LOCAL_COLLAPSE remains stable

OSCILLATING_NONPERSISTENT remains stable

SPIKE_FILTERED remains stable

CLEAN_PASS remains stable
```

Expected output:

```text
classification stability matrix
class-wise pass rates
boundary cases between oscillation and fragmentation
boundary cases between fragmentation and persistence
```

---

## Final Result

```text
PASS — fragmentation topology classification successfully separated persistent, fragmented, oscillating, spike, and clean regimes.
```

Correct final conclusion:

```text
fragmented local collapse is no longer an ambiguous CHECK condition;
it is now an explicit temporal topology class.
```