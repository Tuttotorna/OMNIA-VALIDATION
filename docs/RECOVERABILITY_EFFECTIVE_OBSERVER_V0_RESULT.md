# Recoverability vs Effective Observer Count v0 — Result

## Status

```text
Status: NEGATIVE_RESULT
Version: 0.1.0
Claim level: Level 1 — Toy Demonstration


---

Purpose

This experiment tested whether effective_observer_count predicts structural recoverability better than raw observer count.

The intended hypothesis was:

effective_observer_count
predicts recoverability
better than raw_observer_count

The result did not confirm this hypothesis in v0.

Core boundary:

measurement != inference != decision


---

Experiment File

examples/recoverability_effective_observer_v0.py

Result file:

results/recoverability_effective_observer_v0.json

Reproduction command:

python examples/recoverability_effective_observer_v0.py


---

Results

base_system:
  raw_count = 12
  effective_count = 2.677125569494
  recoverability_score = 0.319309954668

duplicate_system:
  raw_count = 32
  effective_count = 4.189050523886
  recoverability_score = 0.138279316655

balanced_system:
  raw_count = 40
  effective_count = 9.616515593834
  recoverability_score = 0.101542207162

collapsed_system:
  raw_count = 30
  effective_count = 0.0
  recoverability_score = 0.009292827353


---

Recoverability Ranking

Observed ranking by recoverability:

1. base_system
2. duplicate_system
3. balanced_system
4. collapsed_system

Observed ranking by effective observer count:

1. balanced_system
2. duplicate_system
3. base_system
4. collapsed_system

These rankings do not match.

Therefore, v0 does not support the claim that effective_observer_count predicts recoverability.


---

Main Finding

The experiment produced a useful negative result.

It showed that the current toy recoverability function is not aligned with the effective observer count metric.

The strongest contradiction is:

balanced_system:
  effective_count = 9.616515593834
  recoverability_score = 0.101542207162

The balanced system had the highest effective observer count but only ranked third in recoverability.

This means the recoverability function introduced a bias that over-penalized large balanced observer systems.


---

Why The Result Failed

The problem is inside the recovery function:

diversity = len(set(o["family"] for o in observers)) / len(observers)

This penalizes systems with many observers, even if they are balanced.

For the balanced system:

family_count = 8
observer_count = 40
diversity = 8 / 40 = 0.2

For the base system:

family_count = 6
observer_count = 12
diversity = 6 / 12 = 0.5

So the balanced system was structurally punished for having more observers.

That makes the recovery score unsuitable for testing the intended hypothesis.


---

Correct Interpretation

This is not evidence that effective observer count is useless.

It is evidence that this v0 recoverability proxy is flawed.

Correct conclusion:

v0 recoverability_score does not validly test
whether effective_observer_count predicts recovery

More precise conclusion:

the recovery proxy confounds observer quantity
with diversity penalty


---

What Was Still Useful

The collapsed system behaved correctly:

collapsed_system:
  raw_count = 30
  effective_count = 0.0
  recoverability_score = 0.009292827353

This supports the weak boundary claim:

collapsed observer systems produce near-zero recoverability

However, the stronger claim failed:

higher effective_count -> higher recoverability


---

Result Classification

This result should not be classified as a clean PASS.

Recommended status:

NEGATIVE_RESULT

Alternative acceptable status:

REQUIRES_RETEST

Reason:

the experiment exposed a flaw in the recovery proxy
instead of confirming the intended hypothesis


---

Relation To Effective Observer Count

effective_observer_count_v0 successfully showed:

observer_count != effective_observer_count

This experiment tried to extend that result toward recoverability.

That extension failed in v0 because the recoverability proxy was not structurally aligned with the effective count metric.


---

Relation To OMNIA-VALIDATION

This is exactly the kind of result OMNIA-VALIDATION should preserve.

Validation is not confirmation.

A failed hypothesis is useful when it exposes:

a bad proxy
a misleading formula
a broken assumption
a measurement boundary

This experiment exposed a bad proxy.


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

the v0 recoverability proxy does not support
the intended effective-observer-count hypothesis


---

Limitations

This is not the full OMNIA engine.

This is a toy recoverability experiment.

The recovery score is synthetic.

The recovery score contains a flawed diversity penalty.

Observer systems are synthetic.

Projection values are simulated.

The random seed is fixed.

No semantic truth is evaluated.

No general recoverability law is claimed.


---

Required Next Step

The next step should correct the recovery proxy.

Recommended next experiment:

examples/recoverability_effective_observer_v1.py

The v1 recovery score should avoid:

family_count / observer_count

and instead use normalized family balance or effective observer factors directly.

Better candidate:

recoverability_score
=
coverage_quality
× non_redundancy
× family_balance
× collapse_resistance
× projection_accuracy

The v1 test should ask:

does corrected recoverability align better
with effective_observer_count
than with raw_observer_count?


---

Final Result

NEGATIVE_RESULT — recoverability_effective_observer_v0 did not confirm the intended hypothesis.

Correct technical conclusion:

the effective observer idea remains valid,
but this v0 recoverability proxy is invalid for testing it.