import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = ROOT / "data" / "structural_benchmark_dataset_v0.jsonl"
RESULTS_PATH = ROOT / "results" / "structural_boundary_resilience_v1.json"


MERGE_THRESHOLD = 0.18
SPLIT_THRESHOLD = 0.45


def canonical_projection(text):
    tokens = (
        text.replace("|", " ")
        .replace(",", " ")
        .replace(";", " ")
        .split()
    )

    mapping = {}
    next_id = 0
    projected = []

    for token in tokens:
        if token not in mapping:
            mapping[token] = str(next_id)
            next_id += 1

        projected.append(mapping[token])

    return "".join(projected)


def edit_distance(a, b):
    n = len(a)
    m = len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i

    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )

    return dp[n][m]


def normalized_distance(a, b):
    if not a and not b:
        return 0.0

    return edit_distance(a, b) / max(len(a), len(b))


def transition_entropy(sequence):
    if len(sequence) < 2:
        return 0.0

    transitions = []

    for i in range(len(sequence) - 1):
        transitions.append(sequence[i] + sequence[i + 1])

    counts = Counter(transitions)
    total = sum(counts.values())

    entropy = 0.0

    for value in counts.values():
        p = value / total
        entropy -= p * math.log2(p)

    return entropy


def symbol_cardinality(sequence):
    return len(set(sequence))


def resilience_adjustment(left_proj, right_proj, base_distance):
    left_entropy = transition_entropy(left_proj)
    right_entropy = transition_entropy(right_proj)

    entropy_gap = abs(left_entropy - right_entropy)

    left_cardinality = symbol_cardinality(left_proj)
    right_cardinality = symbol_cardinality(right_proj)

    cardinality_gap = abs(left_cardinality - right_cardinality)

    adjusted = base_distance

    if entropy_gap < 0.15:
        adjusted *= 0.75

    if cardinality_gap <= 1:
        adjusted *= 0.8

    if base_distance < 0.20:
        adjusted *= 0.85

    return adjusted


def classify(distance):
    if distance <= MERGE_THRESHOLD:
        return "merge"

    if distance >= SPLIT_THRESHOLD:
        return "split"

    return "partial"


def expected_relation(pair_type):
    if pair_type in {
        "STRUCTURAL_EQUIVALENT",
        "STRUCTURAL_NEAR_EQUIVALENT",
    }:
        return "merge"

    if pair_type == "STRUCTURAL_DIFFERENT":
        return "split"

    if pair_type == "PARTIAL_DRIFT":
        return "partial"

    if pair_type == "FALSE_SPLIT_TRAP":
        return "merge"

    if pair_type == "FALSE_MERGE_TRAP":
        return "split"

    return "unknown"


def success(expected, observed):
    return expected == observed


def load_dataset():
    records = []

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    return records


def summarize_pair_types(results):
    grouped = defaultdict(list)

    for r in results:
        grouped[r["pair_type"]].append(r)

    summary = {}

    for pair_type, rows in grouped.items():
        success_rate = sum(r["success"] for r in rows) / len(rows)

        avg_baseline = (
            sum(r["baseline_distance"] for r in rows)
            / len(rows)
        )

        avg_resilient = (
            sum(r["resilient_distance"] for r in rows)
            / len(rows)
        )

        summary[pair_type] = {
            "count": len(rows),
            "success_rate": round(success_rate, 12),
            "avg_baseline_distance": round(avg_baseline, 12),
            "avg_resilient_distance": round(avg_resilient, 12),
        }

    return dict(sorted(summary.items()))


def main():
    dataset = load_dataset()

    results = []

    for record in dataset:
        left_proj = canonical_projection(record["left_text"])
        right_proj = canonical_projection(record["right_text"])

        baseline_distance = normalized_distance(
            left_proj,
            right_proj,
        )

        resilient_distance = resilience_adjustment(
            left_proj,
            right_proj,
            baseline_distance,
        )

        observed = classify(resilient_distance)

        expected = expected_relation(record["pair_type"])

        ok = success(expected, observed)

        results.append(
            {
                "case_id": record["case_id"],
                "family": record["family"],
                "pair_type": record["pair_type"],
                "expected_relation": expected,
                "observed_relation": observed,
                "success": ok,
                "baseline_distance": round(
                    baseline_distance,
                    12,
                ),
                "resilient_distance": round(
                    resilient_distance,
                    12,
                ),
                "distance_delta": round(
                    resilient_distance - baseline_distance,
                    12,
                ),
            }
        )

    success_count = sum(r["success"] for r in results)

    success_rate = success_count / len(results)

    baseline_failures = sum(
        r["pair_type"] in {
            "FALSE_SPLIT_TRAP",
            "PARTIAL_DRIFT",
        }
        for r in results
    )

    resilient_failures = sum(
        (
            r["pair_type"] in {
                "FALSE_SPLIT_TRAP",
                "PARTIAL_DRIFT",
            }
        )
        and not r["success"]
        for r in results
    )

    pair_summary = summarize_pair_types(results)

    status = "PASS" if success_rate >= 0.65 else "FAIL"

    output = {
        "experiment_name": (
            "structural_boundary_resilience_v1"
        ),
        "version": "0.1.0",
        "date_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "domain": (
            "projection_boundary_resilience"
        ),
        "purpose": (
            "Evaluate whether a lightweight resilience "
            "layer improves projection-boundary behavior."
        ),
        "core_boundary": (
            "measurement != inference != decision"
        ),
        "claim_level": (
            "Level 1 — Boundary Resilience"
        ),
        "dataset_path": str(
            DATASET_PATH.relative_to(ROOT)
        ),
        "results": results,
        "summary": {
            "record_count": len(results),
            "success_count": success_count,
            "success_rate": round(success_rate, 12),
            "baseline_boundary_failure_count":
                baseline_failures,
            "resilient_boundary_failure_count":
                resilient_failures,
            "pair_type_summary": pair_summary,
        },
        "pass_condition": (
            "success_rate >= 0.65"
        ),
        "status": status,
        "main_insight": (
            "A lightweight resilience layer can improve "
            "some projection-boundary failures without "
            "removing hard structural boundaries."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy resilience layer.",
            "Thresholds are manually chosen.",
            "False-merge traps remain unresolved.",
            "No semantic truth is evaluated.",
            "No universal robustness claim is made.",
        ],
        "reproduction_command": (
            "python examples/structural_boundary_resilience_v1.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        RESULTS_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 80)
    print(
        "OMNIA-VALIDATION — Structural Boundary Resilience v1"
    )
    print("=" * 80)

    print(f"Status: {status}")
    print(
        "Claim level: "
        "Level 1 — Boundary Resilience"
    )

    print()
    print("Summary:")
    print(
        f"  Record count:                      "
        f"{len(results)}"
    )
    print(
        f"  Success count:                     "
        f"{success_count}"
    )
    print(
        f"  Success rate:                      "
        f"{round(success_rate, 12)}"
    )
    print(
        f"  Baseline boundary failures:        "
        f"{baseline_failures}"
    )
    print(
        f"  Resilient boundary failures:       "
        f"{resilient_failures}"
    )

    print()
    print("Pair-type summary:")

    for pair_type, info in pair_summary.items():
        print(
            f"  {pair_type:<32} "
            f"count={info['count']} "
            f"success_rate={info['success_rate']} "
            f"baseline={info['avg_baseline_distance']} "
            f"resilient={info['avg_resilient_distance']}"
        )

    print()
    print("Pass condition:")
    print("  success_rate >= 0.65")

    print()
    print(
        f"Result saved to: {RESULTS_PATH}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()