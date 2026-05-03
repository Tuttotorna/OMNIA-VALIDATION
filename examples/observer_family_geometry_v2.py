import json
import math
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

# =============================================================================
# OMNIA-VALIDATION — Observer Family Geometry v2
# =============================================================================

VERSION = "0.3.0"

ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RESULTS_PATH = RESULTS_DIR / "observer_family_geometry_v2.json"

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
    "AABBCCDDAABBCCDD",
    "ABBAABBAABBAABBA",
]

# =============================================================================
# HELPERS
# =============================================================================

def clamp(value):
    return max(0.0, min(1.0, value))


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


def cosine_similarity(a, b):
    keys = set(a.keys()) | set(b.keys())

    if not keys:
        return 1.0

    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)

    norm_a = math.sqrt(sum(a.get(k, 0.0) ** 2 for k in keys))
    norm_b = math.sqrt(sum(b.get(k, 0.0) ** 2 for k in keys))

    if norm_a == 0 and norm_b == 0:
        return 1.0

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return clamp(dot / (norm_a * norm_b))


def euclidean_distance(a, b):
    keys = set(a.keys()) | set(b.keys())

    if not keys:
        return 0.0

    return math.sqrt(
        sum(
            (a.get(k, 0.0) - b.get(k, 0.0)) ** 2
            for k in keys
        )
    )


# =============================================================================
# BASE FEATURE EXTRACTORS
# =============================================================================

def transition_counts(sequence):
    normalized = normalize_symbols(sequence)
    edges = Counter()

    for i in range(len(normalized) - 1):
        edges[(normalized[i], normalized[i + 1])] += 1

    return edges


def transition_counts_windowed(sequence, step=2):
    normalized = normalize_symbols(sequence)
    edges = Counter()

    for i in range(0, len(normalized) - 1, step):
        edges[(normalized[i], normalized[i + 1])] += 1

    return edges


def transition_direction_counts(sequence):
    normalized = normalize_symbols(sequence)
    edges = Counter()

    for i in range(len(normalized) - 1):
        a = int(normalized[i])
        b = int(normalized[i + 1])

        if a == b:
            bucket = "self"
        elif a < b:
            bucket = "up"
        else:
            bucket = "down"

        edges[bucket] += 1

    return edges


def motif_counts(sequence, size):
    normalized = normalize_symbols(sequence)
    motifs = Counter()

    for i in range(len(normalized) - size + 1):
        motifs[normalized[i:i + size]] += 1

    return motifs


def motif_shape_counts(sequence, size):
    normalized = normalize_symbols(sequence)
    motifs = Counter()

    for i in range(len(normalized) - size + 1):
        motif = normalized[i:i + size]
        unique = len(set(motif))

        motifs[f"size_{size}_unique_{unique}"] += 1

    return motifs


def run_length_counts(sequence):
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


def run_length_bucket_counts(sequence):
    runs = run_length_counts(sequence)
    buckets = Counter()

    for run_length, count in runs.items():
        if run_length == 1:
            bucket = "run_1"
        elif run_length <= 3:
            bucket = "run_2_3"
        elif run_length <= 7:
            bucket = "run_4_7"
        else:
            bucket = "run_8_plus"

        buckets[bucket] += count

    return buckets


def periodicity_scores(sequence):
    normalized = normalize_symbols(sequence)
    scores = {}

    if not normalized:
        return {
            "periodicity_strength": 0.0,
            "best_period_norm": 0.0,
        }

    best_score = 0.0
    best_period = 1

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

        score = matches / len(normalized)

        if score > best_score:
            best_score = score
            best_period = period

    scores["periodicity_strength"] = best_score
    scores["best_period_norm"] = best_period / min(8, len(normalized))

    return scores


def symmetry_scores(sequence):
    normalized = normalize_symbols(sequence)

    if not normalized:
        return {
            "mirror_similarity": 1.0,
        }

    reversed_seq = normalized[::-1]

    same_positions = sum(
        1
        for a, b in zip(normalized, reversed_seq)
        if a == b
    )

    return {
        "mirror_similarity": same_positions / len(normalized),
    }


