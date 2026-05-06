# Temporal Collapse Topology Transition Signature Stability v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Transition-Signature Stability Map
```

---

## Purpose

This experiment tests whether transition signatures remain stable under controlled run-length geometry perturbations.

Previous result:

```text
transition =
thresholded_reducible_mass_cost
+
post_reduction_destination_class
```

This experiment asks:

```text
do similar run-length geometries produce stable transition signatures?
```

The answer is precise:

```text
geometries similar by family produce coherent signature clusters,
not identical stable signatures
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates transition-signature consistency and perturbation sensitivity inside the temporal collapse topology classifier.

---

## Experiment File

```text
examples/temporal_collapse_topology_transition_signature_stability_v0.py
```

Result file:

```text
results/temporal_collapse_topology_transition_signature_stability_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_transition_signature_stability_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

variant_count = 24
flat_record_count = 72
node_count = 6

confirmation_windows = [2, 3, 4]
persistence_window = 2

family_count = 6

family_values =
[
  dense_short,
  mixed_staircase,
  single_run,
  spike_plus_long,
  three_equal_runs,
  two_equal_runs
]

unique_transition_signature_count = 67
unique_signature_core_count = 35
signature_cluster_count = 35

stable_family_count = 0
partially_stable_family_count = 0
unstable_family_count = 6

cost_destination_consistency_rate = 1.0
signature_consistency_holds = True
transition_signature_stability_map_detected = True
failure_count = 0
```

The experiment passed.

But it did **not** show identical signature stability inside geometry families.

It showed a **signature-cluster map**.

---

## Main Finding

The strong result is not:

```text
similar geometries produce identical stable signatures
```

The correct result is:

```text
similar geometries produce coherent but perturbation-sensitive signature clusters
```

The internal transition model remained perfectly consistent:

```text
cost_destination_consistency_rate = 1.0
signature_consistency_holds = True
failure_count = 0
```

But family-level stability failed:

```text
stable_family_count = 0
unstable_family_count = 6
```

So the model is structurally coherent, but the signatures are geometry-sensitive.

---

## Signature Definitions

Full transition signature:

```text
SOURCE_CLASS --C=<confirmation_window>/cost=<transition_cost>/remaining=<remaining_run_count>--> DESTINATION_CLASS
```

Signature core:

```text
cost=<transition_cost>/remaining=<remaining_run_count>--> DESTINATION_CLASS
```

The full signature includes:

```text
source class
confirmation window
transition cost
remaining run count
destination class
```

The signature core removes source class and keeps the transition structure:

```text
cost
remaining run count
destination
```

---

## Confirmed Core Rule

The validated rule is:

```text
signature_core =
cost=<thresholded_reducible_mass>/
remaining=<remaining_run_count>
--> <post_reduction_destination_class>
```

Where:

```text
transition_cost =
sum(max(0, run_length - (confirmation_window - 1)))
```

and:

```text
remaining_run_count = len(post_reduction_lengths)
```

and:

```text
0 remaining runs -> CLEAN_PASS
1 remaining run -> SPIKE_FILTERED
2+ remaining runs -> OSCILLATING_NONPERSISTENT
```

---

## By Threshold

### CONFIRMATION_WINDOW = 2

```text
records = 24
unique_transition_signature_count = 23
unique_signature_core_count = 22

transition_cost_values =
[1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15]

destination_class_counts =
{
  SPIKE_FILTERED: 4,
  OSCILLATING_NONPERSISTENT: 20
}

cost_destination_consistency_rate = 1.0
```

At `C=2`, the classifier is strict.

Most geometries require nonzero transition cost.

The signature space is highly differentiated.

---

### CONFIRMATION_WINDOW = 3

```text
records = 24
unique_transition_signature_count = 24
unique_signature_core_count = 23

transition_cost_values =
[0, 1, 2, 3, 4, 5, 6, 9, 10]

destination_class_counts =
{
  SPIKE_FILTERED: 4,
  OSCILLATING_NONPERSISTENT: 20
}

cost_destination_consistency_rate = 1.0
```

At `C=3`, the largest signature differentiation appears:

```text
unique_transition_signature_count = 24
```

Every threshold-conditioned record has a distinct full signature.

---

### CONFIRMATION_WINDOW = 4

```text
records = 24
unique_transition_signature_count = 20
unique_signature_core_count = 19

transition_cost_values =
[0, 1, 2, 3, 4, 6]

destination_class_counts =
{
  SPIKE_FILTERED: 4,
  OSCILLATING_NONPERSISTENT: 20
}

cost_destination_consistency_rate = 1.0
```

