import json
import os
import random
from statistics import mean

VERSION = "0.1.0"

SEED_COUNT = 20
SYSTEMS_PER_SEED = 1500

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "cross_gate_disagreement_stability_v0.json",
)


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def safe_div(a, b):
    if b == 0:
        return 0.0
    return a / b


def beta_like(a, b):
    return random.betavariate(a, b)


def jitter(x, amount=0.035):
    return clamp(x + random.uniform(-amount, amount))


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


def effective_signal_gate(normalized_effective):
    if normalized_effective >= 0.45:
        return "PASS"

    if normalized_effective >= 0.20:
        return "FLAG"

    if normalized_effective >= 0.05:
        return "RETRY"

    return "COLLAPSE"


def recoverability_gate(recoverability_score):
    if recoverability_score >= 0.72:
        return "PASS"

    if recoverability_score >= 0.45:
        return "FLAG"

    if recoverability_score >= 0.30:
        return "RETRY"

    return "COLLAPSE"


def divergence_gate(divergence):
    if divergence >= 0.60:
        return "ESCALATE"

    if divergence >= 0.35:
        return "FLAG"

    if divergence >= 0.20:
        return "RETRY"

    return "PASS"


def collapse_gate(collapse_resistance):
    if collapse_resistance < 0.10:
        return "COLLAPSE"

    if collapse_resistance < 0.20:
        return "FLAG"

    if collapse_resistance < 0.45:
        return "RETRY"

    return "PASS"


def projection_gate(projection_stability):
    if projection_stability < 0.10:
        return "COLLAPSE"

    if projection_stability < 0.20:
        return "FLAG"

    if projection_stability < 0.45:
        return "RETRY"

    return "PASS"


def action_severity(action):
    severity = {
        "PASS": 0,
        "RETRY": 1,
        "FLAG": 2,
        "ESCALATE": 3,
        "COLLAPSE": 4,
    }

    return severity[action]


def severity_to_action(severity_value):
    if severity_value >= 3.50:
        return "COLLAPSE"

    if severity_value >= 2.50:
        return "ESCALATE"

    if severity_value >= 1.50:
        return "FLAG"

    if severity_value >= 0.50:
        return "RETRY"

    return "PASS"


def structural_arbitration(signal_actions):
    severities = [
        action_severity(action)
        for action in signal_actions.values()
    ]

    max_severity = max(severities)
    min_severity = min(severities)
    mean_severity = mean(severities)

    spread = max_severity - min_severity

    collapse_votes = sum(
        1 for action in signal_actions.values()
        if action == "COLLAPSE"
    )

    escalate_votes = sum(
        1 for action in signal_actions.values()
        if action == "ESCALATE"
    )

    pass_votes = sum(
        1 for action in signal_actions.values()
        if action == "PASS"
    )

    if collapse_votes >= 2:
        return "COLLAPSE"

    if collapse_votes == 1 and spread >= 3:
        return "ESCALATE"

    if escalate_votes >= 1 and spread >= 2:
        return "ESCALATE"

    if spread >= 3:
        return "ESCALATE"

    if pass_votes >= 3 and max_severity <= 2:
        return "PASS"

    return severity_to_action(mean_severity)


def compute_disagreement(signal_actions):
    severities = [
        action_severity(action)
        for action in signal_actions.values()
    ]

    unique_actions = len(set(signal_actions.values()))
    spread = max(severities) - min(severities)
    mean_severity = mean(severities)

    variance = mean(
        (value - mean_severity) ** 2
        for value in severities
    )

    return {
        "unique_action_count": unique_actions,
        "severity_spread": spread,
        "severity_variance": variance,
        "mean_severity": mean_severity,
    }


