# Temporal Collapse Topology Reversibility Index v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Reversibility Ranking
```

---

## Purpose

This experiment computes a normalized reversibility index for each collapse-side temporal topology class.

Previous experiments established:

```text
collapse basin is not absorbing
collapse basin is stably stratified by reversibility depth
FRAGMENTED_LOCAL_COLLAPSE escapes at depth 3
GLOBAL_PERSISTENT_COLLAPSE escapes at depth 4
RECOVERY_RELAPSE_COLLAPSE escapes at depth 4
all escape targets point to OSCILLATING_NONPERSISTENT
```

This experiment asks:

```text
which collapse-side class is most reversible?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates a normalized reversibility ranking inside the temporal collapse topology graph.

---

## Experiment File

```text
examples/temporal_collapse_topology_reversibility_index_v0.py
```

Result file:

```text
results/temporal_collapse_topology_reversibility_index_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_reversibility_index_v0.py
```

---

## Reversibility Index Definition

```text
reversibility_index =
0.45 * (1 / minimum_escape_depth)
+ 0.35 * escape_density_normalized
+ 0.10 * target_stability
+ 0.10 * depth_stability
```

Where:

```text
minimum_escape_depth
```

measures how shallowly a collapse-side class can escape back to noise-like topology.

```text
escape_density_normalized
```

measures the escape-example volume relative to the most escape-dense class.

```text
target_stability
```

equals `1.0` when the escape target remains stable.

```text
depth_stability
```

equals `1.0` when the minimum escape depth remains stable.

This is a measurement index.

It is not a semantic truth score.

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

variant_count = 5
node_count = 6

confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4

max_mutation_depth = 4

expected_escape_target = OSCILLATING_NONPERSISTENT

ranking =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE,
  GLOBAL_PERSISTENT_COLLAPSE
]

expected_ranking =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE,
  GLOBAL_PERSISTENT_COLLAPSE
]

ranking_matches_expected = True

top_reversible_class = FRAGMENTED_LOCAL_COLLAPSE
```

The experiment passed.

The central result is:

```text
collapse-basin reversibility ranking detected
```

---

## Main Finding

The measured ranking is:

```text
1. FRAGMENTED_LOCAL_COLLAPSE
2. RECOVERY_RELAPSE_COLLAPSE
3. GLOBAL_PERSISTENT_COLLAPSE
```

Measured scores:

```text
FRAGMENTED_LOCAL_COLLAPSE        index = 0.7

RECOVERY_RELAPSE_COLLAPSE        index = 0.32957317073170733

GLOBAL_PERSISTENT_COLLAPSE       index = 0.3231707317073171
```

Correct conclusion:

```text
FRAGMENTED_LOCAL_COLLAPSE is the most reversible collapse-basin class.
```

---

## Component Partition

### Noise Component

```text
CLEAN_PASS
SPIKE_FILTERED
OSCILLATING_NONPERSISTENT
```

### Collapse Component

```text
FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

The experiment measures reversibility from the collapse component back into the noise component.

---

## Ranking With Scores

### Rank 1 — FRAGMENTED_LOCAL_COLLAPSE

```text
rank = 1
class = FRAGMENTED_LOCAL_COLLAPSE

reversibility_index = 0.7

minimum_escape_depth = 3

escape_example_count_total = 13120

escape_target =
[
  OSCILLATING_NONPERSISTENT
]
```

Interpretation:

```text
FRAGMENTED_LOCAL_COLLAPSE is the highest-reversibility class.
```

It has the shallowest escape depth and the highest escape-example density.

---

### Rank 2 — RECOVERY_RELAPSE_COLLAPSE

```text
rank = 2
class = RECOVERY_RELAPSE_COLLAPSE

reversibility_index = 0.32957317073170733

minimum_escape_depth = 4

escape_example_count_total = 640

escape_target =
[
  OSCILLATING_NONPERSISTENT
]
```

Interpretation:

```text
RECOVERY_RELAPSE_COLLAPSE is less reversible than FRAGMENTED_LOCAL_COLLAPSE,
but slightly more reversible than GLOBAL_PERSISTENT_COLLAPSE.
```

The difference comes from higher escape-example density.

---

### Rank 3 — GLOBAL_PERSISTENT_COLLAPSE

```text
rank = 3
class = GLOBAL_PERSISTENT_COLLAPSE

reversibility_index = 0.3231707317073171

minimum_escape_depth = 4

escape_example_count_total = 400

escape_target =
[
  OSCILLATING_NONPERSISTENT
]
```

Interpretation:

```text
GLOBAL_PERSISTENT_COLLAPSE is the least reversible collapse-side class
under this index.
```

It shares depth 4 with `RECOVERY_RELAPSE_COLLAPSE`, but has lower escape-example density.

---

## Class Reversibility Summary

### FRAGMENTED_LOCAL_COLLAPSE

