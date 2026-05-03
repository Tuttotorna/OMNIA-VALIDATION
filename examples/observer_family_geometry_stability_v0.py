import json
import math
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

# =============================================================================
# OMNIA-VALIDATION — Observer Family Geometry Stability v0
# =============================================================================

VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RESULTS_PATH = RESULTS_DIR / "observer_family_geometry_stability_v0.json"

# =============================================================================
# BASE SAMPLE SET
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


def safe_avg(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


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
# OBSERVER FAMILY — SAME DESIGN AS V3
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
# PERTURBATIONS
# =============================================================================

def mutate_sequence(sequence):
    if len(sequence) < 4:
        return sequence

    chars = list(sequence)
    middle = len(chars) // 2

    chars[middle] = "Z" if chars[middle] != "Z" else "Y"

    return "".join(chars)


def rotate_sequence(sequence):
    if not sequence:
        return sequence

    shift = max(1, len(sequence) // 4)

    return sequence[shift:] + sequence[:shift]


def remove_every_fourth(sequence):
    return "".join(
        char
        for index, char in enumerate(sequence)
        if (index + 1) % 4 != 0
    )


def perturb_samples(samples, mode):
    if mode == "base":
        return list(samples)

    if mode == "mutated":
        return [
            mutate_sequence(sample)
            for sample in samples
        ]

    if mode == "rotated":
        return [
            rotate_sequence(sample)
            for sample in samples
        ]

    if mode == "reduced":
        return [
            sample
            for index, sample in enumerate(samples)
            if index % 4 != 0
        ]

    if mode == "compressed":
        return [
            remove_every_fourth(sample)
            for sample in samples
        ]

    raise ValueError(f"Unknown sample perturbation mode: {mode}")


def perturb_observers(observers, mode):
    output = deepcopy(observers)

    if mode == "base":
        return output

    if mode == "remove_bridges":
        for name in [
            "motif_bridge",
            "run_transition_bridge",
            "periodic_transition_bridge",
        ]:
            output.pop(name, None)

        return output

    if mode == "remove_soft":
        for name in list(output.keys()):
            if "soft" in name:
                output.pop(name, None)

        return output

    if mode == "weight_down":
        for data in output.values():
            for key in data["weights"]:
                data["weights"][key] *= 0.85

        return output

    if mode == "weight_up":
        for data in output.values():
            for key in data["weights"]:
                data["weights"][key] *= 1.15

        return output

    raise ValueError(f"Unknown observer perturbation mode: {mode}")


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

    return {
        "redundant_pair_count": counts.get("redundant", 0),
        "medium_pair_count": counts.get("medium", 0),
        "diverse_pair_count": counts.get("diverse", 0),
        "same_family_medium_or_redundant_count": len(
            same_family_medium_or_redundant
        ),
        "cross_family_diverse_count": len(cross_family_diverse),
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
# STABILITY ANALYSIS
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
            "max_distance_drift": 1.0,
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
        "max_distance_drift": round(
            max(distance_drifts),
            12,
        ),
        "mean_pair_distance_drift": round(
            safe_avg(distance_drifts),
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


def aggregate_stability(comparisons):
    values = {
        "relation_persistence": [],
        "average_distance_drift": [],
        "mean_pair_distance_drift": [],
        "continuity_drift": [],
        "relation_entropy_drift": [],
    }

    for comparison in comparisons:
        for key in values:
            values[key].append(comparison[key])

    return {
        "mean_relation_persistence": round(
            safe_avg(values["relation_persistence"]),
            12,
        ),
        "min_relation_persistence": round(
            min(values["relation_persistence"]),
            12,
        ),
        "mean_average_distance_drift": round(
            safe_avg(values["average_distance_drift"]),
            12,
        ),
        "max_average_distance_drift": round(
            max(values["average_distance_drift"]),
            12,
        ),
        "mean_pair_distance_drift": round(
            safe_avg(values["mean_pair_distance_drift"]),
            12,
        ),
        "mean_continuity_drift": round(
            safe_avg(values["continuity_drift"]),
            12,
        ),
        "max_continuity_drift": round(
            max(values["continuity_drift"]),
            12,
        ),
        "mean_relation_entropy_drift": round(
            safe_avg(values["relation_entropy_drift"]),
            12,
        ),
        "max_relation_entropy_drift": round(
            max(values["relation_entropy_drift"]),
            12,
        ),
    }


def pass_condition(stability_summary):
    return (
        stability_summary["mean_relation_persistence"] >= 0.65
        and stability_summary["min_relation_persistence"] >= 0.40
        and stability_summary["mean_average_distance_drift"] <= 0.12
        and stability_summary["mean_continuity_drift"] <= 0.12
        and stability_summary["mean_relation_entropy_drift"] <= 0.15
    )


# =============================================================================
# MAIN
# =============================================================================

def main():
    base_thresholds = {
        "redundant": 0.20,
        "medium": 0.60,
    }

    configurations = [
        {
            "config_name": "base",
            "sample_mode": "base",
            "observer_mode": "base",
            "thresholds": base_thresholds,
        },
        {
            "config_name": "sample_mutated",
            "sample_mode": "mutated",
            "observer_mode": "base",
            "thresholds": base_thresholds,
        },
        {
            "config_name": "sample_rotated",
            "sample_mode": "rotated",
            "observer_mode": "base",
            "thresholds": base_thresholds,
        },
        {
            "config_name": "sample_reduced",
            "sample_mode": "reduced",
            "observer_mode": "base",
            "thresholds": base_thresholds,
        },
        {
            "config_name": "sample_compressed",
            "sample_mode": "compressed",
            "observer_mode": "base",
            "thresholds": base_thresholds,
        },
        {
            "config_name": "remove_bridges",
            "sample_mode": "base",
            "observer_mode": "remove_bridges",
            "thresholds": base_thresholds,
        },
        {
            "config_name": "remove_soft_observers",
            "sample_mode": "base",
            "observer_mode": "remove_soft",
            "thresholds": base_thresholds,
        },
        {
            "config_name": "weights_down",
            "sample_mode": "base",
            "observer_mode": "weight_down",
            "thresholds": base_thresholds,
        },
        {
            "config_name": "weights_up",
            "sample_mode": "base",
            "observer_mode": "weight_up",
            "thresholds": base_thresholds,
        },
        {
            "config_name": "threshold_tighter",
            "sample_mode": "base",
            "observer_mode": "base",
            "thresholds": {
                "redundant": 0.18,
                "medium": 0.55,
            },
        },
        {
            "config_name": "threshold_looser",
            "sample_mode": "base",
            "observer_mode": "base",
            "thresholds": {
                "redundant": 0.22,
                "medium": 0.65,
            },
        },
    ]

    runs = []

    for config in configurations:
        samples = perturb_samples(
            BASE_SAMPLES,
            config["sample_mode"],
        )

        observers = perturb_observers(
            BASE_OBSERVERS,
            config["observer_mode"],
        )

        run = run_geometry(
            config["config_name"],
            samples,
            observers,
            config["thresholds"],
        )

        runs.append(run)

    baseline = runs[0]

    comparisons = []

    for run in runs[1:]:
        comparison = compare_to_baseline(
            baseline,
            run,
        )

        comparison["config_name"] = run["config_name"]
        comparisons.append(comparison)

    stability_summary = aggregate_stability(comparisons)
    status = "PASS" if pass_condition(stability_summary) else "FAIL"

    output = {
        "experiment_name": "observer_family_geometry_stability_v0",
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "observer_family_geometry_stability",
        "purpose": (
            "Test whether observer-family geometry remains stable under "
            "sample perturbation, observer removal, weight variation, and "
            "threshold sweep."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "baseline_config": "base",
        "run_count": len(runs),
        "comparison_count": len(comparisons),
        "baseline_summary": baseline["summary"],
        "runs": runs,
        "comparisons_to_baseline": comparisons,
        "stability_summary": stability_summary,
        "status": status,
        "pass_condition": (
            "mean_relation_persistence >= 0.65 and "
            "min_relation_persistence >= 0.40 and "
            "mean_average_distance_drift <= 0.12 and "
            "mean_continuity_drift <= 0.12 and "
            "mean_relation_entropy_drift <= 0.15"
        ),
        "main_insight": (
            "Observer-space geometry must be evaluated by persistence under "
            "perturbation, not by a single successful geometry run."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy stability experiment.",
            "Perturbations are synthetic.",
            "Observer weights are manually chosen.",
            "Threshold sweeps are limited.",
            "No semantic truth is evaluated.",
            "No universal observer stability claim is made.",
        ],
        "reproduction_command": (
            "python examples/observer_family_geometry_stability_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION — Observer Family Geometry Stability v0")
    print("=" * 80)

    print(f"Status: {status}")
    print(f"Version: {VERSION}")
    print()

    print("Baseline summary:")
    print(f"  Observer count:                  {baseline['summary']['observer_count']}")
    print(f"  Pair count:                      {baseline['summary']['pair_count']}")
    print(f"  Average distance:                {baseline['summary']['average_distance']}")
    print(f"  Redundant pair count:            {baseline['summary']['redundant_pair_count']}")
    print(f"  Medium pair count:               {baseline['summary']['medium_pair_count']}")
    print(f"  Diverse pair count:              {baseline['summary']['diverse_pair_count']}")
    print(f"  Geometry continuity index:       {baseline['summary']['geometry_continuity_index']}")
    print(f"  Observer relation entropy:       {baseline['summary']['observer_relation_entropy']}")
    print()

    print("Stability summary:")
    for key, value in stability_summary.items():
        print(f"  {key:<32} {value}")

    print()
    print("Comparisons to baseline:")
    for comparison in comparisons:
        print(
            f"  {comparison['config_name']:<24} "
            f"persistence={comparison['relation_persistence']} "
            f"avg_drift={comparison['average_distance_drift']} "
            f"pair_drift={comparison['mean_pair_distance_drift']} "
            f"continuity_drift={comparison['continuity_drift']} "
            f"entropy_drift={comparison['relation_entropy_drift']}"
        )

    print()
    print("Run summaries:")
    for run in runs:
        summary = run["summary"]

        print(
            f"  {run['config_name']:<24} "
            f"obs={summary['observer_count']} "
            f"pairs={summary['pair_count']} "
            f"avg_dist={summary['average_distance']} "
            f"red={summary['redundant_pair_count']} "
            f"med={summary['medium_pair_count']} "
            f"div={summary['diverse_pair_count']} "
            f"gci={summary['geometry_continuity_index']} "
            f"entropy={summary['observer_relation_entropy']}"
        )

    print()
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()