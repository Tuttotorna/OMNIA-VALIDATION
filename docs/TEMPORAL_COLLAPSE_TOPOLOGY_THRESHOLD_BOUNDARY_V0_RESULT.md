# Temporal Collapse Topology Threshold Boundary v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Boundary Map
```

---

## Purpose

This experiment tests the exact threshold boundaries between temporal collapse topology classes.

The previous experiment showed that topology classification remains stable under controlled perturbations.

This experiment asks a sharper question:

```text
where does one temporal collapse class become another?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates boundary behavior between temporal collapse topology classes.

---

## Experiment File

```text
examples/temporal_collapse_topology_threshold_boundary_v0.py
```

Result file:

```text
results/temporal_collapse_topology_threshold_boundary_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_threshold_boundary_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

case_count = 16

pass_case_count = 16
check_case_count = 0
pass_rate = 1.0

confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4

mean_fragmentation_index = 0.30644375
max_fragmentation_index = 0.8889

mean_max_temporal_collapse_run_length = 2.75
mean_local_confirmation_count = 1.5
```

The experiment passed.

All tested boundary cases were classified consistently.

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

---

## Main Finding

The central result is:

```text
pass_rate = 1.0
```

and:

```text
16 / 16 boundary cases passed
```

This means the tested class-transition thresholds behaved consistently.

No tested boundary produced ambiguous classification.

---

## Threshold Rule

The key threshold is:

```text
global_persistence_threshold =
confirmation_window + persistence_window
```

In this experiment:

```text
confirmation_window = 2
persistence_window = 2
```

Therefore:

```text
global_persistence_threshold = 4
```

So the observed boundary is:

```text
max_run = 1
-> spike / oscillation

max_run = 2 or 3
-> local fragmentation

max_run >= 4
-> global persistence
```

The exact threshold case passed:

```text
max_run = 3 -> FRAGMENTED_LOCAL_COLLAPSE
max_run = 4 -> GLOBAL_PERSISTENT_COLLAPSE
```

---

## Boundary Families Tested

The experiment tested eight boundary families:

```text
clean_vs_spike
spike_vs_local_confirmation
local_vs_global
oscillation_vs_fragmentation
fragmented_vs_recovery_relapse
global_vs_recovery_relapse
exact_global_threshold
dense_oscillation_vs_dense_fragmentation
```

Each boundary family had:

```text
case_count = 2
pass_count = 2
check_count = 0
pass_rate = 1.0
```

---

## Boundary Family Results

### clean_vs_spike

```text
cases = 2
pass = 2
check = 0
rate = 1.0
```

Boundary:

```text
no collapse
```

versus:

```text
single-frame collapse
```

Result:

```text
CLEAN_PASS
SPIKE_FILTERED
```

---

### spike_vs_local_confirmation

```text
cases = 2
pass = 2
check = 0
rate = 1.0
```

Boundary:

```text
max_run = 1
```

versus:

```text
max_run = 2
```

Result:

```text
SPIKE_FILTERED
FRAGMENTED_LOCAL_COLLAPSE
```

---

### local_vs_global

```text
cases = 2
pass = 2
check = 0
rate = 1.0
```

Boundary:

```text
max_run = 3
```

versus:

```text
max_run = 4
```

Result:

```text
FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
```

---

### oscillation_vs_fragmentation

```text
cases = 2
pass = 2
check = 0
rate = 1.0
```

Boundary:

```text
many collapse runs of length 1
```

versus:

```text
many collapse runs of length 2
```

Result:

```text
OSCILLATING_NONPERSISTENT
FRAGMENTED_LOCAL_COLLAPSE
```

---

### fragmented_vs_recovery_relapse

```text
cases = 2
pass = 2
check = 0
rate = 1.0
```

Boundary:

```text
two local collapse runs
```

versus:

```text
one local run plus one global run
```

Result:

```text
FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

---

### global_vs_recovery_relapse

```text
cases = 2
pass = 2
check = 0
rate = 1.0
```

Boundary:

```text
one global collapse run
```

versus:

```text
multiple runs with global persistence after reset
```

Result:

```text
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

---

### exact_global_threshold

```text
cases = 2
pass = 2
check = 0
rate = 1.0
```

Boundary:

```text
global_threshold - 1
```

versus:

```text
global_threshold
```

Result:

```text
FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
```

This is the most important threshold validation.

---

### dense_oscillation_vs_dense_fragmentation

```text
cases = 2
pass = 2
check = 0
rate = 1.0
```

Boundary:

```text
dense repeated runs of length 1
```

versus:

```text
dense repeated runs of length 2
```

Result:

```text
OSCILLATING_NONPERSISTENT
FRAGMENTED_LOCAL_COLLAPSE
```

High fragmentation alone did not cause class confusion.

---

## Boundary Case Results

### B00_clean_no_collapse

```text
status = PASS
expected = CLEAN_PASS
predicted = CLEAN_PASS

runs = 0
max_run = 0
local = 0
global = False
fragmentation_index = 0.0
```