At `C=4`, the signature space compresses.

More geometries are already below confirmation threshold.

---

## By Family

## single_run

```text
variants = 4
unique_signatures = 11
unique_cores = 5
core_stability_rate = 0.0
```

### C = 2

```text
core_unique = 4
stable = False

cores =
[
  cost=1/remaining=1--> SPIKE_FILTERED,
  cost=2/remaining=1--> SPIKE_FILTERED,
  cost=3/remaining=1--> SPIKE_FILTERED,
  cost=4/remaining=1--> SPIKE_FILTERED
]
```

### C = 3

```text
core_unique = 4
stable = False

cores =
[
  cost=0/remaining=1--> SPIKE_FILTERED,
  cost=1/remaining=1--> SPIKE_FILTERED,
  cost=2/remaining=1--> SPIKE_FILTERED,
  cost=3/remaining=1--> SPIKE_FILTERED
]
```

### C = 4

```text
core_unique = 3
stable = False

cores =
[
  cost=0/remaining=1--> SPIKE_FILTERED,
  cost=1/remaining=1--> SPIKE_FILTERED,
  cost=2/remaining=1--> SPIKE_FILTERED
]
```

Interpretation:

```text
single-run geometry has stable destination class,
but unstable transition cost.
```

So the family is destination-stable, not signature-stable.

---

## two_equal_runs

```text
variants = 4
unique_signatures = 11
unique_cores = 5
core_stability_rate = 0.0
```

### C = 2

```text
core_unique = 4
stable = False

cores =
[
  cost=2/remaining=2--> OSCILLATING_NONPERSISTENT,
  cost=4/remaining=2--> OSCILLATING_NONPERSISTENT,
  cost=6/remaining=2--> OSCILLATING_NONPERSISTENT,
  cost=8/remaining=2--> OSCILLATING_NONPERSISTENT
]
```

### C = 3

```text
core_unique = 4
stable = False

cores =
[
  cost=0/remaining=2--> OSCILLATING_NONPERSISTENT,
  cost=2/remaining=2--> OSCILLATING_NONPERSISTENT,
  cost=4/remaining=2--> OSCILLATING_NONPERSISTENT,
  cost=6/remaining=2--> OSCILLATING_NONPERSISTENT
]
```

### C = 4

```text
core_unique = 3
stable = False

cores =
[
  cost=0/remaining=2--> OSCILLATING_NONPERSISTENT,
  cost=2/remaining=2--> OSCILLATING_NONPERSISTENT,
  cost=4/remaining=2--> OSCILLATING_NONPERSISTENT
]
```

Interpretation:

```text
two-run equality preserves destination and remaining count,
but transition cost shifts with run length.
```

---

## three_equal_runs

```text
variants = 4
unique_signatures = 11
unique_cores = 5
core_stability_rate = 0.0
```

### C = 2

```text
core_unique = 4
stable = False

cores =
[
  cost=3/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=6/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=9/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=12/remaining=3--> OSCILLATING_NONPERSISTENT
]
```

### C = 3

```text
core_unique = 4
stable = False

cores =
[
  cost=0/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=3/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=6/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=9/remaining=3--> OSCILLATING_NONPERSISTENT
]
```

### C = 4

```text
core_unique = 3
stable = False

cores =
[
  cost=0/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=3/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=6/remaining=3--> OSCILLATING_NONPERSISTENT
]
```

Interpretation:

```text
three equal runs create arithmetic cost ladders.
```

The destination remains fixed, but the cost changes.

---

## mixed_staircase

```text
variants = 4
unique_signatures = 12
unique_cores = 8
core_stability_rate = 0.0
```

### C = 2

```text
core_unique = 4
stable = False

cores =
[
  cost=6/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=10/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=10/remaining=5--> OSCILLATING_NONPERSISTENT,
  cost=15/remaining=5--> OSCILLATING_NONPERSISTENT
]
```

### C = 3

```text
core_unique = 4
stable = False

cores =
[
  cost=3/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=6/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=6/remaining=5--> OSCILLATING_NONPERSISTENT,
  cost=10/remaining=5--> OSCILLATING_NONPERSISTENT
]
```

### C = 4

```text
core_unique = 4
stable = False

cores =
[
  cost=1/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=3/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=3/remaining=5--> OSCILLATING_NONPERSISTENT,
  cost=6/remaining=5--> OSCILLATING_NONPERSISTENT
]
```

Interpretation:

```text
mixed staircase geometries perturb both cost and remaining count.
```

This makes the family strongly signature-sensitive.

---

## spike_plus_long

