# Temporal Collapse Topology Target Reachability v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Post-Reduction Target-Class Law
```

---

## Purpose

This experiment separates the depth law from the target-class law.

The previous experiment confirmed the depth law:

```text
minimum_target_depth =
sum(max(0, run_length - (confirmation_window - 1)))
```

but exposed that the final target class is not always:

```text
OSCILLATING_NONPERSISTENT
```

The reason was structural:

```text
a single remaining sub-threshold run becomes SPIKE_FILTERED
```

not:

```text
OSCILLATING_NONPERSISTENT
```

This experiment asks:

```text
after reducing all confirmed runs below threshold,
which class is actually reached?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates post-reduction target-class reachability under the temporal topology classifier.

---

## Experiment File

```text
examples/temporal_collapse_topology_target_reachability_v0.py
```

Result file:

```text
results/temporal_collapse_topology_target_reachability_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_target_reachability_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

variant_count = 20
flat_record_count = 60
node_count = 6

confirmation_windows = [2, 3, 4]
persistence_window = 2

target_class_values =
[CLEAN_PASS, OSCILLATING_NONPERSISTENT, SPIKE_FILTERED]

remaining_run_count_values =
[0, 1, 2, 3, 4]

prediction_match_rate = 1.0

target_reachability_rule_holds = True

post_reduction_target_class_law_detected = True

depth_law =
minimum_target_depth = sum(max(0, run_length - (confirmation_window - 1)))

target_class_law =
0 remaining runs -> CLEAN_PASS;
1 remaining run -> SPIKE_FILTERED;
2+ remaining runs -> OSCILLATING_NONPERSISTENT

method = post_reduction_target_class_law
```

The experiment passed.

The post-reduction target-class law was detected with zero failures.

---

## Main Finding

The experiment confirms that there are two separate laws:

```text
depth law != target-class law
```

The depth law is:

```text
minimum_target_depth =
sum(max(0, run_length - (confirmation_window - 1)))
```

The target-class law is:

```text
0 remaining runs -> CLEAN_PASS

1 remaining run -> SPIKE_FILTERED

2+ remaining runs -> OSCILLATING_NONPERSISTENT
```

Measured result:

```text
prediction_match_rate = 1.0
failure_count = 0
```

So the final target class is not determined by depth alone.

It is determined by:

```text
remaining_run_count
```

after threshold reduction.

---

## Depth Law

For each collapse run of length `L` and confirmation window `C`:

```text
required edits = max(0, L - (C - 1))
```

Full law:

```text
minimum_target_depth =
sum(max(0, run_length - (confirmation_window - 1)))
```

This measures how much collapse mass must be removed to push every run below confirmation.

---

## Target-Class Law

After reduction, the remaining runs are all below the confirmation threshold.

The final class depends on the number of remaining runs:

```text
remaining_run_count = 0
-> CLEAN_PASS

remaining_run_count = 1
-> SPIKE_FILTERED

remaining_run_count >= 2
-> OSCILLATING_NONPERSISTENT
```

This law explains the boundary exposed in Threshold Sensitivity v0.

---

## By Remaining Run Count

### remaining_run_count = 0

```text
records = 3
observed_classes = [CLEAN_PASS]
stable = True
```

Interpretation:

```text
no remaining collapse run produces CLEAN_PASS
```

---

### remaining_run_count = 1

```text
records = 15
observed_classes = [SPIKE_FILTERED]
stable = True
```

Interpretation:

```text
one remaining sub-threshold run produces SPIKE_FILTERED
```

This explains why `long_single_run` did not reach `OSCILLATING_NONPERSISTENT` in the previous experiment.

---

### remaining_run_count = 2

```text
records = 12
observed_classes = [OSCILLATING_NONPERSISTENT]
stable = True
```

Interpretation:

```text
two remaining sub-threshold runs produce OSCILLATING_NONPERSISTENT
```

---

### remaining_run_count = 3

```text
records = 12
observed_classes = [OSCILLATING_NONPERSISTENT]
stable = True
```

Interpretation:

```text
three remaining sub-threshold runs produce OSCILLATING_NONPERSISTENT
```

---

### remaining_run_count = 4

```text
records = 18
observed_classes = [OSCILLATING_NONPERSISTENT]
stable = True
```

Interpretation:

```text
four remaining sub-threshold runs produce OSCILLATING_NONPERSISTENT
```

---

## By Target Class

### CLEAN_PASS

```text
records = 3
remaining_counts = [0]
depth_values = [0]
```

`CLEAN_PASS` appears only when there are no remaining runs.

---

