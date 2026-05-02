import json
import math
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(
    ROOT,
    "data",
    "structural_benchmark_dataset_v0.jsonl",
)

RESULTS_PATH = os.path.join(
    ROOT,
    "results",
    "structural_benchmark_runner_v0.json",
)


# =============================================================================
# BASIC UTILITIES
# =============================================================================


def normalize_whitespace(text):
    return " ".join(text.strip().split())


def tokenize(text):
    text = normalize_whitespace(text)

    separators = [
        "|",
        ",",
        ";",
        ":",
        "/",
        "\\",
        "-",
        "_",
        "\n",
        "\t",
    ]

    for sep in separators:
        text = text.replace(sep, " ")

    return [token for token in text.split(" ") if token]


def canonical_projection(tokens):
    mapping = {}
    next_id = 0
    projected = []

    for token in tokens:
        if token not in mapping:
            mapping[token] = str(next_id)
            next_id += 1

        projected.append(mapping[token])

    return "".join(projected)


def shannon_entropy(sequence):
    if not sequence:
        return 0.0

    counts = Counter(sequence)
    total = len(sequence)

    entropy = 0.0

    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy


def transition_ratio(sequence):
    if len(sequence) < 2:
        return 0.0

    transitions = 0

    for i in range(len(sequence) - 1):
        if sequence[i] != sequence[i + 1]:
            transitions += 1

    return transitions / (len(sequence) - 1)


def repetition_ratio(sequence):
    if not sequence:
        return 0.0

    counts = Counter(sequence)
    return max(counts.values()) / len(sequence)


