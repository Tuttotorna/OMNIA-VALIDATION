# Temporal Collapse Topology Signature Cluster Invariance v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Signature-Cluster Invariance
```

---

## Purpose

This experiment tests whether signature clusters are invariant transition objects.

The previous experiment showed:

```text
similar geometry families do not necessarily produce identical transition signatures
```

But it also showed:

```text
signature cores form coherent clusters
```

This experiment tests the stronger cluster-level claim:

```text
same transition_cost
+ same remaining_run_count
+ same destination_class
=
same signature_core
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates signature-cluster invariance inside the temporal collapse topology classifier.

---

## Experiment File

```text
examples/temporal_collapse_topology_signature_cluster_invariance_v0.py
```

Result file:

```text
results/temporal_collapse_topology_signature_cluster_invariance_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_signature_cluster_invariance_v0.py
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

family_count = 7

family_values =
[
  dense_short,
  mixed_same_cost,
  single_run,
  spike_plus_long,
  staircase,
  three_equal_runs,
  two_equal_runs
]

cluster_count = 32
signature_core_count = 32
cluster_id_count = 32

multi_record_cluster_count = 20
family_crossing_cluster_count = 7
source_variation_cluster_count = 2
threshold_crossing_cluster_count = 20

cluster_invariance_holds = True
cluster_failure_count = 0

destination_rule_holds = True
destination_failure_count = 0

cluster_invariance_map_detected = True
```

The experiment passed.

No cluster-invariance failure was detected.

No destination-rule failure was detected.

---

## Important Note About `cluster_collision_count`

The script printed:

```text
cluster_collision_count = 32
```

This label is misleading.

In this run, it does **not** indicate 32 failed collisions.

The validation block shows:

```text
cluster_invariance_holds = True
cluster_failure_count = 0
destination_rule_holds = True
destination_failure_count = 0
```

So `cluster_collision_count = 32` should be interpreted as a checked cluster-core mapping count produced by the script’s string-comparison branch, not as an invariance failure.

The actual failure count is:

```text
cluster_failure_count = 0
```

---

## Main Finding

The confirmed invariant is:

```text
same transition_cost
+ same remaining_run_count
+ same destination_class
=
same signature_core
```

Equivalently:

```text
cluster_id =
transition_cost
+
remaining_run_count
+
destination_class
```

produces a unique signature core:

```text
signature_core =
cost=<transition_cost>/remaining=<remaining_run_count>--> <destination_class>
```

This held across:

```text
28 variants
84 threshold-conditioned records
7 geometry families
3 confirmation windows
32 clusters
```

---

## Structural Meaning

The previous result showed that geometry families are perturbation-sensitive.

This result shows that the stable object is not the geometry family.

The stable object is the cluster:

```text
transition_cost + remaining_run_count + destination_class
```

So:

```text
geometry family != invariant signature object
```

but:

```text
cluster_id == invariant signature object
```

This is a stronger structural decomposition.

It means different geometries can converge to the same transition signature core if they share the same cost, same remaining run count, and same destination.

---

## Cluster Definition

Cluster ID:

```text
cluster_id =
cost=<transition_cost>|remaining=<remaining_run_count>|dest=<destination_class>
```

Signature core:

```text
signature_core =
cost=<transition_cost>/remaining=<remaining_run_count>--> <destination_class>
```

Invariance claim:

```text
same transition_cost
same remaining_run_count
same destination_class
->
same signature_core
```

This was confirmed:

```text
cluster_invariance_holds = True
cluster_failure_count = 0
```

---

## Destination Rule

The destination rule also held:

```text
0 remaining runs -> CLEAN_PASS
1 remaining run -> SPIKE_FILTERED
2+ remaining runs -> OSCILLATING_NONPERSISTENT
```

Validation:

```text
destination_rule_holds = True
destination_failure_count = 0
```

In this specific run, observed destinations were:

```text
SPIKE_FILTERED
OSCILLATING_NONPERSISTENT
```

