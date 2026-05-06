# Temporal Collapse Topology — Experiment Chain v0

## Purpose

This document closes the first temporal-collapse topology experiment chain.

The chain does not try to solve a task.

It measures how temporal-collapse structures behave when they are reduced, clustered, connected, ranked, perturbed, and mapped into boundary regimes.

The core question is:

```text
Does temporal-collapse behavior expose a stable structural topology,
or is it only a collection of isolated trajectory labels?

The result of the chain is:

A directed signature-cluster topology was detected.
A central control plane was detected.
The control plane was stress-tested.
Its dependencies were mapped.
Its dependency boundaries were measured.
Its boundary phase diagram was detected.

This is measurement-only.

measurement != inference != decision


---

Experiment Chain

1. Signature-cluster invariance
2. Cluster adjacency graph
3. Cluster graph centrality
4. Cluster graph control plane
5. Control-plane robustness
6. Dependency map
7. Dependency boundary
8. Boundary phase diagram

The chain moves from local structural signatures to global boundary regimes.


---

Canonical Result Files

1. Signature-cluster invariance

docs/TEMPORAL_COLLAPSE_TOPOLOGY_SIGNATURE_CLUSTER_INVARIANCE_V0_RESULT.md

Purpose:

Measure whether temporal-collapse signatures remain invariant across threshold and geometry variations.

Role in the chain:

This establishes that recurrent structural signatures exist before graph construction.


---

2. Cluster adjacency graph

examples/temporal_collapse_topology_cluster_adjacency_graph_v0.py
results/temporal_collapse_topology_cluster_adjacency_graph_v0.json
docs/TEMPORAL_COLLAPSE_TOPOLOGY_CLUSTER_ADJACENCY_GRAPH_V0_RESULT.md

Purpose:

Construct a directed graph where:

nodes = invariant signature clusters
edges = threshold transitions + geometry transitions

Main result:

status: PASS
cluster_adjacency_graph_detected: True
cluster_count: 32
edge_count: 73
threshold_edge_count: 34
geometry_edge_count: 39
family_crossing_edge_count: 5
graph_validation_holds: True

Role in the chain:

This turns local signature clusters into a directed topology.


---

3. Cluster graph centrality

examples/temporal_collapse_topology_cluster_graph_centrality_v0.py
results/temporal_collapse_topology_cluster_graph_centrality_v0.json
docs/TEMPORAL_COLLAPSE_TOPOLOGY_CLUSTER_GRAPH_CENTRALITY_V0_RESULT.md

Purpose:

Rank signature clusters by graph-centrality behavior.

Main result:

status: PASS
centrality_map_detected: True

dominant_cluster:
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

dominant_cluster_centrality_score: 95.0
dominant_cluster_weighted_total_degree: 28

second_cluster:
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

second_cluster_centrality_score: 61.75
second_cluster_weighted_total_degree: 25

Role in the chain:

This identifies the most structurally central clusters in the directed topology.


---

4. Cluster graph control plane

examples/temporal_collapse_topology_cluster_graph_control_plane_v0.py
results/temporal_collapse_topology_cluster_graph_control_plane_v0.json
docs/TEMPORAL_COLLAPSE_TOPOLOGY_CLUSTER_GRAPH_CONTROL_PLANE_V0_RESULT.md

Purpose:

Detect whether a small group of clusters controls the transition topology.

Main result:

status: PASS
control_plane_detected: True
control_plane_member_count: 6

dominant_control_cluster:
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

dominant_control_plane_score: 219.75

second_control_cluster:
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

second_control_plane_score: 131.25

Control-plane members:

cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT
cost=0|remaining=1|dest=SPIKE_FILTERED
cost=1|remaining=3|dest=OSCILLATING_NONPERSISTENT
cost=2|remaining=3|dest=OSCILLATING_NONPERSISTENT

Role in the chain:

This converts centrality into a control-plane measurement.

The control plane is not a semantic controller.

It is a structural concentration layer in the transition graph.


---

5. Control-plane robustness

examples/temporal_collapse_topology_control_plane_robustness_v0.py
results/temporal_collapse_topology_control_plane_robustness_v0.json
docs/TEMPORAL_COLLAPSE_TOPOLOGY_CONTROL_PLANE_ROBUSTNESS_V0_RESULT.md

Purpose:

Stress-test the detected control plane under perturbations.

Perturbation types:

baseline
remove_family
remove_variant
remove_threshold
low_weight_pruning
topology_noise

Main result:

status: CHECK
scenario_count: 21
pass_count: 18
strict_pass_count: 17
robustness_rate: 0.8571428571428571
strict_robustness_rate: 0.8095238095238095

control_plane_robustness_detected: False
strict_control_plane_robustness_detected: True

Important result:

The control plane is mostly stable,
but not fully robust under all tested perturbation families.

Failure-sensitive cases:

remove_family__three_equal_runs
remove_threshold__C2
remove_threshold__C4

Role in the chain:

This prevents overclaiming.

The control plane exists, but it is not universally invariant.

It has dependency structure.


---

6. Dependency map

examples/temporal_collapse_topology_dependency_map_v0.py
results/temporal_collapse_topology_dependency_map_v0.json
docs/TEMPORAL_COLLAPSE_TOPOLOGY_DEPENDENCY_MAP_V0_RESULT.md

Purpose:

Map which axes support, perturb, or break the control plane.

Dependency axes:

family
threshold
variant

Main result:

status: PASS
control_plane_dependency_map_detected: True

dependency_scenario_count: 28
dependency_record_count: 28

critical_dependency_count: 10
moderate_dependency_count: 2
stable_support_count: 16

Critical dependency targets:

C2
C4
dense_short
single_run
spike_plus_long
staircase
three_equal_runs
two_equal_runs

Axis summary:

family:
  scenarios: 14
  critical targets detected
  stable supports detected

threshold:
  scenarios: 6
  critical targets: C2, C4
  stable target: C3

variant:
  scenarios: 8
  all stable

Role in the chain:

This identifies dependency axes behind the incomplete robustness result.

It shows that variant perturbations are stable, while family and threshold perturbations can become critical.


---

7. Dependency boundary

examples/temporal_collapse_topology_dependency_boundary_v0.py
results/temporal_collapse_topology_dependency_boundary_v0.json
docs/TEMPORAL_COLLAPSE_TOPOLOGY_DEPENDENCY_BOUNDARY_V0_RESULT.md

Purpose:

Expand dependency mapping into boundary-distance measurement.

Main result:

status: PASS
version: 0.1.1
dependency_boundary_detected: True

boundary_scenario_count: 104
critical_boundary_count: 31
moderate_boundary_count: 13
stable_boundary_count: 60

minimum_critical_distance: 1
minimum_moderate_distance: 1

Axis summary:

family:
  scenarios: 56
  stable: 22
  moderate: 11
  critical: 23

threshold:
  scenarios: 12
  stable: 2
  moderate: 2
  critical: 8

variant:
  scenarios: 36
  stable: 36
  moderate: 0
  critical: 0

Role in the chain:

This gives the control plane a dependency-boundary geometry.

It shows not only which axes matter, but where stable, drift, and critical behavior appears.


---

8. Boundary phase diagram

examples/temporal_collapse_topology_boundary_phase_diagram_v0.py
results/temporal_collapse_topology_boundary_phase_diagram_v0.json
docs/TEMPORAL_COLLAPSE_TOPOLOGY_BOUNDARY_PHASE_DIAGRAM_V0_RESULT.md

Purpose:

Transform the dependency-boundary map into structural phase zones.

Main result:

status: PASS
version: 0.1.4

boundary_scenario_count: 104
phase_zone_count: 3

stable_zone_count: 60
drift_zone_count: 13
critical_zone_count: 31

family_transition_boundary_detected: True
threshold_transition_boundary_detected: True
variant_transition_boundary_detected: False

phase_diagram_validation_holds: True
phase_diagram_detected: True

Detected zones:

STABLE_ZONE
DRIFT_ZONE
CRITICAL_ZONE

Role in the chain:

This closes the chain by showing that dependency boundaries separate into phase-like regimes.

The final structural result is not just a graph.

It is a graph with measurable dependency zones.


---

Full Structural Path

The experiment chain can be read as:

temporal collapse events
        ↓
collapse runs
        ↓
threshold reduction
        ↓
remaining-run signatures
        ↓
signature clusters
        ↓
cluster adjacency graph
        ↓
centrality map
        ↓
control plane
        ↓
robustness test
        ↓
dependency map
        ↓
dependency boundary map
        ↓
boundary phase diagram

This is the canonical path of the current line.


---

Core Structural Finding

The core finding is:

Temporal-collapse behavior forms a directed structural topology.
Inside that topology, a small control plane emerges.
That control plane is not equally dependent on all perturbation axes.
Variant perturbations remain stable.
Family and threshold perturbations contain drift and critical boundaries.
Those boundaries separate into stable, drift, and critical phase zones.

In simpler terms:

The structure is not random.
The control plane is not fully universal.
The topology has measurable support dependencies.
The dependency landscape has phase-like regions.


---

What Was Confirmed

The chain confirms:

signature clusters exist
directed transition topology exists
graph centrality is measurable
a control plane is detectable
the control plane is partially robust
dependency axes are measurable
boundary distances are measurable
phase zones are detectable


---

What Was Not Confirmed

The chain does not confirm:

semantic causality
real-world causality
model cognition
decision correctness
universal robustness
proof of generality outside the tested construction

The robustness result explicitly prevents claiming universal invariance.

control_plane_robustness_detected: False

Therefore the correct claim is:

A control plane was detected,
but it has measurable dependency boundaries.

Not:

The control plane is universally stable.


---

Important Negative Result

The robustness experiment returned:

status: CHECK
control_plane_robustness_detected: False

This is not a failure of the whole chain.

It is the reason the next experiments were necessary.

The chain did not hide the instability.

It measured it.

Then it mapped it.

Then it turned it into a dependency boundary and a phase diagram.

This is the correct scientific progression:

detect structure
test structure
find instability
map instability
classify boundary regimes


---

Axis-Level Conclusion

Variant axis

variant:
  stable: 36
  drift: 0
  critical: 0

Conclusion:

The tested topology is not dependent on individual variants.

Variant perturbations preserve the control plane.


---

Family axis

family:
  stable: 22
  drift: 11
  critical: 23

Conclusion:

Family structure matters.

Some family perturbations are safe.

Some cause ranking drift.

Some break the expected control plane.


---

Threshold axis

threshold:
  stable: 2
  drift: 2
  critical: 8

Conclusion:

Threshold choice is structurally sensitive.

Critical behavior can appear at boundary distance 1.

The threshold axis is not a neutral parameter.


---

Final Canonical Claim

The safest canonical claim is:

In this v0 temporal-collapse topology chain, OMNIA-VALIDATION detects a directed signature-cluster topology with a measurable control plane. The control plane is not universally invariant: it is stable under tested variant perturbations, but family and threshold perturbations expose drift and critical dependency boundaries. These boundaries separate into stable, drift, and critical phase zones.

This claim is supported by the chain.

It does not overstate the result.

It does not claim semantic causality.

It does not claim generality beyond the tested construction.


---

Boundary Statement

This whole chain remains measurement-only.

measurement != inference != decision

The outputs are structural diagnostics.

They are not decisions.

They are not semantic interpretations.

They are not proof of external truth.

They measure invariance, instability, dependency, and phase-like boundary behavior inside the tested temporal-collapse topology.