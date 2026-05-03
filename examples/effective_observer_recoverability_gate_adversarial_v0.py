import json
import os
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "effective_observer_recoverability_gate_adversarial_v0.json",
)


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def safe_div(a, b):
    if b == 0:
        return 0.0
    return a / b


def compute_effective_count(
    raw_count,
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    return max(
        0.0,
        raw_count
        * non_redundancy
        * family_balance
        * (0.5 + 0.5 * relation_entropy)
        * collapse_resistance
        * projection_stability,
    )


def compute_recoverability_score(
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    return clamp(
        0.25 * non_redundancy
        + 0.20 * family_balance
        + 0.15 * relation_entropy
        + 0.20 * collapse_resistance
        + 0.20 * projection_stability
    )


def compute_divergence(
    normalized_effective,
    recoverability_score,
):
    return abs(normalized_effective - recoverability_score)


def gate_action(
    normalized_effective,
    recoverability_score,
    projection_stability,
    collapse_resistance,
    family_balance,
    non_redundancy,
    divergence,
):
    if collapse_resistance < 0.10:
        return "COLLAPSE"

    if projection_stability < 0.10:
        return "COLLAPSE"

    if divergence >= 0.60:
        return "ESCALATE"

    if recoverability_score < 0.30:
        return "RETRY"

    if family_balance < 0.35:
        return "FLAG"

    if non_redundancy < 0.35:
        return "FLAG"

    if (
        normalized_effective < 0.05
        and recoverability_score >= 0.50
    ):
        return "FLAG"

    if divergence >= 0.35:
        return "FLAG"

    return "PASS"


def evaluate_case(case_name, params):
    raw = params["raw"]
    non_red = params["non_red"]
    family = params["family"]
    entropy = params["entropy"]
    collapse = params["collapse"]
    stability = params["stability"]

    effective_count = compute_effective_count(
        raw_count=raw,
        non_redundancy=non_red,
        family_balance=family,
        relation_entropy=entropy,
        collapse_resistance=collapse,
        projection_stability=stability,
    )

    normalized_effective = safe_div(effective_count, raw)

    recoverability_score = compute_recoverability_score(
        non_redundancy=non_red,
        family_balance=family,
        relation_entropy=entropy,
        collapse_resistance=collapse,
        projection_stability=stability,
    )

    divergence = compute_divergence(
        normalized_effective=normalized_effective,
        recoverability_score=recoverability_score,
    )

    action = gate_action(
        normalized_effective=normalized_effective,
        recoverability_score=recoverability_score,
        projection_stability=stability,
        collapse_resistance=collapse,
        family_balance=family,
        non_redundancy=non_red,
        divergence=divergence,
    )

    return {
        "case": case_name,
        "raw_count": raw,
        "effective_count": effective_count,
        "normalized_effective": normalized_effective,
        "recoverability_score": recoverability_score,
        "projection_stability": stability,
        "collapse_resistance": collapse,
        "family_balance": family,
        "non_redundancy": non_red,
        "relation_entropy": entropy,
        "divergence": divergence,
        "gate_action": action,
    }


def build_adversarial_cases():
    return {
        "clean_balanced": {
            "raw": 40,
            "non_red": 0.95,
            "family": 0.95,
            "entropy": 0.55,
            "collapse": 0.90,
            "stability": 0.90,
            "expected": "PASS",
        },

        "projection_collapse": {
            "raw": 60,
            "non_red": 0.95,
            "family": 0.95,
            "entropy": 0.80,
            "collapse": 0.95,
            "stability": 0.05,
            "expected": "COLLAPSE",
        },

        "collapse_resistance_failure": {
            "raw": 52,
            "non_red": 0.90,
            "family": 0.90,
            "entropy": 0.60,
            "collapse": 0.05,
            "stability": 0.75,
            "expected": "COLLAPSE",
        },

        "false_pass_probe": {
            "raw": 80,
            "non_red": 0.38,
            "family": 0.40,
            "entropy": 0.98,
            "collapse": 0.42,
            "stability": 0.45,
            "expected": "FLAG",
        },

        "false_collapse_probe": {
            "raw": 18,
            "non_red": 0.92,
            "family": 0.90,
            "entropy": 0.25,
            "collapse": 0.11,
            "stability": 0.12,
            "expected": "FLAG",
        },

        "boundary_ambiguity_probe": {
            "raw": 36,
            "non_red": 0.36,
            "family": 0.36,
            "entropy": 0.50,
            "collapse": 0.34,
            "stability": 0.34,
            "expected": "FLAG",
        },

        "signal_contradiction_probe": {
            "raw": 70,
            "non_red": 0.18,
            "family": 0.92,
            "entropy": 0.95,
            "collapse": 0.88,
            "stability": 0.91,
            "expected": "FLAG",
        },

        "high_effective_low_stability_probe": {
            "raw": 90,
            "non_red": 0.95,
            "family": 0.94,
            "entropy": 0.92,
            "collapse": 0.95,
            "stability": 0.11,
            "expected": "FLAG",
        },

        "low_effective_high_recovery_probe": {
            "raw": 16,
            "non_red": 0.85,
            "family": 0.88,
            "entropy": 0.20,
            "collapse": 0.91,
            "stability": 0.93,
            "expected": "PASS",
        },

        "threshold_exploitation_probe": {
            "raw": 50,
            "non_red": 0.351,
            "family": 0.351,
            "entropy": 0.999,
            "collapse": 0.301,
            "stability": 0.301,
            "expected": "FLAG",
        },

        "hidden_dependency_probe": {
            "raw": 75,
            "non_red": 0.21,
            "family": 0.87,
            "entropy": 0.89,
            "collapse": 0.82,
            "stability": 0.85,
            "expected": "FLAG",
        },

        "distributed_collapse_probe": {
            "raw": 44,
            "non_red": 0.41,
            "family": 0.44,
            "entropy": 0.60,
            "collapse": 0.14,
            "stability": 0.14,
            "expected": "FLAG",
        },
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    cases = build_adversarial_cases()

    results = []

    correct_count = 0
    false_pass_count = 0
    false_collapse_count = 0
    mismatch_count = 0

    for case_name, params in cases.items():
        expected = params["expected"]

        result = evaluate_case(case_name, params)

        predicted = result["gate_action"]

        result["expected_action"] = expected
        result["match"] = predicted == expected

        if predicted == expected:
            correct_count += 1
        else:
            mismatch_count += 1

        if expected != "PASS" and predicted == "PASS":
            false_pass_count += 1

        if expected == "PASS" and predicted == "COLLAPSE":
            false_collapse_count += 1

        results.append(result)

    divergence_values = [
        item["divergence"]
        for item in results
    ]

    pass_cases = [
        item
        for item in results
        if item["gate_action"] == "PASS"
    ]

    collapse_cases = [
        item
        for item in results
        if item["gate_action"] == "COLLAPSE"
    ]

    summary = {
        "case_count": len(results),
        "correct_count": correct_count,
        "mismatch_count": mismatch_count,
        "false_pass_count": false_pass_count,
        "false_collapse_count": false_collapse_count,
        "pass_count": len(pass_cases),
        "collapse_count": len(collapse_cases),
        "mean_divergence": mean(divergence_values),
        "max_divergence": max(divergence_values),
        "accuracy": safe_div(correct_count, len(results)),
    }

    status = (
        "PASS"
        if (
            false_pass_count == 0
            and false_collapse_count == 0
            and summary["accuracy"] >= 0.75
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "results": results,
        "reproduction_command": (
            "python examples/"
            "effective_observer_recoverability_gate_adversarial_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Effective Observer Recoverability Gate Adversarial v0"
    )
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)

    print()
    print("Summary")
    print("-" * 80)

    for key, value in summary.items():
        print(f"{key}: {value}")

    print()
    print("Cases")
    print("-" * 80)

    for item in results:
        print(
            f"{item['case']:<38} "
            f"expected={item['expected_action']:<10} "
            f"predicted={item['gate_action']:<10} "
            f"match={str(item['match']):<5} "
            f"divergence={item['divergence']:.12f}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - gate resisted adversarial gate-level probes."
        )
    else:
        print(
            "CHECK - gate exposed adversarial vulnerabilities."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()