def periodicity_score(sequence):
    if not sequence:
        return 0.0

    max_period = min(16, len(sequence) // 2)

    best = 0.0

    for period in range(1, max_period + 1):
        matches = 0
        total = 0

        for i in range(len(sequence) - period):
            total += 1

            if sequence[i] == sequence[i + period]:
                matches += 1

        if total > 0:
            best = max(best, matches / total)

    return best


def omega_proxy(projected):
    entropy = shannon_entropy(projected)

    entropy_norm = min(entropy / 4.0, 1.0)

    transition = transition_ratio(projected)
    repetition = repetition_ratio(projected)
    periodicity = periodicity_score(projected)

    score = (
        0.30 * entropy_norm
        + 0.25 * transition
        + 0.20 * repetition
        + 0.25 * periodicity
    )

    return round(score, 12)


def normalized_edit_distance(a, b):
    if a == b:
        return 0.0

    if not a or not b:
        return 1.0

    rows = len(a) + 1
    cols = len(b) + 1

    dp = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i

    for j in range(cols):
        dp[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )

    distance = dp[-1][-1]
    norm = distance / max(len(a), len(b))

    return round(norm, 12)


def combined_distance(left_projected, right_projected):
    edit = normalized_edit_distance(left_projected, right_projected)

    left_omega = omega_proxy(left_projected)
    right_omega = omega_proxy(right_projected)

    omega_gap = abs(left_omega - right_omega)

    combined = edit + omega_gap

    return round(combined, 12)


# =============================================================================
# DATASET
# =============================================================================


def load_dataset(path):
    records = []

    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()

            if not line:
                continue

            records.append(json.loads(line))

    return records


# =============================================================================
# EXPECTED RELATION LOGIC
# =============================================================================


def classify_expected(pair_type):
    if pair_type in [
        "STRUCTURAL_EQUIVALENT",
        "STRUCTURAL_NEAR_EQUIVALENT",
    ]:
        return "should_merge"

    if pair_type == "PARTIAL_DRIFT":
        return "partial"

    if pair_type in [
        "STRUCTURAL_DIFFERENT",
        "FALSE_MERGE_TRAP",
    ]:
        return "should_split"

    if pair_type == "FALSE_SPLIT_TRAP":
        return "should_merge"

    return "unknown"


def evaluate_behavior(expected, distance):
    if distance <= 0.15:
        observed = "merge"

    elif distance <= 0.45:
        observed = "partial"

    else:
        observed = "split"

    success = False

    if expected == "should_merge":
        success = observed == "merge"

    elif expected == "should_split":
        success = observed == "split"

    elif expected == "partial":
        success = observed == "partial"

    return observed, success


# =============================================================================
# RUNNER
# =============================================================================


def run_record(record):
    left_tokens = tokenize(record["left_text"])
    right_tokens = tokenize(record["right_text"])

    left_projected = canonical_projection(left_tokens)
    right_projected = canonical_projection(right_tokens)

    distance = combined_distance(
        left_projected,
        right_projected,
    )

    expected = classify_expected(record["pair_type"])

    observed, success = evaluate_behavior(
        expected,
        distance,
    )

    return {
        "case_id": record["case_id"],
        "family": record["family"],
        "pair_type": record["pair_type"],
        "expected_relation": expected,
        "observed_relation": observed,
        "success": success,
        "distance": distance,
        "left_projected_preview": left_projected[:64],
        "right_projected_preview": right_projected[:64],
    }


# =============================================================================
# SUMMARY
# =============================================================================


def build_summary(results):
    pair_type_stats = defaultdict(lambda: {
        "count": 0,
        "success": 0,
        "distance_sum": 0.0,
    })

    false_merge_count = 0
    false_split_count = 0
    partial_mismatch_count = 0

    for result in results:
        pair_type = result["pair_type"]

        pair_type_stats[pair_type]["count"] += 1
        pair_type_stats[pair_type]["distance_sum"] += result["distance"]

        if result["success"]:
            pair_type_stats[pair_type]["success"] += 1

        expected = result["expected_relation"]
        observed = result["observed_relation"]

        if expected == "should_split" and observed == "merge":
            false_merge_count += 1

        if expected == "should_merge" and observed == "split":
            false_split_count += 1

        if expected == "partial" and observed != "partial":
            partial_mismatch_count += 1

    pair_type_summary = {}

    for key, stats in sorted(pair_type_stats.items()):
        count = stats["count"]

        pair_type_summary[key] = {
            "count": count,
            "success_rate": round(
                stats["success"] / count,
                12,
            ),
            "avg_distance": round(
                stats["distance_sum"] / count,
                12,
            ),
        }

    total = len(results)
    total_success = sum(1 for r in results if r["success"])

    return {
        "record_count": total,
        "success_count": total_success,
        "success_rate": round(total_success / total, 12),
        "false_merge_count": false_merge_count,
        "false_split_count": false_split_count,
        "partial_mismatch_count": partial_mismatch_count,
        "pair_type_summary": pair_type_summary,
    }


# =============================================================================
# MAIN
# =============================================================================


def main():
    records = load_dataset(DATASET_PATH)

    results = []

    for record in records:
        results.append(run_record(record))

    summary = build_summary(results)

    pass_condition = (
        summary["success_rate"] >= 0.60
        and summary["false_merge_count"] <= 4
        and summary["false_split_count"] <= 4
    )

    status = "PASS" if pass_condition else "FAIL"

    output = {
        "experiment_name": "structural_benchmark_runner_v0",
        "version": "0.1.0",
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "omnia_native_structural_benchmark_execution",
        "purpose": "Run the OMNIA-native structural benchmark dataset.",
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Benchmark Runner",
        "dataset_path": "data/structural_benchmark_dataset_v0.jsonl",
        "results": results,
        "summary": summary,
        "pass_condition": (
            "success_rate >= 0.60 "
            "and false_merge_count <= 4 "
            "and false_split_count <= 4"
        ),
        "status": status,
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy benchmark runner.",
            "Thresholds are manually chosen.",
            "No semantic truth is evaluated.",
            "The dataset is synthetic.",
            "No universal robustness claim is made.",
        ],
        "reproduction_command": (
            "python examples/structural_benchmark_runner_v0.py"
        ),
    }

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)

    with open(RESULTS_PATH, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION — Structural Benchmark Runner v0")
    print("=" * 80)

    print(f"Status: {status}")
    print("Claim level: Level 1 — Benchmark Runner")

    print()
    print("Summary:")
    print(f"  Record count:             {summary['record_count']}")
    print(f"  Success count:            {summary['success_count']}")
    print(f"  Success rate:             {summary['success_rate']}")
    print(f"  False merge count:        {summary['false_merge_count']}")
    print(f"  False split count:        {summary['false_split_count']}")
    print(f"  Partial mismatch count:   {summary['partial_mismatch_count']}")

    print()
    print("Pair-type summary:")

    for pair_type, stats in summary["pair_type_summary"].items():
        print(
            f"  {pair_type:<30} "
            f"count={stats['count']} "
            f"success_rate={stats['success_rate']} "
            f"avg_distance={stats['avg_distance']}"
        )

    print()
    print("Pass condition:")
    print(
        "  success_rate >= 0.60 "
        "and false_merge_count <= 4 "
        "and false_split_count <= 4"
    )

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()