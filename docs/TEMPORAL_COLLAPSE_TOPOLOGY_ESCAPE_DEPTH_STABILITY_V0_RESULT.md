# Temporal Collapse Topology Escape Depth Stability v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Escape-Depth Ordering Stability
```

---

## Purpose

This experiment tests whether the escape-depth ordering discovered in:

```text
Temporal Collapse Topology Absorption Depth v0
```

remains stable under wider trajectory variants.

The previous experiment showed:

```text
FRAGMENTED_LOCAL_COLLAPSE        escape depth = 3
GLOBAL_PERSISTENT_COLLAPSE       escape depth = 4
RECOVERY_RELAPSE_COLLAPSE        escape depth = 4
```

This experiment asks:

```text
does this escape-depth ordering remain stable
when trajectory variants are widened?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates escape-depth ordering stability inside the temporal collapse topology graph.

---

## Experiment File

```text
examples/temporal_collapse_topology_escape_depth_stability_v0.py
```

Result file:

```text
results/temporal_collapse_topology_escape_depth_stability_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_escape_depth_stability_v0.py
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

expected_escape_target = OSCILLATING_NONPERSISTENT

expected_escape_depths =
{
  FRAGMENTED_LOCAL_COLLAPSE: 3,
  GLOBAL_PERSISTENT_COLLAPSE: 4,
  RECOVERY_RELAPSE_COLLAPSE: 4
}

ordering_values =
{
  FRAGMENTED_LOCAL_COLLAPSE: 3,
  GLOBAL_PERSISTENT_COLLAPSE: 4,
  RECOVERY_RELAPSE_COLLAPSE: 4
}

expected_ordering_detected = True
all_depths_stable = True
all_targets_stable = True
all_expected_depths_matched = True
```

The experiment passed.

The central result is:

```text
escape-depth ordering stability detected
```

---

## Main Finding

Across all five variants, the escape-depth ordering remained:

```text
FRAGMENTED_LOCAL_COLLAPSE        escape depth = 3
GLOBAL_PERSISTENT_COLLAPSE       escape depth = 4
RECOVERY_RELAPSE_COLLAPSE        escape depth = 4
```

The escape target was also stable:

```text
OSCILLATING_NONPERSISTENT
```

Therefore the collapse basin is not absorbing.

It is stably stratified by reversibility depth.

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

The experiment measures escape from collapse-side topology back into noise-like topology.

---

## Class Escape-Depth Stability

### FRAGMENTED_LOCAL_COLLAPSE

```text
minimum_escape_depths = [3, 3, 3, 3, 3]
minimum_escape_depth_mean = 3
minimum_escape_depth_std = 0.0

expected_escape_depth = 3
expected_depth_matched = True

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
```

Interpretation:

```text
FRAGMENTED_LOCAL_COLLAPSE is the closest collapse-side class to escape.
```

It is consistently reversible at depth 3.

---

### GLOBAL_PERSISTENT_COLLAPSE

```text
minimum_escape_depths = [4, 4, 4, 4, 4]
minimum_escape_depth_mean = 4
minimum_escape_depth_std = 0.0

expected_escape_depth = 4
expected_depth_matched = True

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
```

Interpretation:

```text
GLOBAL_PERSISTENT_COLLAPSE is consistently reversible at depth 4.
```

It is deeper inside the collapse basin than `FRAGMENTED_LOCAL_COLLAPSE`.

---

### RECOVERY_RELAPSE_COLLAPSE

```text
minimum_escape_depths = [4, 4, 4, 4, 4]
minimum_escape_depth_mean = 4
minimum_escape_depth_std = 0.0

expected_escape_depth = 4
expected_depth_matched = True

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
```

Interpretation:

```text
RECOVERY_RELAPSE_COLLAPSE is consistently reversible at depth 4.
```