Interpretation:

```text
absence of collapse remains clean pass
```

---

### B01_single_spike_len1

```text
status = PASS
expected = SPIKE_FILTERED
predicted = SPIKE_FILTERED

runs = 1
max_run = 1
local = 0
global = False
fragmentation_index = 0.0
```

Interpretation:

```text
single-frame collapse becomes spike, not persistence
```

---

### B02_single_run_len1_spike

```text
status = PASS
expected = SPIKE_FILTERED
predicted = SPIKE_FILTERED

runs = 1
max_run = 1
local = 0
global = False
fragmentation_index = 0.0
```

Interpretation:

```text
a one-frame run remains below local confirmation
```

---

### B03_single_run_len2_local

```text
status = PASS
expected = FRAGMENTED_LOCAL_COLLAPSE
predicted = FRAGMENTED_LOCAL_COLLAPSE

runs = 1
max_run = 2
local = 1
global = False
fragmentation_index = 0.0
```

Interpretation:

```text
max_run = 2 crosses local confirmation threshold
```

---

### B04_single_run_len3_local_only

```text
status = PASS
expected = FRAGMENTED_LOCAL_COLLAPSE
predicted = FRAGMENTED_LOCAL_COLLAPSE

runs = 1
max_run = 3
local = 1
global = False
fragmentation_index = 0.0
```

Interpretation:

```text
max_run = 3 remains local, not global
```

---

### B05_single_run_len4_global

```text
status = PASS
expected = GLOBAL_PERSISTENT_COLLAPSE
predicted = GLOBAL_PERSISTENT_COLLAPSE

runs = 1
max_run = 4
local = 1
global = True
fragmentation_index = 0.0
```

Interpretation:

```text
max_run = 4 reaches global persistence threshold
```

---

### B06_many_len1_oscillation

```text
status = PASS
expected = OSCILLATING_NONPERSISTENT
predicted = OSCILLATING_NONPERSISTENT

runs = 7
max_run = 1
local = 0
global = False
fragmentation_index = 0.8571
```

Interpretation:

```text
high fragmentation index alone does not imply fragmentation
```

No local confirmations exist.

So the class remains oscillation.

---

### B07_many_len2_fragmented

```text
status = PASS
expected = FRAGMENTED_LOCAL_COLLAPSE
predicted = FRAGMENTED_LOCAL_COLLAPSE

runs = 5
max_run = 2
local = 5
global = False
fragmentation_index = 0.8
```

Interpretation:

```text
many local confirmations without global persistence become fragmented local collapse
```

---

### B08_two_len2_fragmented

```text
status = PASS
expected = FRAGMENTED_LOCAL_COLLAPSE
predicted = FRAGMENTED_LOCAL_COLLAPSE

runs = 2
max_run = 2
local = 2
global = False
fragmentation_index = 0.5
```

Interpretation:

```text
two local runs are still fragmented, not relapse, unless global persistence appears
```

---

### B09_len2_then_len4_relapse

```text
status = PASS
expected = RECOVERY_RELAPSE_COLLAPSE
predicted = RECOVERY_RELAPSE_COLLAPSE

runs = 2
max_run = 4
local = 2
global = True
fragmentation_index = 0.5
```

Interpretation:

```text
a later global run after earlier local collapse becomes recovery-relapse collapse
```

---

### B10_single_global_run

```text
status = PASS
expected = GLOBAL_PERSISTENT_COLLAPSE
predicted = GLOBAL_PERSISTENT_COLLAPSE

runs = 1
max_run = 7
local = 1
global = True
fragmentation_index = 0.0
```

Interpretation:

```text
single uninterrupted global run remains global persistence
```

---

### B11_two_runs_second_global

```text
status = PASS
expected = RECOVERY_RELAPSE_COLLAPSE
predicted = RECOVERY_RELAPSE_COLLAPSE

runs = 2
max_run = 7
local = 2
global = True
fragmentation_index = 0.5
```

Interpretation:

```text
multiple runs with global persistence become recovery-relapse
```

---

### B12_global_threshold_minus_1

```text
status = PASS
expected = FRAGMENTED_LOCAL_COLLAPSE
predicted = FRAGMENTED_LOCAL_COLLAPSE

runs = 1
max_run = 3
local = 1
global = False
fragmentation_index = 0.0
```

Interpretation:

```text
one step below global threshold remains local
```

---

### B13_global_threshold_exact

```text
status = PASS
expected = GLOBAL_PERSISTENT_COLLAPSE
predicted = GLOBAL_PERSISTENT_COLLAPSE

runs = 1
max_run = 4
local = 1
global = True
fragmentation_index = 0.0
```

Interpretation:

```text
exact global threshold becomes global persistence
```

---

### B14_dense_len1_oscillation

```text
status = PASS
expected = OSCILLATING_NONPERSISTENT
predicted = OSCILLATING_NONPERSISTENT

runs = 9
max_run = 1
local = 0
global = False
fragmentation_index = 0.8889
```

