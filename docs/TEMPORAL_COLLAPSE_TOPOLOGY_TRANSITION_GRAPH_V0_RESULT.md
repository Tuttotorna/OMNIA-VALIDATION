# Temporal Collapse Topology Transition Graph v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Transition Graph
```

---

## Purpose

This experiment builds the directed transition graph between temporal collapse topology classes.

Previous experiments showed:

```text
classification exists
classification remains stable
class boundaries are consistent
window perturbations preserve coherence
noise can induce topology transitions
minimum transition depth is measurable
```

This experiment asks the next structural question:

```text
which topology classes can mutate into which other topology classes?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates the mutation graph of temporal topology classes.

---

## Experiment File

```text
examples/temporal_collapse_topology_transition_graph_v0.py
```

Result file:

```text
results/temporal_collapse_topology_transition_graph_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_transition_graph_v0.py
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

mean_edge_depth = 1.5
min_edge_depth = 1
max_edge_depth = 2

mean_outgoing_count = 2.3333333333333335
mean_incoming_count = 2.3333333333333335

strongly_connected_component_count = 2
largest_strongly_connected_component_size = 3

classes_with_no_outgoing_edges = []
classes_with_no_incoming_edges = []
```

The experiment passed.

A directed mutation graph was found across all tested topology classes.

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

These are the graph nodes.

---

## Main Finding

The central result is:

```text
edge_count = 14
```

and:

```text
classes_with_no_outgoing_edges = []
classes_with_no_incoming_edges = []
```

This means every tested topology class has at least one outgoing transition and at least one incoming transition.

The topology space is not a flat list of labels.

It is a directed mutation graph.

---

## Graph Interpretation

The graph has:

```text
nodes = topology classes
edges = observed topology transitions
edge weight = minimum mutation depth
```

The edge weight measures:

```text
minimum number of frame mutations required
to transform one topology class into another
```

So the graph captures:

```text
temporal topology phase-space structure
```

not just classification.

---

## Strongly Connected Components

The experiment found two strongly connected components:

```text
[
  CLEAN_PASS,
  OSCILLATING_NONPERSISTENT,
  SPIKE_FILTERED
]
```

and:

```text
[
  FRAGMENTED_LOCAL_COLLAPSE,
  GLOBAL_PERSISTENT_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE
]
```

This means the topology space separates into two strongly connected regions.

---

## Component 1 — Low-Collapse / Nonpersistent Component

```text
CLEAN_PASS
SPIKE_FILTERED
OSCILLATING_NONPERSISTENT
```

This component contains topologies where collapse is absent, isolated, or nonpersistent.

Interpretation:

```text
clean
->
spike
->
oscillation
```

This is the low-collapse region of the topology phase space.

---

## Component 2 — Confirmed / Persistent Collapse Component

