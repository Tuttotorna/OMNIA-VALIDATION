# Temporal Collapse Topology Threshold Sensitivity v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Threshold-Parametric Reversibility Probe
```

---

## Purpose

This experiment tests whether the reducible-collapse-mass rule remains coherent when:

```text
CONFIRMATION_WINDOW
```

changes.

The previous experiment found the rule:

```text
minimum_target_depth =
sum(max(0, run_length - 1))
```

for:

```text
CONFIRMATION_WINDOW = 2
```

This experiment generalizes the rule across:

```text
CONFIRMATION_WINDOW = 2
CONFIRMATION_WINDOW = 3
CONFIRMATION_WINDOW = 4
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates threshold-parametric reversibility behavior under the temporal topology classifier.

---

## Experiment File

```text
examples/temporal_collapse_topology_threshold_sensitivity_v0.py
```

Result file:

```text
results/temporal_collapse_topology_threshold_sensitivity_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_threshold_sensitivity_v0.py
```

---

## Summary Result

```text
Status: CHECK
Version: 0.1.0

variant_count = 12
flat_record_count = 36
node_count = 6

confirmation_windows = [2, 3, 4]
persistence_window = 2

target_class = OSCILLATING_NONPERSISTENT

depth_values_all =
[0, 1, 3, 4, 5, 6, 8, 9, 10, 12]

target_reachable_rate = 0.9166666666666666

all_depths_monotonic_nonincreasing = True

class_transition_count = 10

parametric_rule_holds = True

threshold_parametric_law_detected = False

generalized_rule =
minimum_target_depth = sum(max(0, run_length - (confirmation_window - 1)))

method = threshold_parametric_analytical_rule
```

The result is `CHECK`.

The formula held exactly, but the requested target class was not reachable in every geometry.

---

## Main Finding

The generalized threshold rule was confirmed:

```text
parametric_rule_holds = True
failure_count = 0
```

The rule is:

```text
minimum_target_depth =
sum(max(0, run_length - (confirmation_window - 1)))
```

Also:

```text
all_depths_monotonic_nonincreasing = True
```

This means that increasing the confirmation window never increased the required target depth.

However:

```text
target_reachable_rate = 0.9166666666666666
```

not:

```text
1.0
```

Therefore the full law targeting `OSCILLATING_NONPERSISTENT` was not universally confirmed.

Correct conclusion:

```text
thresholded reducible-mass rule confirmed;
target-class reachability depends on run_count
```

---

## Why Status Is CHECK

The only structural problem is target reachability.

The geometry:

```text
long_single_run
```

has only one collapse run:

```text
runs = [7]
```

After reduction below the confirmation threshold, the sequence becomes:

```text
SPIKE_FILTERED
```

not:

```text
OSCILLATING_NONPERSISTENT
```

So the formula correctly computes the depth needed to reduce the run below threshold, but the resulting target class is not always `OSCILLATING_NONPERSISTENT`.

That is why:

```text
parametric_rule_holds = True
```

but:

```text
threshold_parametric_law_detected = False
```

This is a useful `CHECK`, not a failure.

---

## Generalized Rule

For any confirmation window:

```text
C = confirmation_window
```

a run must be reduced to:

```text
C - 1
```

or less.

Therefore each run of length `L` contributes:

```text
max(0, L - (C - 1))
```

to the minimum target depth.

Full rule:

```text
minimum_target_depth =
sum(max(0, run_length - (confirmation_window - 1)))
```

For the tested windows:

```text
CONFIRMATION_WINDOW = 2
run must become <= 1

CONFIRMATION_WINDOW = 3
run must become <= 2

CONFIRMATION_WINDOW = 4
run must become <= 3
```

---

## By Threshold

### CONFIRMATION_WINDOW = 2

```text
depth_values =
[0, 3, 4, 6, 8, 9, 10, 12]

mean_depth = 6.5
std = 3.095695936834452

source_class_counts =
{
  FRAGMENTED_LOCAL_COLLAPSE: 4,
  RECOVERY_RELAPSE_COLLAPSE: 6,
  GLOBAL_PERSISTENT_COLLAPSE: 1,
  OSCILLATING_NONPERSISTENT: 1
}

target_reachable_rate = 0.9166666666666666
```

At confirmation window 2, the threshold is strict.

More runs count as confirmed collapse, and target depth is highest.

