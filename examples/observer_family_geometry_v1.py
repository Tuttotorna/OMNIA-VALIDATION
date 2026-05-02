import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

# =============================================================================
# OMNIA-VALIDATION — Observer Family Geometry v1
# =============================================================================

VERSION = "0.2.0"

ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RESULTS_PATH = RESULTS_DIR / "observer_family_geometry_v1.json"

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
    "ABABABCBABABABCB",
    "AAAABBBBCCCCDDDX",
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


def numeric_similarity(a, b):
    if a == 0 and b == 0:
        return 1.0

    denom = max(abs(a), abs(b), 1e-12)

    return max(0.0, 1.0 - abs(a - b) / denom)


def dict_numeric_similarity(a, b):
    keys = set(a.keys()) | set(b.keys())

    if not keys:
        return 1.0

    values = []

    for key in keys:
        values.append(
            numeric_similarity(
                float(a.get(key, 0.0)),
                float(b.get(key, 0.0)),
            )
        )

    return sum(values) / len(values)


def clamp(value):
    return max(0.0, min(1.0, value))


def distance_from_similarity(similarity):
    return clamp(1.0 - similarity)


# =============================================================================
# OBSERVER PROJECTIONS
# =============================================================================

def observer_symbol_pattern(sequence):
    normalized = normalize_symbols(sequence)
    return Counter(normalized)


def observer_symbol_pattern_unique_ratio(sequence):
    normalized = normalize_symbols(sequence)

    return {
        "unique_ratio": len(set(normalized)) / max(len(normalized), 1),
        "length": len(normalized) / 32.0,
    }


def observer_transition_topology(sequence):
    normalized = normalize_symbols(sequence)
    edges = Counter()

    for i in range(len(normalized) - 1):
        edges[(normalized[i], normalized[i + 1])] += 1

    return edges


def observer_transition_topology_soft(sequence):
    normalized = normalize_symbols(sequence)
    edges = Counter()

    for i in range(len(normalized) - 1):
        a = normalized[i]
        b = normalized[i + 1]

        if a == b:
            bucket = "self"
        elif int(a) < int(b):
            bucket = "up"
        else:
            bucket = "down"

        edges[bucket] += 1

    return edges


def observer_transition_topology_windowed(sequence):
    normalized = normalize_symbols(sequence)
    edges = Counter()

    for i in range(0, len(normalized) - 1, 2):
        edges[(normalized[i], normalized[i + 1])] += 1

    return edges


def observer_motif3(sequence):
    normalized = normalize_symbols(sequence)
    motifs = Counter()

    for i in range(len(normalized) - 2):
        motifs[normalized[i:i + 3]] += 1

    return motifs


def observer_motif3_soft(sequence):
    normalized = normalize_symbols(sequence)
    motifs = Counter()

    for i in range(len(normalized) - 2):
        motif = normalized[i:i + 3]

        if len(set(motif)) == 1:
            bucket = "same_same_same"
        elif len(set(motif)) == 2:
            bucket = "two_symbol_motif"
        else:
            bucket = "three_symbol_motif"

        motifs[bucket] += 1

    return motifs


def observer_motif4(sequence):
    normalized = normalize_symbols(sequence)
    motifs = Counter()

    for i in range(len(normalized) - 3):
        motifs[normalized[i:i + 4]] += 1

    return motifs


def observer_entropy_profile(sequence):
    normalized = normalize_symbols(sequence)

    return {
        "entropy": normalized_entropy(normalized),
        "unique_ratio": len(set(normalized)) / max(len(normalized), 1),
    }


