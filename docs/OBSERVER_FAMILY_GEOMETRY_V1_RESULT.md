# Observer Family Geometry v1 — Result

## Status

```text
Status: FAIL
Version: 0.2.0
Claim level: Level 1 — Toy Demonstration


---

Purpose

This experiment tests whether observer-family geometry can move beyond the over-separated behavior observed in v0.

v1 introduces:

observer variants
observer families
same-family relations
redundant observer pairs
cross-family diversity

Core boundary:

measurement != inference != decision


---

Experiment File

examples/observer_family_geometry_v1.py

Result file:

results/observer_family_geometry_v1.json

Reproduction command:

python examples/observer_family_geometry_v1.py


---

Global Result

Observer count:                      14
Family count:                        6
Pair count:                          91
Average distance:                    0.934268774571
Min distance:                        0.083333333333
Max distance:                        1.0
Redundant pair count:                2
Medium pair count:                   0
Diverse pair count:                  89
Same-family medium/redundant count:  2
Cross-family diverse count:          81
Unique observer count:               14
Redundant observer count:            0

Final status:

FAIL


---

Pass Condition

observer_count >= 10
and family_count >= 5
and same_family_medium_or_redundant_count >= 3
and cross_family_diverse_count >= 10
and medium_pair_count >= 3
and 0.40 < average_distance < 0.95

Observed:

observer_count = 14
family_count = 6
same_family_medium_or_redundant_count = 2
cross_family_diverse_count = 81
medium_pair_count = 0
average_distance = 0.934268774571

The pass condition failed mainly because:

medium_pair_count = 0

and:

same_family_medium_or_redundant_count = 2

was below the required minimum of 3.


---

Family Summary

entropy:
  observers = 2
  same_family_avg_distance = 0.083333333333
  cross_family_avg_distance = 0.964444444444

motif:
  observers = 3
  same_family_avg_distance = 0.75
  cross_family_avg_distance = 0.98946026196

run_length:
  observers = 2
  same_family_avg_distance = 0.75
  cross_family_avg_distance = 0.984444444444

symbol:
  observers = 2
  same_family_avg_distance = 0.75
  cross_family_avg_distance = 0.964543650794

symmetry:
  observers = 2
  same_family_avg_distance = 0.69
  cross_family_avg_distance = 0.931701643264

transition:
  observers = 3
  same_family_avg_distance = 0.57253968254
  cross_family_avg_distance = 0.988472823473


---

Observer Uniqueness

entropy_profile                  0.892307692308
entropy_profile_extended         0.901025641026
motif3                           0.954719639335
motif3_soft                      0.948076923077
motif4                           0.955064102564
periodicity_profile              0.976153846154
run_length_profile               0.96641025641
run_length_profile_exact         0.96641025641
symbol_pattern                   0.971721611722
symbol_pattern_unique_ratio      0.924358974359
symmetry_profile                 0.85006457218
transition_topology              0.913192918193
transition_topology_soft         0.950384615385
transition_topology_windowed     0.909871794872

All observers still appear globally unique because cross-family distances remain very high.


---

Main Positive Finding

v1 improves on v0.

Unlike v0, v1 detects actual redundancy:

redundant_pair_count = 2

The strongest redundant pair is:

entropy_profile
<-> entropy_profile_extended

distance = 0.083333333333
similarity = 0.916666666667

Another redundant relation appears in the transition family:

transition_topology
<-> transition_topology_windowed

distance = 0.217619047619
similarity = 0.782380952381

This confirms that observer redundancy can be detected.


---

Main Negative Finding

v1 still does not produce a continuous observer geometry.

The critical failure is:

medium_pair_count = 0

The geometry still mostly separates observer pairs into:

redundant
or
diverse

but does not create a meaningful middle region.

This means the observer distance function remains too discontinuous.


---

Interpretation

The correct interpretation is:

v1 introduces redundancy,
but still fails to produce a continuous observer geometry
because medium-distance relations are absent.

This is a useful negative result.

It identifies a specific weakness:

observer distance still saturates too aggressively


---

Why The FAIL Is Useful

The FAIL is not a failure of the research direction.

It is a pressure result.

It shows that observer-family geometry cannot be validated merely by adding more observer variants.

The distance function itself must be improved.

Specifically, it must create:

near relations
medium relations
far relations
redundant relations

instead of mostly:

redundant
far


---

Failure Geometry

Observed relation counts:

redundant = 2
medium = 0
diverse = 89

This means v1 has a geometry gap.

The missing zone is:

0.25 < distance <= 0.60

No observer pairs landed in this range.

That is the central technical failure.


---

Relation To v0

v0 result:

average_distance = 0.962268518518
redundant_pair_count = 0
diverse_pair_count = 15

v1 result:

average_distance = 0.934268774571
redundant_pair_count = 2
diverse_pair_count = 89

v1 improved by introducing redundancy.

But it did not solve distance saturation.


---

Relation To Recoverability Score

Recoverability scoring requires observer weights.

Observer weights require observer geometry.

This result shows that v1 can identify some redundant observers, but it is not yet reliable enough for mature recoverability weighting.

Current risk:

observer diversity may be overestimated

because many cross-family pairs saturate at distance 1.0.


---

Relation To Multi-Projection Recovery

Multi-projection recovery asks whether lost distinctions reappear under expanded observer families.

But recovery evidence is only strong if observer families are genuinely diverse.

v1 begins to test that diversity.

However, because the geometry is still over-separated, recovery confidence should remain conservative.


---

Required Improvement For v2

v2 should focus on medium-distance geometry.

Minimum requirements:

1. produce at least several medium-distance observer pairs

2. reduce distance saturation at 1.0

3. compare observer responses in a shared feature space

4. avoid hard zero similarity between different output types

5. add softer cross-family similarities

6. compute relation bands more gradually

7. introduce observer response correlation

8. distinguish local redundancy from global uniqueness

Expected v2 behavior:

redundant_pair_count > 0
medium_pair_count > 0
diverse_pair_count > 0
average_distance below v1
cross-family diversity preserved


---

Boundary Statement

This experiment does not prove:

truth
meaning
semantic equivalence
causal equivalence
universal observer independence

It only measures:

toy observer-family geometry
under a heuristic distance function


---

Limitations

This is not the full OMNIA engine.

This is a toy observer geometry experiment.

Observer distance is heuristic.

Family bonuses are manually chosen.

Observer families are simplified.

No semantic truth is evaluated.

No universal observer geometry claim is made.

The v1 geometry remains over-separated.

Medium-distance observer relations are absent.


---

Final Result

FAIL — observer family geometry v1 did not satisfy pass condition.

Correct technical conclusion:

v1 successfully introduced redundancy,
but failed to produce continuous observer geometry.

The next version should target the missing middle zone:

medium-distance observer relations