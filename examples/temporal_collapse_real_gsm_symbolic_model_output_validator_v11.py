#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Temporal Collapse Real GSM-Symbolic Model Output Validator — v11

Reads:
    data/temporal_collapse_real_gsm_symbolic_model_outputs_v11.jsonl

Writes:
    results/temporal_collapse_real_gsm_symbolic_model_output_validator_v11.json

Boundary:
    real parsed GSM-Symbolic model-output file records mapped into raw ordered
    structural trajectory events.

Important:
    This validator does not claim that OMNIA solves GSM-Symbolic.
    This validator does not infer semantic truth.
    This validator does not replace benchmark correctness.
    Real parsed model-output file validation does not imply official benchmark scoring.

measurement != inference != decision
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean


INPUT_FILE = Path("data/temporal_collapse_real_gsm_symbolic_model_outputs_v11.jsonl")
OUTPUT_FILE = Path("results/temporal_collapse_real_gsm_symbolic_model_output_validator_v11.json")

EXPERIMENT = "temporal_collapse_real_gsm_symbolic_model_output_validator_v11"

BOUNDARY = (
    "real parsed GSM-Symbolic model-output file records mapped into raw ordered "
    "structural trajectory events"
)

CLAIM = (
    "This script applies the Level 3 raw trajectory warning mechanism to real "
    "parsed GSM-Symbolic model-output file records mapped into raw ordered "
    "structural trajectory events. It does not claim that OMNIA solves "
    "GSM-Symbolic, does not infer semantic truth, and does not replace "
    "benchmark correctness."
)

LIMITATION_NOTE = (
    "Real parsed model-output file validation does not imply official benchmark scoring."
)

