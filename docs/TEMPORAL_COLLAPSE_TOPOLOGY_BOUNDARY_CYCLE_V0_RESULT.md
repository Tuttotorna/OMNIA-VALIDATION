# Temporal Collapse Topology Boundary Cycle v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Basin-Boundary Cycle Measurement
```

---

## Purpose

This experiment measures whether the basin boundary forms a stable reversible cycle between:

```text
OSCILLATING_NONPERSISTENT
```

and:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

Previous experiments established:

```text
FRAGMENTED_LOCAL_COLLAPSE is the canonical basin-entry state

FRAGMENTED_LOCAL_COLLAPSE is the most reversible collapse-basin class

OSCILLATING_NONPERSISTENT is the stable escape target

collapse basin is stably stratified by reversibility depth
```

This experiment asks:

```text
is the basin boundary a stable two-way cycle?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates cycle structure at the boundary between noise-like topology and collapse-entry topology.

---

## Experiment File

```text
examples/temporal_collapse_topology_boundary_cycle_v0.py
```

Result file:

```text
results/temporal_collapse_topology_boundary_cycle_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_boundary_cycle_v0.py
```

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

boundary_cycle =
OSCILLATING_NONPERSISTENT <-> FRAGMENTED_LOCAL_COLLAPSE

forward_transition =
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE

reverse_transition =
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT

all_cycles_detected = True
expected_cycle_detected = True

forward_depths = [1, 1, 1, 1, 1]
reverse_depths = [3, 3, 3, 3, 3]

forward_depth_stable = True
reverse_depth_stable = True

cycle_depth_sums = [4, 4, 4, 4, 4]
cycle_depth_sum_mean = 4

cycle_depth_asymmetries = [2, 2, 2, 2, 2]
cycle_asymmetry_mean = 2

forward_example_total = 360168
reverse_example_total = 13120

boundary_cycle_index_mean = 0.01737394772018297
boundary_cycle_index_std = 0.013133054404879881
```

The experiment passed.

The central result is:

```text
basin-boundary cycle detected
```

---

## Main Finding

The measured cycle is:

```text
OSCILLATING_NONPERSISTENT <-> FRAGMENTED_LOCAL_COLLAPSE
```

The forward transition is shallow:

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
minimum depth = 1
```

The reverse transition is deeper:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
minimum depth = 3
```

Therefore the basin boundary is reversible but asymmetric.

Correct conclusion:

```text
entering the collapse-entry state is easier than escaping it
```

---

## Component Meaning

The two boundary classes are:

```text
OSCILLATING_NONPERSISTENT
```

Noise-side unstable topology.

```text
FRAGMENTED_LOCAL_COLLAPSE
```

Collapse-side basin-entry topology.

Together they form the measured boundary cycle:

```text
noise-side instability
<->
collapse-entry instability
```

This is not semantic oscillation.

It is structural reversibility under controlled mutation.

---

## Forward Transition

### OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE

```text
forward_depths = [1, 1, 1, 1, 1]
forward_depth_stable = True

forward_example_total = 360168
forward_example_mean = 72033.6
```

Interpretation:

```text
OSCILLATING_NONPERSISTENT is one mutation away
from FRAGMENTED_LOCAL_COLLAPSE across all tested variants.
```

This confirms that unstable oscillation can enter local confirmed collapse very easily.

The forward direction is dense and shallow.

---

## Reverse Transition

### FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT

```text
reverse_depths = [3, 3, 3, 3, 3]
reverse_depth_stable = True

reverse_example_total = 13120
reverse_example_mean = 2624
```

Interpretation:

```text
FRAGMENTED_LOCAL_COLLAPSE can return to OSCILLATING_NONPERSISTENT,
but it requires depth 3.
```

This confirms that the collapse-entry state is reversible, but less easily than the forward entry direction.

---

## Cycle Asymmetry

The measured cycle depth is:

```text
forward_depth = 1
reverse_depth = 3
cycle_depth_sum = 4
cycle_depth_asymmetry = 2
```

Across all variants:

```text
cycle_depth_sums = [4, 4, 4, 4, 4]
cycle_depth_asymmetries = [2, 2, 2, 2, 2]
```

Interpretation:

```text
the basin-boundary cycle is stable but not symmetric
```

The forward direction is easier:

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
```

