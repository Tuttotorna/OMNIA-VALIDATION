import json
import math
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

# =============================================================================
# OMNIA-VALIDATION — Observer Family Geometry Adversarial v0
# =============================================================================

VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RESULTS_PATH = RESULTS_DIR / "observer_family_geometry_adversarial_v0.json"

# =============================================================================
# SAMPLE SET
# =============================================================================

BASE_SAMPLES = [
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
    "ABCDABCXABCDABCX",
    "AAAABAAACAAADAAA",
]

DEGENERATE_SAMPLES = [
    "AAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAA",
    "AAAAAAAAAAAAAAAA",
    "BBBBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBBBB",
    "CCCCCCCCCCCCCCCC",
    "CCCCCCCCCCCCCCCC",
]

ALIAS_COLLISION_SAMPLES = [
    "ABABABABABABABAB",
    "1212121212121212",
    "XYXYXYXYXYXYXYXY",
    "0101010101010101",
    "A1A1A1A1A1A1A1A1",
    "B2B2B2B2B2B2B2B2",
    "CDCDCDCDCDCDCDCD",
    "3434343434343434",
]

CHAOTIC_SAMPLES = [
    "AZBYCXDWEVFUGTHS",
    "QWERTYUIOPASDFGH",
    "MNBVCXZLKJHGFDSA",
    "A1B2C3D4E5F6G7H8",
    "ZXCVBNMASDFGHJKL",
    "PLMOKNIJBUHVYGCT",
    "ABCDEFGHHGFEDCBA",
    "AABCDDEEFFFEDCBA",
]

# =============================================================================
# HELPERS
# =============================================================================

def clamp(value):
    return max(0.0, min(1.0, value))


