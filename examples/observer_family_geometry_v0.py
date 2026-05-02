import json
import math
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

# =============================================================================
# OMNIA-VALIDATION — Observer Family Geometry v0
# =============================================================================

VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RESULTS_PATH = RESULTS_DIR / "observer_family_geometry_v0.json"

# =============================================================================
# SYNTHETIC STRUCTURAL SAMPLE
# =============================================================================

SAMPLES = [
    "ABABABABABABABAB",
    "ABCDABCDABCDABCD",
    "AAAABBBBCCCCDDDD",
    "ABCABCABCABCABCA",
    "AABBAABBAABBAABB",
    "ABCDCBAABCDCBAAB",
    "AAAABAAAABAAAABA",
    "ABCDEFGHIJKLMNOP",
]

# =============================================================================
# BASIC HELPERS
# =============================================================================

def normalize_symbols(sequence):
    mapping = {}
    next_id = 0
    normalized = []

    for token in sequence:
        if token not in mapping:
            mapping[token] = str(next_id)
            next_id += 1

        normalized.append(mapping[token])

    return "".join(normalized)


def entropy(sequence):
    if not sequence:
        return 0.0

    counts = Counter(sequence)
    total = len(sequence)

    value = 0.0

    for count in counts.values():
        p = count / total

        if p > 0:
            value -= p * math.log2(p)

    return value


def normalized_entropy(sequence):
    if not sequence:
        return 0.0

    unique = len(set(sequence))

    if unique <= 1:
        return 0.0

    return entropy(sequence) / math.log2(unique)


def counter_overlap(a, b):
    keys = set(a.keys()) | set(b.keys())

    if not keys:
        return 1.0

    numerator = sum(
        min(a.get(k, 0), b.get(k, 0))
        for k in keys
    )

    denominator = sum(
        max(a.get(k, 0), b.get(k, 0))
        for k in keys
    )

    if denominator == 0:
        return 1.0

    return numerator / denominator


def scalar_similarity(a, b):
    if a == 0 and b == 0:
        return 1.0

    denom = max(abs(a), abs(b), 1e-12)

    return max(0.0, 1.0 - abs(a - b) / denom)


def distance_from_similarity(similarity):
    return max(0.0, min(1.0, 1.0 - similarity))


# =============================================================================
# OBSERVER PROJECTIONS
# =============================================================================

def observer_symbol_pattern(sequence):
    normalized = normalize_symbols(sequence)
    return Counter(normalized)


def observer_transition_topology(sequence):
    normalized = normalize_symbols(sequence)
    edges = Counter()

    for i in range(len(normalized) - 1):
        edges[(normalized[i], normalized[i + 1])] += 1

    return edges


def observer_motif3(sequence):
    normalized = normalize_symbols(sequence)
    motifs = Counter()

    for i in range(len(normalized) - 2):
        motifs[normalized[i:i + 3]] += 1

    return motifs


def observer_entropy_profile(sequence):
    normalized = normalize_symbols(sequence)

    return {
        "entropy": normalized_entropy(normalized),
        "unique_ratio": len(set(normalized)) / max(len(normalized), 1),
    }


def observer_run_length_profile(sequence):
    normalized = normalize_symbols(sequence)

    if not normalized:
        return Counter()

    runs = []
    current = normalized[0]
    length = 1

    for token in normalized[1:]:
        if token == current:
            length += 1
        else:
            runs.append((current, length))
            current = token
            length = 1

    runs.append((current, length))

    profile = Counter()

    for _, length in runs:
        if length == 1:
            bucket = "run_1"
        elif length <= 3:
            bucket = "run_2_3"
        elif length <= 7:
            bucket = "run_4_7"
        else:
            bucket = "run_8_plus"

        profile[bucket] += 1

    return profile