```text
variants = 4
unique_signatures = 12
unique_cores = 8
core_stability_rate = 0.0
```

### C = 2

```text
core_unique = 4
stable = False

cores =
[
  cost=3/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=4/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=5/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=6/remaining=4--> OSCILLATING_NONPERSISTENT
]
```

### C = 3

```text
core_unique = 4
stable = False

cores =
[
  cost=2/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=3/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=4/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=5/remaining=4--> OSCILLATING_NONPERSISTENT
]
```

### C = 4

```text
core_unique = 4
stable = False

cores =
[
  cost=1/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=2/remaining=3--> OSCILLATING_NONPERSISTENT,
  cost=3/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=4/remaining=4--> OSCILLATING_NONPERSISTENT
]
```

Interpretation:

```text
the long run controls cost;
the spike count controls remaining-run destination structure.
```

---

## dense_short

```text
variants = 4
unique_signatures = 11
unique_cores = 8
core_stability_rate = 0.0
```

### C = 2

```text
core_unique = 4
stable = False

cores =
[
  cost=2/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=3/remaining=5--> OSCILLATING_NONPERSISTENT,
  cost=4/remaining=6--> OSCILLATING_NONPERSISTENT,
  cost=5/remaining=6--> OSCILLATING_NONPERSISTENT
]
```

### C = 3

```text
core_unique = 4
stable = False

cores =
[
  cost=0/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=0/remaining=5--> OSCILLATING_NONPERSISTENT,
  cost=0/remaining=6--> OSCILLATING_NONPERSISTENT,
  cost=1/remaining=6--> OSCILLATING_NONPERSISTENT
]
```

### C = 4

```text
core_unique = 3
stable = False

cores =
[
  cost=0/remaining=4--> OSCILLATING_NONPERSISTENT,
  cost=0/remaining=5--> OSCILLATING_NONPERSISTENT,
  cost=0/remaining=6--> OSCILLATING_NONPERSISTENT
]
```

Interpretation:

```text
dense short geometries frequently collapse to zero-cost cores at higher thresholds,
but remaining count remains sensitive.
```

---

## Signature Clusters

The experiment detected:

```text
signature_cluster_count = 35
```

Important examples:

```text
cost=1/remaining=1--> SPIKE_FILTERED
records = 3
families = [single_run]
C = [2, 3, 4]
sources = [FRAGMENTED_LOCAL_COLLAPSE]
```

```text
cost=0/remaining=1--> SPIKE_FILTERED
records = 3
families = [single_run]
C = [3, 4]
sources = [SPIKE_FILTERED]
```

```text
cost=2/remaining=2--> OSCILLATING_NONPERSISTENT
records = 3
families = [two_equal_runs]
C = [2, 3, 4]
sources = [FRAGMENTED_LOCAL_COLLAPSE]
```

```text
cost=3/remaining=3--> OSCILLATING_NONPERSISTENT
records = 5
families = [spike_plus_long, three_equal_runs]
C = [2, 3, 4]
sources = [FRAGMENTED_LOCAL_COLLAPSE, RECOVERY_RELAPSE_COLLAPSE]
```

```text
cost=6/remaining=4--> OSCILLATING_NONPERSISTENT
records = 3
families = [mixed_staircase, spike_plus_long]
C = [2, 3]
sources = [RECOVERY_RELAPSE_COLLAPSE]
```

```text
cost=3/remaining=5--> OSCILLATING_NONPERSISTENT
records = 2
families = [dense_short, mixed_staircase]
C = [2, 4]
sources = [FRAGMENTED_LOCAL_COLLAPSE]
```

These clusters show that different geometry families can converge to the same signature core.

So the core is not only family-dependent.

It is controlled by the pair:

```text
transition_cost
remaining_run_count
```

plus destination rule.

---

## Key Structural Boundary

The experiment separates three levels:

### Level 1 — Destination stability

```text
destination class may remain stable
```

Example:

```text
single_run -> SPIKE_FILTERED
two_equal_runs -> OSCILLATING_NONPERSISTENT
```

### Level 2 — Core stability

```text
signature core may still vary
```

because transition cost changes.

### Level 3 — Full signature stability

```text
full signature varies even more
```

because source class and confirmation window are included.

This matters.

A family can have stable destination but unstable transition signature.

---

## Rule Validation

```text
signature_consistency_holds = True
failure_count = 0
failures = []
```

The signature core rule made no errors across:

```text
24 variants
72 threshold-conditioned records
6 geometry families
3 confirmation windows
```

---

## What Passed

The following passed:

```text
signature consistency
cost-destination consistency
signature cluster detection
transition-signature stability map construction
zero-failure validation
```

