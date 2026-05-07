#!/usr/bin/env python3
# ============================================================
# OMNIA-VALIDATION
# Temporal Collapse Multi-Source Real GSM-Symbolic
# Model Output Validator — v12
# ============================================================

import json
from collections import Counter, defaultdict
from pathlib import Path


INPUT_FILE = Path("data/temporal_collapse_multi_source_real_gsm_symbolic_model_outputs_v12.jsonl")
RESULT_FILE = Path("results/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.json")

EXPERIMENT = "temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12"

STATUS = "v12_multi_source_real_model_output_file_mapping"

BOUNDARY = (
    "multi-source real parsed GSM-Symbolic model-output file records mapped "
    "into raw ordered structural trajectory events"
)

CLAIM = (
    "This script applies the Level 3 raw trajectory warning mechanism to "
    "multi-source real parsed GSM-Symbolic model-output file records mapped "
    "into raw ordered structural trajectory events. It does not claim that "
    "OMNIA solves GSM-Symbolic, does not infer semantic truth, does not "
    "replace benchmark correctness, and does not make final decisions."
)

LIMITATION_NOTE = (
    "Multi-source real parsed model-output file validation does not imply "
    "official benchmark scoring, production certification, or semantic truth detection."
)

EXTERNAL_SOURCE_NOTE = (
    "source_independence=external_source_verified means the mapped records preserve "
    "a public/documentable GSM-Symbolic benchmark reference. "
    "independence_method=multi_source_real_model_output_file_mapping means the records "
    "include source-file fields, provider identity, model identity, run identity, "
    "response identity, answer-extraction fields, correctness fields, and cross-source "
    "group fields. Correctness and extraction are reported as evidence; risk_score "
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

GATE_ACTIONS = {
    "STABLE": "PASS",
    "DRIFT": "WATCH",
    "CRITICAL": "ESCALATE",
    "COLLAPSE": "STOP",
}


REQUIRED_EVENT_KEYS = [
    "trajectory_id",
    "step",
    "source_group_id",
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
    "cross_source_group",
    "cross_source_role",
]


def banner(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    records = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc

    return records


def require_keys(records: list[dict]) -> None:
    for index, record in enumerate(records, start=1):
        missing = [key for key in REQUIRED_EVENT_KEYS if key not in record]
        if missing:
            raise ValueError(
                f"Record {index} is missing required keys: {missing}"
            )


def unique_sorted(records: list[dict], key: str) -> list:
    return sorted({record.get(key) for record in records})


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 6)


def safe_rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 6)


def transition_rate(values: list) -> float:
    if len(values) <= 1:
        return 0.0
    changes = sum(1 for a, b in zip(values, values[1:]) if a != b)
    return round(changes / (len(values) - 1), 6)


def classify_risk(score: float) -> str:
    if score < THRESHOLDS["STABLE"]:
        return "STABLE"
    if score < THRESHOLDS["DRIFT"]:
        return "DRIFT"
    if score < THRESHOLDS["CRITICAL"]:
        return "CRITICAL"
    return "COLLAPSE"


def gate_action_for(regime: str) -> str:
    return GATE_ACTIONS[regime]


