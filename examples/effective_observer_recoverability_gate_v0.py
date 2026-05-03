import json
import os
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"
RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "effective_observer_recoverability_gate_v0.json",
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


def compute_adversarial_divergence(normalized_effective, recoverability_score):
    return abs(normalized_effective - recoverability_score)


def gate_action(
    normalized_effective,
    recoverability_score,
    projection_stability,
    collapse_resistance,
    family_balance,
    non_redundancy,
    adversarial_divergence,
):
    if collapse_resistance < 0.10 or projection_stability < 0.10:
        return "COLLAPSE"

    if adversarial_divergence >= 0.55:
        return "ESCALATE"

    if recoverability_score < 0.30:
        return "RETRY"

    if family_balance < 0.35 or non_redundancy < 0.35:
        return "FLAG"

    if normalized_effective < 0.05 and recoverability_score >= 0.50:
        return "FLAG"

    if adversarial_divergence >= 0.30:
        return "FLAG"

    return "PASS"


def build_case(case_name):
    if case_name == "clean_balanced":
        raw = 40
        non_red = 0.95
        family = 0.95
        entropy = 0.55
        collapse = 0.90
        stability = 0.90

    elif case_name == "high_raw_duplicate":
        raw = 80
        non_red = 0.15
        family = 0.25
        entropy = 0.85
        collapse = 0.20
        stability = 0.30

    elif case_name == "projection_collapse":
        raw = 60
        non_red = 0.95
        family = 0.95
        entropy = 0.80
        collapse = 0.95
        stability = 0.05

    elif case_name == "collapse_resistance_failure":
        raw = 52
        non_red = 0.90
        family = 0.90
        entropy = 0.60
        collapse = 0.05
        stability = 0.75

    elif case_name == "balanced_but_dependent":
        raw = 50
        non_red = 0.35
        family = 1.00
        entropy = 0.45
        collapse = 0.25
        stability = 0.40

    elif case_name == "sparse_but_independent":
        raw = 8
        non_red = 1.00
        family = 0.80
        entropy = 0.20
        collapse = 0.90
        stability = 0.95

    elif case_name == "entropy_inflation":
        raw = 55
        non_red = 0.50
        family = 0.50
        entropy = 1.00
        collapse = 0.20
        stability = 0.25

    elif case_name == "observer_alias_attack":
        raw = 48
        non_red = 0.25
        family = 0.40
        entropy = 0.75
        collapse = 0.35
        stability = 0.30

    elif case_name == "partial_collapse":
        raw = 45
        non_red = 0.60
        family = 0.70
        entropy = 0.55
        collapse = 0.15
        stability = 0.20

    elif case_name == "hidden_single_point_failure":
        raw = 52
        non_red = 0.90
        family = 0.90
        entropy = 0.60
        collapse = 0.05
        stability = 0.10

    else:
        raise ValueError(f"unknown case: {case_name}")

    effective_count = compute_effective_count(
        raw,
        non_red,
        family,
        entropy,
        collapse,
        stability,
    )

    normalized_effective = safe_div(effective_count, raw)

    recoverability_score = compute_recoverability_score(
        non_red,
        family,
        entropy,
        collapse,
        stability,
    )

    adversarial_divergence = compute_adversarial_divergence(
        normalized_effective,
        recoverability_score,
    )

    action = gate_action(
        normalized_effective=normalized_effective,
        recoverability_score=recoverability_score,
        projection_stability=stability,
        collapse_resistance=collapse,
        family_balance=family,
        non_redundancy=non_red,
        adversarial_divergence=adversarial_divergence,
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
        "adversarial_divergence": adversarial_divergence,
        "gate_action": action,
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    cases = [
        "clean_balanced",
        "high_raw_duplicate",
        "projection_collapse",
        "collapse_resistance_failure",
        "balanced_but_dependent",
        "sparse_but_independent",
        "entropy_inflation",
        "observer_alias_attack",
        "partial_collapse",
        "hidden_single_point_failure",
    ]

    results = [build_case(case) for case in cases]

    action_counts = {}

    for item in results:
        action = item["gate_action"]
        action_counts[action] = action_counts.get(action, 0) + 1

    flagged_count = sum(
        1
        for item in results
        if item["gate_action"] in {"FLAG", "RETRY", "ESCALATE", "COLLAPSE"}
    )

    pass_count = action_counts.get("PASS", 0)

    divergence_values = [
        item["adversarial_divergence"]
        for item in results
    ]

    summary = {
        "case_count": len(results),
        "pass_count": pass_count,
        "flagged_count": flagged_count,
        "action_counts": action_counts,
        "mean_adversarial_divergence": mean(divergence_values),
        "max_adversarial_divergence": max(divergence_values),
    }

    status = "PASS" if flagged_count >= 7 and pass_count >= 1 else "CHECK"

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "results": results,
        "reproduction_command": "python examples/effective_observer_recoverability_gate_v0.py",
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION - Effective Observer Recoverability Gate v0")
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
            f"{item['case']:<36} "
            f"action={item['gate_action']:<9} "
            f"raw={item['raw_count']:<3} "
            f"effective={item['effective_count']:.6f} "
            f"norm_eff={item['normalized_effective']:.6f} "
            f"recoverability={item['recoverability_score']:.6f} "
            f"divergence={item['adversarial_divergence']:.6f}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - recoverability gate detected adversarial boundary cases."
        )
    else:
        print(
            "CHECK - gate did not detect enough adversarial boundary cases."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()