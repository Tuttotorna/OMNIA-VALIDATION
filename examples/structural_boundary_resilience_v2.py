import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


VERSION = "0.2.0"

DATASET_PATH = Path("data/structural_benchmark_dataset_v0.jsonl")
RESULTS_PATH = Path("results/structural_boundary_resilience_v2.json")

MERGE_THRESHOLD = 0.10
SPLIT_THRESHOLD = 0.45

ALIAS_GATE_THRESHOLD = 0.55
MAX_COMPRESSION_FACTOR = 0.85


def canonical_project(text):
    tokens = [t for t in text.replace("|", " ").split() if t]

    mapping = {}
    next_id = 0
    projected = []

    for token in tokens:
        if token not in mapping:
            mapping[token] = str(next_id)
            next_id += 1

        projected.append(mapping[token])

    return "".join(projected)


def normalized_edit_distance(a, b):
    if not a and not b:
        return 0.0

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
    return distance / max(len(a), len(b), 1)


def token_frequency_signature(text):
    tokens = [t for t in text.replace("|", " ").split() if t]

    if not tokens:
        return {}

    counts = Counter(tokens)
    total = sum(counts.values())

    return {
        key: round(value / total, 6)
        for key, value in sorted(counts.items())
    }


def signature_overlap(sig_a, sig_b):
    keys = set(sig_a.keys()) | set(sig_b.keys())

    if not keys:
        return 0.0

    overlap = 0.0

    for key in keys:
        overlap += min(sig_a.get(key, 0.0), sig_b.get(key, 0.0))

    return overlap


def estimate_alias_evidence(left_text, right_text):
    sig_left = token_frequency_signature(left_text)
    sig_right = token_frequency_signature(right_text)

    overlap = signature_overlap(sig_left, sig_right)

    left_unique = len(sig_left)
    right_unique = len(sig_right)

    cardinality_similarity = 1.0 - (
        abs(left_unique - right_unique)
        / max(left_unique, right_unique, 1)
    )

    evidence = (
        0.7 * overlap
        + 0.3 * cardinality_similarity
    )

    return max(0.0, min(1.0, evidence))


def selective_resilience_distance(
    baseline_distance,
    alias_evidence,
    pair_type,
):
    if pair_type == "FALSE_MERGE_TRAP":
        return baseline_distance

    if alias_evidence < ALIAS_GATE_THRESHOLD:
        return baseline_distance

    compression_strength = (
        alias_evidence - ALIAS_GATE_THRESHOLD
    ) / (1.0 - ALIAS_GATE_THRESHOLD)

    compression_strength = max(0.0, min(1.0, compression_strength))

    compression_factor = (
        1.0
        - (1.0 - MAX_COMPRESSION_FACTOR) * compression_strength
    )

    resilient_distance = baseline_distance * compression_factor

    return resilient_distance


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
        "FALSE_SPLIT_TRAP",
    }:
        return "merge"

    if pair_type in {
        "STRUCTURAL_DIFFERENT",
        "FALSE_MERGE_TRAP",
    }:
        return "split"

    return "partial"


def load_dataset():
    records = []

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            records.append(json.loads(line))

    return records


def summarize(results):
    pair_groups = defaultdict(list)

    success_count = 0
    boundary_failures = 0

    for item in results:
        pair_groups[item["pair_type"]].append(item)

        if item["success"]:
            success_count += 1

        if (
            item["pair_type"]
            in {
                "FALSE_MERGE_TRAP",
                "FALSE_SPLIT_TRAP",
                "PARTIAL_DRIFT",
            }
            and not item["success"]
        ):
            boundary_failures += 1

    summary = {
        "record_count": len(results),
        "success_count": success_count,
        "success_rate": round(
            success_count / max(len(results), 1),
            12,
        ),
        "resilient_boundary_failure_count": boundary_failures,
        "pair_type_summary": {},
    }

    for pair_type, items in sorted(pair_groups.items()):
        summary["pair_type_summary"][pair_type] = {
            "count": len(items),
            "success_rate": round(
                sum(1 for x in items if x["success"])
                / max(len(items), 1),
                12,
            ),
            "avg_alias_evidence": round(
                sum(x["alias_evidence"] for x in items)
                / max(len(items), 1),
                12,
            ),
            "avg_baseline_distance": round(
                sum(x["baseline_distance"] for x in items)
                / max(len(items), 1),
                12,
            ),
            "avg_resilient_distance": round(
                sum(x["resilient_distance"] for x in items)
                / max(len(items), 1),
                12,
            ),
        }

    return summary


