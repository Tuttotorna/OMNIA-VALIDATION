# Temporal Collapse Topology Geometry Sensitivity v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Temporal Topology Geometry-To-Reversibility Mapping
```

---

## Purpose

This experiment measures which trajectory-geometry features control reverse escape depth from:

```text
FRAGMENTED_LOCAL_COLLAPSE
```

to:

```text
OSCILLATING_NONPERSISTENT
```

The previous experiment showed:

```text
boundary-cycle existence is stable,
but reverse escape depth is geometry-sensitive
```

This experiment asks:

```text
which geometric factor causes reverse escape depth
to shift from 3 to 4?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates geometry-to-reversibility mapping under controlled mutation search.

---

## Experiment File

```text
examples/temporal_collapse_topology_geometry_sensitivity_v0.py
```

Result file:

```text
results/temporal_collapse_topology_geometry_sensitivity_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_topology_geometry_sensitivity_v0.py
```

---

## Summary Result

```text
Status: PASS
Version: 0.1.0

variant_count = 10
node_count = 6

confirmation_window = 2
persistence_window = 2
global_persistence_threshold = 4

max_mutation_depth = 4

source_class = FRAGMENTED_LOCAL_COLLAPSE
target_class = OSCILLATING_NONPERSISTENT

reverse_depth_values = [3, 4]

reverse_depths =
[3, 3, 3, 3, 3, 3, 4, 4, 4, 4]

reverse_depth_mean = 3.4
reverse_depth_std = 0.4898979485566356

depth3_count = 6
depth4_count = 4

simple_rule_confirmed = True

inferred_rule =
minimum_reverse_depth = 4 when collapse_run_count >= 4;
otherwise minimum_reverse_depth = 3

run_count_rule_accuracy = 1.0

strongest_feature = collapse_run_count
strongest_abs_correlation = 1.0

geometry_sensitivity_index = 1.4898979485566355

expected_match_rate = 1.0
```

The experiment passed.

The central result is:

```text
geometry-to-reversibility mapping detected
```

---

## Main Finding

The strongest feature controlling reverse escape depth was:

```text
collapse_run_count
```

Measured correlation:

```text
strongest_abs_correlation = 1.0
```

Inferred rule:

```text
minimum_reverse_depth = 4 when collapse_run_count >= 4;
otherwise minimum_reverse_depth = 3
```

Observed mapping:

```text
3 collapse runs -> reverse depth 3
4 collapse runs -> reverse depth 4
```

Correct conclusion:

```text
reverse escape depth is controlled by collapse_run_count
under tested geometries
```

---

## Depth-3 Geometries

The following geometries had reverse escape depth 3:

```text
compact_low_spacing
medium_shifted_spacing
wide_spacing
long_sparse_spacing
front_loaded_geometry
back_loaded_geometry
```

All had:

```text
collapse_run_count = 3
total_collapse_frames = 6
```

This means the following geometrical variations did not break depth 3:

```text
compact spacing
medium spacing
wide spacing
long sparse spacing
front-loaded collapse
back-loaded collapse
```

So in this test, spacing and position were weaker than run count.

---

## Depth-4 Geometries

The following geometries had reverse escape depth 4:

```text
four_spike_oscillation
dense_fragmented_geometry
very_dense_four_run_geometry
sparse_four_run_geometry
```

All had:

```text
collapse_run_count = 4
total_collapse_frames = 8
```

This means the reverse-depth increase was associated with a larger number of confirmed collapse runs.

It was not only caused by density.

The sparse four-run geometry also produced depth 4.

---

## Geometry Records

### Variant 0 — compact_low_spacing

```text
collapse_run_count = 3
trajectory_length = 18
collapse_density_global = 0.3333333333333333
run_spacing_mean = 4
collapse_density_span = 0.6
front_loading_ratio = 0.6666666666666666

minimum_reverse_depth = 3
expected_reverse_depth = 3
predicted_reverse_depth_rule = 3

reverse_example_total = 1600
```

