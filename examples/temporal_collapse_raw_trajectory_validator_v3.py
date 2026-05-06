#!/usr/bin/env python3
"""
Temporal Collapse Raw Trajectory Validator — v3

This script validates Level 3 early-warning measurement over raw ordered
trajectory records.

v0 tested synthetic reference trajectories.
v1 converted Level 2 result files into trajectory-like snapshots.
v2 evaluated an ordered Level 2 stage trajectory.
v3 reads raw ordered trajectory events directly.

It does not predict semantic truth.
It does not make final decisions.
It measures structural warning conditions only.

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

INPUT_PATH = DATA_DIR / "temporal_collapse_raw_trajectories_v3.jsonl"
OUTPUT_PATH = RESULTS_DIR / "temporal_collapse_raw_trajectory_validator_v3.json"


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
    "signature",
    "cluster",
    "delta",
    "iri",
    "boundary_distance",
    "phase",
}


DEFAULT_RAW_TRAJECTORIES = [
    # Stable raw trajectory
    {
        "trajectory_id": "raw_stable_001",
        "step": 1,
        "signature": "S0",
        "cluster": "C0",
        "delta": 0.03,
        "iri": 0.01,
        "boundary_distance": 0.96,
        "phase": "STABLE",
    },
    {
        "trajectory_id": "raw_stable_001",
        "step": 2,
        "signature": "S0",
        "cluster": "C0",
        "delta": 0.04,
        "iri": 0.01,
        "boundary_distance": 0.94,
        "phase": "STABLE",
    },
    {
        "trajectory_id": "raw_stable_001",
        "step": 3,
        "signature": "S0",
        "cluster": "C0",
        "delta": 0.05,
        "iri": 0.02,
        "boundary_distance": 0.93,
        "phase": "STABLE",
    },
    {
        "trajectory_id": "raw_stable_001",
        "step": 4,
        "signature": "S0",
        "cluster": "C0",
        "delta": 0.04,
        "iri": 0.02,
        "boundary_distance": 0.92,
        "phase": "STABLE",
    },

    # Drift raw trajectory
    {
        "trajectory_id": "raw_drift_001",
        "step": 1,
        "signature": "S0",
        "cluster": "C0",
        "delta": 0.08,
        "iri": 0.03,
        "boundary_distance": 0.88,
        "phase": "STABLE",
    },
    {
        "trajectory_id": "raw_drift_001",
        "step": 2,
        "signature": "S0",
        "cluster": "C0",
        "delta": 0.14,
        "iri": 0.06,
        "boundary_distance": 0.78,
        "phase": "STABLE",
    },
    {
        "trajectory_id": "raw_drift_001",
        "step": 3,
        "signature": "S1",
        "cluster": "C1",
        "delta": 0.25,
        "iri": 0.10,
        "boundary_distance": 0.62,
        "phase": "DRIFT",
    },
    {
        "trajectory_id": "raw_drift_001",
        "step": 4,
        "signature": "S1",
        "cluster": "C1",
        "delta": 0.34,
        "iri": 0.15,
        "boundary_distance": 0.55,
        "phase": "DRIFT",
    },

    # Critical raw trajectory
    {
        "trajectory_id": "raw_critical_001",
        "step": 1,
        "signature": "S0",
        "cluster": "C0",
        "delta": 0.16,
        "iri": 0.08,
        "boundary_distance": 0.75,
        "phase": "STABLE",
    },
    {
        "trajectory_id": "raw_critical_001",
        "step": 2,
        "signature": "S1",
        "cluster": "C1",
        "delta": 0.32,
        "iri": 0.16,
        "boundary_distance": 0.55,
        "phase": "DRIFT",
    },
    {
        "trajectory_id": "raw_critical_001",
        "step": 3,
        "signature": "S2",
        "cluster": "C2",
        "delta": 0.55,
        "iri": 0.30,
        "boundary_distance": 0.32,
        "phase": "CRITICAL",
    },
    {
        "trajectory_id": "raw_critical_001",
        "step": 4,
        "signature": "S3",
        "cluster": "C2",
        "delta": 0.68,
        "iri": 0.42,
        "boundary_distance": 0.20,
        "phase": "CRITICAL",
    },

    # Collapse-like raw trajectory
    {
        "trajectory_id": "raw_collapse_like_001",
        "step": 1,
        "signature": "S0",
        "cluster": "C0",
        "delta": 0.22,
        "iri": 0.14,
        "boundary_distance": 0.66,
        "phase": "DRIFT",
    },
    {
        "trajectory_id": "raw_collapse_like_001",
        "step": 2,
        "signature": "S2",
        "cluster": "C2",
        "delta": 0.52,
        "iri": 0.34,
        "boundary_distance": 0.36,
        "phase": "CRITICAL",
    },
    {
        "trajectory_id": "raw_collapse_like_001",
        "step": 3,
        "signature": "S9",
        "cluster": "C9",
        "delta": 0.84,
        "iri": 0.68,
        "boundary_distance": 0.12,
        "phase": "COLLAPSE",
    },
    {
        "trajectory_id": "raw_collapse_like_001",
        "step": 4,
        "signature": "BROKEN",
        "cluster": "C9",
        "delta": 0.96,
        "iri": 0.90,
        "boundary_distance": 0.04,
        "phase": "COLLAPSE",
    },
]


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


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


def mean_or_zero(values: list[float]) -> float:
    return mean(values) if values else 0.0


def ensure_default_input_file() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    if INPUT_PATH.exists():
        return

    lines = [
        json.dumps(item, sort_keys=True)
        for item in DEFAULT_RAW_TRAJECTORIES
    ]

    INPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_jsonl(path: Path) -> list[dict]:
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
    }


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)

    ensure_default_input_file()

    records = read_jsonl(INPUT_PATH)
    grouped = group_trajectories(records)

    results = [
        analyze_trajectory(trajectory_id, events)
        for trajectory_id, events in sorted(grouped.items())
    ]

    aggregate = aggregate_results(results)

    payload = {
        "experiment": "temporal_collapse_raw_trajectory_validator_v3",
        "status": "v3_raw_ordered_trajectory_records",
        "boundary": "raw ordered trajectory records in JSONL format",
        "claim": (
            "This script measures structural warning risk directly over "
            "raw ordered trajectory events using visible signals, weights, "
            "thresholds, and transition evidence."
        ),
        "input_file": str(INPUT_PATH.relative_to(ROOT)),
        "trajectory_count": len(results),
        "weights": WEIGHTS,
        "thresholds": THRESHOLDS,
        "aggregate": aggregate,
        "results": results,
    }

    OUTPUT_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    print("=" * 100)
    print("TEMPORAL COLLAPSE RAW TRAJECTORY VALIDATOR — v3")
    print("=" * 100)

    print()
    print("INPUT FILE")
    print("=" * 100)
    print(INPUT_PATH.relative_to(ROOT))

    print()
    print("TRAJECTORY RESULTS")
    print("=" * 100)

    for result in results:
        print()
        print(f"trajectory_id: {result['trajectory_id']}")
        print(f"event_count:   {result['event_count']}")
        print(f"risk_regime:   {result['risk_regime']}")
        print(f"risk_score:    {result['risk_score']}")
        print(f"gate_action:   {result['gate_action']}")
        print(f"dominant_axis: {result['dominant_axis']}")
        print(f"warning_flags: {result['warning_flags']}")
        print(f"signals:       {result['signals']}")
        print(f"evidence:      {result['transition_evidence']}")

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