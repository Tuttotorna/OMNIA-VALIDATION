# Temporal Collapse Topology Transition Cost Destination v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Transition Cost / Destination Decomposition
```

---

## Purpose

This experiment combines two previously separated laws into one transition model.

Previous results established:

```text
depth law != target-class law
```

The depth law:

```text
transition_cost =
sum(max(0, run_length - (confirmation_window - 1)))
```

The destination law:

```text
0 remaining runs -> CLEAN_PASS

1 remaining run -> SPIKE_FILTERED

2+ remaining runs -> OSCILLATING_NONPERSISTENT
```

This experiment asks:

```text
can temporal topology transitions be represented as:
transition_cost + destination_class?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates transition decomposition under the temporal collapse topology classifier.

---

## Experiment File

```text
examples/temporal_collapse_topology_transition_cost_destination_v0.py
```

Result file:

```text
results/temporal_collapse_topology_transition_cost_destination_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_transition_cost_destination_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

variant_count = 24
flat_record_count = 72
node_count = 6

confirmation_windows = [2, 3, 4]
persistence_window = 2

source_class_values =
[
  CLEAN_PASS,
  FRAGMENTED_LOCAL_COLLAPSE,
  GLOBAL_PERSISTENT_COLLAPSE,
  OSCILLATING_NONPERSISTENT,
  RECOVERY_RELAPSE_COLLAPSE,
  SPIKE_FILTERED
]

destination_class_values =
[
  CLEAN_PASS,
  OSCILLATING_NONPERSISTENT,
  SPIKE_FILTERED
]

transition_cost_values =
[0, 1, 2, 3, 4, 5, 6, 8, 9, 10]

cost_destination_consistency_rate = 1.0

transition_model_holds = True

transition_cost_destination_decomposition_detected = True

unique_transition_signature_count = 54
```

The experiment passed.

The transition model held with zero failures.

---

## Main Finding

Temporal topology transitions decompose into:

```text
thresholded reducible mass
+
post-reduction destination class
```

Formal transition model:

```text
transition =
thresholded_reducible_mass_cost
+
post_reduction_destination_class
```

Cost rule:

```text
transition_cost =
sum(max(0, run_length - (confirmation_window - 1)))
```

Destination rule:

```text
0 remaining runs -> CLEAN_PASS

1 remaining run -> SPIKE_FILTERED

2+ remaining runs -> OSCILLATING_NONPERSISTENT
```

Validation:

```text
cost_destination_consistency_rate = 1.0
transition_model_holds = True
failure_count = 0
```

---

## Structural Meaning

This result separates two things that are often confused:

```text
how far a topology is from a post-reduction state
```

and:

```text
which state is reached after reduction
```

The first is the transition cost.

The second is the destination class.

So the transition is not just:

```text
source -> destination
```

It is:

```text
source -- cost / threshold / remaining structure --> destination
```

This gives a stronger structural representation than a simple class transition graph.

---

## Transition Model

For a given run structure:

```text
run_lengths = [L1, L2, ..., Ln]
```

and a confirmation window:

```text
C = confirmation_window
```

the transition cost is:

```text
transition_cost =
sum(max(0, Li - (C - 1)))
```

The post-reduction run lengths are:

```text
remaining_run_lengths =
[min(Li, C - 1) for each Li, if min(Li, C - 1) > 0]
```

The remaining run count is:

```text
remaining_run_count = len(remaining_run_lengths)
```

Then:

```text
remaining_run_count = 0 -> CLEAN_PASS
remaining_run_count = 1 -> SPIKE_FILTERED
remaining_run_count >= 2 -> OSCILLATING_NONPERSISTENT
```

---

## By Threshold

### CONFIRMATION_WINDOW = 2