def generate_external_style_system(system_id):
    raw_count = random.randint(3, 140)

    source_profile = random.choice(
        [
            "external_clean",
            "external_noisy",
            "external_shifted",
            "external_sparse",
            "external_redundant",
            "external_fragile",
            "external_mixed",
            "external_outlier",
        ]
    )

    if source_profile == "external_clean":
        non_red = beta_like(8, 2)
        family = beta_like(7, 2)
        entropy = beta_like(3, 4)
        collapse = beta_like(9, 2)
        stability = beta_like(9, 2)

    elif source_profile == "external_noisy":
        non_red = beta_like(4, 3)
        family = beta_like(4, 3)
        entropy = beta_like(9, 1.5)
        collapse = beta_like(4, 4)
        stability = beta_like(4, 4)

    elif source_profile == "external_shifted":
        non_red = beta_like(6, 3)
        family = beta_like(3, 6)
        entropy = beta_like(5, 3)
        collapse = beta_like(5, 4)
        stability = beta_like(3, 5)

    elif source_profile == "external_sparse":
        non_red = beta_like(8, 2)
        family = beta_like(4, 5)
        entropy = beta_like(2, 6)
        collapse = beta_like(7, 3)
        stability = beta_like(7, 3)

    elif source_profile == "external_redundant":
        non_red = beta_like(1.8, 8)
        family = beta_like(4, 4)
        entropy = beta_like(6, 2)
        collapse = beta_like(5, 4)
        stability = beta_like(5, 4)

    elif source_profile == "external_fragile":
        non_red = beta_like(4, 4)
        family = beta_like(4, 4)
        entropy = beta_like(4, 4)
        collapse = beta_like(1.2, 8)
        stability = beta_like(2, 7)

    elif source_profile == "external_mixed":
        non_red = beta_like(3, 3)
        family = beta_like(3, 3)
        entropy = beta_like(3, 3)
        collapse = beta_like(3, 3)
        stability = beta_like(3, 3)

    elif source_profile == "external_outlier":
        non_red = random.choice(
            [
                beta_like(1.2, 7),
                beta_like(9, 1.5),
            ]
        )
        family = random.choice(
            [
                beta_like(1.2, 7),
                beta_like(9, 1.5),
            ]
        )
        entropy = random.choice(
            [
                beta_like(1.2, 7),
                beta_like(9, 1.5),
            ]
        )
        collapse = random.choice(
            [
                beta_like(1.2, 7),
                beta_like(9, 1.5),
            ]
        )
        stability = random.choice(
            [
                beta_like(1.2, 7),
                beta_like(9, 1.5),
            ]
        )

    else:
        raise ValueError(f"unknown profile: {source_profile}")

    non_red = jitter(non_red)
    family = jitter(family)
    entropy = jitter(entropy)
    collapse = jitter(collapse)
    stability = jitter(stability)

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

    signal_actions = {
        "effective_signal_gate": effective_signal_gate(normalized_effective),
        "recoverability_gate": recoverability_gate(recoverability_score),
        "divergence_gate": divergence_gate(divergence),
        "collapse_gate": collapse_gate(collapse),
        "projection_gate": projection_gate(stability),
    }

    disagreement = compute_disagreement(signal_actions)

    arbitration_action = structural_arbitration(signal_actions)

    return {
        "system_id": system_id,
        "source_profile": source_profile,
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
        "signal_actions": signal_actions,
        "arbitration_action": arbitration_action,
        "unique_action_count": disagreement["unique_action_count"],
        "severity_spread": disagreement["severity_spread"],
        "severity_variance": disagreement["severity_variance"],
        "mean_severity": disagreement["mean_severity"],
    }


def count_by_key(results, key):
    counts = {}

    for item in results:
        value = item[key]
        counts[value] = counts.get(value, 0) + 1

    return counts


def safe_count(counts, key):
    return counts.get(key, 0)


def evaluate_seed(seed):
    random.seed(seed)

    results = [
        generate_external_style_system(system_id=i)
        for i in range(SYSTEMS_PER_SEED)
    ]

    arbitration_counts = count_by_key(results, "arbitration_action")
    profile_counts = count_by_key(results, "source_profile")

    high_disagreement_count = sum(
        1
        for item in results
        if item["severity_spread"] >= 3
    )

    medium_disagreement_count = sum(
        1
        for item in results
        if item["severity_spread"] == 2
    )

    low_disagreement_count = sum(
        1
        for item in results
        if item["severity_spread"] <= 1
    )

    contradiction_count = sum(
        1
        for item in results
        if "PASS" in item["signal_actions"].values()
        and "COLLAPSE" in item["signal_actions"].values()
    )

    unanimous_count = sum(
        1
        for item in results
        if item["unique_action_count"] == 1
    )

    mean_unique_action_count = mean(
        item["unique_action_count"]
        for item in results
    )

    mean_severity_spread = mean(
        item["severity_spread"]
        for item in results
    )

    mean_severity_variance = mean(
        item["severity_variance"]
        for item in results
    )

    seed_summary = {
        "seed": seed,
        "system_count": SYSTEMS_PER_SEED,
        "arbitration_action_distribution": arbitration_counts,
        "source_profile_distribution": profile_counts,
        "high_disagreement_count": high_disagreement_count,
        "medium_disagreement_count": medium_disagreement_count,
        "low_disagreement_count": low_disagreement_count,
        "contradiction_count": contradiction_count,
        "unanimous_count": unanimous_count,
        "high_disagreement_rate": safe_div(
            high_disagreement_count,
            SYSTEMS_PER_SEED,
        ),
        "medium_disagreement_rate": safe_div(
            medium_disagreement_count,
            SYSTEMS_PER_SEED,
        ),
        "low_disagreement_rate": safe_div(
            low_disagreement_count,
            SYSTEMS_PER_SEED,
        ),
        "contradiction_rate": safe_div(
            contradiction_count,
            SYSTEMS_PER_SEED,
        ),
        "unanimous_rate": safe_div(
            unanimous_count,
            SYSTEMS_PER_SEED,
        ),
        "mean_unique_action_count": mean_unique_action_count,
        "mean_severity_spread": mean_severity_spread,
        "mean_severity_variance": mean_severity_variance,
        "pass_count": safe_count(arbitration_counts, "PASS"),
        "retry_count": safe_count(arbitration_counts, "RETRY"),
        "flag_count": safe_count(arbitration_counts, "FLAG"),
        "escalate_count": safe_count(arbitration_counts, "ESCALATE"),
        "collapse_count": safe_count(arbitration_counts, "COLLAPSE"),
        "pass_rate": safe_div(
            safe_count(arbitration_counts, "PASS"),
            SYSTEMS_PER_SEED,
        ),
        "retry_rate": safe_div(
            safe_count(arbitration_counts, "RETRY"),
            SYSTEMS_PER_SEED,
        ),
        "flag_rate": safe_div(
            safe_count(arbitration_counts, "FLAG"),
            SYSTEMS_PER_SEED,
        ),
        "escalate_rate": safe_div(
            safe_count(arbitration_counts, "ESCALATE"),
            SYSTEMS_PER_SEED,
        ),
        "collapse_rate": safe_div(
            safe_count(arbitration_counts, "COLLAPSE"),
            SYSTEMS_PER_SEED,
        ),
    }

    seed_status = (
        "PASS"
        if (
            high_disagreement_count > 0
            and contradiction_count > 0
            and safe_count(arbitration_counts, "ESCALATE") > 0
            and safe_count(arbitration_counts, "COLLAPSE") > 0
            and safe_count(arbitration_counts, "PASS") > 0
            and mean_severity_spread >= 2.0
        )
        else "CHECK"
    )

    return {
        "seed": seed,
        "status": seed_status,
        "summary": seed_summary,
        "sample_results": results[:10],
    }