The reverse direction is harder:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

This is a directional structural bias.

---

## Variant-Level Results

### Variant 0

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 9608
reverse_examples = 1600

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

boundary_cycle_index = 0.041631973355537054
```

Depth distribution:

```text
forward_counts =
{
  1: 6,
  2: 130,
  3: 1311,
  4: 8161
}

reverse_counts =
{
  1: 0,
  2: 0,
  3: 64,
  4: 1536
}
```

---

### Variant 1

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 26121
reverse_examples = 2112

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

boundary_cycle_index = 0.020213621224302286
```

Depth distribution:

```text
forward_counts =
{
  1: 6,
  2: 182,
  3: 2603,
  4: 23330
}

reverse_counts =
{
  1: 0,
  2: 0,
  3: 64,
  4: 2048
}
```

---

### Variant 2

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 55363
reverse_examples = 2624

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

boundary_cycle_index = 0.011849068872712823
```

Depth distribution:

```text
forward_counts =
{
  1: 6,
  2: 234,
  3: 4335,
  4: 50788
}

reverse_counts =
{
  1: 0,
  2: 0,
  3: 64,
  4: 2560
}
```

---

### Variant 3

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 101303
reverse_examples = 3136

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

boundary_cycle_index = 0.007739158761339743
```

Depth distribution:

```text
forward_counts =
{
  1: 6,
  2: 286,
  3: 6515,
  4: 94496
}

reverse_counts =
{
  1: 0,
  2: 0,
  3: 64,
  4: 3072
}
```

---

### Variant 4

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 167773
reverse_examples = 3648

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

boundary_cycle_index = 0.005435916387022941
```

Depth distribution:

```text
forward_counts =
{
  1: 6,
  2: 338,
  3: 9143,
  4: 158286
}

reverse_counts =
{
  1: 0,
  2: 0,
  3: 64,
  4: 3584
}
```

---

## Density Difference

The forward direction has much higher example volume:

```text
forward_example_total = 360168
reverse_example_total = 13120
```

This means:

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
```

is not only shallower.

It is also much denser.

The reverse path exists and is stable, but it is less dense and requires greater mutation depth.

---

## Why The Result Is PASS

The experiment required:

```text
all_cycles_detected = True
forward_depth_stable = True
reverse_depth_stable = True
expected_cycle_detected = True
```

All were satisfied.

Therefore:

```text
Status = PASS
```

The test confirms a stable reversible boundary cycle.

---

## Structural Meaning

The basin boundary is not a one-way gate.

It is a reversible but asymmetric cycle:

```text
OSCILLATING_NONPERSISTENT <-> FRAGMENTED_LOCAL_COLLAPSE
```

The measured asymmetry is:

```text
entering collapse-entry topology: depth 1
escaping collapse-entry topology: depth 3
```

This means:

```text
the system can move both ways,
but collapse-entry is easier to enter than to exit
```

This is a useful temporal-topology result.

---

## Updated Basin-Boundary Model

The updated model is:

```text
OSCILLATING_NONPERSISTENT
  -> FRAGMENTED_LOCAL_COLLAPSE
  depth = 1

FRAGMENTED_LOCAL_COLLAPSE
  -> OSCILLATING_NONPERSISTENT
  depth = 3
```

Compressed form:

```text
OSCILLATING_NONPERSISTENT <-> FRAGMENTED_LOCAL_COLLAPSE

forward depth = 1
reverse depth = 3
cycle asymmetry = 2
```

This defines the basin boundary as a measurable reversible interface.

---

## Relation To Reversibility Index v0

Reversibility Index v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE is the most reversible collapse-basin class.
```

Boundary Cycle v0 explains why.

`FRAGMENTED_LOCAL_COLLAPSE` is reversible because it is part of a stable two-way boundary cycle with:

```text
OSCILLATING_NONPERSISTENT
```

---

## Relation To Basin Entry Stability v0

Basin Entry Stability v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE is the canonical basin-entry state.
```

Boundary Cycle v0 adds:

