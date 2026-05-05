# Temporal Collapse Topology Absorption Depth v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Absorption Depth Measurement
```

---

## Purpose

This experiment measures the mutation depth at which each collapse-side topology class can escape back to noise-like topology.

The previous experiment showed:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

at mutation depth 3.

This experiment widens the search to:

```text
mutation depth <= 4
```

and asks:

```text
are deeper collapse states absorbing,
or do they also become reversible at larger mutation depth?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates absorption depth and reversibility threshold inside the temporal collapse topology graph.

---

## Experiment File

```text
examples/temporal_collapse_topology_absorption_depth_v0.py
```

Result file:

```text
results/temporal_collapse_topology_absorption_depth_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_absorption_depth_v0.py
```

---

## Summary Result

```text
Status: CHECK
Version: 0.1.0

variant_count = 3
node_count = 6

confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4

max_mutation_depth = 4

reversible_classes =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  GLOBAL_PERSISTENT_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE
]

absorbing_classes = []

stratification_detected = False

fragmented_min_escape_depth = 3
global_persistent_min_escape_depth = 4
recovery_relapse_min_escape_depth = 4
```

The result is `CHECK`.

The original hypothesis was not confirmed.

The correct conclusion is:

```text
collapse basin is not absorbing;
it is depth-stratified by reversibility threshold.
```

---

## Initial Hypothesis

The working hypothesis was:

```text
FRAGMENTED_LOCAL_COLLAPSE is reversible

GLOBAL_PERSISTENT_COLLAPSE remains absorbing

RECOVERY_RELAPSE_COLLAPSE remains absorbing
```

The observed result was:

```text
FRAGMENTED_LOCAL_COLLAPSE escapes at depth 3

GLOBAL_PERSISTENT_COLLAPSE escapes at depth 4

RECOVERY_RELAPSE_COLLAPSE escapes at depth 4
```

Therefore the hypothesis:

```text
deeper collapse states are absorbing
```

was falsified under mutation depth up to 4.

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

The experiment measures escapes from:

```text
COLLAPSE_COMPONENT
```

back into:

```text
NOISE_COMPONENT
```

---

## Main Finding

All collapse-side classes escaped toward the same noise-side target:

```text
OSCILLATING_NONPERSISTENT
```

Escape depths:

```text
FRAGMENTED_LOCAL_COLLAPSE        -> OSCILLATING_NONPERSISTENT at depth 3

GLOBAL_PERSISTENT_COLLAPSE       -> OSCILLATING_NONPERSISTENT at depth 4

RECOVERY_RELAPSE_COLLAPSE        -> OSCILLATING_NONPERSISTENT at depth 4
```

This means the collapse basin is not strictly absorbing under the tested mutation space.

It has an internal reversibility-depth structure.

---

## Class Absorption Summary

### FRAGMENTED_LOCAL_COLLAPSE

```text
absorbing_rate = 0.0
reversible_rate = 1.0

minimum_escape_depths = [3, 3, 3]
minimum_observed_escape_depth = 3
mean_minimum_escape_depth = 3
escape_depth_std = 0.0

unique_escape_targets =
[
  OSCILLATING_NONPERSISTENT
]

total_escape_examples = 6336

depth_hit_counts =
{
  1: 0,
  2: 0,
  3: 3,
  4: 3
}

depth_example_totals =
{
  1: 0,
  2: 0,
  3: 192,
  4: 6144
}

reversibility_index = 0.3333333333333333
absorbing_state_index = 0.00015780337699226762
```

Interpretation:

```text
FRAGMENTED_LOCAL_COLLAPSE is the closest collapse-side class to escape.
```

It escapes at mutation depth 3.

This confirms its role as a reversible basin-entry interface.

---

### GLOBAL_PERSISTENT_COLLAPSE

```text
absorbing_rate = 0.0
reversible_rate = 1.0

minimum_escape_depths = [4, 4, 4]
minimum_observed_escape_depth = 4
mean_minimum_escape_depth = 4
escape_depth_std = 0.0

unique_escape_targets =
[
  OSCILLATING_NONPERSISTENT
]

total_escape_examples = 240

depth_hit_counts =
{
  1: 0,
  2: 0,
  3: 0,
  4: 3
}

depth_example_totals =
{
  1: 0,
  2: 0,
  3: 0,
  4: 240
}

reversibility_index = 0.25
absorbing_state_index = 0.004149377593360996
```

Interpretation:

```text
GLOBAL_PERSISTENT_COLLAPSE is not absorbing under depth <= 4.
```

