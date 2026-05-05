# TEMPORAL COLLAPSE TOPOLOGY TRANSITION GRAPH STABILITY V0

## Overview

This experiment evaluates whether the temporal collapse topology transition graph remains structurally stable under shifted trajectory variants.

The objective is not simple classification accuracy.

The objective is to determine whether the mutation phase-space itself remains invariant when the same structural regimes are translated across different temporal positions and trajectory lengths.

The experiment measures:

- edge persistence
- edge depth stability
- strongly connected component stability
- node metric variance
- transition graph invariance

---

# Core Idea

If the topology graph changes significantly when trajectories are shifted:

```text
same structure
different temporal placement
-> different graph

then the graph is not structural.

It is only a local artifact of specific sequences.

If instead the graph remains stable:

same structure
different temporal placement
-> same graph

then the topology begins to behave like a genuine structural phase-space.


---

Experimental Configuration

Parameters

confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4
max_mutation_depth = 2

Supported Classes

CLEAN_PASS
SPIKE_FILTERED
OSCILLATING_NONPERSISTENT
FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE


---

Variant Construction

Three shifted trajectory variants were generated for every topology class.

The underlying structural regime remained identical while:

sequence length changed

collapse onset positions changed

local timing changed


The experiment therefore isolates:

structural topology
vs
temporal placement


---

Global Result

Final Status

PASS

Key Metrics

variant_count = 3
node_count = 6

edge_count_values = [14, 13, 13]

mean_edge_count = 13.3333
edge_count_std = 0.4714

mean_edge_persistence_rate = 0.95238

fully_persistent_edge_count = 13
partial_edge_count = 1

component_signature_stability_rate = 1.0

largest_scc_size_values = [3, 3, 3]
largest_scc_size_std = 0.0


---

Main Structural Observation

The topology graph remained almost perfectly invariant under trajectory shifts.

This is the critical result:

component_signature_stability_rate = 1.0

The strongly connected component decomposition never changed.

The graph preserved the exact same phase partition:

Cluster A:
CLEAN_PASS
SPIKE_FILTERED
OSCILLATING_NONPERSISTENT

Cluster B:
FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE

This remained invariant across all tested variants.


---

Interpretation

This strongly suggests the graph is not merely memorizing trajectory positions.

Instead, the experiment indicates the existence of a stable structural topology governing regime transitions.

The mutation phase-space behaves approximately like an invariant geometric object.


---

Fully Persistent Edges

The following edges appeared in all tested variants:

CLEAN_PASS -> SPIKE_FILTERED
CLEAN_PASS -> FRAGMENTED_LOCAL_COLLAPSE
CLEAN_PASS -> OSCILLATING_NONPERSISTENT

SPIKE_FILTERED -> CLEAN_PASS
SPIKE_FILTERED -> FRAGMENTED_LOCAL_COLLAPSE
SPIKE_FILTERED -> OSCILLATING_NONPERSISTENT

OSCILLATING_NONPERSISTENT -> FRAGMENTED_LOCAL_COLLAPSE
OSCILLATING_NONPERSISTENT -> SPIKE_FILTERED

FRAGMENTED_LOCAL_COLLAPSE -> RECOVERY_RELAPSE_COLLAPSE

GLOBAL_PERSISTENT_COLLAPSE -> FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE -> RECOVERY_RELAPSE_COLLAPSE

RECOVERY_RELAPSE_COLLAPSE -> FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE -> GLOBAL_PERSISTENT_COLLAPSE

All these edges showed:

persistence_rate = 1.0
depth_std = 0.0

Meaning:

the edges never disappeared

mutation depth never changed

transition geometry remained invariant



---

Partial Edge

Only one edge was unstable:

OSCILLATING_NONPERSISTENT
    ->
RECOVERY_RELAPSE_COLLAPSE

Metrics:

persistence_rate = 0.3333

This edge appeared only in one variant.


---

Important Consequence

This result is structurally important.

It suggests:

OSCILLATING_NONPERSISTENT

is not naturally adjacent to:

RECOVERY_RELAPSE_COLLAPSE

The transition is rare and unstable.

This implies:

oscillation noise
!=
persistent relapse instability

The topology therefore separates:

non-accumulative instability

from:

persistent structural collapse


---

Node Stability

Most node metrics remained perfectly stable.

Examples:

SPIKE_FILTERED
out_std = 0.0
in_std = 0.0

FRAGMENTED_LOCAL_COLLAPSE
out_std = 0.0
in_std = 0.0

GLOBAL_PERSISTENT_COLLAPSE
out_std = 0.0
in_std = 0.0

Only minimal variance appeared in:

OSCILLATING_NONPERSISTENT
RECOVERY_RELAPSE_COLLAPSE

due to the unstable partial edge.


---

Structural Interpretation of SCCs

The SCC decomposition appears to separate two fundamentally different dynamical regions.

Region A — Noise Dynamics

CLEAN_PASS
SPIKE_FILTERED
OSCILLATING_NONPERSISTENT

Characteristics:

low persistence

reversible perturbations

non-accumulative instability

shallow mutation geometry



---

Region B — Collapse Dynamics

FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE

Characteristics:

persistence accumulation

relapse dynamics

regime memory

structural collapse propagation



---

Final Conclusion

The experiment demonstrated that:

the temporal topology transition graph
remains structurally stable
under shifted trajectory variants

The topology is therefore not merely dependent on:

exact collapse timing

sequence alignment

local temporal coordinates


Instead, the graph behaves like a partially invariant mutation geometry over temporal collapse regimes.

The strongest evidence is:

SCC stability = 1.0
edge persistence ≈ 95%
depth variance ≈ 0

This suggests the existence of a stable structural phase-space separating:

noise-like instability

from:

persistent collapse dynamics

within the temporal topology framework.