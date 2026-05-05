# Temporal Collapse Topology Stability v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Collapse Taxonomy Stability
```

---

## Purpose

This experiment tests whether temporal collapse topology classification remains stable under controlled trajectory perturbations.

The previous experiment established six temporal topology classes:

```text
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
CLEAN_PASS
```

This experiment asks whether those classes remain invariant when trajectory parameters change.

Core question:

```text
does the temporal collapse taxonomy remain stable
under perturbations of length, collapse position, gap size, and fragmentation density?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates structural invariance of temporal collapse classification.

---

## Experiment File

```text
examples/temporal_collapse_topology_stability_v0.py
```

Result file:

```text
results/temporal_collapse_topology_stability_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_stability_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

case_count = 39

pass_case_count = 39
check_case_count = 0
pass_rate = 1.0

confirmation_window = 2
persistence_window = 2
reset_window = 2

mean_fragmentation_index = 0.3212641025641026
max_fragmentation_index = 0.8889

mean_max_temporal_collapse_run_length = 5.153846153846154
mean_local_confirmation_count = 1.2307692307692308
```

The experiment passed.

All 39 perturbed cases were classified correctly.

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

All supported classes remained stable under the tested perturbations.

---

## Main Finding

The central result is:

```text
pass_rate = 1.0
```

and:

```text
39 / 39 cases passed
```

This means the temporal collapse taxonomy remained invariant under controlled perturbations.

The classifier did not collapse one topology into another.

---

## Structural Meaning

The previous experiment showed that the taxonomy can classify fixed examples.

This experiment shows that the taxonomy is stable across parameter variation.

That is the important OMNIA-style step:

```text
classification
->
invariance under transformation
```

This supports the principle:

```text
structural truth = invariance under transformation
```

Inside this controlled setup, the taxonomy behaves as a stable structural classifier.

---

## Perturbations Tested

The experiment varied:

```text
trajectory length
spike position
collapse start position
recovery gap length
fragmentation gap length
oscillation gap length
```

Tested trajectory lengths:

```text
12
16
20
```

Recovery gaps tested:

```text
2
3
4
```

Fragmentation gaps tested:

```text
1
2
3
```

Oscillation gaps tested:

```text
1
2
3
```

---

## Family Summary

### clean_pass

```text
case_count = 3
pass_count = 3
check_count = 0
pass_rate = 1.0
```

Interpretation:

```text
clean trajectories remained clean
```

No collapse was falsely introduced by length variation.

---

### spike_filtered

```text
case_count = 9
pass_count = 9
check_count = 0
pass_rate = 1.0
```

Interpretation:

```text
single-frame spikes remained SPIKE_FILTERED
```

Spike position did not change the classification.

---

### global_persistent_collapse

```text
case_count = 9
pass_count = 9
check_count = 0
pass_rate = 1.0
```

Interpretation:

```text
global persistence remained stable
```

Changing trajectory length and collapse start position did not break the global persistent class.

---

### recovery_relapse_collapse

```text
case_count = 6
pass_count = 6
check_count = 0
pass_rate = 1.0
```

Interpretation:

```text
recovery-relapse topology remained stable
```

Recovery gap length did not collapse this class into fragmented or global persistence.

---

### fragmented_local_collapse

```text
case_count = 6
pass_count = 6
check_count = 0
pass_rate = 1.0
```

Interpretation:

```text
fragmented local collapse remained stable
```

Fragmentation density changed, but the class stayed invariant.

---

### oscillating_nonpersistent

```text
case_count = 6
pass_count = 6
check_count = 0
pass_rate = 1.0
```

Interpretation:

```text
oscillation remained nonpersistent
```

Changing oscillation gap frequency did not falsely promote oscillation into fragmentation or persistence.

---

## Topology Metrics

### Fragmentation Index

```text
mean_fragmentation_index = 0.3212641025641026
max_fragmentation_index = 0.8889
```

The maximum value appeared in dense oscillation.

This shows that fragmentation index alone is not enough to classify topology.

It must be interpreted together with:

```text
max_temporal_collapse_run_length
local_confirmation_count
global_persistence_detected
collapse_run_count
```

---

### Maximum Collapse Run Length

```text
mean_max_temporal_collapse_run_length = 5.153846153846154
```

This metric separates single-frame oscillations and spikes from local fragments and global persistence.

---

### Local Confirmation Count

```text
mean_local_confirmation_count = 1.2307692307692308
```

This metric helps separate:

