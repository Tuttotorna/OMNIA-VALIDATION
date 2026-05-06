# Temporal Collapse Topology Boundary Cycle Stability v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Boundary-Cycle Stability Probe
```

---

## Purpose

This experiment stress-tests whether the asymmetric basin-boundary cycle remains stable under altered trajectory geometry.

The previous experiment measured:

```text
OSCILLATING_NONPERSISTENT <-> FRAGMENTED_LOCAL_COLLAPSE

forward depth = 1
reverse depth = 3
cycle asymmetry = 2
```

This experiment changes geometry across:

```text
oscillation spacing
fragmented-collapse spacing
trajectory length
collapse positions
run density
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates whether the boundary cycle remains stable when the geometry of the source trajectories changes.

---

## Experiment File

```text
examples/temporal_collapse_topology_boundary_cycle_stability_v0.py
```

Result file:

```text
results/temporal_collapse_topology_boundary_cycle_stability_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_boundary_cycle_stability_v0.py
```

---

## Summary Result

```text
Status: CHECK
Version: 0.1.0

variant_count = 8
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
expected_cycle_stable = False

forward_depths =
[1, 1, 1, 1, 1, 1, 1, 1]

reverse_depths =
[3, 3, 3, 3, 3, 3, 4, 4]

forward_depth_stable = True
reverse_depth_stable = False

cycle_depth_sums =
[4, 4, 4, 4, 4, 4, 5, 5]

cycle_depth_sum_mean = 4.25
cycle_depth_sum_stable = False

cycle_depth_asymmetries =
[2, 2, 2, 2, 2, 2, 3, 3]

cycle_asymmetry_mean = 2.25
cycle_asymmetry_stable = False

forward_example_total = 676759
reverse_example_total = 16768

cycle_density_ratio_mean = 121.49976751254495

boundary_cycle_index_mean = 0.012006418612918904
boundary_cycle_index_std = 0.01270085228050615
```

The result is `CHECK`.

The cycle exists across all tested geometries, but its reverse depth is geometry-sensitive.

---

## Main Finding

This experiment confirmed:

```text
boundary cycle existence is stable
```

because:

```text
all_cycles_detected = True
```

It also confirmed:

```text
forward entry depth is stable
```

because:

```text
forward_depths = [1, 1, 1, 1, 1, 1, 1, 1]
forward_depth_stable = True
```

But it falsified:

```text
reverse depth is always 3
```

because:

```text
reverse_depths = [3, 3, 3, 3, 3, 3, 4, 4]
reverse_depth_stable = False
```

Correct conclusion:

```text
boundary cycle existence is stable,
but reverse escape depth is geometry-sensitive
```

---

## Component Meaning

The measured boundary remains:

```text
OSCILLATING_NONPERSISTENT <-> FRAGMENTED_LOCAL_COLLAPSE
```

The forward direction is:

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
```

The reverse direction is:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

The forward direction remained stable at depth 1.

The reverse direction remained possible in every geometry, but required either depth 3 or depth 4 depending on geometry.

---

## Stable Component

### Forward Transition

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
```

Measured depths:

```text
[1, 1, 1, 1, 1, 1, 1, 1]
```

Interpretation:

```text
entry into the collapse-entry state is stable and shallow
across all tested geometries
```

This is the strongest stable part of the boundary-cycle structure.

---

## Geometry-Sensitive Component

### Reverse Transition

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

Measured depths:

```text
[3, 3, 3, 3, 3, 3, 4, 4]
```

Interpretation:

```text
escape from the collapse-entry state remains possible in all geometries,
but the required depth depends on trajectory geometry
```

This is why the result is `CHECK`, not `PASS`.

The expected fully stable cycle geometry was not confirmed.

---

## Variant-Level Results

### Variant 0 — compact_low_spacing

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 9608
reverse_examples = 1600

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

density_ratio = 6.005

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

### Variant 1 — medium_shifted_spacing

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 26121
reverse_examples = 2112

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

density_ratio = 12.367897727272727

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

### Variant 2 — wide_spacing

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 55363
reverse_examples = 2624

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

