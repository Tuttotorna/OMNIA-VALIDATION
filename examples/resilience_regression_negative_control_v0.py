#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Resilience Regression Negative Control v0

Purpose:
    Validate that the regression harness is capable of failing when critical
    invariants are intentionally broken.

Previous chain:
    resilience_regression_suite_v0:
        all selected projection/resilience components passed
        4/4 components passed
        15/15 critical checks passed
        -> PASS / REGRESSION_SUITE_PASSED

This experiment asks:
    Does the harness detect deliberate structural regression?

Core boundary:
    measurement != inference != decision

Claim level:
    Level 1 — Negative Control

Expected result:
    PASS for this experiment means the negative control successfully caused
    regression detection.

Important:
    The simulated component result should fail.
    The negative-control experiment should pass because the failure was detected.

PASS condition:
    at least three injected regressions are detected
    and at least one clean control remains passing
    and negative_control_detection_rate >= 0.75
"""

from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


EXPERIMENT_NAME = "resilience_regression_negative_control_v0"
DOMAIN = "regression_harness_failure_sensitivity"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "resilience_regression_negative_control_v0.json"


# ---------------------------------------------------------------------
# Canonical baseline fixtures
# ---------------------------------------------------------------------

def valid_fixture_cross_domain_invariance_v0_2() -> Dict[str, Any]:
    return {
        "experiment_name": "cross_domain_invariance_v0_2",
        "status": "PASS",
        "raw_combined_analysis": {
            "separation_margin": 0.052785411892,
        },
        "normalized_combined_analysis": {
            "separation_margin": 0.602173482822,
            "within_lower_than_cross": True,
            "mean_within_structure_distance": 0.251457342874,
            "mean_cross_structure_distance": 0.853630825696,
        },
        "noise_gradient": {
            "noise_gradient_detected": True,
            "total_violation_count": 0,
        },
    }


def valid_fixture_adversarial_representation_v0() -> Dict[str, Any]:
    return {
        "experiment_name": "adversarial_representation_v0",
        "status": "PASS",
        "operational_classification": "BOUNDARY_DETECTED",
        "attack_count": 8,
        "false_merge_attacks": [
            {"attack": "false_merge"},
        ],
        "false_split_attacks": [
            {"attack": "false_split"},
        ],
        "control_analysis": {
            "controls_ok": True,
        },
    }


def valid_fixture_projection_boundary_map_v0() -> Dict[str, Any]:
    return {
        "experiment_name": "projection_boundary_map_v0",
        "status": "PASS",
        "operational_classification": "BOUNDARY_MAP_BUILT",
        "boundary_summary": {
            "attack_family_count": 7,
            "observed_effect_count": 3,
            "detected_boundary_count": 7,
            "control_ok": True,
        },
    }


def valid_fixture_projection_resilience_layer_v0() -> Dict[str, Any]:
    return {
        "experiment_name": "projection_resilience_layer_v0",
        "status": "PASS",
        "operational_classification": "TOY_RESILIENCE_LAYER_VALIDATED",
        "summary": {
            "mitigation_success_rate": 0.75,
            "control_preservation": True,
            "control_preservation_rate": 1.0,
            "stability_gain": 0.833333333333,
            "baseline_failure_count": 6,
            "resilient_failure_count": 1,
        },
    }


# ---------------------------------------------------------------------
# Critical checks copied from regression harness logic
# ---------------------------------------------------------------------

def evaluate_cross_domain_checks(result: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    checks: Dict[str, Dict[str, Any]] = {}

    raw = result.get("raw_combined_analysis", {})
    normalized = result.get("normalized_combined_analysis", {})
    noise = result.get("noise_gradient", {})

    raw_margin = raw.get("separation_margin")
    normalized_margin = normalized.get("separation_margin")

    checks["normalized_margin_greater_than_raw_margin"] = {
        "passed": (
            raw_margin is not None
            and normalized_margin is not None
            and normalized_margin > raw_margin
        ),
        "raw_margin": raw_margin,
        "normalized_margin": normalized_margin,
    }

    checks["noise_gradient_detected"] = {
        "passed": noise.get("noise_gradient_detected") is True,
        "noise_gradient_detected": noise.get("noise_gradient_detected"),
        "total_violation_count": noise.get("total_violation_count"),
    }

    checks["normalized_within_lower_than_cross"] = {
        "passed": normalized.get("within_lower_than_cross") is True,
        "within_lower_than_cross": normalized.get("within_lower_than_cross"),
        "mean_within": normalized.get("mean_within_structure_distance"),
        "mean_cross": normalized.get("mean_cross_structure_distance"),
    }

    return checks


def evaluate_adversarial_checks(result: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    checks: Dict[str, Dict[str, Any]] = {}

    false_merge_attacks = result.get("false_merge_attacks", [])
    false_split_attacks = result.get("false_split_attacks", [])
    control_analysis = result.get("control_analysis", {})

    attack_count = result.get("attack_count")

    checks["attack_count_positive"] = {
        "passed": attack_count is not None and attack_count > 0,
        "attack_count": attack_count,
    }

    checks["controls_ok"] = {
        "passed": control_analysis.get("controls_ok") is True,
        "controls_ok": control_analysis.get("controls_ok"),
    }

    checks["false_merge_attacks_detected"] = {
        "passed": len(false_merge_attacks) > 0,
        "false_merge_attack_count": len(false_merge_attacks),
    }

    checks["false_split_attacks_detected"] = {
        "passed": len(false_split_attacks) > 0,
        "false_split_attack_count": len(false_split_attacks),
    }

    return checks


def evaluate_boundary_map_checks(result: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    checks: Dict[str, Dict[str, Any]] = {}

    summary = result.get("boundary_summary", {})

    attack_family_count = summary.get("attack_family_count")
    observed_effect_count = summary.get("observed_effect_count")
    detected_boundary_count = summary.get("detected_boundary_count")

    checks["attack_family_count_minimum"] = {
        "passed": attack_family_count is not None and attack_family_count >= 4,
        "attack_family_count": attack_family_count,
    }

    checks["observed_effect_count_minimum"] = {
        "passed": observed_effect_count is not None and observed_effect_count >= 3,
        "observed_effect_count": observed_effect_count,
    }

    checks["detected_boundary_count_minimum"] = {
        "passed": detected_boundary_count is not None and detected_boundary_count >= 5,
        "detected_boundary_count": detected_boundary_count,
    }

    checks["control_ok"] = {
        "passed": summary.get("control_ok") is True,
        "control_ok": summary.get("control_ok"),
    }

    return checks


def evaluate_resilience_layer_checks(result: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    checks: Dict[str, Dict[str, Any]] = {}

    summary = result.get("summary", {})

    mitigation_success_rate = summary.get("mitigation_success_rate")
    stability_gain = summary.get("stability_gain")
    baseline_failure_count = summary.get("baseline_failure_count")
    resilient_failure_count = summary.get("resilient_failure_count")

    checks["mitigation_success_rate_minimum"] = {
        "passed": (
            mitigation_success_rate is not None
            and mitigation_success_rate >= 0.50
        ),
        "mitigation_success_rate": mitigation_success_rate,
    }

    checks["control_preservation"] = {
        "passed": summary.get("control_preservation") is True,
        "control_preservation": summary.get("control_preservation"),
        "control_preservation_rate": summary.get("control_preservation_rate"),
    }

    checks["stability_gain_positive"] = {
        "passed": stability_gain is not None and stability_gain > 0.0,
        "stability_gain": stability_gain,
    }

    checks["resilient_failure_count_below_baseline"] = {
        "passed": (
            baseline_failure_count is not None
            and resilient_failure_count is not None
            and resilient_failure_count < baseline_failure_count
        ),
        "baseline_failure_count": baseline_failure_count,
        "resilient_failure_count": resilient_failure_count,
    }

    return checks


def all_checks_pass(checks: Dict[str, Dict[str, Any]]) -> bool:
    return all(item.get("passed") is True for item in checks.values())


def failed_check_names(checks: Dict[str, Dict[str, Any]]) -> List[str]:
    return [
        name
        for name, item in checks.items()
        if item.get("passed") is not True
    ]


# ---------------------------------------------------------------------
# Regression injection
# ---------------------------------------------------------------------

def inject_cross_domain_margin_regression(result: Dict[str, Any]) -> Dict[str, Any]:
    mutated = copy.deepcopy(result)

    mutated["normalized_combined_analysis"]["separation_margin"] = (
        mutated["raw_combined_analysis"]["separation_margin"]
    )

    return mutated


def inject_cross_domain_noise_regression(result: Dict[str, Any]) -> Dict[str, Any]:
    mutated = copy.deepcopy(result)

    mutated["noise_gradient"]["noise_gradient_detected"] = False
    mutated["noise_gradient"]["total_violation_count"] = 2

    return mutated


def inject_adversarial_controls_regression(result: Dict[str, Any]) -> Dict[str, Any]:
    mutated = copy.deepcopy(result)

    mutated["control_analysis"]["controls_ok"] = False

    return mutated


def inject_adversarial_attack_disappearance(result: Dict[str, Any]) -> Dict[str, Any]:
    mutated = copy.deepcopy(result)

    mutated["attack_count"] = 0
    mutated["false_merge_attacks"] = []
    mutated["false_split_attacks"] = []

    return mutated


def inject_boundary_map_count_regression(result: Dict[str, Any]) -> Dict[str, Any]:
    mutated = copy.deepcopy(result)

    mutated["boundary_summary"]["attack_family_count"] = 2
    mutated["boundary_summary"]["detected_boundary_count"] = 2

    return mutated


def inject_boundary_map_control_regression(result: Dict[str, Any]) -> Dict[str, Any]:
    mutated = copy.deepcopy(result)

    mutated["boundary_summary"]["control_ok"] = False

    return mutated


def inject_resilience_mitigation_regression(result: Dict[str, Any]) -> Dict[str, Any]:
    mutated = copy.deepcopy(result)

    mutated["summary"]["mitigation_success_rate"] = 0.25

    return mutated


def inject_resilience_failure_count_regression(result: Dict[str, Any]) -> Dict[str, Any]:
    mutated = copy.deepcopy(result)

    mutated["summary"]["resilient_failure_count"] = (
        mutated["summary"]["baseline_failure_count"]
    )
    mutated["summary"]["stability_gain"] = 0.0

    return mutated


# ---------------------------------------------------------------------
# Negative control cases
# ---------------------------------------------------------------------

def build_negative_control_cases() -> List[Dict[str, Any]]:
    return [
        {
            "case_id": "clean_cross_domain_fixture",
            "component": "cross_domain_invariance_v0_2",
            "mutation": "none",
            "expected_detection": False,
            "fixture": valid_fixture_cross_domain_invariance_v0_2(),
            "mutator": None,
            "evaluator": evaluate_cross_domain_checks,
        },
        {
            "case_id": "break_normalized_margin",
            "component": "cross_domain_invariance_v0_2",
            "mutation": "normalized_margin_equal_to_raw_margin",
            "expected_detection": True,
            "fixture": valid_fixture_cross_domain_invariance_v0_2(),
            "mutator": inject_cross_domain_margin_regression,
            "evaluator": evaluate_cross_domain_checks,
        },
        {
            "case_id": "break_noise_gradient",
            "component": "cross_domain_invariance_v0_2",
            "mutation": "noise_gradient_false",
            "expected_detection": True,
            "fixture": valid_fixture_cross_domain_invariance_v0_2(),
            "mutator": inject_cross_domain_noise_regression,
            "evaluator": evaluate_cross_domain_checks,
        },
        {
            "case_id": "break_adversarial_controls",
            "component": "adversarial_representation_v0",
            "mutation": "controls_ok_false",
            "expected_detection": True,
            "fixture": valid_fixture_adversarial_representation_v0(),
            "mutator": inject_adversarial_controls_regression,
            "evaluator": evaluate_adversarial_checks,
        },
        {
            "case_id": "break_attack_detection",
            "component": "adversarial_representation_v0",
            "mutation": "attack_count_zero",
            "expected_detection": True,
            "fixture": valid_fixture_adversarial_representation_v0(),
            "mutator": inject_adversarial_attack_disappearance,
            "evaluator": evaluate_adversarial_checks,
        },
        {
            "case_id": "break_boundary_map_counts",
            "component": "projection_boundary_map_v0",
            "mutation": "insufficient_boundary_counts",
            "expected_detection": True,
            "fixture": valid_fixture_projection_boundary_map_v0(),
            "mutator": inject_boundary_map_count_regression,
            "evaluator": evaluate_boundary_map_checks,
        },
        {
            "case_id": "break_boundary_map_control",
            "component": "projection_boundary_map_v0",
            "mutation": "boundary_control_false",
            "expected_detection": True,
            "fixture": valid_fixture_projection_boundary_map_v0(),
            "mutator": inject_boundary_map_control_regression,
            "evaluator": evaluate_boundary_map_checks,
        },
        {
            "case_id": "break_resilience_mitigation_rate",
            "component": "projection_resilience_layer_v0",
            "mutation": "mitigation_success_rate_below_threshold",
            "expected_detection": True,
            "fixture": valid_fixture_projection_resilience_layer_v0(),
            "mutator": inject_resilience_mitigation_regression,
            "evaluator": evaluate_resilience_layer_checks,
        },
        {
            "case_id": "break_resilience_failure_count",
            "component": "projection_resilience_layer_v0",
            "mutation": "resilient_failure_count_equals_baseline",
            "expected_detection": True,
            "fixture": valid_fixture_projection_resilience_layer_v0(),
            "mutator": inject_resilience_failure_count_regression,
            "evaluator": evaluate_resilience_layer_checks,
        },
    ]


def analyze_case(case: Dict[str, Any]) -> Dict[str, Any]:
    original = copy.deepcopy(case["fixture"])

    if case["mutator"] is None:
        mutated = copy.deepcopy(original)
    else:
        mutated = case["mutator"](original)

    checks = case["evaluator"](mutated)

    detected_regression = not all_checks_pass(checks)

    expected_detection = case["expected_detection"]

    expectation_met = detected_regression == expected_detection

    return {
        "case_id": case["case_id"],
        "component": case["component"],
        "mutation": case["mutation"],
        "expected_detection": expected_detection,
        "detected_regression": detected_regression,
        "expectation_met": expectation_met,
        "failed_checks": failed_check_names(checks),
        "checks": checks,
    }


def build_summary(case_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_cases = len(case_results)

    clean_cases = [
        item
        for item in case_results
        if item["expected_detection"] is False
    ]

    injected_cases = [
        item
        for item in case_results
        if item["expected_detection"] is True
    ]

    detected_injected = [
        item
        for item in injected_cases
        if item["detected_regression"] is True
    ]

    clean_preserved = [
        item
        for item in clean_cases
        if item["detected_regression"] is False
    ]

    expectation_met_count = sum(
        1
        for item in case_results
        if item["expectation_met"] is True
    )

    negative_control_detection_rate = (
        len(detected_injected) / len(injected_cases)
        if injected_cases
        else 0.0
    )

    clean_control_preservation_rate = (
        len(clean_preserved) / len(clean_cases)
        if clean_cases
        else 0.0
    )

    return {
        "total_cases": total_cases,
        "clean_case_count": len(clean_cases),
        "injected_regression_case_count": len(injected_cases),
        "detected_injected_regression_count": len(detected_injected),
        "clean_control_preserved_count": len(clean_preserved),
        "expectation_met_count": expectation_met_count,
        "negative_control_detection_rate": round(negative_control_detection_rate, 12),
        "clean_control_preservation_rate": round(clean_control_preservation_rate, 12),
        "all_expectations_met": expectation_met_count == total_cases,
    }


def build_result(case_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary = build_summary(case_results)

    pass_condition = (
        summary["detected_injected_regression_count"] >= 3
        and summary["clean_control_preservation_rate"] == 1.0
        and summary["negative_control_detection_rate"] >= 0.75
        and summary["all_expectations_met"] is True
    )

    if pass_condition:
        status = "PASS"
        operational_classification = "REGRESSION_DETECTION_VALIDATED"
    else:
        status = "FAIL"
        operational_classification = "REGRESSION_DETECTION_NOT_VALIDATED"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Validate that the regression harness detects deliberately injected "
            "critical invariant failures."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Negative Control",
        "case_results": case_results,
        "summary": summary,
        "pass_condition": (
            "detected_injected_regression_count >= 3 and "
            "clean_control_preservation_rate == 1.0 and "
            "negative_control_detection_rate >= 0.75 and "
            "all_expectations_met == true"
        ),
        "status": status,
        "operational_classification": operational_classification,
        "main_insight": (
            "The regression harness is sensitive to deliberately injected "
            "structural invariant failures."
        ),
        "interpretation": (
            "PASS means the negative control successfully triggered regression "
            "detection while preserving the clean control case."
            if status == "PASS"
            else
            "FAIL means the negative control did not reliably demonstrate "
            "regression sensitivity."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy negative-control test.",
            "Regressions are injected into fixtures, not into live code.",
            "It validates harness sensitivity only for selected invariants.",
            "It does not discover new failure modes.",
            "It does not prove universal robustness.",
            "No semantic truth is evaluated.",
        ],
        "reproduction_command": "python examples/resilience_regression_negative_control_v0.py",
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    cases = build_negative_control_cases()
    case_results = [analyze_case(case) for case in cases]
    result = build_result(case_results)

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("OMNIA-VALIDATION — Resilience Regression Negative Control v0")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Operational classification: {result['operational_classification']}")
    print(f"Claim level: {result['claim_level']}")
    print()

    print("Negative-control cases:")
    for item in result["case_results"]:
        print(
            f"  {item['case_id']:38s} "
            f"component={item['component']:34s} "
            f"expected_detection={str(item['expected_detection']):5s} "
            f"detected={str(item['detected_regression']):5s} "
            f"expectation_met={str(item['expectation_met']):5s} "
            f"failed_checks={item['failed_checks']}"
        )

    print()
    print("Summary:")
    summary = result["summary"]
    print(f"  total_cases:                         {summary['total_cases']}")
    print(f"  clean_case_count:                    {summary['clean_case_count']}")
    print(f"  injected_regression_case_count:      {summary['injected_regression_case_count']}")
    print(f"  detected_injected_regression_count:  {summary['detected_injected_regression_count']}")
    print(f"  clean_control_preserved_count:       {summary['clean_control_preserved_count']}")
    print(f"  expectation_met_count:               {summary['expectation_met_count']}")
    print(f"  negative_control_detection_rate:     {summary['negative_control_detection_rate']}")
    print(f"  clean_control_preservation_rate:     {summary['clean_control_preservation_rate']}")
    print(f"  all_expectations_met:                {summary['all_expectations_met']}")

    print()
    print("Pass condition:")
    print(f"  {result['pass_condition']}")

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()