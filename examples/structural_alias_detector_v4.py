import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


VERSION = "0.4.0"

DATASET_PATH = Path("data/structural_benchmark_dataset_v0.jsonl")
RESULTS_PATH = Path("results/structural_alias_detector_v4.json")


# =============================================================================
# TOKENIZATION / CANONICALIZATION
# =============================================================================


def tokenize(text):
    text = (
        text.replace("|", " ")
        .replace(",", " ")
        .replace(";", " ")
        .replace(":", " ")
        .replace("/", " ")
        .replace("\\", " ")
        .replace("\n", " ")
        .replace("\t", " ")
    )

    return [token.strip() for token in text.split() if token.strip()]


def canonicalize(tokens):
    mapping = {}
    next_id = 0
    output = []

    for token in tokens:
        if token not in mapping:
            mapping[token] = str(next_id)
            next_id += 1

        output.append(mapping[token])

    return output


# =============================================================================
# STRUCTURAL FEATURES
# =============================================================================


def transition_distribution(sequence):
    counts = Counter()

    if len(sequence) < 2:
        return {}

    for i in range(len(sequence) - 1):
        edge = (sequence[i], sequence[i + 1])
        counts[edge] += 1

    total = sum(counts.values())

    return {
        edge: count / total
        for edge, count in counts.items()
    }


def motif_distribution(sequence, width):
    counts = Counter()

    if len(sequence) < width:
        return {}

    for i in range(len(sequence) - width + 1):
        motif = tuple(sequence[i:i + width])
        counts[motif] += 1

    total = sum(counts.values())

    return {
        motif: count / total
        for motif, count in counts.items()
    }


def cardinality_profile(sequence):
    if not sequence:
        return {
            "length": 0,
            "unique": 0,
            "unique_ratio": 0.0,
        }

    unique = len(set(sequence))

    return {
        "length": len(sequence),
        "unique": unique,
        "unique_ratio": unique / len(sequence),
    }


# =============================================================================
# FUZZY COMPARISON
# =============================================================================


def distribution_overlap(dist_a, dist_b):
    keys = set(dist_a.keys()) | set(dist_b.keys())

    if not keys:
        return 1.0

    overlap = 0.0

    for key in keys:
        overlap += min(
            dist_a.get(key, 0.0),
            dist_b.get(key, 0.0),
        )

    return overlap


def normalized_length_similarity(len_a, len_b):
    if len_a == 0 and len_b == 0:
        return 1.0

    return min(len_a, len_b) / max(len_a, len_b)


def cardinality_similarity(profile_a, profile_b):
    unique_a = profile_a["unique"]
    unique_b = profile_b["unique"]

    if unique_a == 0 and unique_b == 0:
        unique_score = 1.0
    else:
        unique_score = min(unique_a, unique_b) / max(unique_a, unique_b)

    ratio_gap = abs(
        profile_a["unique_ratio"]
        - profile_b["unique_ratio"]
    )

    ratio_score = max(0.0, 1.0 - ratio_gap)

    return 0.5 * unique_score + 0.5 * ratio_score


def entropy_of_distribution(dist):
    if not dist:
        return 0.0

    entropy = 0.0

    for value in dist.values():
        if value <= 0:
            continue

        entropy -= value * math.log2(value)

    return entropy


def entropy_similarity(dist_a, dist_b):
    entropy_a = entropy_of_distribution(dist_a)
    entropy_b = entropy_of_distribution(dist_b)

    if entropy_a == 0 and entropy_b == 0:
        return 1.0

    return min(entropy_a, entropy_b) / max(entropy_a, entropy_b)


def fuzzy_transition_similarity(seq_a, seq_b):
    trans_a = transition_distribution(seq_a)
    trans_b = transition_distribution(seq_b)

    motif2_a = motif_distribution(seq_a, 2)
    motif2_b = motif_distribution(seq_b, 2)

    motif3_a = motif_distribution(seq_a, 3)
    motif3_b = motif_distribution(seq_b, 3)

    profile_a = cardinality_profile(seq_a)
    profile_b = cardinality_profile(seq_b)

    transition_overlap = distribution_overlap(trans_a, trans_b)
    motif2_overlap = distribution_overlap(motif2_a, motif2_b)
    motif3_overlap = distribution_overlap(motif3_a, motif3_b)

    length_score = normalized_length_similarity(
        profile_a["length"],
        profile_b["length"],
    )

    cardinality_score = cardinality_similarity(
        profile_a,
        profile_b,
    )

    entropy_score = entropy_similarity(
        trans_a,
        trans_b,
    )

    score = (
        0.35 * transition_overlap
        + 0.20 * motif2_overlap
        + 0.15 * motif3_overlap
        + 0.10 * length_score
        + 0.10 * cardinality_score
        + 0.10 * entropy_score
    )

    return {
        "transition_overlap": round(transition_overlap, 12),
        "motif2_overlap": round(motif2_overlap, 12),
        "motif3_overlap": round(motif3_overlap, 12),
        "length_score": round(length_score, 12),
        "cardinality_score": round(cardinality_score, 12),
        "entropy_score": round(entropy_score, 12),
        "fuzzy_similarity": round(score, 12),
    }


# =============================================================================
# CLASSIFICATION
# =============================================================================


def expected_behavior(pair_type):
    if pair_type in {
        "STRUCTURAL_EQUIVALENT",
        "STRUCTURAL_NEAR_EQUIVALENT",
        "FALSE_SPLIT_TRAP",
    }:
        return "high_similarity"

    if pair_type in {
        "STRUCTURAL_DIFFERENT",
        "FALSE_MERGE_TRAP",
    }:
        return "low_similarity"

    if pair_type == "PARTIAL_DRIFT":
        return "medium_similarity"

    return "unknown"