### SPIKE_FILTERED

```text
records = 15
remaining_counts = [1]

depth_values =
[0, 1, 2, 3, 4, 5, 6]
```

`SPIKE_FILTERED` appears only when there is exactly one remaining run.

Its depth can vary because the original single run may have different length and different threshold.

---

### OSCILLATING_NONPERSISTENT

```text
records = 42
remaining_counts = [2, 3, 4]

depth_values =
[0, 1, 2, 3, 4, 5, 6, 8, 9, 10]
```

`OSCILLATING_NONPERSISTENT` appears when there are at least two remaining runs.

Its depth can vary because the reducible mass can vary.

---

## By Threshold

### CONFIRMATION_WINDOW = 2

```text
class_counts =
{
  CLEAN_PASS: 1,
  SPIKE_FILTERED: 5,
  OSCILLATING_NONPERSISTENT: 14
}

prediction_match_rate = 1.0

remaining_counts =
[0, 1, 2, 3, 4]
```

---

### CONFIRMATION_WINDOW = 3

```text
class_counts =
{
  CLEAN_PASS: 1,
  SPIKE_FILTERED: 5,
  OSCILLATING_NONPERSISTENT: 14
}

prediction_match_rate = 1.0

remaining_counts =
[0, 1, 2, 3, 4]
```

---

### CONFIRMATION_WINDOW = 4

```text
class_counts =
{
  CLEAN_PASS: 1,
  SPIKE_FILTERED: 5,
  OSCILLATING_NONPERSISTENT: 14
}

prediction_match_rate = 1.0

remaining_counts =
[0, 1, 2, 3, 4]
```

The target-class law remained stable across all tested confirmation windows.

---

## Geometry Records

### Variant 0 — zero_run_clean

```text
runs = []

C=2 -> depth=0, remaining=0, target=CLEAN_PASS
C=3 -> depth=0, remaining=0, target=CLEAN_PASS
C=4 -> depth=0, remaining=0, target=CLEAN_PASS
```

Interpretation:

```text
zero runs always produce CLEAN_PASS
```

---

### Variant 1 — single_spike_len_1

```text
runs = [1]

C=2 -> depth=0, remaining=1, target=SPIKE_FILTERED
C=3 -> depth=0, remaining=1, target=SPIKE_FILTERED
C=4 -> depth=0, remaining=1, target=SPIKE_FILTERED
```

Interpretation:

```text
one sub-threshold run produces SPIKE_FILTERED
```

---

### Variant 2 — single_run_len_2

```text
runs = [2]

C=2 -> depth=1, remaining=1, target=SPIKE_FILTERED
C=3 -> depth=0, remaining=1, target=SPIKE_FILTERED
C=4 -> depth=0, remaining=1, target=SPIKE_FILTERED
```

Interpretation:

```text
single-run geometries remain SPIKE_FILTERED after threshold reduction
```

---

### Variant 3 — single_run_len_3

```text
runs = [3]

C=2 -> depth=2, remaining=1, target=SPIKE_FILTERED
C=3 -> depth=1, remaining=1, target=SPIKE_FILTERED
C=4 -> depth=0, remaining=1, target=SPIKE_FILTERED
```

---

### Variant 4 — single_run_len_4

```text
runs = [4]

C=2 -> depth=3, remaining=1, target=SPIKE_FILTERED
C=3 -> depth=2, remaining=1, target=SPIKE_FILTERED
C=4 -> depth=1, remaining=1, target=SPIKE_FILTERED
```

---

### Variant 5 — single_run_len_7

```text
runs = [7]

C=2 -> depth=6, remaining=1, target=SPIKE_FILTERED
C=3 -> depth=5, remaining=1, target=SPIKE_FILTERED
C=4 -> depth=4, remaining=1, target=SPIKE_FILTERED
```

Interpretation:

```text
a long single run may require high depth,
but the post-reduction target is still SPIKE_FILTERED
```

Depth and target class are separate.

---

### Variant 6 — two_spikes_len_1_1

```text
runs = [1, 1]

C=2 -> depth=0, remaining=2, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=0, remaining=2, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=0, remaining=2, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 7 — two_runs_len_2_2

```text
runs = [2, 2]

C=2 -> depth=2, remaining=2, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=0, remaining=2, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=0, remaining=2, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 8 — two_runs_len_3_3

```text
runs = [3, 3]

C=2 -> depth=4, remaining=2, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=2, remaining=2, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=0, remaining=2, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 9 — two_runs_len_5_5

```text
runs = [5, 5]

