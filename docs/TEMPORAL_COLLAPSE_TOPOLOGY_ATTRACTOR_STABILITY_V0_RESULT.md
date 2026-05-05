# Temporal Collapse Topology Attractor Stability v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Attractor Stability
```

---

## Purpose

This experiment tests whether the attractor and basin structure detected in the temporal collapse topology graph remains stable under shifted trajectory variants.

Previous experiments showed:

```text
transition graph exists
transition graph remains structurally stable
attractor and basin structure is detectable
```

This experiment asks the sharper question:

```text
does the same attractor / basin / bridge identity remain stable
when the base trajectory variants are shifted?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates attractor-identity stability inside the temporal topology mutation graph.

---

## Experiment File

```text
examples/temporal_collapse_topology_attractor_stability_v0.py
```

Result file:

```text
results/temporal_collapse_topology_attractor_stability_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_attractor_stability_v0.py
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

strongest_attractor_values =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE
]

strongest_basin_values =
[
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE,
  FRAGMENTED_LOCAL_COLLAPSE
]

strongest_bridge_values =
[
  OSCILLATING_NONPERSISTENT,
  SPIKE_FILTERED,
  SPIKE_FILTERED
]

strongest_attractor_stable = True
strongest_basin_stable = True
strongest_bridge_stable = False

scc_signature_stability_rate = 1.0
```

The result is `CHECK`.

The CHECK is caused by unstable bridge identity, not by attractor or basin failure.

---

## Main Result

The central result is:

```text
strongest_attractor_stable = True
strongest_basin_stable = True
scc_signature_stability_rate = 1.0
```

This means the main attractor and basin structure remained stable across all tested variants.

The unstable part is:

```text
strongest_bridge_stable = False
```

The strongest bridge changed from:

```text
variant 0 -> OSCILLATING_NONPERSISTENT
variant 1 -> SPIKE_FILTERED
variant 2 -> SPIKE_FILTERED
```

Correct interpretation:

```text
attractor / basin stable
bridge identity unstable
```

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

These are the tested temporal topology classes.

---

## Stable Attractor

The strongest attractor candidate remained:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

for all three variants.

```text
variant 0 -> FRAGMENTED_LOCAL_COLLAPSE
variant 1 -> FRAGMENTED_LOCAL_COLLAPSE
variant 2 -> FRAGMENTED_LOCAL_COLLAPSE
```

Therefore the attractor identity is stable under shifted trajectory variants.

---

## Stable Basin

The strongest basin candidate also remained:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

for all three variants.

```text
variant 0 -> FRAGMENTED_LOCAL_COLLAPSE
variant 1 -> FRAGMENTED_LOCAL_COLLAPSE
variant 2 -> FRAGMENTED_LOCAL_COLLAPSE
```

Therefore the basin identity is stable under shifted trajectory variants.

---

## Unstable Bridge

The strongest bridge candidate changed:

```text
variant 0 -> OSCILLATING_NONPERSISTENT
variant 1 -> SPIKE_FILTERED
variant 2 -> SPIKE_FILTERED
```

This means bridge identity is more sensitive than attractor identity.

The bridge is not yet structurally invariant under the tested perturbations.

This is the reason for the `CHECK`.

---

## Node Score Stability

Despite the bridge identity shift, node-level score stability was exact.

### Collapse-side nodes

```text
GLOBAL_PERSISTENT_COLLAPSE
attractor_scores = [3, 3, 3]
basin_scores = [5, 5, 5]
escape_scores = [2, 2, 2]

RECOVERY_RELAPSE_COLLAPSE
attractor_scores = [3, 3, 3]
basin_scores = [5, 5, 5]
escape_scores = [2, 2, 2]

FRAGMENTED_LOCAL_COLLAPSE
attractor_scores = [3, 3, 3]
basin_scores = [5, 5, 5]
escape_scores = [2, 2, 2]
```

All collapse-side nodes retained:

```text
attractor_score_std = 0.0
basin_score_std = 0.0
escape_score_std = 0.0
```

This confirms collapse-basin stability.

---

### Noise-side nodes

```text
OSCILLATING_NONPERSISTENT
attractor_scores = [-3, -3, -3]
basin_scores = [2, 2, 2]
escape_scores = [5, 5, 5]

SPIKE_FILTERED
attractor_scores = [-3, -3, -3]
basin_scores = [2, 2, 2]
escape_scores = [5, 5, 5]

CLEAN_PASS
attractor_scores = [-3, -3, -3]
basin_scores = [2, 2, 2]
escape_scores = [5, 5, 5]
```

All noise-side nodes retained:

```text
attractor_score_std = 0.0
basin_score_std = 0.0
escape_score_std = 0.0
```

This confirms source-region stability.

---

## Component Stability

The strongly connected component signature remained stable:

```text
scc_signature_stability_rate = 1.0
```

The same two components appeared in every variant.

### Component A — Noise-like / Source Region

```text
CLEAN_PASS
OSCILLATING_NONPERSISTENT
SPIKE_FILTERED
```

### Component B — Collapse-like / Attractor Region

```text
FRAGMENTED_LOCAL_COLLAPSE
GLOBAL_PERSISTENT_COLLAPSE
RECOVERY_RELAPSE_COLLAPSE
```

This component split remained invariant.

---

## Component Scores

### Variant 0

Noise component:

```text
external_incoming_count = 0
external_outgoing_count = 2
component_attractor_score = -2
```

Collapse component:

```text
external_incoming_count = 3
external_outgoing_count = 0
component_attractor_score = 3
```

### Variant 1

Noise component:

```text
external_incoming_count = 0
external_outgoing_count = 1
component_attractor_score = -1
```

Collapse component:

```text
external_incoming_count = 3
external_outgoing_count = 0
component_attractor_score = 3
```