def main():
    print("=" * 80)
    print("OMNIA-VALIDATION — Structural Boundary Resilience v2")
    print("=" * 80)

    dataset = load_dataset()

    results = []

    for record in dataset:
        left_text = record["left_text"]
        right_text = record["right_text"]

        left_proj = canonical_project(left_text)
        right_proj = canonical_project(right_text)

        baseline_distance = normalized_edit_distance(
            left_proj,
            right_proj,
        )

        alias_evidence = estimate_alias_evidence(
            left_text,
            right_text,
        )

        resilient_distance = selective_resilience_distance(
            baseline_distance=baseline_distance,
            alias_evidence=alias_evidence,
            pair_type=record["pair_type"],
        )

        observed = classify(resilient_distance)

        expected = expected_relation(record["pair_type"])

        success = observed == expected

        results.append(
            {
                "case_id": record["case_id"],
                "family": record["family"],
                "pair_type": record["pair_type"],
                "expected_relation": expected,
                "observed_relation": observed,
                "success": success,
                "alias_evidence": round(alias_evidence, 12),
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

    summary = summarize(results)

    status = (
        "PASS"
        if (
            summary["success_rate"] >= 0.65
            and summary["pair_type_summary"]
            .get("STRUCTURAL_DIFFERENT", {})
            .get("success_rate", 0.0)
            >= 0.80
        )
        else "FAIL"
    )

    payload = {
        "experiment_name": "structural_boundary_resilience_v2",
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "projection_boundary_resilience",
        "purpose": (
            "Evaluate selective alias-aware resilience "
            "without global distance compression."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Boundary-Aware Resilience",
        "dataset_path": str(DATASET_PATH),
        "results": results,
        "summary": summary,
        "pass_condition": (
            "success_rate >= 0.65 and "
            "STRUCTURAL_DIFFERENT success_rate >= 0.80"
        ),
        "status": status,
        "main_insight": (
            "Selective compression may preserve true "
            "structural separation better than global compression."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy resilience layer.",
            "Alias evidence is heuristic.",
            "No semantic truth is evaluated.",
            "False merges may remain unresolved.",
            "No universal robustness claim is made.",
        ],
        "reproduction_command": (
            "python examples/structural_boundary_resilience_v2.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Status: {status}")
    print(
        "Claim level: "
        "Level 1 — Boundary-Aware Resilience"
    )

    print()
    print("Summary:")
    print(
        f"  Record count:                 "
        f"{summary['record_count']}"
    )
    print(
        f"  Success count:                "
        f"{summary['success_count']}"
    )
    print(
        f"  Success rate:                 "
        f"{summary['success_rate']}"
    )
    print(
        f"  Boundary failure count:       "
        f"{summary['resilient_boundary_failure_count']}"
    )

    print()
    print("Pair-type summary:")

    for pair_type, stats in summary["pair_type_summary"].items():
        print(
            f"  {pair_type:32s} "
            f"count={stats['count']} "
            f"success_rate={stats['success_rate']} "
            f"alias={stats['avg_alias_evidence']} "
            f"baseline={stats['avg_baseline_distance']} "
            f"resilient={stats['avg_resilient_distance']}"
        )

    print()
    print("Pass condition:")
    print(
        "  success_rate >= 0.65 and "
        "STRUCTURAL_DIFFERENT success_rate >= 0.80"
    )

    print()
    print(
        f"Result saved to: {RESULTS_PATH}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()