```text
source_class_counts =
{
  CLEAN_PASS: 1,
  SPIKE_FILTERED: 1,
  FRAGMENTED_LOCAL_COLLAPSE: 8,
  GLOBAL_PERSISTENT_COLLAPSE: 2,
  OSCILLATING_NONPERSISTENT: 3,
  RECOVERY_RELAPSE_COLLAPSE: 9
}

destination_class_counts =
{
  CLEAN_PASS: 1,
  SPIKE_FILTERED: 5,
  OSCILLATING_NONPERSISTENT: 18
}

transition_cost_values =
[0, 1, 2, 3, 4, 5, 6, 8, 9, 10]

cost_destination_consistency_rate = 1.0
```

At the strictest threshold, more sources are classified as collapse-side states.

The destination distribution remains structurally consistent.

---

### CONFIRMATION_WINDOW = 3

```text
source_class_counts =
{
  CLEAN_PASS: 1,
  SPIKE_FILTERED: 2,
  FRAGMENTED_LOCAL_COLLAPSE: 8,
  GLOBAL_PERSISTENT_COLLAPSE: 1,
  OSCILLATING_NONPERSISTENT: 7,
  RECOVERY_RELAPSE_COLLAPSE: 5
}

destination_class_counts =
{
  CLEAN_PASS: 1,
  SPIKE_FILTERED: 5,
  OSCILLATING_NONPERSISTENT: 18
}

transition_cost_values =
[0, 1, 2, 3, 4, 5, 6]

cost_destination_consistency_rate = 1.0
```

As the confirmation threshold increases, some source classes soften from collapse-side states into noise-side states.

The cost range narrows.

---

### CONFIRMATION_WINDOW = 4

```text
source_class_counts =
{
  CLEAN_PASS: 1,
  SPIKE_FILTERED: 3,
  FRAGMENTED_LOCAL_COLLAPSE: 9,
  GLOBAL_PERSISTENT_COLLAPSE: 1,
  OSCILLATING_NONPERSISTENT: 9,
  RECOVERY_RELAPSE_COLLAPSE: 1
}

destination_class_counts =
{
  CLEAN_PASS: 1,
  SPIKE_FILTERED: 5,
  OSCILLATING_NONPERSISTENT: 18
}

transition_cost_values =
[0, 1, 3, 4]

cost_destination_consistency_rate = 1.0
```

At the largest tested threshold, fewer trajectories require large transition cost.

The destination rule remains unchanged.

---

## By Destination

### CLEAN_PASS

```text
records = 3
source_classes = [CLEAN_PASS]
transition_cost_values = [0]
remaining_run_count_values = [0]
```

`CLEAN_PASS` appears only when there are no remaining collapse runs.

---

### SPIKE_FILTERED

```text
records = 15

source_classes =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  GLOBAL_PERSISTENT_COLLAPSE,
  SPIKE_FILTERED
]

transition_cost_values =
[0, 1, 2, 3, 4, 5, 6]

remaining_run_count_values =
[1]
```

`SPIKE_FILTERED` appears only when exactly one run remains after reduction.

It can be reached from multiple source classes because source class depends on threshold and original run length.

---

### OSCILLATING_NONPERSISTENT

```text
records = 54

source_classes =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  OSCILLATING_NONPERSISTENT,
  RECOVERY_RELAPSE_COLLAPSE
]

transition_cost_values =
[0, 1, 2, 3, 4, 5, 6, 8, 9, 10]

remaining_run_count_values =
[2, 3, 4, 5, 6]
```

`OSCILLATING_NONPERSISTENT` appears whenever at least two runs remain after reduction.

It can be reached with zero cost or high cost, depending on whether the source was already below threshold.

---

## By Source → Destination

### CLEAN_PASS -> CLEAN_PASS

```text
records = 3
costs = [0]
remaining_counts = [0]
```

No collapse structure is present.

---

### SPIKE_FILTERED -> SPIKE_FILTERED

```text
records = 6
costs = [0]
remaining_counts = [1]
```

Single-run spike structure remains single-run spike structure.

---

### FRAGMENTED_LOCAL_COLLAPSE -> SPIKE_FILTERED

```text
records = 5
costs = [1, 2]
remaining_counts = [1]
```

A single confirmed fragmented run reduces into one sub-threshold run.

Destination:

```text
SPIKE_FILTERED
```

---