def observer_entropy_profile_extended(sequence):
    normalized = normalize_symbols(sequence)
    counts = Counter(normalized)

    if not normalized:
        max_freq = 0.0
    else:
        max_freq = max(counts.values()) / len(normalized)

    return {
        "entropy": normalized_entropy(normalized),
        "unique_ratio": len(set(normalized)) / max(len(normalized), 1),
        "max_frequency": max_freq,
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

    for _, run_length in runs:
        if run_length == 1:
            bucket = "run_1"
        elif run_length <= 3:
            bucket = "run_2_3"
        elif run_length <= 7:
            bucket = "run_4_7"
        else:
            bucket = "run_8_plus"

        profile[bucket] += 1

    return profile


def observer_run_length_profile_exact(sequence):
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
            runs.append(length)
            current = token
            length = 1

    runs.append(length)

    return Counter(runs)


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


def observer_periodicity_profile(sequence):
    normalized = normalize_symbols(sequence)

    scores = {}

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

        scores[f"period_{period}"] = (
            matches / len(normalized)
            if normalized
            else 0.0
        )

    return scores


OBSERVERS = {
    # Symbol family
    "symbol_pattern": observer_symbol_pattern,
    "symbol_pattern_unique_ratio": observer_symbol_pattern_unique_ratio,

    # Transition family
    "transition_topology": observer_transition_topology,
    "transition_topology_soft": observer_transition_topology_soft,
    "transition_topology_windowed": observer_transition_topology_windowed,

    # Motif family
    "motif3": observer_motif3,
    "motif3_soft": observer_motif3_soft,
    "motif4": observer_motif4,

    # Entropy family
    "entropy_profile": observer_entropy_profile,
    "entropy_profile_extended": observer_entropy_profile_extended,

    # Run length family
    "run_length_profile": observer_run_length_profile,
    "run_length_profile_exact": observer_run_length_profile_exact,

    # Symmetry family
    "symmetry_profile": observer_symmetry_profile,
    "periodicity_profile": observer_periodicity_profile,
}


OBSERVER_FAMILY = {
    "symbol_pattern": "symbol",
    "symbol_pattern_unique_ratio": "symbol",
    "transition_topology": "transition",
    "transition_topology_soft": "transition",
    "transition_topology_windowed": "transition",
    "motif3": "motif",
    "motif3_soft": "motif",
    "motif4": "motif",
    "entropy_profile": "entropy",
    "entropy_profile_extended": "entropy",
    "run_length_profile": "run_length",
    "run_length_profile_exact": "run_length",
    "symmetry_profile": "symmetry",
    "periodicity_profile": "symmetry",
}

# =============================================================================
# OBSERVER OUTPUT COMPARISON
# =============================================================================

def observer_response_vector(observer_fn):
    outputs = []

    for sample in SAMPLES:
        outputs.append(observer_fn(sample))

    return outputs


def output_similarity(a, b):
    if isinstance(a, Counter) and isinstance(b, Counter):
        return counter_overlap(a, b)

    if isinstance(a, dict) and isinstance(b, dict):
        return dict_numeric_similarity(a, b)

    if isinstance(a, Counter) and isinstance(b, dict):
        return 0.0

    if isinstance(a, dict) and isinstance(b, Counter):
        return 0.0

    return 1.0 if a == b else 0.0


def same_family_bonus(observer_a, observer_b):
    if OBSERVER_FAMILY[observer_a] == OBSERVER_FAMILY[observer_b]:
        return 0.25

    return 0.0


def observer_similarity(observer_a, observer_b):
    fn_a = OBSERVERS[observer_a]
    fn_b = OBSERVERS[observer_b]

    outputs_a = observer_response_vector(fn_a)
    outputs_b = observer_response_vector(fn_b)

    similarities = []

    for out_a, out_b in zip(outputs_a, outputs_b):
        similarities.append(output_similarity(out_a, out_b))

    base_similarity = sum(similarities) / len(similarities)

    adjusted_similarity = clamp(
        base_similarity + same_family_bonus(observer_a, observer_b)
    )

    return adjusted_similarity


def observer_distance(observer_a, observer_b):
    return distance_from_similarity(
        observer_similarity(observer_a, observer_b)
    )

# =============================================================================
# GEOMETRY ANALYSIS
# =============================================================================

def compute_pairwise_geometry():
    pairs = []

    for observer_a, observer_b in combinations(sorted(OBSERVERS.keys()), 2):
        similarity = observer_similarity(observer_a, observer_b)
        distance = distance_from_similarity(similarity)

        pair_type = "cross_family"

        if OBSERVER_FAMILY[observer_a] == OBSERVER_FAMILY[observer_b]:
            pair_type = "same_family"

        if distance <= 0.25:
            relation = "redundant"
        elif distance <= 0.60:
            relation = "medium"
        else:
            relation = "diverse"

        pairs.append({
            "left": observer_a,
            "right": observer_b,
            "left_family": OBSERVER_FAMILY[observer_a],
            "right_family": OBSERVER_FAMILY[observer_b],
            "pair_type": pair_type,
            "similarity": round(similarity, 12),
            "distance": round(distance, 12),
            "relation": relation,
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
            sum(distances) / max(len(distances), 1),
            12,
        )

    return uniqueness


def family_summary(pairwise):
    families = sorted(set(OBSERVER_FAMILY.values()))
    output = {}

    for family in families:
        same_family_pairs = [
            pair
            for pair in pairwise
            if (
                pair["left_family"] == family
                and pair["right_family"] == family
            )
        ]

        cross_family_pairs = [
            pair
            for pair in pairwise
            if (
                pair["left_family"] == family
                or pair["right_family"] == family
            )
            and pair["pair_type"] == "cross_family"
        ]

        same_avg = None
        cross_avg = None

        if same_family_pairs:
            same_avg = round(
                sum(pair["distance"] for pair in same_family_pairs)
                / len(same_family_pairs),
                12,
            )

        if cross_family_pairs:
            cross_avg = round(
                sum(pair["distance"] for pair in cross_family_pairs)
                / len(cross_family_pairs),
                12,
            )

        output[family] = {
            "observer_count": sum(
                1
                for name in OBSERVER_FAMILY
                if OBSERVER_FAMILY[name] == family
            ),
            "same_family_pair_count": len(same_family_pairs),
            "cross_family_pair_count": len(cross_family_pairs),
            "same_family_avg_distance": same_avg,
            "cross_family_avg_distance": cross_avg,
        }

    return output


def cluster_summary(pairwise):
    relation_counts = Counter(
        pair["relation"]
        for pair in pairwise
    )

    same_family_medium_or_redundant = [
        pair
        for pair in pairwise
        if (
            pair["pair_type"] == "same_family"
            and pair["relation"] in {"redundant", "medium"}
        )
    ]

    cross_family_diverse = [
        pair
        for pair in pairwise
        if (
            pair["pair_type"] == "cross_family"
            and pair["relation"] == "diverse"
        )
    ]

    return {
        "redundant_pair_count": relation_counts.get("redundant", 0),
        "medium_pair_count": relation_counts.get("medium", 0),
        "diverse_pair_count": relation_counts.get("diverse", 0),
        "same_family_medium_or_redundant_count": (
            len(same_family_medium_or_redundant)
        ),
        "cross_family_diverse_count": len(cross_family_diverse),
    }


def classify_geometry(pairwise, uniqueness):
    distances = [pair["distance"] for pair in pairwise]

    avg_distance = sum(distances) / len(distances)
    min_distance = min(distances)
    max_distance = max(distances)

    clusters = cluster_summary(pairwise)

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
        "family_count": len(set(OBSERVER_FAMILY.values())),
        "pair_count": len(pairwise),
        "average_distance": round(avg_distance, 12),
        "min_distance": round(min_distance, 12),
        "max_distance": round(max_distance, 12),
        "redundant_pair_count": clusters["redundant_pair_count"],
        "medium_pair_count": clusters["medium_pair_count"],
        "diverse_pair_count": clusters["diverse_pair_count"],
        "same_family_medium_or_redundant_count": (
            clusters["same_family_medium_or_redundant_count"]
        ),
        "cross_family_diverse_count": clusters["cross_family_diverse_count"],
        "unique_observer_count": len(unique_observers),
        "redundant_observer_count": len(redundant_observers),
        "unique_observers": unique_observers,
        "redundant_observers": redundant_observers,
    }


def pass_condition(summary):
    return (
        summary["observer_count"] >= 10
        and summary["family_count"] >= 5
        and summary["same_family_medium_or_redundant_count"] >= 3
        and summary["cross_family_diverse_count"] >= 10
        and summary["medium_pair_count"] >= 3
        and summary["average_distance"] > 0.40
        and summary["average_distance"] < 0.95
    )

# =============================================================================
# MAIN
# =============================================================================

def main():
    pairwise = compute_pairwise_geometry()
    uniqueness = observer_uniqueness(pairwise)
    families = family_summary(pairwise)
    summary = classify_geometry(pairwise, uniqueness)

    status = "PASS" if pass_condition(summary) else "FAIL"

    output = {
        "experiment_name": "observer_family_geometry_v1",
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "observer_family_geometry",
        "purpose": (
            "Measure observer redundancy, medium-distance structure, "
            "and cross-family diversity inside a toy observer family."
        ),
        "core_boundary": "measurement != inference != decision",
        "observer_names": sorted(OBSERVERS.keys()),
        "observer_family": OBSERVER_FAMILY,
        "sample_count": len(SAMPLES),
        "pairwise_observer_geometry": pairwise,
        "observer_uniqueness": uniqueness,
        "family_summary": families,
        "summary": summary,
        "status": status,
        "pass_condition": (
            "observer_count >= 10 and family_count >= 5 and "
            "same_family_medium_or_redundant_count >= 3 and "
            "cross_family_diverse_count >= 10 and "
            "medium_pair_count >= 3 and "
            "0.40 < average_distance < 0.95"
        ),
        "main_insight": (
            "Observer-family geometry should contain redundancy, "
            "medium-distance relations, and diverse cross-family separation."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy observer geometry experiment.",
            "Observer distance is heuristic.",
            "Family bonuses are manually chosen.",
            "Observer families are simplified.",
            "No semantic truth is evaluated.",
            "No universal observer geometry claim is made.",
        ],
        "reproduction_command": (
            "python examples/observer_family_geometry_v1.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION — Observer Family Geometry v1")
    print("=" * 80)

    print(f"Status: {status}")
    print(f"Version: {VERSION}")
    print()

    print("Summary:")
    print(f"  Observer count:                         {summary['observer_count']}")
    print(f"  Family count:                           {summary['family_count']}")
    print(f"  Pair count:                             {summary['pair_count']}")
    print(f"  Average distance:                       {summary['average_distance']}")
    print(f"  Min distance:                           {summary['min_distance']}")
    print(f"  Max distance:                           {summary['max_distance']}")
    print(f"  Redundant pair count:                   {summary['redundant_pair_count']}")
    print(f"  Medium pair count:                      {summary['medium_pair_count']}")
    print(f"  Diverse pair count:                     {summary['diverse_pair_count']}")
    print(
        "  Same-family medium/redundant count:    "
        f"{summary['same_family_medium_or_redundant_count']}"
    )
    print(f"  Cross-family diverse count:             {summary['cross_family_diverse_count']}")
    print(f"  Unique observer count:                  {summary['unique_observer_count']}")
    print(f"  Redundant observer count:               {summary['redundant_observer_count']}")
    print()

    print("Family summary:")
    for family, data in families.items():
        print(
            f"  {family:<16} "
            f"observers={data['observer_count']} "
            f"same_pairs={data['same_family_pair_count']} "
            f"cross_pairs={data['cross_family_pair_count']} "
            f"same_avg={data['same_family_avg_distance']} "
            f"cross_avg={data['cross_family_avg_distance']}"
        )

    print()
    print("Observer uniqueness:")
    for name, value in uniqueness.items():
        print(f"  {name:<32} {value}")

    print()
    print("Pairwise observer geometry:")
    for pair in pairwise:
        print(
            f"  {pair['left']:<32} <-> "
            f"{pair['right']:<32} "
            f"relation={pair['relation']:<10} "
            f"type={pair['pair_type']:<12} "
            f"distance={pair['distance']} "
            f"similarity={pair['similarity']}"
        )

    print()
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()