---

### Variant 1 — medium_shifted_spacing

```text
collapse_run_count = 3
trajectory_length = 22
collapse_density_global = 0.2727272727272727
run_spacing_mean = 5
collapse_density_span = 0.5
front_loading_ratio = 0.6666666666666666

minimum_reverse_depth = 3
expected_reverse_depth = 3
predicted_reverse_depth_rule = 3

reverse_example_total = 2112
```

---

### Variant 2 — wide_spacing

```text
collapse_run_count = 3
trajectory_length = 26
collapse_density_global = 0.23076923076923078
run_spacing_mean = 6
collapse_density_span = 0.42857142857142855
front_loading_ratio = 0.6666666666666666

minimum_reverse_depth = 3
expected_reverse_depth = 3
predicted_reverse_depth_rule = 3

reverse_example_total = 2624
```

---

### Variant 3 — long_sparse_spacing

```text
collapse_run_count = 3
trajectory_length = 34
collapse_density_global = 0.17647058823529413
run_spacing_mean = 9
collapse_density_span = 0.3
front_loading_ratio = 0.6666666666666666

minimum_reverse_depth = 3
expected_reverse_depth = 3
predicted_reverse_depth_rule = 3

reverse_example_total = 3648
```

---

### Variant 4 — front_loaded_geometry

```text
collapse_run_count = 3
trajectory_length = 28
collapse_density_global = 0.21428571428571427
run_spacing_mean = 4
collapse_density_span = 0.6
front_loading_ratio = 1.0

minimum_reverse_depth = 3
expected_reverse_depth = 3
predicted_reverse_depth_rule = 3

reverse_example_total = 2880
```

---

### Variant 5 — back_loaded_geometry

```text
collapse_run_count = 3
trajectory_length = 32
collapse_density_global = 0.1875
run_spacing_mean = 5
collapse_density_span = 0.5
front_loading_ratio = 0.0

minimum_reverse_depth = 3
expected_reverse_depth = 3
predicted_reverse_depth_rule = 3

reverse_example_total = 3392
```

---

### Variant 6 — four_spike_oscillation

```text
collapse_run_count = 4
trajectory_length = 30
collapse_density_global = 0.26666666666666666
run_spacing_mean = 5
collapse_density_span = 0.47058823529411764
front_loading_ratio = 0.625

minimum_reverse_depth = 4
expected_reverse_depth = 4
predicted_reverse_depth_rule = 4

reverse_example_total = 256
```

---

### Variant 7 — dense_fragmented_geometry

```text
collapse_run_count = 4
trajectory_length = 28
collapse_density_global = 0.2857142857142857
run_spacing_mean = 4
collapse_density_span = 0.5714285714285714
front_loading_ratio = 0.75

minimum_reverse_depth = 4
expected_reverse_depth = 4
predicted_reverse_depth_rule = 4

reverse_example_total = 256
```

---

### Variant 8 — very_dense_four_run_geometry

```text
collapse_run_count = 4
trajectory_length = 24
collapse_density_global = 0.3333333333333333
run_spacing_mean = 3
collapse_density_span = 0.7272727272727273
front_loading_ratio = 0.75

minimum_reverse_depth = 4
expected_reverse_depth = 4
predicted_reverse_depth_rule = 4

reverse_example_total = 256
```

---

### Variant 9 — sparse_four_run_geometry

```text
collapse_run_count = 4
trajectory_length = 36
collapse_density_global = 0.2222222222222222
run_spacing_mean = 8
collapse_density_span = 0.3076923076923077
front_loading_ratio = 0.5

minimum_reverse_depth = 4
expected_reverse_depth = 4
predicted_reverse_depth_rule = 4

reverse_example_total = 256
```

---

## Feature Correlations With Reverse Depth