The experiment produced a map of signature clusters.

---

## What Did Not Hold

The following did not hold:

```text
family-level identical signature stability
```

Measured:

```text
stable_family_count = 0
partially_stable_family_count = 0
unstable_family_count = 6
```

So the correct interpretation is not:

```text
similar geometries have identical signatures
```

The correct interpretation is:

```text
similar geometries generate structured perturbation-sensitive signature clusters
```

---

## Relation To Transition Cost Destination v0

Transition Cost Destination v0 showed:

```text
transition = cost + destination
```

Transition Signature Stability v0 adds:

```text
signature = source + threshold + cost + remaining + destination
```

and shows that:

```text
cost + remaining + destination
```

is internally consistent, while exact signatures are sensitive to perturbation.

---

## Relation To Target Reachability v0

Target Reachability v0 showed:

```text
remaining_run_count determines destination class
```

This experiment confirms that inside signature cores:

```text
remaining=1 -> SPIKE_FILTERED
remaining>=2 -> OSCILLATING_NONPERSISTENT
```

with zero failures.

---

## Relation To Geometry Sensitivity v0

Geometry Sensitivity v0 showed that geometry changes can shift escape depth.

This experiment shows the same principle at the transition-signature level:

```text
geometry perturbation shifts transition_cost and sometimes remaining_run_count
```

Therefore, geometry sensitivity is not noise.

It is encoded directly inside the transition signature.

---

## Relation To OMNIATEMPO

This strengthens OMNIATEMPO by giving it a signature-level transition representation:

```text
temporal topology state
+ confirmation threshold
+ run-length geometry
-> transition signature
```

Instead of storing only class labels, OMNIATEMPO can store:

```text
source class
confirmation window
transition cost
remaining run count
destination class
signature core
signature cluster
```

This allows structural comparison across temporal trajectories.

---

## Relation To TDelta

This result supports a signature-level `TDelta` representation:

```text
TΔ_signature =
(
  source_class,
  confirmation_window,
  transition_cost,
  remaining_run_count,
  destination_class
)
```

and a reduced core:

```text
TΔ_core =
(
  transition_cost,
  remaining_run_count,
  destination_class
)
```

Where:

```text
transition_cost =
sum(max(0, run_length - (confirmation_window - 1)))
```

This separates:

```text
distance
residual structure
destination
```

---

## What This Confirms

This experiment supports:

```text
transition-signature stability map detected

signature_consistency_holds = True

cost_destination_consistency_rate = 1.0

failure_count = 0

signature_cluster_count = 35

unique_signature_core_count = 35

unique_transition_signature_count = 67

family-level identical signature stability does not hold

geometry perturbations generate coherent signature clusters
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal transition-signature law
real-world temporal dynamics
semantic correctness
causal correctness
optimal confirmation thresholds
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates a controlled signature-consistency map inside the tested classifier family.

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
transition signatures
signature cores
signature clusters
perturbation sensitivity
under temporal collapse-run geometry
```

---

## Limitations

```text
This is an analytical signature-stability test.

The result depends on the current classifier rules.

Only confirmation windows 2, 3, and 4 were tested.

Persistence window was fixed at 2.

Only synthetic trajectories were tested.

Only six geometry families were tested.

Only three frame values were used:
PASS
ESCALATE
COLLAPSE

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

The signature map should be re-tested if classifier rules change.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Transition-Signature Stability Map
```

Reason:

```text
variant_count = 24
flat_record_count = 72
cost_destination_consistency_rate = 1.0
signature_consistency_holds = True
transition_signature_stability_map_detected = True
failure_count = 0
signature_cluster_count = 35
```

Important qualifier:

```text
PASS does not mean family-level identical signature stability.
```

It means:

```text
signature cores are internally consistent
and perturbation-sensitive clusters are mapped.
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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_signature_cluster_invariance_v0.py
```

Purpose:

```text
test whether signature clusters remain invariant
under equivalent structural rewrites
```

Main question:

```text
do different geometries with the same cost and remaining_run_count
collapse into the same signature core?
```

Required checks:

```text
run_lengths
confirmation_window
transition_cost
remaining_run_count
destination_class
signature_core
cluster_id
cluster_invariance
family_crossing
source_class_variation
```

Expected structural value:

```text
signature-cluster invariance law
```

---

## Final Result

```text
PASS — transition-signature stability map detected.
```

Correct final conclusion:

```text
signature cores are internally coherent,
but geometry families are perturbation-sensitive.

Similar geometries do not necessarily produce identical signatures.

They produce structured signature clusters.
```