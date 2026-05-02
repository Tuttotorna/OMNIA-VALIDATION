# RESILIENCE REGRESSION NEGATIVE CONTROL v0

## Status

```text
PASS

Operational Classification

REGRESSION_DETECTION_VALIDATED

Claim Level

Level 1 — Negative Control


---

Purpose

This experiment validates that the regression harness is capable of detecting deliberately injected failures.

The goal is not to prove robustness.

The goal is to prove that the regression system is sensitive to structural invariant violations.

This is a negative-control experiment.


---

Core Boundary

measurement != inference != decision


---

What Is Being Tested

The regression harness from:

examples/resilience_regression_suite_v0.py

is challenged with intentionally corrupted fixtures.

The experiment verifies whether critical checks fail when known invariants are manually broken.


---

Tested Components

cross_domain_invariance_v0_2
adversarial_representation_v0
projection_boundary_map_v0
projection_resilience_layer_v0


---

Negative-Control Cases

Clean Control Case

clean_cross_domain_fixture

Expected detection: False
Detected regression: False
Expectation met: True

This validates that the harness does not incorrectly trigger failures on a clean valid fixture.


---

Injected Regression Cases

break_normalized_margin

Mutation:

normalized_margin_equal_to_raw_margin

Failed checks:

normalized_margin_greater_than_raw_margin

Result:

detected_regression = True


---

break_noise_gradient

Mutation:

noise_gradient_false

Failed checks:

noise_gradient_detected

Result:

detected_regression = True


---

break_adversarial_controls

Mutation:

controls_ok_false

Failed checks:

controls_ok

Result:

detected_regression = True


---

break_attack_detection

Mutation:

attack_count_zero

Failed checks:

attack_count_positive
false_merge_attacks_detected
false_split_attacks_detected

Result:

detected_regression = True


---

break_boundary_map_counts

Mutation:

insufficient_boundary_counts

Failed checks:

attack_family_count_minimum
detected_boundary_count_minimum

Result:

detected_regression = True


---

break_boundary_map_control

Mutation:

boundary_control_false

Failed checks:

control_ok

Result:

detected_regression = True


---

break_resilience_mitigation_rate

Mutation:

mitigation_success_rate_below_threshold

Failed checks:

mitigation_success_rate_minimum

Result:

detected_regression = True


---

break_resilience_failure_count

Mutation:

resilient_failure_count_equals_baseline

Failed checks:

stability_gain_positive
resilient_failure_count_below_baseline

Result:

detected_regression = True


---

Summary

Counts

total_cases                         = 9
clean_case_count                    = 1
injected_regression_case_count      = 8
detected_injected_regression_count  = 8
clean_control_preserved_count       = 1
expectation_met_count               = 9


---

Rates

negative_control_detection_rate     = 1.0
clean_control_preservation_rate     = 1.0
all_expectations_met                = True


---

Main Result

The regression harness successfully detected all deliberately injected failures.

At the same time:

the clean control remained valid

no false positive detection occurred on the clean fixture


This demonstrates that the regression suite is sensitive to invariant violations.


---

Main Insight

The regression harness is not merely replaying PASS statuses.

It is capable of detecting structural invariant corruption.

This establishes minimal evidence that the suite behaves as a real regression detector rather than a decorative execution wrapper.


---

Interpretation

PASS means:

injected invariant failures were detected

clean controls remained preserved

expected detection behavior matched observed behavior


This validates sensitivity of the regression harness for the tested toy invariants.


---

Pass Condition

detected_injected_regression_count >= 3
and clean_control_preservation_rate == 1.0
and negative_control_detection_rate >= 0.75
and all_expectations_met == true

Observed:

detected_injected_regression_count = 8
clean_control_preservation_rate    = 1.0
negative_control_detection_rate    = 1.0
all_expectations_met               = true

Result:

PASS


---

Reproduction

python examples/resilience_regression_negative_control_v0.py


---

Result File

results/resilience_regression_negative_control_v0.json


---

Limitations

This is not the full OMNIA engine.
This is a toy negative-control test.
Regressions are injected into fixtures, not into live code.
It validates harness sensitivity only for selected invariants.
It does not discover new failure modes.
It does not prove universal robustness.
No semantic truth is evaluated.


---

Final Conclusion

The regression system now contains:

1. positive validation
2. adversarial validation
3. boundary mapping
4. resilience mitigation
5. regression harness
6. negative-control sensitivity validation

This creates a minimal reproducible structural validation pipeline with:

PASS reproducibility
+
failure detection capability
+
known-boundary tracking
+
regression sensitivity