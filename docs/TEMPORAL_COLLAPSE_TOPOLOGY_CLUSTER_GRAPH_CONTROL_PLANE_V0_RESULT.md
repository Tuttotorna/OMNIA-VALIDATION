# Temporal Collapse Topology — Cluster Graph Control Plane v0 Result

## Status

**PASS**

The experiment detected a signature-cluster control plane inside the temporal-collapse transition topology.

The dominant and second control clusters matched the expected `remaining=3 / OSCILLATING_NONPERSISTENT` control layer.

## Result file

```text
results/temporal_collapse_topology_cluster_graph_control_plane_v0.json

Reproduction command

python examples/temporal_collapse_topology_cluster_graph_control_plane_v0.py

Experiment

temporal_collapse_topology_cluster_graph_control_plane_v0

Version

0.1.0

Method

cluster_graph_control_plane

Core question

Previous experiments showed that invariant signature clusters form a directed transition graph.

This experiment asks a stricter question:

Which clusters act as the control plane of the transition topology?

A control-plane cluster is not merely a high-degree node.

It is a cluster that combines:

centrality_score
bridge_score
family_crossing_edge_total_weight
threshold_edge_total_weight
geometry_edge_total_weight
self_loop_weight
weighted_total_degree

The goal is to separate ordinary bridge clusters from structurally dominant control clusters.

Main conclusion

signature-cluster control plane detected

The transition topology is controlled by a small six-cluster control plane.

The dominant layer is:

remaining=3 / OSCILLATING_NONPERSISTENT

This layer is not just frequent.

It carries the strongest combined control score, centrality score, bridge load, family-crossing evidence, threshold-transition participation, geometry-transition participation, and self-loop persistence.

Summary

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

control_plane_member_count = 6

graph_validation_holds = true
graph_failure_count = 0

control_plane_validation_holds = true
control_plane_failure_count = 0

control_plane_detected = true

Control-plane score

The control-plane score used in this experiment is:

control_plane_score =
    centrality_score
  + 1.50 * family_crossing_edge_total_weight
  + 1.25 * bridge_score
  + 1.00 * self_loop_weight
  + 0.50 * threshold_edge_total_weight
  + 0.50 * geometry_edge_total_weight
  + 0.50 * weighted_total_degree

This score intentionally favors clusters that are not only central, but structurally active across multiple transition mechanisms.

Dominant control cluster

cluster_id =
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

Metrics:

control_plane_rank = 1
control_plane_score = 219.75
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

is_bridge = true
is_source = false
is_attractor = false
is_isolated = false

Interpretation:

The dominant control cluster is the zero-cost remaining=3
OSCILLATING_NONPERSISTENT cluster.

This means the most structurally important cluster is not the one with the highest transition cost.

It is the stable post-reduction cluster where three residual runs remain and the destination class is OSCILLATING_NONPERSISTENT.

Second control cluster

cluster_id =
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

Metrics:

control_plane_rank = 2
control_plane_score = 131.25
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

is_bridge = true
is_source = false
is_attractor = false
is_isolated = false

Interpretation:

The second control cluster is the cost=3 remaining=3
OSCILLATING_NONPERSISTENT cluster.

This cluster acts as a high-throughput transition bridge.

It has more weighted outgoing flow than incoming flow, which makes it structurally important for propagation through the transition graph.

Expected control clusters

The expected dominant control cluster was:

cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

The observed dominant control cluster was:

cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

Result:

dominant_control_cluster_matches_expected = true

The expected second control cluster was:

cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

The observed second control cluster was:

cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

Result:

second_control_cluster_matches_expected = true

Control-plane members

The detected control plane contains six clusters:

rank 1
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT
control_plane_score = 219.75
centrality_score = 95.0

rank 2
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
control_plane_score = 131.25
centrality_score = 61.75

rank 3
cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT
control_plane_score = 83.25
centrality_score = 40.25

rank 4
cost=0|remaining=1|dest=SPIKE_FILTERED
control_plane_score = 83.25
centrality_score = 40.25

rank 5
cost=1|remaining=3|dest=OSCILLATING_NONPERSISTENT
control_plane_score = 61.75
centrality_score = 29.5

rank 6
cost=2|remaining=3|dest=OSCILLATING_NONPERSISTENT
control_plane_score = 57.25
centrality_score = 25.75

Remaining-run control distribution

The strongest aggregate control layer was remaining=3.

remaining=1
cluster_count = 5
control_plane_score_mean = 37.8
centrality_score_mean = 18.8
bridge_score_mean = 7.2
family_crossing_weight_mean = 0

remaining=2
cluster_count = 4
control_plane_score_mean = 37.6875
centrality_score_mean = 18.625
bridge_score_mean = 7.25
family_crossing_weight_mean = 0

remaining=3
cluster_count = 7
control_plane_score_mean = 73.89285714285714
centrality_score_mean = 33.67857142857143
bridge_score_mean = 15.142857142857142
family_crossing_weight_mean = 4.857142857142857

remaining=4
cluster_count = 8
control_plane_score_mean = 22.96875
centrality_score_mean = 11.46875
bridge_score_mean = 5
family_crossing_weight_mean = 0

remaining=5
cluster_count = 4
control_plane_score_mean = 22.3125
centrality_score_mean = 10.9375
bridge_score_mean = 5.5
family_crossing_weight_mean = 0

remaining=6
cluster_count = 4
control_plane_score_mean = 21.0
centrality_score_mean = 10.3125
bridge_score_mean = 4.75
family_crossing_weight_mean = 0

Structural reading of remaining=3

The remaining=3 layer dominates because it is the only remaining-run group with strong family-crossing load.

remaining=3 family_crossing_weight_mean = 4.857142857142857

All other remaining-run groups had:

family_crossing_weight_mean = 0

This matters because family-crossing weight indicates that a cluster is not confined to one geometric family.

A control-plane cluster must survive across structural families, not only inside one local trajectory pattern.

Destination summary

destination = SPIKE_FILTERED
cluster_count = 5
control_plane_score_mean = 37.8
centrality_score_mean = 18.8
bridge_score_mean = 7.2
family_crossing_weight_mean = 0

destination = OSCILLATING_NONPERSISTENT
cluster_count = 27
control_plane_score_mean = 37.96296296296296
centrality_score_mean = 18.037037037037038
bridge_score_mean = 8
family_crossing_weight_mean = 1.2592592592592593

The dominant and second control clusters both belong to:

OSCILLATING_NONPERSISTENT

However, the destination class alone does not define the control plane.

The decisive structure is the combination:

transition_cost
remaining_run_count
destination_class
graph position
family-crossing load
bridge load
threshold-transition load
geometry-transition load
self-loop persistence

Source and attractor structure

The graph contained one source cluster:

cost=2|remaining=4|dest=OSCILLATING_NONPERSISTENT

Metrics:

control_plane_score = 9.0
centrality_score = 4.5
weighted_total_degree = 2
weighted_in_degree = 0
weighted_out_degree = 2
bridge_score = 2
neighbor_count = 2
is_source = true
is_bridge = false
is_attractor = false
is_isolated = false

No attractor cluster was detected:

attractor_cluster_count = 0

This is an important boundary.

The experiment did not detect a terminal-attractor topology.

It detected a control-plane topology.

Boundary statement

This result does not claim that the temporal-collapse system has a final absorbing attractor.

It shows that the directed transition graph has a small set of structurally dominant control clusters.

Therefore:

control-plane topology != terminal-attractor topology

The measured structure is a control layer inside the transition graph, not an endpoint of the graph.

Validation

Graph validation:

graph_validation_holds = true
graph_failure_count = 0

Control-plane validation:

control_plane_validation_holds = true
control_plane_failure_count = 0

Final validation:

control_plane_detected = true

Final check

PASS — signature-cluster control plane detected.

The dominant and second control clusters matched the expected remaining=3 / OSCILLATING_NONPERSISTENT control layer.

Structural conclusion

The temporal-collapse transition topology is controlled by a six-cluster
control plane dominated by the remaining=3 OSCILLATING_NONPERSISTENT layer.

This result extends the previous cluster-adjacency and centrality results.

The topology is no longer only a directed graph of invariant signature clusters.

It now has a measured internal control layer.