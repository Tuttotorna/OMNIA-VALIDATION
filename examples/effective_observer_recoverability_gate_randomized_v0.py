import json
import os
import random
from statistics import mean

VERSION = "0.1.0"

RANDOM_SEED = 42
SYSTEM_COUNT = 1000

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "effective_observer_recoverability_gate_randomized_v0.json",
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
    relation_entropy,
    divergence,
):
    if collapse_resistance < 0.10:
        return "COLLAPSE"

    if projection_stability < 0.10:
        return "COLLAPSE"

    if collapse_resistance < 0.16 and projection_stability < 0.16:
        return "FLAG"

    if normalized_effective < 0.01 and recoverability_score >= 0.30:
        return "FLAG"

    if divergence >= 0.60:
        return "ESCALATE"

    if recoverability_score < 0.30:
        return "RETRY"

    if family_balance < 0.35:
        return "FLAG"

    if non_redundancy < 0.35:
        return "FLAG"

    if relation_entropy > 0.90 and normalized_effective < 0.15:
        return "FLAG"

    if (
        normalized_effective < 0.05
        and recoverability_score >= 0.50
    ):
        return "FLAG"

    if divergence >= 0.35:
        return "FLAG"

    return "PASS"


def generate_system(system_id):
    raw_count = random.randint(4, 100)

    mode = random.choice(
        [
            "balanced",
            "redundant",
            "collapsed",
            "noisy",
            "sparse",
            "contradictory",
            "borderline",
        ]
    )

    if mode == "balanced":
        non_red = random.uniform(0.70, 1.00)
        family = random.uniform(0.70, 1.00)
        entropy = random.uniform(0.20, 0.70)
        collapse = random.uniform(0.65, 1.00)
        stability = random.uniform(0.65, 1.00)

    elif mode == "redundant":
        non_red = random.uniform(0.05, 0.35)
        family = random.uniform(0.30, 0.90)
        entropy = random.uniform(0.40, 1.00)
        collapse = random.uniform(0.35, 0.95)
        stability = random.uniform(0.35, 0.95)

    elif mode == "collapsed":
        non_red = random.uniform(0.20, 0.90)
        family = random.uniform(0.20, 0.90)
        entropy = random.uniform(0.10, 0.80)
        collapse = random.uniform(0.00, 0.12)
        stability = random.uniform(0.00, 0.30)

    elif mode == "noisy":
        non_red = random.uniform(0.35, 0.95)
        family = random.uniform(0.35, 0.95)
        entropy = random.uniform(0.85, 1.00)
        collapse = random.uniform(0.20, 0.80)
        stability = random.uniform(0.20, 0.80)

    elif mode == "sparse":
        non_red = random.uniform(0.70, 1.00)
        family = random.uniform(0.40, 0.90)
        entropy = random.uniform(0.10, 0.45)
        collapse = random.uniform(0.50, 1.00)
        stability = random.uniform(0.50, 1.00)

    elif mode == "contradictory":
        non_red = random.choice(
            [
                random.uniform(0.05, 0.30),
                random.uniform(0.75, 1.00),
            ]
        )
        family = random.choice(
            [
                random.uniform(0.05, 0.30),
                random.uniform(0.75, 1.00),
            ]
        )
        entropy = random.uniform(0.80, 1.00)
        collapse = random.choice(
            [
                random.uniform(0.05, 0.20),
                random.uniform(0.80, 1.00),
            ]
        )
        stability = random.choice(
            [
                random.uniform(0.05, 0.20),
                random.uniform(0.80, 1.00),
            ]
        )

    elif mode == "borderline":
        non_red = random.uniform(0.30, 0.45)
        family = random.uniform(0.30, 0.45)
        entropy = random.uniform(0.45, 0.95)
        collapse = random.uniform(0.10, 0.40)
        stability = random.uniform(0.10, 0.40)

    else:
        raise ValueError(f"unknown mode: {mode}")

    effective_count = compute_effective_count(
        raw_count=raw_count,
        non_redundancy=non_red,
        family_balance=family,
        relation_entropy=entropy,
        collapse_resistance=collapse,
        projection_stability=stability,
    )

    normalized_effective = safe_div(effective_count, raw_count)

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
        relation_entropy=entropy,
        divergence=divergence,
    )

    return {
        "system_id": system_id,
        "mode": mode,
        "raw_count": raw_count,
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


def proxy_expected_action(item):
    if (
        item["collapse_resistance"] < 0.10
        or item["projection_stability"] < 0.10
    ):
        return "COLLAPSE"

    if item["divergence"] >= 0.60:
        return "ESCALATE"

    if item["recoverability_score"] < 0.30:
        return "RETRY"

    if (
        item["family_balance"] < 0.35
        or item["non_redundancy"] < 0.35
    ):
        return "FLAG"

    if (
        item["normalized_effective"] < 0.05
        and item["recoverability_score"] >= 0.50
    ):
        return "FLAG"

    if item["relation_entropy"] > 0.90 and item["normalized_effective"] < 0.15:
        return "FLAG"

    if item["divergence"] >= 0.35:
        return "FLAG"

    return "PASS"


def mean_by_action(results, key):
    output = {}

    actions = sorted(
        set(item["gate_action"] for item in results)
    )

    for action in actions:
        values = [
            item[key]
            for item in results
            if item["gate_action"] == action
        ]

        output[action] = mean(values) if values else 0.0

    return output


def count_by_key(results, key):
    counts = {}

    for item in results:
        value = item[key]
        counts[value] = counts.get(value, 0) + 1

    return counts


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    random.seed(RANDOM_SEED)

    results = [
        generate_system(system_id=i)
        for i in range(SYSTEM_COUNT)
    ]

    for item in results:
        expected = proxy_expected_action(item)
        item["proxy_expected_action"] = expected
        item["proxy_match"] = item["gate_action"] == expected

    action_counts = count_by_key(results, "gate_action")
    mode_counts = count_by_key(results, "mode")

    proxy_match_count = sum(
        1 for item in results if item["proxy_match"]
    )

    proxy_mismatch_count = SYSTEM_COUNT - proxy_match_count

    false_pass_proxy_count = sum(
        1
        for item in results
        if item["gate_action"] == "PASS"
        and item["proxy_expected_action"] != "PASS"
    )

    false_collapse_proxy_count = sum(
        1
        for item in results
        if item["gate_action"] == "COLLAPSE"
        and item["proxy_expected_action"] != "COLLAPSE"
    )

    divergence_values = [
        item["divergence"]
        for item in results
    ]

    recoverability_values = [
        item["recoverability_score"]
        for item in results
    ]

    normalized_effective_values = [
        item["normalized_effective"]
        for item in results
    ]

    summary = {
        "system_count": SYSTEM_COUNT,
        "random_seed": RANDOM_SEED,
        "proxy_match_count": proxy_match_count,
        "proxy_mismatch_count": proxy_mismatch_count,
        "proxy_accuracy": safe_div(proxy_match_count, SYSTEM_COUNT),
        "false_pass_proxy_count": false_pass_proxy_count,
        "false_collapse_proxy_count": false_collapse_proxy_count,
        "gate_action_distribution": action_counts,
        "mode_distribution": mode_counts,
        "mean_divergence": mean(divergence_values),
        "max_divergence": max(divergence_values),
        "mean_recoverability_score": mean(recoverability_values),
        "mean_normalized_effective": mean(normalized_effective_values),
        "mean_divergence_by_action": mean_by_action(results, "divergence"),
        "mean_recoverability_by_action": mean_by_action(
            results,
            "recoverability_score",
        ),
        "mean_normalized_effective_by_action": mean_by_action(
            results,
            "normalized_effective",
        ),
    }

    status = (
        "PASS"
        if (
            summary["proxy_accuracy"] >= 0.95
            and false_pass_proxy_count == 0
            and false_collapse_proxy_count == 0
            and "PASS" in action_counts
            and "FLAG" in action_counts
            and "COLLAPSE" in action_counts
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
            "effective_observer_recoverability_gate_randomized_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Effective Observer Recoverability Gate Randomized v0"
    )
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)
    print("Random seed:", RANDOM_SEED)
    print("System count:", SYSTEM_COUNT)

    print()
    print("Summary")
    print("-" * 80)

    for key, value in summary.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in sorted(value.items()):
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

    print()
    print("Sample systems")
    print("-" * 80)

    for item in results[:20]:
        print(
            f"id={item['system_id']:<4} "
            f"mode={item['mode']:<14} "
            f"action={item['gate_action']:<9} "
            f"expected={item['proxy_expected_action']:<9} "
            f"match={str(item['proxy_match']):<5} "
            f"raw={item['raw_count']:<3} "
            f"eff={item['effective_count']:.6f} "
            f"norm_eff={item['normalized_effective']:.6f} "
            f"rec={item['recoverability_score']:.6f} "
            f"div={item['divergence']:.6f}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - randomized population validation produced coherent gate behavior."
        )
    else:
        print(
            "CHECK - randomized population validation exposed gate inconsistencies."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()