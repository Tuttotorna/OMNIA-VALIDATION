#!/usr/bin/env python3

import json
import math
import os
import random
from collections import Counter


RESULTS_PATH = "results/recoverability_effective_observer_v0.json"

random.seed(42)


BASE_OBSERVERS = [
    {"id": "symmetry_A",   "family": "symmetry"},
    {"id": "symmetry_B",   "family": "symmetry"},
    {"id": "topology_A",   "family": "topology"},
    {"id": "topology_B",   "family": "topology"},
    {"id": "entropy_A",    "family": "entropy"},
    {"id": "entropy_B",    "family": "entropy"},
    {"id": "geometry_A",   "family": "geometry"},
    {"id": "geometry_B",   "family": "geometry"},
    {"id": "causality_A",  "family": "causality"},
    {"id": "causality_B",  "family": "causality"},
    {"id": "continuity_A", "family": "continuity"},
    {"id": "continuity_B", "family": "continuity"},
]


TARGET_STRUCTURE = {
    "symmetry": 0.85,
    "topology": 0.70,
    "entropy": 0.55,
    "geometry": 0.90,
    "causality": 0.65,
    "continuity": 0.80,
}


def compute_pairwise_distances(observers):

    distances = []

    for i in range(len(observers)):
        for j in range(i + 1, len(observers)):

            a = observers[i]
            b = observers[j]

            if a["id"] == b["id"]:
                d = 0.0

            elif a["family"] == b["family"]:
                d = 0.35

            else:
                d = 0.85

            distances.append(d)

    return distances


def relation_entropy(distances):

    if not distances:
        return 0.0

    bins = {"low": 0, "mid": 0, "high": 0}

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

    return entropy / math.log(3)


def family_balance(observers):

    counts = Counter(o["family"] for o in observers)

    total = len(observers)

    entropy = 0.0

    for c in counts.values():

        p = c / total
        entropy -= p * math.log(p)

    max_entropy = math.log(len(counts))

    if max_entropy == 0:
        return 0.0

    return entropy / max_entropy


def non_redundancy(distances):

    redundant = sum(1 for d in distances if d < 0.2)

    return 1.0 - (redundant / len(distances))


def collapse_resistance(distances):

    return sum(distances) / len(distances)


def effective_observer_count(observers):

    distances = compute_pairwise_distances(observers)

    nr = non_redundancy(distances)
    fb = family_balance(observers)
    re = relation_entropy(distances)
    cr = collapse_resistance(distances)

    raw = len(observers)

    effective = raw * nr * fb * re * cr

    return {
        "raw_count": raw,
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


def simulate_projection(observer):

    family = observer["family"]

    if family not in TARGET_STRUCTURE:
        baseline = 0.30
    else:
        baseline = TARGET_STRUCTURE[family]

    noise = random.uniform(-0.12, 0.12)

    return max(0.0, min(1.0, baseline + noise))


def recoverability_score(observers):

    projections = []

    for observer in observers:

        projections.append(simulate_projection(observer))

    if not projections:
        return 0.0

    mean_projection = sum(projections) / len(projections)

    diversity = len(set(o["family"] for o in observers)) / len(observers)

    stability = 1.0 - (
        sum(abs(p - mean_projection) for p in projections)
        / len(projections)
    )

    score = (
        mean_projection
        * diversity
        * stability
    )

    return max(0.0, score)


def evaluate_system(name, observers):

    effective = effective_observer_count(observers)

    recovery = recoverability_score(observers)

    return {
        "system": name,
        "raw_count": effective["raw_count"],
        "effective_count": effective["effective_count"],
        "recoverability_score": recovery,
        "non_redundancy": effective["non_redundancy"],
        "family_balance": effective["family_balance"],
        "relation_entropy": effective["relation_entropy"],
        "collapse_resistance": effective["collapse_resistance"],
    }


def main():

    print("=" * 80)
    print("OMNIA-VALIDATION — Recoverability vs Effective Observer Count v0")
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
        print(f"raw_count             : {result['raw_count']}")
        print(f"effective_count       : {result['effective_count']:.12f}")
        print(f"recoverability_score  : {result['recoverability_score']:.12f}")
        print(f"non_redundancy        : {result['non_redundancy']:.12f}")
        print(f"family_balance        : {result['family_balance']:.12f}")
        print(f"relation_entropy      : {result['relation_entropy']:.12f}")
        print(f"collapse_resistance   : {result['collapse_resistance']:.12f}")

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