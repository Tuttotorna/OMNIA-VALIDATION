# Temporal Collapse Topology — Dependency Boundary v0 Result

## Status

PASS

## Experiment

`temporal_collapse_topology_dependency_boundary_v0`

## Version

`0.1.0`

## Result file

`results/temporal_collapse_topology_dependency_boundary_v0.json`

## Reproduction command

```bash
python examples/temporal_collapse_topology_dependency_boundary_v0.py


---

Summary

This experiment tests whether the previously detected temporal-collapse control plane has measurable dependency boundaries.

The result is positive.

The control plane is not uniformly robust. It has measurable stable, moderate, and critical perturbation boundaries across the tested family, threshold, and variant axes.

status: PASS
baseline_status: PASS
baseline_strict_status: PASS
boundary_scenario_count: 104
critical_boundary_count: 31
moderate_boundary_count: 13
stable_boundary_count: 60
minimum_critical_distance: 1
minimum_moderate_distance: 1
dependency_boundary_detected: True


---

Tested control-plane pair

The expected control-plane pair was:

dominant:
cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT

second:
cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT

These are the same two dominant structures detected in the previous control-plane experiment.


---

Boundary definition

A dependency boundary is detected when perturbation scenarios expose different response zones in the control plane.

The tested response zones are:

STABLE_SUPPORT
MODERATE_RANK_DRIFT
CRITICAL_TOP6_LOSS
CRITICAL_ORDER_INVERSION
CRITICAL_ABSENCE

Meaning:

STABLE_SUPPORT:
the expected control-plane pair remains structurally stable.

MODERATE_RANK_DRIFT:
the expected pair remains present, but its rank drifts.

CRITICAL_TOP6_LOSS:
one expected control-plane member falls outside the top-6 control layer.

CRITICAL_ORDER_INVERSION:
the expected dominant/second order is inverted.

CRITICAL_ABSENCE:
one expected control-plane member disappears from the tested topology.


---

Result by boundary axis

family:
  scenarios: 56
  pass: 33
  check: 23
  strict_pass: 22
  critical: 23
  moderate: 11
  stable: 22
  minimum_critical_distance: 1
  minimum_moderate_distance: 1
  impact_mean: 91.67857142857143
  impact_max: 302.0

threshold:
  scenarios: 12
  pass: 4
  check: 8
  strict_pass: 2
  critical: 8
  moderate: 2
  stable: 2
  minimum_critical_distance: 1
  minimum_moderate_distance: 2
  impact_mean: 97.33333333333333
  impact_max: 288.0

variant:
  scenarios: 36
  pass: 36
  check: 0
  strict_pass: 36
  critical: 0
  moderate: 0
  stable: 36
  minimum_critical_distance: None
  minimum_moderate_distance: None
  impact_mean: 0.0
  impact_max: 0.0


---

Main structural result

The control plane has measurable dependency boundaries.

It is stable under all tested variant removals.

It is sensitive under family and threshold perturbations.

The most important boundary fact is:

minimum_critical_distance: 1

That means a one-step perturbation is sufficient to create a critical boundary in some axes.

This matters because the control plane is not merely globally fragile or globally stable. It has a structured perturbation landscape.


---

Minimum critical boundaries

The minimum critical boundary distance was 1.

The critical one-step boundaries were:

remove_family_boundary__three_equal_runs
class: CRITICAL_ORDER_INVERSION
axis: family
distance: 1
impact: 98.0
dominant_rank: 6
second_rank: 1

keep_threshold_boundary__C3__C4
class: CRITICAL_TOP6_LOSS
axis: threshold
distance: 1
impact: 90.0
dominant_rank: 1
second_rank: 7

remove_threshold_boundary__C2
class: CRITICAL_TOP6_LOSS
axis: threshold
distance: 1
impact: 90.0
dominant_rank: 1
second_rank: 7

keep_threshold_boundary__C2__C3
class: CRITICAL_ORDER_INVERSION
axis: threshold
distance: 1
impact: 58.0
dominant_rank: 2
second_rank: 1

remove_threshold_boundary__C4
class: CRITICAL_ORDER_INVERSION
axis: threshold
distance: 1
impact: 58.0
dominant_rank: 2
second_rank: 1


---

Strongest critical boundaries

The strongest critical boundary was:

remove_family_boundary__mixed_same_cost__three_equal_runs
axis: family
distance: 2
class: CRITICAL_ABSENCE
impact: 302.0
dominant_rank: None
second_rank: 16

This means that removing both mixed_same_cost and three_equal_runs destroys the expected dominant control cluster from the tested topology and pushes the expected second cluster down to rank 16.

The strongest threshold critical boundaries were:

keep_threshold_boundary__C2
axis: threshold
distance: 2
class: CRITICAL_TOP6_LOSS
impact: 288.0
dominant_rank: 20
second_rank: 1

remove_threshold_boundary__C3__C4
axis: threshold
distance: 2
class: CRITICAL_TOP6_LOSS
impact: 288.0
dominant_rank: 20
second_rank: 1

These show that threshold composition is not a neutral parameter. The control-plane topology depends strongly on which confirmation-window layer is preserved or removed.


---

Moderate boundaries

Moderate boundaries were detected where the expected pair remained present but drifted in rank.

Examples:

remove_family_boundary__mixed_same_cost
axis: family
distance: 1
class: MODERATE_RANK_DRIFT
impact: 16.0
dominant_rank: 1
second_rank: 4

remove_family_boundary__spike_plus_long__three_equal_runs
axis: family
distance: 2
class: MODERATE_RANK_DRIFT
impact: 36.0
dominant_rank: 3
second_rank: 4

keep_threshold_boundary__C3
axis: threshold
distance: 2
class: MODERATE_RANK_DRIFT
impact: 18.0
dominant_rank: 2
second_rank: 3

remove_threshold_boundary__C2__C4
axis: threshold
distance: 2
class: MODERATE_RANK_DRIFT
impact: 18.0
dominant_rank: 2
second_rank: 3

Moderate boundaries are important because they show partial structural preservation.

The control plane does not collapse, but its internal ordering changes.


---

Stable boundaries

Stable boundaries were also detected.

Examples:

keep_threshold_boundary__C2__C4
axis: threshold
distance: 1
class: STABLE_SUPPORT
dominant_rank: 1
second_rank: 2

remove_family_boundary__dense_short
axis: family
distance: 1
class: STABLE_SUPPORT
dominant_rank: 1
second_rank: 2

remove_family_boundary__single_run
axis: family
distance: 1
class: STABLE_SUPPORT
dominant_rank: 1
second_rank: 2

remove_family_boundary__spike_plus_long
axis: family
distance: 1
class: STABLE_SUPPORT
dominant_rank: 1
second_rank: 2

remove_family_boundary__staircase
axis: family
distance: 1
class: STABLE_SUPPORT
dominant_rank: 1
second_rank: 2

remove_family_boundary__two_equal_runs
axis: family
distance: 1
class: STABLE_SUPPORT
dominant_rank: 1
second_rank: 2

remove_threshold_boundary__C3
axis: threshold
distance: 1
class: STABLE_SUPPORT
dominant_rank: 1
second_rank: 2

The full variant axis was stable in all tested cases:

variant:
  stable: 36
  moderate: 0
  critical: 0

This means the tested topology is not fragile to individual variant removal. Its fragility is concentrated in family composition and threshold-layer structure.


---

Interpretation

The measured topology has three zones:

stable zone:
perturbations that preserve the expected control-plane pair.

moderate zone:
perturbations that preserve the pair but alter rank structure.

critical zone:
perturbations that invert, displace, or remove expected control-plane members.

This is stronger than a binary robustness test.

A binary robustness test says:

stable / unstable

This experiment says:

where stable,
where drifting,
where critical,
and at what boundary distance.


---

Structural conclusion

The temporal-collapse control plane has measurable dependency boundaries.

The boundary map shows:

family axis:
mixed stability, moderate drift, and critical failure boundaries.

threshold axis:
high sensitivity, including one-step critical boundaries.

variant axis:
fully stable under tested variant removals.

The core conclusion is:

The control plane is not uniformly robust.
It has measurable dependency boundaries:
stable regions, moderate drift regions, and critical failure boundaries.


---

Boundary statement

measurement != inference != decision

This experiment does not decide whether a system is good or bad.

It measures how a previously detected control-plane topology behaves under structured perturbation.

The output is a structural measurement of boundary behavior, not a semantic judgment.


---

Final check

PASS — dependency boundary detected:
the control plane has measurable stable, moderate, and critical perturbation boundaries.