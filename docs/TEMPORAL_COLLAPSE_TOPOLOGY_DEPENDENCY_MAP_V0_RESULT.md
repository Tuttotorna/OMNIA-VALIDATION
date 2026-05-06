# Temporal Collapse Topology Dependency Map v0 — Result

## File

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_DEPENDENCY_MAP_V0_RESULT.md

Experiment

temporal_collapse_topology_dependency_map_v0

Status

PASS

Version

0.1.0

Reproduction

python examples/temporal_collapse_topology_dependency_map_v0.py

Purpose

This experiment tests whether the previously detected temporal-collapse control plane depends on specific structural axes.

The tested axes are:

family structure

confirmation threshold

individual geometry variant


The goal is not to prove that the control plane is universally invariant.

The goal is to measure where the control plane remains stable, where it drifts, and where it breaks.

Baseline

The baseline control plane was detected successfully.

baseline_status: PASS
baseline_strict_status: PASS

Expected dominant control cluster:

cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

Expected second control cluster:

cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

Summary

dependency_scenario_count: 28
dependency_record_count: 28
critical_dependency_count: 10
moderate_dependency_count: 2
stable_support_count: 16
control_plane_dependency_map_detected: True
method: control_plane_dependency_map

Main Result

The experiment detected a measurable dependency map for the control plane.

The control plane is not unconditional.

It depends on specific families and thresholds. Some perturbations preserve it, some move it, and some destroy or invert its expected rank structure.

Dependency Classes

The experiment separates perturbations into three classes.

CRITICAL_ABSENCE

The expected control cluster is no longer present.

This is the strongest failure mode.

CRITICAL_TOP6_LOSS

The expected pair remains measurable but falls out of the top control layer.

This means the control plane is still structurally present but no longer dominant.

CRITICAL_ORDER_INVERSION

The expected pair is still present, but the order is inverted.

This means the second expected cluster becomes stronger than the expected dominant cluster.

MODERATE_RANK_DRIFT

The expected pair remains present and correctly ordered, but rank position changes.

This is a weaker instability.

STABLE_SUPPORT

The perturbation does not damage the expected control-plane relation.

By Dependency Axis

Family Axis

scenario_count: 14
pass_count: 8
check_count: 6
strict_pass_count: 7
pass_rate: 0.5714285714285714
strict_pass_rate: 0.5
impact_score_mean: 68.71428571428571
impact_score_max: 181.0

Critical family targets:

dense_short
single_run
spike_plus_long
staircase
three_equal_runs
two_equal_runs

Stable family targets:

dense_short
mixed_same_cost
single_run
spike_plus_long
staircase
three_equal_runs
two_equal_runs

Interpretation:

The family axis is not uniformly stable.

Some families can be removed without damaging the control plane.

But isolating certain families produces critical absence because a single family alone does not contain enough structure to preserve the global control-plane relation.

The strongest family-axis failure is:

keep_only_family__spike_plus_long
impact_score: 181.0
dependency_class: CRITICAL_ABSENCE

Threshold Axis

scenario_count: 6
pass_count: 2
check_count: 4
strict_pass_count: 1
pass_rate: 0.3333333333333333
strict_pass_rate: 0.16666666666666666
impact_score_mean: 60.333333333333336
impact_score_max: 151.0

Critical threshold targets:

C2
C4

Stable threshold target:

C3

Interpretation:

The threshold axis is the most fragile axis.

The control plane depends strongly on the presence and interaction of multiple confirmation windows.

Keeping only C2 causes a major top-layer failure.

Removing C4 causes an order inversion.

Removing C3 remains stable.

This means C3 is not the fragile point; it acts more like a stable middle support.

Variant Axis

scenario_count: 8
pass_count: 8
check_count: 0
strict_pass_count: 8
pass_rate: 1.0
strict_pass_rate: 1.0
impact_score_mean: 0.0
impact_score_max: 0.0

Stable variant targets:

two_runs_len_4_4
three_runs_len_4_4_4
staircase_1_2_3_4
single_run_len_5
mixed_1_2_3
mixed_1_1_4
long_then_spikes_4_1_1
dense_short_2_2_1_2_1_2

Interpretation:

Single-variant removal is fully stable in this test.

No selected individual variant was structurally necessary by itself.

This means the control plane is not carried by one isolated sample.

It is carried by the relational structure across families and thresholds.

Critical Dependencies

1. keep_only_family__spike_plus_long

axis: family
target: spike_plus_long
class: CRITICAL_ABSENCE
impact_score: 181.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: None
expected_second_rank: 4
dominant_cluster: cost=5|remaining=4|dest=OSCILLATING_NONPERSISTENT
second_cluster: cost=2|remaining=3|dest=OSCILLATING_NONPERSISTENT

Interpretation:

Keeping only spike_plus_long destroys the expected dominant control cluster.

This is the strongest measured dependency failure.

2. keep_only_family__two_equal_runs

axis: family
target: two_equal_runs
class: CRITICAL_ABSENCE
impact_score: 175.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: None
expected_second_rank: None
dominant_cluster: cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT
second_cluster: cost=2|remaining=2|dest=OSCILLATING_NONPERSISTENT

Interpretation:

Keeping only two_equal_runs collapses the control plane into the remaining=2 layer.

The expected remaining=3 control pair disappears.

3. keep_only_family__staircase

axis: family
target: staircase
class: CRITICAL_ABSENCE
impact_score: 175.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: None
expected_second_rank: None
dominant_cluster: cost=3|remaining=4|dest=OSCILLATING_NONPERSISTENT
second_cluster: cost=6|remaining=4|dest=OSCILLATING_NONPERSISTENT

Interpretation:

Keeping only staircase shifts control into the remaining=4 layer.

