#!/usr/bin/env python3
"""
TEMPORAL COLLAPSE REPEATED-RUN CROSS-PROVIDER STABILITY VALIDATOR — v14

Boundary:
- Reads repeated-run cross-provider GSM-Symbolic mapped JSONL records.
- Groups raw ordered structural events into trajectories.
- Measures structural warning signals across repeated runs and providers.
- Does not solve GSM-Symbolic.
- Does not infer semantic truth.
- Does not replace benchmark correctness.
- Does not make final decisions.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


INPUT_FILE = Path("data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl")
OUTPUT_FILE = Path("results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json")

EXPERIMENT = "temporal_collapse_repeated_run_cross_provider_stability_validator_v14"
STATUS = "v14_repeated_run_cross_provider_stability_mapping"

BOUNDARY = (
    "repeated-run cross-provider real parsed GSM-Symbolic model-output file records "
    "mapped into raw ordered structural trajectory events"
)

CLAIM = (
    "This script applies the Level 3 raw trajectory warning mechanism to repeated-run "
    "cross-provider real parsed GSM-Symbolic model-output file records mapped into raw "
    "ordered structural trajectory events. It does not claim that OMNIA solves GSM-Symbolic, "
    "does not infer semantic truth, does not replace benchmark correctness, and does not make "
    "final decisions."
)

LIMITATION_NOTE = (
    "Repeated-run cross-provider stability validation does not imply official benchmark scoring, "
    "production certification, semantic truth detection, or final decision authority."
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


REQUIRED_KEYS = {
    "trajectory_id",
    "step",
    "template_id",
    "question_id",
    "variant_type",
    "provider",
    "model_name",
    "model_version",
    "run_id",
    "run_index",
    "run_group_id",
    "response_id",
    "source_file",
    "source_file_hash",
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
    "stability_group",
    "cross_provider_group",
    "cross_provider_role",
    "mapping_notes",
}


def banner(title: str) -> None:
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def round6(value: float) -> float:
    return round(float(value), 6)


def unique_sorted(records: list[dict[str, Any]], key: str) -> list[Any]:
    return sorted({record[key] for record in records})


def count_changes(values: list[Any]) -> float:
    if len(values) <= 1:
        return 0.0
    return sum(1 for a, b in zip(values, values[1:]) if a != b) / (len(values) - 1)


def phase_rank(phase: str) -> int:
    order = {
        "STABLE": 0,
        "DRIFT": 1,
        "CRITICAL": 2,
        "COLLAPSE": 3,
    }
    return order.get(str(phase), 0)


def classify_regime(score: float) -> str:
    if score < THRESHOLDS["STABLE"]:
        return "STABLE"
    if score < THRESHOLDS["DRIFT"]:
        return "DRIFT"
    return "CRITICAL"


def gate_action(regime: str) -> str:
    if regime == "STABLE":
        return "PASS"
    if regime == "DRIFT":
        return "WATCH"
    return "ESCALATE"


def dominant_axis(signals: dict[str, float]) -> str:
    return max(signals.items(), key=lambda item: item[1])[0]


def warning_flags(signals: dict[str, float]) -> list[str]:
    flags: list[str] = []

    if signals["transition_density"] >= 0.55:
        flags.append("high_transition_density")
    if signals["drift_progression"] >= 0.50:
        flags.append("high_drift_progression")
    if signals["boundary_proximity"] >= 0.70:
        flags.append("boundary_proximity")
    if signals["collapse_similarity"] >= 0.35:
        flags.append("collapse_similarity")
    if signals["irreversibility_signal"] >= 0.50:
        flags.append("irreversibility_signal")

    return flags


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    records: list[dict[str, Any]] = []

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at line {line_number}: {exc}") from exc

        missing = sorted(REQUIRED_KEYS - set(record))
        if missing:
            raise ValueError(f"Missing required keys at line {line_number}: {missing}")

        records.append(record)

    return records


def validate_records(records: list[dict[str, Any]]) -> None:
    if not records:
        raise ValueError("Input file contains no records.")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record["trajectory_id"]].append(record)

    bad_steps = {}
    for trajectory_id, events in grouped.items():
        steps = sorted(event["step"] for event in events)
        if steps != [1, 2, 3, 4, 5]:
            bad_steps[trajectory_id] = steps

    if bad_steps:
        raise ValueError(f"Bad trajectory step structure: {bad_steps}")

    expected_single_values = {
        "source": ["gsm_symbolic_repeated_run_cross_provider_stability_v14"],
        "source_independence": ["external_source_verified"],
        "independence_method": ["repeated_run_cross_provider_stability_mapping"],
        "benchmark_name": ["GSM-Symbolic"],
        "source_record_type": ["repeated_run_real_model_output_file"],
        "mapping_method": ["repeated_run_real_model_output_file_to_trajectory"],
        "answer_extraction_method": ["final_numeric_answer_extractor_v1"],
    }

    for key, expected in expected_single_values.items():
        observed = unique_sorted(records, key)
        if observed != expected:
            raise ValueError(f"Unexpected values for {key}: observed={observed}, expected={expected}")


def correctness_profile(events: list[dict[str, Any]]) -> dict[str, Any]:
    correctness = [bool(event["is_correct"]) for event in events]
    correct_count = sum(1 for value in correctness if value)
    incorrect_count = len(correctness) - correct_count

    return {
        "event_count": len(events),
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "accuracy_rate": round6(correct_count / len(events)),
        "correctness_changes": round6(count_changes(correctness)),
        "starts_correct": correctness[0],
        "ends_correct": correctness[-1],
    }


def extraction_profile(events: list[dict[str, Any]]) -> dict[str, Any]:
    extracted = [event["model_final_answer"] != "not_extracted" for event in events]
    extracted_count = sum(1 for value in extracted if value)
    not_extracted_count = len(extracted) - extracted_count

    return {
        "event_count": len(events),
        "extracted_count": extracted_count,
        "not_extracted_count": not_extracted_count,
        "extraction_rate": round6(extracted_count / len(events)),
        "extraction_changes": round6(count_changes(extracted)),
        "starts_extracted": extracted[0],
        "ends_extracted": extracted[-1],
        "answer_extraction_methods": sorted({event["answer_extraction_method"] for event in events}),
    }


def analyze_trajectory(events: list[dict[str, Any]]) -> dict[str, Any]:
    events = sorted(events, key=lambda event: event["step"])

    first = events[0]

    signatures = [event["signature"] for event in events]
    clusters = [event["cluster"] for event in events]
    phases = [event["phase"] for event in events]
    deltas = [float(event["delta"]) for event in events]
    iris = [float(event["iri"]) for event in events]
    boundary_distances = [float(event["boundary_distance"]) for event in events]
    model_answers = [event["model_final_answer"] for event in events]

    cp = correctness_profile(events)
    ep = extraction_profile(events)

    signature_changes = count_changes(signatures)
    cluster_changes = count_changes(clusters)
    phase_changes = count_changes(phases)

    delta_early_mean = mean(deltas[:2])
    delta_late_mean = mean(deltas[-2:])
    iri_early_mean = mean(iris[:2])
    iri_late_mean = mean(iris[-2:])

    boundary_proximities = [1.0 - value for value in boundary_distances]
    max_boundary_proximity = max(boundary_proximities)

    collapse_phase_count = sum(1 for phase in phases if phase == "COLLAPSE")
    broken_signature_count = sum(1 for signature in signatures if "BROKEN" in signature)
    not_extracted_signature_count = sum(1 for answer in model_answers if answer == "not_extracted")

    transition_density = mean(
        [
            signature_changes,
            cluster_changes,
            phase_changes,
            cp["correctness_changes"],
            ep["extraction_changes"],
        ]
    )

    drift_progression = max(0.0, delta_late_mean - delta_early_mean)
    boundary_proximity = max_boundary_proximity

    collapse_similarity = mean(
        [
            collapse_phase_count / len(events),
            broken_signature_count / len(events),
            not_extracted_signature_count / len(events),
            1.0 if phases[-1] == "COLLAPSE" else 0.0,
        ]
    )

    irreversibility_signal = max(max(iris), iri_late_mean)

    signals = {
        "transition_density": round6(transition_density),
        "drift_progression": round6(drift_progression),
        "boundary_proximity": round6(boundary_proximity),
        "collapse_similarity": round6(collapse_similarity),
        "irreversibility_signal": round6(irreversibility_signal),
    }

    risk_score = round6(
        signals["transition_density"] * WEIGHTS["transition_density"]
        + signals["drift_progression"] * WEIGHTS["drift_progression"]
        + signals["boundary_proximity"] * WEIGHTS["boundary_proximity"]
        + signals["collapse_similarity"] * WEIGHTS["collapse_similarity"]
        + signals["irreversibility_signal"] * WEIGHTS["irreversibility_signal"]
    )

    risk_regime = classify_regime(risk_score)

    transition_evidence = {
        "signature_changes": round6(signature_changes),
        "cluster_changes": round6(cluster_changes),
        "phase_changes": round6(phase_changes),
        "delta_early_mean": round6(delta_early_mean),
        "delta_late_mean": round6(delta_late_mean),
        "iri_early_mean": round6(iri_early_mean),
        "iri_late_mean": round6(iri_late_mean),
        "min_boundary_distance": round6(min(boundary_distances)),
        "max_boundary_proximity": round6(max_boundary_proximity),
        "collapse_phase_count": collapse_phase_count,
        "broken_signature_count": broken_signature_count,
        "not_extracted_signature_count": not_extracted_signature_count,
        "correctness_changes": cp["correctness_changes"],
        "extraction_changes": ep["extraction_changes"],
        "correct_count": cp["correct_count"],
        "incorrect_count": cp["incorrect_count"],
        "accuracy_rate": cp["accuracy_rate"],
        "extracted_count": ep["extracted_count"],
        "not_extracted_count": ep["not_extracted_count"],
        "extraction_rate": ep["extraction_rate"],
        "starts_correct": cp["starts_correct"],
        "ends_correct": cp["ends_correct"],
        "starts_extracted": ep["starts_extracted"],
        "ends_extracted": ep["ends_extracted"],
        "source": first["source"],
        "source_independence": first["source_independence"],
        "independence_method": first["independence_method"],
        "external_source_reference": first["external_source_reference"],
        "benchmark_name": first["benchmark_name"],
        "source_record_type": first["source_record_type"],
        "mapping_method": first["mapping_method"],
        "source_file": first["source_file"],
        "source_file_hash": first["source_file_hash"],
        "provider": first["provider"],
        "run_id": first["run_id"],
        "run_index": first["run_index"],
        "run_group_id": first["run_group_id"],
        "template_id": first["template_id"],
        "stability_group": first["stability_group"],
        "cross_provider_group": first["cross_provider_group"],
        "cross_provider_role": first["cross_provider_role"],
        "answer_extraction_method": first["answer_extraction_method"],
    }

    return {
        "trajectory_id": first["trajectory_id"],
        "source": first["source"],
        "source_independence": first["source_independence"],
        "independence_method": first["independence_method"],
        "external_source_reference": first["external_source_reference"],
        "benchmark_name": first["benchmark_name"],
        "source_record_type": first["source_record_type"],
        "mapping_method": first["mapping_method"],
        "source_file": first["source_file"],
        "source_file_hash": first["source_file_hash"],
        "provider": first["provider"],
        "model_name": first["model_name"],
        "model_version": first["model_version"],
        "run_id": first["run_id"],
        "run_index": first["run_index"],
        "run_group_id": first["run_group_id"],
        "template_id": first["template_id"],
        "stability_group": first["stability_group"],
        "cross_provider_group": first["cross_provider_group"],
        "cross_provider_role": first["cross_provider_role"],
        "answer_extraction_method": first["answer_extraction_method"],
        "source_record_reference": "multiple_source_record_references",
        "mapping_notes": "multiple_mapping_notes",
        "response_id": "multiple_response_ids",
        "question_id": "multiple_question_ids",
        "variant_type": "multiple_variant_types",
        "raw_question_hash": "multiple_raw_question_hashes",
        "raw_output_hash": "multiple_raw_output_hashes",
        "expected_answer": "multiple_expected_answers",
        "model_final_answer": "multiple_model_final_answers",
        "correctness_profile": cp,
        "extraction_profile": ep,
        "event_count": len(events),
        "risk_regime": risk_regime,
        "risk_score": risk_score,
        "gate_action": gate_action(risk_regime),
        "dominant_axis": dominant_axis(signals),
        "warning_flags": warning_flags(signals),
        "signals": signals,
        "transition_evidence": transition_evidence,
    }


def summarize_group(name: str, group_value: str, results: list[dict[str, Any]]) -> dict[str, Any]:
    regime_counts = dict(sorted(Counter(result["risk_regime"] for result in results).items()))
    highest = max(results, key=lambda result: result["risk_score"])

    return {
        name: group_value,
        "trajectory_count": len(results),
        "event_count": sum(result["event_count"] for result in results),
        "average_risk_score": round6(mean(result["risk_score"] for result in results)),
        "average_accuracy_rate": round6(mean(result["correctness_profile"]["accuracy_rate"] for result in results)),
        "average_extraction_rate": round6(mean(result["extraction_profile"]["extraction_rate"] for result in results)),
        "regime_counts": regime_counts,
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
        "providers": sorted({result["provider"] for result in results}),
        "model_names": sorted({result["model_name"] for result in results}),
        "model_versions": sorted({result["model_version"] for result in results}),
        "run_ids": sorted({result["run_id"] for result in results}),
        "run_indexes": sorted({result["run_index"] for result in results}),
        "run_group_ids": sorted({result["run_group_id"] for result in results}),
        "stability_groups": sorted({result["stability_group"] for result in results}),
        "cross_provider_groups": sorted({result["cross_provider_group"] for result in results}),
        "cross_provider_roles": sorted({result["cross_provider_role"] for result in results}),
        "answer_extraction_methods": sorted({result["answer_extraction_method"] for result in results}),
    }


def summarize_cross_provider_group(group_value: str, results: list[dict[str, Any]]) -> dict[str, Any]:
    provider_risk_scores = {
        result["provider"] + "_run_" + str(result["run_index"]): result["risk_score"]
        for result in results
    }
    provider_risk_regimes = {
        result["provider"] + "_run_" + str(result["run_index"]): result["risk_regime"]
        for result in results
    }
    provider_accuracy_rates = {
        result["provider"] + "_run_" + str(result["run_index"]): result["correctness_profile"]["accuracy_rate"]
        for result in results
    }
    provider_extraction_rates = {
        result["provider"] + "_run_" + str(result["run_index"]): result["extraction_profile"]["extraction_rate"]
        for result in results
    }

    risk_values = list(provider_risk_scores.values())
    accuracy_values = list(provider_accuracy_rates.values())
    extraction_values = list(provider_extraction_rates.values())

    highest = max(results, key=lambda result: result["risk_score"])

    return {
        "cross_provider_group": group_value,
        "template_ids": sorted({result["template_id"] for result in results}),
        "providers": sorted({result["provider"] for result in results}),
        "run_ids": sorted({result["run_id"] for result in results}),
        "run_indexes": sorted({result["run_index"] for result in results}),
        "trajectory_ids": sorted(result["trajectory_id"] for result in results),
        "provider_run_risk_scores": provider_risk_scores,
        "provider_run_risk_regimes": provider_risk_regimes,
        "provider_run_accuracy_rates": provider_accuracy_rates,
        "provider_run_extraction_rates": provider_extraction_rates,
        "cross_provider_risk_spread": round6(max(risk_values) - min(risk_values)),
        "cross_provider_accuracy_spread": round6(max(accuracy_values) - min(accuracy_values)),
        "cross_provider_extraction_spread": round6(max(extraction_values) - min(extraction_values)),
        "risk_regime_disagreement": len(set(provider_risk_regimes.values())) > 1,
        "accuracy_disagreement": len(set(accuracy_values)) > 1,
        "extraction_disagreement": len(set(extraction_values)) > 1,
        "highest_risk_provider": highest["provider"],
        "highest_risk_run_id": highest["run_id"],
        "highest_risk_trajectory": highest["trajectory_id"],
        "highest_risk_score": highest["risk_score"],
    }


def summarize_stability_group(group_value: str, results: list[dict[str, Any]]) -> dict[str, Any]:
    risk_scores = [result["risk_score"] for result in results]
    accuracy_rates = [result["correctness_profile"]["accuracy_rate"] for result in results]
    extraction_rates = [result["extraction_profile"]["extraction_rate"] for result in results]
    highest = max(results, key=lambda result: result["risk_score"])

    return {
        "stability_group": group_value,
        "template_ids": sorted({result["template_id"] for result in results}),
        "provider": sorted({result["provider"] for result in results})[0],
        "run_ids": sorted({result["run_id"] for result in results}),
        "run_indexes": sorted({result["run_index"] for result in results}),
        "trajectory_ids": sorted(result["trajectory_id"] for result in results),
        "run_risk_scores": {result["run_id"]: result["risk_score"] for result in results},
        "run_risk_regimes": {result["run_id"]: result["risk_regime"] for result in results},
        "run_accuracy_rates": {result["run_id"]: result["correctness_profile"]["accuracy_rate"] for result in results},
        "run_extraction_rates": {result["run_id"]: result["extraction_profile"]["extraction_rate"] for result in results},
        "repeated_run_risk_spread": round6(max(risk_scores) - min(risk_scores)),
        "repeated_run_accuracy_spread": round6(max(accuracy_rates) - min(accuracy_rates)),
        "repeated_run_extraction_spread": round6(max(extraction_rates) - min(extraction_rates)),
        "repeated_run_risk_regime_disagreement": len({result["risk_regime"] for result in results}) > 1,
        "highest_risk_run_id": highest["run_id"],
        "highest_risk_trajectory": highest["trajectory_id"],
        "highest_risk_score": highest["risk_score"],
    }


def build_result(records: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record["trajectory_id"]].append(record)

    results = [analyze_trajectory(events) for events in grouped.values()]
    results.sort(key=lambda result: result["risk_score"], reverse=True)

    regime_counts = dict(sorted(Counter(result["risk_regime"] for result in results).items()))
    highest = max(results, key=lambda result: result["risk_score"])

    by_source_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_provider: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_run: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_stability_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_cross_provider_group: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for result in results:
        by_source_file[result["source_file"]].append(result)
        by_provider[result["provider"]].append(result)
        by_run[result["run_id"]].append(result)
        by_stability_group[result["stability_group"]].append(result)
        by_cross_provider_group[result["cross_provider_group"]].append(result)

    source_summary = [
        summarize_group("source_file", source_file, group_results)
        for source_file, group_results in sorted(by_source_file.items())
    ]

    provider_summary = [
        summarize_group("provider", provider, group_results)
        for provider, group_results in sorted(by_provider.items())
    ]

    run_summary = [
        summarize_group("run_id", run_id, group_results)
        for run_id, group_results in sorted(by_run.items())
    ]

    stability_group_summary = [
        summarize_stability_group(stability_group, group_results)
        for stability_group, group_results in sorted(by_stability_group.items())
    ]

    cross_provider_summary = [
        summarize_cross_provider_group(cross_provider_group, group_results)
        for cross_provider_group, group_results in sorted(by_cross_provider_group.items())
    ]

    aggregate = {
        "aggregate_risk_score": round6(mean(result["risk_score"] for result in results)),
        "aggregate_risk_regime": classify_regime(mean(result["risk_score"] for result in results)),
        "aggregate_gate_action": gate_action(classify_regime(mean(result["risk_score"] for result in results))),
        "aggregate_accuracy_rate": round6(mean(result["correctness_profile"]["accuracy_rate"] for result in results)),
        "aggregate_extraction_rate": round6(mean(result["extraction_profile"]["extraction_rate"] for result in results)),
        "regime_counts": regime_counts,
        "highest_risk_trajectory": highest["trajectory_id"],
        "highest_risk_score": highest["risk_score"],
        "highest_risk_provider": highest["provider"],
        "highest_risk_run_id": highest["run_id"],
        "source_count": len({record["source"] for record in records}),
        "independence_method_count": len({record["independence_method"] for record in records}),
        "external_source_reference_count": len({record["external_source_reference"] for record in records}),
        "benchmark_count": len({record["benchmark_name"] for record in records}),
        "source_record_type_count": len({record["source_record_type"] for record in records}),
        "mapping_method_count": len({record["mapping_method"] for record in records}),
        "source_file_count": len({record["source_file"] for record in records}),
        "source_file_hash_count": len({record["source_file_hash"] for record in records}),
        "provider_count": len({record["provider"] for record in records}),
        "model_count": len({record["model_name"] for record in records}),
        "model_version_count": len({record["model_version"] for record in records}),
        "run_count": len({record["run_id"] for record in records}),
        "run_group_count": len({record["run_group_id"] for record in records}),
        "answer_extraction_method_count": len({record["answer_extraction_method"] for record in records}),
        "stability_group_count": len({record["stability_group"] for record in records}),
        "cross_provider_group_count": len({record["cross_provider_group"] for record in records}),
        "trajectory_count": len(results),
        "event_count": len(records),
    }

    return {
        "experiment": EXPERIMENT,
        "status": STATUS,
        "boundary": BOUNDARY,
        "claim": CLAIM,
        "limitation_note": LIMITATION_NOTE,
        "input_file": str(INPUT_FILE),
        "trajectory_count": len(results),
        "event_count": len(records),
        "source_count": len({record["source"] for record in records}),
        "source_independence_values": unique_sorted(records, "source_independence"),
        "independence_method_values": unique_sorted(records, "independence_method"),
        "external_source_references": unique_sorted(records, "external_source_reference"),
        "benchmark_names": unique_sorted(records, "benchmark_name"),
        "source_record_types": unique_sorted(records, "source_record_type"),
        "mapping_methods": unique_sorted(records, "mapping_method"),
        "source_files": unique_sorted(records, "source_file"),
        "source_file_hashes": unique_sorted(records, "source_file_hash"),
        "providers": unique_sorted(records, "provider"),
        "model_names": unique_sorted(records, "model_name"),
        "model_versions": unique_sorted(records, "model_version"),
        "run_ids": unique_sorted(records, "run_id"),
        "run_group_ids": unique_sorted(records, "run_group_id"),
        "answer_extraction_methods": unique_sorted(records, "answer_extraction_method"),
        "stability_groups": unique_sorted(records, "stability_group"),
        "cross_provider_groups": unique_sorted(records, "cross_provider_group"),
        "cross_provider_roles": unique_sorted(records, "cross_provider_role"),
        "external_source_note": (
            "source_independence=external_source_verified means the mapped records preserve a "
            "public/documentable GSM-Symbolic benchmark reference. "
            "independence_method=repeated_run_cross_provider_stability_mapping means the records "
            "include source-file fields, provider identity, model identity, run identity, repeated-run "
            "identity, response identity, answer-extraction fields, correctness fields, stability-group "
            "fields, and cross-provider group fields. Correctness, extraction, repeated-run spread, and "
            "cross-provider spread are reported as evidence; risk_score remains a structural warning "
            "measurement."
        ),
        "weights": WEIGHTS,
        "thresholds": THRESHOLDS,
        "aggregate": aggregate,
        "source_summary": source_summary,
        "provider_summary": provider_summary,
        "run_summary": run_summary,
        "stability_group_summary": stability_group_summary,
        "cross_provider_summary": cross_provider_summary,
        "results": results,
    }


def main() -> None:
    banner("TEMPORAL COLLAPSE REPEATED-RUN CROSS-PROVIDER STABILITY VALIDATOR — v14")

    banner("INPUT FILE")
    print(INPUT_FILE)

    banner("LIMITATION NOTE")
    print(LIMITATION_NOTE)

    records = load_jsonl(INPUT_FILE)
    validate_records(records)

    result = build_result(records)

    banner("SOURCE SUMMARY")
    print(json.dumps(result["source_summary"], indent=2, ensure_ascii=False))

    banner("PROVIDER SUMMARY")
    print(json.dumps(result["provider_summary"], indent=2, ensure_ascii=False))

    banner("RUN SUMMARY")
    print(json.dumps(result["run_summary"], indent=2, ensure_ascii=False))

    banner("STABILITY GROUP SUMMARY")
    print(json.dumps(result["stability_group_summary"], indent=2, ensure_ascii=False))

    banner("CROSS-PROVIDER SUMMARY")
    print(json.dumps(result["cross_provider_summary"], indent=2, ensure_ascii=False))

    banner("TRAJECTORY RESULTS")
    for item in result["results"]:
        print()
        print(f"trajectory_id:              {item['trajectory_id']}")
        print(f"provider:                   {item['provider']}")
        print(f"run_id:                     {item['run_id']}")
        print(f"run_index:                  {item['run_index']}")
        print(f"stability_group:            {item['stability_group']}")
        print(f"cross_provider_group:       {item['cross_provider_group']}")
        print(f"template_id:                {item['template_id']}")
        print(f"model_name:                 {item['model_name']}")
        print(f"model_version:              {item['model_version']}")
        print(f"source_file:                {item['source_file']}")
        print(f"source_file_hash:           {item['source_file_hash']}")
        print(f"event_count:                {item['event_count']}")
        print(f"risk_regime:                {item['risk_regime']}")
        print(f"risk_score:                 {item['risk_score']}")
        print(f"gate_action:                {item['gate_action']}")
        print(f"dominant_axis:              {item['dominant_axis']}")
        print(f"warning_flags:              {item['warning_flags']}")
        print(f"correctness_profile:        {item['correctness_profile']}")
        print(f"extraction_profile:         {item['extraction_profile']}")
        print(f"signals:                    {item['signals']}")

    banner("AGGREGATE")
    print(json.dumps(result["aggregate"], indent=2, ensure_ascii=False))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    banner(f"Wrote result file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()