def observer_symmetry_profile(sequence):
    normalized = normalize_symbols(sequence)

    if not normalized:
        return {
            "mirror_similarity": 1.0,
            "periodicity_strength": 0.0,
        }

    reversed_seq = normalized[::-1]

    same_positions = sum(
        1
        for a, b in zip(normalized, reversed_seq)
        if a == b
    )

    mirror_similarity = same_positions / len(normalized)

    periodicity_scores = []

    for period in range(1, min(8, len(normalized)) + 1):
        template = normalized[:period]
        reconstructed = (
            template * ((len(normalized) // period) + 1)
        )[:len(normalized)]

        matches = sum(
            1
            for a, b in zip(normalized, reconstructed)
            if a == b
        )

        periodicity_scores.append(matches / len(normalized))

    return {
        "mirror_similarity": mirror_similarity,
        "periodicity_strength": max(periodicity_scores),
    }


OBSERVERS = {
    "symbol_pattern": observer_symbol_pattern,
    "transition_topology": observer_transition_topology,
    "motif3": observer_motif3,
    "entropy_profile": observer_entropy_profile,
    "run_length_profile": observer_run_length_profile,
    "symmetry_profile": observer_symmetry_profile,
}

# =============================================================================
# OBSERVER OUTPUT SIMILARITY
# =============================================================================

def compare_outputs(a, b):
    if isinstance(a, Counter) and isinstance(b, Counter):
        return counter_overlap(a, b)

    if isinstance(a, dict) and isinstance(b, dict):
        keys = set(a.keys()) | set(b.keys())

        if not keys:
            return 1.0

        sims = []

        for key in keys:
            sims.append(
                scalar_similarity(
                    float(a.get(key, 0.0)),
                    float(b.get(key, 0.0)),
                )
            )

        return sum(sims) / len(sims)

    return 1.0 if a == b else 0.0


def observer_response_vector(observer_fn):
    outputs = []

    for sample in SAMPLES:
        outputs.append(observer_fn(sample))

    return outputs


def observer_similarity(observer_a, observer_b):
    fn_a = OBSERVERS[observer_a]
    fn_b = OBSERVERS[observer_b]

    outputs_a = observer_response_vector(fn_a)
    outputs_b = observer_response_vector(fn_b)

    similarities = []

    for out_a, out_b in zip(outputs_a, outputs_b):
        similarities.append(compare_outputs(out_a, out_b))

    return sum(similarities) / len(similarities)


def observer_distance(observer_a, observer_b):
    sim = observer_similarity(observer_a, observer_b)
    return distance_from_similarity(sim)


# =============================================================================
# GEOMETRY SUMMARY
# =============================================================================

def compute_pairwise_geometry():
    pairs = []

    for observer_a, observer_b in combinations(sorted(OBSERVERS.keys()), 2):
        similarity = observer_similarity(observer_a, observer_b)
        distance = distance_from_similarity(similarity)

        pairs.append({
            "left": observer_a,
            "right": observer_b,
            "similarity": round(similarity, 12),
            "distance": round(distance, 12),
        })

    return pairs


def observer_uniqueness(pairwise):
    names = sorted(OBSERVERS.keys())

    uniqueness = {}

    for name in names:
        distances = []

        for pair in pairwise:
            if pair["left"] == name or pair["right"] == name:
                distances.append(pair["distance"])

        uniqueness[name] = round(
            sum(distances) / len(distances),
            12,
        )

    return uniqueness


def classify_geometry(pairwise, uniqueness):
    distances = [p["distance"] for p in pairwise]

    avg_distance = sum(distances) / len(distances)
    max_distance = max(distances)
    min_distance = min(distances)

    redundancy_pairs = [
        p
        for p in pairwise
        if p["distance"] <= 0.20
    ]

    diverse_pairs = [
        p
        for p in pairwise
        if p["distance"] >= 0.60
    ]

    unique_observers = [
        name
        for name, value in uniqueness.items()
        if value >= 0.45
    ]

    redundant_observers = [
        name
        for name, value in uniqueness.items()
        if value <= 0.25
    ]

    return {
        "observer_count": len(OBSERVERS),
        "pair_count": len(pairwise),
        "average_distance": round(avg_distance, 12),
        "min_distance": round(min_distance, 12),
        "max_distance": round(max_distance, 12),
        "redundancy_pair_count": len(redundancy_pairs),
        "diverse_pair_count": len(diverse_pairs),
        "unique_observer_count": len(unique_observers),
        "redundant_observer_count": len(redundant_observers),
        "unique_observers": unique_observers,
        "redundant_observers": redundant_observers,
    }


def pass_condition(summary):
    return (
        summary["observer_count"] >= 5
        and summary["average_distance"] > 0.25
        and summary["diverse_pair_count"] >= 2
        and summary["unique_observer_count"] >= 2
    )


# =============================================================================
# MAIN
# =============================================================================

def main():
    pairwise = compute_pairwise_geometry()
    uniqueness = observer_uniqueness(pairwise)
    summary = classify_geometry(pairwise, uniqueness)

    status = "PASS" if pass_condition(summary) else "FAIL"

    output = {
        "experiment_name": "observer_family_geometry_v0",
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "observer_family_geometry",
        "purpose": (
            "Measure redundancy and diversity inside a toy observer family."
        ),
        "core_boundary": "measurement != inference != decision",
        "observer_names": sorted(OBSERVERS.keys()),
        "sample_count": len(SAMPLES),
        "pairwise_observer_geometry": pairwise,
        "observer_uniqueness": uniqueness,
        "summary": summary,
        "status": status,
        "pass_condition": (
            "observer_count >= 5 and average_distance > 0.25 "
            "and diverse_pair_count >= 2 and unique_observer_count >= 2"
        ),
        "main_insight": (
            "Observer count alone is insufficient; recovery evidence "
            "must account for observer redundancy and diversity."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy observer geometry experiment.",
            "Observer distance is heuristic.",
            "Observer families are simplified.",
            "No semantic truth is evaluated.",
            "No universal observer geometry claim is made.",
        ],
        "reproduction_command": (
            "python examples/observer_family_geometry_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION — Observer Family Geometry v0")
    print("=" * 80)

    print(f"Status: {status}")
    print(f"Version: {VERSION}")
    print()

    print("Summary:")
    print(f"  Observer count:             {summary['observer_count']}")
    print(f"  Pair count:                 {summary['pair_count']}")
    print(f"  Average distance:           {summary['average_distance']}")
    print(f"  Min distance:               {summary['min_distance']}")
    print(f"  Max distance:               {summary['max_distance']}")
    print(f"  Redundancy pair count:      {summary['redundancy_pair_count']}")
    print(f"  Diverse pair count:         {summary['diverse_pair_count']}")
    print(f"  Unique observer count:      {summary['unique_observer_count']}")
    print(f"  Redundant observer count:   {summary['redundant_observer_count']}")
    print()

    print("Observer uniqueness:")
    for name, value in uniqueness.items():
        print(f"  {name:<24} {value}")

    print()
    print("Pairwise observer geometry:")
    for pair in pairwise:
        print(
            f"  {pair['left']:<24} <-> "
            f"{pair['right']:<24} "
            f"distance={pair['distance']} "
            f"similarity={pair['similarity']}"
        )

    print()
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()