```text
FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

This component contains topologies where local confirmation or global persistence is present.

Interpretation:

```text
fragmented local collapse
global persistent collapse
recovery-relapse collapse
```

This is the confirmed-collapse region of the topology phase space.

---

## Structural Meaning Of The Two Components

The graph suggests a structural separation between:

```text
nonpersistent instability
```

and:

```text
confirmed collapse topology
```

The boundary between these components is crossed by transitions such as:

```text
SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE
```

These are important because they represent escalation pathways.

---

## Node Metrics

### GLOBAL_PERSISTENT_COLLAPSE

```text
outgoing_count = 2
incoming_count = 1
min_outgoing_depth = 1
mean_outgoing_depth = 1.5
```

Outgoing transitions:

```text
GLOBAL_PERSISTENT_COLLAPSE -> RECOVERY_RELAPSE_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE -> FRAGMENTED_LOCAL_COLLAPSE
```

Incoming transitions:

```text
RECOVERY_RELAPSE_COLLAPSE -> GLOBAL_PERSISTENT_COLLAPSE
```

Interpretation:

```text
global persistence is close to relapse and fragmentation boundaries
```

---

### RECOVERY_RELAPSE_COLLAPSE

```text
outgoing_count = 2
incoming_count = 3
min_outgoing_depth = 1
mean_outgoing_depth = 1.5
```

Outgoing transitions:

```text
RECOVERY_RELAPSE_COLLAPSE -> FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE -> GLOBAL_PERSISTENT_COLLAPSE
```

Incoming transitions:

```text
OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
FRAGMENTED_LOCAL_COLLAPSE -> RECOVERY_RELAPSE_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE -> RECOVERY_RELAPSE_COLLAPSE
```

Interpretation:

```text
recovery-relapse is a central node inside the confirmed-collapse component
```

---

### FRAGMENTED_LOCAL_COLLAPSE

```text
outgoing_count = 1
incoming_count = 5
min_outgoing_depth = 2
mean_outgoing_depth = 2
```

Outgoing transition:

```text
FRAGMENTED_LOCAL_COLLAPSE -> RECOVERY_RELAPSE_COLLAPSE
```

Incoming transitions:

```text
CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE
SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE -> FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE -> FRAGMENTED_LOCAL_COLLAPSE
```

Interpretation:

```text
fragmented local collapse is the strongest attractor node in the tested graph
```

It has the highest incoming count.

It also has the highest minimum outgoing depth:

```text
min_outgoing_depth = 2
```

So it is harder to leave than the other tested nodes.

---

### OSCILLATING_NONPERSISTENT

```text
outgoing_count = 3
incoming_count = 2
min_outgoing_depth = 1
mean_outgoing_depth = 1.6666666666666667
```

Outgoing transitions:

```text
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT -> SPIKE_FILTERED
OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
```

Incoming transitions:

```text
CLEAN_PASS -> OSCILLATING_NONPERSISTENT
SPIKE_FILTERED -> OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
oscillation is a bridge between nonpersistent instability and confirmed-collapse topology
```

---

### SPIKE_FILTERED

```text
outgoing_count = 3
incoming_count = 2
min_outgoing_depth = 1
mean_outgoing_depth = 1
```

Outgoing transitions:

```text
SPIKE_FILTERED -> OSCILLATING_NONPERSISTENT
SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE
SPIKE_FILTERED -> CLEAN_PASS
```

Incoming transitions:

```text
CLEAN_PASS -> SPIKE_FILTERED
OSCILLATING_NONPERSISTENT -> SPIKE_FILTERED
```

Interpretation:

```text
spike is a highly labile boundary node
```

It can return to clean, become oscillation, or cross into fragmented local collapse.

---

### CLEAN_PASS

```text
outgoing_count = 3
incoming_count = 1
min_outgoing_depth = 1
mean_outgoing_depth = 1.6666666666666667
```

Outgoing transitions:

```text
CLEAN_PASS -> SPIKE_FILTERED
CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE
CLEAN_PASS -> OSCILLATING_NONPERSISTENT
```

Incoming transition:

```text
SPIKE_FILTERED -> CLEAN_PASS
```

Interpretation:

```text
clean pass is fragile to collapse injection
```

It has multiple outgoing paths but only one incoming path in this tested graph.

---

## Edge List

### CLEAN_PASS -> SPIKE_FILTERED

```text
minimum_mutation_depth = 1
example_count = 144
```

Interpretation:

```text
one collapse injection can turn clean pass into a spike
```

---

### CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE

```text
minimum_mutation_depth = 2
example_count = 11
```

Interpretation:

```text
two mutations can create local confirmed collapse from clean pass
```

---

### CLEAN_PASS -> OSCILLATING_NONPERSISTENT

```text
minimum_mutation_depth = 2
example_count = 55
```

Interpretation:

```text
two separated collapse injections can create oscillation
```

---

### SPIKE_FILTERED -> OSCILLATING_NONPERSISTENT

```text
minimum_mutation_depth = 1
example_count = 128
```

Interpretation:

```text
one additional isolated collapse can turn spike into oscillation
```

---

### SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE

```text
minimum_mutation_depth = 1
example_count = 48
```

Interpretation:

```text
one adjacent collapse can turn spike into local confirmation
```

---

### SPIKE_FILTERED -> CLEAN_PASS

```text
minimum_mutation_depth = 1
example_count = 24
```

Interpretation:

```text
one mutation can remove the spike and restore clean pass
```

---

### OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE

```text
minimum_mutation_depth = 1
example_count = 136
```

Interpretation:

```text
one bridge mutation can create local confirmation
```

---

### OSCILLATING_NONPERSISTENT -> SPIKE_FILTERED

```text
minimum_mutation_depth = 2
example_count = 12
```

Interpretation:

```text
two mutations can reduce oscillation to isolated spike behavior
```

---

### OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE

```text
minimum_mutation_depth = 2
example_count = 2
```

Interpretation:

```text
two mutations can jump oscillation into confirmed relapse topology
```

---

### FRAGMENTED_LOCAL_COLLAPSE -> RECOVERY_RELAPSE_COLLAPSE

```text
minimum_mutation_depth = 2
example_count = 7
```

Interpretation:

```text
two bridge mutations can turn fragmented local collapse into relapse topology
```

---

### GLOBAL_PERSISTENT_COLLAPSE -> RECOVERY_RELAPSE_COLLAPSE

```text
minimum_mutation_depth = 1
example_count = 470
```

Interpretation:

```text
one separate collapse run can turn global persistence into relapse topology
```

This was the densest observed transition.

---

### GLOBAL_PERSISTENT_COLLAPSE -> FRAGMENTED_LOCAL_COLLAPSE

```text
minimum_mutation_depth = 2
example_count = 40
```

Interpretation:

```text
two dropout mutations can fragment global persistence
```

---

### RECOVERY_RELAPSE_COLLAPSE -> FRAGMENTED_LOCAL_COLLAPSE

```text
minimum_mutation_depth = 1
example_count = 160
```

Interpretation:

```text
one dropout inside a global relapse run can remove global persistence
```

---

### RECOVERY_RELAPSE_COLLAPSE -> GLOBAL_PERSISTENT_COLLAPSE

```text
minimum_mutation_depth = 2
example_count = 4
```

Interpretation:

```text
two mutations can remove relapse structure and restore global persistence
```

---

## Structural Graph Result

The graph supports the following structure:

```text
Low-collapse component:

CLEAN_PASS
<-> SPIKE_FILTERED
<-> OSCILLATING_NONPERSISTENT

Confirmed-collapse component:

FRAGMENTED_LOCAL_COLLAPSE
<-> RECOVERY_RELAPSE_COLLAPSE
<-> GLOBAL_PERSISTENT_COLLAPSE
```

With cross-component escalation paths:

```text
CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE
SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
```

---

## Main Structural Result

The topology classes form a directed phase space.

The phase space has two main regions:

```text
nonpersistent / low-collapse region
```

and:

```text
confirmed-collapse region
```

This means temporal topology is not just a class assignment.

It has transition structure.

---

## Why This Matters

The transition graph allows the system to measure:

```text
which regimes are close
which regimes are far
which regimes are central
which regimes are fragile
which regimes act as attractors
which regimes act as bridges
```

This is stronger than TSI alone.

TSI gives local boundary distance.

The graph gives global topology of the mutation space.

---

## Relation To Phase Transition v0

Phase Transition v0 introduced:

```text
Topology Stability Index
```

Transition Graph v0 generalizes that into:

```text
directed topology phase space
```

Instead of only asking:

```text
how far until any transition?
```

the graph asks:

```text
which transitions are reachable,
and at what mutation depth?
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO by adding a graph layer to temporal topology.

OMNIATEMPO can now represent:

```text
temporal class
class boundary distance
mutation direction
transition graph
component structure
```

That is a much stronger temporal measurement framework than a single collapse score.

---

## Relation To TDelta

This experiment also informs TDelta.

Future TDelta can use the transition graph to distinguish:

```text
movement inside one component
```

from:

```text
movement across components
```

For example:

```text
CLEAN_PASS -> SPIKE_FILTERED
```

is different from:

```text
OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
```

because the second crosses from nonpersistent topology into confirmed-collapse topology.

---

## What This Confirms

This experiment supports:

```text
topology transition graph is measurable

all tested classes have outgoing transitions

all tested classes have incoming transitions

minimum mutation depth can be used as edge weight

two strongly connected components were identified

fragmented local collapse acts as a strong incoming attractor

spike filtered is a highly labile boundary node

oscillation can act as bridge toward confirmed collapse

global persistence is close to relapse topology

recovery-relapse and fragmented-local are tightly connected
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal transition graph
real-world temporal reliability
semantic correctness
causal correctness
optimal mutation model
complete graph over all possible trajectories
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates a controlled synthetic transition graph.

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
directed mutation transitions between temporal topology classes
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

The mutation search was deterministic.

No probabilistic noise model was used.

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
Level 2 — Temporal Topology Transition Graph
```

Reason:

```text
6 topology nodes tested

14 directed transitions found

all nodes have outgoing transitions

all nodes have incoming transitions

mean edge depth = 1.5

min edge depth = 1

max edge depth = 2

2 strongly connected components identified

largest strongly connected component size = 3

no isolated topology class was found
```

This is a successful controlled topology transition graph experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_transition_graph_stability_v0.py
```

Purpose:

```text
test whether the transition graph remains stable
under different base trajectories and shifted mutation positions
```

Main question:

```text
is the transition graph structure stable,
or is it an artifact of the chosen base examples?
```

Required checks:

```text
edge persistence across variants

component stability

incoming/outgoing count stability

edge-depth stability

attractor-node stability

bridge-node stability
```

Expected structural value:

```text
transition graph invariance
```

---

## Final Result

```text
PASS — temporal topology transition graph exposed a connected mutation phase space.
```

Correct final conclusion:

```text
temporal collapse topology classes form a directed mutation graph with two strongly connected structural regions.
```