### GLOBAL_PERSISTENT_COLLAPSE -> SPIKE_FILTERED

```text
records = 4
costs = [3, 4, 5, 6]
remaining_counts = [1]
```

A single long persistent run reduces into one sub-threshold run.

Destination:

```text
SPIKE_FILTERED
```

This confirms that high transition cost does not imply `OSCILLATING_NONPERSISTENT`.

Destination depends on remaining run count.

---

### OSCILLATING_NONPERSISTENT -> OSCILLATING_NONPERSISTENT

```text
records = 19
costs = [0]
remaining_counts = [2, 3, 4, 6]
```

Already sub-threshold multi-run structures stay `OSCILLATING_NONPERSISTENT`.

---

### FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT

```text
records = 20
costs = [1, 2, 3, 4, 6]
remaining_counts = [2, 3, 4, 5, 6]
```

Fragmented collapse with multiple remaining runs reduces into `OSCILLATING_NONPERSISTENT`.

---

### RECOVERY_RELAPSE_COLLAPSE -> OSCILLATING_NONPERSISTENT

```text
records = 15
costs = [3, 4, 5, 6, 8, 9, 10]
remaining_counts = [2, 3, 4, 5]
```

Relapse-style collapse can reduce into `OSCILLATING_NONPERSISTENT` when more than one run remains.

---

## Geometry Records

### Variant 0 — zero_run_clean

```text
runs = []

C=2 -> source=CLEAN_PASS, cost=0, remaining=0, dest=CLEAN_PASS
C=3 -> source=CLEAN_PASS, cost=0, remaining=0, dest=CLEAN_PASS
C=4 -> source=CLEAN_PASS, cost=0, remaining=0, dest=CLEAN_PASS
```

---

### Variant 1 — single_spike_len_1

```text
runs = [1]

C=2 -> source=SPIKE_FILTERED, cost=0, remaining=1, dest=SPIKE_FILTERED
C=3 -> source=SPIKE_FILTERED, cost=0, remaining=1, dest=SPIKE_FILTERED
C=4 -> source=SPIKE_FILTERED, cost=0, remaining=1, dest=SPIKE_FILTERED
```

---

### Variant 2 — single_run_len_2

```text
runs = [2]

C=2 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=1, remaining=1, dest=SPIKE_FILTERED
C=3 -> source=SPIKE_FILTERED, cost=0, remaining=1, dest=SPIKE_FILTERED
C=4 -> source=SPIKE_FILTERED, cost=0, remaining=1, dest=SPIKE_FILTERED
```

---

### Variant 3 — single_run_len_3

```text
runs = [3]

C=2 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=2, remaining=1, dest=SPIKE_FILTERED
C=3 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=1, remaining=1, dest=SPIKE_FILTERED
C=4 -> source=SPIKE_FILTERED, cost=0, remaining=1, dest=SPIKE_FILTERED
```

---

### Variant 4 — single_run_len_4

```text
runs = [4]

C=2 -> source=GLOBAL_PERSISTENT_COLLAPSE, cost=3, remaining=1, dest=SPIKE_FILTERED
C=3 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=2, remaining=1, dest=SPIKE_FILTERED
C=4 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=1, remaining=1, dest=SPIKE_FILTERED
```

---

### Variant 5 — single_run_len_7

```text
runs = [7]

C=2 -> source=GLOBAL_PERSISTENT_COLLAPSE, cost=6, remaining=1, dest=SPIKE_FILTERED
C=3 -> source=GLOBAL_PERSISTENT_COLLAPSE, cost=5, remaining=1, dest=SPIKE_FILTERED
C=4 -> source=GLOBAL_PERSISTENT_COLLAPSE, cost=4, remaining=1, dest=SPIKE_FILTERED
```

Important point:

```text
single-run collapse can have high cost
but still reduce to SPIKE_FILTERED
```

So destination is not determined by cost.

---

### Variant 6 — two_spikes_len_1_1

```text
runs = [1, 1]

C=2 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=2, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 7 — two_runs_len_2_2

```text
runs = [2, 2]

