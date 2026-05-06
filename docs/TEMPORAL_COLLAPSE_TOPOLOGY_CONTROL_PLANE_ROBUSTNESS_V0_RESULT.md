# Temporal Collapse Topology — Control Plane Robustness v0 Result

## Status

CHECK

## Experiment

`temporal_collapse_topology_control_plane_robustness_v0`

## Version

`0.1.0`

## Reproduction command

```bash
python examples/temporal_collapse_topology_control_plane_robustness_v0.py

Purpose

This experiment tests whether the previously detected temporal-collapse control plane remains stable under dataset perturbation.

The baseline control plane had identified two dominant structural clusters:

dominant: cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT
second:   cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

This robustness test asks whether that pair remains structurally dominant when parts of the topology are removed or perturbed.

Tested perturbations

The experiment evaluated 21 scenarios:

baseline:             1
remove_family:        7
remove_variant:       8
remove_threshold:     3
low_weight_pruning:   1
topology_noise:       1

The perturbation classes were:

1. Baseline topology
2. Removal of one whole structural family
3. Removal of selected individual variants
4. Removal of one confirmation threshold
5. Low-weight topology pruning
6. Addition of topology noise

Summary

scenario_count: 21
pass_count: 18
strict_pass_count: 17
robustness_rate: 0.8571428571428571
strict_robustness_rate: 0.8095238095238095

expected_dominant_control_cluster:
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

expected_second_control_cluster:
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

dominant_top1_count: 19
second_top2_count: 17
expected_pair_present_count: 21
expected_pair_order_preserved_count: 19
top6_contains_expected_pair_count: 20

dominant_rank_mean: 1.2857142857142858
second_rank_mean: 2.238095238095238

control_plane_robustness_detected: false
strict_control_plane_robustness_detected: true

Result interpretation

The control plane was not fully robust under the tested perturbations.

The result is therefore CHECK, not PASS.

This does not mean that the control plane is absent. It means the opposite is more precise:

The control plane exists in the baseline topology,
but it depends on specific structural families and threshold windows.

The expected dominant and second clusters remained present in all 21 scenarios. However, their rank order and top-6 control-plane membership were not preserved in every perturbation.

Robustness rule

The experiment used the following robustness rule:

PASS when expected dominant and second control clusters remain present,
remain inside top-6, and preserve pair order under dataset perturbations.

The experiment used the following stricter rule:

STRICT PASS when expected dominant remains rank 1
and expected second remains rank 2.

The global robustness rule failed because the robustness rate was below the required threshold.

required robustness_rate >= 0.90
observed robustness_rate = 0.8571428571428571

By perturbation type

baseline:
  scenarios: 1
  pass: 1
  strict: 1
  pass_rate: 1.0
  strict_rate: 1.0

remove_family:
  scenarios: 7
  pass: 6
  strict: 5
  pass_rate: 0.8571428571428571
  strict_rate: 0.7142857142857143

remove_variant:
  scenarios: 8
  pass: 8
  strict: 8
  pass_rate: 1.0
  strict_rate: 1.0

remove_threshold:
  scenarios: 3
  pass: 1
  strict: 1
  pass_rate: 0.3333333333333333
  strict_rate: 0.3333333333333333

low_weight_pruning:
  scenarios: 1
  pass: 1
  strict: 1
  pass_rate: 1.0
  strict_rate: 1.0

topology_noise:
  scenarios: 1
  pass: 1
  strict: 1
  pass_rate: 1.0
  strict_rate: 1.0

Stable perturbation classes

The control plane remained stable under:

remove_variant
low_weight_pruning
topology_noise

The strongest result is variant removal:

remove_variant:
  scenarios: 8
  pass_count: 8
  strict_pass_count: 8
  pass_rate: 1.0
  strict_pass_rate: 1.0

This means individual variant removal did not break the expected control-plane pair.

Fragile perturbation classes

The control plane was fragile under:

remove_family
remove_threshold

The weakest result is threshold removal:

remove_threshold:
  scenarios: 3
  pass_count: 1
  strict_pass_count: 1
  pass_rate: 0.3333333333333333

This means the detected control plane depends strongly on the confirmation-window structure.

Failure cases

1. remove_family__three_equal_runs

scenario: remove_family__three_equal_runs
status: CHECK
expected_dominant_rank: 6
expected_second_rank: 1
dominant_cluster_id: cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
second_cluster_id: cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT

Removing the three_equal_runs family reverses the expected dominant/second pair order.

The expected dominant cluster:

cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

falls to rank 6.

The expected second cluster:

cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

rises to rank 1.

This indicates that the three_equal_runs family is structurally critical for maintaining the baseline control-plane hierarchy.

2. remove_threshold__C2

scenario: remove_threshold__C2
status: CHECK
expected_dominant_rank: 1
expected_second_rank: 7
dominant_cluster_id: cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT
second_cluster_id: cost=0|remaining=2|dest=OSCILLATING_NONPERSISTENT

Removing confirmation window C=2 preserves the expected dominant cluster at rank 1.

However, the expected second cluster falls to rank 7.

Since the robustness rule requires the expected pair to remain inside the top-6, this scenario fails the robustness condition.

3. remove_threshold__C4

scenario: remove_threshold__C4
status: CHECK
expected_dominant_rank: 2
expected_second_rank: 1
dominant_cluster_id: cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT
second_cluster_id: cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

Removing confirmation window C=4 reverses the expected control-cluster order.

The expected dominant cluster moves to rank 2.

The expected second cluster moves to rank 1.

This shows that C=4 contributes to preserving the baseline dominant/second hierarchy.

Rank values

Expected dominant cluster rank values:

[1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1]

Expected second cluster rank values:

[2, 2, 4, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 7, 2, 1, 2, 2]

The rank sequences show that most scenarios preserve the expected order, but a small number of structurally targeted perturbations alter the hierarchy.

Structural conclusion

The experiment establishes a negative-but-useful result:

The temporal-collapse control plane is stable under local perturbations,
but not invariant under all structural perturbations.

More precisely:

The control plane survives all tested scenarios as a recognizable pair,
but its rank dominance depends on specific topology-supporting components.

The most important dependencies are:

1. the three_equal_runs family
2. confirmation window C=2
3. confirmation window C=4

Boundary

This result must not be described as a full robustness confirmation.

Correct statement:

The baseline control plane is structurally real,
but only conditionally robust under tested perturbations.

Incorrect statement:

The control plane is fully robust.

Also incorrect:

The control plane failed.

The measured result is:

CHECK: structurally informative partial robustness.

Interpretation for the validation chain

Earlier experiments detected:

1. invariant signature clusters
2. cluster adjacency graph
3. cluster graph centrality
4. baseline control plane

This experiment adds the next constraint:

5. control-plane robustness under perturbation is partial, not absolute

Therefore, the validation chain should not claim unconditional invariance.

It should claim:

Temporal-collapse topology contains a measurable control plane,
but the control plane has identifiable structural dependencies.

Final check

status: CHECK
message: control-plane robustness was not fully confirmed under the tested perturbation scenarios