# Temporal Collapse Topology Basin Entry v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Basin Entry Measurement
```

---

## Purpose

This experiment measures whether there is a stable entry state into the confirmed-collapse topology basin.

Previous experiments established:

```text
temporal topology classes exist
transition graph exists
transition graph remains mostly stable
attractor and basin structure exists
FRAGMENTED_LOCAL_COLLAPSE behaves as attractor / basin / bridge candidate
```

This experiment asks the sharper question:

```text
is FRAGMENTED_LOCAL_COLLAPSE the canonical entry state
into confirmed-collapse topology?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates basin-entry structure inside the temporal collapse topology graph.

---

## Experiment File

```text
examples/temporal_collapse_topology_basin_entry_v0.py
```

Result file:

```text
results/temporal_collapse_topology_basin_entry_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_basin_entry_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

variant_count = 3
node_count = 6

confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4

max_mutation_depth = 2

entry_count_values = [4, 3, 3]
mean_entry_count = 3.3333333333333335
entry_count_std = 0.4714045207910317

dominant_entry_values =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE
]

dominant_entry_stable = True
fragmented_local_entry_dominant = True

fully_persistent_entry_count = 3
partial_entry_count = 1

target_frequency =
{
  FRAGMENTED_LOCAL_COLLAPSE: 9,
  RECOVERY_RELAPSE_COLLAPSE: 1
}

target_example_totals =
{
  FRAGMENTED_LOCAL_COLLAPSE: 813,
  RECOVERY_RELAPSE_COLLAPSE: 2
}
```

The experiment passed.

`FRAGMENTED_LOCAL_COLLAPSE` behaved as the dominant basin-entry state into confirmed-collapse topology.

---

## Component Partition

The experiment separates topology classes into two macro-components.

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

The experiment measures transitions from:

```text
NOISE_COMPONENT
```

into:

```text
COLLAPSE_COMPONENT
```

---

## Main Finding

The central result is:

```text
fragmented_local_entry_dominant = True
```

and:

```text
dominant_entry_stable = True
```

This means:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

was the dominant entry target in every tested variant.

Correct conclusion:

```text
confirmed-collapse topology has a measurable basin-entry state
```

---

## Fully Persistent Basin Entries

Three basin-entry paths persisted across all variants:

```text
CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE

SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE

OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
```

All three had:

```text
persistence_rate = 1.0
entry_depth_std = 0.0
```

This is the strongest part of the result.

It means every noise-side source class had a stable entry route into the confirmed-collapse basin through:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

---

## Entry Stability

### CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE

```text
present_variant_count = 3
persistence_rate = 1.0

entry_depths = [2, 2, 2]
entry_depth_mean = 2
entry_depth_std = 0.0

example_counts = [11, 15, 19]
example_count_mean = 15
```

Interpretation:

```text
CLEAN_PASS requires depth 2 to enter confirmed-collapse topology
through FRAGMENTED_LOCAL_COLLAPSE.
```

This is stable across tested variants.

---

### SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE

```text
present_variant_count = 3
persistence_rate = 1.0

entry_depths = [1, 1, 1]
entry_depth_mean = 1
entry_depth_std = 0.0

example_counts = [48, 68, 88]
example_count_mean = 68
```

Interpretation:

```text
SPIKE_FILTERED is one mutation away
from FRAGMENTED_LOCAL_COLLAPSE.
```

This confirms spike instability is close to local confirmed collapse.

---

### OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE

```text
present_variant_count = 3
persistence_rate = 1.0

entry_depths = [1, 1, 1]
entry_depth_mean = 1
entry_depth_std = 0.0

example_counts = [136, 188, 240]
example_count_mean = 188
```

Interpretation:

```text
OSCILLATING_NONPERSISTENT is one mutation away
from FRAGMENTED_LOCAL_COLLAPSE.
```

This is the densest persistent entry route.

It produced the largest number of examples.

---

## Weak Alternative Entry

One alternative entry appeared:

```text
OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
```

Metrics:

```text
present_variant_count = 1
persistence_rate = 0.3333333333333333

entry_depths = [2]
entry_depth_mean = 2
entry_depth_std = 0.0

example_counts = [2]
example_count_mean = 2
```

