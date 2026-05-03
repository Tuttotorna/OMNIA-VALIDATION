import json
import math
import os
import random
from statistics import mean

VERSION = "0.1.0"

RESULTS_PATH = (
    "results/correlation_analysis_effective_observer_stability_v0.json"
)

SEEDS = list(range(20))
SYSTEMS_PER_SEED = 500

FAMILY_COUNT = 8


def safe_log2(x):
    if x <= 0:
        return 0.0
    return math.log(x, 2)


def pearson(xs, ys):
    n = len(xs)

    if n == 0:
        return 0.0

    mean_x = mean(xs)
    mean_y = mean(ys)

    num = 0.0
    den_x = 0.0
    den_y = 0.0

    for x, y in zip(xs, ys):
        dx = x - mean_x
        dy = y - mean_y

        num += dx * dy
        den_x += dx * dx
        den_y += dy * dy

    den = math.sqrt(den_x * den_y)

    if den == 0:
        return 0.0

    return num / den


def rank(values):
    indexed = list(enumerate(values))
    indexed.sort(key=lambda x: x[1])

    ranks = [0.0] * len(values)

    for i, (idx, _) in enumerate(indexed):
        ranks[idx] = i + 1

    return ranks


def spearman(xs, ys):
    return pearson(rank(xs), rank(ys))


def entropy(values):
    total = sum(values)

    if total <= 0:
        return 0.0

    probs = [v / total for v in values if v > 0]

    return -sum(p * safe_log2(p) for p in probs)


def generate_system(rng, system_id):
    family_distribution = []

    for _ in range(FAMILY_COUNT):
        family_distribution.append(rng.randint(0, 8))

    raw_count = sum(family_distribution)

    if raw_count <= 0:
        family_distribution[rng.randint(0, FAMILY_COUNT - 1)] = 1
        raw_count = 1

    occupied_families = sum(
        1 for x in family_distribution if x > 0
    )

    family_balance = occupied_families / FAMILY_COUNT

    pair_count = raw_count * (raw_count - 1) / 2

    redundancy_pairs = 0.0

    for count in family_distribution:
        redundancy_pairs += count * (count - 1) / 2

    non_redundancy = 1.0

    if pair_count > 0:
        non_redundancy = 1.0 - (
            redundancy_pairs / pair_count
        )

    relation_entropy = entropy(family_distribution)
    max_entropy = safe_log2(FAMILY_COUNT)

    normalized_entropy = 0.0

    if max_entropy > 0:
        normalized_entropy = (
            relation_entropy / max_entropy
        )

    collapse_resistance = (
        0.45 * non_redundancy
        + 0.35 * family_balance
        + 0.20 * normalized_entropy
    )

    collapse_resistance = max(
        0.0,
        min(1.0, collapse_resistance),
    )

    effective_count = (
        raw_count
        * non_redundancy
        * family_balance
        * collapse_resistance
    )

    projection_stability = (
        0.40 * collapse_resistance
        + 0.35 * family_balance
        + 0.25 * non_redundancy
    )

    recoverability_score = (
        effective_count / (effective_count + 10.0)
    ) * projection_stability

    return {
        "system_id": system_id,
        "raw_count": raw_count,
        "effective_count": effective_count,
        "recoverability_score": recoverability_score,
    }


def run_seed(seed):
    rng = random.Random(seed)

    systems = []

    for i in range(SYSTEMS_PER_SEED):
        systems.append(
            generate_system(
                rng=rng,
                system_id=i,
            )
        )

    raws = [x["raw_count"] for x in systems]
    effectives = [x["effective_count"] for x in systems]
    recoveries = [
        x["recoverability_score"]
        for x in systems
    ]

    raw_pearson = pearson(raws, recoveries)
    effective_pearson = pearson(
        effectives,
        recoveries,
    )

    raw_spearman = spearman(raws, recoveries)
    effective_spearman = spearman(
        effectives,
        recoveries,
    )

    pearson_improvement = (
        effective_pearson - raw_pearson
    )

    spearman_improvement = (
        effective_spearman - raw_spearman
    )

    return {
        "seed": seed,
        "raw_pearson": raw_pearson,
        "effective_pearson": effective_pearson,
        "pearson_improvement": pearson_improvement,
        "raw_spearman": raw_spearman,
        "effective_spearman": effective_spearman,
        "spearman_improvement": spearman_improvement,
    }


def main():
    print("=" * 80)
    print(
        "OMNIA-VALIDATION — Correlation Analysis Stability v0"
    )
    print("=" * 80)
    print()

    seed_results = []

    for seed in SEEDS:
        result = run_seed(seed)
        seed_results.append(result)

        print(
            f"seed={seed:<2} "
            f"pearson_improvement="
            f"{result['pearson_improvement']:.12f} "
            f"spearman_improvement="
            f"{result['spearman_improvement']:.12f}"
        )

    pearson_improvements = [
        x["pearson_improvement"]
        for x in seed_results
    ]

    spearman_improvements = [
        x["spearman_improvement"]
        for x in seed_results
    ]

    positive_seed_count = sum(
        1
        for x in seed_results
        if (
            x["pearson_improvement"] > 0
            and x["spearman_improvement"] > 0
        )
    )

    negative_seed_count = (
        len(seed_results) - positive_seed_count
    )

    summary = {
        "seed_count": len(SEEDS),
        "systems_per_seed": SYSTEMS_PER_SEED,
        "mean_pearson_improvement": mean(
            pearson_improvements
        ),
        "min_pearson_improvement": min(
            pearson_improvements
        ),
        "max_pearson_improvement": max(
            pearson_improvements
        ),
        "mean_spearman_improvement": mean(
            spearman_improvements
        ),
        "min_spearman_improvement": min(
            spearman_improvements
        ),
        "max_spearman_improvement": max(
            spearman_improvements
        ),
        "positive_seed_count": positive_seed_count,
        "negative_seed_count": negative_seed_count,
    }

    status = "PASS"

    if positive_seed_count < len(SEEDS):
        status = "PARTIAL_PASS"

    result = {
        "status": status,
        "version": VERSION,
        "seed_results": seed_results,
        "summary": summary,
    }

    os.makedirs("results", exist_ok=True)

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key:<35}: {value:.12f}")
        else:
            print(f"{key:<35}: {value}")

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS — effective_count outperformed raw_count "
            "across all tested seeds."
        )
    else:
        print(
            "PARTIAL_PASS — some seeds did not preserve "
            "the improvement."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()