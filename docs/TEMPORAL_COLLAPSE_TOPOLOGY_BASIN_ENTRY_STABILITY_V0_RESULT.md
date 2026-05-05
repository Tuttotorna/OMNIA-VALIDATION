# Temporal Collapse Topology Basin Entry Stability v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Basin Entry Invariance
```

---

## Purpose

This experiment stress-tests whether `FRAGMENTED_LOCAL_COLLAPSE` remains the canonical basin-entry state under a wider experimental space.

The previous experiment showed:

```text
FRAGMENTED_LOCAL_COLLAPSE behaves as the dominant basin-entry state
```

This experiment widens the test space by using:

```text
5 trajectory variants
larger trajectory lengths
shifted collapse positions
mutation depth up to 3
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates basin-entry invariance inside the temporal collapse topology graph.

---

## Experiment File

```text
examples/temporal_collapse_topology_basin_entry_stability_v0.py
```

Result file:

```text
results/temporal_collapse_topology_basin_entry_stability_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_basin_entry_stability_v0.py
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

max_mutation_depth = 3

entry_count_values = [6, 5, 5, 5, 5]
mean_entry_count = 5.2
entry_count_std = 0.4

dominant_entry_values =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE
]

dominant_entry_stable = True
fragmented_local_entry_dominant = True
canonical_entries_present = True

target_example_totals =
{
  FRAGMENTED_LOCAL_COLLAPSE: 38687,
  GLOBAL_PERSISTENT_COLLAPSE: 24,
  RECOVERY_RELAPSE_COLLAPSE: 88
}

fragmented_to_relapse_example_ratio = 439.625
```

The experiment passed.

The result is:

```text
basin-entry invariance detected
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

The experiment measures basin-entry paths from the noise component into the collapse component.

---

## Main Finding

The central result is:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

remained the dominant basin-entry class across all five variants.

```text
dominant_entry_values =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE
]
```

Therefore:

```text
dominant_entry_stable = True
fragmented_local_entry_dominant = True
```

Correct conclusion:

```text
FRAGMENTED_LOCAL_COLLAPSE is the canonical basin-entry state
under the tested widened mutation space.
```

---

## Canonical Entries

The canonical entries were:

```text
CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE

SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE

OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
```

All canonical entries were present.

```text
canonical_entries_present = True
```

This means every noise-side class had a persistent route into the collapse basin through:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

---

## Fully Persistent Entries

The experiment found five fully persistent entries:

```text
CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE

SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE

SPIKE_FILTERED -> GLOBAL_PERSISTENT_COLLAPSE

OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE

OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
```

The first three canonical basin-entry observations remain structurally central.

The two secondary entries are real under depth 3, but they are not dominant by example volume.

---

## Partial Entry

One partial entry appeared:

```text
OSCILLATING_NONPERSISTENT -> GLOBAL_PERSISTENT_COLLAPSE
```

Metrics:

```text
present_variant_count = 1
persistence_rate = 0.2
entry_depth = 3
example_count_total = 4
```

Interpretation:

```text
direct entry from oscillation to global persistent collapse is possible
but weak and not stable under shifted variants.
```

---

## Entry Stability Details

### CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE

```text
present_variant_count = 5
persistence_rate = 1.0

entry_depths = [2, 2, 2, 2, 2]
entry_depth_mean = 2
entry_depth_std = 0.0

example_count_total = 3745
```

Interpretation:

```text
CLEAN_PASS consistently enters the collapse basin
through FRAGMENTED_LOCAL_COLLAPSE at depth 2.
```

---

### SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE

```text
present_variant_count = 5
persistence_rate = 1.0

entry_depths = [1, 1, 1, 1, 1]
entry_depth_mean = 1
entry_depth_std = 0.0

example_count_total = 9835
```

Interpretation:

```text
SPIKE_FILTERED is consistently one mutation away
from FRAGMENTED_LOCAL_COLLAPSE.
```

---

### OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE

```text
present_variant_count = 5
persistence_rate = 1.0

entry_depths = [1, 1, 1, 1, 1]
entry_depth_mean = 1
entry_depth_std = 0.0

