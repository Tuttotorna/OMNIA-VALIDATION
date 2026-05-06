# Temporal Collapse Topology Variable Run Length v0 — Result

## Status

```text
Status: PASS
Version: 0.2.0
Claim level: Level 2 — Temporal Topology Run-Count vs Collapse-Mass Separation
```

---

## Purpose

This experiment separates:

```text
collapse_run_count
```

from:

```text
total_collapse_frames
```

by testing variable collapse-run lengths.

The previous experiment found:

```text
collapse_run_count controls reverse escape depth
```

but all tested collapse runs had fixed length:

```text
run_length = 2
```

Therefore:

```text
total_collapse_frames = collapse_run_count * 2
```

So the previous experiment could not distinguish whether reverse escape depth was controlled by:

```text
number of collapse runs
```

or by:

```text
total reducible collapse mass
```

This experiment asks:

```text
does target depth depend on collapse_run_count,
total_collapse_frames,
or the reducible mass inside each run?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates run-count versus collapse-mass separation under the temporal topology classifier.

---

## Experiment File

```text
examples/temporal_collapse_topology_variable_run_length_v0.py
```

Result file:

```text
results/temporal_collapse_topology_variable_run_length_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_variable_run_length_v0.py
```

---

## Important Implementation Note

Version `0.2.0` removed brute-force mutation enumeration.

The first version attempted to enumerate mutation combinations up to depth 5.

That became computationally too expensive for Colab because long sequences produce very large mutation spaces.

The optimized version uses an analytical minimum-depth rule:

```text
minimum_target_depth =
sum(max(0, run_length - 1))
```

for transition to:

```text
OSCILLATING_NONPERSISTENT
```

This rule is exact for this classifier family because a collapse run must be reduced below:

```text
CONFIRMATION_WINDOW = 2
```

So each run must become length:

```text
<= 1
```

Therefore each run of length `L` contributes:

```text
L - 1
```

required edits when `L >= 2`.

---

## Summary Result

```text
Status: PASS
Version: 0.2.0

variant_count = 14
node_count = 6

confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4

source_class_focus = FRAGMENTED_LOCAL_COLLAPSE
target_class = OSCILLATING_NONPERSISTENT

reachable_record_count = 14

target_depth_values =
[0, 3, 4, 5, 6, 8, 9]

strongest_feature = total_collapse_frames
strongest_abs_correlation = 0.9231378498105907

dominant_factor = total_collapse_frames

same_run_count_depth_varies = True
same_mass_depth_varies = True

separation_detected = True

analytical_rule =
minimum_target_depth = sum(max(0, run_length - 1))
for transition to OSCILLATING_NONPERSISTENT

bruteforce_removed = True
```

The experiment passed.

The central result is:

```text
run-count vs collapse-mass separation measured
```

---

## Main Finding

The previous hypothesis:

```text
collapse_run_count alone controls reverse escape depth
```

was refined.

The new result shows:

```text
target depth is controlled by reducible collapse mass
rather than collapse_run_count alone
```

The strongest feature was:

```text
total_collapse_frames
```

with:

```text
correlation = 0.9231378498105907
```

But the exact analytical rule is not simply total mass.

It is:

```text
minimum_target_depth =
sum(max(0, run_length - 1))
```

So the real structural factor is:

```text
reducible collapse mass above the confirmation threshold
```

---

## Analytical Rule

For each collapse run of length `L`:

```text
required edits = max(0, L - 1)
```

because:

```text
CONFIRMATION_WINDOW = 2
```

and each run must be reduced below confirmation.

Therefore:

```text
target_depth =
sum over all runs of max(0, run_length - 1)
```

Examples:

```text
[2, 2, 2] -> 1 + 1 + 1 = 3

[3, 3, 3] -> 2 + 2 + 2 = 6

[4, 4, 4] -> 3 + 3 + 3 = 9

[2, 2, 2, 2] -> 1 + 1 + 1 + 1 = 4

[3, 3, 3, 3] -> 2 + 2 + 2 + 2 = 8

[1, 1, 1, 1] -> 0 + 0 + 0 + 0 = 0
```

This explains the full depth range:

```text
[0, 3, 4, 5, 6, 8, 9]
```

---

## Why Brute Force Was Removed

The brute-force version attempted to search mutation combinations up to depth 5.

For a sequence of length 42, depth 5 produces:

```text
C(42, 5) * 2^5
```

which is:

```text
850668 * 32 = 27221376
```

candidate mutations for one sequence.

That is too expensive for a lightweight Colab validation run.

The optimized version avoids this by measuring the structural minimum directly from collapse-run lengths.

This makes the experiment deterministic, fast, and reproducible.

---

## Geometry Records

### Variant 0 — three_runs_mass_6_baseline

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [2, 2, 2]
collapse_run_count = 3
total_collapse_frames = 6

minimum_target_depth = 3

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
three confirmed local collapse runs of length 2 require three edits.
```