No `CLEAN_PASS` case was included in this dataset because all tested geometries contained at least one run.

---

## By Threshold

### CONFIRMATION_WINDOW = 2

```text
records = 28
clusters = 22
cores = 22

transition_cost_values =
[0, 1, 2, 3, 4, 5, 6, 9, 10]

remaining_run_count_values =
[1, 2, 3, 4, 5, 6]

destination_class_counts =
{
  SPIKE_FILTERED: 5,
  OSCILLATING_NONPERSISTENT: 23
}

destination_match_rate = 1.0
```

At `C=2`, the strict threshold produces the broadest cluster spread:

```text
clusters = 22
```

---

### CONFIRMATION_WINDOW = 3

```text
records = 28
clusters = 21
cores = 21

transition_cost_values =
[0, 1, 2, 3, 4, 5, 6]

remaining_run_count_values =
[1, 2, 3, 4, 5, 6]

destination_class_counts =
{
  SPIKE_FILTERED: 5,
  OSCILLATING_NONPERSISTENT: 23
}

destination_match_rate = 1.0
```

At `C=3`, the cluster spread is still broad but slightly compressed.

---

### CONFIRMATION_WINDOW = 4

```text
records = 28
clusters = 16
cores = 16

transition_cost_values =
[0, 1, 2, 3, 4]

remaining_run_count_values =
[1, 2, 3, 4, 5, 6]

destination_class_counts =
{
  SPIKE_FILTERED: 5,
  OSCILLATING_NONPERSISTENT: 23
}

destination_match_rate = 1.0
```

At `C=4`, more runs fall below confirmation threshold.

The cluster space compresses:

```text
clusters = 16
```

---

## By Family

### single_run

```text
records = 15
clusters = 5
cores = 5

transition_cost_values =
[0, 1, 2, 3, 4]

remaining_run_count_values =
[1]

destination_class_values =
[SPIKE_FILTERED]
```

Single-run geometries always map to:

```text
remaining_run_count = 1
destination = SPIKE_FILTERED
```

Only the transition cost changes.

---

### two_equal_runs

```text
records = 12
clusters = 4
cores = 4

transition_cost_values =
[0, 2, 4, 6]

remaining_run_count_values =
[2]

destination_class_values =
[OSCILLATING_NONPERSISTENT]
```

Two equal runs always preserve:

```text
remaining_run_count = 2
destination = OSCILLATING_NONPERSISTENT
```

Cost changes by threshold and run length.

---

### three_equal_runs

```text
records = 12
clusters = 4
cores = 4

transition_cost_values =
[0, 3, 6, 9]

remaining_run_count_values =
[3]

destination_class_values =
[OSCILLATING_NONPERSISTENT]
```

Three equal runs preserve:

```text
remaining_run_count = 3
destination = OSCILLATING_NONPERSISTENT
```

Cost changes in arithmetic steps.

---

### mixed_same_cost

```text
records = 12
clusters = 4
cores = 4

transition_cost_values =
[0, 1, 2, 3]

remaining_run_count_values =
[3]

destination_class_values =
[OSCILLATING_NONPERSISTENT]
```

The mixed same-cost family confirms that different internal run-length patterns can map into shared cluster IDs.

The object being preserved is not raw geometry.

It is:

```text
cost + remaining count + destination
```

---

### staircase

```text
records = 9
clusters = 7
cores = 7

transition_cost_values =
[1, 3, 6, 10]

remaining_run_count_values =
[4, 5]

destination_class_values =
[OSCILLATING_NONPERSISTENT]
```

Staircase geometries perturb both:

```text
transition cost
remaining run count
```

So they produce more cluster diversity.

---

### spike_plus_long

```text
records = 12
clusters = 8
cores = 8

transition_cost_values =
[1, 2, 3, 4, 5, 6]

remaining_run_count_values =
[3, 4]

destination_class_values =
[OSCILLATING_NONPERSISTENT]
```

The long run controls cost.

The spike count contributes to remaining run count.

---

