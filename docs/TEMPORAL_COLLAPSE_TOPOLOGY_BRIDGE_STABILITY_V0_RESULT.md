# Temporal Collapse Topology Bridge Stability v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Bridge Stability
```

---

## Purpose

This experiment isolates the bridge instability exposed by:

```text
Temporal Collapse Topology Attractor Stability v0
```

The previous experiment showed:

```text
attractor identity stable
basin identity stable
SCC signature stable
bridge identity unstable under the previous bridge ranking
```

This experiment asks a sharper question:

```text
are OSCILLATING_NONPERSISTENT and SPIKE_FILTERED equivalent bridge candidates,
or does one class dominate the bridge role under a stricter bridge metric?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates bridge-role stability inside the temporal topology transition graph.

---

## Experiment File

```text
examples/temporal_collapse_topology_bridge_stability_v0.py
```

Result file:

```text
results/temporal_collapse_topology_bridge_stability_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_bridge_stability_v0.py
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

max_mutation_depth = 2

edge_count_values = [14, 13, 13]
mean_edge_count = 13.333333333333334
edge_count_std = 0.4714045207910317

ranked_first_bridge_values =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE
]

stable_ranked_first_bridge = True
stable_top_bridge_set = True

bridge_equivalence_candidates =
[
  FRAGMENTED_LOCAL_COLLAPSE
]

candidate_frequency =
{
  FRAGMENTED_LOCAL_COLLAPSE: 3
}
```

The result is `CHECK`.

The CHECK is not caused by runtime failure.

The CHECK is caused by falsification of the initial hypothesis.

---

## Initial Hypothesis

The experiment was designed to test whether these two classes were equivalent bridge candidates:

```text
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
```

Expected possibility:

```text
bridge role may be distributed across multiple noise-side classes
```

Observed result:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

was the only stable ranked-first bridge candidate across all three variants.

Therefore the initial multi-candidate bridge hypothesis was not supported.

---

## Main Result

The central finding is:

```text
ranked_first_bridge_values =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE
]
```

and:

```text
stable_ranked_first_bridge = True
```

This means the bridge role was not unstable under this metric.

It was stable and singular.

The dominant bridge was:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

---

## Why The Status Is CHECK

The experiment status is `CHECK` because the test expected to expose:

```text
multi-candidate bridge structure
```

with both:

```text
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
```

appearing as legitimate equivalent bridge candidates.

Instead, the experiment found:

```text
single dominant bridge structure
```

with:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

as the unique stable bridge candidate.

So the correct interpretation is:

```text
the hypothesis failed;
the measurement succeeded.
```

---

## Structural Interpretation

The result implies:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

is not only:

```text
strongest attractor candidate
strongest basin candidate
```

but also:

```text
stable dominant bridge candidate
```

under the current bridge metric.

This means it acts as a structural entry node into confirmed-collapse topology.

It receives cross-component transitions from the noise-like region and connects into the confirmed-collapse component.

---

## Supported Classes

```text
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
CLEAN_PASS
```

---

## Component Partition

The experiment uses the same macro-partition established in earlier graph tests.

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

The bridge analysis measures cross-component contribution between these two regions.

---

## Bridge Metric

The bridge score combines:

```text
cross-component outgoing contribution
cross-component incoming contribution
direct incoming degree
direct outgoing degree
```

The purpose is to detect nodes that act as structural connectors across component boundaries.

Under this metric, the strongest bridge was consistently:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

---

## Bridge Metric Stability

### GLOBAL_PERSISTENT_COLLAPSE

```text
bridge_scores = [3, 3, 3]
component_crossing_scores = [0, 0, 0]

bridge_score_std = 0.0
component_crossing_score_std = 0.0
```

Interpretation:

```text
stable, but not a bridge node
```

---

### RECOVERY_RELAPSE_COLLAPSE

```text
bridge_scores = [7, 4, 4]
component_crossing_scores = [1, 0, 0]

bridge_score_std = 1.4142135623730951
component_crossing_score_std = 0.4714045207910317
```

Interpretation:

```text
partially variant-sensitive
```

It sometimes receives or participates in cross-component structure, but it is not the stable bridge leader.

---

### FRAGMENTED_LOCAL_COLLAPSE