---

### CONFIRMATION_WINDOW = 3

```text
depth_values =
[0, 3, 4, 5, 6, 8]

mean_depth = 3.6666666666666665
std = 2.560381915956203

source_class_counts =
{
  OSCILLATING_NONPERSISTENT: 3,
  FRAGMENTED_LOCAL_COLLAPSE: 6,
  GLOBAL_PERSISTENT_COLLAPSE: 1,
  RECOVERY_RELAPSE_COLLAPSE: 2
}

target_reachable_rate = 0.9166666666666666
```

At confirmation window 3, some previously confirmed collapses become nonpersistent.

Target depth drops.

---

### CONFIRMATION_WINDOW = 4

```text
depth_values =
[0, 1, 3, 4]

mean_depth = 1.6666666666666667
std = 1.699673171197595

source_class_counts =
{
  OSCILLATING_NONPERSISTENT: 5,
  FRAGMENTED_LOCAL_COLLAPSE: 6,
  GLOBAL_PERSISTENT_COLLAPSE: 1
}

target_reachable_rate = 0.9166666666666666
```

At confirmation window 4, target depth drops further.

This confirms monotonic threshold behavior.

---

## Geometry Records

### Variant 0 — three_runs_len_2

```text
runs = [2, 2, 2]
mass = 6

depths =
{
  2: 3,
  3: 0,
  4: 0
}

classes =
{
  2: FRAGMENTED_LOCAL_COLLAPSE,
  3: OSCILLATING_NONPERSISTENT,
  4: OSCILLATING_NONPERSISTENT
}
```

Interpretation:

```text
length-2 runs are confirmed when C=2,
but not confirmed when C>=3.
```

---

### Variant 1 — three_runs_len_3

```text
runs = [3, 3, 3]
mass = 9

depths =
{
  2: 6,
  3: 3,
  4: 0
}

classes =
{
  2: FRAGMENTED_LOCAL_COLLAPSE,
  3: FRAGMENTED_LOCAL_COLLAPSE,
  4: OSCILLATING_NONPERSISTENT
}
```

Interpretation:

```text
length-3 runs remain confirmed for C=2 and C=3,
but not for C=4.
```

---

### Variant 2 — three_runs_len_4

```text
runs = [4, 4, 4]
mass = 12

depths =
{
  2: 9,
  3: 6,
  4: 3
}

classes =
{
  2: RECOVERY_RELAPSE_COLLAPSE,
  3: FRAGMENTED_LOCAL_COLLAPSE,
  4: FRAGMENTED_LOCAL_COLLAPSE
}
```

Interpretation:

```text
longer confirmed runs keep nonzero target depth across all tested thresholds.
```

---

### Variant 3 — four_runs_len_2

```text
runs = [2, 2, 2, 2]
mass = 8

depths =
{
  2: 4,
  3: 0,
  4: 0
}

classes =
{
  2: FRAGMENTED_LOCAL_COLLAPSE,
  3: OSCILLATING_NONPERSISTENT,
  4: OSCILLATING_NONPERSISTENT
}
```

Interpretation:

```text
four length-2 runs are collapse only at C=2.
```

---

### Variant 4 — four_runs_len_3

```text
runs = [3, 3, 3, 3]
mass = 12

depths =
{
  2: 8,
  3: 4,
  4: 0
}

classes =
{
  2: FRAGMENTED_LOCAL_COLLAPSE,
  3: FRAGMENTED_LOCAL_COLLAPSE,
  4: OSCILLATING_NONPERSISTENT
}
```

Interpretation:

```text
the required depth decreases exactly as threshold increases.
```

---

### Variant 5 — four_runs_len_4

```text
runs = [4, 4, 4, 4]
mass = 16

depths =
{
  2: 12,
  3: 8,
  4: 4
}

classes =
{
  2: RECOVERY_RELAPSE_COLLAPSE,
  3: FRAGMENTED_LOCAL_COLLAPSE,
  4: FRAGMENTED_LOCAL_COLLAPSE
}
```

Interpretation:

```text
four long runs stay structurally confirmed under all tested thresholds.
```

---

### Variant 6 — mixed_2_3_4