example_count_total = 25107
```

Interpretation:

```text
OSCILLATING_NONPERSISTENT is consistently one mutation away
from FRAGMENTED_LOCAL_COLLAPSE.
```

This is the strongest entry route by example volume.

---

### SPIKE_FILTERED -> GLOBAL_PERSISTENT_COLLAPSE

```text
present_variant_count = 5
persistence_rate = 1.0

entry_depths = [3, 3, 3, 3, 3]
entry_depth_mean = 3
entry_depth_std = 0.0

example_count_total = 20
```

Interpretation:

```text
SPIKE_FILTERED can reach GLOBAL_PERSISTENT_COLLAPSE at depth 3,
but this path is sparse compared with FRAGMENTED_LOCAL_COLLAPSE.
```

---

### OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE

```text
present_variant_count = 5
persistence_rate = 1.0

entry_depths = [2, 3, 3, 3, 3]
entry_depth_mean = 2.8
entry_depth_std = 0.4

example_count_total = 88
```

Interpretation:

```text
OSCILLATING_NONPERSISTENT can reach RECOVERY_RELAPSE_COLLAPSE,
but this route is much weaker than its entry into FRAGMENTED_LOCAL_COLLAPSE.
```

---

### OSCILLATING_NONPERSISTENT -> GLOBAL_PERSISTENT_COLLAPSE

```text
present_variant_count = 1
persistence_rate = 0.2

entry_depths = [3]
entry_depth_mean = 3
entry_depth_std = 0.0

example_count_total = 4
```

Interpretation:

```text
this is a weak partial entry.
```

It does not challenge the dominance of `FRAGMENTED_LOCAL_COLLAPSE`.

---

## Source Entry Stability

### CLEAN_PASS

```text
targets_by_variant =
[
  [FRAGMENTED_LOCAL_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE]
]

unique_targets =
[
  FRAGMENTED_LOCAL_COLLAPSE
]

minimum_entry_depth = 2
mean_entry_depth = 2
```

Interpretation:

```text
CLEAN_PASS has exactly one stable basin-entry target.
```

---

### SPIKE_FILTERED

```text
targets_by_variant =
[
  [FRAGMENTED_LOCAL_COLLAPSE, GLOBAL_PERSISTENT_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE, GLOBAL_PERSISTENT_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE, GLOBAL_PERSISTENT_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE, GLOBAL_PERSISTENT_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE, GLOBAL_PERSISTENT_COLLAPSE]
]

unique_targets =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  GLOBAL_PERSISTENT_COLLAPSE
]

minimum_entry_depth = 1
mean_entry_depth = 2
```

Interpretation:

```text
SPIKE_FILTERED has two stable targets,
but FRAGMENTED_LOCAL_COLLAPSE is the dominant and closest target.
```

`GLOBAL_PERSISTENT_COLLAPSE` appears only at depth 3 with very low example volume.

---

### OSCILLATING_NONPERSISTENT

```text
targets_by_variant =
[
  [FRAGMENTED_LOCAL_COLLAPSE, GLOBAL_PERSISTENT_COLLAPSE, RECOVERY_RELAPSE_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE, RECOVERY_RELAPSE_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE, RECOVERY_RELAPSE_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE, RECOVERY_RELAPSE_COLLAPSE],
  [FRAGMENTED_LOCAL_COLLAPSE, RECOVERY_RELAPSE_COLLAPSE]
]

unique_targets =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  GLOBAL_PERSISTENT_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE
]