```text
bridge_scores = [12, 12, 12]
component_crossing_scores = [3, 3, 3]

bridge_score_std = 0.0
component_crossing_score_std = 0.0
```

Interpretation:

```text
stable dominant bridge
```

This is the strongest result in the experiment.

`FRAGMENTED_LOCAL_COLLAPSE` is both high-scoring and perfectly stable across variants.

---

### OSCILLATING_NONPERSISTENT

```text
bridge_scores = [11, 7, 7]
component_crossing_scores = [2, 1, 1]

bridge_score_std = 1.8856180831641267
component_crossing_score_std = 0.4714045207910317
```

Interpretation:

```text
important but unstable secondary bridge
```

It participates in cross-component movement, but its score changes when the partial edge disappears.

---

### SPIKE_FILTERED

```text
bridge_scores = [8, 8, 8]
component_crossing_scores = [1, 1, 1]

bridge_score_std = 0.0
component_crossing_score_std = 0.0
```

Interpretation:

```text
stable secondary bridge contribution
```

It is stable but weaker than `FRAGMENTED_LOCAL_COLLAPSE`.

---

### CLEAN_PASS

```text
bridge_scores = [7, 7, 7]
component_crossing_scores = [1, 1, 1]

bridge_score_std = 0.0
component_crossing_score_std = 0.0
```

Interpretation:

```text
stable weak bridge contribution
```

It can cross toward collapse topology but is not the dominant bridge.

---

## Variant-Level Result

### Variant 0

```text
edge_count = 14
top_bridge_score = 12
ranked_first = FRAGMENTED_LOCAL_COLLAPSE
tied_top = [FRAGMENTED_LOCAL_COLLAPSE]
```

### Variant 1

```text
edge_count = 13
top_bridge_score = 12
ranked_first = FRAGMENTED_LOCAL_COLLAPSE
tied_top = [FRAGMENTED_LOCAL_COLLAPSE]
```

### Variant 2

```text
edge_count = 13
top_bridge_score = 12
ranked_first = FRAGMENTED_LOCAL_COLLAPSE
tied_top = [FRAGMENTED_LOCAL_COLLAPSE]
```

The ranked-first bridge did not change.

---

## Component Results

### Variant 0

Noise component:

```text
nodes =
CLEAN_PASS
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED

external_incoming_count = 0
external_outgoing_count = 2

external_outgoing_nodes =
FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

Collapse component:

```text
nodes =
FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE

external_incoming_count = 3
external_outgoing_count = 0

external_incoming_nodes =
CLEAN_PASS
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
```

---

### Variant 1

Noise component:

```text
external_incoming_count = 0
external_outgoing_count = 1

external_outgoing_nodes =
FRAGMENTED_LOCAL_COLLAPSE
```

Collapse component:

```text
external_incoming_count = 3
external_outgoing_count = 0

external_incoming_nodes =
CLEAN_PASS
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
```

---

### Variant 2

Noise component:

```text
external_incoming_count = 0
external_outgoing_count = 1

external_outgoing_nodes =
FRAGMENTED_LOCAL_COLLAPSE
```

Collapse component:

```text
external_incoming_count = 3
external_outgoing_count = 0

external_incoming_nodes =
CLEAN_PASS
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
```

---

## Critical Observation

Across all variants, the collapse component receives incoming structure from:

```text
CLEAN_PASS
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
```

but emits no external outgoing structure back to the noise component.

This reinforces the previous attractor result:

```text
noise/source region
->
collapse/attractor region
```

The bridge role is therefore better interpreted as an entry interface into the collapse component.

Under the current metric, that interface is dominated by:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

---

## Updated Interpretation

Before this experiment, the working hypothesis was:

```text
bridge identity may alternate between OSCILLATING_NONPERSISTENT and SPIKE_FILTERED
```

After this experiment, the interpretation changes to:

```text
OSCILLATING_NONPERSISTENT and SPIKE_FILTERED are source-side contributors

