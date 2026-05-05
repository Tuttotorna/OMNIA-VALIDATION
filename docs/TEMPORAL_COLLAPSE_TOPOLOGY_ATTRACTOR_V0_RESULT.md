# Temporal Collapse Topology Attractor v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Attractor Detection
```

---

## Purpose

This experiment tests whether attractor and basin structure exists inside the temporal collapse topology transition graph.

Previous experiments established:

```text
temporal topology classes
topology thresholds
window sensitivity
noise robustness
phase-transition depth
transition graph
transition graph stability
```

This experiment asks the next structural question:

```text
does the transition graph contain attractor-like regions?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates attractor and basin structure inside the temporal topology mutation graph.

---

## Experiment File

```text
examples/temporal_collapse_topology_attractor_v0.py
```

Result file:

```text
results/temporal_collapse_topology_attractor_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_attractor_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

node_count = 6
edge_count = 14

confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4

max_mutation_depth = 2

strongly_connected_component_count = 2
largest_scc_size = 3

strongest_attractor_candidate = FRAGMENTED_LOCAL_COLLAPSE
strongest_basin_candidate = FRAGMENTED_LOCAL_COLLAPSE
strongest_bridge_candidate = OSCILLATING_NONPERSISTENT

mean_attractor_score = 0
mean_basin_score = 3.5
mean_escape_score = 3.5
```

The experiment passed.

Attractor and basin structure was detected inside the temporal topology transition graph.

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

These are the topology graph nodes.

---

## Main Finding

The central result is:

```text
strongest_attractor_candidate = FRAGMENTED_LOCAL_COLLAPSE
```

and:

```text
strongest_basin_candidate = FRAGMENTED_LOCAL_COLLAPSE
```

This means `FRAGMENTED_LOCAL_COLLAPSE` is the strongest attractor-like node in the tested graph.

It has:

```text
direct_incoming_count = 5
direct_outgoing_count = 1
reachable_incoming_count = 5
reachable_outgoing_count = 2
attractor_score = 3
basin_score = 5
escape_score = 2
```

This makes it the strongest tested basin node.

---

## Structural Interpretation

The transition graph separates into two strongly connected components:

```text
CLEAN_PASS
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
```

and:

```text
FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

The first component behaves like a source-like instability region.

The second component behaves like an attractor-like collapse region.

---

## Component-Level Result

### Component A — Source-Like / Noise Region

```text
nodes =
CLEAN_PASS
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED

size = 3

external_incoming_count = 0
external_outgoing_count = 2

component_attractor_score = -2
```

Interpretation:

```text
this component has outgoing paths toward confirmed-collapse topology
but no external incoming paths from the confirmed-collapse component
```

This component represents:

```text
clean / spike / oscillating instability
```

It is not attractor-like.

It is source-like.

---

### Component B — Attractor-Like / Collapse Region

```text
nodes =
FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE

size = 3

external_incoming_count = 3
external_outgoing_count = 0

component_attractor_score = 3
```

Interpretation:

```text
this component receives transitions from the noise region
and does not emit transitions back to the noise region
within the tested mutation graph
```

This component represents:

```text
confirmed / persistent collapse topology
```

It is attractor-like.

---

## Main Structural Result

The mutation graph shows a one-way macro-structure:

```text
noise-like region
->
confirmed-collapse region
```

More explicitly:

```text
CLEAN_PASS / SPIKE_FILTERED / OSCILLATING_NONPERSISTENT
->
FRAGMENTED_LOCAL_COLLAPSE / GLOBAL_PERSISTENT_COLLAPSE / RECOVERY_RELAPSE_COLLAPSE
```

The reverse macro-transition was not observed in this tested graph.

This supports the interpretation:

```text
persistent collapse topology behaves like an attractor basin
```

---

## Node Metrics

### FRAGMENTED_LOCAL_COLLAPSE

```text
direct_incoming_count = 5
direct_outgoing_count = 1

reachable_incoming_count = 5
reachable_outgoing_count = 2

attractor_score = 3
basin_score = 5
escape_score = 2
```

Interpretation:

```text
strongest attractor-like node
```

It receives paths from all other tested classes.

It has the highest direct incoming count.

It also has limited escape paths.

---

### RECOVERY_RELAPSE_COLLAPSE

```text
direct_incoming_count = 3
direct_outgoing_count = 2

reachable_incoming_count = 5
reachable_outgoing_count = 2

attractor_score = 3
basin_score = 5
escape_score = 2
```

Interpretation:

```text
strong attractor-like node inside the collapse component
```

It has the same reachability attractor score as `FRAGMENTED_LOCAL_COLLAPSE`, but lower direct incoming count.

---

### GLOBAL_PERSISTENT_COLLAPSE

```text
direct_incoming_count = 1
direct_outgoing_count = 2

reachable_incoming_count = 5
reachable_outgoing_count = 2

attractor_score = 3
basin_score = 5
escape_score = 2
```

Interpretation:

```text
global persistent collapse belongs to the attractor-like collapse component
```

It has strong reachability basin structure, even though direct incoming count is lower.

---

### OSCILLATING_NONPERSISTENT

```text
direct_incoming_count = 2
direct_outgoing_count = 3

reachable_incoming_count = 2
reachable_outgoing_count = 5

attractor_score = -3
basin_score = 2
escape_score = 5
```

Interpretation:

```text
strongest bridge candidate
```

It can reach many other classes and acts as an exit path from noise-like instability into collapse topology.

---

### SPIKE_FILTERED

```text
direct_incoming_count = 2
direct_outgoing_count = 3