C=2 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=2, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=2, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 8 — two_runs_len_3_3

```text
runs = [3, 3]

C=2 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=4, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=2, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=2, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 9 — two_runs_len_5_5

```text
runs = [5, 5]

C=2 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=8, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=6, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=4, remaining=2, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 10 — three_spikes_len_1_1_1

```text
runs = [1, 1, 1]

C=2 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=3, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=3, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=3, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 11 — three_runs_len_2_2_2

```text
runs = [2, 2, 2]

C=2 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=3, remaining=3, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=3, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=3, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 12 — three_runs_len_3_3_3

```text
runs = [3, 3, 3]

C=2 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=6, remaining=3, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=3, remaining=3, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=3, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 13 — three_runs_len_4_4_4

```text
runs = [4, 4, 4]

C=2 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=9, remaining=3, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=6, remaining=3, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=3, remaining=3, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 14 — four_spikes_len_1_1_1_1

```text
runs = [1, 1, 1, 1]

C=2 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=4, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 15 — four_runs_len_2_2_2_2

```text
runs = [2, 2, 2, 2]

C=2 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=4, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=4, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 16 — mixed_1_2_3_4

```text
runs = [1, 2, 3, 4]

C=2 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=6, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=3, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=1, remaining=4, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 17 — mixed_2_3_4_5

```text
runs = [2, 3, 4, 5]

C=2 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=10, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=6, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=3, remaining=4, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 18 — mixed_single_confirmed_plus_spikes

```text
runs = [1, 1, 4, 1]

C=2 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=3, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=2, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=1, remaining=4, dest=OSCILLATING_NONPERSISTENT
```

Important point:

```text
one confirmed run plus several spike runs reduces to OSCILLATING_NONPERSISTENT
```

because the remaining run count is greater than one.

---

### Variant 19 — mixed_two_confirmed_plus_spikes

```text
runs = [1, 3, 1, 4]

C=2 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=5, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=3, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=1, remaining=4, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 20 — relapse_two_long_runs

```text
runs = [5, 5]

C=2 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=8, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=6, remaining=2, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=4, remaining=2, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 21 — dense_many_short_runs

```text
runs = [2, 2, 1, 2, 1, 2]

C=2 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=4, remaining=6, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=6, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=OSCILLATING_NONPERSISTENT, cost=0, remaining=6, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 22 — sparse_long_then_spikes

```text
runs = [6, 1, 1, 1]

C=2 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=5, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=4, remaining=4, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=3, remaining=4, dest=OSCILLATING_NONPERSISTENT
```

---

### Variant 23 — staircase_1_2_3_4_5

```text
runs = [1, 2, 3, 4, 5]

C=2 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=10, remaining=5, dest=OSCILLATING_NONPERSISTENT
C=3 -> source=RECOVERY_RELAPSE_COLLAPSE, cost=6, remaining=5, dest=OSCILLATING_NONPERSISTENT
C=4 -> source=FRAGMENTED_LOCAL_COLLAPSE, cost=3, remaining=5, dest=OSCILLATING_NONPERSISTENT
```

---

## Rule Validation

```text
transition_model_holds = True
failure_count = 0
failures = []
```

The model made no cost or destination errors across:

```text
24 variants
72 threshold-conditioned records
3 confirmation windows
```

---

## Transition Signatures

The experiment generated:

```text
unique_transition_signature_count = 54
```

A transition signature has the form:

```text
SOURCE_CLASS --C=<confirmation_window>/cost=<transition_cost>/remaining=<remaining_run_count>--> DESTINATION_CLASS
```

Example:

```text
RECOVERY_RELAPSE_COLLAPSE --C=2/cost=10/remaining=4--> OSCILLATING_NONPERSISTENT
```

This is structurally stronger than a plain transition edge because it preserves:

```text
source class
confirmation threshold
transition cost
remaining run count
destination class
```

---

## Structural Meaning

The temporal topology transition graph now has weighted, threshold-parametric edges.

A transition is not merely:

```text
A -> B
```

It is:

```text
A -- cost / threshold / remaining structure --> B
```

This means the topology can measure:

```text
how expensive the transition is
```

and:

```text
where the transition lands
```

as separate but compatible quantities.

---

## Relation To Target Reachability v0

Target Reachability v0 showed:

```text
remaining_run_count determines destination class
```

Transition Cost Destination v0 adds the cost component:

```text
thresholded reducible mass determines transition cost
```

Together:

```text
transition_cost = thresholded reducible mass