density_ratio = 21.098704268292682

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

### Variant 3 — long_sparse_spacing

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 167773
reverse_examples = 3648

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

density_ratio = 45.99040570175438

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

### Variant 4 — front_loaded_geometry

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 75883
reverse_examples = 2880

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

density_ratio = 26.348263888888887

boundary_cycle_index = 0.009488291185113925
```

Depth distribution:

```text
forward_counts =
{
  1: 6,
  2: 260,
  3: 5365,
  4: 70252
}

reverse_counts =
{
  1: 0,
  2: 0,
  3: 64,
  4: 2816
}
```

---

### Variant 5 — back_loaded_geometry

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 3

forward_examples = 131746
reverse_examples = 3392

cycle_depth_sum = 4
cycle_depth_asymmetry = 2

density_ratio = 38.84021226415094

boundary_cycle_index = 0.006436628057018809
```

Depth distribution:

```text
forward_counts =
{
  1: 6,
  2: 312,
  3: 7773,
  4: 123655
}

reverse_counts =
{
  1: 0,
  2: 0,
  3: 64,
  4: 3328
}
```

---

### Variant 6 — four_spike_oscillation

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 4

forward_examples = 120702
reverse_examples = 256

cycle_depth_sum = 5
cycle_depth_asymmetry = 3

density_ratio = 471.4921875

boundary_cycle_index = 0.00042418518334410367
```

Depth distribution:

```text
forward_counts =
{
  1: 8,
  2: 365,
  3: 8004,
  4: 112325
}

reverse_counts =
{
  1: 0,
  2: 0,
  3: 0,
  4: 256
}
```

---

### Variant 7 — dense_fragmented_geometry

```text
cycle_detected = True

forward_depth = 1
reverse_depth = 4

forward_examples = 89563
reverse_examples = 256

cycle_depth_sum = 5
cycle_depth_asymmetry = 3

density_ratio = 349.85546875

boundary_cycle_index = 0.0005716646382992977
```

Depth distribution:

```text
forward_counts =
{
  1: 8,
  2: 331,
  3: 6552,
  4: 82672
}

reverse_counts =
{
  1: 0,
  2: 0,
  3: 0,
  4: 256
}
```

---

## Why The Result Is CHECK

The original expectation was:

```text
forward_depth = 1
reverse_depth = 3
cycle_asymmetry = 2
```

for all geometries.

The experiment found:

```text
forward_depth = 1
```

for all geometries.

But reverse depth shifted:

```text
reverse_depth = 3
```

for six geometries.

```text
reverse_depth = 4
```

for two geometries.

Therefore:

```text
expected_cycle_stable = False
reverse_depth_stable = False
cycle_asymmetry_stable = False
cycle_depth_sum_stable = False
```

The result is `CHECK`.

This does not invalidate the boundary cycle.

It refines it.

---

## Structural Meaning

The basin boundary has two layers of stability.

### Stable Layer

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
```

This transition is stable at depth 1 under all tested geometries.

### Geometry-Sensitive Layer

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

This transition remains possible under all tested geometries, but the required depth shifts between 3 and 4.

Therefore:

```text
boundary cycle existence is stable
```

but:

```text
reverse escape depth is geometry-sensitive
```

---

## Updated Boundary-Cycle Model

The previous model was:

```text
OSCILLATING_NONPERSISTENT <-> FRAGMENTED_LOCAL_COLLAPSE

forward depth = 1
reverse depth = 3
cycle asymmetry = 2
```

The updated model is:

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
  depth = 1 stable

FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
  depth = 3 or 4 depending on geometry
```

So the boundary cycle is real, but its reverse direction has geometry-dependent depth.

---

## Relation To Boundary Cycle v0

Boundary Cycle v0 found:

```text
forward depth = 1
reverse depth = 3
cycle asymmetry = 2
```

Boundary Cycle Stability v0 shows this is true for many geometries, but not all.

The stress test exposed:

```text
reverse depth = 4
```

in denser/four-spike geometries.

Therefore Boundary Cycle v0 was correct inside its geometry family, but not universal across altered geometry.

---

## Relation To Reversibility Index v0

Reversibility Index v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE is the most reversible collapse-side class.
```

