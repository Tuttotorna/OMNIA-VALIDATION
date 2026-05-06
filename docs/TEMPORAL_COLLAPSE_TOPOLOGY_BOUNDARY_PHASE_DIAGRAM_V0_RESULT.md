# Temporal Collapse Topology — Boundary Phase Diagram v0 Result

## Status

**PASS**

The experiment detected a boundary phase diagram over the temporal-collapse topology dependency map.

The result shows that dependency boundaries separate into three structural zones:

```text
STABLE_ZONE
DRIFT_ZONE
CRITICAL_ZONE

This is a structural measurement result.

It does not claim semantic causality.
It does not make external decisions.
It does not assign meaning to the trajectories.

It measures how the previously detected control plane behaves under boundary perturbations.


---

Experiment

experiment: temporal_collapse_topology_boundary_phase_diagram_v0
version: 0.1.4
status: PASS
method: boundary_phase_diagram
input_result_file: results/temporal_collapse_topology_dependency_boundary_v0.json
reproduction_command: python examples/temporal_collapse_topology_boundary_phase_diagram_v0.py


---

Input Dependency Boundary

The phase diagram consumes the dependency-boundary result:

results/temporal_collapse_topology_dependency_boundary_v0.json

Required input condition:

dependency_boundary_detected: True
boundary_scenario_count: 104
critical_boundary_count: 31
moderate_boundary_count: 13
stable_boundary_count: 60

The phase diagram is not computed from raw trajectories directly.

It is computed from the already measured boundary records of the control-plane dependency map.


---

Summary

boundary_scenario_count: 104
phase_zone_count: 3
stable_zone_count: 60
drift_zone_count: 13
critical_zone_count: 31

family_transition_boundary_detected: True
threshold_transition_boundary_detected: True
variant_transition_boundary_detected: False

minimum_critical_distance: 1
minimum_drift_distance: 1

phase_diagram_validation_holds: True
phase_diagram_detected: True


---

Main Result

The dependency boundary map separates into three zones.

STABLE_ZONE   -> 60 records
DRIFT_ZONE    -> 13 records
CRITICAL_ZONE -> 31 records

This means the control plane has measurable structural regimes.

Some perturbations preserve the expected control plane.

Some perturbations preserve it but alter its ranking.

Some perturbations break it by absence, order inversion, or top-6 loss.


---

Phase Zone Definitions

STABLE_ZONE

record_count: 60
axes: family, threshold, variant
dependency_classes: STABLE_SUPPORT
minimum_distance: 1
maximum_distance: 6
impact_mean: 10.801041666666666
impact_max: 63.0

Interpretation:

Stable-zone perturbations preserve the expected control-plane structure.

They do not remove the expected dominant and second control clusters.
They do not invert the expected pair.
They do not push the expected pair outside the relevant top structure.


---

DRIFT_ZONE

record_count: 13
axes: family, threshold
dependency_classes: MODERATE_RANK_DRIFT
minimum_distance: 1
maximum_distance: 5
impact_mean: 68.1298076923077
impact_max: 91.75

Interpretation:

Drift-zone perturbations do not fully break the expected control plane.

They preserve structural recognizability, but ranking stability is affected.

The expected dominant and second clusters may remain present, but their rank position changes.


---

CRITICAL_ZONE

record_count: 31
axes: family, threshold
dependency_classes:
- CRITICAL_ABSENCE
- CRITICAL_ORDER_INVERSION
- CRITICAL_TOP6_LOSS

minimum_distance: 1
maximum_distance: 6
impact_mean: 290.2681451612903
impact_max: 489.8125

Interpretation:

Critical-zone perturbations break the expected control-plane structure.

Critical behavior appears through at least one of three failure modes:

CRITICAL_ABSENCE
CRITICAL_ORDER_INVERSION
CRITICAL_TOP6_LOSS

These are structural failures of the measured control plane.

They are not semantic failures.


---

Axis Phase Matrix

Family Axis

STABLE_ZONE:
  record_count: 22
  minimum_distance: 1
  maximum_distance: 6
  impact_mean: 18.664772727272727
  impact_max: 63.0

DRIFT_ZONE:
  record_count: 11
  minimum_distance: 1
  maximum_distance: 5
  impact_mean: 63.83522727272727
  impact_max: 78.125

CRITICAL_ZONE:
  record_count: 23
  minimum_distance: 1
  maximum_distance: 6
  impact_mean: 332.88858695652175
  impact_max: 489.8125

Conclusion:

The family axis contains all three regimes.

It is structurally phase-sensitive.

A family perturbation can be stable, drift-producing, or critical depending on which family boundary is crossed.


---

Threshold Axis

STABLE_ZONE:
  record_count: 2
  minimum_distance: 1
  maximum_distance: 1
  impact_mean: 28.5
  impact_max: 28.5

DRIFT_ZONE:
  record_count: 2
  minimum_distance: 2
  maximum_distance: 2
  impact_mean: 91.75
  impact_max: 91.75

CRITICAL_ZONE:
  record_count: 8
  minimum_distance: 1
  maximum_distance: 2
  impact_mean: 167.734375
  impact_max: 297.5625

Conclusion:

The threshold axis is highly sensitive.

Critical behavior can appear at distance 1.

This means a single threshold-boundary change can be enough to break the expected control plane.


---

Variant Axis

STABLE_ZONE:
  record_count: 36
  minimum_distance: 1
  maximum_distance: 2
  impact_mean: 5.012152777777778
  impact_max: 15.4375

Conclusion:

The variant axis remains stable under the tested perturbations.

No drift zone was detected on this axis.

No critical zone was detected on this axis.

This means the measured control plane is not dependent on individual variants in the tested set.


---

Distance Phase Map

Family

distance=1:
  stable: 5
  drift: 1
  critical: 1
  dominant_phase: STABLE_ZONE

distance=2:
  stable: 10
  drift: 5
  critical: 6
  dominant_phase: STABLE_ZONE

distance=5:
  stable: 5
  drift: 5
  critical: 11
  dominant_phase: CRITICAL_ZONE

distance=6:
  stable: 2
  drift: 0
  critical: 5
  dominant_phase: CRITICAL_ZONE

Family-axis interpretation:

At low distance, the family axis is mostly stable.

At higher distance, the dominant phase becomes critical.

This shows a structural transition from stable to critical behavior.


---

Threshold

distance=1:
  stable: 2
  drift: 0
  critical: 4
  dominant_phase: CRITICAL_ZONE

distance=2:
  stable: 0
  drift: 2
  critical: 4
  dominant_phase: CRITICAL_ZONE

Threshold-axis interpretation:

The threshold axis is critical-dominant even at distance 1.

This means the threshold choice is a structural control variable.

It is not a neutral parameter in this topology.


---

Variant

distance=1:
  stable: 8
  drift: 0
  critical: 0
  dominant_phase: STABLE_ZONE

distance=2:
  stable: 28
  drift: 0
  critical: 0
  dominant_phase: STABLE_ZONE

Variant-axis interpretation:

The variant axis remains stable at both tested distances.

This confirms that the topology is not merely memorizing individual variant records.

The measured control plane is supported by broader structural families and threshold relations.


---

Phase Boundaries

axis=family
stable_count: 22
drift_count: 11
critical_count: 23
minimum_stable_distance: 1
minimum_drift_distance: 1
minimum_critical_distance: 1
transition_boundary_detected: True

axis=threshold
stable_count: 2
drift_count: 2
critical_count: 8
minimum_stable_distance: 1
minimum_drift_distance: 2
minimum_critical_distance: 1
transition_boundary_detected: True

axis=variant
stable_count: 36
drift_count: 0
critical_count: 0
minimum_stable_distance: 1
minimum_drift_distance: None
minimum_critical_distance: None
transition_boundary_detected: False

Interpretation:

Family and threshold axes contain transition boundaries.

Variant axis does not.

This separates structural dependence from individual-record dependence.


---

Minimum Critical Boundaries

The minimum critical distance is:

minimum_critical_distance: 1

Critical behavior appears at the smallest tested boundary distance.

Representative minimum critical boundaries:

remove_family_boundary__three_equal_runs
axis: family
distance: 1
class: CRITICAL_ORDER_INVERSION
impact: 118.75
dominant_rank: 6
second_rank: 1

keep_threshold_boundary__C3__C4
axis: threshold
distance: 1
class: CRITICAL_TOP6_LOSS
impact: 106.5
dominant_rank: 1
second_rank: 7

remove_threshold_boundary__C2
axis: threshold
distance: 1
class: CRITICAL_TOP6_LOSS
impact: 106.5
dominant_rank: 1
second_rank: 7

keep_threshold_boundary__C2__C3
axis: threshold
distance: 1
class: CRITICAL_ORDER_INVERSION
impact: 88.4375
dominant_rank: 2
second_rank: 1

remove_threshold_boundary__C4
axis: threshold
distance: 1
class: CRITICAL_ORDER_INVERSION
impact: 88.4375
dominant_rank: 2
second_rank: 1

Interpretation:

Criticality is not only a high-distance effect.

Some single-boundary perturbations are enough to produce structural breakage.


---

Maximum-Impact Critical Boundaries

The strongest critical boundaries are family-axis reductions.

Top maximum-impact examples:

keep_family_boundary__staircase
axis: family
distance: 6
class: CRITICAL_ABSENCE
impact: 489.8125
dominant_rank: None
second_rank: None

keep_family_boundary__dense_short__staircase
axis: family
distance: 5
class: CRITICAL_ABSENCE
impact: 483.0625
dominant_rank: None
second_rank: None

keep_family_boundary__dense_short
axis: family
distance: 6
class: CRITICAL_ABSENCE
impact: 483.0625
dominant_rank: None
second_rank: None

keep_family_boundary__staircase__two_equal_runs
axis: family
distance: 5
class: CRITICAL_ABSENCE
impact: 473.5
dominant_rank: None
second_rank: None

keep_family_boundary__two_equal_runs
axis: family
distance: 6
class: CRITICAL_ABSENCE
impact: 473.5
dominant_rank: None
second_rank: None

Interpretation:

The largest failures occur when the family support structure is reduced too aggressively.

This confirms that the control plane is not held by isolated variants.

It is held by a structural family configuration.


---

Minimum Drift Boundaries

The minimum drift distance is:

minimum_drift_distance: 1

Representative drift boundaries:

remove_family_boundary__mixed_same_cost
axis: family
distance: 1
class: MODERATE_RANK_DRIFT
impact: 62.125
dominant_rank: 1
second_rank: 4

keep_threshold_boundary__C3
axis: threshold
distance: 2
class: MODERATE_RANK_DRIFT
impact: 91.75
dominant_rank: 2
second_rank: 3

remove_threshold_boundary__C2__C4
axis: threshold
distance: 2
class: MODERATE_RANK_DRIFT
impact: 91.75
dominant_rank: 2
second_rank: 3

Interpretation:

Drift means the control plane remains visible, but its rank ordering changes.

This is not full collapse.

It is structural reweighting.


---

Minimum Stable Boundaries

Representative stable minimum-distance boundaries:

keep_threshold_boundary__C2__C4
axis: threshold
distance: 1
class: STABLE_SUPPORT
impact: 28.5
dominant_rank: 1
second_rank: 2

remove_family_boundary__dense_short
axis: family
distance: 1
class: STABLE_SUPPORT
impact: 0.0
dominant_rank: 1
second_rank: 2

remove_family_boundary__single_run
axis: family
distance: 1
class: STABLE_SUPPORT
impact: 0.0
dominant_rank: 1
second_rank: 2

remove_threshold_boundary__C3
axis: threshold
distance: 1
class: STABLE_SUPPORT
impact: 28.5
dominant_rank: 1
second_rank: 2

remove_variant_boundary__dense_short_2_2_1_2_1_2
axis: variant
distance: 1
class: STABLE_SUPPORT
impact: 0.0
dominant_rank: 1
second_rank: 2

Interpretation:

Some single-boundary perturbations are safe.

Others are critical.

Therefore the topology does not depend only on perturbation size.

It depends on which structural boundary is crossed.


---

Validation

phase_diagram_validation_holds: True
failure_count: 0
failures: []

Validation passed.

The phase diagram contains:

STABLE_ZONE
DRIFT_ZONE
CRITICAL_ZONE

It also confirms:

family_transition_boundary_detected: True
threshold_transition_boundary_detected: True
variant_transition_boundary_detected: False


---

Structural Conclusion

The control plane has a measurable dependency phase diagram.

The tested topology separates into:

stable support
rank drift
critical failure

The variant axis remains stable.

The family and threshold axes contain real transition boundaries.

This means the control plane is not a superficial artifact of individual variants.

It is structurally supported by family-level configuration and threshold-level behavior.

The strongest result is:

variant perturbations stay stable
family perturbations can drift or become critical
threshold perturbations can become critical at distance 1


---

Boundary Statement

This result is measurement-only.

measurement != inference != decision

The experiment measures structural behavior under controlled boundary perturbations.

It does not infer semantic meaning.

It does not decide what action should be taken.

It does not claim external causal truth.

It identifies structural phase zones in the measured dependency topology.