EXTERNAL_SOURCE_NOTE = (
    "source_independence=external_source_verified means the mapped records preserve "
    "a public/documentable GSM-Symbolic benchmark reference. "
    "independence_method=real_model_output_file_mapping means the records include "
    "source-file fields such as source_file, source_file_hash, source_record_reference, "
    "provider, model_name, model_version, run_id, response_id, raw_question_hash, "
    "raw_output_hash, answer_extraction_method, expected_answer, model_final_answer, "
    "and is_correct. Correctness and extraction are reported as evidence; risk_score "
    "remains a structural warning measurement."
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

REQUIRED_FIELDS = [
    "trajectory_id",
    "step",
    "template_id",
    "question_id",
    "variant_type",
    "model_name",
    "model_version",
    "provider",
    "run_id",
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
    "mapping_notes",
]

EXPECTED_BOUNDARY_VALUES = {
    "source_independence": "external_source_verified",
    "independence_method": "real_model_output_file_mapping",
    "source_record_type": "real_model_output_file",
    "mapping_method": "real_model_output_file_to_trajectory",
}


def banner(title: str) -> None:
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at line {line_number}: {exc}") from exc
        record["_line_number"] = line_number
        records.append(record)

    if not records:
        raise ValueError(f"Input file is empty: {path}")

    return records


def validate_required_fields(records: list[dict]) -> None:
    errors = []

    for record in records:
        line_number = record.get("_line_number", "?")

        for field in REQUIRED_FIELDS:
            if field not in record:
                errors.append(f"line {line_number}: missing required field {field}")

        for field, expected in EXPECTED_BOUNDARY_VALUES.items():
            actual = record.get(field)
            if actual != expected:
                errors.append(
                    f"line {line_number}: expected {field}={expected!r}, got {actual!r}"
                )

        for numeric_field in ["step", "delta", "iri", "boundary_distance"]:
            if numeric_field in record:
                value = record[numeric_field]
                if not isinstance(value, (int, float)):
                    errors.append(
                        f"line {line_number}: {numeric_field} must be numeric, got {type(value).__name__}"
                    )

        if "is_correct" in record and not isinstance(record["is_correct"], bool):
            errors.append(f"line {line_number}: is_correct must be boolean")

        if "source_file" in record and not record["source_file"]:
            errors.append(f"line {line_number}: source_file must not be empty")

        if "source_file_hash" in record and not str(record["source_file_hash"]).startswith("sha256:"):
            errors.append(f"line {line_number}: source_file_hash must start with sha256:")

        if "raw_question_hash" in record and not str(record["raw_question_hash"]).startswith("sha256:"):
            errors.append(f"line {line_number}: raw_question_hash must start with sha256:")

        if "raw_output_hash" in record and not str(record["raw_output_hash"]).startswith("sha256:"):
            errors.append(f"line {line_number}: raw_output_hash must start with sha256:")

    if errors:
        joined = "\n".join(errors)
        raise ValueError(f"Validation failed:\n{joined}")


def group_by_trajectory(records: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        grouped[record["trajectory_id"]].append(record)

    for trajectory_id, events in grouped.items():
        events.sort(key=lambda item: item["step"])

        expected_steps = list(range(1, len(events) + 1))
        actual_steps = [event["step"] for event in events]
        if actual_steps != expected_steps:
            raise ValueError(
                f"Trajectory {trajectory_id} has non-contiguous steps: {actual_steps}, "
                f"expected {expected_steps}"
            )

    return dict(grouped)


def fraction_changes(values: list[str]) -> float:
    if len(values) <= 1:
        return 0.0

    changes = 0
    for previous, current in zip(values, values[1:]):
        if previous != current:
            changes += 1

    return round(changes / (len(values) - 1), 6)


def split_early_late(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0

    midpoint = max(1, len(values) // 2)
    early = values[:midpoint]
    late = values[midpoint:]

    if not late:
        late = values

    return round(mean(early), 6), round(mean(late), 6)


def correctness_profile(events: list[dict]) -> dict:
    correctness = [bool(event["is_correct"]) for event in events]
    correct_count = sum(1 for value in correctness if value)
    incorrect_count = len(correctness) - correct_count

    return {
        "event_count": len(events),
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "accuracy_rate": round(correct_count / len(events), 6),
        "correctness_changes": fraction_changes([str(value) for value in correctness]),
        "starts_correct": correctness[0],
        "ends_correct": correctness[-1],
    }


def extraction_profile(events: list[dict]) -> dict:
    extracted = [
        str(event.get("model_final_answer", "")).strip().lower() not in {
            "",
            "not_extracted",
            "none",
            "null",
        }
        for event in events
    ]

    extracted_count = sum(1 for value in extracted if value)
    not_extracted_count = len(extracted) - extracted_count

    methods = sorted({event["answer_extraction_method"] for event in events})

    return {
        "event_count": len(events),
        "extracted_count": extracted_count,
        "not_extracted_count": not_extracted_count,
        "extraction_rate": round(extracted_count / len(events), 6),
        "extraction_changes": fraction_changes([str(value) for value in extracted]),
        "starts_extracted": extracted[0],
        "ends_extracted": extracted[-1],
        "answer_extraction_methods": methods,
    }


def compute_signals(events: list[dict]) -> tuple[dict, dict]:
    signatures = [event["signature"] for event in events]
    clusters = [event["cluster"] for event in events]
    phases = [event["phase"] for event in events]

    deltas = [float(event["delta"]) for event in events]
    iris = [float(event["iri"]) for event in events]
    boundary_distances = [float(event["boundary_distance"]) for event in events]

    signature_changes = fraction_changes(signatures)
    cluster_changes = fraction_changes(clusters)
    phase_changes = fraction_changes(phases)

    delta_early_mean, delta_late_mean = split_early_late(deltas)
    iri_early_mean, iri_late_mean = split_early_late(iris)

    delta_progression = max(0.0, delta_late_mean - delta_early_mean)
    iri_progression = max(0.0, iri_late_mean - iri_early_mean)

    min_boundary_distance = round(min(boundary_distances), 6)
    max_boundary_proximity = round(1.0 - min_boundary_distance, 6)

    collapse_phase_count = sum(1 for phase in phases if phase.upper() == "COLLAPSE")
    broken_signature_count = sum(
        1 for signature in signatures if "BROKEN" in signature.upper()
    )
    not_extracted_signature_count = sum(
        1 for signature in signatures if "NOT_EXTRACTED" in signature.upper()
    )

    transition_density = round(
        (signature_changes + cluster_changes + phase_changes) / 3.0,
        6,
    )

    drift_progression = round(
        min(1.0, (delta_progression * 0.65) + (iri_progression * 0.35)),
        6,
    )

    boundary_proximity = round(max_boundary_proximity, 6)

    collapse_similarity = round(
        min(
            1.0,
            (collapse_phase_count / max(1, len(events))) * 0.45
            + (broken_signature_count / max(1, len(events))) * 0.25
            + (not_extracted_signature_count / max(1, len(events))) * 0.15
            + max(0.0, delta_late_mean) * 0.10
            + max(0.0, iri_late_mean) * 0.05,
        ),
        6,
    )

    irreversibility_signal = round(min(1.0, iri_late_mean), 6)

    signals = {
        "transition_density": transition_density,
        "drift_progression": drift_progression,
        "boundary_proximity": boundary_proximity,
        "collapse_similarity": collapse_similarity,
        "irreversibility_signal": irreversibility_signal,
    }

    evidence = {
        "signature_changes": signature_changes,
        "cluster_changes": cluster_changes,
        "phase_changes": phase_changes,
        "delta_early_mean": delta_early_mean,
        "delta_late_mean": delta_late_mean,
        "iri_early_mean": iri_early_mean,
        "iri_late_mean": iri_late_mean,
        "min_boundary_distance": min_boundary_distance,
        "max_boundary_proximity": max_boundary_proximity,
        "collapse_phase_count": collapse_phase_count,
        "broken_signature_count": broken_signature_count,
        "not_extracted_signature_count": not_extracted_signature_count,
    }

    return signals, evidence


def risk_score(signals: dict) -> float:
    score = 0.0
    for key, weight in WEIGHTS.items():
        score += weight * float(signals[key])
    return round(score, 6)


def classify(score: float) -> str:
    if score < THRESHOLDS["STABLE"]:
        return "STABLE"
    if score < THRESHOLDS["DRIFT"]:
        return "DRIFT"
    if score < THRESHOLDS["CRITICAL"]:
        return "CRITICAL"
    return "COLLAPSE"


def gate_action(regime: str) -> str:
    return {
        "STABLE": "PASS",
        "DRIFT": "WATCH",
        "CRITICAL": "ESCALATE",
        "COLLAPSE": "STOP",
    }[regime]


def warning_flags(signals: dict) -> list[str]:
    flags = []

    if signals["transition_density"] >= 0.50:
        flags.append("high_transition_density")
    if signals["drift_progression"] >= 0.50:
        flags.append("high_drift_progression")
    if signals["boundary_proximity"] >= 0.70:
        flags.append("boundary_proximity")
    if signals["collapse_similarity"] >= 0.50:
        flags.append("collapse_similarity")
    if signals["irreversibility_signal"] >= 0.70:
        flags.append("irreversibility_signal")

    return flags


def summarize_value(values: list[str]) -> str:
    unique = sorted(set(values))
    if len(unique) == 1:
        return unique[0]
    return f"multiple_{values[0].split('_')[0] if values else 'values'}"


def compact_multiple(values: list[str], label: str) -> str:
    unique = sorted(set(values))
    if len(unique) == 1:
        return unique[0]
    return f"multiple_{label}"


def build_result(trajectory_id: str, events: list[dict]) -> dict:
    first = events[0]

    signals, transition_evidence = compute_signals(events)
    correctness = correctness_profile(events)
    extraction = extraction_profile(events)

    transition_evidence.update(
        {
            "correctness_changes": correctness["correctness_changes"],
            "extraction_changes": extraction["extraction_changes"],
            "correct_count": correctness["correct_count"],
            "incorrect_count": correctness["incorrect_count"],
            "accuracy_rate": correctness["accuracy_rate"],
            "extracted_count": extraction["extracted_count"],
            "not_extracted_count": extraction["not_extracted_count"],
            "extraction_rate": extraction["extraction_rate"],
            "starts_correct": correctness["starts_correct"],
            "ends_correct": correctness["ends_correct"],
            "starts_extracted": extraction["starts_extracted"],
            "ends_extracted": extraction["ends_extracted"],
            "source": first["source"],
            "source_independence": first["source_independence"],
            "independence_method": first["independence_method"],
            "external_source_reference": first["external_source_reference"],
            "benchmark_name": first["benchmark_name"],
            "source_record_type": first["source_record_type"],
            "source_record_reference": compact_multiple(
                [event["source_record_reference"] for event in events],
                "source_record_references",
            ),
            "mapping_method": first["mapping_method"],
            "mapping_notes": compact_multiple(
                [event["mapping_notes"] for event in events],
                "mapping_notes",
            ),
            "source_file": first["source_file"],
            "source_file_hash": first["source_file_hash"],
            "model_name": first["model_name"],
            "model_version": first["model_version"],
            "provider": first["provider"],
            "run_id": first["run_id"],
            "response_id": compact_multiple(
                [event["response_id"] for event in events],
                "response_ids",
            ),
            "template_id": first["template_id"],
            "question_id": compact_multiple(
                [event["question_id"] for event in events],
                "question_ids",
            ),
            "variant_type": compact_multiple(
                [event["variant_type"] for event in events],
                "variant_types",
            ),
            "raw_question_hash": compact_multiple(
                [event["raw_question_hash"] for event in events],
                "raw_question_hashes",
            ),
            "raw_output_hash": compact_multiple(
                [event["raw_output_hash"] for event in events],
                "raw_output_hashes",
            ),
            "answer_extraction_method": first["answer_extraction_method"],
            "expected_answer": compact_multiple(
                [event["expected_answer"] for event in events],
                "expected_answers",
            ),
            "model_final_answer": compact_multiple(
                [event["model_final_answer"] for event in events],
                "model_final_answers",
            ),
        }
    )

    score = risk_score(signals)
    regime = classify(score)

    dominant_axis = max(signals.items(), key=lambda item: item[1])[0]

    return {
        "trajectory_id": trajectory_id,
        "source": first["source"],
        "source_independence": first["source_independence"],
        "independence_method": first["independence_method"],
        "external_source_reference": first["external_source_reference"],
        "benchmark_name": first["benchmark_name"],
        "source_record_type": first["source_record_type"],
        "source_record_reference": compact_multiple(
            [event["source_record_reference"] for event in events],
            "source_record_references",
        ),
        "mapping_method": first["mapping_method"],
        "mapping_notes": compact_multiple(
            [event["mapping_notes"] for event in events],
            "mapping_notes",
        ),
        "source_file": first["source_file"],
        "source_file_hash": first["source_file_hash"],
        "model_name": first["model_name"],
        "model_version": first["model_version"],
        "provider": first["provider"],
        "run_id": first["run_id"],
        "response_id": compact_multiple(
            [event["response_id"] for event in events],
            "response_ids",
        ),
        "template_id": first["template_id"],
        "question_id": compact_multiple(
            [event["question_id"] for event in events],
            "question_ids",
        ),
        "variant_type": compact_multiple(
            [event["variant_type"] for event in events],
            "variant_types",
        ),
        "raw_question_hash": compact_multiple(
            [event["raw_question_hash"] for event in events],
            "raw_question_hashes",
        ),
        "raw_output_hash": compact_multiple(
            [event["raw_output_hash"] for event in events],
            "raw_output_hashes",
        ),
        "answer_extraction_method": first["answer_extraction_method"],
        "expected_answer": compact_multiple(
            [event["expected_answer"] for event in events],
            "expected_answers",
        ),
        "model_final_answer": compact_multiple(
            [event["model_final_answer"] for event in events],
            "model_final_answers",
        ),
        "correctness_profile": correctness,
        "extraction_profile": extraction,
        "event_count": len(events),
        "risk_regime": regime,
        "risk_score": score,
        "gate_action": gate_action(regime),
        "dominant_axis": dominant_axis,
        "warning_flags": warning_flags(signals),
        "signals": signals,
        "transition_evidence": transition_evidence,
    }


def aggregate_results(results: list[dict]) -> dict:
    scores = [item["risk_score"] for item in results]
    accuracy_rates = [item["correctness_profile"]["accuracy_rate"] for item in results]
    extraction_rates = [item["extraction_profile"]["extraction_rate"] for item in results]

    aggregate_score = round(mean(scores), 6)
    aggregate_regime = classify(aggregate_score)

    highest = max(results, key=lambda item: item["risk_score"])

    return {
        "aggregate_risk_score": aggregate_score,
        "aggregate_risk_regime": aggregate_regime,
        "aggregate_gate_action": gate_action(aggregate_regime),
        "aggregate_accuracy_rate": round(mean(accuracy_rates), 6),
        "aggregate_extraction_rate": round(mean(extraction_rates), 6),
        "regime_counts": dict(sorted(Counter(item["risk_regime"] for item in results).items())),
        "highest_risk_trajectory": highest["trajectory_id"],
        "highest_risk_score": highest["risk_score"],
        "source_count": len({item["source"] for item in results}),
        "independence_method_count": len({item["independence_method"] for item in results}),
        "external_source_reference_count": len({item["external_source_reference"] for item in results}),
        "benchmark_count": len({item["benchmark_name"] for item in results}),
        "source_record_type_count": len({item["source_record_type"] for item in results}),
        "mapping_method_count": len({item["mapping_method"] for item in results}),
        "source_file_count": len({item["source_file"] for item in results}),
        "source_file_hash_count": len({item["source_file_hash"] for item in results}),
        "model_count": len({item["model_name"] for item in results}),
        "model_version_count": len({item["model_version"] for item in results}),
        "provider_count": len({item["provider"] for item in results}),
        "answer_extraction_method_count": len(
            {item["answer_extraction_method"] for item in results}
        ),
    }


def build_source_summary(results: list[dict]) -> list[dict]:
    grouped = defaultdict(list)

    for item in results:
        key = (
            item["source"],
            item["source_independence"],
            item["independence_method"],
            item["external_source_reference"],
            item["benchmark_name"],
            item["source_record_type"],
            item["mapping_method"],
            item["source_file"],
            item["source_file_hash"],
            item["model_name"],
            item["model_version"],
            item["provider"],
            item["answer_extraction_method"],
        )
        grouped[key].append(item)

    summary = []

    for key, items in grouped.items():
        (
            source,
            source_independence,
            independence_method,
            external_source_reference,
            benchmark_name,
            source_record_type,
            mapping_method,
            source_file,
            source_file_hash,
            model_name,
            model_version,
            provider,
            answer_extraction_method,
        ) = key

        highest = max(items, key=lambda item: item["risk_score"])

        summary.append(
            {
                "source": source,
                "source_independence": source_independence,
                "independence_method": independence_method,
                "external_source_reference": external_source_reference,
                "benchmark_name": benchmark_name,
                "source_record_type": source_record_type,
                "mapping_method": mapping_method,
                "source_file": source_file,
                "source_file_hash": source_file_hash,
                "model_name": model_name,
                "model_version": model_version,
                "provider": provider,
                "answer_extraction_method": answer_extraction_method,
                "trajectory_count": len(items),
                "average_risk_score": round(mean(item["risk_score"] for item in items), 6),
                "average_accuracy_rate": round(
                    mean(item["correctness_profile"]["accuracy_rate"] for item in items),
                    6,
                ),
                "average_extraction_rate": round(
                    mean(item["extraction_profile"]["extraction_rate"] for item in items),
                    6,
                ),
                "regime_counts": dict(
                    sorted(Counter(item["risk_regime"] for item in items).items())
                ),
                "highest_risk_trajectory": highest["trajectory_id"],
                "highest_risk_score": highest["risk_score"],
            }
        )

    summary.sort(
        key=lambda item: (
            item["source"],
            item["model_name"],
            item["model_version"],
            item["average_risk_score"],
        )
    )

    return summary


def strip_internal_fields(records: list[dict]) -> list[dict]:
    clean = []
    for record in records:
        item = dict(record)
        item.pop("_line_number", None)
        clean.append(item)
    return clean


def main() -> None:
    banner("TEMPORAL COLLAPSE REAL GSM-SYMBOLIC MODEL OUTPUT VALIDATOR — v11")

    banner("INPUT FILE")
    print(INPUT_FILE)

    records = load_jsonl(INPUT_FILE)
    validate_required_fields(records)

    grouped = group_by_trajectory(records)

    results = []
    for trajectory_id, events in grouped.items():
        results.append(build_result(trajectory_id, events))

    results.sort(key=lambda item: item["risk_score"], reverse=True)

    aggregate = aggregate_results(results)
    source_summary = build_source_summary(results)

    payload = {
        "experiment": EXPERIMENT,
        "status": "v11_real_model_output_file_mapping",
        "boundary": BOUNDARY,
        "claim": CLAIM,
        "limitation_note": LIMITATION_NOTE,
        "input_file": str(INPUT_FILE),
        "trajectory_count": len(results),
        "source_count": len({record["source"] for record in records}),
        "source_independence_values": sorted(
            {record["source_independence"] for record in records}
        ),
        "independence_method_values": sorted(
            {record["independence_method"] for record in records}
        ),
        "external_source_references": sorted(
            {record["external_source_reference"] for record in records}
        ),
        "benchmark_names": sorted({record["benchmark_name"] for record in records}),
        "source_record_types": sorted({record["source_record_type"] for record in records}),
        "mapping_methods": sorted({record["mapping_method"] for record in records}),
        "source_files": sorted({record["source_file"] for record in records}),
        "source_file_hashes": sorted({record["source_file_hash"] for record in records}),
        "model_names": sorted({record["model_name"] for record in records}),
        "model_versions": sorted({record["model_version"] for record in records}),
        "providers": sorted({record["provider"] for record in records}),
        "answer_extraction_methods": sorted(
            {record["answer_extraction_method"] for record in records}
        ),
        "external_source_note": EXTERNAL_SOURCE_NOTE,
        "weights": WEIGHTS,
        "thresholds": THRESHOLDS,
        "aggregate": aggregate,
        "source_summary": source_summary,
        "results": results,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    banner("LIMITATION NOTE")
    print(LIMITATION_NOTE)

    banner("SOURCE SUMMARY")
    print(json.dumps(source_summary, indent=2))

    banner("TRAJECTORY RESULTS")
    for item in results:
        print()
        print(f"trajectory_id:              {item['trajectory_id']}")
        print(f"template_id:                {item['template_id']}")
        print(f"question_id:                {item['question_id']}")
        print(f"variant_type:               {item['variant_type']}")
        print(f"source_file:                {item['source_file']}")
        print(f"source_file_hash:           {item['source_file_hash']}")
        print(f"provider:                   {item['provider']}")
        print(f"model_name:                 {item['model_name']}")
        print(f"model_version:              {item['model_version']}")
        print(f"run_id:                     {item['run_id']}")
        print(f"response_id:                {item['response_id']}")
        print(f"raw_question_hash:          {item['raw_question_hash']}")
        print(f"raw_output_hash:            {item['raw_output_hash']}")
        print(f"answer_extraction_method:   {item['answer_extraction_method']}")
        print(f"expected_answer:            {item['expected_answer']}")
        print(f"model_final_answer:         {item['model_final_answer']}")
        print(f"correctness_profile:        {item['correctness_profile']}")
        print(f"extraction_profile:         {item['extraction_profile']}")
        print(f"source:                     {item['source']}")
        print(f"source_independence:        {item['source_independence']}")
        print(f"independence_method:        {item['independence_method']}")
        print(f"external_source_reference:  {item['external_source_reference']}")
        print(f"benchmark_name:             {item['benchmark_name']}")
        print(f"source_record_type:         {item['source_record_type']}")
        print(f"source_record_reference:    {item['source_record_reference']}")
        print(f"mapping_method:             {item['mapping_method']}")
        print(f"mapping_notes:              {item['mapping_notes']}")
        print(f"event_count:                {item['event_count']}")
        print(f"risk_regime:                {item['risk_regime']}")
        print(f"risk_score:                 {item['risk_score']}")
        print(f"gate_action:                {item['gate_action']}")
        print(f"dominant_axis:              {item['dominant_axis']}")
        print(f"warning_flags:              {item['warning_flags']}")
        print(f"signals:                    {item['signals']}")
        print(f"evidence:                   {item['transition_evidence']}")

    banner("AGGREGATE")
    print(json.dumps(aggregate, indent=2))

    banner(f"Wrote result file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()