Boundary Cycle Stability v0 refines this:

```text
FRAGMENTED_LOCAL_COLLAPSE remains reversible,
but the cost of escape depends on geometry.
```

This means reversibility should be treated as a depth-sensitive and geometry-sensitive measurement.

---

## Relation To OMNIATEMPO

This experiment improves OMNIATEMPO by adding geometry sensitivity to boundary-cycle measurement.

OMNIATEMPO should not only measure:

```text
does a cycle exist?
```

It should also measure:

```text
how stable is the cycle depth?
```

and:

```text
how sensitive is reverse escape to geometry?
```

This gives temporal topology a sharper diagnostic layer.

---

## Relation To TDelta

This result supports future metrics such as:

```text
TDelta_boundary_entry
TDelta_boundary_escape
TDelta_cycle_asymmetry
TDelta_geometry_sensitivity

TΔ_boundary_entry
TΔ_boundary_escape
TΔ_cycle_asymmetry
TΔ_geometry_sensitivity
```

Measured values:

```text
TΔ_boundary_entry = 1

TΔ_boundary_escape = 3 or 4

TΔ_cycle_asymmetry = 2 or 3
```

A possible geometry-sensitivity measure:

```text
TΔ_geometry_sensitivity =
std(reverse_depths)
```

Under this experiment:

```text
reverse_depths = [3, 3, 3, 3, 3, 3, 4, 4]
```

So the reverse path is structurally geometry-sensitive.

---

## What This Confirms

This experiment supports:

```text
boundary cycle exists across all tested geometries

OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE is stable at depth 1

FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT remains possible in all geometries

forward entry is shallower than reverse escape

cycle asymmetry persists

reverse escape depth is geometry-sensitive

boundary cycle existence is more stable than boundary cycle depth
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal boundary-cycle stability
universal reverse-depth stability
real-world temporal dynamics
semantic correctness
causal correctness
optimal mutation model
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates controlled synthetic boundary-cycle stability probing under altered trajectory geometry.

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
boundary-cycle existence
forward-depth stability
reverse-depth sensitivity
cycle-asymmetry sensitivity
under controlled mutation search
```

---

## Limitations

```text
Only eight geometry variants were tested.

Only two boundary classes were tested directly.

Only mutation depths 1, 2, 3, and 4 were searched.

Only three frame values were allowed:
PASS
ESCALATE
COLLAPSE

The geometries were synthetic.

The mutation graph was deterministic.

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

Higher mutation depths may expose additional cycle structure.

Different geometry families may produce different reverse-depth behavior.
```

---

## Result Classification

Recommended classification:

```text
CHECK
```

Evidence level:

```text
Level 2 — Temporal Topology Boundary-Cycle Stability Probe
```

Reason:

```text
all_cycles_detected = True

forward_depth_stable = True

reverse_depth_stable = False

reverse_depths = [3, 3, 3, 3, 3, 3, 4, 4]

cycle_asymmetry_stable = False

cycle_depth_sum_stable = False

expected_cycle_stable = False
```

This is a useful `CHECK`.

It proves cycle existence stability, while exposing geometry sensitivity in reverse escape depth.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_geometry_sensitivity_v0.py
```

Purpose:

```text
measure which geometric factors cause reverse escape depth
to shift from 3 to 4
```

Main question:

```text
which trajectory geometry features control reverse-depth sensitivity?
```

Required checks:

```text
number of collapse runs

run spacing

trajectory length

front-loaded vs back-loaded collapse

dense vs sparse fragmentation

collapse-run count

minimum reverse depth

reverse density

geometry-sensitivity index
```

Expected structural value:

```text
geometry-to-reversibility mapping
```

---

## Final Result

```text
CHECK — boundary-cycle existence remained stable,
but reverse escape depth was geometry-sensitive.
```

Correct final conclusion:

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
is stable at depth 1,
while
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
remains possible but shifts between depth 3 and depth 4
depending on geometry.
```