# =============================================================================
# COMMON RESPONSE VECTOR
# =============================================================================

def base_common_features(sequence):
    normalized = normalize_symbols(sequence)
    length = len(normalized)
    unique = len(set(normalized))

    transitions = transition_counts(sequence)
    motifs3 = motif_counts(sequence, 3)
    motifs4 = motif_counts(sequence, 4)
    runs = run_length_counts(sequence)
    run_buckets = run_length_bucket_counts(sequence)
    periodicity = periodicity_scores(sequence)
    symmetry = symmetry_scores(sequence)

    repeated_transition_mass = sum(
        count
        for count in transitions.values()
        if count > 1
    )

    repeated_motif3_mass = sum(
        count
        for count in motifs3.values()
        if count > 1
    )

    repeated_motif4_mass = sum(
        count
        for count in motifs4.values()
        if count > 1
    )

    max_run = max(runs.keys()) if runs else 0

    return {
        "entropy": normalized_entropy(normalized),
        "unique_ratio": unique / max(length, 1),
        "transition_density": len(transitions) / max(length - 1, 1),
        "transition_repetition": repeated_transition_mass / max(length - 1, 1),
        "motif3_density": len(motifs3) / max(length - 2, 1),
        "motif3_repetition": repeated_motif3_mass / max(length - 2, 1),
        "motif4_density": len(motifs4) / max(length - 3, 1),
        "motif4_repetition": repeated_motif4_mass / max(length - 3, 1),
        "run_count_norm": sum(runs.values()) / max(length, 1),
        "max_run_norm": max_run / max(length, 1),
        "run_1_ratio": run_buckets.get("run_1", 0) / max(sum(run_buckets.values()), 1),
        "run_2_3_ratio": run_buckets.get("run_2_3", 0) / max(sum(run_buckets.values()), 1),
        "run_4_7_ratio": run_buckets.get("run_4_7", 0) / max(sum(run_buckets.values()), 1),
        "periodicity_strength": periodicity["periodicity_strength"],
        "best_period_norm": periodicity["best_period_norm"],
        "mirror_similarity": symmetry["mirror_similarity"],
    }


def weighted_common_vector(sequence, weights):
    base = base_common_features(sequence)

    return {
        key: value * weights.get(key, 0.0)
        for key, value in base.items()
    }


# =============================================================================
# OBSERVER DEFINITIONS
# =============================================================================