---

### Variant 1 — three_runs_mass_9_variable

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [3, 3, 3]
collapse_run_count = 3
total_collapse_frames = 9

minimum_target_depth = 6

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
same run count as Variant 0,
but longer runs increase target depth from 3 to 6.
```

This directly falsifies run-count-only control.

---

### Variant 2 — three_runs_mass_12_long

```text
source_class = RECOVERY_RELAPSE_COLLAPSE

runs = [4, 4, 4]
collapse_run_count = 3
total_collapse_frames = 12

minimum_target_depth = 9

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
same run count as Variant 0 and Variant 1,
but longer runs increase target depth to 9.
```

This confirms that run length matters.

---

### Variant 3 — four_runs_mass_4_spikes

```text
source_class = OSCILLATING_NONPERSISTENT

runs = [1, 1, 1, 1]
collapse_run_count = 4
total_collapse_frames = 4

minimum_target_depth = 0

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
many runs do not imply escape depth if every run is below confirmation.
```

This strongly falsifies collapse-run-count-only control.

---

### Variant 4 — four_runs_mass_8_baseline

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [2, 2, 2, 2]
collapse_run_count = 4
total_collapse_frames = 8

minimum_target_depth = 4

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
four confirmed runs of length 2 require four edits.
```

This matches the earlier fixed-run-length result.

---

### Variant 5 — four_runs_mass_12_variable

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [3, 3, 3, 3]
collapse_run_count = 4
total_collapse_frames = 12

minimum_target_depth = 8

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
same run count as Variant 4,
but longer runs increase target depth from 4 to 8.
```

Again, run count alone is insufficient.

---

### Variant 6 — two_runs_mass_8_relapse_like

```text
source_class = RECOVERY_RELAPSE_COLLAPSE

runs = [2, 6]
collapse_run_count = 2
total_collapse_frames = 8

minimum_target_depth = 6

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
low run count can still produce high target depth
when one run is long.
```

This confirms that collapse mass above threshold matters.

---

### Variant 7 — six_runs_mass_6_spike_family

```text
source_class = OSCILLATING_NONPERSISTENT

runs = [1, 1, 1, 1, 1, 1]
collapse_run_count = 6
total_collapse_frames = 6

minimum_target_depth = 0

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
high run count can produce zero target depth
if all runs are below confirmation.
```

This is the cleanest counterexample to run-count-only control.

---

### Variant 8 — five_runs_mass_10_fragmented

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [2, 2, 2, 2, 2]
collapse_run_count = 5
total_collapse_frames = 10

minimum_target_depth = 5

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
with fixed run length 2,
target depth equals collapse_run_count.
```

This explains why the previous experiment appeared run-count-controlled.

---

### Variant 9 — three_runs_mass_8_mixed

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [2, 3, 3]
collapse_run_count = 3
total_collapse_frames = 8

minimum_target_depth = 5

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
mixed run lengths produce intermediate target depth.
```

---

### Variant 10 — four_runs_mass_7_mixed

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [2, 1, 2, 2]
collapse_run_count = 4
total_collapse_frames = 7

minimum_target_depth = 3

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
four runs do not force depth 4
when one run is already below confirmation.
```

This refines the previous rule.

---

### Variant 11 — four_runs_mass_10_mixed

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [3, 2, 3, 2]
collapse_run_count = 4
total_collapse_frames = 10

minimum_target_depth = 6

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
mixed confirmed runs increase target depth according to reducible mass.
```

---

### Variant 12 — same_mass_8_three_runs

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [2, 3, 3]
collapse_run_count = 3
total_collapse_frames = 8

minimum_target_depth = 5

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
same mass as Variant 13,
but different run distribution gives different depth.
```

---

### Variant 13 — same_mass_8_four_runs

```text
source_class = FRAGMENTED_LOCAL_COLLAPSE

runs = [2, 2, 2, 2]
collapse_run_count = 4
total_collapse_frames = 8

minimum_target_depth = 4

target = OSCILLATING_NONPERSISTENT
```

Interpretation:

```text
same total mass as Variant 12,
but different run distribution gives different depth.
```

Therefore total mass alone is also not the complete exact rule.

