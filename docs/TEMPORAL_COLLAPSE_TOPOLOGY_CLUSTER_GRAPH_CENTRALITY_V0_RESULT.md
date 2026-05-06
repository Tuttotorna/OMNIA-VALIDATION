# Temporal Collapse Topology Cluster Graph Centrality v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Signature-Cluster Centrality Map
```

---

## Purpose

This experiment measures centrality inside the invariant signature-cluster graph.

Previous result:

```text
invariant signature clusters form a directed transition topology
under threshold transitions and geometry transitions
```

This experiment asks the next structural question:

```text
which invariant clusters control the transition topology?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates graph centrality over invariant temporal-collapse signature clusters.

---

## Experiment File

```text
examples/temporal_collapse_topology_cluster_graph_centrality_v0.py
```

Result file:

```text
results/temporal_collapse_topology_cluster_graph_centrality_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_cluster_graph_centrality_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

variant_count = 28
flat_record_count = 84
node_count = 6

confirmation_windows = [2, 3, 4]
persistence_window = 2

cluster_count = 32
edge_count = 73

threshold_edge_count = 34
geometry_edge_count = 39

source_cluster_count = 1
attractor_cluster_count = 0
bridge_cluster_count = 31
isolated_cluster_count = 0

dominant_cluster =
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

dominant_cluster_centrality_score = 95.0
dominant_cluster_weighted_total_degree = 28

second_cluster =
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

second_cluster_centrality_score = 61.75
second_cluster_weighted_total_degree = 25

dominant_cluster_matches_expected = True
second_cluster_matches_expected = True

graph_validation_holds = True
graph_failure_count = 0

centrality_map_detected = True
```

The experiment passed.

The expected dominant and second cluster were confirmed under the centrality scoring rule.

---

## Main Finding

The confirmed result is:

```text
the invariant signature-cluster graph has a measurable centrality structure
```

The dominant control cluster is:

```text
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT
```

The second control cluster is:

```text
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
```

So the strongest control region is not generic oscillation.

It is specifically the:

```text
remaining=3 OSCILLATING_NONPERSISTENT cluster layer
```

---

## Centrality Definition

Centrality was measured over invariant signature-cluster nodes.

Node identity:

```text
cluster_id =
transition_cost
+
remaining_run_count
+
destination_class
```

Graph edges:

```text
threshold_transition
geometry_transition
```

Centrality inputs:

```text
weighted_total_degree
weighted_in_degree
weighted_out_degree
bridge_score
self_loop_weight
threshold_edge_total_weight
geometry_edge_total_weight
family_crossing_edge_total_weight
```

Centrality score:

```text
centrality_score =
weighted_total_degree
+
bridge_score
+
0.25 * threshold_edge_total_weight
+
0.25 * geometry_edge_total_weight
+
0.50 * family_crossing_edge_total_weight
+
0.50 * self_loop_weight
```

This scoring rule favors:

```text
high graph connectivity
balanced bridge behavior
threshold relevance
geometry relevance
family-crossing evidence
local self-preservation
```

---

## Validation

Graph validation passed:

```text
graph_validation_holds = True
graph_failure_count = 0
```

This means:

```text
all graph edges were valid
all edge weights were positive
no missing source cluster was detected
no missing target cluster was detected
```

The centrality map was detected:

```text
centrality_map_detected = True
```

The expected dominant cluster matched:

```text
dominant_cluster_matches_expected = True
```

The expected second cluster matched:

```text
second_cluster_matches_expected = True
```

---

## Dominant Cluster

The dominant cluster is:

```text
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT
```

Measured values:

```text
centrality_rank = 1
centrality_score = 95.0

weighted_total_degree = 28
weighted_in_degree = 16
weighted_out_degree = 12

in_degree = 5
out_degree = 3

bridge_score = 45
self_loop_weight = 9

threshold_edge_total_weight = 13
geometry_edge_total_weight = 15
family_crossing_edge_total_weight = 21
```

Structural interpretation:

```text
zero-cost / three-remaining-run oscillating state
is the strongest transition-control hub
```

It dominates because it combines:

```text
high incoming weight
high outgoing weight
strong bridge role
strong self-loop stability
strong threshold-edge participation
strong geometry-edge participation
strong family-crossing evidence
```

This is not a terminal attractor.

It is a central bridge-control cluster.

---

## Why The Dominant Cluster Matters

The dominant cluster has:

```text
weighted_in_degree = 16
weighted_out_degree = 12
```

So it receives many transitions and also emits many transitions.

It has:

```text
bridge_score = 45
```