def observed_behavior(score):
    if score >= 0.70:
        return "high_similarity"

    if score <= 0.35:
        return "low_similarity"

    return "medium_similarity"


def success(expected, observed):
    return expected == observed


# =============================================================================
# DATASET / SUMMARY
# =============================================================================


def load_dataset():
    rows = []

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            rows.append(json.loads(line))

    return rows


def summarize(results):
    pair_type_groups = defaultdict(list)

    for item in results:
        pair_type_groups[item["pair_type"]].append(item)

    pair_type_summary = {}

    for pair_type, items in sorted(pair_type_groups.items()):
        count = len(items)
        success_count = sum(1 for item in items if item["success"])

        pair_type_summary[pair_type] = {
            "count": count,
            "success_count": success_count,
            "success_rate": round(success_count / count, 12),
            "avg_fuzzy_similarity": round(
                sum(item["fuzzy_similarity"] for item in items)
                / count,
                12,
            ),
            "avg_transition_overlap": round(
                sum(item["transition_overlap"] for item in items)
                / count,
                12,
            ),
            "avg_motif3_overlap": round(
                sum(item["motif3_overlap"] for item in items)
                / count,
                12,
            ),
        }

    success_count = sum(1 for item in results if item["success"])
    record_count = len(results)

    return {
        "record_count": record_count,
        "success_count": success_count,
        "success_rate": round(
            success_count / max(record_count, 1),
            12,
        ),
        "pair_type_summary": pair_type_summary,
    }


# =============================================================================
# MAIN
# =============================================================================


def main():
    dataset = load_dataset()

    results = []

    for row in dataset:
        left_tokens = tokenize(row["left_text"])
        right_tokens = tokenize(row["right_text"])

        left_canonical = canonicalize(left_tokens)
        right_canonical = canonicalize(right_tokens)

        fuzzy = fuzzy_transition_similarity(
            left_canonical,
            right_canonical,
        )

        expected = expected_behavior(row["pair_type"])
        observed = observed_behavior(fuzzy["fuzzy_similarity"])

        ok = success(expected, observed)

        results.append(
            {
                "case_id": row["case_id"],
                "pair_type": row["pair_type"],
                "family": row["family"],
                "expected_behavior": expected,
                "observed_behavior": observed,
                "success": ok,
                "fuzzy_similarity": fuzzy["fuzzy_similarity"],
                "transition_overlap": fuzzy["transition_overlap"],
                "motif2_overlap": fuzzy["motif2_overlap"],
                "motif3_overlap": fuzzy["motif3_overlap"],
                "length_score": fuzzy["length_score"],
                "cardinality_score": fuzzy["cardinality_score"],
                "entropy_score": fuzzy["entropy_score"],
            }
        )

    summary = summarize(results)

    pair_summary = summary["pair_type_summary"]

    clean_separation_ok = (
        pair_summary
        .get("STRUCTURAL_DIFFERENT", {})
        .get("success_rate", 0.0)
        >= 0.80
    )

    near_equivalence_ok = (
        pair_summary
        .get("STRUCTURAL_NEAR_EQUIVALENT", {})
        .get("success_rate", 0.0)
        >= 0.50
    )

    partial_drift_nonzero = (
        pair_summary
        .get("PARTIAL_DRIFT", {})
        .get("success_rate", 0.0)
        > 0.0
    )

    status = (
        "PASS"
        if (
            summary["success_rate"] >= 0.55
            and clean_separation_ok
            and near_equivalence_ok
            and partial_drift_nonzero
        )
        else "FAIL"
    )

    payload = {
        "experiment_name": "structural_alias_detector_v4",
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "fuzzy_structural_alias_detection",
        "purpose": (
            "Measure fuzzy transition-topology similarity instead "
            "of exact graph-signature identity."
        ),
        "core_boundary": "measurement != inference != decision",
        "dataset_path": str(DATASET_PATH),
        "summary": summary,
        "status": status,
        "pass_condition": (
            "success_rate >= 0.55 and "
            "STRUCTURAL_DIFFERENT success_rate >= 0.80 and "
            "STRUCTURAL_NEAR_EQUIVALENT success_rate >= 0.50 and "
            "PARTIAL_DRIFT success_rate > 0.0"
        ),
        "results": results,
        "main_insight": (
            "Fuzzy transition topology is less brittle than exact "
            "graph-signature matching."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy fuzzy topology detector.",
            "Thresholds are manually chosen.",
            "No semantic truth is evaluated.",
            "False-merge traps remain hard boundaries.",
            "No universal robustness claim is made.",
        ],
        "reproduction_command": (
            "python examples/structural_alias_detector_v4.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION — Structural Alias Detector v4")
    print("=" * 80)

    print(f"Status: {status}")
    print("Version: 0.4.0")
    print()

    print("Summary:")
    print(f"  Record count:   {summary['record_count']}")
    print(f"  Success count:  {summary['success_count']}")
    print(f"  Success rate:   {summary['success_rate']}")
    print()

    print("Pair-type summary:")

    for pair_type, stats in summary["pair_type_summary"].items():
        print(
            f"  {pair_type:30s} "
            f"count={stats['count']} "
            f"success_rate={stats['success_rate']} "
            f"avg_similarity={stats['avg_fuzzy_similarity']} "
            f"transition={stats['avg_transition_overlap']} "
            f"motif3={stats['avg_motif3_overlap']}"
        )

    print()
    print("Pass condition:")
    print(
        "  success_rate >= 0.55 and "
        "STRUCTURAL_DIFFERENT success_rate >= 0.80 and "
        "STRUCTURAL_NEAR_EQUIVALENT success_rate >= 0.50 and "
        "PARTIAL_DRIFT success_rate > 0.0"
    )

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()