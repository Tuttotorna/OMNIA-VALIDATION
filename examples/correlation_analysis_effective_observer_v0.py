#!/usr/bin/env python3

import json
import math
import os
import random
from collections import Counter
from itertools import combinations


VERSION = "0.1.0"
RESULTS_PATH = "results/correlation_analysis_effective_observer_v0.json"

RANDOM_SEED = 42
SYSTEM_COUNT = 500

random.seed(RANDOM_SEED)


FAMILIES = [
    "spatial",
    "temporal",
    "causal",
    "symbolic",
    "entropy",
    "topological",
    "relational",
    "spectral",
]


# =============================================================================
# BASIC HELPERS
# =============================================================================

def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def mean(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


def pearson_correlation(xs, ys):
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0

    mx = mean(xs)
    my = mean(ys)

    numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys))

    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))

    if dx == 0.0 or dy == 0.0:
        return 0.0

    return numerator / (dx * dy)


def rank_values(values):
    indexed = list(enumerate(values))
    indexed.sort(key=lambda x: x[1])

    ranks = [0.0] * len(values)

    i = 0

    while i < len(indexed):
        j = i

        while j + 1 < len(indexed) and indexed[j + 1][1] == indexed[i][1]:
            j += 1

        avg_rank = (i + j + 2) / 2.0

        for k in range(i, j + 1):
            ranks[indexed[k][0]] = avg_rank

        i = j + 1

    return ranks


def spearman_correlation(xs, ys):
    return pearson_correlation(rank_values(xs), rank_values(ys))


# =============================================================================
# OBSERVER GENERATION
# =============================================================================

def make_projection(family_strength, noise_level):
    return [
        round(
            clamp(
                family_strength + random.uniform(-noise_level, noise_level)
            ),
            6,
        )
        for _ in range(6)
    ]


def make_observer(family, idx, family_strength, noise_level):
    return {
        "id": f"{family}_{idx}_{random.randint(0, 999999)}",
        "family": family,
        "projection": make_projection(family_strength, noise_level),
    }


def build_random_system(system_id):
    family_count = random.randint(1, len(FAMILIES))

    selected_families = random.sample(FAMILIES, family_count)

    observers = []

    collapse_probability = random.random()

    force_collapse = collapse_probability < 0.08
    force_duplicate = 0.08 <= collapse_probability < 0.20
    force_imbalance = 0.20 <= collapse_probability < 0.35

    if force_collapse:
        shared_projection = [0.5] * 6

        raw_count = random.randint(8, 50)

        for i in range(raw_count):
            family = random.choice(selected_families)

            observers.append(
                {
                    "id": f"collapsed_{system_id}_{i}",
                    "family": family,
                    "projection": shared_projection[:],
                }
            )

        return observers

    if force_imbalance:
        dominant_family = random.choice(selected_families)

        for family in selected_families:
            if family == dominant_family:
                size = random.randint(12, 35)
            else:
                size = random.randint(1, 3)

            family_strength = random.uniform(0.25, 0.95)
            noise_level = random.uniform(0.02, 0.22)

            for i in range(size):
                observers.append(
                    make_observer(
                        family,
                        i,
                        family_strength,
                        noise_level,
                    )
                )

        return observers

    for family in selected_families:
        size = random.randint(1, 8)

        family_strength = random.uniform(0.25, 0.95)
        noise_level = random.uniform(0.02, 0.28)

        for i in range(size):
            observers.append(
                make_observer(
                    family,
                    i,
                    family_strength,
                    noise_level,
                )
            )

    if force_duplicate and observers:
        duplicate_count = random.randint(4, 20)

        for i in range(duplicate_count):
            source = random.choice(observers)

            observers.append(
                {
                    "id": source["id"],
                    "family": source["family"],
                    "projection": source["projection"][:],
                }
            )

    return observers


# =============================================================================
# DISTANCE AND STRUCTURAL METRICS
# =============================================================================

def projection_distance(a, b):
    pa = a["projection"]
    pb = b["projection"]

    squared = [(x - y) ** 2 for x, y in zip(pa, pb)]

    return math.sqrt(sum(squared)) / math.sqrt(len(pa))


def compute_pairwise_distances(observers):
    distances = []

    for a, b in combinations(observers, 2):
        distances.append(projection_distance(a, b))

    return distances


def compute_non_redundancy(observers):
    distances = compute_pairwise_distances(observers)

    if not distances:
        return 0.0

    threshold = 0.03

    non_redundant_pairs = sum(1 for d in distances if d > threshold)

    return non_redundant_pairs / len(distances)


def compute_family_balance(observers):
    if not observers:
        return 0.0

    counts = Counter(o["family"] for o in observers)

    if len(counts) <= 1:
        return 0.0

    total = len(observers)

    entropy = 0.0

    for count in counts.values():
        p = count / total
        entropy -= p * math.log(p)

    max_entropy = math.log(len(counts))

    if max_entropy == 0.0:
        return 0.0

    return entropy / max_entropy


def compute_relation_entropy(observers):
    distances = compute_pairwise_distances(observers)

    if not distances:
        return 0.0

    bins = [0, 0, 0]

    for d in distances:
        if d < 0.12:
            bins[0] += 1
        elif d < 0.32:
            bins[1] += 1
        else:
            bins[2] += 1

    total = sum(bins)

    entropy = 0.0

    for value in bins:
        if value == 0:
            continue

        p = value / total
        entropy -= p * math.log(p)

    max_entropy = math.log(len(bins))

    if max_entropy == 0.0:
        return 0.0

    return entropy / max_entropy


