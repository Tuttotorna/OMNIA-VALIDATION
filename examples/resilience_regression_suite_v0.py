#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Resilience Regression Suite v0

Purpose:
    Run the current projection / resilience validation chain as a regression
    suite.

Previous chain:
    cross_domain_invariance_v0_2:
        normalization preserved structure under deterministic noise
        -> PASS

    adversarial_representation_v0:
        false merge and false split boundaries were detected
        -> PASS / BOUNDARY_DETECTED

    projection_boundary_map_v0:
        projection failure modes were mapped by attack family
        -> PASS / BOUNDARY_MAP_BUILT

    projection_resilience_layer_v0:
        selected projection failures were mitigated while controls were preserved
        -> PASS / TOY_RESILIENCE_LAYER_VALIDATED

This suite asks:
    Do all known projection boundary and resilience experiments still pass
    together after future changes?

Core boundary:
    measurement != inference != decision

Claim level:
    Level 1 — Regression Harness

PASS condition:
    all component scripts execute with return_code == 0
    and all component statuses are PASS
    and critical invariants are preserved
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


EXPERIMENT_NAME = "resilience_regression_suite_v0"
DOMAIN = "projection_resilience_regression_harness"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "resilience_regression_suite_v0.json"


COMPONENTS = [
    {
        "name": "cross_domain_invariance_v0_2",
        "script": "examples/cross_domain_invariance_v0_2.py",
        "result": "results/cross_domain_invariance_v0_2.json",
        "expected_status": "PASS",
        "expected_operational_classification": None,
        "critical_checks": [
            "normalized_margin_greater_than_raw_margin",
            "noise_gradient_detected",
            "normalized_within_lower_than_cross",
        ],
    },
    {
        "name": "adversarial_representation_v0",
        "script": "examples/adversarial_representation_v0.py",
        "result": "results/adversarial_representation_v0.json",
        "expected_status": "PASS",
        "expected_operational_classification": "BOUNDARY_DETECTED",
        "critical_checks": [
            "attack_count_positive",
            "controls_ok",
            "false_merge_attacks_detected",
            "false_split_attacks_detected",
        ],
    },
    {
        "name": "projection_boundary_map_v0",
        "script": "examples/projection_boundary_map_v0.py",
        "result": "results/projection_boundary_map_v0.json",
        "expected_status": "PASS",
        "expected_operational_classification": "BOUNDARY_MAP_BUILT",
        "critical_checks": [
            "attack_family_count_minimum",
            "observed_effect_count_minimum",
            "detected_boundary_count_minimum",
            "control_ok",
        ],
    },
    {
        "name": "projection_resilience_layer_v0",
        "script": "examples/projection_resilience_layer_v0.py",
        "result": "results/projection_resilience_layer_v0.json",
        "expected_status": "PASS",
        "expected_operational_classification": "TOY_RESILIENCE_LAYER_VALIDATED",
        "critical_checks": [
            "mitigation_success_rate_minimum",
            "control_preservation",
            "stability_gain_positive",
            "resilient_failure_count_below_baseline",
        ],
    },
]


# ---------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON result: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def run_component(component: Dict[str, Any]) -> Dict[str, Any]:
    script_path = ROOT / component["script"]
    result_path = ROOT / component["result"]

    if not script_path.exists():
        return {
            "name": component["name"],
            "script": component["script"],
            "result": component["result"],
            "return_code": None,
            "executed": False,
            "status": "MISSING_SCRIPT",
            "operational_classification": None,
            "stdout": "",
            "stderr": f"Missing script: {script_path}",
            "critical_checks": {},
            "critical_check_passed": False,
            "component_passed": False,
        }

    completed = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    stdout = completed.stdout
    stderr = completed.stderr

    parsed_result: Optional[Dict[str, Any]] = None

    if completed.returncode == 0 and result_path.exists():
        parsed_result = read_json(result_path)

    status = (
        parsed_result.get("status")
        if parsed_result is not None
        else "NO_RESULT_JSON"
    )

    operational_classification = (
        parsed_result.get("operational_classification")
        if parsed_result is not None
        else None
    )

    critical_checks = (
        evaluate_critical_checks(component, parsed_result)
        if parsed_result is not None
        else {}
    )

    critical_check_passed = (
        all(item["passed"] for item in critical_checks.values())
        if critical_checks
        else False
    )

    expected_status_ok = status == component["expected_status"]

    expected_operational = component.get("expected_operational_classification")
    if expected_operational is None:
        expected_operational_ok = True
    else:
        expected_operational_ok = operational_classification == expected_operational

    component_passed = (
        completed.returncode == 0
        and expected_status_ok
        and expected_operational_ok
        and critical_check_passed
    )

    return {
        "name": component["name"],
        "script": component["script"],
        "result": component["result"],
        "return_code": completed.returncode,
        "executed": True,
        "status": status,
        "expected_status": component["expected_status"],
        "status_ok": expected_status_ok,
        "operational_classification": operational_classification,
        "expected_operational_classification": expected_operational,
        "operational_classification_ok": expected_operational_ok,
        "stdout_tail": tail(stdout, 40),
        "stderr_tail": tail(stderr, 40),
        "critical_checks": critical_checks,
        "critical_check_passed": critical_check_passed,
        "component_passed": component_passed,
    }