def safe_avg(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


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


# =============================================================================
# FEATURE EXTRACTORS
# =============================================================================

def transition_counts(sequence):
    normalized = normalize_symbols(sequence)
    edges = Counter()

    for i in range(len(normalized) - 1):
        edges[(normalized[i], normalized[i + 1])] += 1

    return edges


def motif_counts(sequence, size):
    normalized = normalize_symbols(sequence)
    motifs = Counter()

    for i in range(len(normalized) - size + 1):
        motifs[normalized[i:i + size]] += 1

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

    return {
        "periodicity_strength": best_score,
        "best_period_norm": best_period / min(8, len(normalized)),
    }


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


def base_common_features(sequence):
    normalized = normalize_symbols(sequence)
    length = len(normalized)
    unique = len(set(normalized))

    transitions = transition_counts(sequence)
    motifs2 = motif_counts(sequence, 2)
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

    repeated_motif2_mass = sum(
        count
        for count in motifs2.values()
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
    run_bucket_total = max(sum(run_buckets.values()), 1)

    return {
        "entropy": normalized_entropy(normalized),
        "unique_ratio": unique / max(length, 1),

        "transition_density": len(transitions) / max(length - 1, 1),
        "transition_repetition": repeated_transition_mass / max(length - 1, 1),

        "motif2_density": len(motifs2) / max(length - 1, 1),
        "motif2_repetition": repeated_motif2_mass / max(length - 1, 1),

        "motif3_density": len(motifs3) / max(length - 2, 1),
        "motif3_repetition": repeated_motif3_mass / max(length - 2, 1),

        "motif4_density": len(motifs4) / max(length - 3, 1),
        "motif4_repetition": repeated_motif4_mass / max(length - 3, 1),

        "run_count_norm": sum(runs.values()) / max(length, 1),
        "max_run_norm": max_run / max(length, 1),

        "run_1_ratio": run_buckets.get("run_1", 0) / run_bucket_total,
        "run_2_3_ratio": run_buckets.get("run_2_3", 0) / run_bucket_total,
        "run_4_7_ratio": run_buckets.get("run_4_7", 0) / run_bucket_total,

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
# BASE OBSERVERS — V3 FAMILY
# =============================================================================

BASE_OBSERVERS = {
    "entropy_profile": {
        "family": "entropy",
        "weights": {
            "entropy": 1.0,
            "unique_ratio": 0.75,
            "transition_density": 0.25,
            "motif3_density": 0.18,
            "run_count_norm": 0.10,
        },
    },
    "entropy_profile_extended": {
        "family": "entropy",
        "weights": {
            "entropy": 1.0,
            "unique_ratio": 0.75,
            "transition_density": 0.30,
            "motif3_density": 0.22,
            "run_count_norm": 0.18,
            "periodicity_strength": 0.12,
        },
    },

    "transition_topology": {
        "family": "transition",
        "weights": {
            "transition_density": 1.0,
            "transition_repetition": 1.0,
            "motif2_density": 0.60,
            "motif2_repetition": 0.60,
            "motif3_density": 0.35,
            "motif3_repetition": 0.35,
            "periodicity_strength": 0.25,
        },
    },
    "transition_topology_soft": {
        "family": "transition",
        "weights": {
            "transition_density": 0.80,
            "transition_repetition": 0.80,
            "motif2_density": 0.45,
            "motif2_repetition": 0.45,
            "motif3_density": 0.35,
            "motif3_repetition": 0.35,
            "entropy": 0.25,
            "unique_ratio": 0.18,
        },
    },
    "transition_topology_windowed": {
        "family": "transition",
        "weights": {
            "transition_density": 0.65,
            "transition_repetition": 0.65,
            "motif2_density": 0.35,
            "motif2_repetition": 0.35,
            "periodicity_strength": 0.45,
            "best_period_norm": 0.30,
            "mirror_similarity": 0.18,
        },
    },

    "motif3": {
        "family": "motif",
        "weights": {
            "motif3_density": 1.0,
            "motif3_repetition": 1.0,
            "motif2_density": 0.45,
            "motif2_repetition": 0.45,
            "transition_density": 0.35,
            "transition_repetition": 0.35,
            "periodicity_strength": 0.22,
        },
    },
    "motif3_soft": {
        "family": "motif",
        "weights": {
            "motif3_density": 0.70,
            "motif3_repetition": 0.70,
            "motif2_density": 0.35,
            "motif2_repetition": 0.35,
            "entropy": 0.30,
            "unique_ratio": 0.20,
            "transition_density": 0.30,
        },
    },
    "motif4": {
        "family": "motif",
        "weights": {
            "motif4_density": 1.0,
            "motif4_repetition": 1.0,
            "motif3_density": 0.55,
            "motif3_repetition": 0.55,
            "transition_density": 0.18,
        },
    },
    "motif_bridge": {
        "family": "motif",
        "weights": {
            "motif2_density": 0.65,
            "motif2_repetition": 0.65,
            "motif3_density": 0.55,
            "motif3_repetition": 0.55,
            "transition_density": 0.55,
            "transition_repetition": 0.55,
            "entropy": 0.25,
        },
    },

    "run_length_profile": {
        "family": "run_length",
        "weights": {
            "run_count_norm": 1.0,
            "max_run_norm": 1.0,
            "run_1_ratio": 0.85,
            "run_2_3_ratio": 0.85,
            "run_4_7_ratio": 0.85,
        },
    },
    "run_length_profile_soft": {
        "family": "run_length",
        "weights": {
            "run_count_norm": 0.70,
            "max_run_norm": 0.70,
            "run_1_ratio": 0.55,
            "run_2_3_ratio": 0.55,
            "entropy": 0.28,
            "unique_ratio": 0.20,
            "transition_density": 0.18,
        },
    },
    "run_transition_bridge": {
        "family": "run_length",
        "weights": {
            "run_count_norm": 0.50,
            "max_run_norm": 0.50,
            "run_1_ratio": 0.45,
            "transition_density": 0.45,
            "transition_repetition": 0.45,
            "motif2_density": 0.25,
            "entropy": 0.20,
        },
    },

    "symbol_pattern": {
        "family": "symbol",
        "weights": {
            "unique_ratio": 1.0,
            "entropy": 0.80,
            "transition_density": 0.25,
            "motif3_density": 0.20,
            "run_count_norm": 0.10,
        },
    },
    "symbol_pattern_soft": {
        "family": "symbol",
        "weights": {
            "unique_ratio": 0.70,
            "entropy": 0.60,
            "transition_density": 0.30,
            "run_count_norm": 0.25,
            "motif2_density": 0.20,
        },
    },

    "symmetry_profile": {
        "family": "symmetry",
        "weights": {
            "mirror_similarity": 1.0,
            "periodicity_strength": 0.45,
            "best_period_norm": 0.30,
            "transition_repetition": 0.18,
        },
    },
    "periodicity_profile": {
        "family": "symmetry",
        "weights": {
            "periodicity_strength": 1.0,
            "best_period_norm": 0.85,
            "mirror_similarity": 0.35,
            "transition_repetition": 0.30,
            "motif2_repetition": 0.20,
        },
    },
    "periodic_transition_bridge": {
        "family": "symmetry",
        "weights": {
            "periodicity_strength": 0.70,
            "best_period_norm": 0.45,
            "transition_density": 0.45,
            "transition_repetition": 0.45,
            "motif2_repetition": 0.35,
            "mirror_similarity": 0.25,
        },
    },
}

# =============================================================================
# ADVERSARIAL OBSERVER CONSTRUCTIONS
# =============================================================================

def make_duplicate_observers(observers):
    output = deepcopy(observers)

    output["entropy_profile_clone_A"] = deepcopy(output["entropy_profile"])
    output["entropy_profile_clone_B"] = deepcopy(output["entropy_profile"])

    output["transition_topology_clone_A"] = deepcopy(output["transition_topology"])
    output["transition_topology_clone_B"] = deepcopy(output["transition_topology"])

    output["motif3_clone_A"] = deepcopy(output["motif3"])
    output["motif3_clone_B"] = deepcopy(output["motif3"])

    return output


def make_family_imbalance_observers(observers):
    output = deepcopy(observers)

    source = output["transition_topology"]

    for index in range(10):
        name = f"transition_clone_family_pressure_{index:02d}"
        output[name] = deepcopy(source)

    return output


def make_fake_bridge_observers(observers):
    output = deepcopy(observers)

    output["fake_bridge_entropy_transition"] = {
        "family": "fake_bridge",
        "weights": {
            "entropy": 0.75,
            "unique_ratio": 0.60,
            "transition_density": 0.75,
            "transition_repetition": 0.75,
            "motif2_density": 0.55,
            "periodicity_strength": 0.45,
        },
    }

    output["fake_bridge_symbol_motif"] = {
        "family": "fake_bridge",
        "weights": {
            "unique_ratio": 0.75,
            "entropy": 0.65,
            "motif3_density": 0.75,
            "motif3_repetition": 0.75,
            "motif4_density": 0.40,
        },
    }

    output["fake_bridge_run_symmetry"] = {
        "family": "fake_bridge",
        "weights": {
            "run_count_norm": 0.65,
            "max_run_norm": 0.65,
            "periodicity_strength": 0.60,
            "mirror_similarity": 0.60,
            "best_period_norm": 0.45,
        },
    }

    return output


def make_observer_collapse(observers):
    output = {}

    collapsed_weights = {
        "entropy": 1.0,
        "unique_ratio": 1.0,
        "transition_density": 1.0,
        "motif3_density": 1.0,
        "periodicity_strength": 1.0,
        "run_count_norm": 1.0,
    }

    for name, data in observers.items():
        output[name] = {
            "family": data["family"],
            "weights": deepcopy(collapsed_weights),
        }

    return output


def make_sparse_observers(observers):
    output = {}

    keep = [
        "entropy_profile",
        "transition_topology",
        "motif3",
        "run_length_profile",
        "symbol_pattern",
        "symmetry_profile",
    ]

    for name in keep:
        output[name] = deepcopy(observers[name])

    return output


# =============================================================================
# GEOMETRY CORE
# =============================================================================

def observer_response(observer_name, observers, samples):
    observer = observers[observer_name]
    weights = observer["weights"]

    vectors = []

    for sample in samples:
        vectors.append(
            weighted_common_vector(sample, weights)
        )

    aggregate = {}
    feature_names = sorted(base_common_features(samples[0]).keys())

    for feature in feature_names:
        values = [
            vector.get(feature, 0.0)
            for vector in vectors
        ]

        mean_value = safe_avg(values)

        variance = safe_avg([
            (value - mean_value) ** 2
            for value in values
        ])

        aggregate[f"mean_{feature}"] = mean_value
        aggregate[f"var_{feature}"] = variance

    return aggregate


def observer_similarity(observer_a, observer_b, observers, samples):
    response_a = observer_response(observer_a, observers, samples)
    response_b = observer_response(observer_b, observers, samples)

    raw_similarity = cosine_similarity(response_a, response_b)

    smoothed_similarity = 0.08 + 0.92 * raw_similarity

    return clamp(smoothed_similarity)


def observer_distance(observer_a, observer_b, observers, samples):
    return 1.0 - observer_similarity(
        observer_a,
        observer_b,
        observers,
        samples,
    )


def classify_relation(distance, thresholds):
    if distance <= thresholds["redundant"]:
        return "redundant"

    if distance <= thresholds["medium"]:
        return "medium"

    return "diverse"


def compute_pairwise_geometry(observers, samples, thresholds):
    pairs = []

    for observer_a, observer_b in combinations(sorted(observers.keys()), 2):
        similarity = observer_similarity(
            observer_a,
            observer_b,
            observers,
            samples,
        )

        distance = 1.0 - similarity

        family_a = observers[observer_a]["family"]
        family_b = observers[observer_b]["family"]

        pair_type = (
            "same_family"
            if family_a == family_b
            else "cross_family"
        )

        pairs.append({
            "pair_key": f"{observer_a}::{observer_b}",
            "left": observer_a,
            "right": observer_b,
            "left_family": family_a,
            "right_family": family_b,
            "pair_type": pair_type,
            "similarity": round(similarity, 12),
            "distance": round(distance, 12),
            "relation": classify_relation(distance, thresholds),
        })

    return pairs


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

    cross_family_redundant = [
        pair
        for pair in pairwise
        if (
            pair["pair_type"] == "cross_family"
            and pair["relation"] == "redundant"
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
        "cross_family_redundant_count": len(cross_family_redundant),
    }


def observer_uniqueness(pairwise, observers):
    uniqueness = {}

    for name in sorted(observers.keys()):
        distances = [
            pair["distance"]
            for pair in pairwise
            if pair["left"] == name or pair["right"] == name
        ]

        uniqueness[name] = round(
            safe_avg(distances),
            12,
        )

    return uniqueness


def geometry_continuity_index(summary):
    pair_count = summary["pair_count"]

    if pair_count == 0:
        return 0.0

    return round(
        summary["medium_pair_count"] / pair_count,
        12,
    )


def observer_relation_entropy(summary):
    counts = [
        summary["redundant_pair_count"],
        summary["medium_pair_count"],
        summary["diverse_pair_count"],
    ]

    total = sum(counts)

    if total == 0:
        return 0.0

    probs = [
        count / total
        for count in counts
        if count > 0
    ]

    raw = -sum(
        p * math.log2(p)
        for p in probs
    )

    return round(raw / math.log2(3), 12)


def summarize_geometry(pairwise, observers):
    distances = [
        pair["distance"]
        for pair in pairwise
    ]

    relations = relation_summary(pairwise)
    uniqueness = observer_uniqueness(pairwise, observers)

    unique_observers = [
        name
        for name, value in uniqueness.items()
        if value >= 0.30
    ]

    redundant_observers = [
        name
        for name, value in uniqueness.items()
        if value <= 0.20
    ]

    summary = {
        "observer_count": len(observers),
        "family_count": len(
            set(observer["family"] for observer in observers.values())
        ),
        "pair_count": len(pairwise),
        "average_distance": round(safe_avg(distances), 12),
        "min_distance": round(min(distances), 12) if distances else 0.0,
        "max_distance": round(max(distances), 12) if distances else 0.0,
        **relations,
        "unique_observer_count": len(unique_observers),
        "redundant_observer_count": len(redundant_observers),
        "unique_observers": unique_observers,
        "redundant_observers": redundant_observers,
    }

    summary["geometry_continuity_index"] = geometry_continuity_index(summary)
    summary["observer_relation_entropy"] = observer_relation_entropy(summary)

    return summary, uniqueness


def family_summary(pairwise, observers):
    families = sorted(
        set(observer["family"] for observer in observers.values())
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

        output[family] = {
            "observer_count": sum(
                1
                for observer in observers.values()
                if observer["family"] == family
            ),
            "same_family_pair_count": len(same_family_pairs),
            "cross_family_pair_count": len(cross_family_pairs),
            "same_family_avg_distance": round(
                safe_avg([pair["distance"] for pair in same_family_pairs]),
                12,
            ) if same_family_pairs else None,
            "cross_family_avg_distance": round(
                safe_avg([pair["distance"] for pair in cross_family_pairs]),
                12,
            ) if cross_family_pairs else None,
        }

    return output


def run_geometry(config_name, samples, observers, thresholds):
    pairwise = compute_pairwise_geometry(
        observers,
        samples,
        thresholds,
    )

    summary, uniqueness = summarize_geometry(
        pairwise,
        observers,
    )

    families = family_summary(
        pairwise,
        observers,
    )

    return {
        "config_name": config_name,
        "sample_count": len(samples),
        "observer_count": len(observers),
        "thresholds": thresholds,
        "summary": summary,
        "observer_uniqueness": uniqueness,
        "family_summary": families,
        "pairwise_observer_geometry": pairwise,
    }


# =============================================================================
# ADVERSARIAL ANALYSIS
# =============================================================================

def pair_relation_map(run):
    return {
        pair["pair_key"]: pair["relation"]
        for pair in run["pairwise_observer_geometry"]
    }


def pair_distance_map(run):
    return {
        pair["pair_key"]: pair["distance"]
        for pair in run["pairwise_observer_geometry"]
    }


def compare_to_baseline(baseline, run):
    baseline_relations = pair_relation_map(baseline)
    run_relations = pair_relation_map(run)

    baseline_distances = pair_distance_map(baseline)
    run_distances = pair_distance_map(run)

    shared_keys = sorted(
        set(baseline_relations.keys()) & set(run_relations.keys())
    )

    if not shared_keys:
        return {
            "shared_pair_count": 0,
            "relation_persistence": 0.0,
            "average_distance_drift": 1.0,
            "mean_pair_distance_drift": 1.0,
            "max_pair_distance_drift": 1.0,
            "continuity_drift": 1.0,
            "relation_entropy_drift": 1.0,
        }

    stable_relations = sum(
        1
        for key in shared_keys
        if baseline_relations[key] == run_relations[key]
    )

    distance_drifts = [
        abs(baseline_distances[key] - run_distances[key])
        for key in shared_keys
    ]

    baseline_summary = baseline["summary"]
    run_summary = run["summary"]

    return {
        "shared_pair_count": len(shared_keys),
        "relation_persistence": round(
            stable_relations / len(shared_keys),
            12,
        ),
        "average_distance_drift": round(
            abs(
                baseline_summary["average_distance"]
                - run_summary["average_distance"]
            ),
            12,
        ),
        "mean_pair_distance_drift": round(
            safe_avg(distance_drifts),
            12,
        ),
        "max_pair_distance_drift": round(
            max(distance_drifts),
            12,
        ),
        "continuity_drift": round(
            abs(
                baseline_summary["geometry_continuity_index"]
                - run_summary["geometry_continuity_index"]
            ),
            12,
        ),
        "relation_entropy_drift": round(
            abs(
                baseline_summary["observer_relation_entropy"]
                - run_summary["observer_relation_entropy"]
            ),
            12,
        ),
        "medium_pair_count_drift": abs(
            baseline_summary["medium_pair_count"]
            - run_summary["medium_pair_count"]
        ),
        "redundant_pair_count_drift": abs(
            baseline_summary["redundant_pair_count"]
            - run_summary["redundant_pair_count"]
        ),
        "diverse_pair_count_drift": abs(
            baseline_summary["diverse_pair_count"]
            - run_summary["diverse_pair_count"]
        ),
    }


def attack_score(baseline, run, comparison):
    summary = run["summary"]
    baseline_summary = baseline["summary"]

    redundant_growth = (
        summary["redundant_pair_count"]
        - baseline_summary["redundant_pair_count"]
    )

    entropy_loss = (
        baseline_summary["observer_relation_entropy"]
        - summary["observer_relation_entropy"]
    )

    continuity_loss = abs(
        baseline_summary["geometry_continuity_index"]
        - summary["geometry_continuity_index"]
    )

    avg_distance_drift = comparison["average_distance_drift"]

    cross_family_redundant_growth = summary["cross_family_redundant_count"]

    raw = (
        max(0, redundant_growth) * 0.015
        + max(0.0, entropy_loss) * 0.60
        + continuity_loss * 0.50
        + avg_distance_drift * 0.50
        + cross_family_redundant_growth * 0.01
    )

    return round(raw, 12)


def classify_attack_outcome(score):
    if score >= 0.80:
        return "COLLAPSE"

    if score >= 0.45:
        return "WEAKENED"

    if score >= 0.20:
        return "STRESSED"

    return "RESISTED"


def aggregate_adversarial_results(adversarial_results):
    attack_scores = [
        result["attack_score"]
        for result in adversarial_results
    ]

    outcomes = Counter(
        result["attack_outcome"]
        for result in adversarial_results
    )

    resisted_count = outcomes.get("RESISTED", 0)
    stressed_count = outcomes.get("STRESSED", 0)
    weakened_count = outcomes.get("WEAKENED", 0)
    collapse_count = outcomes.get("COLLAPSE", 0)

    return {
        "attack_count": len(adversarial_results),
        "mean_attack_score": round(safe_avg(attack_scores), 12),
        "max_attack_score": round(max(attack_scores), 12),
        "resisted_count": resisted_count,
        "stressed_count": stressed_count,
        "weakened_count": weakened_count,
        "collapse_count": collapse_count,
        "non_collapse_count": resisted_count + stressed_count + weakened_count,
    }


def pass_condition(summary):
    return (
        summary["collapse_count"] >= 1
        and summary["resisted_count"] >= 1
        and summary["max_attack_score"] >= 0.80
        and summary["mean_attack_score"] >= 0.20
    )


# =============================================================================
# MAIN
# =============================================================================

def main():
    thresholds = {
        "redundant": 0.20,
        "medium": 0.60,
    }

    configurations = [
        {
            "config_name": "base",
            "samples": BASE_SAMPLES,
            "observers": BASE_OBSERVERS,
            "thresholds": thresholds,
        },
        {
            "config_name": "degenerate_samples",
            "samples": DEGENERATE_SAMPLES,
            "observers": BASE_OBSERVERS,
            "thresholds": thresholds,
        },
        {
            "config_name": "alias_collision_samples",
            "samples": ALIAS_COLLISION_SAMPLES,
            "observers": BASE_OBSERVERS,
            "thresholds": thresholds,
        },
        {
            "config_name": "chaotic_samples",
            "samples": CHAOTIC_SAMPLES,
            "observers": BASE_OBSERVERS,
            "thresholds": thresholds,
        },
        {
            "config_name": "duplicate_observers",
            "samples": BASE_SAMPLES,
            "observers": make_duplicate_observers(BASE_OBSERVERS),
            "thresholds": thresholds,
        },
        {
            "config_name": "family_imbalance_observers",
            "samples": BASE_SAMPLES,
            "observers": make_family_imbalance_observers(BASE_OBSERVERS),
            "thresholds": thresholds,
        },
        {
            "config_name": "fake_bridge_observers",
            "samples": BASE_SAMPLES,
            "observers": make_fake_bridge_observers(BASE_OBSERVERS),
            "thresholds": thresholds,
        },
        {
            "config_name": "observer_collapse",
            "samples": BASE_SAMPLES,
            "observers": make_observer_collapse(BASE_OBSERVERS),
            "thresholds": thresholds,
        },
        {
            "config_name": "sparse_observers",
            "samples": BASE_SAMPLES,
            "observers": make_sparse_observers(BASE_OBSERVERS),
            "thresholds": thresholds,
        },
    ]

    runs = []

    for config in configurations:
        runs.append(
            run_geometry(
                config["config_name"],
                config["samples"],
                deepcopy(config["observers"]),
                config["thresholds"],
            )
        )

    baseline = runs[0]

    adversarial_results = []

    for run in runs[1:]:
        comparison = compare_to_baseline(
            baseline,
            run,
        )

        score = attack_score(
            baseline,
            run,
            comparison,
        )

        outcome = classify_attack_outcome(score)

        adversarial_results.append({
            "config_name": run["config_name"],
            "attack_score": score,
            "attack_outcome": outcome,
            "comparison_to_baseline": comparison,
            "summary": run["summary"],
        })

    adversarial_summary = aggregate_adversarial_results(
        adversarial_results
    )

    status = (
        "PASS"
        if pass_condition(adversarial_summary)
        else "FAIL"
    )

    output = {
        "experiment_name": "observer_family_geometry_adversarial_v0",
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "observer_family_geometry_adversarial",
        "purpose": (
            "Test whether observer-family geometry exposes measurable "
            "failure boundaries under adversarial observer and sample "
            "constructions."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "baseline_config": "base",
        "run_count": len(runs),
        "attack_count": len(adversarial_results),
        "baseline_summary": baseline["summary"],
        "runs": runs,
        "adversarial_results": adversarial_results,
        "adversarial_summary": adversarial_summary,
        "status": status,
        "pass_condition": (
            "collapse_count >= 1 and resisted_count >= 1 and "
            "max_attack_score >= 0.80 and mean_attack_score >= 0.20"
        ),
        "main_insight": (
            "A useful observer geometry should not only pass stability tests; "
            "it should also expose measurable collapse regions under "
            "adversarial pressure."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy adversarial geometry experiment.",
            "Attack score is heuristic.",
            "Adversarial cases are synthetic.",
            "Observer weights are manually chosen.",
            "No semantic truth is evaluated.",
            "No universal adversarial robustness claim is made.",
        ],
        "reproduction_command": (
            "python examples/observer_family_geometry_adversarial_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION — Observer Family Geometry Adversarial v0")
    print("=" * 80)

    print(f"Status: {status}")
    print(f"Version: {VERSION}")
    print()

    print("Baseline summary:")
    print(f"  Observer count:              {baseline['summary']['observer_count']}")
    print(f"  Pair count:                  {baseline['summary']['pair_count']}")
    print(f"  Average distance:            {baseline['summary']['average_distance']}")
    print(f"  Redundant pair count:        {baseline['summary']['redundant_pair_count']}")
    print(f"  Medium pair count:           {baseline['summary']['medium_pair_count']}")
    print(f"  Diverse pair count:          {baseline['summary']['diverse_pair_count']}")
    print(f"  Geometry continuity index:   {baseline['summary']['geometry_continuity_index']}")
    print(f"  Observer relation entropy:   {baseline['summary']['observer_relation_entropy']}")
    print()

    print("Adversarial summary:")
    for key, value in adversarial_summary.items():
        print(f"  {key:<28} {value}")

    print()
    print("Adversarial results:")
    for result in adversarial_results:
        comparison = result["comparison_to_baseline"]
        summary = result["summary"]

        print(
            f"  {result['config_name']:<28} "
            f"outcome={result['attack_outcome']:<9} "
            f"score={result['attack_score']} "
            f"persistence={comparison['relation_persistence']} "
            f"avg_drift={comparison['average_distance_drift']} "
            f"red={summary['redundant_pair_count']} "
            f"med={summary['medium_pair_count']} "
            f"div={summary['diverse_pair_count']} "
            f"entropy={summary['observer_relation_entropy']}"
        )

    print()
    print("Run summaries:")
    for run in runs:
        summary = run["summary"]

        print(
            f"  {run['config_name']:<28} "
            f"obs={summary['observer_count']} "
            f"pairs={summary['pair_count']} "
            f"avg_dist={summary['average_distance']} "
            f"red={summary['redundant_pair_count']} "
            f"med={summary['medium_pair_count']} "
            f"div={summary['diverse_pair_count']} "
            f"gci={summary['geometry_continuity_index']} "
            f"entropy={summary['observer_relation_entropy']} "
            f"cross_red={summary['cross_family_redundant_count']}"
        )

    print()
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()