import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# =============================================================================
# OMNIA-VALIDATION — Multi Projection Recovery v0
# =============================================================================

VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RESULTS_PATH = RESULTS_DIR / "multi_projection_recovery_v0.json"

# =============================================================================
# DATASET
# =============================================================================

DATASET = [
    {
        "case_id": "recover_001_binary_alias",
        "pair_type": "RECOVERABLE_COLLAPSE",
        "expected_recoverable": True,
        "seq_a": "ABABABABABABABAB",
        "seq_b": "1212121212121212",
    },
    {
        "case_id": "recover_002_four_cycle_alias",
        "pair_type": "RECOVERABLE_COLLAPSE",
        "expected_recoverable": True,
        "seq_a": "ABCDABCDABCDABCD",
        "seq_b": "1234123412341234",
    },
    {
        "case_id": "recover_003_nested_alias",
        "pair_type": "RECOVERABLE_COLLAPSE",
        "expected_recoverable": True,
        "seq_a": "AAAABBBBCCCCDDDD",
        "seq_b": "1111222233334444",
    },
    {
        "case_id": "recover_004_projection_collision",
        "pair_type": "RECOVERABLE_COLLAPSE",
        "expected_recoverable": True,
        "seq_a": "0101010101010101",
        "seq_b": "XYXYXYXYXYXYXYXY",
    },
    {
        "case_id": "recover_005_partial_drift",
        "pair_type": "PARTIAL_RECOVERY",
        "expected_recoverable": True,
        "seq_a": "ABABABABABABABAB",
        "seq_b": "ABABABCBABABABCB",
    },
    {
        "case_id": "recover_006_run_drift",
        "pair_type": "PARTIAL_RECOVERY",
        "expected_recoverable": True,
        "seq_a": "AAAABBBBCCCCDDDD",
        "seq_b": "AAAABBBBCCCCDDDX",
    },
    {
        "case_id": "recover_007_irrecoverable",
        "pair_type": "IRRECOVERABLE_COLLAPSE",
        "expected_recoverable": False,
        "seq_a": "AAAAAAAAAAAAAAAA",
        "seq_b": "BBBBBBBBBBBBBBBB",
    },
    {
        "case_id": "recover_008_entropy_flat",
        "pair_type": "IRRECOVERABLE_COLLAPSE",
        "expected_recoverable": False,
        "seq_a": "1111111111111111",
        "seq_b": "XXXXXXXXXXXXXXXX",
    },
]

# =============================================================================
# PROJECTIONS
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


def transition_graph(sequence):
    edges = Counter()

    for i in range(len(sequence) - 1):
        edge = (sequence[i], sequence[i + 1])
        edges[edge] += 1

    return edges


def motif_counts(sequence, size=3):
    motifs = Counter()

    for i in range(len(sequence) - size + 1):
        motif = sequence[i : i + size]
        motifs[motif] += 1

    return motifs


def normalized_entropy(sequence):
    counts = Counter(sequence)
    total = len(sequence)

    probs = [v / total for v in counts.values()]

    entropy = -sum(
        p * math.log2(p)
        for p in probs
        if p > 0
    )

    max_entropy = math.log2(max(len(counts), 2))

    return entropy / max_entropy if max_entropy > 0 else 0.0


# =============================================================================
# SIMILARITY
# =============================================================================

def counter_overlap(a, b):
    keys = set(a.keys()) | set(b.keys())

    if not keys:
        return 1.0

    numerator = sum(min(a.get(k, 0), b.get(k, 0)) for k in keys)
    denominator = sum(max(a.get(k, 0), b.get(k, 0)) for k in keys)

    if denominator == 0:
        return 1.0

    return numerator / denominator


def entropy_similarity(a, b):
    ea = normalized_entropy(a)
    eb = normalized_entropy(b)

    return 1.0 - abs(ea - eb)


# =============================================================================
# MULTI-PROJECTION RECOVERY
# =============================================================================

def projection_family(sequence):
    return {
        "normalized": normalize_symbols(sequence),
        "transitions": transition_graph(sequence),
        "motif3": motif_counts(sequence, 3),
        "entropy": normalized_entropy(sequence),
    }