The expected control plane disappears.

4. keep_only_family__single_run

axis: family
target: single_run
class: CRITICAL_ABSENCE
impact_score: 175.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: None
expected_second_rank: None
dominant_cluster: cost=0|remaining=1|dest=SPIKE_FILTERED
second_cluster: cost=1|remaining=1|dest=SPIKE_FILTERED

Interpretation:

Keeping only single_run shifts the topology into the SPIKE_FILTERED layer.

The original oscillating control plane is absent.

5. keep_only_family__dense_short

axis: family
target: dense_short
class: CRITICAL_ABSENCE
impact_score: 175.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: None
expected_second_rank: None
dominant_cluster: cost=0|remaining=6|dest=OSCILLATING_NONPERSISTENT
second_cluster: cost=0|remaining=5|dest=OSCILLATING_NONPERSISTENT

Interpretation:

Keeping only dense_short shifts the topology into high remaining-run-count layers.

The expected remaining=3 control pair disappears.

6. keep_only_threshold__C2

axis: threshold
target: C2
class: CRITICAL_TOP6_LOSS
impact_score: 151.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: 20
expected_second_rank: 1
dominant_cluster: cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
second_cluster: cost=6|remaining=4|dest=OSCILLATING_NONPERSISTENT

Interpretation:

Keeping only threshold C2 severely damages the control-plane ranking.

The expected dominant cluster falls to rank 20.

This shows that C2 alone overemphasizes reducible mass and does not preserve the full control-plane topology.

7. keep_only_threshold__C4

axis: threshold
target: C4
class: CRITICAL_TOP6_LOSS
impact_score: 80.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: 1
expected_second_rank: 12
dominant_cluster: cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT
second_cluster: cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT

Interpretation:

Keeping only threshold C4 preserves the dominant expected cluster but loses the expected second cluster from the top control layer.

This means C4 alone filters too aggressively.

8. remove_threshold__C2

axis: threshold
target: C2
class: CRITICAL_TOP6_LOSS
impact_score: 65.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: 1
expected_second_rank: 7
dominant_cluster: cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT
second_cluster: cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT

Interpretation:

Removing C2 keeps the expected dominant cluster at rank 1.

But the expected second cluster falls out of the top 6.

This means C2 contributes materially to preserving the second control cluster.

9. remove_family__three_equal_runs

axis: family
target: three_equal_runs
class: CRITICAL_ORDER_INVERSION
impact_score: 65.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: 6
expected_second_rank: 1
dominant_cluster: cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
second_cluster: cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT

Interpretation:

Removing three_equal_runs causes the expected pair order to invert.

This is structurally important.

The three_equal_runs family is not just another sample family; it stabilizes the expected dominant control cluster.

10. remove_threshold__C4

axis: threshold
target: C4
class: CRITICAL_ORDER_INVERSION
impact_score: 49.0
status: CHECK
strict_status: CHECK
expected_dominant_rank: 2
expected_second_rank: 1
dominant_cluster: cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
second_cluster: cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

Interpretation:

Removing C4 inverts the expected dominant and second control clusters.

This means C4 contributes to preserving the correct top-order relation.

Moderate Dependencies

keep_only_threshold__C3

axis: threshold
target: C3
class: MODERATE_RANK_DRIFT
impact_score: 17.0
status: PASS
strict_status: CHECK
expected_dominant_rank: 2
expected_second_rank: 3

Interpretation:

Keeping only C3 does not destroy the expected pair.

But it shifts ranks enough to fail strict control-plane preservation.

remove_family__mixed_same_cost

axis: family
target: mixed_same_cost
class: MODERATE_RANK_DRIFT
impact_score: 16.0
status: PASS
strict_status: CHECK
expected_dominant_rank: 1
expected_second_rank: 4

Interpretation:

Removing mixed_same_cost preserves the expected pair and order.

But the expected second cluster drifts from rank 2 to rank 4.

This family contributes to rank sharpness.

Stable Supports

The following perturbations preserved the expected control-plane pair with no measured impact.

remove_variant__two_runs_len_4_4
remove_variant__three_runs_len_4_4_4
remove_variant__staircase_1_2_3_4
remove_variant__single_run_len_5
remove_variant__mixed_1_2_3
remove_variant__mixed_1_1_4
remove_variant__long_then_spikes_4_1_1
remove_variant__dense_short_2_2_1_2_1_2
remove_threshold__C3
remove_family__two_equal_runs
remove_family__staircase
remove_family__spike_plus_long
remove_family__single_run
remove_family__dense_short
keep_only_family__three_equal_runs
keep_only_family__mixed_same_cost

Interpretation:

The stable supports show that the control plane is not fragile to every perturbation.

It is robust to selected single-variant removals and some family removals.

But it is not robust to all threshold removals or all family isolations.

Structural Reading

The dependency map reveals three distinct facts.

First, the control plane is not a single-sample artifact. Removing individual variants does not damage it.

Second, the control plane is not universal across every restricted subspace. Keeping only certain families destroys it.

Third, threshold interaction matters. The control plane is created by the multi-threshold structure, not by one confirmation window alone.

Most Important Finding

The strongest control-plane layer remains:

remaining=3
destination=OSCILLATING_NONPERSISTENT

But this layer is dependent on structural context.

The control plane is therefore better described as:

context-dependent structural control layer

not as:

absolute invariant attractor

Boundary

This result is structural only.

It measures dependency across synthetic temporal-collapse topology perturbations.

It does not claim semantic causality.

It does not claim model correctness.

It does not claim real-world causal necessity.

It measures how the detected control-plane topology changes when families, thresholds, and variants are removed or isolated.

Final Check

PASS — control-plane dependency map detected