This is the strongest bridge score in the tested graph.

It also has:

```text
family_crossing_edge_total_weight = 21
```

This is crucial.

It means the cluster is not only central inside one family.

It is central across multiple geometry families.

Correct interpretation:

```text
the dominant cluster is a family-crossing transition hub
```

---

## Second Cluster

The second cluster is:

```text
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
```

Measured values:

```text
centrality_rank = 2
centrality_score = 61.75

weighted_total_degree = 25
weighted_in_degree = 10
weighted_out_degree = 15

in_degree = 5
out_degree = 7

bridge_score = 26
self_loop_weight = 3

threshold_edge_total_weight = 11
geometry_edge_total_weight = 14
family_crossing_edge_total_weight = 6
```

Structural interpretation:

```text
cost-3 / three-remaining-run oscillating state
is the second strongest transition-control hub
```

This cluster is more outward-directed than the dominant cluster:

```text
weighted_out_degree = 15
weighted_in_degree = 10
```

So it behaves as a strong transition-distribution node.

---

## Dominant Pair

The dominant pair is:

```text
rank 1:
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

rank 2:
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
```

Both share:

```text
remaining_run_count = 3
destination_class = OSCILLATING_NONPERSISTENT
```

They differ by:

```text
transition_cost = 0
transition_cost = 3
```

This reveals the central control axis:

```text
same destination
same remaining run count
different transition cost
```

Correct structural reading:

```text
remaining=3 OSCILLATING_NONPERSISTENT is the central control layer,
while transition cost separates stable and reducible variants.
```

---

## Centrality Ranking

### Rank 1

```text
cluster =
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

centrality_score = 95.0
weighted_total_degree = 28
weighted_in_degree = 16
weighted_out_degree = 12
bridge_score = 45
self_loop_weight = 9
threshold_edge_total_weight = 13
geometry_edge_total_weight = 15
family_crossing_edge_total_weight = 21
```

---

### Rank 2

```text
cluster =
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

centrality_score = 61.75
weighted_total_degree = 25
weighted_in_degree = 10
weighted_out_degree = 15
bridge_score = 26
self_loop_weight = 3
threshold_edge_total_weight = 11
geometry_edge_total_weight = 14
family_crossing_edge_total_weight = 6
```

---

### Rank 3

```text
cluster =
cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT

centrality_score = 40.25
weighted_total_degree = 17
weighted_in_degree = 8
weighted_out_degree = 9
bridge_score = 16
self_loop_weight = 6
threshold_edge_total_weight = 8
geometry_edge_total_weight = 9
family_crossing_edge_total_weight = 0
```

---

### Rank 4

```text
cluster =
cost=0|remaining=1|dest=SPIKE_FILTERED

centrality_score = 40.25
weighted_total_degree = 17
weighted_in_degree = 8
weighted_out_degree = 9
bridge_score = 16
self_loop_weight = 6
threshold_edge_total_weight = 8
geometry_edge_total_weight = 9
family_crossing_edge_total_weight = 0
```

---

### Rank 5

```text
cluster =
cost=1|remaining=3|dest=OSCILLATING_NONPERSISTENT

centrality_score = 29.5
weighted_total_degree = 12
weighted_in_degree = 6
weighted_out_degree = 6
bridge_score = 13
self_loop_weight = 1
threshold_edge_total_weight = 6
geometry_edge_total_weight = 6
family_crossing_edge_total_weight = 2
```

---

### Rank 6

```text
cluster =
cost=2|remaining=3|dest=OSCILLATING_NONPERSISTENT

centrality_score = 25.75
weighted_total_degree = 9
weighted_in_degree = 4
weighted_out_degree = 5
bridge_score = 12
self_loop_weight = 0
threshold_edge_total_weight = 5
geometry_edge_total_weight = 4
family_crossing_edge_total_weight = 5
```

---

### Rank 7

```text
cluster =
cost=0|remaining=6|dest=OSCILLATING_NONPERSISTENT

centrality_score = 21.25
weighted_total_degree = 9
weighted_in_degree = 6
weighted_out_degree = 3
bridge_score = 9
self_loop_weight = 2
threshold_edge_total_weight = 4
geometry_edge_total_weight = 5
family_crossing_edge_total_weight = 0
```

---

### Rank 8

```text
cluster =
cost=3|remaining=4|dest=OSCILLATING_NONPERSISTENT

centrality_score = 20.25
weighted_total_degree = 9
weighted_in_degree = 5
weighted_out_degree = 4
bridge_score = 9
self_loop_weight = 0
threshold_edge_total_weight = 4
geometry_edge_total_weight = 5
family_crossing_edge_total_weight = 0
```