FRAGMENTED_LOCAL_COLLAPSE is the stable collapse-side entry bridge
```

That is a cleaner structural distinction.

---

## Relation To Attractor Stability v0

Attractor Stability v0 found:

```text
strongest_bridge_values =
[
  OSCILLATING_NONPERSISTENT,
  SPIKE_FILTERED,
  SPIKE_FILTERED
]
```

That was based on a different bridge ranking rule.

Bridge Stability v0 used a stricter cross-component bridge metric.

It found:

```text
ranked_first_bridge_values =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE
]
```

This means the previous bridge instability was metric-sensitive.

The updated interpretation:

```text
source-side bridge label is unstable;
collapse-side bridge interface is stable.
```

---

## Relation To Transition Graph Stability v0

Transition Graph Stability v0 showed:

```text
mean_edge_persistence_rate = 0.95238
component_signature_stability_rate = 1.0
```

Bridge Stability v0 adds:

```text
the cross-component interface is stable
```

but also confirms that one edge is variant-sensitive:

```text
OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
```

This explains the score variation in:

```text
OSCILLATING_NONPERSISTENT
RECOVERY_RELAPSE_COLLAPSE
```

---

## Relation To OMNIATEMPO

This experiment refines OMNIATEMPO’s bridge concept.

OMNIATEMPO should distinguish:

```text
source-side transition contributors
```

from:

```text
collapse-side entry interface
```

The current result suggests:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

is the stable collapse-side entry interface.

This is a more precise statement than:

```text
the bridge is unstable
```

The correct statement is:

```text
bridge definition matters;
under cross-component entry scoring,
the bridge is stable and singular.
```

---

## Relation To TDelta

For future TDelta work, this matters because basin entry can be treated as:

```text
entry into FRAGMENTED_LOCAL_COLLAPSE
```

rather than simply:

```text
movement through any noise-side bridge
```

This may allow a clearer temporal divergence signal:

```text
TΔ_entry_to_confirmed_collapse
```

or:

```text
TΔ_basin_entry
```

---

## What This Confirms

This experiment supports:

```text
FRAGMENTED_LOCAL_COLLAPSE is the stable ranked-first bridge under the current metric

FRAGMENTED_LOCAL_COLLAPSE has bridge_score = 12 across all variants

FRAGMENTED_LOCAL_COLLAPSE has component_crossing_score = 3 across all variants

bridge_score_std = 0.0 for FRAGMENTED_LOCAL_COLLAPSE

component_crossing_score_std = 0.0 for FRAGMENTED_LOCAL_COLLAPSE

the collapse-side entry interface is stable

the source-side bridge interpretation is metric-sensitive

OSCILLATING_NONPERSISTENT is an important but unstable secondary contributor

SPIKE_FILTERED is a stable but weaker secondary contributor
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal bridge structure
optimal bridge metric
real-world temporal reliability
semantic correctness
causal correctness
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates a controlled synthetic bridge-role measurement and falsifies the initial equivalence hypothesis.

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
bridge-role stability
inside temporal topology transition graphs
under shifted trajectory variants
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

The bridge metric is hand-defined.

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
CHECK
```

Evidence level:

```text
Level 2 — Temporal Topology Bridge Stability
```

Reason:

```text
the expected multi-candidate bridge structure was not observed

OSCILLATING_NONPERSISTENT and SPIKE_FILTERED were not equivalent top bridge candidates

FRAGMENTED_LOCAL_COLLAPSE emerged as a stable single dominant bridge

ranked_first_bridge_values were stable across all variants

stable_ranked_first_bridge = True

stable_top_bridge_set = True

bridge_equivalence_candidates = [FRAGMENTED_LOCAL_COLLAPSE]
```

This is a useful CHECK.

It falsifies the planned hypothesis and reveals a stronger singular bridge structure.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_basin_entry_v0.py
```

Purpose:

```text
measure basin entry explicitly through FRAGMENTED_LOCAL_COLLAPSE
```

Main question:

```text
is FRAGMENTED_LOCAL_COLLAPSE the canonical entry state
into confirmed-collapse topology?
```

Required checks:

```text
entry frequency

entry depth

entry stability

entry from CLEAN_PASS

entry from SPIKE_FILTERED

entry from OSCILLATING_NONPERSISTENT

basin-entry dominance

alternative entry paths
```

Expected structural value:

```text
confirmed-collapse basin entry measurement
```

---

## Final Result

```text
CHECK — expected multi-candidate bridge structure was not observed.
```

Correct final conclusion:

```text
FRAGMENTED_LOCAL_COLLAPSE emerged as a stable single dominant bridge under the current cross-component bridge metric.
```