minimum_entry_depth = 1
mean_entry_depth = 2
```

Interpretation:

```text
OSCILLATING_NONPERSISTENT has multiple possible collapse targets,
but FRAGMENTED_LOCAL_COLLAPSE remains the closest and dominant target.
```

---

## Dominance By Example Volume

The decisive evidence is the target example distribution:

```text
FRAGMENTED_LOCAL_COLLAPSE = 38687
RECOVERY_RELAPSE_COLLAPSE = 88
GLOBAL_PERSISTENT_COLLAPSE = 24
```

The dominance ratio over relapse is:

```text
fragmented_to_relapse_example_ratio = 439.625
```

This means the dominant entry target is not merely frequent by class count.

It is overwhelmingly dominant by mutation-example volume.

---

## Structural Meaning

The widened test space confirmed that:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

is not just one possible collapse target.

It is the canonical basin-entry state under the tested topology.

It acts as the stable contact point between:

```text
noise-like temporal instability
```

and:

```text
confirmed-collapse topology
```

This gives the temporal topology framework a sharper structure:

```text
noise/source region
->
FRAGMENTED_LOCAL_COLLAPSE
->
confirmed-collapse basin
```

---

## Why The Result Is Stronger Than Basin Entry v0

Basin Entry v0 tested:

```text
3 variants
mutation depth <= 2
```

Basin Entry Stability v0 tested:

```text
5 variants
mutation depth <= 3
larger trajectory lengths
shifted collapse positions
```

Despite the wider space, the dominant entry state remained identical:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

This moves the result from:

```text
basin-entry measured
```

to:

```text
basin-entry invariance detected
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO because the temporal topology now has a stable basin-entry state.

OMNIATEMPO can distinguish:

```text
noise-side topology
canonical basin-entry topology
secondary collapse-entry routes
confirmed-collapse topology
```

The canonical basin-entry topology is:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

This is a structural measurement result.

It is not a semantic assertion.

---

## Relation To TDelta

This result supports a future definition of:

```text
TDelta_basin_entry
```

or:

```text
TΔ_basin_entry
```

A possible structural interpretation:

```text
TΔ_basin_entry = minimum temporal / mutation distance
to FRAGMENTED_LOCAL_COLLAPSE
```

This is cleaner than using a generic collapse label.

It separates:

```text
transient/noise instability
```

from:

```text
entry into confirmed-collapse topology
```

---

## What This Confirms

This experiment supports:

```text
basin-entry invariance detected

FRAGMENTED_LOCAL_COLLAPSE is the canonical basin-entry state

dominant_entry_stable = True

fragmented_local_entry_dominant = True

canonical_entries_present = True

all noise-side classes can enter through FRAGMENTED_LOCAL_COLLAPSE

CLEAN_PASS enters at depth 2

SPIKE_FILTERED enters at depth 1

OSCILLATING_NONPERSISTENT enters at depth 1

FRAGMENTED_LOCAL_COLLAPSE dominates target example volume

secondary entries exist but are sparse by comparison
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal basin-entry invariance
real-world temporal reliability
semantic correctness
causal correctness
optimal mutation model
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates controlled synthetic basin-entry invariance under widened test conditions.

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
basin-entry invariance
from noise-like temporal topology
into confirmed-collapse topology
under widened synthetic mutation tests
```

---

## Limitations

```text
Only five variants were tested.

Only six topology classes were tested.

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

Higher mutation depths may expose additional paths.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Basin Entry Invariance
```

Reason:

```text
variant_count = 5

max_mutation_depth = 3

dominant_entry_stable = True

fragmented_local_entry_dominant = True

canonical_entries_present = True

FRAGMENTED_LOCAL_COLLAPSE persisted as dominant entry target in every variant

FRAGMENTED_LOCAL_COLLAPSE target_example_total = 38687

RECOVERY_RELAPSE_COLLAPSE target_example_total = 88

GLOBAL_PERSISTENT_COLLAPSE target_example_total = 24

fragmented_to_relapse_example_ratio = 439.625
```

This is a successful controlled basin-entry invariance experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_basin_escape_v0.py
```

Purpose:

```text
test whether confirmed-collapse topology can escape back
to the noise-like component under controlled mutations
```

Main question:

```text
is the confirmed-collapse basin absorbing,
or can it return to noise-like topology?
```

Required checks:

```text
escape paths from FRAGMENTED_LOCAL_COLLAPSE

escape paths from GLOBAL_PERSISTENT_COLLAPSE

escape paths from RECOVERY_RELAPSE_COLLAPSE

escape depth

escape frequency

escape stability

absorbing-basin score
```

Expected structural value:

```text
basin absorption measurement
```

---

## Final Result

```text
PASS — basin-entry invariance detected.
```

Correct final conclusion:

```text
FRAGMENTED_LOCAL_COLLAPSE remains the canonical basin-entry state
under widened trajectory variants and mutation depth up to 3.
```