```text
minimum_escape_depths = [3, 3, 3, 3, 3]
minimum_escape_depth = 3
mean_escape_depth = 3
escape_depth_std = 0.0

escape_depth_stable = True

escape_targets_by_variant =
[
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT]
]

escape_target_stable = True

escape_example_counts = [1600, 2112, 2624, 3136, 3648]
escape_example_count_total = 13120

depth_component = 0.3333333333333333
density_component = 1.0
target_stability_component = 1.0
depth_stability_component = 1.0

reversibility_index = 0.7
```

Interpretation:

```text
FRAGMENTED_LOCAL_COLLAPSE combines:
shallowest escape depth
highest escape density
stable target
stable depth
```

This is why it ranks first.

---

### RECOVERY_RELAPSE_COLLAPSE

```text
minimum_escape_depths = [4, 4, 4, 4, 4]
minimum_escape_depth = 4
mean_escape_depth = 4
escape_depth_std = 0.0

escape_depth_stable = True

escape_targets_by_variant =
[
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT]
]

escape_target_stable = True

escape_example_counts = [128, 128, 128, 128, 128]
escape_example_count_total = 640

depth_component = 0.25
density_component = 0.04878048780487805
target_stability_component = 1.0
depth_stability_component = 1.0

reversibility_index = 0.32957317073170733
```

Interpretation:

```text
RECOVERY_RELAPSE_COLLAPSE has stable reversibility at depth 4.
```

It ranks second because its escape density is higher than `GLOBAL_PERSISTENT_COLLAPSE`.

---

### GLOBAL_PERSISTENT_COLLAPSE

```text
minimum_escape_depths = [4, 4, 4, 4, 4]
minimum_escape_depth = 4
mean_escape_depth = 4
escape_depth_std = 0.0

escape_depth_stable = True

escape_targets_by_variant =
[
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT]
]

escape_target_stable = True

escape_example_counts = [80, 80, 80, 80, 80]
escape_example_count_total = 400

depth_component = 0.25
density_component = 0.03048780487804878
target_stability_component = 1.0
depth_stability_component = 1.0

reversibility_index = 0.3231707317073171
```

Interpretation:

```text
GLOBAL_PERSISTENT_COLLAPSE has stable reversibility at depth 4,
but lower escape density than RECOVERY_RELAPSE_COLLAPSE.
```

Therefore it ranks third.

---

## Depth Distribution

### FRAGMENTED_LOCAL_COLLAPSE

```text
depth_hits =
{
  1: 0,
  2: 0,
  3: 5,
  4: 5
}

depth_examples =
{
  1: 0,
  2: 0,
  3: 320,
  4: 12800
}
```

Interpretation:

```text
escape first appears at depth 3,
then becomes much denser at depth 4.
```

---

### RECOVERY_RELAPSE_COLLAPSE

```text
depth_hits =
{
  1: 0,
  2: 0,
  3: 0,
  4: 5
}

depth_examples =
{
  1: 0,
  2: 0,
  3: 0,
  4: 640
}
```

Interpretation:

```text
escape first appears at depth 4.
```

---

### GLOBAL_PERSISTENT_COLLAPSE

```text
depth_hits =
{
  1: 0,
  2: 0,
  3: 0,
  4: 5
}

depth_examples =
{
  1: 0,
  2: 0,
  3: 0,
  4: 400
}
```

Interpretation:

```text
escape first appears at depth 4.
```

---

## Variant-Level Stability

Across all five variants:

```text
FRAGMENTED_LOCAL_COLLAPSE:
minimum_escape_depth = 3
target = OSCILLATING_NONPERSISTENT

RECOVERY_RELAPSE_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT

GLOBAL_PERSISTENT_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
```

The target remained stable.

The escape depth remained stable.

The ranking remained stable.

---

## Why The Result Is PASS

The experiment required:

```text
ranking_matches_expected = True
top_reversible_class = FRAGMENTED_LOCAL_COLLAPSE
```

Both conditions were satisfied.

Therefore:

```text
Status = PASS
```

The result confirms a normalized reversibility ranking for collapse-side temporal topology classes.

---

## Structural Meaning

The collapse basin is not flat.

It has a measurable reversibility hierarchy:

```text
FRAGMENTED_LOCAL_COLLAPSE
>
RECOVERY_RELAPSE_COLLAPSE
>
GLOBAL_PERSISTENT_COLLAPSE
```

The highest-reversibility class is:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

This confirms its role as:

```text
entry interface
escape interface
highest reversibility class
basin boundary class
```

This is the strongest structural interpretation so far.

---

## Updated Collapse-Basin Model

The collapse basin now has three measurable layers:

```text
boundary / interface layer:
FRAGMENTED_LOCAL_COLLAPSE

relapse-reversible layer:
RECOVERY_RELAPSE_COLLAPSE

persistent-collapse layer:
GLOBAL_PERSISTENT_COLLAPSE
```

All classes can return to:

```text
OSCILLATING_NONPERSISTENT
```

but with different reversibility strength.

The measured order is:

```text
FRAGMENTED_LOCAL_COLLAPSE
  escape depth 3
  highest density
  highest reversibility

RECOVERY_RELAPSE_COLLAPSE
  escape depth 4
  medium density
  medium reversibility

GLOBAL_PERSISTENT_COLLAPSE
  escape depth 4
  lower density
  lowest reversibility
```

---

## Relation To Escape Depth Stability v0

Escape Depth Stability v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE        escape depth = 3
GLOBAL_PERSISTENT_COLLAPSE       escape depth = 4
RECOVERY_RELAPSE_COLLAPSE        escape depth = 4
```

Reversibility Index v0 adds density and stability into a single normalized score.

This converts:

```text
escape-depth ordering
```

into:

```text
reversibility ranking
```

---

## Relation To Basin Entry Stability v0

Basin Entry Stability v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE is the canonical basin-entry state.
```

Reversibility Index v0 shows:

```text
FRAGMENTED_LOCAL_COLLAPSE is also the most reversible collapse-side state.
```

Together:

```text
FRAGMENTED_LOCAL_COLLAPSE is the basin boundary class.
```

It is both the easiest entry state and the easiest escape state.

---

## Relation To Basin Escape v0

Basin Escape v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

Reversibility Index v0 generalizes this into a ranking across all collapse-side classes.

---

## Relation To OMNIATEMPO

This result strengthens OMNIATEMPO by introducing a normalized reversibility metric.

OMNIATEMPO can now represent:

```text
collapse class
escape depth
escape density
target stability
depth stability
reversibility index
```

This gives the temporal topology framework a measurable internal order.

The collapse basin becomes a scored structure, not only a set of class labels.

---

## Relation To TDelta

This result supports future metrics such as:

```text
TDelta_escape_depth
TDelta_reversibility
TΔ_escape_depth
TΔ_reversibility
```

Possible structure:

```text
TΔ_escape_depth(class) = minimum mutation depth needed to escape

TΔ_reversibility(class) = normalized score combining:
escape depth
escape density
target stability
depth stability
```

Under this experiment:

```text
TΔ_reversibility(FRAGMENTED_LOCAL_COLLAPSE) = 0.7

TΔ_reversibility(RECOVERY_RELAPSE_COLLAPSE) = 0.32957317073170733

TΔ_reversibility(GLOBAL_PERSISTENT_COLLAPSE) = 0.3231707317073171
```

---

## What This Confirms

This experiment supports:

```text
collapse-basin reversibility ranking detected

FRAGMENTED_LOCAL_COLLAPSE is the most reversible collapse-side class

RECOVERY_RELAPSE_COLLAPSE ranks second

GLOBAL_PERSISTENT_COLLAPSE ranks third

all collapse-side classes escape toward OSCILLATING_NONPERSISTENT

escape targets are stable

escape depths are stable

reversibility ranking matches expected order

FRAGMENTED_LOCAL_COLLAPSE acts as the basin boundary class
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal reversibility ranking
real-world recoverability
semantic correctness
causal correctness
optimal mutation model
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates controlled synthetic reversibility ranking under the tested mutation space.

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
normalized reversibility ranking
inside collapse-side temporal topology
under controlled mutation search
```

---

## Limitations

```text
Only five variants were tested.

Only three collapse-side source classes were tested.

Only mutation depths 1, 2, 3, and 4 were searched.

Only three frame values were allowed:
PASS
ESCALATE
COLLAPSE

The reversibility index is hand-weighted.

The base trajectories were synthetic.

The mutation graph was deterministic.

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

Different index weights may change close rankings between
RECOVERY_RELAPSE_COLLAPSE and GLOBAL_PERSISTENT_COLLAPSE.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Reversibility Ranking
```

Reason:

```text
variant_count = 5

max_mutation_depth = 4

ranking_matches_expected = True

top_reversible_class = FRAGMENTED_LOCAL_COLLAPSE

FRAGMENTED_LOCAL_COLLAPSE reversibility_index = 0.7

RECOVERY_RELAPSE_COLLAPSE reversibility_index = 0.32957317073170733

GLOBAL_PERSISTENT_COLLAPSE reversibility_index = 0.3231707317073171

all classes escape toward OSCILLATING_NONPERSISTENT

escape depth is stable

escape target is stable
```

This is a successful controlled reversibility-ranking experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_boundary_cycle_v0.py
```

Purpose:

```text
measure the cycle between OSCILLATING_NONPERSISTENT and FRAGMENTED_LOCAL_COLLAPSE
```

Main question:

```text
is the basin boundary a stable two-way cycle?
```

Required checks:

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE

FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT

cycle depth

cycle asymmetry

cycle density

cycle stability

boundary-cycle index
```

Expected structural value:

```text
basin-boundary cycle measurement
```

---

## Final Result

```text
PASS — collapse-basin reversibility ranking detected.
```

Correct final conclusion:

```text
FRAGMENTED_LOCAL_COLLAPSE is the most reversible collapse-basin class
and acts as the basin boundary class.
```