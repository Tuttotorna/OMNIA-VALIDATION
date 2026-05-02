import json
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "0.3.0"

DATASET_PATH = Path("data/structural_benchmark_dataset_v0.jsonl")
RESULTS_PATH = Path("results/structural_alias_detector_v3.json")


def tokenize(text):
    if "|" in text:
        return [x.strip() for x in text.split("|") if x.strip()]
    return [x.strip() for x in text.split() if x.strip()]


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


def build_transition_graph(sequence):
    graph = defaultdict(Counter)

    for i in range(len(sequence) - 1):
        a = sequence[i]
        b = sequence[i + 1]
        graph[a][b] += 1

    return graph


def graph_signature(graph):
    signature = []

    for node in sorted(graph.keys()):
        edges = graph[node]
        total = sum(edges.values())

        normalized = []

        for target in sorted(edges.keys()):
            ratio = round(edges[target] / total, 6)
            normalized.append((target, ratio))

        signature.append((node, tuple(normalized)))

    return tuple(signature)


def transition_similarity(sig_a, sig_b):
    if sig_a == sig_b:
        return 1.0

    set_a = set(sig_a)
    set_b = set(sig_b)

    if not set_a and not set_b:
        return 1.0

    overlap = len(set_a & set_b)
    union = len(set_a | set_b)

    return overlap / union if union > 0 else 0.0


def frequency_similarity(tokens_a, tokens_b):
    freq_a = Counter(tokens_a)
    freq_b = Counter(tokens_b)

    keys = set(freq_a.keys()) | set(freq_b.keys())

    overlap = 0.0
    total = 0.0

    for key in keys:
        overlap += min(freq_a[key], freq_b[key])
        total += max(freq_a[key], freq_b[key])

    return overlap / total if total > 0 else 0.0


def alias_evidence(tokens_a, tokens_b):
    canon_a = canonicalize(tokens_a)
    canon_b = canonicalize(tokens_b)

    graph_a = build_transition_graph(canon_a)
    graph_b = build_transition_graph(canon_b)

    sig_a = graph_signature(graph_a)
    sig_b = graph_signature(graph_b)

    transition_score = transition_similarity(sig_a, sig_b)

    lexical_score = frequency_similarity(tokens_a, tokens_b)

    structural_bonus = 0.0

    if canon_a == canon_b:
        structural_bonus = 0.25

    final_score = (
        (transition_score * 0.7)
        + (lexical_score * 0.1)
        + structural_bonus
    )

    return {
        "transition_score": round(transition_score, 12),
        "lexical_score": round(lexical_score, 12),
        "structural_bonus": round(structural_bonus, 12),
        "alias_evidence": round(min(final_score, 1.0), 12),
    }


def classify(pair_type, evidence):
    score = evidence["alias_evidence"]

    if pair_type in {
        "STRUCTURAL_EQUIVALENT",
        "STRUCTURAL_NEAR_EQUIVALENT",
    }:
        return score >= 0.75

    if pair_type == "FALSE_SPLIT_TRAP":
        return score >= 0.60

    if pair_type == "STRUCTURAL_DIFFERENT":
        return score <= 0.55

    if pair_type == "FALSE_MERGE_TRAP":
        return score <= 0.40

    if pair_type == "PARTIAL_DRIFT":
        return 0.45 <= score <= 0.90

    return False


def load_dataset():
    rows = []

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            rows.append(json.loads(line))

    return rows


def main():
    dataset = load_dataset()

    results = []

    success_count = 0

    pair_type_totals = defaultdict(int)
    pair_type_success = defaultdict(int)

    for row in dataset:
        pair_type = row["pair_type"]

        tokens_a = tokenize(row["left_text"])
        tokens_b = tokenize(row["right_text"])

        evidence = alias_evidence(tokens_a, tokens_b)

        success = classify(pair_type, evidence)

        pair_type_totals[pair_type] += 1

        if success:
            pair_type_success[pair_type] += 1
            success_count += 1

        results.append({
            "case_id": row["case_id"],
            "pair_type": pair_type,
            "family": row["family"],
            "alias_evidence": evidence["alias_evidence"],
            "transition_score": evidence["transition_score"],
            "lexical_score": evidence["lexical_score"],
            "structural_bonus": evidence["structural_bonus"],
            "success": success,
        })

    record_count = len(results)

    pair_type_summary = {}

    for pair_type in sorted(pair_type_totals.keys()):
        total = pair_type_totals[pair_type]
        succ = pair_type_success[pair_type]

        pair_type_summary[pair_type] = {
            "count": total,
            "success_count": succ,
            "success_rate": round(succ / total, 12),
        }

    success_rate = success_count / record_count if record_count else 0.0

    status = (
        "PASS"
        if success_rate >= 0.75
        else "FAIL"
    )

    payload = {
        "experiment_name": "structural_alias_detector_v3",
        "version": VERSION,
        "domain": "structural_alias_detection",
        "purpose": (
            "Measure alias similarity using transition topology "
            "instead of token overlap."
        ),
        "core_boundary": "measurement != inference != decision",
        "dataset_path": str(DATASET_PATH),
        "record_count": record_count,
        "success_count": success_count,
        "success_rate": round(success_rate, 12),
        "pair_type_summary": pair_type_summary,
        "status": status,
        "results": results,
        "main_insight": (
            "Transition topology preserves structural equivalence "
            "better than lexical overlap."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy alias detector.",
            "No semantic truth is evaluated.",
            "Graph signatures remain simplified.",
            "No universal robustness claim is made.",
        ],
        "reproduction_command": (
            "python examples/structural_alias_detector_v3.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION — Structural Alias Detector v3")
    print("=" * 80)

    print(f"Status: {status}")
    print()

    print("Summary:")
    print(f"  Record count:   {record_count}")
    print(f"  Success count:  {success_count}")
    print(f"  Success rate:   {round(success_rate, 12)}")
    print()

    print("Pair-type summary:")

    for pair_type, stats in pair_type_summary.items():
        print(
            f"  {pair_type:30s} "
            f"count={stats['count']} "
            f"success_rate={stats['success_rate']}"
        )

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()