### Variant 2

Noise component:

```text
external_incoming_count = 0
external_outgoing_count = 1
component_attractor_score = -1
```

Collapse component:

```text
external_incoming_count = 3
external_outgoing_count = 0
component_attractor_score = 3
```

The collapse component remained exactly attractor-like:

```text
component_attractor_score = 3
```

in all variants.

The noise component remained source-like:

```text
component_attractor_score < 0
```

in all variants.

Only the number of outgoing paths from the noise component changed.

---

## Structural Meaning

This experiment shows that the macro-topology is stable:

```text
noise/source component
->
collapse/attractor component
```

The attractor basin is stable.

The source region is stable.

The component split is stable.

The unstable part is the specific bridge node identity.

This means the system can distinguish:

```text
stable basin structure
```

from:

```text
unstable bridge role
```

That distinction is important.

A bridge can be sensitive while the basin remains stable.

---

## Why The Result Is CHECK

The experiment was intentionally strict.

It required all of the following:

```text
strongest_attractor_stable = True
strongest_basin_stable = True
strongest_bridge_stable = True
scc_signature_stability_rate = 1.0
```

The observed values were:

```text
strongest_attractor_stable = True
strongest_basin_stable = True
strongest_bridge_stable = False
scc_signature_stability_rate = 1.0
```

Therefore the correct result is:

```text
CHECK
```

This CHECK is not a collapse of the attractor result.

It exposes a more precise structural distinction:

```text
attractor identity is stable
bridge identity is not stable
```

---

## Structural Result

The stable part:

```text
FRAGMENTED_LOCAL_COLLAPSE remains the strongest attractor.

FRAGMENTED_LOCAL_COLLAPSE remains the strongest basin.

The SCC split remains stable.

Collapse-side nodes keep attractor_score = 3.

Noise-side nodes keep attractor_score = -3.
```

The unstable part:

```text
the strongest bridge alternates between
OSCILLATING_NONPERSISTENT and SPIKE_FILTERED
```

Therefore:

```text
collapse basin = stable
bridge identity = perturbation-sensitive
```

---

## Relation To Attractor v0

Attractor v0 found:

```text
strongest_attractor_candidate = FRAGMENTED_LOCAL_COLLAPSE
strongest_basin_candidate = FRAGMENTED_LOCAL_COLLAPSE
strongest_bridge_candidate = OSCILLATING_NONPERSISTENT
```

Attractor Stability v0 confirms the first two:

```text
strongest_attractor_candidate remains FRAGMENTED_LOCAL_COLLAPSE
strongest_basin_candidate remains FRAGMENTED_LOCAL_COLLAPSE
```

but weakens the third:

```text
strongest_bridge_candidate is not invariant
```

So the updated interpretation is:

```text
the attractor basin is stable;
the bridge role is not yet canonical.
```

---

## Relation To Transition Graph Stability v0

Transition Graph Stability v0 showed that the graph structure remained largely stable:

```text
component_signature_stability_rate = 1.0
mean_edge_persistence_rate = 0.95238
```

Attractor Stability v0 confirms the same macro-structure:

```text
scc_signature_stability_rate = 1.0
```

but adds that bridge identity is sensitive to the one partial edge:

```text
OSCILLATING_NONPERSISTENT -> RECOVERY_RELAPSE_COLLAPSE
```

That explains the bridge instability.

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO because it separates three levels:

```text
class identity
graph/component structure
role identity
```

The first two can be stable while the third can be unstable.

That is a useful measurement distinction.

OMNIATEMPO should not treat “bridge” as a fixed semantic identity yet.

It should treat bridge status as:

```text
role-sensitive
variant-dependent
```

until further stability tests are passed.

---

## Relation To TDelta

For future TDelta work, this means:

```text
basin entry
```

may be more reliable than:

```text
specific bridge-node identity
```

A robust temporal divergence measure should prioritize:

```text
component transition
```

over:

```text
single bridge-class label
```

because the component structure is stable while bridge identity is not.

---

## What This Confirms

This experiment supports:

```text
attractor identity stability

basin identity stability

SCC signature stability

collapse component stability

source/noise component stability

node attractor-score stability

node basin-score stability

node escape-score stability

bridge identity instability
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal attractor stability
universal bridge stability
real-world temporal reliability
semantic correctness
causal correctness
optimal mutation model
probabilistic attractor dynamics
full OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It validates controlled synthetic attractor/basin stability and exposes bridge sensitivity.

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
attractor, basin, bridge, and SCC stability
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
Level 2 — Temporal Topology Attractor Stability
```

Reason:

```text
strongest_attractor_stable = True

strongest_basin_stable = True

scc_signature_stability_rate = 1.0

node attractor_score std = 0.0 for all classes

node basin_score std = 0.0 for all classes

node escape_score std = 0.0 for all classes

but strongest_bridge_stable = False
```

This is a structurally useful CHECK.

It confirms attractor/basin stability while exposing bridge instability.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_bridge_stability_v0.py
```

Purpose:

```text
isolate bridge instability and measure whether
OSCILLATING_NONPERSISTENT and SPIKE_FILTERED
are both legitimate bridge candidates
```

Main question:

```text
is bridge identity truly unstable,
or does the current bridge metric need refinement?
```

Required checks:

```text
bridge score ranking stability

bridge tie detection

partial-edge sensitivity

bridge role under variant shifts

bridge class equivalence

component-crossing contribution
```

Expected structural value:

```text
bridge role clarification
```

---

## Final Result

```text
CHECK — attractor and basin identities remained stable, but bridge identity changed across shifted trajectory variants.
```

Correct final conclusion:

```text
the collapse attractor basin is stable;
the bridge role is perturbation-sensitive and requires a dedicated bridge-stability test.
```