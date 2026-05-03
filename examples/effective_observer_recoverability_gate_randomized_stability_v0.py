Nome file:

examples/effective_observer_recoverability_gate_randomized_stability_v0.py

Contenuto completo:

import json
import os
import random
from statistics import mean

VERSION = "0.1.0"

SEED_COUNT = 20
SYSTEMS_PER_SEED = 1000

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "effective_observer_recoverability_gate_randomized_stability_v0.json",
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


def count_by_key(results, key):
    counts = {}

    for item in results:
        value = item[key]
        counts[value] = counts.get(value, 0) + 1

    return counts


def evaluate_seed(seed):
    random.seed(seed)

    results = [
        generate_system(system_id=i)
        for i in range(SYSTEMS_PER_SEED)
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

    proxy_mismatch_count = SYSTEMS_PER_SEED - proxy_match_count

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

    pass_count = action_counts.get("PASS", 0)
    flag_count = action_counts.get("FLAG", 0)
    retry_count = action_counts.get("RETRY", 0)
    escalate_count = action_counts.get("ESCALATE", 0)
    collapse_count = action_counts.get("COLLAPSE", 0)

    divergence_values = [
        item["divergence"]
        for item in results
    ]

    seed_summary = {
        "seed": seed,
        "system_count": SYSTEMS_PER_SEED,
        "proxy_match_count": proxy_match_count,
        "proxy_mismatch_count": proxy_mismatch_count,
        "proxy_accuracy": safe_div(proxy_match_count, SYSTEMS_PER_SEED),
        "false_pass_proxy_count": false_pass_proxy_count,
        "false_collapse_proxy_count": false_collapse_proxy_count,
        "pass_count": pass_count,
        "flag_count": flag_count,
        "retry_count": retry_count,
        "escalate_count": escalate_count,
        "collapse_count": collapse_count,
        "pass_rate": safe_div(pass_count, SYSTEMS_PER_SEED),
        "flag_rate": safe_div(flag_count, SYSTEMS_PER_SEED),
        "retry_rate": safe_div(retry_count, SYSTEMS_PER_SEED),
        "escalate_rate": safe_div(escalate_count, SYSTEMS_PER_SEED),
        "collapse_rate": safe_div(collapse_count, SYSTEMS_PER_SEED),
        "mean_divergence": mean(divergence_values),
        "max_divergence": max(divergence_values),
        "gate_action_distribution": action_counts,
        "mode_distribution": mode_counts,
    }

    seed_status = (
        "PASS"
        if (
            seed_summary["proxy_accuracy"] >= 0.95
            and false_pass_proxy_count == 0
            and false_collapse_proxy_count == 0
            and pass_count > 0
            and flag_count > 0
            and collapse_count > 0
        )
        else "CHECK"
    )

    return {
        "seed": seed,
        "status": seed_status,
        "summary": seed_summary,
        "sample_results": results[:20],
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    seeds = list(range(SEED_COUNT))

    seed_runs = [
        evaluate_seed(seed)
        for seed in seeds
    ]

    seed_summaries = [
        run["summary"]
        for run in seed_runs
    ]

    pass_seed_count = sum(
        1 for run in seed_runs if run["status"] == "PASS"
    )

    check_seed_count = SEED_COUNT - pass_seed_count

    proxy_accuracies = [
        item["proxy_accuracy"]
        for item in seed_summaries
    ]

    false_pass_counts = [
        item["false_pass_proxy_count"]
        for item in seed_summaries
    ]

    false_collapse_counts = [
        item["false_collapse_proxy_count"]
        for item in seed_summaries
    ]

    pass_rates = [
        item["pass_rate"]
        for item in seed_summaries
    ]

    flag_rates = [
        item["flag_rate"]
        for item in seed_summaries
    ]

    retry_rates = [
        item["retry_rate"]
        for item in seed_summaries
    ]

    escalate_rates = [
        item["escalate_rate"]
        for item in seed_summaries
    ]

    collapse_rates = [
        item["collapse_rate"]
        for item in seed_summaries
    ]

    summary = {
        "seed_count": SEED_COUNT,
        "systems_per_seed": SYSTEMS_PER_SEED,
        "total_system_count": SEED_COUNT * SYSTEMS_PER_SEED,
        "pass_seed_count": pass_seed_count,
        "check_seed_count": check_seed_count,
        "mean_proxy_accuracy": mean(proxy_accuracies),
        "min_proxy_accuracy": min(proxy_accuracies),
        "max_proxy_accuracy": max(proxy_accuracies),
        "mean_false_pass_proxy_count": mean(false_pass_counts),
        "max_false_pass_proxy_count": max(false_pass_counts),
        "mean_false_collapse_proxy_count": mean(false_collapse_counts),
        "max_false_collapse_proxy_count": max(false_collapse_counts),
        "mean_pass_rate": mean(pass_rates),
        "min_pass_rate": min(pass_rates),
        "max_pass_rate": max(pass_rates),
        "mean_flag_rate": mean(flag_rates),
        "mean_retry_rate": mean(retry_rates),
        "mean_escalate_rate": mean(escalate_rates),
        "mean_collapse_rate": mean(collapse_rates),
    }

    status = (
        "PASS"
        if (
            pass_seed_count == SEED_COUNT
            and summary["min_proxy_accuracy"] >= 0.95
            and summary["max_false_pass_proxy_count"] == 0
            and summary["max_false_collapse_proxy_count"] == 0
            and summary["mean_pass_rate"] > 0.0
            and summary["mean_flag_rate"] > 0.0
            and summary["mean_collapse_rate"] > 0.0
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "seed_runs": seed_runs,
        "reproduction_command": (
            "python examples/"
            "effective_observer_recoverability_gate_randomized_stability_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Effective Observer Recoverability Gate Randomized Stability v0"
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
    print("Seed summaries")
    print("-" * 80)

    for run in seed_runs:
        s = run["summary"]
        print(
            f"seed={run['seed']:<2} "
            f"status={run['status']:<5} "
            f"accuracy={s['proxy_accuracy']:.12f} "
            f"false_pass={s['false_pass_proxy_count']} "
            f"false_collapse={s['false_collapse_proxy_count']} "
            f"PASS={s['pass_count']} "
            f"FLAG={s['flag_count']} "
            f"RETRY={s['retry_count']} "
            f"ESCALATE={s['escalate_count']} "
            f"COLLAPSE={s['collapse_count']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - randomized gate behavior remained stable across seeds."
        )
    else:
        print(
            "CHECK - randomized gate behavior showed cross-seed instability."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()