It shares the deeper escape threshold with `GLOBAL_PERSISTENT_COLLAPSE`.

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
FRAGMENTED_LOCAL_COLLAPSE first escapes at depth 3,
but escape examples become much denser at depth 4.
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
GLOBAL_PERSISTENT_COLLAPSE first escapes only at depth 4.
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
RECOVERY_RELAPSE_COLLAPSE first escapes only at depth 4.
```

---

## Variant-Level Result

Every variant preserved the same ordering.

### Variant 0

```text
FRAGMENTED_LOCAL_COLLAPSE:
minimum_escape_depth = 3
target = OSCILLATING_NONPERSISTENT
examples = 1600

GLOBAL_PERSISTENT_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 80

RECOVERY_RELAPSE_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 128
```

### Variant 1

```text
FRAGMENTED_LOCAL_COLLAPSE:
minimum_escape_depth = 3
target = OSCILLATING_NONPERSISTENT
examples = 2112

GLOBAL_PERSISTENT_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 80

RECOVERY_RELAPSE_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 128
```

### Variant 2

```text
FRAGMENTED_LOCAL_COLLAPSE:
minimum_escape_depth = 3
target = OSCILLATING_NONPERSISTENT
examples = 2624

GLOBAL_PERSISTENT_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 80

RECOVERY_RELAPSE_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 128
```

### Variant 3

```text
FRAGMENTED_LOCAL_COLLAPSE:
minimum_escape_depth = 3
target = OSCILLATING_NONPERSISTENT
examples = 3136

GLOBAL_PERSISTENT_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 80

RECOVERY_RELAPSE_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 128
```

### Variant 4

```text
FRAGMENTED_LOCAL_COLLAPSE:
minimum_escape_depth = 3
target = OSCILLATING_NONPERSISTENT
examples = 3648

GLOBAL_PERSISTENT_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 80

RECOVERY_RELAPSE_COLLAPSE:
minimum_escape_depth = 4
target = OSCILLATING_NONPERSISTENT
examples = 128
```

The escape-depth ordering did not change.

---

## Why The Result Is PASS

The experiment required all of the following:

```text
expected_ordering_detected = True
all_depths_stable = True
all_targets_stable = True
all_expected_depths_matched = True
```

All were satisfied.

Therefore:

```text
Status = PASS
```

The test confirms a stable depth-stratification pattern.

---

## Structural Meaning

The collapse basin is not absorbing.

But it is not structureless either.

It has a stable reversibility-depth ordering:

```text
FRAGMENTED_LOCAL_COLLAPSE        depth 3
GLOBAL_PERSISTENT_COLLAPSE       depth 4
RECOVERY_RELAPSE_COLLAPSE        depth 4
```

All escape routes return to:

```text
OSCILLATING_NONPERSISTENT
```

So the measured structure is:

```text
collapse-side class
->
minimum escape depth
->
OSCILLATING_NONPERSISTENT
```

This gives the basin an internal depth profile.

---

## Updated Collapse-Basin Model

The model is now:

```text
noise-like topology
<->
FRAGMENTED_LOCAL_COLLAPSE
  escape depth = 3

noise-like topology
<->
GLOBAL_PERSISTENT_COLLAPSE
  escape depth = 4

noise-like topology
<->
RECOVERY_RELAPSE_COLLAPSE
  escape depth = 4
```

But the return target is not arbitrary.

It is consistently:

```text
OSCILLATING_NONPERSISTENT
```

More precise form:

```text
FRAGMENTED_LOCAL_COLLAPSE
  -> OSCILLATING_NONPERSISTENT at depth 3

GLOBAL_PERSISTENT_COLLAPSE
  -> OSCILLATING_NONPERSISTENT at depth 4

RECOVERY_RELAPSE_COLLAPSE
  -> OSCILLATING_NONPERSISTENT at depth 4