reachable_incoming_count = 2
reachable_outgoing_count = 5

attractor_score = -3
basin_score = 2
escape_score = 5
```

Interpretation:

```text
labile boundary node
```

It sits in the noise-like component and can transition toward more severe collapse topology.

---

### CLEAN_PASS

```text
direct_incoming_count = 1
direct_outgoing_count = 3

reachable_incoming_count = 2
reachable_outgoing_count = 5

attractor_score = -3
basin_score = 2
escape_score = 5
```

Interpretation:

```text
source-like clean node
```

It is structurally fragile to collapse injection and can reach the collapse component.

---

## Attractor Candidates

The ranked attractor candidates were:

```text
FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
CLEAN_PASS
```

The first three belong to the confirmed-collapse component.

The last three belong to the noise-like component.

This ranking supports the component-level split.

---

## Basin Candidates

The ranked basin candidates were:

```text
FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
CLEAN_PASS
```

Again, the confirmed-collapse component ranks above the noise-like component.

---

## Bridge Candidates

The ranked bridge candidates were:

```text
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
RECOVERY_RELAPSE_COLLAPSE
FRAGMENTED_LOCAL_COLLAPSE
CLEAN_PASS
GLOBAL_PERSISTENT_COLLAPSE
```

The strongest bridge candidate is:

```text
OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
oscillation is the most important transition bridge
from nonpersistent instability toward confirmed collapse topology
```

This matches the previous transition graph result.

---

## Macro-Dynamics

The observed macro-dynamics are:

```text
CLEAN_PASS
SPIKE_FILTERED
OSCILLATING_NONPERSISTENT
```

toward:

```text
FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
```

This is not a semantic judgment.

It is a graph-structural observation.

The tested mutation graph has no external outgoing edge from the confirmed-collapse component back into the noise-like component.

So the collapse component behaves as an attractor basin under the tested mutation rules.

---

## Important Finding

The key distinction is:

```text
nonpersistent instability
```

versus:

```text
accumulative collapse topology
```

The experiment supports the idea that:

```text
not all instability becomes collapse
```

but once the topology enters the confirmed-collapse component, it remains inside that component under the tested graph.

This is the first clear attractor-like result in this validation sequence.

---

## Relation To Transition Graph Stability v0

Transition Graph Stability v0 showed that the graph structure remains stable across shifted trajectory variants.

Attractor v0 uses that graph to measure:

```text
basins
bridges
source-like regions
attractor-like regions
```

So the validation sequence is:

```text
transition graph exists
->
transition graph remains stable
->
attractor/basin structure is measurable
```

---

## Relation To Phase Transition v0

Phase Transition v0 introduced:

```text
Topology Stability Index
```

Attractor v0 extends that into graph-level dynamics.

Instead of only asking:

```text
how far is a class from mutation?
```

this experiment asks:

```text
where does mutation tend to flow in class space?
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO by adding attractor and basin concepts to temporal topology.

The system can now measure:

```text
class identity
transition distance
transition graph
graph stability
source-like regions
bridge nodes
attractor-like basins
```

This moves the framework from temporal classification toward structural temporal dynamics.

---

## Relation To TDelta

This experiment also strengthens future TDelta work.

A future TDelta can distinguish:

```text
time to local collapse
time to confirmed collapse
time to enter collapse basin
time to leave noise-like instability
```

The attractor structure gives a stronger interpretation of temporal divergence.

---

## What This Confirms

This experiment supports:

```text
attractor-like collapse basin is measurable

FRAGMENTED_LOCAL_COLLAPSE is the strongest attractor-like node

OSCILLATING_NONPERSISTENT is the strongest bridge candidate

the topology graph separates into source-like and attractor-like components

confirmed-collapse topology receives transitions from the noise-like component

confirmed-collapse topology does not emit observed transitions back to the noise-like component

nonpersistent instability and accumulative collapse are structurally distinct
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal attractor structure
real-world temporal reliability
semantic correctness
causal correctness
optimal mutation model
probabilistic attractor dynamics
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates a controlled synthetic attractor-basin measurement.

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
attractor and basin structure
inside a temporal topology transition graph
```

---

## Limitations

```text
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
Level 2 — Temporal Topology Attractor Detection
```

Reason:

```text
6 topology nodes tested

14 directed edges used

2 strongly connected components detected

strongest attractor candidate identified

strongest basin candidate identified

strongest bridge candidate identified

component attractor scores separated source-like and attractor-like regions

collapse component had external_incoming_count = 3 and external_outgoing_count = 0

noise component had external_incoming_count = 0 and external_outgoing_count = 2
```

This is a successful controlled attractor-basin experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_attractor_stability_v0.py
```

Purpose:

```text
test whether attractor and basin structure remains stable
under shifted base trajectories and graph variants
```

Main question:

```text
is the detected attractor basin stable,
or is it an artifact of one transition graph?
```

Required checks:

```text
strongest attractor stability

strongest bridge stability

component attractor-score stability

basin-score stability

escape-score stability

source-like component stability

collapse-basin component stability
```

Expected structural value:

```text
attractor invariance
```

---

## Final Result

```text
PASS — attractor and basin structure was detected inside the temporal topology transition graph.
```

Correct final conclusion:

```text
the confirmed-collapse topology component behaves as an attractor-like basin,
while the clean/spike/oscillation component behaves as a source-like instability region.
```