def tail(text: str, max_lines: int) -> str:
    if not text:
        return ""

    lines = text.splitlines()
    return "\n".join(lines[-max_lines:])


# ---------------------------------------------------------------------
# Critical invariant checks
# ---------------------------------------------------------------------

def evaluate_critical_checks(
    component: Dict[str, Any],
    result: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
    checks: Dict[str, Dict[str, Any]] = {}

    for check_name in component["critical_checks"]:
        if check_name == "normalized_margin_greater_than_raw_margin":
            raw = result.get("raw_combined_analysis", {})
            normalized = result.get("normalized_combined_analysis", {})

            raw_margin = raw.get("separation_margin")
            normalized_margin = normalized.get("separation_margin")

            passed = (
                raw_margin is not None
                and normalized_margin is not None
                and normalized_margin > raw_margin
            )

            checks[check_name] = {
                "passed": passed,
                "raw_margin": raw_margin,
                "normalized_margin": normalized_margin,
            }

        elif check_name == "noise_gradient_detected":
            noise = result.get("noise_gradient", {})
            passed = noise.get("noise_gradient_detected") is True

            checks[check_name] = {
                "passed": passed,
                "noise_gradient_detected": noise.get("noise_gradient_detected"),
                "total_violation_count": noise.get("total_violation_count"),
            }

        elif check_name == "normalized_within_lower_than_cross":
            normalized = result.get("normalized_combined_analysis", {})
            passed = normalized.get("within_lower_than_cross") is True

            checks[check_name] = {
                "passed": passed,
                "within_lower_than_cross": normalized.get("within_lower_than_cross"),
                "mean_within": normalized.get("mean_within_structure_distance"),
                "mean_cross": normalized.get("mean_cross_structure_distance"),
            }

        elif check_name == "attack_count_positive":
            attack_count = result.get("attack_count")
            passed = attack_count is not None and attack_count > 0

            checks[check_name] = {
                "passed": passed,
                "attack_count": attack_count,
            }

        elif check_name == "controls_ok":
            control_analysis = result.get("control_analysis", {})
            passed = control_analysis.get("controls_ok") is True

            checks[check_name] = {
                "passed": passed,
                "controls_ok": control_analysis.get("controls_ok"),
            }

        elif check_name == "false_merge_attacks_detected":
            attacks = result.get("false_merge_attacks", [])
            passed = len(attacks) > 0

            checks[check_name] = {
                "passed": passed,
                "false_merge_attack_count": len(attacks),
            }

        elif check_name == "false_split_attacks_detected":
            attacks = result.get("false_split_attacks", [])
            passed = len(attacks) > 0

            checks[check_name] = {
                "passed": passed,
                "false_split_attack_count": len(attacks),
            }

        elif check_name == "attack_family_count_minimum":
            summary = result.get("boundary_summary", {})
            count = summary.get("attack_family_count")
            passed = count is not None and count >= 4

            checks[check_name] = {
                "passed": passed,
                "attack_family_count": count,
            }

        elif check_name == "observed_effect_count_minimum":
            summary = result.get("boundary_summary", {})
            count = summary.get("observed_effect_count")
            passed = count is not None and count >= 3

            checks[check_name] = {
                "passed": passed,
                "observed_effect_count": count,
            }

        elif check_name == "detected_boundary_count_minimum":
            summary = result.get("boundary_summary", {})
            count = summary.get("detected_boundary_count")
            passed = count is not None and count >= 5

            checks[check_name] = {
                "passed": passed,
                "detected_boundary_count": count,
            }

        elif check_name == "control_ok":
            summary = result.get("boundary_summary", {})
            passed = summary.get("control_ok") is True

            checks[check_name] = {
                "passed": passed,
                "control_ok": summary.get("control_ok"),
            }

        elif check_name == "mitigation_success_rate_minimum":
            summary = result.get("summary", {})
            rate = summary.get("mitigation_success_rate")
            passed = rate is not None and rate >= 0.50

            checks[check_name] = {
                "passed": passed,
                "mitigation_success_rate": rate,
            }

        elif check_name == "control_preservation":
            summary = result.get("summary", {})
            passed = summary.get("control_preservation") is True

            checks[check_name] = {
                "passed": passed,
                "control_preservation": summary.get("control_preservation"),
                "control_preservation_rate": summary.get("control_preservation_rate"),
            }

        elif check_name == "stability_gain_positive":
            summary = result.get("summary", {})
            gain = summary.get("stability_gain")
            passed = gain is not None and gain > 0.0

            checks[check_name] = {
                "passed": passed,
                "stability_gain": gain,
            }

        elif check_name == "resilient_failure_count_below_baseline":
            summary = result.get("summary", {})
            baseline = summary.get("baseline_failure_count")
            resilient = summary.get("resilient_failure_count")

            passed = (
                baseline is not None
                and resilient is not None
                and resilient < baseline
            )

            checks[check_name] = {
                "passed": passed,
                "baseline_failure_count": baseline,
                "resilient_failure_count": resilient,
            }

        else:
            checks[check_name] = {
                "passed": False,
                "error": "Unknown critical check",
            }

    return checks


# ---------------------------------------------------------------------
# Suite aggregation
# ---------------------------------------------------------------------

def build_suite_summary(component_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_components = len(component_results)

    executed_count = sum(
        1
        for item in component_results
        if item["executed"] is True
    )

    passed_components = [
        item
        for item in component_results
        if item["component_passed"] is True
    ]

    failed_components = [
        item
        for item in component_results
        if item["component_passed"] is False
    ]

    critical_check_total = 0
    critical_check_passed = 0

    for component in component_results:
        for check in component.get("critical_checks", {}).values():
            critical_check_total += 1
            if check.get("passed") is True:
                critical_check_passed += 1

    all_components_passed = len(passed_components) == total_components

    all_return_codes_zero = all(
        item["return_code"] == 0
        for item in component_results
    )

    all_critical_checks_passed = (
        critical_check_total > 0
        and critical_check_passed == critical_check_total
    )

    regression_passed = (
        all_components_passed
        and all_return_codes_zero
        and all_critical_checks_passed
    )

    return {
        "total_components": total_components,
        "executed_count": executed_count,
        "passed_component_count": len(passed_components),
        "failed_component_count": len(failed_components),
        "failed_components": [item["name"] for item in failed_components],
        "all_components_passed": all_components_passed,
        "all_return_codes_zero": all_return_codes_zero,
        "critical_check_total": critical_check_total,
        "critical_check_passed": critical_check_passed,
        "all_critical_checks_passed": all_critical_checks_passed,
        "regression_passed": regression_passed,
    }


def build_result(component_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary = build_suite_summary(component_results)

    if summary["regression_passed"] is True:
        status = "PASS"
        operational_classification = "REGRESSION_SUITE_PASSED"
    else:
        status = "FAIL"
        operational_classification = "REGRESSION_SUITE_FAILED"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Run projection resilience experiments as a regression suite and "
            "verify critical invariants."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Regression Harness",
        "components": component_results,
        "summary": summary,
        "pass_condition": (
            "all component scripts return 0, all component statuses are PASS, "
            "and all critical invariants pass"
        ),
        "status": status,
        "operational_classification": operational_classification,
        "main_insight": (
            "Known projection boundary and resilience behavior can be checked as "
            "a reproducible regression harness."
        ),
        "interpretation": (
            "PASS means all known projection boundary and resilience experiments "
            "still satisfy their expected statuses and critical invariants."
            if status == "PASS"
            else
            "FAIL means at least one known projection boundary or resilience "
            "invariant regressed."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This suite only checks selected known experiments.",
            "It does not discover new failure modes.",
            "It does not prove universal robustness.",
            "It depends on toy scripts and toy metrics.",
            "No semantic truth is evaluated.",
        ],
        "reproduction_command": "python examples/resilience_regression_suite_v0.py",
    }


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    component_results = []

    print("=" * 80)
    print("OMNIA-VALIDATION — Resilience Regression Suite v0")
    print("=" * 80)
    print()

    for component in COMPONENTS:
        print("-" * 80)
        print(f"Running component: {component['name']}")
        print(f"Script: {component['script']}")
        print("-" * 80)

        component_result = run_component(component)
        component_results.append(component_result)

        print(f"Return code: {component_result['return_code']}")
        print(f"Status: {component_result['status']}")
        print(
            "Operational classification: "
            f"{component_result['operational_classification']}"
        )
        print(f"Component passed: {component_result['component_passed']}")

        if component_result["critical_checks"]:
            print("Critical checks:")
            for check_name, check in component_result["critical_checks"].items():
                print(f"  {check_name}: {check['passed']}")

        print()

    result = build_result(component_results)

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("REGRESSION SUITE SUMMARY")
    print("=" * 80)

    summary = result["summary"]
    print(f"Status: {result['status']}")
    print(f"Operational classification: {result['operational_classification']}")
    print(f"Total components: {summary['total_components']}")
    print(f"Executed components: {summary['executed_count']}")
    print(f"Passed components: {summary['passed_component_count']}")
    print(f"Failed components: {summary['failed_component_count']}")
    print(f"All return codes zero: {summary['all_return_codes_zero']}")
    print(f"Critical checks passed: {summary['critical_check_passed']}/{summary['critical_check_total']}")
    print(f"All critical checks passed: {summary['all_critical_checks_passed']}")
    print(f"Regression passed: {summary['regression_passed']}")

    if summary["failed_components"]:
        print()
        print("Failed components:")
        for name in summary["failed_components"]:
            print(f"  - {name}")

    print()
    print("Pass condition:")
    print(f"  {result['pass_condition']}")

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()