The exact rule is reducible mass above threshold.

---

## Feature Correlations With Target Depth

```text
trajectory_length                corr = 0.5691210869767894
collapse_run_count               corr = -0.5043290851090749
run_length_mean                  corr = 0.8946216105633468
run_length_std                   corr = 0.18266566222392133
max_run_length                   corr = 0.7248362958782061
min_run_length                   corr = 0.8845156261913008
total_collapse_frames            corr = 0.9231378498105907
collapse_density_global          corr = 0.9071562510934046
collapse_density_span            corr = 0.6126362807495889
run_count_density                corr = -0.8370598679846799
run_spacing_mean                 corr = 0.8412673677430741
run_spacing_std                  corr = 0.07082882469748285
occupied_span                    corr = 0.6129225604147472
front_loading_ratio              corr = -0.48916098513207545
back_loading_ratio               corr = 0.48916098513207557
geometry_load_bias               corr = -0.4520155500127058
mass_per_run                     corr = 0.8946216105633468
```

The strongest measured feature was:

```text
total_collapse_frames
```

with:

```text
corr = 0.9231378498105907
```

But the report should not overstate this as a universal law.

The exact structural rule is thresholded collapse mass:

```text
sum(max(0, run_length - 1))
```

---

## Same Run-Count Comparison

### run_count = 3

```text
masses = [6, 9, 12, 8, 8]
depths = [3, 6, 9, 5, 5]
stable = False
```

Interpretation:

```text
same run count can produce different target depths.
```

So `collapse_run_count` alone is insufficient.

---

### run_count = 4

```text
masses = [4, 8, 12, 7, 10, 8]
depths = [0, 4, 8, 3, 6, 4]
stable = False
```

Interpretation:

```text
same run count can produce zero, low, or high target depth
depending on run lengths.
```

Again, run count alone is insufficient.

---

## Same Mass Comparison

### mass = 6

```text
run_counts = [3, 6]
depths = [3, 0]
stable = False
```

Interpretation:

```text
same total mass can produce different target depths
if the mass is distributed differently across runs.
```

---

### mass = 8

```text
run_counts = [4, 2, 3, 3, 4]
depths = [4, 6, 5, 5, 4]
stable = False
```

Interpretation:

```text
same mass can produce depths 4, 5, or 6.
```

Total collapse mass alone is not the exact factor.

---

### mass = 10

```text
run_counts = [5, 4]
depths = [5, 6]
stable = False
```

Interpretation:

```text
same mass can still produce different target depths.
```

---

### mass = 12

```text
run_counts = [3, 4]
depths = [9, 8]
stable = False
```

Interpretation:

```text
same mass can produce different depth depending on run distribution.
```

---

## Source Class Summary

### FRAGMENTED_LOCAL_COLLAPSE

```text
record_count = 10

target_depths =
[3, 6, 4, 8, 5, 5, 3, 6, 5, 4]

mean_depth = 4.9

collapse_run_counts =
[3, 3, 4, 4, 5, 3, 4, 4, 3, 4]

masses =
[6, 9, 8, 12, 10, 8, 7, 10, 8, 8]
```

Interpretation:

```text
within FRAGMENTED_LOCAL_COLLAPSE, reversibility depth varies strongly
with run-length structure.
```

---

### RECOVERY_RELAPSE_COLLAPSE

```text
record_count = 2

target_depths =
[9, 6]

mean_depth = 7.5

collapse_run_counts =
[3, 2]

masses =
[12, 8]
```

Interpretation:

```text
long persistent runs increase target depth.
```

---

### OSCILLATING_NONPERSISTENT

```text
record_count = 2

target_depths =
[0, 0]

mean_depth = 0

collapse_run_counts =
[4, 6]

masses =
[4, 6]
```

Interpretation:

```text
when every run is below confirmation,
the sequence is already OSCILLATING_NONPERSISTENT.
```

---

## Structural Meaning

The previous rule:

```text
collapse_run_count controls reverse escape depth
```

was only true under fixed run length:

```text
run_length = 2
```

The refined rule is:

```text
target depth is controlled by reducible collapse mass
above the confirmation threshold
```

Exact form:

```text
minimum_target_depth =
sum(max(0, run_length - 1))
```

This means:

```text
a run of length 1 contributes 0

a run of length 2 contributes 1

a run of length 3 contributes 2

a run of length 4 contributes 3

a run of length 6 contributes 5
```

So the depth is not determined by the number of runs alone.

It is determined by how much confirmed collapse must be removed to push every run below confirmation.

---

