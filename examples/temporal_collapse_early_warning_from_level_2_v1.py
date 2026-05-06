#!/usr/bin/env python3
"""
Temporal Collapse Early Warning from Level 2 — v1

This script applies the Level 3 early-warning layer to trajectory-like
records derived from existing Level 2 temporal-collapse topology results.

It does not predict semantic truth.
It does not make final decisions.
It measures structural warning conditions only.

measurement != inference != decision
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
OUTPUT_PATH = RESULTS_DIR / "temporal_collapse_early_warning_from_level_2_v1.json"


LEVEL_2_RESULT_FILES = [
    "temporal_collapse_topology_cluster_adjacency_graph_v0.json",
    "temporal_collapse_topology_cluster_graph_centrality_v0.json",
    "temporal_collapse_topology_cluster_graph_control_plane_v0.json",
    "temporal_collapse_topology_control_plane_robustness_v0.json",
    "temporal_collapse_topology_dependency_map_v0.json",
    "temporal_collapse_topology_dependency_boundary_v0.json",
    "temporal_collapse_topology_boundary_phase_diagram_v0.json",
]


WEIGHTS = {
    "transition_density": 0.20,
    "drift_score": 0.20,
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


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def safe_load_json(path: Path) -> dict:
    if not path.exists():
        return {
            "missing": True,
            "path": str(path.relative_to(ROOT)),
        }

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "missing": False,
            "load_error": str(exc),
            "path": str(path.relative_to(ROOT)),
        }


def flatten_numbers(obj) -> list[float]:
    numbers = []

    if isinstance(obj, bool):
        return numbers

    if isinstance(obj, (int, float)):
        numbers.append(float(obj))
        return numbers

    if isinstance(obj, dict):
        for value in obj.values():
            numbers.extend(flatten_numbers(value))
        return numbers

    if isinstance(obj, list):
        for item in obj:
            numbers.extend(flatten_numbers(item))
        return numbers

    return numbers


def count_status_markers(obj) -> dict[str, int]:
    markers = {
        "PASS": 0,
        "CHECK": 0,
        "FAIL": 0,
        "STOP": 0,
        "WATCH": 0,
        "ESCALATE": 0,
        "CRITICAL": 0,
        "COLLAPSE": 0,
        "DRIFT": 0,
        "STABLE": 0,
    }

    def walk(value) -> None:
        if isinstance(value, str):
            token = value.strip().upper()
            if token in markers:
                markers[token] += 1

        elif isinstance(value, dict):
            for item in value.values():
                walk(item)

        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(obj)
    return markers


def file_signal_from_payload(payload: dict) -> dict:
    """
    Converts a Level 2 JSON payload into a bounded signal snapshot.

    This is intentionally conservative:
    - missing files create risk pressure
    - CHECK markers create boundary pressure
    - FAIL/COLLAPSE markers create collapse pressure
    - numeric dispersion creates drift pressure
    """

    if payload.get("missing"):
        return {
            "source_status": "MISSING",
            "transition_density": 0.40,
            "drift_score": 0.40,
            "boundary_proximity": 0.60,
            "collapse_similarity": 0.30,
            "irreversibility_signal": 0.20,
        }

    if payload.get("load_error"):
        return {
            "source_status": "LOAD_ERROR",
            "transition_density": 0.50,
            "drift_score": 0.50,
            "boundary_proximity": 0.70,
            "collapse_similarity": 0.40,
            "irreversibility_signal": 0.30,
        }

    markers = count_status_markers(payload)
    numbers = flatten_numbers(payload)

    pass_count = markers["PASS"]
    check_count = markers["CHECK"]
    fail_count = markers["FAIL"] + markers["STOP"] + markers["COLLAPSE"]

    total_markers = max(1, pass_count + check_count + fail_count)

    check_ratio = check_count / total_markers
    fail_ratio = fail_count / total_markers

    if numbers:
        numeric_mean = clamp01(abs(mean(numbers)))
        numeric_range = clamp01(max(numbers) - min(numbers))
    else:
        numeric_mean = 0.0
        numeric_range = 0.0

    transition_density = clamp01(check_ratio + (0.50 * fail_ratio))
    drift_score = clamp01((numeric_mean + numeric_range + check_ratio) / 3.0)
    boundary_proximity = clamp01((check_ratio * 0.70) + (fail_ratio * 0.90) + (numeric_range * 0.30))
    collapse_similarity = clamp01((fail_ratio * 0.80) + (check_ratio * 0.30))
    irreversibility_signal = clamp01(fail_ratio)

    return {
        "source_status": "LOADED",
        "transition_density": transition_density,
        "drift_score": drift_score,
        "boundary_proximity": boundary_proximity,
        "collapse_similarity": collapse_similarity,
        "irreversibility_signal": irreversibility_signal,
    }


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


def dominant_axis(signals: dict[str, float]) -> str:
    return max(WEIGHTS.keys(), key=lambda key: signals[key])


def warning_flags(signals: dict[str, float]) -> list[str]:
    flags = []

    if signals["transition_density"] >= 0.50:
        flags.append("high_transition_density")

    if signals["drift_score"] >= 0.50:
        flags.append("high_drift_score")

    if signals["boundary_proximity"] >= 0.60:
        flags.append("boundary_proximity")

    if signals["collapse_similarity"] >= 0.60:
        flags.append("collapse_similarity")

    if signals["irreversibility_signal"] >= 0.50:
        flags.append("irreversibility_signal")

    return flags


def analyze_level_2_file(filename: str) -> dict:
    path = RESULTS_DIR / filename
    payload = safe_load_json(path)
    raw_signals = file_signal_from_payload(payload)

    signals = {
        key: raw_signals[key]
        for key in WEIGHTS
    }

    risk_score = compute_risk_score(signals)
    risk_regime = classify_regime(risk_score)

    return {
        "source_file": f"results/{filename}",
        "source_status": raw_signals["source_status"],
        "risk_regime": risk_regime,
        "risk_score": round(risk_score, 6),
        "gate_action": GATE_ACTIONS[risk_regime],
        "dominant_axis": dominant_axis(signals),
        "warning_flags": warning_flags(signals),
        "signals": {
            key: round(value, 6)
            for key, value in signals.items()
        },
    }


def aggregate_results(results: list[dict]) -> dict:
    scores = [item["risk_score"] for item in results]

    regime_counts = {}
    for item in results:
        regime = item["risk_regime"]
        regime_counts[regime] = regime_counts.get(regime, 0) + 1

    if not scores:
        return {
            "aggregate_risk_score": 0.0,
            "aggregate_risk_regime": "STABLE",
            "regime_counts": {},
        }

    aggregate_score = clamp01(mean(scores))
    aggregate_regime = classify_regime(aggregate_score)

    return {
        "aggregate_risk_score": round(aggregate_score, 6),
        "aggregate_risk_regime": aggregate_regime,
        "aggregate_gate_action": GATE_ACTIONS[aggregate_regime],
        "regime_counts": regime_counts,
    }


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    results = [
        analyze_level_2_file(filename)
        for filename in LEVEL_2_RESULT_FILES
    ]

    aggregate = aggregate_results(results)

    payload = {
        "experiment": "temporal_collapse_early_warning_from_level_2_v1",
        "status": "v1_level_2_derived",
        "boundary": "derived from existing Level 2 temporal-collapse result files",
        "claim": (
            "This script applies the Level 3 early-warning layer to "
            "trajectory-like snapshots derived from Level 2 result files."
        ),
        "level_2_result_files": [
            f"results/{filename}"
            for filename in LEVEL_2_RESULT_FILES
        ],
        "weights": WEIGHTS,
        "thresholds": THRESHOLDS,
        "aggregate": aggregate,
        "results": results,
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 100)
    print("TEMPORAL COLLAPSE EARLY WARNING FROM LEVEL 2 — v1")
    print("=" * 100)

    for result in results:
        print()
        print(f"source_file:   {result['source_file']}")
        print(f"source_status: {result['source_status']}")
        print(f"risk_regime:   {result['risk_regime']}")
        print(f"risk_score:    {result['risk_score']}")
        print(f"gate_action:   {result['gate_action']}")
        print(f"dominant_axis: {result['dominant_axis']}")
        print(f"warning_flags: {result['warning_flags']}")

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