C=2 -> depth=8, remaining=2, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=6, remaining=2, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=4, remaining=2, target=OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
two-run geometries always reduce to OSCILLATING_NONPERSISTENT
```

---

### Variant 10 — three_spikes_len_1_1_1

```text
runs = [1, 1, 1]

C=2 -> depth=0, remaining=3, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=0, remaining=3, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=0, remaining=3, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 11 — three_runs_len_2_2_2

```text
runs = [2, 2, 2]

C=2 -> depth=3, remaining=3, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=0, remaining=3, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=0, remaining=3, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 12 — three_runs_len_3_3_3

```text
runs = [3, 3, 3]

C=2 -> depth=6, remaining=3, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=3, remaining=3, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=0, remaining=3, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 13 — three_runs_len_4_4_4

```text
runs = [4, 4, 4]

C=2 -> depth=9, remaining=3, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=6, remaining=3, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=3, remaining=3, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 14 — four_spikes_len_1_1_1_1

```text
runs = [1, 1, 1, 1]

C=2 -> depth=0, remaining=4, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=0, remaining=4, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=0, remaining=4, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 15 — four_runs_len_2_2_2_2

```text
runs = [2, 2, 2, 2]

C=2 -> depth=4, remaining=4, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=0, remaining=4, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=0, remaining=4, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 16 — mixed_1_2_3_4

```text
runs = [1, 2, 3, 4]

C=2 -> depth=6, remaining=4, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=3, remaining=4, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=1, remaining=4, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 17 — mixed_2_3_4_5

```text
runs = [2, 3, 4, 5]

C=2 -> depth=10, remaining=4, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=6, remaining=4, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=3, remaining=4, target=OSCILLATING_NONPERSISTENT
```

---

### Variant 18 — mixed_single_confirmed_plus_spikes

```text
runs = [1, 1, 4, 1]

C=2 -> depth=3, remaining=4, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=2, remaining=4, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=1, remaining=4, target=OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
even one confirmed run can reduce to OSCILLATING_NONPERSISTENT
if other spike runs remain present
```

This matters.

The target class depends on total remaining run count, not only confirmed-run count.

---

### Variant 19 — mixed_two_confirmed_plus_spikes

```text
runs = [1, 3, 1, 4]

C=2 -> depth=5, remaining=4, target=OSCILLATING_NONPERSISTENT
C=3 -> depth=3, remaining=4, target=OSCILLATING_NONPERSISTENT
C=4 -> depth=1, remaining=4, target=OSCILLATING_NONPERSISTENT
```

---

## Rule Validation

```text
target_reachability_rule_holds = True
failure_count = 0
prediction_match_rate = 1.0
```

No failures were found.

The target-class law matched every tested case.

---

## Structural Meaning

The temporal topology now separates into two independent layers.

### Layer 1 — Depth Law

```text
How many edits are needed to reduce all confirmed runs below threshold?
```

Answer:

```text
minimum_target_depth =
sum(max(0, run_length - (confirmation_window - 1)))
```

### Layer 2 — Target-Class Law

```text
After reduction, which target class is reached?
```

Answer:

```text
0 remaining runs -> CLEAN_PASS
1 remaining run -> SPIKE_FILTERED
2+ remaining runs -> OSCILLATING_NONPERSISTENT
```

This solves the boundary exposed by Threshold Sensitivity v0.

---

## Relation To Threshold Sensitivity v0

Threshold Sensitivity v0 returned:

```text
CHECK
```

because the depth formula held, but the target class was not always:

```text
OSCILLATING_NONPERSISTENT
```

Target Reachability v0 explains why:

```text
single-run post-reduction cases become SPIKE_FILTERED
```

So Threshold Sensitivity v0 was not a formula failure.

It exposed a missing target-class law.

---

## Relation To Variable Run Length v0

Variable Run Length v0 established:

```text
target depth depends on reducible collapse mass
```

Target Reachability v0 adds:

```text
target class depends on remaining run count
```

Together:

```text
reducible mass -> depth

remaining run count -> target class
```

---

## Relation To OMNIATEMPO

This result strengthens OMNIATEMPO by separating:

```text
transition cost
```

from:

```text
transition destination
```

OMNIATEMPO can now represent:

```text
confirmation window
thresholded reducible mass
minimum target depth
remaining run count
post-reduction class
```

This turns temporal collapse topology into a more precise structural transition system.

---

## Relation To TDelta

This result supports two `TDelta`-style quantities:

```text
TΔ_depth(C) =
sum(max(0, run_length - (C - 1)))
```

and:

```text
TΔ_target_class =
class(remaining_run_count)
```