Interpretation:

```text
dense single-frame instability remains oscillation
```

Even with very high fragmentation index, no local confirmation exists.

---

### B15_dense_len2_fragmentation

```text
status = PASS
expected = FRAGMENTED_LOCAL_COLLAPSE
predicted = FRAGMENTED_LOCAL_COLLAPSE

runs = 7
max_run = 2
local = 7
global = False
fragmentation_index = 0.8571
```

Interpretation:

```text
dense local confirmations become fragmented local collapse
```

This confirms the difference between dense oscillation and dense fragmentation.

---

## Boundary Map

The experiment supports this boundary map:

```text
no collapse
-> CLEAN_PASS

one run, max_run = 1
-> SPIKE_FILTERED

multiple runs, max_run = 1
-> OSCILLATING_NONPERSISTENT

max_run >= 2 and max_run < 4
and global_persistence_detected = False
-> FRAGMENTED_LOCAL_COLLAPSE

max_run >= 4
and collapse_run_count = 1
-> GLOBAL_PERSISTENT_COLLAPSE

max_run >= 4
and collapse_run_count > 1
-> RECOVERY_RELAPSE_COLLAPSE
```

With current settings:

```text
confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4
```

---

## Main Structural Result

The core result is:

```text
threshold boundaries between topology classes are consistent
```

The taxonomy does not merely classify stable cases.

It also handles exact transition points.

This moves the system from:

```text
taxonomy stability
```

to:

```text
boundary geometry
```

---

## Important Finding

High fragmentation index alone is not enough.

Two cases show this clearly:

```text
B14_dense_len1_oscillation
fragmentation_index = 0.8889
class = OSCILLATING_NONPERSISTENT

B15_dense_len2_fragmentation
fragmentation_index = 0.8571
class = FRAGMENTED_LOCAL_COLLAPSE
```

The lower fragmentation index case is fragmented, while the higher fragmentation index case is oscillating.

Therefore the classifier must use:

```text
max_run
local_confirmation_count
global_persistence_detected
collapse_run_count
```

not fragmentation index alone.

---

## Relation To Topology Stability v0

Topology Stability v0 showed that the classes remain stable under broader perturbations.

Threshold Boundary v0 shows that the exact transition points also behave consistently.

So the validation sequence is:

```text
classification exists
->
classification remains stable
->
classification boundaries are consistent
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO by giving temporal topology a boundary map.

It shows that collapse topology is not a narrative label.

It is determined by measurable temporal structure:

```text
run count
run length
local confirmation
global persistence
reset count
```

---

## Relation To TDelta

This experiment clarifies future TDelta work.

A future TDelta cannot be assigned from collapse presence alone.

It must first know which temporal topology exists.

A spike, oscillation, fragment, relapse, and global collapse require different timing interpretations.

---

## What This Confirms

This experiment supports:

```text
clean/pass boundary
spike/local boundary
local/global boundary
oscillation/fragmentation boundary
fragmentation/recovery-relapse boundary
global/recovery-relapse boundary
exact global threshold behavior
dense oscillation/dense fragmentation separation
multi-signal threshold classification
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal topology thresholds
real-world temporal reliability
semantic correctness
causal correctness
optimal confirmation window
optimal persistence window
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates controlled synthetic boundary cases.

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
threshold boundaries between temporal collapse topology classes
```

---

## Limitations

```text
Only 16 boundary cases were tested.

Confirmation window is fixed at 2.

Persistence window is fixed at 2.

Global persistence threshold is fixed at 4.

Boundary cases are synthetic.

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
Level 2 — Temporal Topology Boundary Map
```

Reason:

```text
16 boundary cases tested

16 / 16 cases passed

8 / 8 boundary families had pass_rate = 1.0

exact threshold max_run = 3 vs 4 was validated

dense oscillation remained separate from dense fragmentation

fragmented local collapse remained separate from recovery-relapse

single global collapse remained separate from relapse global collapse
```

This is a successful controlled threshold-boundary experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_window_sensitivity_v0.py
```

Purpose:

```text
test whether topology boundaries remain stable
when confirmation_window and persistence_window vary
```

Main question:

```text
does the topology boundary map remain coherent
under temporal-window perturbation?
```

Required perturbations:

```text
confirmation_window = 2, 3, 4

persistence_window = 2, 3, 4

global_persistence_threshold =
confirmation_window + persistence_window
```

Required checks:

```text
local/global boundary shifts predictably

spike/local boundary shifts predictably

fragmentation classification remains coherent

oscillation remains nonpersistent

recovery-relapse remains distinct from global persistence
```

Expected output:

```text
window-sensitive boundary map
class-wise stability under window perturbation
threshold shift accuracy
```

---

## Final Result

```text
PASS — topology threshold boundaries remained consistent across tested boundary cases.
```

Correct final conclusion:

```text
the transition boundaries between temporal collapse topology classes are structurally consistent under the tested threshold cases.
```