OBSERVERS = {
    # entropy cluster
    "entropy_profile": {
        "family": "entropy",
        "weights": {
            "entropy": 1.0,
            "unique_ratio": 0.8,
            "transition_density": 0.15,
            "motif3_density": 0.1,
        },
    },
    "entropy_profile_extended": {
        "family": "entropy",
        "weights": {
            "entropy": 1.0,
            "unique_ratio": 0.8,
            "transition_density": 0.2,
            "motif3_density": 0.15,
            "run_count_norm": 0.15,
        },
    },

    # transition cluster
    "transition_topology": {
        "family": "transition",
        "weights": {
            "transition_density": 1.0,
            "transition_repetition": 1.0,
            "motif3_density": 0.35,
            "motif3_repetition": 0.35,
            "periodicity_strength": 0.25,
        },
    },
    "transition_topology_soft": {
        "family": "transition",
        "weights": {
            "transition_density": 0.85,
            "transition_repetition": 0.85,
            "motif3_density": 0.25,
            "motif3_repetition": 0.25,
            "entropy": 0.2,
        },
    },
    "transition_topology_windowed": {
        "family": "transition",
        "weights": {
            "transition_density": 0.75,
            "transition_repetition": 0.75,
            "periodicity_strength": 0.4,
            "best_period_norm": 0.3,
        },
    },

    # motif cluster
    "motif3": {
        "family": "motif",
        "weights": {
            "motif3_density": 1.0,
            "motif3_repetition": 1.0,
            "transition_density": 0.35,
            "transition_repetition": 0.35,
            "periodicity_strength": 0.2,
        },
    },
    "motif3_soft": {
        "family": "motif",
        "weights": {
            "motif3_density": 0.75,
            "motif3_repetition": 0.75,
            "entropy": 0.25,
            "transition_density": 0.25,
        },
    },
    "motif4": {
        "family": "motif",
        "weights": {
            "motif4_density": 1.0,
            "motif4_repetition": 1.0,
            "motif3_density": 0.4,
            "motif3_repetition": 0.4,
        },
    },

    # run cluster
    "run_length_profile": {
        "family": "run_length",
        "weights": {
            "run_count_norm": 1.0,
            "max_run_norm": 1.0,
            "run_1_ratio": 0.8,
            "run_2_3_ratio": 0.8,
            "run_4_7_ratio": 0.8,
        },
    },
    "run_length_profile_soft": {
        "family": "run_length",
        "weights": {
            "run_count_norm": 0.75,
            "max_run_norm": 0.75,
            "run_1_ratio": 0.6,
            "run_2_3_ratio": 0.6,
            "entropy": 0.25,
        },
    },

    # symbol cluster
    "symbol_pattern": {
        "family": "symbol",
        "weights": {
            "unique_ratio": 1.0,
            "entropy": 0.8,
            "transition_density": 0.2,
            "motif3_density": 0.15,
        },
    },
    "symbol_pattern_soft": {
        "family": "symbol",
        "weights": {
            "unique_ratio": 0.75,
            "entropy": 0.6,
            "run_count_norm": 0.25,
            "transition_density": 0.2,
        },
    },

    # symmetry cluster
    "symmetry_profile": {
        "family": "symmetry",
        "weights": {
            "mirror_similarity": 1.0,
            "periodicity_strength": 0.4,
            "best_period_norm": 0.3,
        },
    },
    "periodicity_profile": {
        "family": "symmetry",
        "weights": {
            "periodicity_strength": 1.0,
            "best_period_norm": 1.0,
            "mirror_similarity": 0.3,
            "transition_repetition": 0.2,
        },
    },
}

# =============================================================================
# OBSERVER RESPONSE GEOMETRY
# =============================================================================

def observer_response(observer_name):
    observer = OBSERVERS[observer_name]
    weights = observer["weights"]

    vectors = []

    for sample in SAMPLES:
        vectors.append(
            weighted_common_vector(sample, weights)
        )

    aggregate = {}

    feature_names = sorted(base_common_features(SAMPLES[0]).keys())

    for feature in feature_names:
        values = [vector.get(feature, 0.0) for vector in vectors]
        aggregate[f"mean_{feature}"] = sum(values) / len(values)

        variance = sum(
            (value - aggregate[f"mean_{feature}"]) ** 2
            for value in values
        ) / len(values)

        aggregate[f"var_{feature}"] = variance

    return aggregate


def observer_similarity(observer_a, observer_b):
    response_a = observer_response(observer_a)
    response_b = observer_response(observer_b)

    return cosine_similarity(response_a, response_b)


def observer_distance(observer_a, observer_b):
    return 1.0 - observer_similarity(observer_a, observer_b)


# =============================================================================
# GEOMETRY ANALYSIS
# =============================================================================

def classify_relation(distance):
    if distance <= 0.20:
        return "redundant"

    if distance <= 0.60:
        return "medium"

    return "diverse"