def summarize_numeric(seed_summaries, key):
    values = [
        item[key]
        for item in seed_summaries
    ]

    return {
        "mean": mean(values),
        "min": min(values),
        "max": max(values),
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

    summary = {
        "seed_count": SEED_COUNT,
        "systems_per_seed": SYSTEMS_PER_SEED,
        "total_system_count": SEED_COUNT * SYSTEMS_PER_SEED,
        "pass_seed_count": pass_seed_count,
        "check_seed_count": check_seed_count,
        "high_disagreement_count": summarize_numeric(
            seed_summaries,
            "high_disagreement_count",
        ),
        "medium_disagreement_count": summarize_numeric(
            seed_summaries,
            "medium_disagreement_count",
        ),
        "low_disagreement_count": summarize_numeric(
            seed_summaries,
            "low_disagreement_count",
        ),
        "contradiction_count": summarize_numeric(
            seed_summaries,
            "contradiction_count",
        ),
        "unanimous_count": summarize_numeric(
            seed_summaries,
            "unanimous_count",
        ),
        "mean_unique_action_count": summarize_numeric(
            seed_summaries,
            "mean_unique_action_count",
        ),
        "mean_severity_spread": summarize_numeric(
            seed_summaries,
            "mean_severity_spread",
        ),
        "mean_severity_variance": summarize_numeric(
            seed_summaries,
            "mean_severity_variance",
        ),
        "pass_rate": summarize_numeric(seed_summaries, "pass_rate"),
        "retry_rate": summarize_numeric(seed_summaries, "retry_rate"),
        "flag_rate": summarize_numeric(seed_summaries, "flag_rate"),
        "escalate_rate": summarize_numeric(
            seed_summaries,
            "escalate_rate",
        ),
        "collapse_rate": summarize_numeric(
            seed_summaries,
            "collapse_rate",
        ),
    }

    status = (
        "PASS"
        if (
            pass_seed_count == SEED_COUNT
            and summary["high_disagreement_count"]["min"] > 0
            and summary["contradiction_count"]["min"] > 0
            and summary["mean_severity_spread"]["min"] >= 2.0
            and summary["escalate_rate"]["mean"] > 0.0
            and summary["collapse_rate"]["mean"] > 0.0
            and summary["pass_rate"]["mean"] > 0.0
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "seed_runs": seed_runs,
        "reproduction_command": (
            "python examples/cross_gate_disagreement_stability_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION - Cross-Gate Disagreement Stability v0")
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)
    print("Seed count:", SEED_COUNT)
    print("Systems per seed:", SYSTEMS_PER_SEED)

    print()
    print("Summary")
    print("-" * 80)

    for key, value in summary.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

    print()
    print("Seed summaries")
    print("-" * 80)

    for run in seed_runs:
        s = run["summary"]
        print(
            f"seed={run['seed']:<2} "
            f"status={run['status']:<5} "
            f"high={s['high_disagreement_count']} "
            f"contradiction={s['contradiction_count']} "
            f"unanimous={s['unanimous_count']} "
            f"mean_spread={s['mean_severity_spread']:.12f} "
            f"PASS={s['pass_count']} "
            f"RETRY={s['retry_count']} "
            f"FLAG={s['flag_count']} "
            f"ESCALATE={s['escalate_count']} "
            f"COLLAPSE={s['collapse_count']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - cross-gate disagreement remained stable across seeds."
        )
    else:
        print(
            "CHECK - cross-gate disagreement showed cross-seed instability."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()