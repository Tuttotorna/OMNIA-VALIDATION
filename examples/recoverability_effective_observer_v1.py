import json
import math
import os
import random
from collections import Counter
from itertools import combinations


VERSION = "0.1.0"

RESULTS_PATH = "results/recoverability_effective_observer_v1.json"

random.seed(42)


# =============================================================================
# OBSERVER GENERATION
# =============================================================================

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


def make_observer(family, idx):
    projection = [round(random.uniform(0.0, 1.0), 6) for _ in range(6)]

    return {
        "id": f"{family}_{idx}",
        "family": family,
        "projection": projection,
    }


def build_system(family_sizes):
    observers = []

    for family, size in family_sizes.items():
        for idx in range(size):
            observers.append(make_observer(family, idx))

    return observers


def duplicate_observers(observers, duplication_factor):
    duplicated = list(observers)

    for _ in range(duplication_factor):
        duplicated.extend(random.sample(observers, k=len(observers) // 2))

    return duplicated


def collapse_observers(observers):
    collapsed_projection = [0.5] * 6

    result = []

    for observer in observers:
        result.append(
            {
                "id": observer["id"],
                "family": observer["family"],
                "projection": collapsed_projection[:],
            }
        )

    return result


# =============================================================================
# DISTANCES
# =============================================================================

def projection_distance(a, b):
    pa = a["projection"]
    pb = b["projection"]

    squared = [(x - y) ** 2 for x, y in zip(pa, pb)]

    return math.sqrt(sum(squared))


def compute_pairwise_distances(observers):
    distances = []

    for a, b in combinations(observers, 2):
        distances.append(projection_distance(a, b))

    return distances


# =============================================================================
# STRUCTURAL METRICS
# =============================================================================

def compute_non_redundancy(observers):
    distances = compute_pairwise_distances(observers)

    if not distances:
        return 0.0

    threshold = 0.05

    unique_pairs = sum(1 for d in distances if d > threshold)

    return unique_pairs / len(distances)


def compute_family_balance(observers):
    families = [o["family"] for o in observers]

    counts = Counter(families)

    values = list(counts.values())

    if not values:
        return 0.0

    mean_value = sum(values) / len(values)

    imbalance = sum(abs(v - mean_value) for v in values)

    max_imbalance = len(observers)

    return max(0.0, 1.0 - (imbalance / max_imbalance))


def compute_relation_entropy(observers):
    distances = compute_pairwise_distances(observers)

    if not distances:
        return 0.0

    bins = [0, 0, 0]

    for d in distances:
        if d < 0.3:
            bins[0] += 1
        elif d < 0.7:
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

    return entropy / max_entropy if max_entropy > 0 else 0.0


def compute_collapse_resistance(observers):
    distances = compute_pairwise_distances(observers)

    if not distances:
        return 0.0

    mean_distance = sum(distances) / len(distances)

    return min(1.0, mean_distance)


def compute_projection_stability(observers):
    distances = compute_pairwise_distances(observers)

    if not distances:
        return 0.0

    variance = sum(
        (d - (sum(distances) / len(distances))) ** 2
        for d in distances
    ) / len(distances)

    stability = 1.0 / (1.0 + variance)

    return stability


# =============================================================================
# EFFECTIVE OBSERVER COUNT
# =============================================================================

def compute_effective_observer_count(
    observers,
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
):
    raw_count = len(observers)

    effective = (
        raw_count
        * non_redundancy
        * family_balance
        * relation_entropy
        * collapse_resistance
    )

    return effective


# =============================================================================
# RECOVERABILITY V1
# =============================================================================

def compute_recoverability_v1(
    projection_stability,
    non_redundancy,
    family_balance,
    collapse_resistance,
):
    return (
        projection_stability
        * non_redundancy
        * family_balance
        * collapse_resistance
    )


# =============================================================================
# SYSTEM ANALYSIS
# =============================================================================

def analyze_system(name, observers):
    non_redundancy = compute_non_redundancy(observers)

    family_balance = compute_family_balance(observers)

    relation_entropy = compute_relation_entropy(observers)

    collapse_resistance = compute_collapse_resistance(observers)

    projection_stability = compute_projection_stability(observers)

    effective_count = compute_effective_observer_count(
        observers,
        non_redundancy,
        family_balance,
        relation_entropy,
        collapse_resistance,
    )

    recoverability = compute_recoverability_v1(
        projection_stability,
        non_redundancy,
        family_balance,
        collapse_resistance,
    )

    return {
        "system": name,
        "raw_count": len(observers),
        "effective_count": effective_count,
        "recoverability_score": recoverability,
        "projection_stability": projection_stability,
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

    base_system = build_system(
        {
            "spatial": 2,
            "temporal": 2,
            "causal": 2,
            "symbolic": 2,
            "entropy": 2,
            "topological": 2,
        }
    )

    duplicate_system = duplicate_observers(base_system, duplication_factor=4)

    balanced_system = build_system(
        {
            family: 5
            for family in FAMILIES
        }
    )

    collapsed_system = collapse_observers(
        build_system(
            {
                family: 4
                for family in FAMILIES[:6]
            }
        )
    )

    systems = [
        ("base_system", base_system),
        ("duplicate_system", duplicate_system),
        ("balanced_system", balanced_system),
        ("collapsed_system", collapsed_system),
    ]

    results = []

    print("=" * 80)
    print("OMNIA-VALIDATION — Recoverability vs Effective Observer Count v1")
    print("=" * 80)
    print()

    for name, observers in systems:
        result = analyze_system(name, observers)

        results.append(result)

        print(name)
        print("-" * 80)

        for key, value in result.items():
            if key == "system":
                continue

            if isinstance(value, float):
                print(f"{key:22}: {value:.12f}")
            else:
                print(f"{key:22}: {value}")

        print()

    ranked = sorted(
        results,
        key=lambda x: x["recoverability_score"],
        reverse=True,
    )

    print("=" * 80)
    print("RANKING BY RECOVERABILITY")
    print("=" * 80)

    for idx, item in enumerate(ranked, start=1):
        print(
            f"{idx}. "
            f"{item['system']} "
            f"(recoverability={item['recoverability_score']:.12f}, "
            f"effective={item['effective_count']:.12f})"
        )

    payload = {
        "status": "PASS",
        "version": VERSION,
        "results": results,
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()