### dense_short

```text
records = 12
clusters = 8
cores = 8

transition_cost_values =
[0, 1, 2, 3, 4, 5]

remaining_run_count_values =
[4, 5, 6]

destination_class_values =
[OSCILLATING_NONPERSISTENT]
```

Dense short geometries produce many remaining runs and several cost states.

They are cluster-rich but still invariant at the cluster-ID level.

---

## Family-Crossing Clusters

The experiment detected:

```text
family_crossing_cluster_count = 7
```

This is important.

It means the same cluster can appear across different geometry families.

So cluster identity is not bound to family identity.

---

### Cluster: cost=0 | remaining=3 | OSCILLATING_NONPERSISTENT

```text
cluster_id =
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

records = 10

families =
[
  mixed_same_cost,
  three_equal_runs
]

source_classes =
[
  OSCILLATING_NONPERSISTENT
]

confirmation_windows =
[2, 3, 4]

signature_core =
cost=0/remaining=3--> OSCILLATING_NONPERSISTENT
```

This confirms a zero-cost invariant cluster across two geometry families.

---

### Cluster: cost=3 | remaining=3 | OSCILLATING_NONPERSISTENT

```text
cluster_id =
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

records = 9

families =
[
  mixed_same_cost,
  spike_plus_long,
  three_equal_runs
]

source_classes =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE
]

confirmation_windows =
[2, 3, 4]

signature_core =
cost=3/remaining=3--> OSCILLATING_NONPERSISTENT
```

This is the strongest family-crossing example.

Three different geometry families converge to the same signature core.

It also shows source-class variation:

```text
FRAGMENTED_LOCAL_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

without breaking cluster invariance.

---

### Cluster: cost=1 | remaining=3 | OSCILLATING_NONPERSISTENT

```text
records = 4
families = [mixed_same_cost, spike_plus_long]
source_classes = [FRAGMENTED_LOCAL_COLLAPSE]
confirmation_windows = [3, 4]

signature_core =
cost=1/remaining=3--> OSCILLATING_NONPERSISTENT
```

---

### Cluster: cost=2 | remaining=3 | OSCILLATING_NONPERSISTENT

```text
records = 3
families = [mixed_same_cost, spike_plus_long]
source_classes = [FRAGMENTED_LOCAL_COLLAPSE]
confirmation_windows = [3, 4]

signature_core =
cost=2/remaining=3--> OSCILLATING_NONPERSISTENT
```

---

### Cluster: cost=6 | remaining=4 | OSCILLATING_NONPERSISTENT

```text
records = 3
families = [spike_plus_long, staircase]
source_classes = [RECOVERY_RELAPSE_COLLAPSE]
confirmation_windows = [2, 3]

signature_core =
cost=6/remaining=4--> OSCILLATING_NONPERSISTENT
```

---

### Cluster: cost=3 | remaining=4 | OSCILLATING_NONPERSISTENT

```text
records = 3
families = [spike_plus_long, staircase]

source_classes =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE
]

confirmation_windows =
[3, 4]

signature_core =
cost=3/remaining=4--> OSCILLATING_NONPERSISTENT
```

This cluster also has source-class variation.

The source class can change while the cluster core remains invariant.

---

### Cluster: cost=3 | remaining=5 | OSCILLATING_NONPERSISTENT

```text
records = 2
families = [dense_short, staircase]
source_classes = [FRAGMENTED_LOCAL_COLLAPSE]
confirmation_windows = [2, 4]

signature_core =
cost=3/remaining=5--> OSCILLATING_NONPERSISTENT
```

---

## Source-Variation Clusters

The experiment detected:

```text
source_variation_cluster_count = 2
```

This means the same signature core can be reached from different source classes.

---

### Source-Variation Cluster 1

```text
cluster_id =
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

record_count = 9

source_classes =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE
]

families =
[
  mixed_same_cost,
  spike_plus_long,
  three_equal_runs
]

