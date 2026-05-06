# Temporal Collapse Topology — Index v0

## Purpose

This index is the entry point for the Temporal Collapse Topology experiment line.

It links the scripts, result files, and technical documents produced in the v0 chain.

The purpose of this line is not to solve a semantic task.

It measures whether temporal-collapse behavior exposes a reproducible structural topology under controlled transformations.

```text
measurement != inference != decision


---

Core Result

The v0 chain detected:

directed signature-cluster topology
centrality structure
control plane
dependency map
dependency boundary map
boundary phase diagram

The final canonical claim is:

In this v0 temporal-collapse topology chain, OMNIA-VALIDATION detects a directed signature-cluster topology with a measurable control plane.

The control plane is not universally invariant.

It is stable under tested variant perturbations, but family and threshold perturbations expose drift and critical dependency boundaries.

These boundaries separate into stable, drift, and critical phase zones.


---

Fast Reading Path

Read these in order:

1. TEMPORAL_COLLAPSE_TOPOLOGY_EXPERIMENT_CHAIN_V0.md
2. TEMPORAL_COLLAPSE_TOPOLOGY_BOUNDARY_PHASE_DIAGRAM_V0_RESULT.md
3. TEMPORAL_COLLAPSE_TOPOLOGY_DEPENDENCY_BOUNDARY_V0_RESULT.md
4. TEMPORAL_COLLAPSE_TOPOLOGY_CLUSTER_GRAPH_CONTROL_PLANE_V0_RESULT.md

The chain document gives the full logic.

The phase diagram document gives the final structural closure.

The dependency-boundary document explains why the phase diagram exists.

The control-plane document explains what is being stress-tested.


---

Main Documents

Experiment Chain

docs/TEMPORAL_COLLAPSE_TOPOLOGY_EXPERIMENT_CHAIN_V0.md

Purpose:

Closes the v0 chain and explains the full progression:

signature clusters
→ adjacency graph
→ centrality
→ control plane
→ robustness
→ dependency map
→ dependency boundary
→ boundary phase diagram


---

Boundary Phase Diagram Result

docs/TEMPORAL_COLLAPSE_TOPOLOGY_BOUNDARY_PHASE_DIAGRAM_V0_RESULT.md

Purpose:

Documents the final phase-zone result.

Main outcome:

status: PASS
boundary_scenario_count: 104
phase_zone_count: 3

stable_zone_count: 60
drift_zone_count: 13
critical_zone_count: 31

phase_diagram_detected: True


---

Dependency Boundary Result

docs/TEMPORAL_COLLAPSE_TOPOLOGY_DEPENDENCY_BOUNDARY_V0_RESULT.md

Purpose:

Documents the 104 boundary scenarios used by the phase diagram.

Main outcome:

status: PASS
boundary_scenario_count: 104

critical_boundary_count: 31
moderate_boundary_count: 13
stable_boundary_count: 60

minimum_critical_distance: 1
minimum_moderate_distance: 1


---

Dependency Map Result

docs/TEMPORAL_COLLAPSE_TOPOLOGY_DEPENDENCY_MAP_V0_RESULT.md

Purpose:

Maps which structural axes support, perturb, or break the control plane.

Main axes:

family
threshold
variant

Main outcome:

status: PASS
critical_dependency_count: 10
moderate_dependency_count: 2
stable_support_count: 16


---

Control-Plane Robustness Result

docs/TEMPORAL_COLLAPSE_TOPOLOGY_CONTROL_PLANE_ROBUSTNESS_V0_RESULT.md

Purpose:

Stress-tests the detected control plane.

Main outcome:

status: CHECK
scenario_count: 21
pass_count: 18
strict_pass_count: 17

control_plane_robustness_detected: False
strict_control_plane_robustness_detected: True

Important:

This CHECK result is not hidden.

It is the reason the dependency-map and boundary experiments were created.

The correct conclusion is not universal robustness.

The correct conclusion is measurable dependency structure.


---

Cluster Graph Control Plane Result

docs/TEMPORAL_COLLAPSE_TOPOLOGY_CLUSTER_GRAPH_CONTROL_PLANE_V0_RESULT.md

Purpose:

Detects the control plane inside the directed signature-cluster topology.

Main outcome:

status: PASS
control_plane_detected: True
control_plane_member_count: 6

dominant_control_cluster:
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

second_control_cluster:
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT


---

Cluster Graph Centrality Result

docs/TEMPORAL_COLLAPSE_TOPOLOGY_CLUSTER_GRAPH_CENTRALITY_V0_RESULT.md

Purpose:

Ranks signature clusters by graph-centrality behavior.

Main outcome:

status: PASS
centrality_map_detected: True

dominant_cluster:
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

second_cluster:
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT


---

Cluster Adjacency Graph Result

docs/TEMPORAL_COLLAPSE_TOPOLOGY_CLUSTER_ADJACENCY_GRAPH_V0_RESULT.md

Purpose:

Builds the directed transition topology.

Main outcome:

status: PASS
cluster_adjacency_graph_detected: True

cluster_count: 32
edge_count: 73
threshold_edge_count: 34
geometry_edge_count: 39


---

Signature-Cluster Invariance Result

docs/TEMPORAL_COLLAPSE_TOPOLOGY_SIGNATURE_CLUSTER_INVARIANCE_V0_RESULT.md

Purpose:

Documents the first layer of signature-cluster invariance.

Role:

Establishes that recurring structural signatures exist before graph construction.


---

Scripts

Cluster adjacency graph

examples/temporal_collapse_topology_cluster_adjacency_graph_v0.py

Output:

results/temporal_collapse_topology_cluster_adjacency_graph_v0.json


---

Cluster graph centrality

examples/temporal_collapse_topology_cluster_graph_centrality_v0.py

Output:

results/temporal_collapse_topology_cluster_graph_centrality_v0.json


---

Cluster graph control plane

examples/temporal_collapse_topology_cluster_graph_control_plane_v0.py

Output:

results/temporal_collapse_topology_cluster_graph_control_plane_v0.json


---

Control-plane robustness

examples/temporal_collapse_topology_control_plane_robustness_v0.py

Output:

results/temporal_collapse_topology_control_plane_robustness_v0.json


---

Dependency map

examples/temporal_collapse_topology_dependency_map_v0.py

Output:

results/temporal_collapse_topology_dependency_map_v0.json


---

Dependency boundary

examples/temporal_collapse_topology_dependency_boundary_v0.py

Output:

results/temporal_collapse_topology_dependency_boundary_v0.json


---

Boundary phase diagram

examples/temporal_collapse_topology_boundary_phase_diagram_v0.py

Output:

results/temporal_collapse_topology_boundary_phase_diagram_v0.json


---

Result Files

results/temporal_collapse_topology_cluster_adjacency_graph_v0.json
results/temporal_collapse_topology_cluster_graph_centrality_v0.json
results/temporal_collapse_topology_cluster_graph_control_plane_v0.json
results/temporal_collapse_topology_control_plane_robustness_v0.json
results/temporal_collapse_topology_dependency_map_v0.json
results/temporal_collapse_topology_dependency_boundary_v0.json
results/temporal_collapse_topology_boundary_phase_diagram_v0.json


---

Reproduction Order

Run the scripts in this order:

python examples/temporal_collapse_topology_cluster_adjacency_graph_v0.py
python examples/temporal_collapse_topology_cluster_graph_centrality_v0.py
python examples/temporal_collapse_topology_cluster_graph_control_plane_v0.py
python examples/temporal_collapse_topology_control_plane_robustness_v0.py
python examples/temporal_collapse_topology_dependency_map_v0.py
python examples/temporal_collapse_topology_dependency_boundary_v0.py
python examples/temporal_collapse_topology_boundary_phase_diagram_v0.py

Reason:

The phase diagram depends on the dependency-boundary result.
The dependency boundary depends on the dependency/control-plane logic.
The dependency map depends on the detected control plane.
The control plane depends on the graph topology.
The graph topology depends on signature clusters.


---

Structural Path

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


---

Final v0 Interpretation

The v0 experiment chain shows that temporal-collapse behavior can be measured as a structured topology.

The topology contains a detectable control plane.

That control plane is not universally invariant.

It is stable under tested variant perturbations.

It becomes sensitive under family and threshold perturbations.

Those sensitivities are not random noise.

They organize into stable, drift, and critical zones.


---

Correct Claim

Use this claim:

OMNIA-VALIDATION detected a directed temporal-collapse signature topology with a measurable control plane and a dependency boundary phase diagram.

The tested variant axis remained stable, while family and threshold axes exposed drift and critical boundaries.

Do not claim:

The control plane is universally stable.

Do not claim:

The experiment proves semantic causality.

Do not claim:

The experiment makes decisions.


---

Boundary Statement

This index describes structural measurements only.

measurement != inference != decision

The experiment chain measures invariance, instability, dependency, and phase-like boundary behavior inside the tested temporal-collapse topology.

It does not infer meaning.

It does not decide actions.

It does not claim external causal truth.