```

---

## Relation To Absorption Depth v0

Absorption Depth v0 produced a `CHECK` because the binary absorbing-state hypothesis failed.

It showed:

```text
all collapse-side classes become reversible under depth 4
```

Escape Depth Stability v0 confirms that this was not accidental.

The ordering is stable under wider variants:

```text
3, 4, 4
```

Therefore the correct interpretation is not:

```text
absorbing vs reversible
```

but:

```text
escape-depth stratification
```

---

## Relation To Basin Escape v0

Basin Escape v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

at depth 3.

Escape Depth Stability v0 confirms that:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

is the shallowest escape class and that the deeper collapse classes require depth 4.

---

## Relation To Basin Entry Stability v0

Basin Entry Stability v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE is the canonical entry state
into the collapse basin.
```

Escape Depth Stability v0 shows:

```text
FRAGMENTED_LOCAL_COLLAPSE is also the shallowest escape state
from the collapse basin.
```

Therefore `FRAGMENTED_LOCAL_COLLAPSE` is the boundary class:

```text
canonical entry state
shallowest escape state
interface between noise-like topology and collapse topology
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO by giving the collapse basin a stable internal profile.

OMNIATEMPO can now represent:

```text
entry depth
escape depth
reversibility threshold
collapse-basin internal depth
```

This moves the temporal topology from a flat class system to a depth-ordered structure.

The key distinction is:

```text
basin membership
```

versus:

```text
basin depth
```

---

## Relation To TDelta

This result supports a future metric such as:

```text
TDelta_escape_depth
```

or:

```text
TΔ_escape_depth
```

Measured values:

```text
TΔ_escape_depth(FRAGMENTED_LOCAL_COLLAPSE) = 3

TΔ_escape_depth(GLOBAL_PERSISTENT_COLLAPSE) = 4

TΔ_escape_depth(RECOVERY_RELAPSE_COLLAPSE) = 4
```

This allows temporal topology to quantify how deep a state is inside the collapse basin.

---

## What This Confirms

This experiment supports:

```text
escape-depth ordering stability detected

collapse basin is not absorbing

collapse basin is stably stratified by reversibility depth

FRAGMENTED_LOCAL_COLLAPSE escapes at depth 3

GLOBAL_PERSISTENT_COLLAPSE escapes at depth 4

RECOVERY_RELAPSE_COLLAPSE escapes at depth 4

all escape targets are OSCILLATING_NONPERSISTENT

escape target stability confirmed

escape depth stability confirmed

expected ordering matched across all five variants
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal escape-depth ordering
real-world recoverability
semantic correctness
causal correctness
optimal mutation model
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates controlled synthetic escape-depth ordering stability under the tested mutation space.

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
escape-depth ordering stability
from collapse-side topology
back to noise-like topology
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

The base trajectories were synthetic.

The mutation graph was deterministic.

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

Higher mutation depths may expose further structure.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Escape-Depth Ordering Stability
```

Reason:

```text
variant_count = 5

max_mutation_depth = 4

expected_ordering_detected = True

all_depths_stable = True

all_targets_stable = True

all_expected_depths_matched = True

FRAGMENTED_LOCAL_COLLAPSE escape_depth = 3

GLOBAL_PERSISTENT_COLLAPSE escape_depth = 4

RECOVERY_RELAPSE_COLLAPSE escape_depth = 4

all classes escape toward OSCILLATING_NONPERSISTENT
```

This is a successful controlled escape-depth ordering stability experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_reversibility_index_v0.py
```

Purpose:

```text
measure a normalized reversibility index for each temporal topology class
```

Main question:

```text
which collapse-side class is most reversible,
and how does reversibility compare across basin depth?
```

Required checks:

```text
minimum escape depth

escape example density

escape target stability

depth-normalized reversibility

class ranking

ordering stability
```

Expected structural value:

```text
collapse-basin reversibility ranking
```

---

## Final Result

```text
PASS — escape-depth ordering stability detected.
```

Correct final conclusion:

```text
collapse basin is not absorbing;
it is stably stratified by reversibility depth.
```