It requires deeper mutation than `FRAGMENTED_LOCAL_COLLAPSE` to escape.

Its escape threshold is:

```text
minimum_escape_depth = 4
```

---

### RECOVERY_RELAPSE_COLLAPSE

```text
absorbing_rate = 0.0
reversible_rate = 1.0

minimum_escape_depths = [4, 4, 4]
minimum_observed_escape_depth = 4
mean_minimum_escape_depth = 4
escape_depth_std = 0.0

unique_escape_targets =
[
  OSCILLATING_NONPERSISTENT
]

total_escape_examples = 384

depth_hit_counts =
{
  1: 0,
  2: 0,
  3: 0,
  4: 3
}

depth_example_totals =
{
  1: 0,
  2: 0,
  3: 0,
  4: 384
}

reversibility_index = 0.25
absorbing_state_index = 0.0025974025974025974
```

Interpretation:

```text
RECOVERY_RELAPSE_COLLAPSE is not absorbing under depth <= 4.
```

Like `GLOBAL_PERSISTENT_COLLAPSE`, it escapes only at depth 4.

---

## Depth Distribution

### FRAGMENTED_LOCAL_COLLAPSE

```text
depth_hits =
{
  1: 0,
  2: 0,
  3: 3,
  4: 3
}

depth_examples =
{
  1: 0,
  2: 0,
  3: 192,
  4: 6144
}
```

Interpretation:

```text
escape first appears at depth 3,
then becomes much denser at depth 4.
```

---

### GLOBAL_PERSISTENT_COLLAPSE

```text
depth_hits =
{
  1: 0,
  2: 0,
  3: 0,
  4: 3
}

depth_examples =
{
  1: 0,
  2: 0,
  3: 0,
  4: 240
}
```

Interpretation:

```text
escape first appears only at depth 4.
```

---

### RECOVERY_RELAPSE_COLLAPSE

```text
depth_hits =
{
  1: 0,
  2: 0,
  3: 0,
  4: 3
}

depth_examples =
{
  1: 0,
  2: 0,
  3: 0,
  4: 384
}
```

Interpretation:

```text
escape first appears only at depth 4.
```

---

## Variant-Level Result

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

All variants showed the same escape-depth pattern.

---

## Why The Result Is CHECK

The script expected this separation:

```text
FRAGMENTED_LOCAL_COLLAPSE = reversible

GLOBAL_PERSISTENT_COLLAPSE = absorbing

RECOVERY_RELAPSE_COLLAPSE = absorbing
```

But the observed result was:

```text
FRAGMENTED_LOCAL_COLLAPSE = reversible at depth 3

GLOBAL_PERSISTENT_COLLAPSE = reversible at depth 4

RECOVERY_RELAPSE_COLLAPSE = reversible at depth 4
```

Therefore:

```text
stratification_detected = False
```

because the test’s binary stratification condition was not met.

However, the experiment still revealed a real structural stratification:

```text
reversible at depth 3
vs
reversible at depth 4
```

So the `CHECK` is useful.

It means:

```text
the expected absorbing split was wrong,
but a reversibility-depth split was measured.
```

---

## Structural Meaning

The collapse basin is not absorbing under the tested mutation space.

It has a depth-stratified reversibility structure:

```text
FRAGMENTED_LOCAL_COLLAPSE
  escape depth = 3

GLOBAL_PERSISTENT_COLLAPSE
  escape depth = 4

RECOVERY_RELAPSE_COLLAPSE
  escape depth = 4
```

This means:

```text
FRAGMENTED_LOCAL_COLLAPSE is closer to escape.

GLOBAL_PERSISTENT_COLLAPSE and RECOVERY_RELAPSE_COLLAPSE require deeper mutation to escape.

All collapse-side classes escape toward OSCILLATING_NONPERSISTENT under depth <= 4.
```

The correct topology is not:

```text
reversible entry state
vs
absorbing deep states
```

The correct topology is:

```text
shallower reversible state
vs
deeper reversible states
```

---

## Updated Collapse-Basin Model

Previous model:

```text
noise-like topology
->
FRAGMENTED_LOCAL_COLLAPSE
->
absorbing deeper collapse states
```

Updated model:

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

All escape targets point to:

```text
OSCILLATING_NONPERSISTENT
```

So `OSCILLATING_NONPERSISTENT` acts as the common noise-side return state.

---

## Relation To Basin Escape v0

Basin Escape v0 found:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

at depth 3.

Absorption Depth v0 extends that result and shows:

```text
GLOBAL_PERSISTENT_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

at depth 4.

and:

```text
RECOVERY_RELAPSE_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

at depth 4.

Therefore Basin Escape v0 was incomplete because it only searched to depth 3.

Absorption Depth v0 shows that deeper collapse states also become reversible when the mutation search is widened to depth 4.

---

## Relation To Basin Entry Stability v0

Basin Entry Stability v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE is the canonical entry state
into the collapse basin.
```

Absorption Depth v0 shows:

```text
FRAGMENTED_LOCAL_COLLAPSE is also the shallowest escape state
from the collapse basin.
```

So `FRAGMENTED_LOCAL_COLLAPSE` remains the boundary/interface class:

```text
entry interface
escape interface
lowest escape-depth collapse class
```

---

## Relation To OMNIATEMPO

This experiment improves OMNIATEMPO by replacing a binary view:

```text
absorbing vs non-absorbing
```

with a graded view:

```text
escape depth
```

The measured structure is:

```text
FRAGMENTED_LOCAL_COLLAPSE: escape depth 3

GLOBAL_PERSISTENT_COLLAPSE: escape depth 4

RECOVERY_RELAPSE_COLLAPSE: escape depth 4
```

This gives OMNIATEMPO a more precise temporal topology layer:

```text
reversibility threshold
```

instead of only:

```text
collapse state
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

A possible definition:

```text
TΔ_escape_depth(class) =
minimum mutation depth required for class to return
to noise-like topology
```

Under this experiment:

```text
TΔ_escape_depth(FRAGMENTED_LOCAL_COLLAPSE) = 3

TΔ_escape_depth(GLOBAL_PERSISTENT_COLLAPSE) = 4

TΔ_escape_depth(RECOVERY_RELAPSE_COLLAPSE) = 4
```

This is useful because it quantifies how deep a collapse-side class is inside the basin.

---

## What This Confirms

This experiment supports:

```text
collapse basin is not absorbing under depth <= 4

all collapse-side classes are reversible under depth <= 4

all collapse-side classes escape toward OSCILLATING_NONPERSISTENT

FRAGMENTED_LOCAL_COLLAPSE has minimum escape depth 3

GLOBAL_PERSISTENT_COLLAPSE has minimum escape depth 4

RECOVERY_RELAPSE_COLLAPSE has minimum escape depth 4

FRAGMENTED_LOCAL_COLLAPSE is closer to escape

GLOBAL_PERSISTENT_COLLAPSE and RECOVERY_RELAPSE_COLLAPSE require deeper mutation to escape

escape-depth stratification was measured
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal escape-depth structure
real-world recoverability
semantic correctness
causal correctness
optimal mutation model
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates controlled synthetic absorption-depth measurement under mutation depth up to 4.

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
escape-depth threshold
from collapse-side topology
back to noise-like topology
under controlled mutation search
```

---

## Limitations

```text
Only three variants were tested.

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

Higher mutation depths may expose more escape paths or change density.
```

---

## Result Classification

Recommended classification:

```text
CHECK
```

Evidence level:

```text
Level 2 — Temporal Topology Absorption Depth Measurement
```

Reason:

```text
the binary absorbing-state hypothesis was falsified

all collapse-side classes became reversible under mutation depth <= 4

FRAGMENTED_LOCAL_COLLAPSE escaped at depth 3

GLOBAL_PERSISTENT_COLLAPSE escaped at depth 4

RECOVERY_RELAPSE_COLLAPSE escaped at depth 4

all escape targets were OSCILLATING_NONPERSISTENT

stratification_detected = False only because the expected binary split failed

a different stratification was measured:
depth 3 vs depth 4 reversibility
```

This is a useful CHECK.

It replaces the previous absorbing-basin model with a depth-stratified reversibility model.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_escape_depth_stability_v0.py
```

Purpose:

```text
test whether the escape-depth ordering remains stable
under wider trajectory variants
```

Main question:

```text
is the ordering FRAGMENTED_LOCAL_COLLAPSE at depth 3
and deeper collapse states at depth 4 stable?
```

Required checks:

```text
more variants per collapse class

longer trajectories

shifted collapse positions

escape depth 1..4

escape target stability

escape example-density stability

escape-depth ordering stability
```

Expected structural value:

```text
escape-depth ordering stability
```

---

## Final Result

```text
CHECK — all collapse-side classes became reversible under mutation depth up to 4.
```

Correct final conclusion:

```text
collapse basin is not absorbing;
it is depth-stratified by reversibility threshold.
```