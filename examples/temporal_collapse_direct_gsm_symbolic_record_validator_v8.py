#!/usr/bin/env python3
"""
Temporal Collapse Direct GSM-Symbolic Record Validator — v8

This script validates the Level 3 raw trajectory warning mechanism over
direct GSM-Symbolic public benchmark records mapped into raw ordered
structural trajectory events.

v8 boundary:
    source_independence = external_source_verified
    independence_method = direct_public_benchmark_record_mapping
    benchmark_name = GSM-Symbolic
    source_record_type = template_variant
    mapping_method = template_variant_to_trajectory
    external_source_reference = GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository

This does not claim that OMNIA solves GSM-Symbolic.

It only maps direct GSM-Symbolic-style public benchmark records into
ordered structural trajectory events and measures warning risk.

measurement != inference != decision
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"

INPUT_PATH = DATA_DIR / "temporal_collapse_direct_gsm_symbolic_records_v8.jsonl"
OUTPUT_PATH = RESULTS_DIR / "temporal_collapse_direct_gsm_symbolic_record_validator_v8.json"


WEIGHTS = {
    "transition_density": 0.20,
    "drift_progression": 0.20,
    "boundary_proximity": 0.25,
    "collapse_similarity": 0.25,
    "irreversibility_signal": 0.10,
}


THRESHOLDS = {
    "STABLE": 0.25,
    "DRIFT": 0.50,
    "CRITICAL": 0.75,
}


GATE_ACTIONS = {
    "STABLE": "PASS",
    "DRIFT": "WATCH",
    "CRITICAL": "ESCALATE",
    "COLLAPSE": "STOP",
}


REQUIRED_FIELDS = {
    "trajectory_id",
    "step",
    "template_id",
    "question_id",
    "variant_type",
    "signature",
    "cluster",
    "delta",
    "iri",
    "boundary_distance",
    "phase",
    "source",
    "source_independence",
    "independence_method",
    "external_source_reference",
    "benchmark_name",
    "source_record_type",
    "source_record_reference",
    "mapping_method",
    "mapping_notes",
}


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def mean_or_zero(values: list[float]) -> float:
    return mean(values) if values else 0.0


def normalized_change_count(values: list[str]) -> float:
    if len(values) < 2:
        return 0.0

    changes = 0

    for previous, current in zip(values, values[1:]):
        if previous != current:
            changes += 1

    return changes / (len(values) - 1)


def split_early_late(values: list[float]) -> tuple[list[float], list[float]]:
    if not values:
        return [], []

    if len(values) == 1:
        return values, values

    midpoint = max(1, len(values) // 2)

    return values[:midpoint], values[midpoint:]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path.relative_to(ROOT)}")

    records = []

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()

        if not stripped:
            continue

        try:
            item = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at line {line_number}: {exc}") from exc

        missing = REQUIRED_FIELDS.difference(item.keys())

        if missing:
            raise ValueError(
                f"Missing required fields at line {line_number}: {sorted(missing)}"
            )

        records.append(item)

    return records


def group_trajectories(records: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)

    for item in records:
        grouped[str(item["trajectory_id"])].append(item)

    for trajectory_id in grouped:
        grouped[trajectory_id].sort(key=lambda item: safe_float(item["step"]))

    return dict(grouped)


def unique_value(events: list[dict], key: str, default: str = "unknown") -> str:
    values = sorted({str(item.get(key, default)) for item in events})

    if not values:
        return default

    if len(values) == 1:
        return values[0]

    return "mixed:" + ",".join(values)


def compact_values(events: list[dict], key: str, default: str = "unknown") -> str:
    values = sorted({str(item.get(key, default)) for item in events})

    if not values:
        return default

    if len(values) == 1:
        return values[0]

    return "multiple_" + key + "s"


def trajectory_source(events: list[dict]) -> str:
    return unique_value(events, "source")


def trajectory_source_independence(events: list[dict]) -> str:
    return unique_value(events, "source_independence", default="not_declared")


def trajectory_independence_method(events: list[dict]) -> str:
    return unique_value(events, "independence_method", default="not_declared")


def trajectory_external_source_reference(events: list[dict]) -> str:
    return unique_value(events, "external_source_reference", default="not_declared")


def trajectory_benchmark_name(events: list[dict]) -> str:
    return unique_value(events, "benchmark_name", default="not_declared")


def trajectory_source_record_type(events: list[dict]) -> str:
    return unique_value(events, "source_record_type", default="not_declared")


def trajectory_mapping_method(events: list[dict]) -> str:
    return unique_value(events, "mapping_method", default="not_declared")


def trajectory_template_ids(events: list[dict]) -> str:
    return compact_values(events, "template_id", default="not_declared")


def trajectory_question_ids(events: list[dict]) -> str:
    return compact_values(events, "question_id", default="not_declared")


def trajectory_variant_types(events: list[dict]) -> str:
    return compact_values(events, "variant_type", default="not_declared")


def trajectory_source_record_references(events: list[dict]) -> str:
    return compact_values(events, "source_record_reference", default="not_declared")


def trajectory_mapping_notes(events: list[dict]) -> str:
    return compact_values(events, "mapping_notes", default="not_declared")


def compute_transition_density(events: list[dict]) -> float:
    signatures = [str(item["signature"]) for item in events]
    clusters = [str(item["cluster"]) for item in events]
    phases = [str(item["phase"]).upper() for item in events]

    signature_change = normalized_change_count(signatures)
    cluster_change = normalized_change_count(clusters)
    phase_change = normalized_change_count(phases)

    return clamp01(
        mean([
            signature_change,
            cluster_change,
            phase_change,
        ])
    )


def compute_drift_progression(events: list[dict]) -> float:
    deltas = [
        clamp01(safe_float(item["delta"]))
        for item in events
    ]

    if not deltas:
        return 0.0

    early, late = split_early_late(deltas)

    delta_mean = mean_or_zero(deltas)
    delta_range = max(deltas) - min(deltas)
    late_minus_early = max(0.0, mean_or_zero(late) - mean_or_zero(early))

    return clamp01(
        mean([
            delta_mean,
            delta_range,
            late_minus_early,
        ])
    )


def event_boundary_proximities(events: list[dict]) -> list[float]:
    return [
        clamp01(1.0 - clamp01(safe_float(item["boundary_distance"], default=1.0)))
        for item in events
    ]


def compute_boundary_proximity(events: list[dict]) -> float:
    proximities = event_boundary_proximities(events)

    if not proximities:
        return 0.0

    _, late = split_early_late(proximities)

    return clamp01(
        mean([
            max(proximities),
            mean_or_zero(late),
        ])
    )


def compute_collapse_similarity(events: list[dict], boundary_proximity: float) -> float:
    if not events:
        return 0.0

    phases = [
        str(item["phase"]).upper()
        for item in events
    ]

    deltas = [
        clamp01(safe_float(item["delta"]))
        for item in events
    ]

    iris = [
        clamp01(safe_float(item["iri"]))
        for item in events
    ]

    collapse_phase_ratio = phases.count("COLLAPSE") / len(phases)

    broken_marker = 1.0 if any(
        str(item["signature"]).upper() in {"BROKEN", "FAIL", "NULL", "COLLAPSE"}
        for item in events
    ) else 0.0

    return clamp01(
        mean([
            collapse_phase_ratio,
            max(deltas) if deltas else 0.0,
            max(iris) if iris else 0.0,
            boundary_proximity,
            broken_marker,
        ])
    )


def compute_irreversibility_signal(events: list[dict]) -> float:
    iris = [
        clamp01(safe_float(item["iri"]))
        for item in events
    ]

    if not iris:
        return 0.0

    _, late = split_early_late(iris)

    return clamp01(
        mean([
            max(iris),
            mean_or_zero(late),
        ])
    )


def compute_risk_score(signals: dict[str, float]) -> float:
    return clamp01(
        sum(WEIGHTS[key] * signals[key] for key in WEIGHTS)
    )


def classify_regime(risk_score: float) -> str:
    if risk_score < THRESHOLDS["STABLE"]:
        return "STABLE"

    if risk_score < THRESHOLDS["DRIFT"]:
        return "DRIFT"

    if risk_score < THRESHOLDS["CRITICAL"]:
        return "CRITICAL"

    return "COLLAPSE"


def gate_action_for_regime(regime: str) -> str:
    return GATE_ACTIONS[regime]


def dominant_axis(signals: dict[str, float]) -> str:
    return max(WEIGHTS.keys(), key=lambda key: signals[key])


def warning_flags(signals: dict[str, float]) -> list[str]:
    flags = []

    if signals["transition_density"] >= 0.50:
        flags.append("high_transition_density")

    if signals["drift_progression"] >= 0.50:
        flags.append("high_drift_progression")

    if signals["boundary_proximity"] >= 0.60:
        flags.append("boundary_proximity")

    if signals["collapse_similarity"] >= 0.60:
        flags.append("collapse_similarity")

    if signals["irreversibility_signal"] >= 0.50:
        flags.append("irreversibility_signal")

    return flags


def transition_evidence(events: list[dict]) -> dict:
    signatures = [str(item["signature"]) for item in events]
    clusters = [str(item["cluster"]) for item in events]
    phases = [str(item["phase"]).upper() for item in events]

    deltas = [
        clamp01(safe_float(item["delta"]))
        for item in events
    ]

    iris = [
        clamp01(safe_float(item["iri"]))
        for item in events
    ]

    boundary_distances = [
        clamp01(safe_float(item["boundary_distance"], default=1.0))
        for item in events
    ]

    proximities = [
        clamp01(1.0 - value)
        for value in boundary_distances
    ]

    delta_early, delta_late = split_early_late(deltas)
    iri_early, iri_late = split_early_late(iris)

    return {
        "signature_changes": round(normalized_change_count(signatures), 6),
        "cluster_changes": round(normalized_change_count(clusters), 6),
        "phase_changes": round(normalized_change_count(phases), 6),
        "delta_early_mean": round(mean_or_zero(delta_early), 6),
        "delta_late_mean": round(mean_or_zero(delta_late), 6),
        "iri_early_mean": round(mean_or_zero(iri_early), 6),
        "iri_late_mean": round(mean_or_zero(iri_late), 6),
        "min_boundary_distance": round(min(boundary_distances) if boundary_distances else 1.0, 6),
        "max_boundary_proximity": round(max(proximities) if proximities else 0.0, 6),
        "collapse_phase_count": phases.count("COLLAPSE"),
        "source": trajectory_source(events),
        "source_independence": trajectory_source_independence(events),
        "independence_method": trajectory_independence_method(events),
        "external_source_reference": trajectory_external_source_reference(events),
        "benchmark_name": trajectory_benchmark_name(events),
        "source_record_type": trajectory_source_record_type(events),
        "source_record_reference": trajectory_source_record_references(events),
        "mapping_method": trajectory_mapping_method(events),
        "mapping_notes": trajectory_mapping_notes(events),
        "template_id": trajectory_template_ids(events),
        "question_id": trajectory_question_ids(events),
        "variant_type": trajectory_variant_types(events),
    }


def analyze_trajectory(trajectory_id: str, events: list[dict]) -> dict:
    boundary_proximity = compute_boundary_proximity(events)

    signals = {
        "transition_density": compute_transition_density(events),
        "drift_progression": compute_drift_progression(events),
        "boundary_proximity": boundary_proximity,
        "collapse_similarity": compute_collapse_similarity(events, boundary_proximity),
        "irreversibility_signal": compute_irreversibility_signal(events),
    }

    risk_score = compute_risk_score(signals)
    risk_regime = classify_regime(risk_score)

    return {
        "trajectory_id": trajectory_id,
        "source": trajectory_source(events),
        "source_independence": trajectory_source_independence(events),
        "independence_method": trajectory_independence_method(events),
        "external_source_reference": trajectory_external_source_reference(events),
        "benchmark_name": trajectory_benchmark_name(events),
        "source_record_type": trajectory_source_record_type(events),
        "source_record_reference": trajectory_source_record_references(events),
        "mapping_method": trajectory_mapping_method(events),
        "mapping_notes": trajectory_mapping_notes(events),
        "template_id": trajectory_template_ids(events),
        "question_id": trajectory_question_ids(events),
        "variant_type": trajectory_variant_types(events),
        "event_count": len(events),
        "risk_regime": risk_regime,
        "risk_score": round(risk_score, 6),
        "gate_action": gate_action_for_regime(risk_regime),
        "dominant_axis": dominant_axis(signals),
        "warning_flags": warning_flags(signals),
        "signals": {
            key: round(value, 6)
            for key, value in signals.items()
        },
        "transition_evidence": transition_evidence(events),
    }


def aggregate_results(results: list[dict]) -> dict:
    if not results:
        return {
            "aggregate_risk_score": 0.0,
            "aggregate_risk_regime": "STABLE",
            "aggregate_gate_action": "PASS",
            "regime_counts": {},
            "highest_risk_trajectory": None,
            "highest_risk_score": 0.0,
            "source_count": 0,
            "independence_method_count": 0,
            "external_source_reference_count": 0,
            "benchmark_count": 0,
            "source_record_type_count": 0,
            "mapping_method_count": 0,
        }

    scores = [item["risk_score"] for item in results]
    aggregate_score = clamp01(mean(scores))
    aggregate_regime = classify_regime(aggregate_score)

    regime_counts = {}

    for item in results:
        regime = item["risk_regime"]
        regime_counts[regime] = regime_counts.get(regime, 0) + 1

    highest = max(results, key=lambda item: item["risk_score"])

    return {
        "aggregate_risk_score": round(aggregate_score, 6),
        "aggregate_risk_regime": aggregate_regime,
        "aggregate_gate_action": gate_action_for_regime(aggregate_regime),
        "regime_counts": regime_counts,
        "highest_risk_trajectory": highest["trajectory_id"],
        "highest_risk_score": highest["risk_score"],
        "source_count": len({item["source"] for item in results}),
        "independence_method_count": len({item["independence_method"] for item in results}),
        "external_source_reference_count": len({item["external_source_reference"] for item in results}),
        "benchmark_count": len({item["benchmark_name"] for item in results}),
        "source_record_type_count": len({item["source_record_type"] for item in results}),
        "mapping_method_count": len({item["mapping_method"] for item in results}),
    }


def build_source_summary(results: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)

    for result in results:
        key = (
            result["source"],
            result["source_record_type"],
            result["mapping_method"],
        )
        grouped[key].append(result)

    summaries = []

    for (source, source_record_type, mapping_method), items in sorted(grouped.items()):
        scores = [item["risk_score"] for item in items]

        regime_counts = {}

        for item in items:
            regime = item["risk_regime"]
            regime_counts[regime] = regime_counts.get(regime, 0) + 1

        highest = max(items, key=lambda item: item["risk_score"])

        summaries.append({
            "source": source,
            "source_independence": unique_summary_value(items, "source_independence"),
            "independence_method": unique_summary_value(items, "independence_method"),
            "external_source_reference": unique_summary_value(items, "external_source_reference"),
            "benchmark_name": unique_summary_value(items, "benchmark_name"),
            "source_record_type": source_record_type,
            "mapping_method": mapping_method,
            "trajectory_count": len(items),
            "average_risk_score": round(mean_or_zero(scores), 6),
            "regime_counts": regime_counts,
            "highest_risk_trajectory": highest["trajectory_id"],
            "highest_risk_score": highest["risk_score"],
        })

    return summaries


def unique_summary_value(items: list[dict], key: str, default: str = "not_declared") -> str:
    values = sorted({str(item.get(key, default)) for item in items})

    if not values:
        return default

    if len(values) == 1:
        return values[0]

    return "mixed:" + ",".join(values)


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    records = read_jsonl(INPUT_PATH)
    grouped = group_trajectories(records)

    results = [
        analyze_trajectory(trajectory_id, events)
        for trajectory_id, events in sorted(grouped.items())
    ]

    aggregate = aggregate_results(results)
    source_summary = build_source_summary(results)

    source_independence_values = sorted({
        item.get("source_independence", "not_declared")
        for item in results
    })

    independence_method_values = sorted({
        item.get("independence_method", "not_declared")
        for item in results
    })

    external_source_references = sorted({
        item.get("external_source_reference", "not_declared")
        for item in results
    })

    benchmark_names = sorted({
        item.get("benchmark_name", "not_declared")
        for item in results
    })

    source_record_types = sorted({
        item.get("source_record_type", "not_declared")
        for item in results
    })

    mapping_methods = sorted({
        item.get("mapping_method", "not_declared")
        for item in results
    })

    payload = {
        "experiment": "temporal_collapse_direct_gsm_symbolic_record_validator_v8",
        "status": "v8_direct_public_benchmark_record_mapping",
        "boundary": (
            "direct GSM-Symbolic public benchmark records mapped into raw ordered "
            "structural trajectory events"
        ),
        "claim": (
            "This script applies the Level 3 raw trajectory warning mechanism "
            "to direct GSM-Symbolic public benchmark records mapped into raw "
            "ordered structural trajectory events. It does not claim that OMNIA "
            "solves GSM-Symbolic or evaluates semantic correctness."
        ),
        "input_file": str(INPUT_PATH.relative_to(ROOT)),
        "trajectory_count": len(results),
        "source_count": aggregate["source_count"],
        "source_independence_values": source_independence_values,
        "independence_method_values": independence_method_values,
        "external_source_references": external_source_references,
        "benchmark_names": benchmark_names,
        "source_record_types": source_record_types,
        "mapping_methods": mapping_methods,
        "external_source_note": (
            "source_independence=external_source_verified means the trajectory "
            "records are mapped from a public/documentable benchmark source. "
            "independence_method=direct_public_benchmark_record_mapping means "
            "the records include direct benchmark record fields such as template_id, "
            "question_id, variant_type, source_record_reference, and mapping_method. "
            "This does not imply semantic solving or benchmark correctness."
        ),
        "weights": WEIGHTS,
        "thresholds": THRESHOLDS,
        "aggregate": aggregate,
        "source_summary": source_summary,
        "results": results,
    }

    OUTPUT_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    print("=" * 100)
    print("TEMPORAL COLLAPSE DIRECT GSM-SYMBOLIC RECORD VALIDATOR — v8")
    print("=" * 100)

    print()
    print("INPUT FILE")
    print("=" * 100)
    print(INPUT_PATH.relative_to(ROOT))

    print()
    print("SOURCE SUMMARY")
    print("=" * 100)
    print(json.dumps(source_summary, indent=2))

    print()
    print("TRAJECTORY RESULTS")
    print("=" * 100)

    for result in results:
        print()
        print(f"trajectory_id:              {result['trajectory_id']}")
        print(f"template_id:                {result['template_id']}")
        print(f"question_id:                {result['question_id']}")
        print(f"variant_type:               {result['variant_type']}")
        print(f"source:                     {result['source']}")
        print(f"source_independence:        {result['source_independence']}")
        print(f"independence_method:        {result['independence_method']}")
        print(f"external_source_reference:  {result['external_source_reference']}")
        print(f"benchmark_name:             {result['benchmark_name']}")
        print(f"source_record_type:         {result['source_record_type']}")
        print(f"source_record_reference:    {result['source_record_reference']}")
        print(f"mapping_method:             {result['mapping_method']}")
        print(f"mapping_notes:              {result['mapping_notes']}")
        print(f"event_count:                {result['event_count']}")
        print(f"risk_regime:                {result['risk_regime']}")
        print(f"risk_score:                 {result['risk_score']}")
        print(f"gate_action:                {result['gate_action']}")
        print(f"dominant_axis:              {result['dominant_axis']}")
        print(f"warning_flags:              {result['warning_flags']}")
        print(f"signals:                    {result['signals']}")
        print(f"evidence:                   {result['transition_evidence']}")

    print()
    print("=" * 100)
    print("AGGREGATE")
    print("=" * 100)
    print(json.dumps(aggregate, indent=2))

    print()
    print("=" * 100)
    print(f"Wrote result file: {OUTPUT_PATH.relative_to(ROOT)}")
    print("=" * 100)


if __name__ == "__main__":
    main()