def compute_collapse_resistance(observers):
    distances = compute_pairwise_distances(observers)

    if not distances:
        return 0.0

    return clamp(mean(distances) / 0.55)


def compute_projection_stability(observers):
    distances = compute_pairwise_distances(observers)

    if not distances:
        return 0.0

    avg = mean(distances)

    variance = mean([(d - avg) ** 2 for d in distances])

    return 1.0 / (1.0 + variance)


def compute_projection_coverage(observers):
    if not observers:
        return 0.0

    families_present = len(set(o["family"] for o in observers))

    return families_present / len(FAMILIES)


# =============================================================================
# EFFECTIVE COUNT AND RECOVERABILITY
# =============================================================================

def compute_effective_observer_count(
    raw_count,
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
):
    return (
        raw_count
        * non_redundancy
        * family_balance
        * relation_entropy
        * collapse_resistance
    )


def compute_recoverability(
    projection_stability,
    projection_coverage,
    non_redundancy,
    family_balance,
    collapse_resistance,
):
    return (
        projection_stability
        * projection_coverage
        * non_redundancy
        * family_balance
        * collapse_resistance
    )


def analyze_system(system_id, observers):
    raw_count = len(observers)

    non_redundancy = compute_non_redundancy(observers)
    family_balance = compute_family_balance(observers)
    relation_entropy = compute_relation_entropy(observers)
    collapse_resistance = compute_collapse_resistance(observers)
    projection_stability = compute_projection_stability(observers)
    projection_coverage = compute_projection_coverage(observers)

    effective_count = compute_effective_observer_count(
        raw_count,
        non_redundancy,
        family_balance,
        relation_entropy,
        collapse_resistance,
    )

    recoverability = compute_recoverability(
        projection_stability,
        projection_coverage,
        non_redundancy,
        family_balance,
        collapse_resistance,
    )

    return {
        "system_id": system_id,
        "raw_count": raw_count,
        "family_count": len(set(o["family"] for o in observers)),
        "effective_count": effective_count,
        "recoverability_score": recoverability,
        "projection_stability": projection_stability,
        "projection_coverage": projection_coverage,
        "non_redundancy": non_redundancy,
        "family_balance": family_balance,
        "relation_entropy": relation_entropy,
        "collapse_resistance": collapse_resistance,
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    os.makedirs("results", exist_ok=True)

    print("=" * 80)
    print("OMNIA-VALIDATION — Correlation Analysis: Effective Observer Count v0")
    print("=" * 80)
    print()

    results = []

    for system_id in range(SYSTEM_COUNT):
        observers = build_random_system(system_id)
        results.append(analyze_system(system_id, observers))

    raw_counts = [r["raw_count"] for r in results]
    effective_counts = [r["effective_count"] for r in results]
    recoverability_scores = [r["recoverability_score"] for r in results]

    raw_pearson = pearson_correlation(raw_counts, recoverability_scores)
    effective_pearson = pearson_correlation(effective_counts, recoverability_scores)

    raw_spearman = spearman_correlation(raw_counts, recoverability_scores)
    effective_spearman = spearman_correlation(effective_counts, recoverability_scores)

    improvement_pearson = effective_pearson - raw_pearson
    improvement_spearman = effective_spearman - raw_spearman

    status = "PASS" if (
        effective_pearson > raw_pearson
        and effective_spearman > raw_spearman
    ) else "NEGATIVE_RESULT"

    summary = {
        "system_count": SYSTEM_COUNT,
        "raw_pearson_recoverability": raw_pearson,
        "effective_pearson_recoverability": effective_pearson,
        "raw_spearman_recoverability": raw_spearman,
        "effective_spearman_recoverability": effective_spearman,
        "pearson_improvement": improvement_pearson,
        "spearman_improvement": improvement_spearman,
        "mean_raw_count": mean(raw_counts),
        "mean_effective_count": mean(effective_counts),
        "mean_recoverability": mean(recoverability_scores),
    }

    payload = {
        "status": status,
        "version": VERSION,
        "random_seed": RANDOM_SEED,
        "summary": summary,
        "results": results,
        "reproduction_command": "python examples/correlation_analysis_effective_observer_v0.py",
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("Status:", status)
    print("Version:", VERSION)
    print("System count:", SYSTEM_COUNT)
    print()

    print("Correlation summary")
    print("-" * 80)
    print(f"raw_count       Pearson vs recoverability: {raw_pearson:.12f}")
    print(f"effective_count Pearson vs recoverability: {effective_pearson:.12f}")
    print(f"Pearson improvement:                    {improvement_pearson:.12f}")
    print()
    print(f"raw_count       Spearman vs recoverability: {raw_spearman:.12f}")
    print(f"effective_count Spearman vs recoverability: {effective_spearman:.12f}")
    print(f"Spearman improvement:                     {improvement_spearman:.12f}")
    print()

    print("Mean values")
    print("-" * 80)
    print(f"mean_raw_count:        {summary['mean_raw_count']:.12f}")
    print(f"mean_effective_count:  {summary['mean_effective_count']:.12f}")
    print(f"mean_recoverability:   {summary['mean_recoverability']:.12f}")
    print()

    print("Top 10 by recoverability")
    print("-" * 80)

    ranked = sorted(
        results,
        key=lambda x: x["recoverability_score"],
        reverse=True,
    )

    for item in ranked[:10]:
        print(
            f"system={item['system_id']:<4} "
            f"raw={item['raw_count']:<3} "
            f"families={item['family_count']:<2} "
            f"effective={item['effective_count']:.6f} "
            f"recoverability={item['recoverability_score']:.6f}"
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()