```text
OSCILLATING_NONPERSISTENT
```

from:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

Oscillation has collapse events, but no local confirmations.

Fragmentation has local confirmations, but no global persistence.

---

## Important Boundary

The experiment confirms that high fragmentation index alone does not imply fragmented local collapse.

For example:

```text
oscillating_nonpersistent_L20_gap1
fragmentation_index = 0.8889
```

But it remains:

```text
OSCILLATING_NONPERSISTENT
```

because:

```text
max_run = 1
local_confirmation_count = 0
global_persistence_detected = False
```

Therefore topology classification must be multi-signal.

---

## Case-Level Interpretation

The experiment confirms:

```text
CLEAN_PASS remains stable under length change

SPIKE_FILTERED remains stable under spike position change

GLOBAL_PERSISTENT_COLLAPSE remains stable under start-position and length change

RECOVERY_RELAPSE_COLLAPSE remains stable under recovery-gap variation

FRAGMENTED_LOCAL_COLLAPSE remains stable under fragmentation-density variation

OSCILLATING_NONPERSISTENT remains stable under oscillation-frequency variation
```

No tested perturbation caused a topology class to collapse into another.

---

## Main Structural Result

The core result is:

```text
temporal collapse topology classification
remained stable under controlled trajectory perturbations
```

This moves the work from:

```text
taxonomy definition
```

to:

```text
taxonomy invariance
```

That is a stronger result than classification alone.

---

## Relation To Fragmentation Classification v0

Fragmentation Classification v0 showed that six topology classes could be separated.

Topology Stability v0 shows that those classes remain stable when the input trajectories are perturbed.

So the sequence is:

```text
classification exists
->
classification remains invariant
```

---

## Relation To Regime Reset v0

Regime Reset v0 exposed the unresolved fragmented persistence boundary.

Fragmentation Classification v0 named that boundary.

Topology Stability v0 tests whether the naming remains stable across variations.

This confirms that the previous CHECK was not a defect.

It was a missing topology class.

---

## Relation To OMNIATEMPO

This experiment supports OMNIATEMPO because it treats time as structure.

It does not merely ask:

```text
did collapse occur?
```

It asks:

```text
what temporal shape did collapse take?
```

And then:

```text
does that shape remain invariant under perturbation?
```

That is the core of temporal structural measurement.

---

## Relation To TDelta

This experiment supports future TDelta measurement.

A single divergence time is not enough.

Temporal divergence may appear as:

```text
spike
oscillation
fragmentation
recovery-relapse
global persistence
```

Stable topology classification is required before assigning precise temporal divergence indices.

---

## What This Confirms

This experiment supports:

```text
taxonomy stability
classification invariance
clean pass stability
spike filtering stability
global persistence stability
recovery-relapse stability
fragmented local collapse stability
oscillation nonpersistence stability
multi-signal topology classification
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal taxonomy validity
real-world temporal reliability
semantic correctness
causal correctness
optimal thresholds
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates controlled synthetic topology stability.

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
stability of temporal collapse topology classification
under controlled perturbations
```

---

## Limitations

```text
Only 39 synthetic cases were tested.

Trajectory lengths were limited to 12, 16, and 20.

Confirmation window was fixed at 2.

Persistence window was fixed at 2.

Reset window was fixed at 2.

Perturbations were controlled and hand-generated.

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
Level 2 — Temporal Collapse Taxonomy Stability
```

Reason:

```text
39 cases tested

39 / 39 cases passed

6 / 6 families had pass_rate = 1.0

taxonomy remained stable under controlled perturbations

no class collapsed into another class

fragmented local collapse remained distinct from oscillation and global persistence
```

This is a successful controlled topology stability experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_threshold_boundary_v0.py
```

Purpose:

```text
test boundary cases between topology classes
```

Main question:

```text
where are the classification boundaries
between oscillation, fragmentation, recovery-relapse, and global persistence?
```

Required boundary tests:

```text
max_run = 1 versus max_run = 2

local_confirmation_count = 0 versus 1

fragmentation_index high with no local confirmation

fragmentation_index high with local confirmation

global_persistence_detected false versus true

single long run versus multiple short runs

recovery-relapse versus fragmented local collapse
```

Expected output:

```text
boundary map between topology classes
```

---

## Final Result

```text
PASS — temporal collapse topology classification remained stable under trajectory perturbations.
```

Correct final conclusion:

```text
the temporal collapse taxonomy remained invariant under controlled perturbations,
supporting it as a stable structural classification layer.
```