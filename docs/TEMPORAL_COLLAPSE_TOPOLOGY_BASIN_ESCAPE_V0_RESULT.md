# Temporal Collapse Topology Basin Escape v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Basin Escape Measurement
```

---

## Purpose

This experiment tests whether confirmed-collapse topology behaves as an absorbing basin under controlled mutations.

Previous experiments established:

```text
confirmed-collapse topology has a measurable basin-entry state

FRAGMENTED_LOCAL_COLLAPSE is the canonical basin-entry state

basin-entry invariance was detected under widened variants and mutation depth 3
```

This experiment asks the opposite question:

```text
can confirmed-collapse topology escape back into noise-like topology?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates basin-escape structure inside the temporal collapse topology graph.

---

## Experiment File

```text
examples/temporal_collapse_topology_basin_escape_v0.py
```

Result file:

```text
results/temporal_collapse_topology_basin_escape_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_basin_escape_v0.py
```

---

## Summary Result

```text
Status: CHECK
Version: 0.1.0

variant_count = 5
node_count = 6

confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4

max_mutation_depth = 3

escape_count_values = [1, 1, 1, 1, 1]
mean_escape_count = 1
escape_count_std = 0.0

fully_persistent_escape_count = 1
partial_escape_count = 0

total_escape_path_count = 1
total_escape_example_count = 320

fully_persistent_escapes =
[
  FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
]

dominant_escape_values =
[
  OSCILLATING_NONPERSISTENT,
  OSCILLATING_NONPERSISTENT,
  OSCILLATING_NONPERSISTENT,
  OSCILLATING_NONPERSISTENT,
  OSCILLATING_NONPERSISTENT
]

dominant_escape_stable = True

absorbing_basin_score = 0.5

strong_absorption = False
weak_absorption = False
```

The result is `CHECK`.

The confirmed-collapse basin exposed a stable escape path back to noise-like topology.

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

The experiment measures transitions from:

```text
COLLAPSE_COMPONENT
```

back into:

```text
NOISE_COMPONENT
```

---

## Main Finding

The central finding is:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

This escape path was present in every tested variant.

```text
present_variant_count = 5
persistence_rate = 1.0

escape_depths = [3, 3, 3, 3, 3]
escape_depth_mean = 3
escape_depth_std = 0.0

example_counts = [64, 64, 64, 64, 64]
example_count_total = 320
```

Correct conclusion:

```text
confirmed-collapse basin is not fully absorbing
```

More precise conclusion:

```text
the basin-entry state is reversible at depth 3,
while deeper collapse states remained absorbing under tested mutations
```

---

## Escape Stability

Only one escape path was found:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

It is fully persistent:

```text
persistence_rate = 1.0
```

It has stable depth:

```text
escape_depth_std = 0.0
```

It has stable example count across variants:

```text
example_counts = [64, 64, 64, 64, 64]
```

This means the escape is not noise from one trajectory variant.

It is structurally repeatable under the tested mutation space.

---

## Source Escape Stability

### FRAGMENTED_LOCAL_COLLAPSE

```text
targets_by_variant =
[
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT],
  [OSCILLATING_NONPERSISTENT]
]

unique_targets =
[
  OSCILLATING_NONPERSISTENT
]

target_count_by_variant = [1, 1, 1, 1, 1]

minimum_escape_depth = 3
mean_escape_depth = 3
```

Interpretation:

```text
FRAGMENTED_LOCAL_COLLAPSE has a stable escape route
back to OSCILLATING_NONPERSISTENT at mutation depth 3.
```

This makes `FRAGMENTED_LOCAL_COLLAPSE` reversible under the tested conditions.

---

### GLOBAL_PERSISTENT_COLLAPSE

```text
targets_by_variant =
[
  [],
  [],
  [],
  [],
  []
]

unique_targets = []

target_count_by_variant = [0, 0, 0, 0, 0]

minimum_escape_depth = None
mean_escape_depth = None
```

Interpretation:

```text
GLOBAL_PERSISTENT_COLLAPSE exposed no escape path
back to noise-like topology under mutation depth <= 3.
```

It behaved as absorbing under the tested mutation space.

---

### RECOVERY_RELAPSE_COLLAPSE

```text
targets_by_variant =
[
  [],
  [],
  [],
  [],
  []
]

unique_targets = []

target_count_by_variant = [0, 0, 0, 0, 0]

minimum_escape_depth = None
mean_escape_depth = None
```

Interpretation:

```text
RECOVERY_RELAPSE_COLLAPSE exposed no escape path
back to noise-like topology under mutation depth <= 3.
```

It also behaved as absorbing under the tested mutation space.

---

## Variant-Level Result

Every variant produced the same escape result.

### Variant 0

```text
escape_count = 1
dominant_escape = OSCILLATING_NONPERSISTENT
target_examples =
{
  OSCILLATING_NONPERSISTENT: 64
}
```

### Variant 1

```text
escape_count = 1
dominant_escape = OSCILLATING_NONPERSISTENT
target_examples =
{
  OSCILLATING_NONPERSISTENT: 64
}
```

### Variant 2

```text
escape_count = 1
dominant_escape = OSCILLATING_NONPERSISTENT
target_examples =
{
  OSCILLATING_NONPERSISTENT: 64
}
```

### Variant 3

```text
escape_count = 1
dominant_escape = OSCILLATING_NONPERSISTENT
target_examples =
{
  OSCILLATING_NONPERSISTENT: 64
}
```

### Variant 4

```text
escape_count = 1
dominant_escape = OSCILLATING_NONPERSISTENT
target_examples =
{
  OSCILLATING_NONPERSISTENT: 64
}
```

This is a stable escape pattern, not a variant-specific accident.

---

## Why The Result Is CHECK

The experiment tested whether the confirmed-collapse basin behaves as absorbing.

The result found a fully persistent escape path:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

Therefore:

```text
strong_absorption = False
weak_absorption = False
```

The basin is not fully absorbing.

So the correct result is:

```text
CHECK
```

This CHECK is structurally useful.

It identifies the exact reversible part of the collapse basin.

---

## Structural Meaning

The confirmed-collapse basin is not homogeneous.

It separates into two different subregions:

```text
reversible basin-entry state
```

and:

```text
deeper absorbing collapse states
```

Specifically:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

is reversible at depth 3.

But:

```text
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

showed no escape back to noise-like topology under the tested mutation space.

Therefore the topology is better described as:

```text
noise-like topology
->
FRAGMENTED_LOCAL_COLLAPSE
<-> 
OSCILLATING_NONPERSISTENT

FRAGMENTED_LOCAL_COLLAPSE
->
GLOBAL_PERSISTENT_COLLAPSE / RECOVERY_RELAPSE_COLLAPSE
```

The entry state is not final collapse.

It is a reversible interface.

---

## Updated Interpretation of FRAGMENTED_LOCAL_COLLAPSE

Previous experiments showed `FRAGMENTED_LOCAL_COLLAPSE` as:

```text
attractor candidate
basin candidate
bridge interface
dominant basin-entry state
canonical basin-entry state
```

This experiment adds:

```text
reversible basin-entry state
```

So the updated structural role is:

```text
FRAGMENTED_LOCAL_COLLAPSE is the canonical entry state,
but not an absorbing state.
```

It is the interface between:

```text
noise-like instability
```

and:

```text
deeper confirmed-collapse dynamics
```

---

## Relation To Basin Entry Stability v0

Basin Entry Stability v0 found:

```text
FRAGMENTED_LOCAL_COLLAPSE remains the canonical basin-entry state
under widened trajectory variants and mutation depth up to 3.
```

Basin Escape v0 now shows:

```text
the canonical entry state can escape back to OSCILLATING_NONPERSISTENT
at depth 3.
```

Together:

```text
FRAGMENTED_LOCAL_COLLAPSE is a stable entry interface,
not an absorbing endpoint.
```

This is more precise than treating all collapse classes as equivalent.

---

## Relation To Attractor v0

Attractor v0 identified the confirmed-collapse component as attractor-like.

Basin Escape v0 refines that result.

The collapse component is attractor-like at the component level, but not every node inside it is absorbing.

The component contains:

```text
reversible entry topology
```

and:

```text
absorbing deeper-collapse topology
```

This is a stronger structural interpretation.

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO by adding internal structure to the collapse basin.

OMNIATEMPO can now distinguish:

```text
noise-like region
basin-entry interface
reversible collapse entry
deeper absorbing collapse states
```

The relevant structure is:

```text
OSCILLATING_NONPERSISTENT
<->
FRAGMENTED_LOCAL_COLLAPSE
```

at the basin boundary.

This is a temporal topology result, not a semantic statement.

---

## Relation To TDelta

This result is important for future TDelta definitions.

There should not be only one generic collapse time.

A better future decomposition is:

```text
TΔ_entry
TΔ_escape
TΔ_absorption
```

Where:

```text
TΔ_entry
```

measures time or mutation distance into:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

```text
TΔ_escape
```

measures return distance from:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

to:

```text
OSCILLATING_NONPERSISTENT
```

```text
TΔ_absorption
```

measures entry into deeper states with no observed escape under the tested mutation space:

```text
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