where:

```text
C = confirmation_window
```

and:

```text
class(0)  = CLEAN_PASS
class(1)  = SPIKE_FILTERED
class(>=2) = OSCILLATING_NONPERSISTENT
```

This separates transition distance from destination class.

---

## What This Confirms

This experiment supports:

```text
post-reduction target-class law detected

prediction_match_rate = 1.0

target_reachability_rule_holds = True

failure_count = 0

remaining_run_count = 0 maps to CLEAN_PASS

remaining_run_count = 1 maps to SPIKE_FILTERED

remaining_run_count >= 2 maps to OSCILLATING_NONPERSISTENT

depth law and target-class law are separable
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal temporal target law
real-world temporal dynamics
semantic correctness
causal correctness
optimal confirmation thresholds
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates a controlled post-reduction target-class law inside the tested classifier family.

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
post-reduction target-class reachability
under temporal collapse-run geometry
```

---

## Limitations

```text
This is an analytical target-class test.

The result depends on the current classifier rules.

Only confirmation windows 2, 3, and 4 were tested.

Persistence window was fixed at 2.

Only synthetic trajectories were tested.

Only three frame values were used:
PASS
ESCALATE
COLLAPSE

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

The target-class law should be re-tested if the classifier changes.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Post-Reduction Target-Class Law
```

Reason:

```text
variant_count = 20

flat_record_count = 60

prediction_match_rate = 1.0

target_reachability_rule_holds = True

post_reduction_target_class_law_detected = True

failure_count = 0
```

This is a successful controlled target-reachability law experiment.

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

Temporal Collapse Topology Noise Robustness v0
-> minimal controlled noise exposes topology instability

Temporal Collapse Topology Phase Transition v0
-> topology stability index and transition distance become measurable

Temporal Collapse Topology Transition Graph v0
-> directed mutation graph between temporal topology classes becomes measurable

Temporal Collapse Topology Transition Graph Stability v0
-> transition graph structure remains stable across shifted trajectory variants

Temporal Collapse Topology Attractor v0
-> attractor and basin structure is detected inside the temporal topology graph

Temporal Collapse Topology Attractor Stability v0
-> attractor and basin identities remain stable, while bridge identity is perturbation-sensitive

Temporal Collapse Topology Bridge Stability v0
-> expected multi-bridge hypothesis is falsified; stable single dominant bridge emerges

Temporal Collapse Topology Basin Entry v0
-> FRAGMENTED_LOCAL_COLLAPSE is confirmed as dominant basin-entry state

Temporal Collapse Topology Basin Entry Stability v0
-> basin-entry invariance is detected under widened variants and mutation depth 3

Temporal Collapse Topology Basin Escape v0
-> basin-entry state is reversible while deeper collapse states remained absorbing under tested mutations

Temporal Collapse Topology Absorption Depth v0
-> all collapse-side states become reversible under depth 4, revealing escape-depth stratification

Temporal Collapse Topology Escape Depth Stability v0
-> escape-depth ordering stability is detected across widened variants

Temporal Collapse Topology Reversibility Index v0
-> collapse-basin reversibility ranking is detected

Temporal Collapse Topology Boundary Cycle v0
-> stable asymmetric boundary cycle detected between OSCILLATING_NONPERSISTENT and FRAGMENTED_LOCAL_COLLAPSE

Temporal Collapse Topology Boundary Cycle Stability v0
-> boundary-cycle existence remains stable, but reverse escape depth is geometry-sensitive

Temporal Collapse Topology Geometry Sensitivity v0
-> collapse_run_count controls reverse escape depth under fixed run-length geometries

Temporal Collapse Topology Variable Run Length v0
-> variable run lengths refine the control factor to reducible collapse mass

Temporal Collapse Topology Threshold Sensitivity v0
-> thresholded reducible-mass rule confirmed, but target reachability depends on run count

Temporal Collapse Topology Target Reachability v0
-> post-reduction target-class law detected
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_transition_cost_destination_v0.py
```

Purpose:

```text
combine depth law and target-class law into one transition model
```

Main question:

```text
can temporal topology transitions be represented as:
transition_cost + destination_class?
```

Required checks:

```text
source class
confirmation window
run lengths
minimum transition cost
remaining run count
destination class
transition signature
cost-destination consistency
```

Expected structural value:

```text
transition cost / destination decomposition
```

---

## Final Result

```text
PASS — post-reduction target-class law detected.
```

Correct final conclusion:

```text
depth law and target-class law are separable:
depth depends on thresholded reducible mass,
while target class depends on remaining_run_count.
```