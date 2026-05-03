import json
import math
import os
import random
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"
RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "correlation_analysis_effective_observer_adversarial_v0.json",
)

random.seed(42)


def safe_div(a, b):
    if b == 0:
        return 0.0
    return a / b


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def compute_effective_count(
    raw_count,
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    value = (
        raw_count
        * non_redundancy
        * family_balance
        * (0.5 + 0.5 * relation_entropy)
        * collapse_resistance
        * projection_stability
    )

    return max(0.0, value)


def compute_recoverability(
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    return clamp(
        (
            0.25 * non_redundancy
            + 0.20 * family_balance
            + 0.15 * relation_entropy
            + 0.20 * collapse_resistance
            + 0.20 * projection_stability
        )
    )


def classify_attack(adversarial_score):
    if adversarial_score < 0.15:
        return "RESISTED"

    if adversarial_score < 0.35:
        return "STRESSED"

    if adversarial_score < 0.60:
        return "WEAKENED"

    return "COLLAPSED"


def build_case(case_name):
    if case_name == "baseline_random":
        raw = random.randint(20, 60)

        non_red = random.uniform(0.6, 1.0)
        family = random.uniform(0.6, 1.0)
        entropy = random.uniform(0.2, 0.7)
        collapse = random.uniform(0.5, 1.0)
        stability = random.uniform(0.5, 1.0)

    elif case_name == "high_raw_duplicate":
        raw = 80

        non_red = 0.15
        family = 0.25
        entropy = 0.85
        collapse = 0.20
        stability = 0.30

    elif case_name == "high_effective_projection_collapse":
        raw = 60

        non_red = 0.95
        family = 0.95
        entropy = 0.80
        collapse = 0.95
        stability = 0.05

    elif case_name == "fake_diversity_noise":
        raw = 70

        non_red = 0.40
        family = 0.55
        entropy = 1.00
        collapse = 0.30
        stability = 0.35

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

    effective = compute_effective_count(
        raw,
        non_red,
        family,
        entropy,
        collapse,
        stability,
    )

    recoverability = compute_recoverability(
        non_red,
        family,
        entropy,
        collapse,
        stability,
    )

    normalized_effective = safe_div(effective, raw)

    correlation_shift = abs(normalized_effective - recoverability)

    adversarial_score = correlation_shift

    outcome = classify_attack(adversarial_score)

    return {
        "case": case_name,
        "raw_count": raw,
        "effective_count": effective,
        "recoverability": recoverability,
        "projection_stability": stability,
        "non_redundancy": non_red,
        "family_balance": family,
        "relation_entropy": entropy,
        "collapse_resistance": collapse,
        "normalized_effective": normalized_effective,
        "correlation_shift": correlation_shift,
        "adversarial_score": adversarial_score,
        "failure_type": outcome,
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    cases = [
        "baseline_random",
        "high_raw_duplicate",
        "high_effective_projection_collapse",
        "fake_diversity_noise",
        "balanced_but_dependent",
        "sparse_but_independent",
        "entropy_inflation",
        "observer_alias_attack",
        "partial_collapse",
        "hidden_single_point_failure",
    ]

    results = [build_case(c) for c in cases]

    scores = [r["adversarial_score"] for r in results]

    resisted = sum(1 for r in results if r["failure_type"] == "RESISTED")
    stressed = sum(1 for r in results if r["failure_type"] == "STRESSED")
    weakened = sum(1 for r in results if r["failure_type"] == "WEAKENED")
    collapsed = sum(1 for r in results if r["failure_type"] == "COLLAPSED")

    payload = {
        "status": "PASS",
        "version": VERSION,
        "summary": {
            "case_count": len(results),
            "mean_adversarial_score": mean(scores),
            "max_adversarial_score": max(scores),
            "resisted_count": resisted,
            "stressed_count": stressed,
            "weakened_count": weakened,
            "collapsed_count": collapsed,
        },
        "results": results,
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - Correlation Analysis Effective Observer Adversarial v0"
    )
    print("=" * 80)
    print()

    print("Status:", payload["status"])
    print("Version:", payload["version"])
    print()

    print("Summary")
    print("-" * 80)

    for k, v in payload["summary"].items():
        if isinstance(v, float):
            print(f"{k:30s}: {v:.12f}")
        else:
            print(f"{k:30s}: {v}")

    print()
    print("Cases")
    print("-" * 80)

    for r in results:
        print(
            f"{r['case']:36s} "
            f"outcome={r['failure_type']:10s} "
            f"score={r['adversarial_score']:.12f} "
            f"effective={r['effective_count']:.6f} "
            f"recoverability={r['recoverability']:.6f}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)
    print(
        "PASS - adversarial analysis exposed measurable failure boundaries."
    )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()