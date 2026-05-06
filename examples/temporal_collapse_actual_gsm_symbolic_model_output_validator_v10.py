#!/usr/bin/env python3
"""
Temporal Collapse Actual GSM-Symbolic Model Output Validator — v10

This script validates the Level 3 raw trajectory warning mechanism over
bounded actual-output-style GSM-Symbolic model-output traces mapped into
raw ordered structural trajectory events.

v10 boundary:
    source_independence = external_source_verified
    independence_method = actual_model_output_trace_mapping
    benchmark_name = GSM-Symbolic
    source_record_type = actual_model_output
    mapping_method = actual_model_output_to_trajectory

Important limitation:
    These are bounded actual-output-style records for validator construction,
    not an official public GSM-Symbolic model-output benchmark run.

This does not claim that OMNIA solves GSM-Symbolic.

This does not infer semantic truth.

Correctness and extraction are tracked as evidence, not as the final measurement.

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

INPUT_PATH = DATA_DIR / "temporal_collapse_actual_gsm_symbolic_model_outputs_v10.jsonl"
OUTPUT_PATH = RESULTS_DIR / "temporal_collapse_actual_gsm_symbolic_model_output_validator_v10.json"


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
    "model_name",
    "model_version",
    "run_id",
    "response_id",
    "raw_question_hash",
    "raw_output_hash",
    "answer_extraction_method",
    "expected_answer",
    "model_final_answer",
    "is_correct",
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


def safe_bool(value) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in {"true", "1", "yes", "y"}:
            return True

        if normalized in {"false", "0", "no", "n"}:
            return False

    return bool(value)


def is_extracted_answer(value) -> bool:
    normalized = str(value).strip().lower()

    if normalized in {
        "",
        "none",
        "null",
        "not_extracted",
        "not extracted",
        "nan",
        "n/a",
        "unknown",
    }:
        return False

    return True


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


def normalized_bool_change_count(values: list[bool]) -> float:
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

    plural_labels = {
        "template_id": "multiple_template_ids",
        "question_id": "multiple_question_ids",
        "variant_type": "multiple_variant_types",
        "source_record_reference": "multiple_source_record_references",
        "mapping_notes": "multiple_mapping_notes",
        "response_id": "multiple_response_ids",
        "expected_answer": "multiple_expected_answers",
        "model_final_answer": "multiple_model_final_answers",
        "raw_question_hash": "multiple_raw_question_hashes",
        "raw_output_hash": "multiple_raw_output_hashes",
        "answer_extraction_method": "multiple_answer_extraction_methods",
    }

    return plural_labels.get(key, f"multiple_{key}_values")


def trajectory_field(events: list[dict], key: str) -> str:
    return unique_value(events, key, "not_declared")


def trajectory_compact(events: list[dict], key: str) -> str:
    return compact_values(events, key, "not_declared")


def compute_correctness_profile(events: list[dict]) -> dict:
    correctness = [safe_bool(item["is_correct"]) for item in events]

    correct_count = sum(1 for value in correctness if value)
    incorrect_count = sum(1 for value in correctness if not value)

    return {
        "event_count": len(events),
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "accuracy_rate": round(correct_count / len(events), 6) if events else 0.0,
        "correctness_changes": round(normalized_bool_change_count(correctness), 6),
        "starts_correct": correctness[0] if correctness else None,
        "ends_correct": correctness[-1] if correctness else None,
    }


def compute_extraction_profile(events: list[dict]) -> dict:
    extracted = [
        is_extracted_answer(item.get("model_final_answer"))
        for item in events
    ]

    extracted_count = sum(1 for value in extracted if value)
    not_extracted_count = sum(1 for value in extracted if not value)

    methods = sorted({
        str(item.get("answer_extraction_method", "not_declared"))
        for item in events
    })

    return {
        "event_count": len(events),
        "extracted_count": extracted_count,
        "not_extracted_count": not_extracted_count,
        "extraction_rate": round(extracted_count / len(events), 6) if events else 0.0,
        "extraction_changes": round(normalized_bool_change_count(extracted), 6),
        "starts_extracted": extracted[0] if extracted else None,
        "ends_extracted": extracted[-1] if extracted else None,
        "answer_extraction_methods": methods,
    }


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
        marker in str(item["signature"]).upper()
        for item in events
        for marker in {"BROKEN", "FAIL", "NULL", "COLLAPSE", "NOT_EXTRACTED"}
    ) else 0.0

    extraction_failure_marker = 1.0 if any(
        not is_extracted_answer(item.get("model_final_answer"))
        for item in events
    ) else 0.0

    return clamp01(
        mean([
            collapse_phase_ratio,
            max(deltas) if deltas else 0.0,
            max(iris) if iris else 0.0,
            boundary_proximity,
            max(broken_marker, extraction_failure_marker),
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
    correctness = [safe_bool(item["is_correct"]) for item in events]
    extraction = [is_extracted_answer(item.get("model_final_answer")) for item in events]

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

    correct_count = sum(1 for value in correctness if value)
    incorrect_count = sum(1 for value in correctness if not value)

    extracted_count = sum(1 for value in extraction if value)
    not_extracted_count = sum(1 for value in extraction if not value)

    return {
        "signature_changes": round(normalized_change_count(signatures), 6),
        "cluster_changes": round(normalized_change_count(clusters), 6),
        "phase_changes": round(normalized_change_count(phases), 6),
        "correctness_changes": round(normalized_bool_change_count(correctness), 6),
        "extraction_changes": round(normalized_bool_change_count(extraction), 6),
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "accuracy_rate": round(correct_count / len(events), 6) if events else 0.0,
        "extracted_count": extracted_count,
        "not_extracted_count": not_extracted_count,
        "extraction_rate": round(extracted_count / len(events), 6) if events else 0.0,
        "starts_correct": correctness[0] if correctness else None,
        "ends_correct": correctness[-1] if correctness else None,
        "starts_extracted": extraction[0] if extraction else None,
        "ends_extracted": extraction[-1] if extraction else None,
        "delta_early_mean": round(mean_or_zero(delta_early), 6),
        "delta_late_mean": round(mean_or_zero(delta_late), 6),
        "iri_early_mean": round(mean_or_zero(iri_early), 6),
        "iri_late_mean": round(mean_or_zero(iri_late), 6),
        "min_boundary_distance": round(min(boundary_distances) if boundary_distances else 1.0, 6),
        "max_boundary_proximity": round(max(proximities) if proximities else 0.0, 6),
        "collapse_phase_count": phases.count("COLLAPSE"),
        "source": trajectory_field(events, "source"),
        "source_independence": trajectory_field(events, "source_independence"),
        "independence_method": trajectory_field(events, "independence_method"),
        "external_source_reference": trajectory_field(events, "external_source_reference"),
        "benchmark_name": trajectory_field(events, "benchmark_name"),
        "source_record_type": trajectory_field(events, "source_record_type"),
        "source_record_reference": trajectory_compact(events, "source_record_reference"),
        "mapping_method": trajectory_field(events, "mapping_method"),
        "mapping_notes": trajectory_compact(events, "mapping_notes"),
        "model_name": trajectory_field(events, "model_name"),
        "model_version": trajectory_field(events, "model_version"),
        "run_id": trajectory_field(events, "run_id"),
        "response_id": trajectory_compact(events, "response_id"),
        "template_id": trajectory_compact(events, "template_id"),
        "question_id": trajectory_compact(events, "question_id"),
        "variant_type": trajectory_compact(events, "variant_type"),
        "raw_question_hash": trajectory_compact(events, "raw_question_hash"),
        "raw_output_hash": trajectory_compact(events, "raw_output_hash"),
        "answer_extraction_method": trajectory_compact(events, "answer_extraction_method"),
        "expected_answer": trajectory_compact(events, "expected_answer"),
        "model_final_answer": trajectory_compact(events, "model_final_answer"),
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

    correctness_profile = compute_correctness_profile(events)
    extraction_profile = compute_extraction_profile(events)

    return {
        "trajectory_id": trajectory_id,
        "source": trajectory_field(events, "source"),
        "source_independence": trajectory_field(events, "source_independence"),
        "independence_method": trajectory_field(events, "independence_method"),
        "external_source_reference": trajectory_field(events, "external_source_reference"),
        "benchmark_name": trajectory_field(events, "benchmark_name"),
        "source_record_type": trajectory_field(events, "source_record_type"),
        "source_record_reference": trajectory_compact(events, "source_record_reference"),
        "mapping_method": trajectory_field(events, "mapping_method"),
        "mapping_notes": trajectory_compact(events, "mapping_notes"),
        "model_name": trajectory_field(events, "model_name"),
        "model_version": trajectory_field(events, "model_version"),
        "run_id": trajectory_field(events, "run_id"),
        "response_id": trajectory_compact(events, "response_id"),
        "template_id": trajectory_compact(events, "template_id"),
        "question_id": trajectory_compact(events, "question_id"),
        "variant_type": trajectory_compact(events, "variant_type"),
        "raw_question_hash": trajectory_compact(events, "raw_question_hash"),
        "raw_output_hash": trajectory_compact(events, "raw_output_hash"),
        "answer_extraction_method": trajectory_compact(events, "answer_extraction_method"),
        "expected_answer": trajectory_compact(events, "expected_answer"),
        "model_final_answer": trajectory_compact(events, "model_final_answer"),
        "correctness_profile": correctness_profile,
        "extraction_profile": extraction_profile,
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
            "aggregate_accuracy_rate": 0.0,
            "aggregate_extraction_rate": 0.0,
            "regime_counts": {},
            "highest_risk_trajectory": None,
            "highest_risk_score": 0.0,
            "source_count": 0,
            "independence_method_count": 0,
            "external_source_reference_count": 0,
            "benchmark_count": 0,
            "source_record_type_count": 0,
            "mapping_method_count": 0,
            "model_count": 0,
            "model_version_count": 0,
            "answer_extraction_method_count": 0,
        }

    scores = [item["risk_score"] for item in results]

    accuracy_rates = [
        item["correctness_profile"]["accuracy_rate"]
        for item in results
    ]

    extraction_rates = [
        item["extraction_profile"]["extraction_rate"]
        for item in results
    ]

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
        "aggregate_accuracy_rate": round(mean_or_zero(accuracy_rates), 6),
        "aggregate_extraction_rate": round(mean_or_zero(extraction_rates), 6),
        "regime_counts": regime_counts,
        "highest_risk_trajectory": highest["trajectory_id"],
        "highest_risk_score": highest["risk_score"],
        "source_count": len({item["source"] for item in results}),
        "independence_method_count": len({item["independence_method"] for item in results}),
        "external_source_reference_count": len({item["external_source_reference"] for item in results}),
        "benchmark_count": len({item["benchmark_name"] for item in results}),
        "source_record_type_count": len({item["source_record_type"] for item in results}),
        "mapping_method_count": len({item["mapping_method"] for item in results}),
        "model_count": len({item["model_name"] for item in results}),
        "model_version_count": len({item["model_version"] for item in results}),
        "answer_extraction_method_count": len({item["answer_extraction_method"] for item in results}),
    }


def unique_summary_value(items: list[dict], key: str, default: str = "not_declared") -> str:
    values = sorted({str(item.get(key, default)) for item in items})

    if not values:
        return default

    if len(values) == 1:
        return values[0]

    return "mixed:" + ",".join(values)


def build_source_summary(results: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str, str, str, str], list[dict]] = defaultdict(list)

    for result in results:
        key = (
            result["source"],
            result["source_record_type"],
            result["mapping_method"],
            result["model_name"],
            result["model_version"],
            result["answer_extraction_method"],
        )
        grouped[key].append(result)

    summaries = []

    for (
        source,
        source_record_type,
        mapping_method,
        model_name,
        model_version,
        answer_extraction_method,
    ), items in sorted(grouped.items()):
        scores = [item["risk_score"] for item in items]

        accuracy_rates = [
            item["correctness_profile"]["accuracy_rate"]
            for item in items
        ]

        extraction_rates = [
            item["extraction_profile"]["extraction_rate"]
            for item in items
        ]

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
            "model_name": model_name,
            "model_version": model_version,
            "answer_extraction_method": answer_extraction_method,
            "trajectory_count": len(items),
            "average_risk_score": round(mean_or_zero(scores), 6),
            "average_accuracy_rate": round(mean_or_zero(accuracy_rates), 6),
            "average_extraction_rate": round(mean_or_zero(extraction_rates), 6),
            "regime_counts": regime_counts,
            "highest_risk_trajectory": highest["trajectory_id"],
            "highest_risk_score": highest["risk_score"],
        })

    return summaries


def collect_values(results: list[dict], key: str) -> list[str]:
    return sorted({
        str(item.get(key, "not_declared"))
        for item in results
    })


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

    payload = {
        "experiment": "temporal_collapse_actual_gsm_symbolic_model_output_validator_v10",
        "status": "v10_actual_model_output_style_trace_validation",
        "boundary": (
            "bounded actual-output-style GSM-Symbolic model-output traces mapped "
            "into raw ordered structural trajectory events"
        ),
        "claim": (
            "This script applies the Level 3 raw trajectory warning mechanism "
            "to bounded actual-output-style GSM-Symbolic model-output traces mapped "
            "into raw ordered structural trajectory events. It does not claim that "
            "OMNIA solves GSM-Symbolic, does not infer semantic truth, and does not "
            "replace benchmark correctness."
        ),
        "limitation_note": (
            "These are bounded actual-output-style records for validator construction, "
            "not an official public GSM-Symbolic model-output benchmark run."
        ),
        "input_file": str(INPUT_PATH.relative_to(ROOT)),
        "trajectory_count": len(results),
        "source_count": aggregate["source_count"],
        "source_independence_values": collect_values(results, "source_independence"),
        "independence_method_values": collect_values(results, "independence_method"),
        "external_source_references": collect_values(results, "external_source_reference"),
        "benchmark_names": collect_values(results, "benchmark_name"),
        "source_record_types": collect_values(results, "source_record_type"),
        "mapping_methods": collect_values(results, "mapping_method"),
        "model_names": collect_values(results, "model_name"),
        "model_versions": collect_values(results, "model_version"),
        "answer_extraction_methods": collect_values(results, "answer_extraction_method"),
        "external_source_note": (
            "source_independence=external_source_verified means the trace boundary "
            "is mapped from a public/documentable GSM-Symbolic benchmark reference. "
            "independence_method=actual_model_output_trace_mapping means the records "
            "include model-output-style fields such as model_name, model_version, "
            "run_id, response_id, raw_question_hash, raw_output_hash, "
            "answer_extraction_method, expected_answer, model_final_answer, and "
            "is_correct. Correctness and extraction are reported as evidence; "
            "risk_score remains a structural warning measurement."
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
    print("TEMPORAL COLLAPSE ACTUAL GSM-SYMBOLIC MODEL OUTPUT VALIDATOR — v10")
    print("=" * 100)

    print()
    print("INPUT FILE")
    print("=" * 100)
    print(INPUT_PATH.relative_to(ROOT))

    print()
    print("LIMITATION NOTE")
    print("=" * 100)
    print(payload["limitation_note"])

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
        print(f"model_name:                 {result['model_name']}")
        print(f"model_version:              {result['model_version']}")
        print(f"run_id:                     {result['run_id']}")
        print(f"response_id:                {result['response_id']}")
        print(f"raw_question_hash:          {result['raw_question_hash']}")
        print(f"raw_output_hash:            {result['raw_output_hash']}")
        print(f"answer_extraction_method:   {result['answer_extraction_method']}")
        print(f"expected_answer:            {result['expected_answer']}")
        print(f"model_final_answer:         {result['model_final_answer']}")
        print(f"correctness_profile:        {result['correctness_profile']}")
        print(f"extraction_profile:         {result['extraction_profile']}")
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