```text
runs = [2, 3, 4]
mass = 9

depths =
{
  2: 6,
  3: 3,
  4: 1
}

classes =
{
  2: RECOVERY_RELAPSE_COLLAPSE,
  3: FRAGMENTED_LOCAL_COLLAPSE,
  4: FRAGMENTED_LOCAL_COLLAPSE
}
```

Interpretation:

```text
mixed run lengths produce a graded threshold response.
```

---

### Variant 7 — mixed_1_2_3_4

```text
runs = [1, 2, 3, 4]
mass = 10

depths =
{
  2: 6,
  3: 3,
  4: 1
}

classes =
{
  2: RECOVERY_RELAPSE_COLLAPSE,
  3: FRAGMENTED_LOCAL_COLLAPSE,
  4: FRAGMENTED_LOCAL_COLLAPSE
}
```

Interpretation:

```text
the length-1 run contributes zero across all tested thresholds.
```

---

### Variant 8 — long_single_run

```text
runs = [7]
mass = 7

depths =
{
  2: 6,
  3: 5,
  4: 4
}

classes =
{
  2: GLOBAL_PERSISTENT_COLLAPSE,
  3: GLOBAL_PERSISTENT_COLLAPSE,
  4: GLOBAL_PERSISTENT_COLLAPSE
}
```

Interpretation:

```text
the depth formula holds,
but target class after reduction is SPIKE_FILTERED,
not OSCILLATING_NONPERSISTENT.
```

This is the reason for `CHECK`.

---

### Variant 9 — relapse_two_long_runs

```text
runs = [5, 5]
mass = 10

depths =
{
  2: 8,
  3: 6,
  4: 4
}

classes =
{
  2: RECOVERY_RELAPSE_COLLAPSE,
  3: RECOVERY_RELAPSE_COLLAPSE,
  4: FRAGMENTED_LOCAL_COLLAPSE
}
```

Interpretation:

```text
two long runs remain target-reachable as OSCILLATING_NONPERSISTENT
after reduction below threshold.
```

---

### Variant 10 — all_spikes_len_1

```text
runs = [1, 1, 1, 1, 1]
mass = 5

depths =
{
  2: 0,
  3: 0,
  4: 0
}

classes =
{
  2: OSCILLATING_NONPERSISTENT,
  3: OSCILLATING_NONPERSISTENT,
  4: OSCILLATING_NONPERSISTENT
}
```

Interpretation:

```text
all runs are below every tested confirmation threshold.
```

---

### Variant 11 — mixed_threshold_boundary

```text
runs = [2, 3, 4, 5]
mass = 14

depths =
{
  2: 10,
  3: 6,
  4: 3
}

classes =
{
  2: RECOVERY_RELAPSE_COLLAPSE,
  3: RECOVERY_RELAPSE_COLLAPSE,
  4: FRAGMENTED_LOCAL_COLLAPSE
}
```

Interpretation:

```text
a mixed threshold-boundary case follows the generalized formula exactly.
```

---

## Strongest Features By Threshold

```text
confirmation_window = 2
strongest_feature = collapse_density_global
abs_corr = 0.9475021705473168

confirmation_window = 3
strongest_feature = total_collapse_frames
abs_corr = 0.821196563691916

confirmation_window = 4
strongest_feature = run_length_mean
abs_corr = 0.8255019780771843
```

Interpretation:

```text
the strongest simple feature changes with threshold.
```

This confirms that threshold choice affects which coarse geometry feature appears most predictive.

The exact rule remains thresholded reducible mass.

---

## Rule Validation

```text
parametric_rule_holds = True
failure_count = 0
failures = []
```

This is the strongest result in the experiment.

The formula made no depth errors.

---

## Target Reachability

The target was:

```text
OSCILLATING_NONPERSISTENT
```

Reachability result:

```text
target_reachable_count = 33
flat_record_count = 36
target_reachable_rate = 0.9166666666666666
```

The three non-reachable cases are the same geometry across three thresholds:

```text
long_single_run
```

Reason:

```text
single run reduced below threshold -> SPIKE_FILTERED
multiple sub-threshold runs -> OSCILLATING_NONPERSISTENT
```

So the missing condition is:

```text
target-class reachability requires enough remaining sub-threshold runs
to be classified as OSCILLATING_NONPERSISTENT.
```

---

## Structural Meaning

The thresholded mass rule is valid:

```text
minimum_target_depth =
sum(max(0, run_length - (confirmation_window - 1)))
```

