#!/usr/bin/env python3
"""
Temporal Collapse Cross-Provider Disagreement Validator — v13

Boundary:
    Cross-provider real parsed GSM-Symbolic model-output records are mapped
    into raw ordered structural trajectory events.

Claim:
    This script applies the Level 3 raw trajectory warning mechanism to
    cross-provider real parsed GSM-Symbolic model-output records.

    It does not claim that OMNIA solves GSM-Symbolic.
    It does not infer semantic truth.
    It does not replace benchmark correctness.
    It does not make final decisions.

Core rule:
    measurement != inference != decision
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Tuple


INPUT_FILE = Path("data/temporal_collapse_cross_provider_disagreement_v13.jsonl")
OUTPUT_FILE = Path("results/temporal_collapse_cross_provider_disagreement_validator_v13.json")

EXPERIMENT = "temporal_collapse_cross_provider_disagreement_validator_v13"
STATUS = "v13_cross_provider_disagreement_mapping"

LIMITATION_NOTE = (
    "Cross-provider disagreement validation does not imply official benchmark "
    "scoring, production certification, semantic truth detection, or final decision authority."
)

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

REQUIRED_KEYS = [
    "trajectory_id",
    "step",
    "template_id",
    "question_id",
    "variant_type",
    "provider",
    "model_name",
    "model_version",
    "run_id",
    "response_id",
    "source_file",
    "source_file_hash",
    "source_group_id",
    "cross_provider_group",
    "cross_provider_role",
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
]


def banner(title: str) -> None:
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    records: List[Dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at line {line_no}: {exc}") from exc

            missing = [key for key in REQUIRED_KEYS if key not in record]
            if missing:
                raise ValueError(
                    f"Record at line {line_no} is missing required keys: {missing}"
                )

            records.append(record)

    if not records:
        raise ValueError(f"Input file is empty: {path}")

    return records


def unique_sorted(records: Iterable[Dict[str, Any]], key: str) -> List[Any]:
    return sorted({record[key] for record in records})


def group_by(records: Iterable[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
    grouped: Dict[Any, List[Dict[str, Any]]] = defaultdict(list)

    for record in records:
        grouped[record[key]].append(record)

    return dict(grouped)


def changes_ratio(values: List[Any]) -> float:
    if len(values) <= 1:
        return 0.0

    changes = sum(1 for a, b in zip(values, values[1:]) if a != b)
    return round(changes / (len(values) - 1), 6)


def early_late_mean(values: List[float]) -> Tuple[float, float]:
    if not values:
        return 0.0, 0.0

    split = max(1, len(values) // 2)
    early = values[:split]
    late = values[split:]

    if not late:
        late = early

    return round(mean(early), 6), round(mean(late), 6)


def classify_risk(score: float) -> Tuple[str, str]:
    if score < THRESHOLDS["STABLE"]:
        return "STABLE", "PASS"

    if score < THRESHOLDS["DRIFT"]:
        return "DRIFT", "WATCH"

    if score < THRESHOLDS["CRITICAL"]:
        return "CRITICAL", "ESCALATE"

    return "COLLAPSE", "STOP"


def extraction_status(answer: str) -> bool:
    return str(answer).strip().lower() != "not_extracted"


def build_correctness_profile(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    correctness = [bool(event["is_correct"]) for event in events]
    event_count = len(correctness)
    correct_count = sum(1 for item in correctness if item)
    incorrect_count = event_count - correct_count

    return {
        "event_count": event_count,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "accuracy_rate": round(correct_count / event_count, 6),
        "correctness_changes": changes_ratio(correctness),
        "starts_correct": correctness[0],
        "ends_correct": correctness[-1],
    }


def build_extraction_profile(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    extracted = [extraction_status(event["model_final_answer"]) for event in events]
    event_count = len(extracted)
    extracted_count = sum(1 for item in extracted if item)
    not_extracted_count = event_count - extracted_count

    return {
        "event_count": event_count,
        "extracted_count": extracted_count,
        "not_extracted_count": not_extracted_count,
        "extraction_rate": round(extracted_count / event_count, 6),
        "extraction_changes": changes_ratio(extracted),
        "starts_extracted": extracted[0],
        "ends_extracted": extracted[-1],
        "answer_extraction_methods": unique_sorted(events, "answer_extraction_method"),
    }


def collapse_similarity(events: List[Dict[str, Any]]) -> float:
    phases = [event["phase"] for event in events]
    signatures = [event["signature"] for event in events]
    model_answers = [str(event["model_final_answer"]).lower() for event in events]

    collapse_phase_count = sum(1 for phase in phases if phase == "COLLAPSE")
    broken_signature_count = sum(
        1
        for signature in signatures
        if "BROKEN" in signature or "NOT_EXTRACTED" in signature
    )
    not_extracted_count = sum(1 for answer in model_answers if answer == "not_extracted")

    event_count = len(events)

    value = (
        0.40 * (collapse_phase_count / event_count)
        + 0.35 * (broken_signature_count / event_count)
        + 0.25 * (not_extracted_count / event_count)
    )

    return round(value, 6)


def warning_flags(signals: Dict[str, float]) -> List[str]:
    flags: List[str] = []

    if signals["transition_density"] >= 0.50:
        flags.append("high_transition_density")

    if signals["drift_progression"] >= 0.50:
        flags.append("high_drift_progression")

    if signals["boundary_proximity"] >= 0.70:
        flags.append("boundary_proximity")

    if signals["collapse_similarity"] >= 0.50:
        flags.append("collapse_similarity")

    if signals["irreversibility_signal"] >= 0.50:
        flags.append("irreversibility_signal")

    return flags


def dominant_axis(signals: Dict[str, float]) -> str:
    return max(signals.items(), key=lambda item: item[1])[0]


def summarize_multiple(events: List[Dict[str, Any]], key: str) -> Any:
    values = unique_sorted(events, key)

    if len(values) == 1:
        return values[0]

    return f"multiple_{key}s"


def build_trajectory_result(trajectory_id: str, events: List[Dict[str, Any]]) -> Dict[str, Any]:
    events = sorted(events, key=lambda event: event["step"])

    signatures = [event["signature"] for event in events]
    clusters = [event["cluster"] for event in events]
    phases = [event["phase"] for event in events]
    deltas = [float(event["delta"]) for event in events]
    iris = [float(event["iri"]) for event in events]
    boundary_distances = [float(event["boundary_distance"]) for event in events]

    delta_early_mean, delta_late_mean = early_late_mean(deltas)
    iri_early_mean, iri_late_mean = early_late_mean(iris)

    transition_density = round(
        mean(
            [
                changes_ratio(signatures),
                changes_ratio(clusters),
                changes_ratio(phases),
            ]
        ),
        6,
    )

    drift_progression = round(
        max(
            0.0,
            mean(
                [
                    delta_late_mean - delta_early_mean,
                    iri_late_mean - iri_early_mean,
                ]
            ),
        ),
        6,
    )

    boundary_proximity = round(1.0 - min(boundary_distances), 6)
    collapse_sim = collapse_similarity(events)
    irreversibility_signal = round(max(iris), 6)

    signals = {
        "transition_density": transition_density,
        "drift_progression": drift_progression,
        "boundary_proximity": boundary_proximity,
        "collapse_similarity": collapse_sim,
        "irreversibility_signal": irreversibility_signal,
    }

    risk_score = round(
        sum(WEIGHTS[key] * value for key, value in signals.items()),
        6,
    )

    risk_regime, gate_action = classify_risk(risk_score)

    correctness_profile = build_correctness_profile(events)
    extraction_profile = build_extraction_profile(events)

    transition_evidence = {
        "signature_changes": changes_ratio(signatures),
        "cluster_changes": changes_ratio(clusters),
        "phase_changes": changes_ratio(phases),
        "delta_early_mean": delta_early_mean,
        "delta_late_mean": delta_late_mean,
        "iri_early_mean": iri_early_mean,
        "iri_late_mean": iri_late_mean,
        "min_boundary_distance": round(min(boundary_distances), 6),
        "max_boundary_proximity": boundary_proximity,
        "collapse_phase_count": sum(1 for phase in phases if phase == "COLLAPSE"),
        "broken_signature_count": sum(
            1
            for signature in signatures
            if "BROKEN" in signature or "NOT_EXTRACTED" in signature
        ),
        "not_extracted_signature_count": sum(
            1
            for event in events
            if str(event["model_final_answer"]).lower() == "not_extracted"
        ),
        "correctness_changes": correctness_profile["correctness_changes"],
        "extraction_changes": extraction_profile["extraction_changes"],
        "correct_count": correctness_profile["correct_count"],
        "incorrect_count": correctness_profile["incorrect_count"],
        "accuracy_rate": correctness_profile["accuracy_rate"],
        "extracted_count": extraction_profile["extracted_count"],
        "not_extracted_count": extraction_profile["not_extracted_count"],
        "extraction_rate": extraction_profile["extraction_rate"],
        "starts_correct": correctness_profile["starts_correct"],
        "ends_correct": correctness_profile["ends_correct"],
        "starts_extracted": extraction_profile["starts_extracted"],
        "ends_extracted": extraction_profile["ends_extracted"],
        "source": summarize_multiple(events, "source"),
        "source_independence": summarize_multiple(events, "source_independence"),
        "independence_method": summarize_multiple(events, "independence_method"),
        "external_source_reference": summarize_multiple(events, "external_source_reference"),
        "benchmark_name": summarize_multiple(events, "benchmark_name"),
        "source_record_type": summarize_multiple(events, "source_record_type"),
        "mapping_method": summarize_multiple(events, "mapping_method"),
        "source_file": summarize_multiple(events, "source_file"),
        "source_file_hash": summarize_multiple(events, "source_file_hash"),
        "source_group_id": summarize_multiple(events, "source_group_id"),
        "model_name": summarize_multiple(events, "model_name"),
        "model_version": summarize_multiple(events, "model_version"),
        "provider": summarize_multiple(events, "provider"),
        "run_id": summarize_multiple(events, "run_id"),
        "template_id": summarize_multiple(events, "template_id"),
        "cross_provider_group": summarize_multiple(events, "cross_provider_group"),
        "cross_provider_role": summarize_multiple(events, "cross_provider_role"),
        "answer_extraction_method": summarize_multiple(events, "answer_extraction_method"),
        "source_record_reference": summarize_multiple(events, "source_record_reference"),
        "mapping_notes": summarize_multiple(events, "mapping_notes"),
        "response_id": summarize_multiple(events, "response_id"),
        "question_id": summarize_multiple(events, "question_id"),
        "variant_type": summarize_multiple(events, "variant_type"),
        "raw_question_hash": summarize_multiple(events, "raw_question_hash"),
        "raw_output_hash": summarize_multiple(events, "raw_output_hash"),
        "expected_answer": summarize_multiple(events, "expected_answer"),
        "model_final_answer": summarize_multiple(events, "model_final_answer"),
    }

    first = events[0]

    return {
        "trajectory_id": trajectory_id,
        "source": first["source"],
        "source_independence": first["source_independence"],
        "independence_method": first["independence_method"],
        "external_source_reference": first["external_source_reference"],
        "benchmark_name": first["benchmark_name"],
        "source_record_type": first["source_record_type"],
        "mapping_method": first["mapping_method"],
        "source_file": first["source_file"],
        "source_file_hash": first["source_file_hash"],
        "source_group_id": first["source_group_id"],
        "model_name": first["model_name"],
        "model_version": first["model_version"],
        "provider": first["provider"],
        "run_id": first["run_id"],
        "template_id": first["template_id"],
        "cross_provider_group": first["cross_provider_group"],
        "cross_provider_role": first["cross_provider_role"],
        "answer_extraction_method": first["answer_extraction_method"],
        "source_record_reference": summarize_multiple(events, "source_record_reference"),
        "mapping_notes": summarize_multiple(events, "mapping_notes"),
        "response_id": summarize_multiple(events, "response_id"),
        "question_id": summarize_multiple(events, "question_id"),
        "variant_type": summarize_multiple(events, "variant_type"),
        "raw_question_hash": summarize_multiple(events, "raw_question_hash"),
        "raw_output_hash": summarize_multiple(events, "raw_output_hash"),
        "expected_answer": summarize_multiple(events, "expected_answer"),
        "model_final_answer": summarize_multiple(events, "model_final_answer"),
        "correctness_profile": correctness_profile,
        "extraction_profile": extraction_profile,
        "event_count": len(events),
        "risk_regime": risk_regime,
        "risk_score": risk_score,
        "gate_action": gate_action,
        "dominant_axis": dominant_axis(signals),
        "warning_flags": warning_flags(signals),
        "signals": signals,
        "transition_evidence": transition_evidence,
    }


def summarize_group(group_key: str, group_value: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    risk_scores = [result["risk_score"] for result in results]
    accuracy_rates = [result["correctness_profile"]["accuracy_rate"] for result in results]
    extraction_rates = [result["extraction_profile"]["extraction_rate"] for result in results]

    regime_counts: Dict[str, int] = defaultdict(int)
    for result in results:
        regime_counts[result["risk_regime"]] += 1

    highest = max(results, key=lambda result: result["risk_score"])

    summary = {
        group_key: group_value,
        "trajectory_count": len(results),
        "event_count": sum(result["event_count"] for result in results),
        "average_risk_score": round(mean(risk_scores), 6),
        "average_accuracy_rate": round(mean(accuracy_rates), 6),
        "average_extraction_rate": round(mean(extraction_rates), 6),
        "regime_counts": dict(sorted(regime_counts.items())),
        "highest_risk_trajectory": highest["trajectory_id"],
        "highest_risk_score": highest["risk_score"],
        "sources": sorted({result["source"] for result in results}),
        "source_independences": sorted({result["source_independence"] for result in results}),
        "independence_methods": sorted({result["independence_method"] for result in results}),
        "external_source_references": sorted({result["external_source_reference"] for result in results}),
        "benchmark_names": sorted({result["benchmark_name"] for result in results}),
        "source_record_types": sorted({result["source_record_type"] for result in results}),
        "mapping_methods": sorted({result["mapping_method"] for result in results}),
        "source_files": sorted({result["source_file"] for result in results}),
        "source_file_hashes": sorted({result["source_file_hash"] for result in results}),
        "source_group_ids": sorted({result["source_group_id"] for result in results}),
        "model_names": sorted({result["model_name"] for result in results}),
        "model_versions": sorted({result["model_version"] for result in results}),
        "providers": sorted({result["provider"] for result in results}),
        "answer_extraction_methods": sorted(
            {result["answer_extraction_method"] for result in results}
        ),
        "cross_provider_groups": sorted({result["cross_provider_group"] for result in results}),
        "cross_provider_roles": sorted({result["cross_provider_role"] for result in results}),
    }

    return summary


def build_cross_provider_summary(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped = group_by(results, "cross_provider_group")
    summaries: List[Dict[str, Any]] = []

    for cross_provider_group, group_results in sorted(grouped.items()):
        provider_risk_scores = {
            result["provider"]: result["risk_score"] for result in group_results
        }
        provider_risk_regimes = {
            result["provider"]: result["risk_regime"] for result in group_results
        }
        provider_accuracy_rates = {
            result["provider"]: result["correctness_profile"]["accuracy_rate"]
            for result in group_results
        }
        provider_extraction_rates = {
            result["provider"]: result["extraction_profile"]["extraction_rate"]
            for result in group_results
        }

        highest = max(group_results, key=lambda result: result["risk_score"])
        risk_values = list(provider_risk_scores.values())

        summaries.append(
            {
                "cross_provider_group": cross_provider_group,
                "template_ids": sorted({result["template_id"] for result in group_results}),
                "providers": sorted({result["provider"] for result in group_results}),
                "trajectory_ids": sorted({result["trajectory_id"] for result in group_results}),
                "provider_risk_scores": provider_risk_scores,
                "provider_risk_regimes": provider_risk_regimes,
                "provider_accuracy_rates": provider_accuracy_rates,
                "provider_extraction_rates": provider_extraction_rates,
                "cross_provider_risk_spread": round(max(risk_values) - min(risk_values), 6),
                "cross_provider_accuracy_spread": round(
                    max(provider_accuracy_rates.values()) - min(provider_accuracy_rates.values()),
                    6,
                ),
                "cross_provider_extraction_spread": round(
                    max(provider_extraction_rates.values())
                    - min(provider_extraction_rates.values()),
                    6,
                ),
                "risk_regime_disagreement": len(set(provider_risk_regimes.values())) > 1,
                "accuracy_disagreement": len(set(provider_accuracy_rates.values())) > 1,
                "extraction_disagreement": len(set(provider_extraction_rates.values())) > 1,
                "highest_risk_provider": highest["provider"],
                "highest_risk_trajectory": highest["trajectory_id"],
                "highest_risk_score": highest["risk_score"],
            }
        )

    return summaries


def build_aggregate(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    risk_scores = [result["risk_score"] for result in results]
    accuracy_rates = [result["correctness_profile"]["accuracy_rate"] for result in results]
    extraction_rates = [result["extraction_profile"]["extraction_rate"] for result in results]

    aggregate_risk_score = round(mean(risk_scores), 6)
    aggregate_risk_regime, aggregate_gate_action = classify_risk(aggregate_risk_score)

    regime_counts: Dict[str, int] = defaultdict(int)
    for result in results:
        regime_counts[result["risk_regime"]] += 1

    highest = max(results, key=lambda result: result["risk_score"])

    return {
        "aggregate_risk_score": aggregate_risk_score,
        "aggregate_risk_regime": aggregate_risk_regime,
        "aggregate_gate_action": aggregate_gate_action,
        "aggregate_accuracy_rate": round(mean(accuracy_rates), 6),
        "aggregate_extraction_rate": round(mean(extraction_rates), 6),
        "regime_counts": dict(sorted(regime_counts.items())),
        "highest_risk_trajectory": highest["trajectory_id"],
        "highest_risk_score": highest["risk_score"],
        "highest_risk_provider": highest["provider"],
        "source_count": len({result["source"] for result in results}),
        "independence_method_count": len({result["independence_method"] for result in results}),
        "external_source_reference_count": len(
            {result["external_source_reference"] for result in results}
        ),
        "benchmark_count": len({result["benchmark_name"] for result in results}),
        "source_record_type_count": len({result["source_record_type"] for result in results}),
        "mapping_method_count": len({result["mapping_method"] for result in results}),
        "source_file_count": len({result["source_file"] for result in results}),
        "source_file_hash_count": len({result["source_file_hash"] for result in results}),
        "source_group_count": len({result["source_group_id"] for result in results}),
        "provider_count": len({result["provider"] for result in results}),
        "model_count": len({result["model_name"] for result in results}),
        "model_version_count": len({result["model_version"] for result in results}),
        "answer_extraction_method_count": len(
            {result["answer_extraction_method"] for result in results}
        ),
        "cross_provider_group_count": len({result["cross_provider_group"] for result in results}),
        "trajectory_count": len(results),
        "event_count": sum(result["event_count"] for result in results),
    }


def validate_expected_boundaries(records: List[Dict[str, Any]], results: List[Dict[str, Any]]) -> None:
    expected_single_values = {
        "source": "gsm_symbolic_cross_provider_disagreement_v13",
        "source_independence": "external_source_verified",
        "independence_method": "cross_provider_real_model_output_disagreement_mapping",
        "benchmark_name": "GSM-Symbolic",
        "source_record_type": "cross_provider_real_model_output_file",
        "mapping_method": "cross_provider_real_model_output_file_to_trajectory",
        "answer_extraction_method": "final_numeric_answer_extractor_v1",
    }

    for key, expected in expected_single_values.items():
        actual_values = unique_sorted(records, key)
        if actual_values != [expected]:
            raise AssertionError(f"{key} expected {[expected]}, got {actual_values}")

    providers = unique_sorted(records, "provider")
    if providers != ["provider_a", "provider_b"]:
        raise AssertionError(f"providers expected ['provider_a', 'provider_b'], got {providers}")

    trajectory_ids = unique_sorted(records, "trajectory_id")
    if len(trajectory_ids) != 10:
        raise AssertionError(f"expected 10 trajectories, got {len(trajectory_ids)}")

    cross_provider_groups = unique_sorted(records, "cross_provider_group")
    if len(cross_provider_groups) != 5:
        raise AssertionError(
            f"expected 5 cross_provider_groups, got {len(cross_provider_groups)}"
        )

    for trajectory_id, events in group_by(records, "trajectory_id").items():
        steps = [event["step"] for event in sorted(events, key=lambda event: event["step"])]
        if steps != [1, 2, 3, 4, 5]:
            raise AssertionError(f"{trajectory_id} expected steps [1,2,3,4,5], got {steps}")

    if len(results) != 10:
        raise AssertionError(f"expected 10 trajectory results, got {len(results)}")


def main() -> None:
    banner("TEMPORAL COLLAPSE CROSS-PROVIDER DISAGREEMENT VALIDATOR — v13")

    banner("INPUT FILE")
    print(INPUT_FILE)

    banner("LIMITATION NOTE")
    print(LIMITATION_NOTE)

    records = load_jsonl(INPUT_FILE)

    trajectories = group_by(records, "trajectory_id")
    results = [
        build_trajectory_result(trajectory_id, events)
        for trajectory_id, events in sorted(trajectories.items())
    ]
    results = sorted(results, key=lambda result: result["risk_score"], reverse=True)

    validate_expected_boundaries(records, results)

    source_summary = [
        summarize_group("source_file", source_file, group_results)
        for source_file, group_results in sorted(group_by(results, "source_file").items())
    ]

    provider_summary = [
        summarize_group("provider", provider, group_results)
        for provider, group_results in sorted(group_by(results, "provider").items())
    ]

    source_group_summary = [
        summarize_group("source_group_id", source_group_id, group_results)
        for source_group_id, group_results in sorted(group_by(results, "source_group_id").items())
    ]

    cross_provider_summary = build_cross_provider_summary(results)
    aggregate = build_aggregate(results)

    output = {
        "experiment": EXPERIMENT,
        "status": STATUS,
        "boundary": (
            "cross-provider real parsed GSM-Symbolic model-output file records "
            "mapped into raw ordered structural trajectory events"
        ),
        "claim": (
            "This script applies the Level 3 raw trajectory warning mechanism to "
            "cross-provider real parsed GSM-Symbolic model-output file records mapped "
            "into raw ordered structural trajectory events. It does not claim that "
            "OMNIA solves GSM-Symbolic, does not infer semantic truth, does not replace "
            "benchmark correctness, and does not make final decisions."
        ),
        "limitation_note": LIMITATION_NOTE,
        "input_file": str(INPUT_FILE),
        "trajectory_count": len(results),
        "event_count": len(records),
        "source_count": len(unique_sorted(records, "source")),
        "source_independence_values": unique_sorted(records, "source_independence"),
        "independence_method_values": unique_sorted(records, "independence_method"),
        "external_source_references": unique_sorted(records, "external_source_reference"),
        "benchmark_names": unique_sorted(records, "benchmark_name"),
        "source_record_types": unique_sorted(records, "source_record_type"),
        "mapping_methods": unique_sorted(records, "mapping_method"),
        "source_files": unique_sorted(records, "source_file"),
        "source_file_hashes": unique_sorted(records, "source_file_hash"),
        "source_group_ids": unique_sorted(records, "source_group_id"),
        "providers": unique_sorted(records, "provider"),
        "model_names": unique_sorted(records, "model_name"),
        "model_versions": unique_sorted(records, "model_version"),
        "answer_extraction_methods": unique_sorted(records, "answer_extraction_method"),
        "cross_provider_groups": unique_sorted(records, "cross_provider_group"),
        "cross_provider_roles": unique_sorted(records, "cross_provider_role"),
        "external_source_note": (
            "source_independence=external_source_verified means the mapped records preserve "
            "a public/documentable GSM-Symbolic benchmark reference. "
            "independence_method=cross_provider_real_model_output_disagreement_mapping means "
            "the records include source-file fields, provider identity, model identity, run "
            "identity, response identity, answer-extraction fields, correctness fields, and "
            "cross-provider group fields. Correctness, extraction, and provider disagreement "
            "are reported as evidence; risk_score remains a structural warning measurement."
        ),
        "weights": WEIGHTS,
        "thresholds": THRESHOLDS,
        "aggregate": aggregate,
        "source_summary": source_summary,
        "provider_summary": provider_summary,
        "source_group_summary": source_group_summary,
        "cross_provider_summary": cross_provider_summary,
        "results": results,
    }

    banner("SOURCE SUMMARY")
    print(json.dumps(source_summary, indent=2, ensure_ascii=False))

    banner("PROVIDER SUMMARY")
    print(json.dumps(provider_summary, indent=2, ensure_ascii=False))

    banner("CROSS-PROVIDER SUMMARY")
    print(json.dumps(cross_provider_summary, indent=2, ensure_ascii=False))

    banner("TRAJECTORY RESULTS")
    for result in results:
        print()
        print(f"trajectory_id:              {result['trajectory_id']}")
        print(f"provider:                   {result['provider']}")
        print(f"source_group_id:            {result['source_group_id']}")
        print(f"cross_provider_group:       {result['cross_provider_group']}")
        print(f"template_id:                {result['template_id']}")
        print(f"model_name:                 {result['model_name']}")
        print(f"model_version:              {result['model_version']}")
        print(f"source_file:                {result['source_file']}")
        print(f"source_file_hash:           {result['source_file_hash']}")
        print(f"event_count:                {result['event_count']}")
        print(f"risk_regime:                {result['risk_regime']}")
        print(f"risk_score:                 {result['risk_score']}")
        print(f"gate_action:                {result['gate_action']}")
        print(f"dominant_axis:              {result['dominant_axis']}")
        print(f"warning_flags:              {result['warning_flags']}")
        print(f"correctness_profile:        {result['correctness_profile']}")
        print(f"extraction_profile:         {result['extraction_profile']}")
        print(f"signals:                    {result['signals']}")

    banner("AGGREGATE")
    print(json.dumps(aggregate, indent=2, ensure_ascii=False))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    banner(f"Wrote result file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()