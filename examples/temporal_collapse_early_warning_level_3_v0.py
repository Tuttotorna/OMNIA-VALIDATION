#!/usr/bin/env python3
"""
Temporal Collapse Early Warning — Level 3 v0

This script introduces a minimal bounded early-warning layer for
temporal-collapse trajectories.

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
RESULTS_DIR.mkdir(exist_ok=True)

OUTPUT_PATH = RESULTS_DIR / "temporal_collapse_early_warning_level_3_v0.json"


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


SYNTHETIC_TRAJECTORIES = [
    {
        "trajectory_id": "stable_reference_001",
        "steps": [
            {"signature": "A", "cluster": "C1", "delta": 0.05, "iri": 0.02},
            {"signature": "A", "cluster": "C1", "delta": 0.07, "iri": 0.03},
            {"signature": "A", "cluster": "C1", "delta": 0.06, "iri": 0.02},
            {"signature": "A", "cluster": "C1", "delta": 0.08, "iri": 0.03},
        ],
    },
    {
        "trajectory_id": "drift_reference_001",
        "steps": [
            {"signature": "A", "cluster": "C1", "delta": 0.10, "iri": 0.05},
            {"signature": "A", "cluster": "C1", "delta": 0.18, "iri": 0.08},
            {"signature": "B", "cluster": "C1", "delta": 0.28, "iri": 0.12},
            {"signature": "B", "cluster": "C2", "delta": 0.36, "iri": 0.18},
        ],
    },
    {
        "trajectory_id": "critical_reference_001",
        "steps": [
            {"signature": "A", "cluster": "C1", "delta": 0.20, "iri": 0.10},
            {"signature": "B", "cluster": "C2", "delta": 0.42, "iri": 0.22},
            {"signature": "C", "cluster": "C3", "delta": 0.61, "iri": 0.31},
            {"signature": "C", "cluster": "C3", "delta": 0.68, "iri": 0.40},
        ],
    },
    {
        "trajectory_id": "collapse_reference_001",
        "steps": [
            {"signature": "A", "cluster": "C1", "delta": 0.30, "iri": 0.20},
            {"signature": "B", "cluster": "C2", "delta": 0.62, "iri": 0.42},
            {"signature": "X", "cluster": "C9", "delta": 0.87, "iri": 0.70},
            {"signature": "BROKEN", "cluster": "C9", "delta": 1.00, "iri": 0.95},
        ],
    },
]


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def normalized_change_count(values: list[str]) -> float:
    if len(values) < 2:
        return 0.0

    changes = 0
    for previous, current in zip(values, values[1:]):
        if previous != current:
            changes += 1

    return changes / (len(values) - 1)


def compute_transition_density(steps: list[dict]) -> float:
    signatures = [str(step.get("signature", "")) for step in steps]
    clusters = [str(step.get("cluster", "")) for step in steps]

    signature_change = normalized_change_count(signatures)
    cluster_change = normalized_change_count(clusters)

    return clamp01((signature_change + cluster_change) / 2.0)


def compute_drift_score(steps: list[dict]) -> float:
    deltas = [float(step.get("delta", 0.0)) for step in steps]

    if not deltas:
        return 0.0

    delta_range = max(deltas) - min(deltas)
    delta_mean = mean(deltas)

    return clamp01((delta_range + delta_mean) / 2.0)


def compute_boundary_proximity(steps: list[dict]) -> float:
    """
    Minimal v0 proxy.

    A trajectory is considered closer to a boundary when recent delta values
    approach high instability territory.
    """

    deltas = [float(step.get("delta", 0.0)) for step in steps]

    if not deltas:
        return 0.0

    recent = deltas[-2:] if len(deltas) >= 2 else deltas

    return clamp01(mean(recent))


def compute_collapse_similarity(steps: list[dict]) -> float:
    """
    Minimal v0 proxy.

    Collapse-like behavior is approximated by high delta, frequent structural
    changes, and explicit BROKEN-like markers if present.
    """

    if not steps:
        return 0.0

    transition_density = compute_transition_density(steps)
    max_delta = max(float(step.get("delta", 0.0)) for step in steps)

    broken_markers = {"BROKEN", "COLLAPSE", "NULL", "FAIL"}
    signatures = {str(step.get("signature", "")).upper() for step in steps}

    marker_signal = 1.0 if signatures.intersection(broken_markers) else 0.0

    return clamp01((0.40 * transition_density) + (0.40 * max_delta) + (0.20 * marker_signal))


def compute_irreversibility_signal(steps: list[dict]) -> float:
    iris = [float(step.get("iri", 0.0)) for step in steps]

    if not iris:
        return 0.0

    return clamp01(max(iris))


def compute_risk_score(signals: dict[str, float]) -> float:
    score = 0.0

    for key, weight in WEIGHTS.items():
        score += weight * signals[key]

    return clamp01(score)


def classify_regime(risk_score: float) -> str:
    if risk_score < THRESHOLDS["STABLE"]:
        return "STABLE"

    if risk_score < THRESHOLDS["DRIFT"]:
        return "DRIFT"

    if risk_score < THRESHOLDS["CRITICAL"]:
        return "CRITICAL"

    return "COLLAPSE"


def dominant_axis(signals: dict[str, float]) -> str:
    return max(signals.items(), key=lambda item: item[1])[0]


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


def analyze_trajectory(trajectory: dict) -> dict:
    steps = trajectory.get("steps", [])

    signals = {
        "transition_density": compute_transition_density(steps),
        "drift_score": compute_drift_score(steps),
        "boundary_proximity": compute_boundary_proximity(steps),
        "collapse_similarity": compute_collapse_similarity(steps),
        "irreversibility_signal": compute_irreversibility_signal(steps),
    }

    risk_score = compute_risk_score(signals)
    risk_regime = classify_regime(risk_score)

    return {
        "trajectory_id": trajectory.get("trajectory_id", "unknown"),
        "risk_regime": risk_regime,
        "risk_score": round(risk_score, 6),
        "gate_action": GATE_ACTIONS[risk_regime],
        "dominant_axis": dominant_axis(signals),
        "warning_flags": warning_flags(signals),
        "signals": {key: round(value, 6) for key, value in signals.items()},
        "weights": WEIGHTS,
        "thresholds": THRESHOLDS,
    }


def main() -> None:
    results = [analyze_trajectory(item) for item in SYNTHETIC_TRAJECTORIES]

    payload = {
        "experiment": "temporal_collapse_early_warning_level_3_v0",
        "status": "v0_minimal_reference",
        "boundary": "synthetic reference trajectories only",
        "claim": (
            "This script measures structural early-warning signals for "
            "temporal-collapse-like trajectories inside a bounded v0 setup."
        ),
        "results": results,
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 80)
    print("TEMPORAL COLLAPSE EARLY WARNING — LEVEL 3 v0")
    print("=" * 80)

    for result in results:
        print()
        print(f"trajectory_id: {result['trajectory_id']}")
        print(f"risk_regime:   {result['risk_regime']}")
        print(f"risk_score:    {result['risk_score']}")
        print(f"gate_action:   {result['gate_action']}")
        print(f"dominant_axis: {result['dominant_axis']}")
        print(f"warning_flags: {result['warning_flags']}")

    print()
    print("=" * 80)
    print(f"Wrote result file: {OUTPUT_PATH.relative_to(ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    main()

 