But target class identity requires an additional condition.

Correct structural refinement:

```text
depth law = thresholded reducible collapse mass

target class law = depends on remaining run count after reduction
```

Therefore the complete model is two-layered:

```text
Layer 1:
how many edits are needed to reduce every run below confirmation?

Layer 2:
what class results after all confirmed runs are reduced below confirmation?
```

The first layer passed.

The second layer exposed a boundary case.

---

## Relation To Variable Run Length v0

Variable Run Length v0 found:

```text
minimum_target_depth =
sum(max(0, run_length - 1))
```

Threshold Sensitivity v0 generalizes it:

```text
minimum_target_depth =
sum(max(0, run_length - (confirmation_window - 1)))
```

So the prior result was the special case:

```text
confirmation_window = 2
```

---

## Relation To Geometry Sensitivity v0

Geometry Sensitivity v0 found that fixed run-length geometries appeared controlled by:

```text
collapse_run_count
```

Variable Run Length v0 refined that to:

```text
reducible collapse mass
```

Threshold Sensitivity v0 now refines it further:

```text
thresholded reducible collapse mass
```

This gives the correct hierarchy:

```text
fixed run length:
collapse_run_count approximates depth

variable run length:
reducible collapse mass determines depth

variable confirmation threshold:
thresholded reducible collapse mass determines depth
```

---

## Relation To OMNIATEMPO

This result strengthens OMNIATEMPO by making reversibility threshold-parametric.

OMNIATEMPO can now represent:

```text
confirmation_window
collapse run lengths
thresholded reducible collapse mass
minimum target depth
post-reduction target class
```

This is stronger than a fixed-threshold classifier.

It gives the temporal topology a parameterized structural law.

---

## Relation To TDelta

This result supports a threshold-parametric `TDelta` form:

```text
TΔ_thresholded_reducible_mass(C) =
sum(max(0, run_length - (C - 1)))
```

where:

```text
C = confirmation_window
```

Measured target depth follows:

```text
minimum_target_depth = TΔ_thresholded_reducible_mass(C)
```

inside this classifier family.

---

## What This Confirms

This experiment supports:

```text
thresholded reducible-mass rule confirmed

parametric_rule_holds = True

failure_count = 0

depths are monotonic nonincreasing as confirmation_window increases

class transitions occur when threshold changes

minimum target depth follows the generalized formula

threshold choice affects source classification

target reachability depends on run count after reduction
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal temporal reversibility law
universal target-class reachability
real-world temporal dynamics
semantic correctness
causal correctness
optimal confirmation thresholds
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates a controlled threshold-parametric analytical rule inside the tested classifier family.

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
threshold-parametric minimum target depth
under temporal collapse-run geometry
```

---

## Limitations

```text
This is an analytical shortcut, not brute-force mutation enumeration.

The result depends on the current classifier rules.

Only confirmation windows 2, 3, and 4 were tested.

Persistence window was fixed at 2.

Only synthetic trajectories were tested.

Only three frame values were used:
PASS
ESCALATE
COLLAPSE

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

Target reachability was defined specifically for OSCILLATING_NONPERSISTENT.

A different target class would produce a different reachability result.
```

---

## Result Classification

Recommended classification:

```text
CHECK
```

Evidence level:

```text
Level 2 — Temporal Topology Threshold-Parametric Reversibility Probe
```

Reason:

```text
parametric_rule_holds = True

failure_count = 0

all_depths_monotonic_nonincreasing = True

target_reachable_rate = 0.9166666666666666

threshold_parametric_law_detected = False
```

This is a successful formula validation with a target-reachability boundary exposed.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_target_reachability_v0.py
```

Purpose:

```text
separate depth law from target-class reachability law
```

Main question:

```text
after reducing all confirmed runs below threshold,
which target class is reached?
```

Required checks:

```text
single-run cases

multi-run cases

zero-run cases

SPIKE_FILTERED target

OSCILLATING_NONPERSISTENT target

CLEAN_PASS target

remaining run count

post-reduction class

target reachability map
```

Expected structural value:

```text
post-reduction target-class law
```

---

## Final Result

```text
CHECK — thresholded reducible-mass rule confirmed,
but target-class reachability depends on run_count.
```

Correct final conclusion:

```text
the depth law is threshold-parametric and valid,
but the final target class requires a separate reachability rule.
```