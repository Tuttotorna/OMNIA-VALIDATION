# Recoverability vs Effective Observer Count v1 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 1 — Toy Demonstration


---

Purpose

This experiment retests the relation between effective_observer_count and structural recoverability after correcting the flawed v0 recovery proxy.

The v0 experiment produced a negative result because the recovery function penalized large balanced observer systems.

The v1 goal is to test a corrected proxy.

Core boundary:

measurement != inference != decision


---

Experiment File

examples/recoverability_effective_observer_v1.py

Result file:

results/recoverability_effective_observer_v1.json

Reproduction command:

python examples/recoverability_effective_observer_v1.py


---

Main Result

The v1 proxy fixed the main v0 failure.

The balanced system now ranks first in both effective count and recoverability:

balanced_system:
  raw_count = 40
  effective_count = 12.988021497284
  recoverability_score = 0.944132368906

The collapsed system correctly collapses to zero:

collapsed_system:
  raw_count = 24
  effective_count = 0.0
  recoverability_score = 0.0

However, effective_count is still not equivalent to recoverability.


---

Results

base_system:
  raw_count = 12
  effective_count = 3.885575001999
  recoverability_score = 0.919857579715
  projection_stability = 0.955037325049
  non_redundancy = 1.0
  family_balance = 1.0
  relation_entropy = 0.336181495014
  collapse_resistance = 0.963164010022

duplicate_system:
  raw_count = 36
  effective_count = 10.689955398699
  recoverability_score = 0.564839997560
  projection_stability = 0.901145449925
  non_redundancy = 0.931746031746
  family_balance = 0.722222222222
  relation_entropy = 0.473743041740
  collapse_resistance = 0.931455581153

balanced_system:
  raw_count = 40
  effective_count = 12.988021497284
  recoverability_score = 0.944132368906
  projection_stability = 0.944132368906
  non_redundancy = 1.0
  family_balance = 1.0
  relation_entropy = 0.324700537432
  collapse_resistance = 1.0

collapsed_system:
  raw_count = 24
  effective_count = 0.0
  recoverability_score = 0.0
  projection_stability = 1.0
  non_redundancy = 0.0
  family_balance = 1.0
  relation_entropy = 0.0
  collapse_resistance = 0.0


---

Ranking By Effective Count

1. balanced_system
2. duplicate_system
3. base_system
4. collapsed_system


---

Ranking By Recoverability

1. balanced_system
2. base_system
3. duplicate_system
4. collapsed_system

The rankings partially align.

They agree on:

balanced_system = strongest
collapsed_system = weakest

They disagree on:

base_system
duplicate_system


---

Interpretation

The corrected recoverability proxy behaves better than v0.

It no longer punishes the balanced system for having many observers.

This confirms that the v0 negative result was caused by a flawed proxy.

However, the duplicate system still shows a mismatch:

duplicate_system:
  effective_count = 10.689955398699
  recoverability_score = 0.564839997560

while:

base_system:
  effective_count = 3.885575001999
  recoverability_score = 0.919857579715

So effective_observer_count is not a complete recoverability metric.

It measures structural observer capacity, but recovery also depends on projection stability and the quality of the observer projections.


---

Correct Technical Conclusion

v1 fixes the v0 proxy bias,
but effective_count is still not equivalent to recoverability.

More precise:

effective_observer_count is a structural capacity estimate,
not a direct recoverability score.


---

What v1 Confirms

v1 supports these weaker claims:

collapsed observer systems have zero effective recovery capacity

balanced observer systems can produce high effective count and high recoverability

raw observer count alone remains misleading

proxy design strongly affects validation outcome

v1 does not prove:

higher effective_count always means higher recoverability


---

Why Duplicate System Matters

The duplicate system has high effective count because it still contains many non-identical pairwise distances.

But its recoverability is lower because its family balance and projection structure are weaker.

This means future effective-count metrics need stronger duplicate and family-correlation penalties.

Possible improvement:

effective_count_v2
=
raw_count
× non_redundancy
× family_balance
× relation_entropy
× collapse_resistance
× projection_quality
× anti_duplication_penalty


---

Relation To v0

v0 result:

NEGATIVE_RESULT

v0 failed because it used:

family_count / observer_count

That punished large balanced systems.

v1 removed that specific defect and produced a more coherent ranking.

Therefore:

v0 exposed proxy failure
v1 corrected the proxy failure


---

Relation To OMNIA-VALIDATION

This is the desired validation pattern:

define metric
test metric
find proxy failure
document negative result
correct proxy
retest
preserve both results

The value is not only in the PASS.

The value is in the measured correction path.


---

Boundary Statement

This experiment does not prove:

truth
meaning
semantic correctness
intelligence
causality
observer optimality
universal recoverability
full OMNIA correctness

It only shows:

a corrected toy recoverability proxy aligns better
with effective observer structure than v0,
while still remaining distinct from effective count itself


---

Limitations

This is not the full OMNIA engine.

This is a toy recoverability experiment.

Observer projections are synthetic.

The effective-count formula is exploratory.

The recoverability proxy is exploratory.

Only four systems were tested.

No statistical correlation analysis was performed.

No semantic truth is evaluated.

No universal recoverability law is claimed.


---

Required Next Step

The next step should move from four hand-built systems to many randomized systems.

Recommended experiment:

examples/correlation_analysis_effective_observer_v0.py

Purpose:

compare correlation between:

raw_count and recoverability

effective_count and recoverability

Required output:

corr(raw_count, recoverability)
corr(effective_count, recoverability)

Core question:

does effective_observer_count predict recoverability
better than raw observer count
across many randomized observer systems?


---

Final Result

PASS — recoverability_effective_observer_v1 corrected the v0 proxy bias.

Correct final conclusion:

effective_observer_count is useful,
but it is not identical to recoverability.