def split_early_late(values: list[float]) -> tuple[list[float], list[float]]:
    if not values:
        return [], []
    midpoint = max(1, len(values) // 2)
    return values[:midpoint], values[midpoint:]


def compute_correctness_profile(events: list[dict]) -> dict:
    correctness = [bool(event["is_correct"]) for event in events]
    event_count = len(correctness)
    correct_count = sum(1 for value in correctness if value)
    incorrect_count = event_count - correct_count

    return {
        "event_count": event_count,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "accuracy_rate": safe_rate(correct_count, event_count),
        "correctness_changes": transition_rate(correctness),
        "starts_correct": correctness[0] if correctness else False,
        "ends_correct": correctness[-1] if correctness else False,
    }


def is_extracted(event: dict) -> bool:
    value = str(event.get("model_final_answer", "")).strip().lower()
    signature = str(event.get("signature", "")).strip().lower()
    return value not in {"", "none", "null", "not_extracted"} and "not_extracted" not in signature


def compute_extraction_profile(events: list[dict]) -> dict:
    extracted_values = [is_extracted(event) for event in events]
    event_count = len(extracted_values)
    extracted_count = sum(1 for value in extracted_values if value)
    not_extracted_count = event_count - extracted_count

    methods = sorted({event["answer_extraction_method"] for event in events})

    return {
        "event_count": event_count,
        "extracted_count": extracted_count,
        "not_extracted_count": not_extracted_count,
        "extraction_rate": safe_rate(extracted_count, event_count),
        "extraction_changes": transition_rate(extracted_values),
        "starts_extracted": extracted_values[0] if extracted_values else False,
        "ends_extracted": extracted_values[-1] if extracted_values else False,
        "answer_extraction_methods": methods,
    }


def compute_transition_evidence(events: list[dict]) -> dict:
    signatures = [event["signature"] for event in events]
    clusters = [event["cluster"] for event in events]
    phases = [event["phase"] for event in events]
    deltas = [float(event["delta"]) for event in events]
    iris = [float(event["iri"]) for event in events]
    boundary_distances = [float(event["boundary_distance"]) for event in events]

    delta_early, delta_late = split_early_late(deltas)
    iri_early, iri_late = split_early_late(iris)

    correctness_profile = compute_correctness_profile(events)
    extraction_profile = compute_extraction_profile(events)

    boundary_proximities = [1.0 - value for value in boundary_distances]

    evidence = {
        "signature_changes": transition_rate(signatures),
        "cluster_changes": transition_rate(clusters),
        "phase_changes": transition_rate(phases),
        "delta_early_mean": mean(delta_early),
        "delta_late_mean": mean(delta_late),
        "iri_early_mean": mean(iri_early),
        "iri_late_mean": mean(iri_late),
        "min_boundary_distance": round(min(boundary_distances), 6),
        "max_boundary_proximity": round(max(boundary_proximities), 6),
        "collapse_phase_count": sum(1 for phase in phases if phase == "COLLAPSE"),
        "broken_signature_count": sum(
            1 for signature in signatures
            if "BROKEN" in signature or "COLLAPSE_PRESSURE" in signature
        ),
        "not_extracted_signature_count": sum(
            1 for signature in signatures
            if "NOT_EXTRACTED" in signature
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
    }

    metadata_fields = [
        "source",
        "source_independence",
        "independence_method",
        "external_source_reference",
        "benchmark_name",
        "source_record_type",
        "mapping_method",
        "source_file",
        "source_file_hash",
        "source_group_id",
        "model_name",
        "model_version",
        "provider",
        "run_id",
        "template_id",
        "cross_source_group",
        "cross_source_role",
        "answer_extraction_method",
    ]

    for field in metadata_fields:
        values = sorted({event[field] for event in events})
        evidence[field] = values[0] if len(values) == 1 else "multiple_" + field + "s"

    multi_fields = [
        "source_record_reference",
        "mapping_notes",
        "response_id",
        "question_id",
        "variant_type",
        "raw_question_hash",
        "raw_output_hash",
        "expected_answer",
        "model_final_answer",
    ]

    for field in multi_fields:
        values = sorted({event[field] for event in events})
        evidence[field] = values[0] if len(values) == 1 else "multiple_" + field + "s"

    return evidence


def compute_signals(events: list[dict], evidence: dict) -> dict:
    deltas = [float(event["delta"]) for event in events]
    iris = [float(event["iri"]) for event in events]
    boundary_distances = [float(event["boundary_distance"]) for event in events]

    transition_density = mean([
        evidence["signature_changes"],
        evidence["cluster_changes"],
        evidence["phase_changes"],
        evidence["correctness_changes"],
        evidence["extraction_changes"],
    ])

    delta_progression = max(0.0, evidence["delta_late_mean"] - evidence["delta_early_mean"])
    iri_progression = max(0.0, evidence["iri_late_mean"] - evidence["iri_early_mean"])

    drift_progression = round(
        min(1.0, (delta_progression + iri_progression) / 2.0),
        6,
    )

    boundary_proximity = round(
        min(1.0, max(0.0, 1.0 - min(boundary_distances))),
        6,
    )

    collapse_phase_component = min(1.0, evidence["collapse_phase_count"] / max(1, len(events)))
    broken_component = min(1.0, evidence["broken_signature_count"] / max(1, len(events)))
    not_extracted_component = min(1.0, evidence["not_extracted_signature_count"] / max(1, len(events)))

    collapse_similarity = round(
        min(
            1.0,
            (
                0.35 * collapse_phase_component
                + 0.30 * broken_component
                + 0.20 * not_extracted_component
                + 0.15 * max(deltas)
            ),
        ),
        6,
    )

    irreversibility_signal = round(min(1.0, max(iris)), 6)

    return {
        "transition_density": transition_density,
        "drift_progression": drift_progression,
        "boundary_proximity": boundary_proximity,
        "collapse_similarity": collapse_similarity,
        "irreversibility_signal": irreversibility_signal,
    }


def compute_risk_score(signals: dict) -> float:
    score = sum(WEIGHTS[key] * signals[key] for key in WEIGHTS)
    return round(score, 6)


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


def dominant_axis(signals: dict) -> str:
    return max(signals, key=lambda key: signals[key])


def collapse_representative(events: list[dict]) -> dict:
    fields = [
        "trajectory_id",
        "source",
        "source_independence",
        "independence_method",
        "external_source_reference",
        "benchmark_name",
        "source_record_type",
        "mapping_method",
        "source_file",
        "source_file_hash",
        "source_group_id",
        "model_name",
        "model_version",
        "provider",
        "run_id",
        "template_id",
        "cross_source_group",
        "cross_source_role",
        "answer_extraction_method",
    ]

    out = {}
    for field in fields:
        values = sorted({event[field] for event in events})
        out[field] = values[0] if len(values) == 1 else "multiple_" + field + "s"

    multi_fields = [
        "source_record_reference",
        "mapping_notes",
        "response_id",
        "question_id",
        "variant_type",
        "raw_question_hash",
        "raw_output_hash",
        "expected_answer",
        "model_final_answer",
    ]

    for field in multi_fields:
        values = sorted({event[field] for event in events})
        out[field] = values[0] if len(values) == 1 else "multiple_" + field + "s"

    return out


def validate_trajectory_steps(grouped: dict[str, list[dict]]) -> None:
    for trajectory_id, events in grouped.items():
        steps = [int(event["step"]) for event in sorted(events, key=lambda item: int(item["step"]))]
        expected = list(range(1, len(events) + 1))
        if steps != expected:
            raise ValueError(
                f"Invalid steps for {trajectory_id}: got {steps}, expected {expected}"
            )


def analyze_trajectory(trajectory_id: str, events: list[dict]) -> dict:
    events = sorted(events, key=lambda item: int(item["step"]))

    evidence = compute_transition_evidence(events)
    signals = compute_signals(events, evidence)
    risk_score = compute_risk_score(signals)
    risk_regime = classify_risk(risk_score)
    gate_action = gate_action_for(risk_regime)

    representative = collapse_representative(events)

    result = {
        "trajectory_id": trajectory_id,
        **representative,
        "correctness_profile": compute_correctness_profile(events),
        "extraction_profile": compute_extraction_profile(events),
        "event_count": len(events),
        "risk_regime": risk_regime,
        "risk_score": risk_score,
        "gate_action": gate_action,
        "dominant_axis": dominant_axis(signals),
        "warning_flags": warning_flags(signals),
        "signals": signals,
        "transition_evidence": evidence,
    }

    return result


def summarize_group(records: list[dict], results: list[dict], group_key: str) -> list[dict]:
    grouped_results = defaultdict(list)
    for result in results:
        grouped_results[result[group_key]].append(result)

    summaries = []

    for group_value, group_results in sorted(grouped_results.items()):
        risk_scores = [item["risk_score"] for item in group_results]
        accuracy_rates = [item["correctness_profile"]["accuracy_rate"] for item in group_results]
        extraction_rates = [item["extraction_profile"]["extraction_rate"] for item in group_results]
        regime_counts = Counter(item["risk_regime"] for item in group_results)
        highest = max(group_results, key=lambda item: item["risk_score"])

        matching_events = [
            event for event in records
            if event[group_key] == group_value
        ]

        summary = {
            group_key: group_value,
            "trajectory_count": len(group_results),
            "event_count": len(matching_events),
            "average_risk_score": mean(risk_scores),
            "average_accuracy_rate": mean(accuracy_rates),
            "average_extraction_rate": mean(extraction_rates),
            "regime_counts": dict(sorted(regime_counts.items())),
            "highest_risk_trajectory": highest["trajectory_id"],
            "highest_risk_score": highest["risk_score"],
        }

        for field in [
            "source",
            "source_independence",
            "independence_method",
            "external_source_reference",
            "benchmark_name",
            "source_record_type",
            "mapping_method",
            "source_file",
            "source_file_hash",
            "source_group_id",
            "model_name",
            "model_version",
            "provider",
            "answer_extraction_method",
            "cross_source_group",
            "cross_source_role",
        ]:
            values = sorted({event[field] for event in matching_events})
            summary[field + "s"] = values

        summaries.append(summary)

    return summaries


def summarize_sources(records: list[dict], results: list[dict]) -> list[dict]:
    source_files = sorted({event["source_file"] for event in records})
    summaries = []

    for source_file in source_files:
        matching_events = [event for event in records if event["source_file"] == source_file]
        matching_trajectory_ids = sorted({event["trajectory_id"] for event in matching_events})
        matching_results = [
            result for result in results
            if result["trajectory_id"] in matching_trajectory_ids
        ]

        risk_scores = [item["risk_score"] for item in matching_results]
        accuracy_rates = [item["correctness_profile"]["accuracy_rate"] for item in matching_results]
        extraction_rates = [item["extraction_profile"]["extraction_rate"] for item in matching_results]
        regime_counts = Counter(item["risk_regime"] for item in matching_results)
        highest = max(matching_results, key=lambda item: item["risk_score"])

        summaries.append({
            "source": unique_single(matching_events, "source"),
            "source_independence": unique_single(matching_events, "source_independence"),
            "independence_method": unique_single(matching_events, "independence_method"),
            "external_source_reference": unique_single(matching_events, "external_source_reference"),
            "benchmark_name": unique_single(matching_events, "benchmark_name"),
            "source_record_type": unique_single(matching_events, "source_record_type"),
            "mapping_method": unique_single(matching_events, "mapping_method"),
            "source_file": source_file,
            "source_file_hash": unique_single(matching_events, "source_file_hash"),
            "source_group_ids": unique_sorted(matching_events, "source_group_id"),
            "providers": unique_sorted(matching_events, "provider"),
            "model_names": unique_sorted(matching_events, "model_name"),
            "model_versions": unique_sorted(matching_events, "model_version"),
            "answer_extraction_methods": unique_sorted(matching_events, "answer_extraction_method"),
            "trajectory_count": len(matching_results),
            "event_count": len(matching_events),
            "average_risk_score": mean(risk_scores),
            "average_accuracy_rate": mean(accuracy_rates),
            "average_extraction_rate": mean(extraction_rates),
            "regime_counts": dict(sorted(regime_counts.items())),
            "highest_risk_trajectory": highest["trajectory_id"],
            "highest_risk_score": highest["risk_score"],
        })

    return summaries


def unique_single(records: list[dict], key: str):
    values = unique_sorted(records, key)
    return values[0] if len(values) == 1 else values


def summarize_cross_source(records: list[dict], results: list[dict]) -> list[dict]:
    cross_groups = sorted({event["cross_source_group"] for event in records})
    summaries = []

    result_by_trajectory = {result["trajectory_id"]: result for result in results}

    for cross_group in cross_groups:
        events = [event for event in records if event["cross_source_group"] == cross_group]
        trajectory_ids = sorted({event["trajectory_id"] for event in events})
        group_results = [result_by_trajectory[trajectory_id] for trajectory_id in trajectory_ids]

        provider_scores = {}
        provider_regimes = {}
        provider_accuracy = {}
        provider_extraction = {}

        for result in group_results:
            provider = result["provider"]
            provider_scores[provider] = result["risk_score"]
            provider_regimes[provider] = result["risk_regime"]
            provider_accuracy[provider] = result["correctness_profile"]["accuracy_rate"]
            provider_extraction[provider] = result["extraction_profile"]["extraction_rate"]

        score_values = list(provider_scores.values())
        risk_spread = round(max(score_values) - min(score_values), 6) if score_values else 0.0

        highest = max(group_results, key=lambda item: item["risk_score"])

        summaries.append({
            "cross_source_group": cross_group,
            "template_ids": unique_sorted(events, "template_id"),
            "providers": unique_sorted(events, "provider"),
            "trajectory_ids": trajectory_ids,
            "provider_risk_scores": provider_scores,
            "provider_risk_regimes": provider_regimes,
            "provider_accuracy_rates": provider_accuracy,
            "provider_extraction_rates": provider_extraction,
            "cross_source_risk_spread": risk_spread,
            "highest_risk_provider": highest["provider"],
            "highest_risk_trajectory": highest["trajectory_id"],
            "highest_risk_score": highest["risk_score"],
        })

    return summaries


def aggregate_results(records: list[dict], results: list[dict]) -> dict:
    risk_scores = [result["risk_score"] for result in results]
    accuracy_rates = [result["correctness_profile"]["accuracy_rate"] for result in results]
    extraction_rates = [result["extraction_profile"]["extraction_rate"] for result in results]

    aggregate_risk_score = mean(risk_scores)
    aggregate_risk_regime = classify_risk(aggregate_risk_score)
    highest = max(results, key=lambda item: item["risk_score"])

    return {
        "aggregate_risk_score": aggregate_risk_score,
        "aggregate_risk_regime": aggregate_risk_regime,
        "aggregate_gate_action": gate_action_for(aggregate_risk_regime),
        "aggregate_accuracy_rate": mean(accuracy_rates),
        "aggregate_extraction_rate": mean(extraction_rates),
        "regime_counts": dict(sorted(Counter(result["risk_regime"] for result in results).items())),
        "highest_risk_trajectory": highest["trajectory_id"],
        "highest_risk_score": highest["risk_score"],
        "highest_risk_provider": highest["provider"],
        "source_count": len(set(event["source"] for event in records)),
        "independence_method_count": len(set(event["independence_method"] for event in records)),
        "external_source_reference_count": len(set(event["external_source_reference"] for event in records)),
        "benchmark_count": len(set(event["benchmark_name"] for event in records)),
        "source_record_type_count": len(set(event["source_record_type"] for event in records)),
        "mapping_method_count": len(set(event["mapping_method"] for event in records)),
        "source_file_count": len(set(event["source_file"] for event in records)),
        "source_file_hash_count": len(set(event["source_file_hash"] for event in records)),
        "source_group_count": len(set(event["source_group_id"] for event in records)),
        "provider_count": len(set(event["provider"] for event in records)),
        "model_count": len(set(event["model_name"] for event in records)),
        "model_version_count": len(set(event["model_version"] for event in records)),
        "answer_extraction_method_count": len(set(event["answer_extraction_method"] for event in records)),
        "cross_source_group_count": len(set(event["cross_source_group"] for event in records)),
        "trajectory_count": len(results),
        "event_count": len(records),
    }


def main() -> None:
    banner("TEMPORAL COLLAPSE MULTI-SOURCE REAL GSM-SYMBOLIC MODEL OUTPUT VALIDATOR — v12")

    banner("INPUT FILE")
    print(INPUT_FILE)

    records = load_jsonl(INPUT_FILE)
    require_keys(records)

    grouped = defaultdict(list)
    for record in records:
        grouped[record["trajectory_id"]].append(record)

    validate_trajectory_steps(grouped)

    results = [
        analyze_trajectory(trajectory_id, events)
        for trajectory_id, events in sorted(grouped.items())
    ]

    results = sorted(
        results,
        key=lambda item: item["risk_score"],
        reverse=True,
    )

    aggregate = aggregate_results(records, results)
    source_summary = summarize_sources(records, results)
    provider_summary = summarize_group(records, results, "provider")
    source_group_summary = summarize_group(records, results, "source_group_id")
    cross_source_summary = summarize_cross_source(records, results)

    payload = {
        "experiment": EXPERIMENT,
        "status": STATUS,
        "boundary": BOUNDARY,
        "claim": CLAIM,
        "limitation_note": LIMITATION_NOTE,
        "input_file": str(INPUT_FILE),
        "trajectory_count": len(results),
        "event_count": len(records),
        "source_count": len(set(record["source"] for record in records)),
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
        "cross_source_groups": unique_sorted(records, "cross_source_group"),
        "cross_source_roles": unique_sorted(records, "cross_source_role"),
        "external_source_note": EXTERNAL_SOURCE_NOTE,
        "weights": WEIGHTS,
        "thresholds": THRESHOLDS,
        "aggregate": aggregate,
        "source_summary": source_summary,
        "provider_summary": provider_summary,
        "source_group_summary": source_group_summary,
        "cross_source_summary": cross_source_summary,
        "results": results,
    }

    banner("LIMITATION NOTE")
    print(LIMITATION_NOTE)

    banner("SOURCE SUMMARY")
    print(json.dumps(source_summary, indent=2))

    banner("PROVIDER SUMMARY")
    print(json.dumps(provider_summary, indent=2))

    banner("CROSS-SOURCE SUMMARY")
    print(json.dumps(cross_source_summary, indent=2))

    banner("TRAJECTORY RESULTS")

    for result in results:
        print()
        print(f"trajectory_id:              {result['trajectory_id']}")
        print(f"provider:                   {result['provider']}")
        print(f"source_group_id:            {result['source_group_id']}")
        print(f"cross_source_group:         {result['cross_source_group']}")
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
    print(json.dumps(aggregate, indent=2))

    RESULT_FILE.parent.mkdir(parents=True, exist_ok=True)
    RESULT_FILE.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    banner(f"Wrote result file: {RESULT_FILE}")


if __name__ == "__main__":
    main()