---

### Rank 9

```text
cluster =
cost=1|remaining=1|dest=SPIKE_FILTERED

centrality_score = 19.5
weighted_total_degree = 10
weighted_in_degree = 5
weighted_out_degree = 5
bridge_score = 7
self_loop_weight = 0
threshold_edge_total_weight = 4
geometry_edge_total_weight = 6
family_crossing_edge_total_weight = 0
```

---

### Rank 10

```text
cluster =
cost=2|remaining=2|dest=OSCILLATING_NONPERSISTENT

centrality_score = 17.25
weighted_total_degree = 9
weighted_in_degree = 5
weighted_out_degree = 4
bridge_score = 6
self_loop_weight = 0
threshold_edge_total_weight = 4
geometry_edge_total_weight = 5
family_crossing_edge_total_weight = 0
```

---

## Remaining-Run Count Summary

The strongest remaining-run count was:

```text
remaining_run_count = 3
```

Measured values:

```text
cluster_count = 7
weighted_total_degree_mean = 12.142857142857142
centrality_score_mean = 33.67857142857143
bridge_score_mean = 15.142857142857142
```

This is the strongest group by centrality.

Comparison:

```text
remaining=1
centrality_score_mean = 18.8

remaining=2
centrality_score_mean = 18.625

remaining=3
centrality_score_mean = 33.67857142857143

remaining=4
centrality_score_mean = 11.46875

remaining=5
centrality_score_mean = 10.9375

remaining=6
centrality_score_mean = 10.3125
```

Correct interpretation:

```text
remaining=3 is the central graph-control regime
```

This supports the dominant-pair result.

---

## Destination Summary

### SPIKE_FILTERED

```text
cluster_count = 5
weighted_total_degree_mean = 8.8
centrality_score_mean = 18.8
bridge_score_mean = 7.2
```

### OSCILLATING_NONPERSISTENT

```text
cluster_count = 27
weighted_total_degree_mean = 7.185185185185185
centrality_score_mean = 18.037037037037038
bridge_score_mean = 8
```

Important reading:

```text
SPIKE_FILTERED has fewer clusters but high average centrality.
OSCILLATING_NONPERSISTENT has many more clusters and contains the dominant hubs.
```

So the dominant topology is not explained by destination class alone.

It is explained by:

```text
destination_class
+
remaining_run_count
+
transition_cost
```

---

## Source Cluster

The single source cluster is:

```text
cost=2|remaining=4|dest=OSCILLATING_NONPERSISTENT
```

Measured values:

```text
centrality_score = 4.5
weighted_in_degree = 0
weighted_out_degree = 2
weighted_total_degree = 2
bridge_score = 2
neighbor_count = 2

is_source = true
is_bridge = false
is_attractor = false
is_isolated = false
```

Interpretation:

```text
one source-only cluster exists,
but it is not structurally dominant
```

Its centrality rank is low:

```text
rank = 31
```

So the source cluster is not the control center.

---

## Attractor Result

The experiment found:

```text
attractor_cluster_count = 0
```

So this test does not confirm terminal attractors.

Correct interpretation:

```text
the graph has no terminal attractor clusters under this edge construction
```

This matters because the dominant cluster is not an attractor.

It is a bridge-control hub.

---

## Bridge Result

The experiment found:

```text
bridge_cluster_count = 31
cluster_count = 32
```

So:

```text
31 / 32 clusters are bridge clusters
```

This confirms that the graph is mostly transitional.

Correct structural interpretation:

```text
the cluster graph is a bridge-dominated transition-control topology
```

not a sink-dominated attractor topology.

---

## Isolated Result

The experiment found:

```text
isolated_cluster_count = 0
```

So every cluster participates in the graph.

There are no disconnected cluster nodes in the tested topology.

---

## Why This Is Stronger Than The Previous Test

The previous test showed:

```text
invariant clusters form a directed graph
```

This test shows:

```text
the graph has a measurable control hierarchy
```

That is a stronger result.

The hierarchy is:

```text
rank 1:
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

rank 2:
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

rank 3:
cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT

rank 4:
cost=0|remaining=1|dest=SPIKE_FILTERED

rank 5:
cost=1|remaining=3|dest=OSCILLATING_NONPERSISTENT
```

This means:

```text
not all invariant clusters are structurally equal
```

Some clusters control more of the transition topology than others.

---

## Structural Interpretation

The confirmed structural stack is now:

```text
temporal trajectory
->
collapse-run geometry
->
transition cost
->
remaining run count
->
destination class
->
signature cluster
->
cluster adjacency graph
->
cluster centrality map
```

The centrality map identifies which invariant clusters dominate transition flow.

In this run, dominance concentrates around:

```text
remaining=3
destination=OSCILLATING_NONPERSISTENT
```

especially:

```text
cost=0
cost=3
```

So the central control structure is:

```text
zero-cost and cost-3 three-run oscillating clusters
```

---

## What This Confirms

This experiment supports:

```text
signature-cluster centrality map detected

cluster_count = 32
edge_count = 73

threshold_edge_count = 34
geometry_edge_count = 39

dominant_cluster_matches_expected = True
second_cluster_matches_expected = True

graph_validation_holds = True
graph_failure_count = 0

centrality_map_detected = True
```

It also confirms:

```text
the dominant cluster is:
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

the second cluster is:
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
```

---

## What This Does Not Confirm

This experiment does not confirm:

```text
terminal attractors
```

Because:

```text
attractor_cluster_count = 0
```

It does not prove:

```text
universal centrality law
real-world temporal dynamics
semantic correctness
causal correctness
optimal centrality scoring
probabilistic transition dominance
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates a controlled centrality map inside the tested synthetic temporal-collapse topology.

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
centrality_score
weighted_degree
bridge_score
self_loop_weight
threshold_edge_weight
geometry_edge_weight
family_crossing_edge_weight
dominant_cluster
second_cluster
source clusters
attractor clusters
bridge clusters
inside the invariant signature-cluster graph
```

---

## Limitations

```text
This is a synthetic graph-centrality test.

The result depends on the current classifier rules.

Only confirmation windows 2, 3, and 4 were tested.

Persistence window was fixed at 2.

Only synthetic trajectories were tested.

Only seven geometry families were tested.

Only three frame values were used:
PASS
ESCALATE
COLLAPSE

Edges are generated by designed threshold and geometry orderings.

Centrality score is a defined measurement rule, not an external standard.

No external temporal dataset was used.

No probabilistic transition model was used.

No semantic ground truth exists.

No attractor clusters were detected.

The centrality ranking should be re-tested if classifier rules or edge rules change.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Signature-Cluster Centrality Map
```

Reason:

```text
variant_count = 28
flat_record_count = 84

cluster_count = 32
edge_count = 73

dominant_cluster_matches_expected = True
second_cluster_matches_expected = True

graph_validation_holds = True
graph_failure_count = 0

centrality_map_detected = True
```

Important qualifier:

```text
PASS does not mean attractor dominance.
```

It means:

```text
centrality dominance was detected inside the invariant signature-cluster graph.
```

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

Temporal Collapse Topology Geometry Sensitivity v0
-> collapse_run_count controls reverse escape depth under fixed run-length geometries

Temporal Collapse Topology Variable Run Length v0
-> variable run lengths refine the control factor to reducible collapse mass

Temporal Collapse Topology Threshold Sensitivity v0
-> thresholded reducible-mass rule confirmed, but target reachability depends on run count

Temporal Collapse Topology Target Reachability v0
-> post-reduction target-class law detected

Temporal Collapse Topology Transition Cost Destination v0
-> transition cost / destination decomposition detected

Temporal Collapse Topology Transition Signature Stability v0
-> transition-signature stability map detected; family-level signatures are perturbation-sensitive

Temporal Collapse Topology Signature Cluster Invariance v0
-> signature-cluster invariance detected

Temporal Collapse Topology Cluster Adjacency Graph v0
-> invariant signature clusters form a directed transition topology

Temporal Collapse Topology Cluster Graph Centrality v0
-> invariant signature-cluster graph has a measurable centrality structure
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_cluster_graph_control_plane_v0.py
```

Purpose:

```text
separate control-plane clusters from ordinary bridge clusters
```

Main question:

```text
which clusters control graph transitions across threshold and geometry perturbations?
```

Required checks:

```text
cluster_id
centrality_score
family_crossing_edge_total_weight
threshold_edge_total_weight
geometry_edge_total_weight
self_loop_weight
bridge_score
control_plane_score
control_plane_rank
dominant_control_cluster
control_plane_members
```

Expected structural value:

```text
signature-cluster control plane
```

---

## Final Result

```text
PASS — signature-cluster centrality map detected.
```

Correct final conclusion:

```text
the invariant signature-cluster graph has a measurable centrality structure,
dominated by the remaining=3 OSCILLATING_NONPERSISTENT control layer.
```