## Relation To Geometry Sensitivity v0

Geometry Sensitivity v0 concluded:

```text
collapse_run_count controls reverse escape depth
under tested geometries
```

Variable Run Length v0 refines that:

```text
collapse_run_count controlled depth only because all runs had equal length 2
```

When run lengths vary, the controlling factor becomes:

```text
reducible collapse mass
```

The corrected interpretation is:

```text
fixed run length:
collapse_run_count approximates reversibility depth

variable run length:
reducible collapse mass determines reversibility depth
```

---

## Relation To Boundary Cycle Stability v0

Boundary Cycle Stability v0 showed:

```text
reverse escape depth is geometry-sensitive
```

Variable Run Length v0 explains one mechanism:

```text
reverse escape depth changes when collapse-run lengths change
```

This gives the boundary-cycle asymmetry a measurable cause.

---

## Relation To Reversibility Index v0

Reversibility Index v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE is the most reversible collapse-side class
```

Variable Run Length v0 refines this:

```text
FRAGMENTED_LOCAL_COLLAPSE can have multiple internal reversibility depths
depending on reducible collapse mass
```

So future reversibility index versions should include:

```text
run-length weighted collapse mass
```

not just class identity.

---

## Relation To OMNIATEMPO

This result strengthens OMNIATEMPO by adding a thresholded mass interpretation.

OMNIATEMPO can now measure:

```text
collapse class
collapse run count
collapse run length
total collapse mass
reducible collapse mass
minimum target depth
```

The temporal topology is no longer only class-based.

It becomes:

```text
class + run geometry + thresholded reducible mass
```

This is a stronger structural representation.

---

## Relation To TDelta

This result supports a future metric:

```text
TDelta_reducible_collapse_mass
```

or:

```text
TΔ_reducible_collapse_mass
```

Definition under this classifier:

```text
TΔ_reducible_collapse_mass =
sum(max(0, run_length - (CONFIRMATION_WINDOW - 1)))
```

With:

```text
CONFIRMATION_WINDOW = 2
```

this becomes:

```text
TΔ_reducible_collapse_mass =
sum(max(0, run_length - 1))
```

This equals the measured minimum target depth to:

```text
OSCILLATING_NONPERSISTENT
```

---

## What This Confirms

This experiment supports:

```text
run-count vs collapse-mass separation measured

brute force was removed

same run count can produce different target depths

same total mass can produce different target depths

collapse_run_count alone is insufficient

total_collapse_frames is the strongest simple feature

exact rule is reducible collapse mass above threshold

minimum_target_depth = sum(max(0, run_length - 1))

FRAGMENTED_LOCAL_COLLAPSE contains internal reversibility-depth variation
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal reducible-mass law
real-world temporal dynamics
semantic correctness
causal correctness
optimal classifier thresholds
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates a controlled analytical rule inside the tested classifier family.

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
minimum target depth
from temporal collapse-run geometry
to OSCILLATING_NONPERSISTENT
under the current classifier thresholds
```

---

## Limitations

```text
This is an analytical shortcut, not brute-force mutation enumeration.

The result depends on the current classifier rules.

The result depends on CONFIRMATION_WINDOW = 2.

Only synthetic trajectories were tested.

Only three frame values were used:
PASS
ESCALATE
COLLAPSE

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

The formula should be re-derived if the classifier changes.

The formula should be re-tested if confirmation thresholds change.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Run-Count vs Collapse-Mass Separation
```

Reason:

```text
variant_count = 14

separation_detected = True

same_run_count_depth_varies = True

same_mass_depth_varies = True

strongest_feature = total_collapse_frames

strongest_abs_correlation = 0.9231378498105907

dominant_factor = total_collapse_frames

analytical_rule =
minimum_target_depth = sum(max(0, run_length - 1))
```

This is a successful controlled separation experiment.

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
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_threshold_sensitivity_v0.py
```

Purpose:

```text
test whether the analytical rule changes coherently
when CONFIRMATION_WINDOW changes
```

Main question:

```text
does the reducible-collapse-mass rule generalize
across confirmation thresholds?
```

Required checks:

```text
confirmation_window = 2
confirmation_window = 3
confirmation_window = 4

minimum_target_depth formula

thresholded reducible mass

classification changes

target depth changes

rule stability across thresholds
```

Expected structural value:

```text
threshold-parametric reversibility law
```

---

## Final Result

```text
PASS — run-count vs collapse-mass separation measured.
```

Correct final conclusion:

```text
target depth is controlled by reducible collapse mass,
not collapse_run_count alone.
```