```text
trajectory_length                corr = 0.26440136032562617
collapse_run_count               corr = 1.0
total_collapse_frames            corr = 1.0
collapse_density_global          corr = 0.38335304529663844
collapse_density_span            corr = 0.12075710544041504
run_count_density                corr = 0.38335304529663844
run_spacing_mean                 corr = -0.13671718540493266
run_spacing_std                  corr = None
center_spacing_mean              corr = -0.13671718540493266
center_spacing_std               corr = None
run_start_span                   corr = 0.4047499544129309
occupied_span                    corr = 0.4047499544129309
front_loading_ratio              corr = 0.0914360005603718
back_loading_ratio               corr = -0.09143600056037172
geometry_load_bias               corr = -0.39553704377880605
compactness_score                corr = 0.24097762022740862
```

The strongest feature was:

```text
collapse_run_count
```

with:

```text
correlation = 1.0
```

`total_collapse_frames` also had correlation 1.0 because all runs had length 2, so:

```text
total_collapse_frames = collapse_run_count * 2
```

In this dataset, `collapse_run_count` is the more structurally direct variable.

---

## Feature Group Stats

### collapse_run_count

```text
depth3_mean = 3
depth4_mean = 4
difference = 1
```

This is the cleanest separator.

---

### total_collapse_frames

```text
depth3_mean = 6
depth4_mean = 8
difference = 2
```

This follows from run count because every run has length 2.

---

### trajectory_length

```text
depth3_mean = 26.666666666666668
depth4_mean = 29.5
difference = 2.833333333333332
```

Trajectory length had weaker correlation.

It did not explain the rule cleanly.

---

### collapse_density_global

```text
depth3_mean = 0.23584768989180754
depth4_mean = 0.276984126984127
difference = 0.041136437092319456
```

Density increased mildly for depth 4, but it was not the deciding factor.

---

### run_spacing_mean

```text
depth3_mean = 5.5
depth4_mean = 5.0
difference = -0.5
```

Spacing did not control the depth shift.

The sparse four-run geometry still produced depth 4.

---

### geometry_load_bias

```text
depth3_mean = 0.5555555555555556
depth4_mean = 0.3125
difference = -0.24305555555555558
```

Front/back loading did not explain the depth shift.

Both front-loaded and back-loaded three-run geometries remained depth 3.

---

## Inferred Rule

The inferred rule is:

```text
if collapse_run_count >= 4:
    minimum_reverse_depth = 4
else:
    minimum_reverse_depth = 3
```

Observed accuracy:

```text
run_count_rule_accuracy = 1.0
```

Expected match rate:

```text
expected_match_rate = 1.0
```

This means the rule matched every tested geometry.

---

## Structural Meaning

The reverse escape path:

```text
FRAGMENTED_LOCAL_COLLAPSE -> OSCILLATING_NONPERSISTENT
```

is not controlled primarily by where collapse appears.

It is controlled by how many local confirmed collapse runs exist.

This means:

```text
more fragmented confirmed-collapse runs
increase the mutation depth needed to escape
```

In simple form:

```text
3 local collapse runs -> escape depth 3
4 local collapse runs -> escape depth 4
```

So the boundary is not only geometry-sensitive.

It is specifically fragmentation-count-sensitive under the tested geometries.

---

## Relation To Boundary Cycle Stability v0

Boundary Cycle Stability v0 showed:

```text
boundary-cycle existence remained stable,
but reverse escape depth shifted from 3 to 4
```

Geometry Sensitivity v0 explains the shift:

```text
collapse_run_count controlled reverse escape depth
```

The variants with reverse depth 4 were exactly the geometries with four collapse runs.

---

## Relation To Reversibility Index v0

Reversibility Index v0 showed:

```text
FRAGMENTED_LOCAL_COLLAPSE is the most reversible collapse-basin class
```

Geometry Sensitivity v0 refines this:

```text
FRAGMENTED_LOCAL_COLLAPSE is highly reversible,
but its escape depth increases with fragmentation count
```

So the reversibility index should eventually include:

```text
fragmentation-count sensitivity
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO by identifying a structural control variable:

```text
collapse_run_count
```

OMNIATEMPO can now measure:

```text
collapse class
fragmentation count
reverse escape depth
geometry sensitivity
reversibility mapping
```

This turns the temporal topology from classification into a parameterized measurement layer.

---

## Relation To TDelta

This result supports future metrics such as:

```text
TDelta_geometry_sensitivity
TDelta_fragmentation_count
TDelta_reverse_escape_depth

TΔ_geometry_sensitivity
TΔ_fragmentation_count
TΔ_reverse_escape_depth
```

Measured rule:

```text
TΔ_reverse_escape_depth = 3
when collapse_run_count = 3
```

and:

```text
TΔ_reverse_escape_depth = 4
when collapse_run_count = 4
```

A possible early relation:

```text
TΔ_reverse_escape_depth ≈ collapse_run_count
```

under this controlled synthetic family.

This must not be generalized beyond the tested geometry family without further validation.

---

## What This Confirms

This experiment supports:

```text
geometry-to-reversibility mapping detected

reverse escape depth has values 3 and 4

collapse_run_count is the strongest feature

collapse_run_count correlation = 1.0

run_count_rule_accuracy = 1.0

3 collapse runs map to reverse depth 3

4 collapse runs map to reverse depth 4

spacing alone did not control the depth shift

front/back loading did not control the depth shift

reverse escape depth is controlled by collapse_run_count under tested geometries
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal geometry-to-reversibility law
universal relation between collapse_run_count and escape depth
real-world temporal dynamics
semantic correctness
causal correctness
optimal mutation model
probabilistic transition dynamics
full OMNIATEMPO correctness
full TDelta correctness
full OMNIA correctness
```

It validates a controlled synthetic geometry-to-reversibility mapping.

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
which geometry features control reverse escape depth
from FRAGMENTED_LOCAL_COLLAPSE
to OSCILLATING_NONPERSISTENT
under controlled mutation search
```

---

## Limitations

```text
Only ten geometry variants were tested.

Only one source class was tested:
FRAGMENTED_LOCAL_COLLAPSE

Only one target class was tested:
OSCILLATING_NONPERSISTENT

Only mutation depths 1, 2, 3, and 4 were searched.

Only three frame values were allowed:
PASS
ESCALATE
COLLAPSE

All collapse runs had length 2.

Because all run lengths were fixed,
total_collapse_frames and collapse_run_count were perfectly correlated.

The geometries were synthetic.

The mutation graph was deterministic.

No probabilistic transition model was used.

No external temporal dataset was used.

No semantic ground truth exists.

The inferred rule may fail with variable run lengths.
```

---

## Result Classification

Recommended classification:

```text
PASS
```

Evidence level:

```text
Level 2 — Temporal Topology Geometry-To-Reversibility Mapping
```

Reason:

```text
variant_count = 10

simple_rule_confirmed = True

run_count_rule_accuracy = 1.0

expected_match_rate = 1.0

strongest_feature = collapse_run_count

strongest_abs_correlation = 1.0

reverse_depths = [3, 3, 3, 3, 3, 3, 4, 4, 4, 4]
```

This is a successful controlled geometry-to-reversibility mapping experiment.

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
-> collapse_run_count controls reverse escape depth under tested geometries
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_topology_variable_run_length_v0.py
```

Purpose:

```text
separate collapse_run_count from total_collapse_frames
by testing variable collapse-run lengths
```

Main question:

```text
is reverse escape depth controlled by number of runs,
total collapse frames,
or both?
```

Required checks:

```text
same run count with different run lengths

different run count with same total collapse frames

variable run lengths

reverse escape depth

reverse example density

correlation with collapse_run_count

correlation with total_collapse_frames

dominant geometry factor
```

Expected structural value:

```text
run-count vs collapse-mass separation
```

---

## Final Result

```text
PASS — geometry-to-reversibility mapping detected.
```

Correct final conclusion:

```text
reverse escape depth is controlled by collapse_run_count
under tested geometries.
```