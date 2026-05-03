# Observer Family Geometry v2 — Result

## Status

```text
Status: FAIL
Version: 0.3.0
Claim level: Level 1 — Toy Demonstration


---

Purpose

This experiment tests whether observer-family geometry can reduce distance saturation by comparing observers inside a shared response feature space.

v2 attempts to fix the main v1 failure:

medium_pair_count = 0

Core boundary:

measurement != inference != decision


---

Experiment File

examples/observer_family_geometry_v2.py

Result file:

results/observer_family_geometry_v2.json

Reproduction command:

python examples/observer_family_geometry_v2.py


---

Global Result

Observer count:                      14
Family count:                        6
Pair count:                          91
Average distance:                    0.766832219068
Min distance:                        0.006202430057
Max distance:                        1.0
Redundant pair count:                12
Medium pair count:                   6
Diverse pair count:                  73
Same-family medium/redundant count:  8
Cross-family diverse count:          71
Unique observer count:               14
Redundant observer count:            0

Final status:

FAIL


---

Pass Condition

observer_count >= 10
and family_count >= 5
and redundant_pair_count >= 2
and medium_pair_count >= 10
and diverse_pair_count >= 10
and same_family_medium_or_redundant_count >= 5
and cross_family_diverse_count >= 5
and 0.20 < average_distance < 0.80

Observed:

observer_count = 14
family_count = 6
redundant_pair_count = 12
medium_pair_count = 6
diverse_pair_count = 73
same_family_medium_or_redundant_count = 8
cross_family_diverse_count = 71
average_distance = 0.766832219068

The only failing condition is:

medium_pair_count >= 10

Observed:

medium_pair_count = 6


---

Relation Counts

redundant = 12
medium    = 6
diverse   = 73

This is a major improvement over v1.

v1 produced:

redundant = 2
medium    = 0
diverse   = 89

v2 successfully introduced a non-empty medium-distance region.


---

Distance Saturation

v1 average distance:

0.934268774571

v2 average distance:

0.766832219068

This means v2 reduced distance saturation.

The observer geometry is no longer almost entirely pushed toward distance 1.0.


---

Family Summary

entropy:
  observers = 2
  same_family_avg_distance = 0.006202430057
  cross_family_avg_distance = 0.745424645098

motif:
  observers = 3
  same_family_avg_distance = 0.467676968235
  cross_family_avg_distance = 0.865142235378

run_length:
  observers = 2
  same_family_avg_distance = 0.073373407014
  cross_family_avg_distance = 0.913979296385

symbol:
  observers = 2
  same_family_avg_distance = 0.043949888754
  cross_family_avg_distance = 0.735018536637

symmetry:
  observers = 2
  same_family_avg_distance = 0.109216949356
  cross_family_avg_distance = 0.919574483667

transition:
  observers = 3
  same_family_avg_distance = 0.110599622813
  cross_family_avg_distance = 0.834627215858


---

Observer Uniqueness

entropy_profile                  0.697453679681
entropy_profile_extended         0.679669115894
motif3                           0.750944800621
motif3_soft                      0.735460289875
motif4                           0.925576107726
periodicity_profile              0.83857089066
run_length_profile               0.905576318237
run_length_profile_soft          0.793058291554
symbol_pattern                   0.691748009107
symbol_pattern_soft              0.671970810648
symmetry_profile                 0.87590768678
transition_topology              0.72773725119
transition_topology_soft         0.693847208744
transition_topology_windowed     0.748130606236

All observers still remain globally unique.

This is not necessarily wrong.

It means that even redundant local pairs still sit inside a broader diverse observer family.


---

Main Positive Finding

v2 partially succeeds.

It introduces all three required relation zones:

redundant
medium
diverse

This fixes the most important v1 defect.

The framework now detects:

local redundancy
medium-distance relations
broad observer diversity


---

Main Negative Finding

v2 still fails to produce enough medium-distance relations.

Target:

medium_pair_count >= 10

Observed:

medium_pair_count = 6

So the geometry remains somewhat polarized.

It is no longer only:

redundant / diverse

but it is still dominated by:

diverse


---

Correct Interpretation

Correct conclusion:

v2 partially succeeds:
it reduces distance saturation
and produces medium-distance observer relations,
but does not yet reach the target density
for medium geometry.

Incorrect conclusion:

v2 failed completely.

The FAIL is threshold-specific.

The structural direction improved clearly from v1.


---

Key Improvement Over v1

v1 medium_pair_count = 0
v2 medium_pair_count = 6

v1 redundant_pair_count = 2
v2 redundant_pair_count = 12

v1 average_distance = 0.934268774571
v2 average_distance = 0.766832219068

This shows that the shared response feature space is better than the previous direct output comparison.


---

Medium-Distance Relations Found

Examples of medium relations include:

entropy_profile_extended
<-> run_length_profile_soft

distance = 0.590689935516

motif3
<-> transition_topology

distance = 0.366223146548

motif3
<-> transition_topology_soft

distance = 0.440427323378

periodicity_profile
<-> transition_topology_windowed

distance = 0.396511979007

run_length_profile_soft
<-> symbol_pattern_soft

distance = 0.480864312723

symmetry_profile
<-> transition_topology_windowed

distance = 0.563792927308

These are important because they show that observer geometry is becoming continuous rather than binary.


---

Redundant Relations Found

Examples of redundant relations:

entropy_profile
<-> entropy_profile_extended

distance = 0.006202430057

motif3
<-> motif3_soft

distance = 0.113244800561

periodicity_profile
<-> symmetry_profile

distance = 0.109216949356

run_length_profile
<-> run_length_profile_soft

distance = 0.073373407014

symbol_pattern
<-> symbol_pattern_soft

distance = 0.043949888754

transition_topology
<-> transition_topology_soft

distance = 0.045865734498

transition_topology
<-> transition_topology_windowed

distance = 0.105370149781

transition_topology_soft
<-> transition_topology_windowed

distance = 0.18056298416

This confirms that observer redundancy is now measurable.


---

Why The FAIL Is Useful

The result gives a precise next pressure point.

The problem is no longer:

no medium geometry exists

The problem is now:

medium geometry exists,
but not densely enough

This is a better failure.

It means the framework is moving from binary separation toward continuous observer-space measurement.


---

Relation To Observer Family Geometry

This result is the strongest executable support so far for:

OBSERVER_FAMILY_GEOMETRY

v2 demonstrates that observer families can be described through:

redundancy
medium distance
diversity
family structure
observer uniqueness


---

Relation To Recoverability Score

Recoverability score depends on observer weighting.

Observer weighting depends on observer geometry.

v2 provides a more usable geometry than v0 or v1 because it can assign different observer weights based on:

local redundancy
medium relation
high diversity

This is closer to the intended recoverability framework.


---

Relation To Multi-Projection Recovery

Multi-projection recovery becomes stronger when observers are not redundant.

v2 can now begin to support this distinction.

For example:

recovery under two redundant observers

should count less than:

recovery under two medium or diverse observers

v2 makes that distinction measurable.


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
under a shared response feature space


---

Limitations

This is not the full OMNIA engine.

This is a toy observer geometry experiment.

Observer response vectors are manually weighted.

Feature-space geometry is heuristic.

Observer families are simplified.

No semantic truth is evaluated.

No universal observer geometry claim is made.

Medium-distance density remains below target.


---

Required Improvement For v3

v3 should focus on increasing medium-distance density without destroying redundancy or diversity.

Minimum goals:

1. keep redundant_pair_count > 0

2. increase medium_pair_count to at least 10

3. preserve diverse_pair_count > 0

4. keep average_distance below 0.80

5. avoid collapsing all observers into medium similarity

6. reduce hard distance = 1.0 cases where possible

7. add response-correlation smoothing

8. compute observer coverage or entropy

Expected v3 behavior:

redundant > 0
medium >= 10
diverse > 0
average_distance < 0.80


---

Final Result

FAIL — observer family geometry v2 did not satisfy pass condition.

Correct technical conclusion:

v2 partially succeeds:
it reduces distance saturation
and creates medium-distance observer relations,
but still fails the required medium-density threshold.

This is a useful negative result and a clear bridge toward v3.