def recoverability_score(seq_a, seq_b):
    pa = projection_family(seq_a)
    pb = projection_family(seq_b)

    normalized_match = (
        1.0
        if pa["normalized"] == pb["normalized"]
        else 0.0
    )

    transition_overlap = counter_overlap(
        pa["transitions"],
        pb["transitions"],
    )

    motif_overlap = counter_overlap(
        pa["motif3"],
        pb["motif3"],
    )

    entropy_match = entropy_similarity(seq_a, seq_b)

    score = (
        0.35 * normalized_match
        + 0.30 * transition_overlap
        + 0.20 * motif_overlap
        + 0.15 * entropy_match
    )

    return {
        "recoverability_score": round(score, 12),
        "normalized_match": round(normalized_match, 12),
        "transition_overlap": round(transition_overlap, 12),
        "motif3_overlap": round(motif_overlap, 12),
        "entropy_similarity": round(entropy_match, 12),
    }


def classify(score):
    if score >= 0.80:
        return "RECOVERABLE"

    if score >= 0.45:
        return "PARTIAL"

    return "IRRECOVERABLE"


# =============================================================================
# MAIN
# =============================================================================

def main():
    results = []

    success_count = 0

    for row in DATASET:
        metrics = recoverability_score(
            row["seq_a"],
            row["seq_b"],
        )

        observed = classify(
            metrics["recoverability_score"]
        )

        expected = (
            "RECOVERABLE"
            if row["expected_recoverable"]
            else "IRRECOVERABLE"
        )

        success = (
            observed == expected
            or (
                expected == "RECOVERABLE"
                and observed == "PARTIAL"
                and row["pair_type"] == "PARTIAL_RECOVERY"
            )
        )

        if success:
            success_count += 1

        results.append({
            "case_id": row["case_id"],
            "pair_type": row["pair_type"],
            "expected_behavior": expected,
            "observed_behavior": observed,
            "success": success,
            **metrics,
        })

    record_count = len(results)
    success_rate = success_count / record_count

    pair_summary = {}

    for r in results:
        pt = r["pair_type"]

        if pt not in pair_summary:
            pair_summary[pt] = {
                "count": 0,
                "success_count": 0,
                "recoverability_scores": [],
            }

        pair_summary[pt]["count"] += 1

        if r["success"]:
            pair_summary[pt]["success_count"] += 1

        pair_summary[pt]["recoverability_scores"].append(
            r["recoverability_score"]
        )

    for pt in pair_summary:
        data = pair_summary[pt]

        data["success_rate"] = round(
            data["success_count"] / data["count"],
            12,
        )

        data["avg_recoverability"] = round(
            sum(data["recoverability_scores"])
            / len(data["recoverability_scores"]),
            12,
        )

        del data["recoverability_scores"]

    status = (
        "PASS"
        if success_rate >= 0.75
        else "FAIL"
    )

    output = {
        "experiment_name": "multi_projection_recovery_v0",
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": "multi_projection_recoverability",
        "purpose": (
            "Measure whether structural collapse "
            "can be partially or fully reversed "
            "through observer-family expansion."
        ),
        "core_boundary": (
            "measurement != inference != decision"
        ),
        "summary": {
            "record_count": record_count,
            "success_count": success_count,
            "success_rate": round(success_rate, 12),
            "pair_type_summary": pair_summary,
        },
        "status": status,
        "pass_condition": "success_rate >= 0.75",
        "results": results,
        "main_insight": (
            "Some projection collapses remain "
            "recoverable under expanded observer families."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy recoverability framework.",
            "Observer families are simplified.",
            "No semantic truth is evaluated.",
            "Recoverability is projection-relative.",
            "No universal recoverability claim is made.",
        ],
        "reproduction_command": (
            "python examples/multi_projection_recovery_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    # =========================================================================
    # PRINT
    # =========================================================================

    print("=" * 80)
    print("OMNIA-VALIDATION — Multi Projection Recovery v0")
    print("=" * 80)

    print(f"Status: {status}")
    print(f"Version: {VERSION}")
    print()

    print("Summary:")
    print(f"  Record count:   {record_count}")
    print(f"  Success count:  {success_count}")
    print(f"  Success rate:   {round(success_rate, 12)}")
    print()

    print("Pair-type summary:")

    for pt, data in pair_summary.items():
        print(
            f"  {pt:<30} "
            f"count={data['count']} "
            f"success_rate={data['success_rate']} "
            f"avg_recoverability={data['avg_recoverability']}"
        )

    print()
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()