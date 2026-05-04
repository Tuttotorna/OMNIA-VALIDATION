import json
import os
import random
from statistics import mean

VERSION = "0.1.0"

RANDOM_SEED = 314159
SYSTEM_COUNT = 1500

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "effective_observer_recoverability_gate_external_proxy_v0.json",
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


def external_proxy_label(item):
    severe_collapse = (
        item["collapse_resistance"] < 0.08
        or item["projection_stability"] < 0.08
    )

    likely_collapse = (
        item["collapse_resistance"] < 0.12
        and item["projection_stability"] < 0.22
    )

    if severe_collapse or likely_collapse:
        return "COLLAPSE"

    if item["external_risk_score"] >= 0.72:
        return "ESCALATE"

    if item["recoverability_score"] < 0.28:
        return "RETRY"

    if item["external_risk_score"] >= 0.42:
        return "FLAG"

    if item["normalized_effective"] >= 0.45 and item["recoverability_score"] >= 0.72:
        return "PASS"

    return "FLAG"


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

    external_risk_score = clamp(
        0.28 * (1.0 - collapse)
        + 0.24 * (1.0 - stability)
        + 0.18 * (1.0 - non_red)
        + 0.14 * (1.0 - family)
        + 0.10 * entropy
        + 0.06 * divergence
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

    item = {
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
        "external_risk_score": external_risk_score,
        "gate_action": action,
    }

    item["external_proxy_label"] = external_proxy_label(item)
    item["external_proxy_match"] = (
        item["gate_action"] == item["external_proxy_label"]
    )

    return item


def count_by_key(results, key):
    counts = {}

    for item in results:
        value = item[key]
        counts[value] = counts.get(value, 0) + 1

    return counts


def mean_by_key(results, key):
    values = [item[key] for item in results]
    return mean(values) if values else 0.0


def mean_by_action(results, key):
    output = {}

    for action in sorted(set(item["gate_action"] for item in results)):
        values = [
            item[key]
            for item in results
            if item["gate_action"] == action
        ]

        output[action] = mean(values) if values else 0.0

    return output


def mean_by_profile(results, key):
    output = {}

    for profile in sorted(set(item["source_profile"] for item in results)):
        values = [
            item[key]
            for item in results
            if item["source_profile"] == profile
        ]

        output[profile] = mean(values) if values else 0.0

    return output


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    random.seed(RANDOM_SEED)

    results = [
        generate_external_style_system(system_id=i)
        for i in range(SYSTEM_COUNT)
    ]

    match_count = sum(
        1
        for item in results
        if item["external_proxy_match"]
    )

    mismatch_count = SYSTEM_COUNT - match_count

    false_pass_count = sum(
        1
        for item in results
        if item["gate_action"] == "PASS"
        and item["external_proxy_label"] != "PASS"
    )

    false_collapse_count = sum(
        1
        for item in results
        if item["gate_action"] == "COLLAPSE"
        and item["external_proxy_label"] != "COLLAPSE"
    )

    action_counts = count_by_key(results, "gate_action")
    label_counts = count_by_key(results, "external_proxy_label")
    profile_counts = count_by_key(results, "source_profile")

    summary = {
        "system_count": SYSTEM_COUNT,
        "random_seed": RANDOM_SEED,
        "match_count": match_count,
        "mismatch_count": mismatch_count,
        "proxy_alignment": safe_div(match_count, SYSTEM_COUNT),
        "false_pass_count": false_pass_count,
        "false_collapse_count": false_collapse_count,
        "gate_action_distribution": action_counts,
        "external_proxy_label_distribution": label_counts,
        "source_profile_distribution": profile_counts,
        "mean_external_risk_score": mean_by_key(results, "external_risk_score"),
        "mean_divergence": mean_by_key(results, "divergence"),
        "mean_recoverability_score": mean_by_key(
            results,
            "recoverability_score",
        ),
        "mean_normalized_effective": mean_by_key(
            results,
            "normalized_effective",
        ),
        "mean_external_risk_by_action": mean_by_action(
            results,
            "external_risk_score",
        ),
        "mean_divergence_by_action": mean_by_action(results, "divergence"),
        "mean_risk_by_profile": mean_by_profile(
            results,
            "external_risk_score",
        ),
    }

    status = (
        "PASS"
        if (
            summary["proxy_alignment"] >= 0.70
            and false_pass_count <= 5
            and false_collapse_count <= 10
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
            "effective_observer_recoverability_gate_external_proxy_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Effective Observer Recoverability Gate External Proxy v0"
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
            f"profile={item['source_profile']:<20} "
            f"gate={item['gate_action']:<9} "
            f"label={item['external_proxy_label']:<9} "
            f"match={str(item['external_proxy_match']):<5} "
            f"risk={item['external_risk_score']:.6f} "
            f"rec={item['recoverability_score']:.6f} "
            f"norm_eff={item['normalized_effective']:.6f} "
            f"div={item['divergence']:.6f}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - external-style proxy validation produced coherent gate behavior."
        )
    else:
        print(
            "CHECK - external-style proxy validation exposed gate mismatch."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()