destination_class = function(remaining_run_count)
```

---

## Relation To Threshold Sensitivity v0

Threshold Sensitivity v0 returned `CHECK` because the depth formula held but `OSCILLATING_NONPERSISTENT` was not always the destination.

This experiment resolves that boundary.

The correct formulation is not:

```text
all reduced states target OSCILLATING_NONPERSISTENT
```

The correct formulation is:

```text
all reduced states land in the class determined by remaining_run_count
```

---

## Relation To Variable Run Length v0

Variable Run Length v0 showed that run count alone is insufficient.

Transition Cost Destination v0 confirms the refined model:

```text
run lengths determine cost

remaining run count determines destination
```

---

## Relation To Boundary Cycle Stability v0

Boundary Cycle Stability v0 showed geometry-sensitive reverse depth.

This experiment explains the mechanism:

```text
reverse depth varies because thresholded reducible mass varies
```

and:

```text
destination varies according to remaining run count
```

So the boundary cycle can be represented with weighted cost/destination edges.

---

## Relation To OMNIATEMPO

This result strengthens OMNIATEMPO by adding a transition model:

```text
temporal topology state
+ confirmation threshold
+ run-length geometry
-> transition cost
+ destination class
```

This gives OMNIATEMPO a structural transition representation, not only a classifier.

---

## Relation To TDelta

This result supports a `TDelta`-style transition cost:

```text
TΔ_cost(C) =
sum(max(0, run_length - (C - 1)))
```

and a destination function:

```text
D(remaining_run_count) =
CLEAN_PASS                 if remaining_run_count = 0
SPIKE_FILTERED             if remaining_run_count = 1
OSCILLATING_NONPERSISTENT   if remaining_run_count >= 2
```

Together:

```text
Transition(C) = (TΔ_cost(C), D(remaining_run_count))
```

This separates distance from destination.

---

## What This Confirms

This experiment supports:

```text
transition cost / destination decomposition detected

transition_model_holds = True

failure_count = 0

cost_destination_consistency_rate = 1.0

transition cost follows thresholded reducible mass

destination class follows remaining run count

source class may change with confirmation threshold

destination distribution remains rule-consistent

temporal topology transitions can be represented as cost + destination
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal temporal transition law
real-world temporal dynamics
semantic correctness
causal correctness
optimal confirmation thresholds
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates a controlled cost/destination decomposition inside the tested classifier family.

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
transition cost
destination class
cost-destination consistency
under temporal collapse-run geometry
```

---

## Limitations

```text
This is an analytical transition model.

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

The transition model should be re-tested if classifier rules change.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Transition Cost / Destination Decomposition
```

Reason:

```text
variant_count = 24
flat_record_count = 72
cost_destination_consistency_rate = 1.0
transition_model_holds = True
transition_cost_destination_decomposition_detected = True
failure_count = 0
unique_transition_signature_count = 54
```

This is a successful controlled transition-decomposition experiment.

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

Temporal Collapse Topology Transition Cost Destination v0
-> transition cost / destination decomposition detected
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_transition_signature_stability_v0.py
```

Purpose:

```text
test whether transition signatures remain stable
under geometry perturbations
```

Main question:

```text
do similar run-length geometries produce stable transition signatures?
```

Required checks:

```text
source class
confirmation window
transition cost
remaining run count
destination class
transition signature
signature stability
signature clusters
perturbation sensitivity
```

Expected structural value:

```text
transition-signature stability map
```

---

## Final Result

```text
PASS — transition cost / destination decomposition detected.
```

Correct final conclusion:

```text
temporal topology transitions decompose into
thresholded reducible mass + post-reduction destination class.
```