def compute_pairwise_geometry():
    pairs = []

    for observer_a, observer_b in combinations(sorted(OBSERVERS.keys()), 2):
        similarity = observer_similarity(observer_a, observer_b)
        distance = observer_distance(observer_a, observer_b)

        family_a = OBSERVERS[observer_a]["family"]
        family_b = OBSERVERS[observer_b]["family"]

        pair_type = (
            "same_family"
            if family_a == family_b
            else "cross_family"
        )

        pairs.append({
            "left": observer_a,
            "right": observer_b,
            "left_family": family_a,
            "right_family": family_b,
            "pair_type": pair_type,
            "similarity": round(similarity, 12),
            "distance": round(distance, 12),
            "relation": classify_relation(distance),
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
    families = sorted(
        set(observer["family"] for observer in OBSERVERS.values())
    )

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
                pair["pair_type"] == "cross_family"
                and (
                    pair["left_family"] == family
                    or pair["right_family"] == family
                )
            )
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
                for observer in OBSERVERS.values()
                if observer["family"] == family
            ),
            "same_family_pair_count": len(same_family_pairs),
            "cross_family_pair_count": len(cross_family_pairs),
            "same_family_avg_distance": same_avg,
            "cross_family_avg_distance": cross_avg,
        }

    return output


def relation_summary(pairwise):
    counts = Counter(pair["relation"] for pair in pairwise)

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
        "redundant_pair_count": counts.get("redundant", 0),
        "medium_pair_count": counts.get("medium", 0),
        "diverse_pair_count": counts.get("diverse", 0),
        "same_family_medium_or_redundant_count": len(
            same_family_medium_or_redundant
        ),
        "cross_family_diverse_count": len(cross_family_diverse),
    }


def classify_geometry(pairwise, uniqueness):
    distances = [pair["distance"] for pair in pairwise]
    relations = relation_summary(pairwise)

    unique_observers = [
        name
        for name, value in uniqueness.items()
        if value >= 0.35
    ]

    redundant_observers = [
        name
        for name, value in uniqueness.items()
        if value <= 0.20
    ]

    return {
        "observer_count": len(OBSERVERS),
        "family_count": len(
            set(observer["family"] for observer in OBSERVERS.values())
        ),
        "pair_count": len(pairwise),
        "average_distance": round(sum(distances) / len(distances), 12),
        "min_distance": round(min(distances), 12),
        "max_distance": round(max(distances), 12),
        **relations,
        "unique_observer_count": len(unique_observers),
        "redundant_observer_count": len(redundant_observers),
        "unique_observers": unique_observers,
        "redundant_observers": redundant_observers,
    }


def pass_condition(summary):
    return (
        summary["observer_count"] >= 10
        and summary["family_count"] >= 5
        and summary["redundant_pair_count"] >= 2
        and summary["medium_pair_count"] >= 10
        and summary["diverse_pair_count"] >= 10
        and summary["same_family_medium_or_redundant_count"] >= 5
        and summary["cross_family_diverse_count"] >= 5
        and 0.20 < summary["average_distance"] < 0.80
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
        "experiment_name": "observer_family_geometry_v2",
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "observer_family_geometry",
        "purpose": (
            "Measure observer redundancy, medium-distance structure, and "
            "cross-family diversity using a shared observer-response feature space."
        ),
        "core_boundary": "measurement != inference != decision",
        "observer_names": sorted(OBSERVERS.keys()),
        "observer_family": {
            name: data["family"]
            for name, data in OBSERVERS.items()
        },
        "sample_count": len(SAMPLES),
        "pairwise_observer_geometry": pairwise,
        "observer_uniqueness": uniqueness,
        "family_summary": families,
        "summary": summary,
        "status": status,
        "pass_condition": (
            "observer_count >= 10 and family_count >= 5 and "
            "redundant_pair_count >= 2 and medium_pair_count >= 10 and "
            "diverse_pair_count >= 10 and "
            "same_family_medium_or_redundant_count >= 5 and "
            "cross_family_diverse_count >= 5 and "
            "0.20 < average_distance < 0.80"
        ),
        "main_insight": (
            "A shared response feature space can reduce distance saturation "
            "and reveal medium-distance observer relations."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy observer geometry experiment.",
            "Observer response vectors are manually weighted.",
            "Feature-space geometry is heuristic.",
            "Observer families are simplified.",
            "No semantic truth is evaluated.",
            "No universal observer geometry claim is made.",
        ],
        "reproduction_command": (
            "python examples/observer_family_geometry_v2.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION — Observer Family Geometry v2")
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