Interpretation:

```text
OSCILLATING_NONPERSISTENT can occasionally jump directly
into RECOVERY_RELAPSE_COLLAPSE,
but this path is weak and not stable.
```

This alternative does not challenge the dominant basin-entry result.

It confirms that direct relapse entry is possible but rare under the tested mutation structure.

---

## Source Entry Stability

### CLEAN_PASS

```text
targets_by_variant =
[
  [FRAGMENTED_LOCAL_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE]
]

unique_targets =
[
  FRAGMENTED_LOCAL_COLLAPSE
]

target_count_by_variant = [1, 1, 1]
```

Interpretation:

```text
CLEAN_PASS has exactly one stable basin-entry target:
FRAGMENTED_LOCAL_COLLAPSE.
```

---

### SPIKE_FILTERED

```text
targets_by_variant =
[
  [FRAGMENTED_LOCAL_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE]
]

unique_targets =
[
  FRAGMENTED_LOCAL_COLLAPSE
]

target_count_by_variant = [1, 1, 1]
```

Interpretation:

```text
SPIKE_FILTERED has exactly one stable basin-entry target:
FRAGMENTED_LOCAL_COLLAPSE.
```

---

### OSCILLATING_NONPERSISTENT

```text
targets_by_variant =
[
  [FRAGMENTED_LOCAL_COLLAPSE, RECOVERY_RELAPSE_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE]
]

unique_targets =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE
]

target_count_by_variant = [2, 1, 1]
```

Interpretation:

```text
OSCILLATING_NONPERSISTENT has one stable entry target
and one weak alternative target.
```

The stable target is:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

The weak alternative is:

```text
RECOVERY_RELAPSE_COLLAPSE
```

---

## Variant-Level Results

### Variant 0

```text
entry_count = 4
dominant_entry = FRAGMENTED_LOCAL_COLLAPSE

target_counts =
{
  FRAGMENTED_LOCAL_COLLAPSE: 3,
  RECOVERY_RELAPSE_COLLAPSE: 1
}

target_examples =
{
  FRAGMENTED_LOCAL_COLLAPSE: 195,
  RECOVERY_RELAPSE_COLLAPSE: 2
}
```

Variant 0 contains the weak alternative entry:

```text
OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
```

But the dominant entry remains:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

---

### Variant 1

```text
entry_count = 3
dominant_entry = FRAGMENTED_LOCAL_COLLAPSE

target_counts =
{
  FRAGMENTED_LOCAL_COLLAPSE: 3
}

target_examples =
{
  FRAGMENTED_LOCAL_COLLAPSE: 271
}
```

Variant 1 has only the canonical basin-entry target.

---

### Variant 2

```text
entry_count = 3
dominant_entry = FRAGMENTED_LOCAL_COLLAPSE

target_counts =
{
  FRAGMENTED_LOCAL_COLLAPSE: 3
}

target_examples =
{
  FRAGMENTED_LOCAL_COLLAPSE: 347
}
```

Variant 2 also has only the canonical basin-entry target.

---

## Structural Meaning

This experiment shows that:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

is not merely a class label.

It acts as:

```text
the dominant measurable entry state
into confirmed-collapse topology
```

From every noise-side class, the stable route into the collapse component points to:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

This makes `FRAGMENTED_LOCAL_COLLAPSE` structurally special.

It is:

```text
local confirmation
before global persistence
```

and therefore behaves as the first stable contact point with confirmed-collapse topology.

---

## Why This Matters

Earlier experiments showed that temporal collapse topology has:

```text
classes
thresholds
transition graph
stable components
attractor basin
bridge structure
```

This experiment adds:

```text
basin-entry state
```

That is stronger than saying:

```text
collapse component exists
```

It says:

```text
there is a measurable entry class into the collapse component
```

This is a useful structural layer.

---

## Relation To Bridge Stability v0

Bridge Stability v0 found that:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

was the stable single dominant bridge under the cross-component bridge metric.

Basin Entry v0 confirms and sharpens that result.

It shows that `FRAGMENTED_LOCAL_COLLAPSE` is not only bridge-like.

It is specifically the dominant entry target from the noise component into the collapse component.

Correct sequence:

```text
bridge stability
->
basin entry measurement
```

---

## Relation To Attractor v0

Attractor v0 found:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

as:

```text
strongest attractor candidate
strongest basin candidate
```

Basin Entry v0 adds:

```text
dominant entry state
```

So the current structural role of `FRAGMENTED_LOCAL_COLLAPSE` is:

```text
attractor candidate
basin candidate
bridge interface
basin-entry state
```

This convergence is important.

---

## Relation To Transition Graph Stability v0

Transition Graph Stability v0 showed that the topology graph remained stable under shifted trajectory variants.

Basin Entry v0 shows that the entry into the collapse component also remains stable.

So the validation path is:

```text
transition graph stable
->
attractor basin stable
->
basin entry stable
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO by adding a concrete basin-entry concept.

OMNIATEMPO can now distinguish:

```text
noise-side instability
basin-entry state
confirmed-collapse basin
global-persistence topology
recovery-relapse topology
```

This creates a more detailed temporal phase-space.

The key new state is:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

as:

```text
entry into confirmed-collapse topology
```

---

## Relation To TDelta

This result is directly relevant to future TDelta work.

A future temporal divergence measure can define:

```text
TΔ_basin_entry
```

as the time or mutation depth required to enter:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

This is cleaner than using generic collapse labels.

It allows a more precise distinction between:

```text
transient instability
```

and:

```text
confirmed-collapse basin entry
```

---

## What This Confirms

This experiment supports:

```text
confirmed-collapse topology has a measurable basin-entry state

FRAGMENTED_LOCAL_COLLAPSE is the dominant entry target

dominant_entry_stable = True

fragmented_local_entry_dominant = True

all noise-side classes have stable entry into FRAGMENTED_LOCAL_COLLAPSE

CLEAN_PASS enters FRAGMENTED_LOCAL_COLLAPSE at depth 2

SPIKE_FILTERED enters FRAGMENTED_LOCAL_COLLAPSE at depth 1

OSCILLATING_NONPERSISTENT enters FRAGMENTED_LOCAL_COLLAPSE at depth 1

the alternative RECOVERY_RELAPSE_COLLAPSE entry is weak and variant-sensitive
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal basin-entry structure
real-world temporal reliability
semantic correctness
causal correctness
optimal mutation model
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates a controlled synthetic basin-entry measurement.

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
basin-entry dominance
from noise-like temporal topology
into confirmed-collapse topology
```

---

## Limitations

```text
Only three variants were tested.

Only six topology classes were tested.

Only mutation depths 1 and 2 were searched.

Only three frame values were allowed:
PASS
ESCALATE
COLLAPSE

The base trajectories were synthetic.

The mutation graph was deterministic.

No probabilistic transition model was used.

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
Level 2 — Temporal Topology Basin Entry Measurement
```

Reason:

```text
dominant_entry_stable = True

fragmented_local_entry_dominant = True

fully_persistent_entry_count = 3

CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE persisted in all variants

SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE persisted in all variants

OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE persisted in all variants

target_example_totals strongly favored FRAGMENTED_LOCAL_COLLAPSE

FRAGMENTED_LOCAL_COLLAPSE examples = 813

RECOVERY_RELAPSE_COLLAPSE examples = 2
```

This is a successful controlled basin-entry experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_basin_entry_stability_v0.py
```

Purpose:

```text
stress-test whether FRAGMENTED_LOCAL_COLLAPSE remains the canonical basin-entry state
under wider trajectory lengths, shifted collapse positions, and expanded mutation search.
```

Main question:

```text
does basin-entry dominance remain stable
when the experimental space is widened?
```

Required checks:

```text
more variants per source class

larger trajectory lengths

entry depth 1, 2, and 3

entry frequency stability

entry target dominance

alternative entry suppression

source-specific entry profiles
```

Expected structural value:

```text
basin-entry invariance
```

---

## Final Result

```text
PASS — FRAGMENTED_LOCAL_COLLAPSE behaved as the dominant basin-entry state into confirmed-collapse topology.
```

Correct final conclusion:

```text
confirmed-collapse topology has a measurable basin-entry state:
FRAGMENTED_LOCAL_COLLAPSE.
```