signature_core =
cost=3/remaining=3--> OSCILLATING_NONPERSISTENT
```

This shows:

```text
different source classes can collapse into the same cluster
```

if cost, remaining count, and destination are identical.

---

### Source-Variation Cluster 2

```text
cluster_id =
cost=3|remaining=4|dest=OSCILLATING_NONPERSISTENT

record_count = 3

source_classes =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  RECOVERY_RELAPSE_COLLAPSE
]

families =
[
  spike_plus_long,
  staircase
]

signature_core =
cost=3/remaining=4--> OSCILLATING_NONPERSISTENT
```

This confirms source-class variation at another remaining-count level.

---

## Threshold-Crossing Clusters

The experiment detected:

```text
threshold_crossing_cluster_count = 20
```

This means a cluster can remain invariant across different confirmation windows.

The confirmation window can change the source classification, but the cluster core can remain identical when the tuple stays fixed:

```text
transition_cost
remaining_run_count
destination_class
```

So the threshold is not automatically part of the invariant core.

It belongs to the full transition signature, not the reduced cluster core.

---

## Multi-Record Clusters

The experiment detected:

```text
multi_record_cluster_count = 20
```

This matters because single-record clusters do not strongly test invariance.

Multi-record clusters show repeated convergence into the same core.

The strongest multi-record examples were:

```text
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT
records = 10
```

```text
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
records = 9
```

```text
cost=0|remaining=1|dest=SPIKE_FILTERED
records = 6
```

```text
cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT
records = 6
```

These are the best evidence clusters in this run.

---

## What This Confirms

This experiment supports:

```text
signature-cluster invariance detected

cluster_invariance_holds = True

cluster_failure_count = 0

destination_rule_holds = True

destination_failure_count = 0

cluster_count = 32

signature_core_count = 32

cluster_id_count = 32

family_crossing_cluster_count = 7

source_variation_cluster_count = 2

threshold_crossing_cluster_count = 20

multi_record_cluster_count = 20
```

The core confirmed law is:

```text
same transition_cost
+ same remaining_run_count
+ same destination_class
=
same signature_core
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal temporal topology law
real-world temporal dynamics
semantic correctness
causal correctness
optimal confirmation thresholds
probabilistic transition dynamics
all possible cluster invariance cases
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates a controlled signature-cluster invariance law inside the tested classifier family.

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
signature cluster identity
signature core invariance
family-crossing cluster behavior
source-class variation
threshold-crossing cluster behavior
under temporal collapse-run geometry
```

---

## Limitations

```text
This is an analytical cluster-invariance test.

The result depends on the current classifier rules.

Only confirmation windows 2, 3, and 4 were tested.

Persistence window was fixed at 2.

Only synthetic trajectories were tested.

Only seven geometry families were tested.

Only three frame values were used:
PASS
ESCALATE
COLLAPSE

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

The cluster map should be re-tested if classifier rules change.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Signature-Cluster Invariance
```

Reason:

```text
variant_count = 28
flat_record_count = 84
cluster_count = 32
signature_core_count = 32
cluster_invariance_holds = True
cluster_failure_count = 0
destination_rule_holds = True
destination_failure_count = 0
cluster_invariance_map_detected = True
```

Important qualifier:

```text
PASS does not mean geometry-family invariance.
```

It means:

```text
cluster identity is invariant under the tested mappings.
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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_cluster_adjacency_graph_v0.py
```

Purpose:

```text
build a graph where nodes are invariant signature clusters
and edges represent threshold or geometry transitions between clusters
```

Main question:

```text
how do invariant signature clusters connect to each other?
```

Required checks:

```text
cluster_id
signature_core
threshold transition
geometry transition
cluster adjacency
cluster degree
family-crossing edges
source-variation edges
cluster attractors
cluster bridges
```

Expected structural value:

```text
signature-cluster adjacency graph
```

---

## Final Result

```text
PASS — signature-cluster invariance detected.
```

Correct final conclusion:

```text
signature clusters are invariant objects defined by
transition cost + remaining run count + destination class.
```