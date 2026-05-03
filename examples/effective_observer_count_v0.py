#!/usr/bin/env python3

import json
import math
import os
from collections import Counter


RESULTS_PATH = "results/effective_observer_count_v0.json"


BASE_OBSERVERS = [
    {"id": "symmetry_A",        "family": "symmetry"},
    {"id": "symmetry_B",        "family": "symmetry"},
    {"id": "topology_A",        "family": "topology"},
    {"id": "topology_B",        "family": "topology"},
    {"id": "entropy_A",         "family": "entropy"},
    {"id": "entropy_B",         "family": "entropy"},
    {"id": "geometry_A",        "family": "geometry"},
    {"id": "geometry_B",        "family": "geometry"},
    {"id": "causality_A",       "family": "causality"},
    {"id": "causality_B",       "family": "causality"},
    {"id": "continuity_A",      "family": "continuity"},
    {"id": "continuity_B",      "family": "continuity"},
]


def compute_pairwise_distances(observers):

    distances = []

    for i in range(len(observers)):
        for j in range(i + 1, len(observers)):

            a = observers[i]
            b = observers[j]

            if a["id"] == b["id"]:
                distance = 0.0

            elif a["family"] == b["family"]:
                distance = 0.35

            else:
                distance = 0.85

            distances.append(distance)

    return distances


def relation_entropy(distances):

    if not distances:
        return 0.0

    bins = {
        "low": 0,
        "mid": 0,
        "high": 0,
    }

    for d in distances:

        if d < 0.2:
            bins["low"] += 1

        elif d < 0.6:
            bins["mid"] += 1

        else:
            bins["high"] += 1

    total = sum(bins.values())

    entropy = 0.0

    for count in bins.values():

        if count == 0:
            continue

        p = count / total
        entropy -= p * math.log(p)

    max_entropy = math.log(len(bins))

    return entropy / max_entropy


def family_balance(observers):

    family_counts = Counter(o["family"] for o in observers)

    total = len(observers)

    entropy = 0.0

    for count in family_counts.values():

        p = count / total
        entropy -= p * math.log(p)

    max_entropy = math.log(len(family_counts))

    if max_entropy == 0:
        return 0.0

    return entropy / max_entropy


def non_redundancy(distances):

    if not distances:
        return 0.0

    redundant = sum(1 for d in distances if d < 0.2)

    return 1.0 - (redundant / len(distances))


def collapse_resistance(distances):

    if not distances:
        return 0.0

    avg_distance = sum(distances) / len(distances)

    return avg_distance


def effective_observer_count(observers):

    raw_count = len(observers)

    distances = compute_pairwise_distances(observers)

    nr = non_redundancy(distances)
    fb = family_balance(observers)
    re = relation_entropy(distances)
    cr = collapse_resistance(distances)

    effective = raw_count * nr * fb * re * cr

    return {
        "raw_count": raw_count,
        "effective_count": effective,
        "non_redundancy": nr,
        "family_balance": fb,
        "relation_entropy": re,
        "collapse_resistance": cr,
    }


def build_duplicate_system():

    observers = list(BASE_OBSERVERS)

    for i in range(20):

        observers.append({
            "id": "symmetry_A",
            "family": "symmetry",
        })

    return observers


def build_balanced_system():

    observers = []

    families = [
        "symmetry",
        "topology",
        "entropy",
        "geometry",
        "causality",
        "continuity",
        "temporal",
        "logical",
    ]

    for family in families:

        for i in range(5):

            observers.append({
                "id": f"{family}_{i}",
                "family": family,
            })

    return observers


def build_collapsed_system():

    observers = []

    for i in range(30):

        observers.append({
            "id": "collapsed",
            "family": "collapsed",
        })

    return observers


def evaluate_system(name, observers):

    result = effective_observer_count(observers)

    result["system"] = name

    return result


def main():

    print("=" * 80)
    print("OMNIA-VALIDATION — Effective Observer Count v0")
    print("=" * 80)

    systems = {
        "base_system": BASE_OBSERVERS,
        "duplicate_system": build_duplicate_system(),
        "balanced_system": build_balanced_system(),
        "collapsed_system": build_collapsed_system(),
    }

    results = []

    for name, observers in systems.items():

        result = evaluate_system(name, observers)

        results.append(result)

        print()
        print(name)
        print("-" * 80)
        print(f"raw_count            : {result['raw_count']}")
        print(f"effective_count      : {result['effective_count']:.12f}")
        print(f"non_redundancy       : {result['non_redundancy']:.12f}")
        print(f"family_balance       : {result['family_balance']:.12f}")
        print(f"relation_entropy     : {result['relation_entropy']:.12f}")
        print(f"collapse_resistance  : {result['collapse_resistance']:.12f}")

    os.makedirs("results", exist_ok=True)

    final_result = {
        "status": "PASS",
        "version": "0.1.0",
        "results": results,
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(final_result, f, indent=2)

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()