---

## What This Confirms

This experiment supports:

```text
confirmed-collapse basin is not fully absorbing

FRAGMENTED_LOCAL_COLLAPSE has a stable escape path

FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT persists across all variants

escape depth is stable at 3

escape_depth_std = 0.0

GLOBAL_PERSISTENT_COLLAPSE exposed no escape path

RECOVERY_RELAPSE_COLLAPSE exposed no escape path

basin-entry state is reversible

deeper collapse states remained absorbing under tested mutations
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal basin escape behavior
real-world recoverability
semantic correctness
causal correctness
optimal mutation model
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates a controlled synthetic basin-escape measurement under mutation depth up to 3.

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
escape paths from confirmed-collapse topology
back to noise-like topology
under controlled mutation search
```

---

## Limitations

```text
Only five variants were tested.

Only three collapse-side source classes were tested.

Only mutation depths 1, 2, and 3 were searched.

Only three frame values were allowed:
PASS
ESCALATE
COLLAPSE

The base trajectories were synthetic.

The mutation graph was deterministic.

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

Higher mutation depths may expose additional escape paths.
```

---

## Result Classification

Recommended classification:

```text
CHECK
```

Evidence level:

```text
Level 2 — Temporal Topology Basin Escape Measurement
```

Reason:

```text
the absorbing-basin hypothesis was falsified

fully_persistent_escape_count = 1

FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT persisted in all 5 variants

persistence_rate = 1.0

escape_depths = [3, 3, 3, 3, 3]

escape_depth_std = 0.0

example_count_total = 320

GLOBAL_PERSISTENT_COLLAPSE had no observed escape

RECOVERY_RELAPSE_COLLAPSE had no observed escape
```

This is a useful CHECK.

It reveals that the basin-entry state is reversible while deeper collapse states remained absorbing under the tested mutation space.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_absorption_depth_v0.py
```

Purpose:

```text
measure the mutation depth at which each collapse-side class becomes absorbing or reversible
```

Main question:

```text
where is the boundary between reversible basin-entry topology
and absorbing collapse topology?
```

Required checks:

```text
absorption depth for FRAGMENTED_LOCAL_COLLAPSE

absorption depth for GLOBAL_PERSISTENT_COLLAPSE

absorption depth for RECOVERY_RELAPSE_COLLAPSE

escape depth distribution

escape target distribution

reversibility index

absorbing-state index
```

Expected structural value:

```text
collapse-basin internal stratification
```

---

## Final Result

```text
CHECK — confirmed-collapse basin exposed a stable escape path back to noise-like topology.
```

Correct final conclusion:

```text
the basin-entry state is reversible at depth 3,
while deeper collapse states remained absorbing under tested mutations.
```