```text
the canonical basin-entry state is part of a reversible boundary cycle
```

So the updated role is:

```text
FRAGMENTED_LOCAL_COLLAPSE is the basin-entry and basin-exit interface.
```

---

## Relation To Escape Depth Stability v0

Escape Depth Stability v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE escapes at depth 3
```

Boundary Cycle v0 adds the other half:

```text
OSCILLATING_NONPERSISTENT enters FRAGMENTED_LOCAL_COLLAPSE at depth 1
```

So the full boundary relation is:

```text
entry depth = 1
exit depth = 3
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO by identifying a stable reversible boundary cycle.

OMNIATEMPO can now represent:

```text
noise-side instability
collapse-entry topology
forward transition depth
reverse transition depth
cycle asymmetry
boundary-cycle index
```

This makes the temporal topology more than a set of labels.

It becomes a directed, depth-weighted topology.

---

## Relation To TDelta

This result supports future metrics such as:

```text
TDelta_boundary_entry
TDelta_boundary_escape
TDelta_cycle_asymmetry
TΔ_boundary_entry
TΔ_boundary_escape
TΔ_cycle_asymmetry
```

Measured values:

```text
TΔ_boundary_entry = 1

TΔ_boundary_escape = 3

TΔ_cycle_asymmetry = 2
```

Possible structural definition:

```text
TΔ_cycle_asymmetry =
TΔ_boundary_escape - TΔ_boundary_entry
```

Under this experiment:

```text
3 - 1 = 2
```

---

## What This Confirms

This experiment supports:

```text
basin-boundary cycle detected

OSCILLATING_NONPERSISTENT <-> FRAGMENTED_LOCAL_COLLAPSE is measurable

forward direction is depth 1

reverse direction is depth 3

forward depth is stable

reverse depth is stable

cycle depth sum is 4

cycle asymmetry is 2

entering collapse-entry topology is easier than escaping it

FRAGMENTED_LOCAL_COLLAPSE is the basin boundary class
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal boundary-cycle structure
real-world temporal dynamics
semantic correctness
causal correctness
optimal mutation model
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates controlled synthetic basin-boundary cycle measurement under the tested mutation space.

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
reversible cycle structure
between OSCILLATING_NONPERSISTENT
and FRAGMENTED_LOCAL_COLLAPSE
under controlled mutation search
```

---

## Limitations

```text
Only five variants were tested.

Only two boundary classes were tested directly.

Only mutation depths 1, 2, 3, and 4 were searched.

Only three frame values were allowed:
PASS
ESCALATE
COLLAPSE

The cycle index decreases as sequence length increases because the formula normalizes by density imbalance.

The base trajectories were synthetic.

The mutation graph was deterministic.

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

Different cycle-index definitions may produce different scale values.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Basin-Boundary Cycle Measurement
```

Reason:

```text
variant_count = 5

max_mutation_depth = 4

all_cycles_detected = True

expected_cycle_detected = True

forward_depths = [1, 1, 1, 1, 1]

reverse_depths = [3, 3, 3, 3, 3]

forward_depth_stable = True

reverse_depth_stable = True

cycle_depth_sum_mean = 4

cycle_asymmetry_mean = 2

forward_example_total = 360168

reverse_example_total = 13120
```

This is a successful controlled basin-boundary cycle measurement.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_boundary_cycle_stability_v0.py
```

Purpose:

```text
stress-test whether the boundary cycle remains stable
under wider trajectory variants and altered oscillation/collapse geometry
```

Main question:

```text
does the asymmetric boundary cycle remain stable
when the geometry of the source trajectories changes?
```

Required checks:

```text
more variants

different oscillation spacing

different fragmented-collapse run spacing

different trajectory lengths

forward depth stability

reverse depth stability

cycle asymmetry stability

boundary-cycle index stability
```

Expected structural value:

```text
boundary-cycle stability
```

---

## Final Result

```text
PASS — basin-boundary cycle detected.
```

Correct final conclusion:

```text
OSCILLATING_NONPERSISTENT and FRAGMENTED_LOCAL_COLLAPSE
form a stable reversible but asymmetric basin-boundary cycle.
```