#!/usr/bin/env python3
"""
Temporal Collapse Trajectory-Native Validator — v2

This script moves Level 3 beyond snapshot-derived warning.

v0 tested synthetic reference trajectories.
v1 converted Level 2 result files into trajectory-like snapshots.
v2 constructs an ordered trajectory from Level 2 temporal-collapse stages
and evaluates risk across the chain as a trajectory.

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
OUTPUT_PATH = RESULTS_DIR / "temporal_collapse_trajectory_native_validator_v2.json"


ORDERED_LEVEL_2_STAGES = [
    {
        "stage_index": 1,
        "stage_name": "cluster_adjacency_graph",
        "source_file": "temporal_collapse_topology_cluster_adjacency_graph_v0.json",
    },
    {
        "stage_index": 2,
        "stage_name": "cluster_graph_centrality",
        "source_file": "temporal_collapse_topology_cluster_graph_centrality_v0.json",
    },
    {
        "stage_index": 3,
        "stage_name": "cluster_graph_control_plane",
        "source_file": "temporal_collapse_topology_cluster_graph_control_plane_v0.json",
    },
    {
        "stage_index": 4,
        "stage_name": "control_plane_robustness",
        "source_file": "temporal_collapse_topology_control_plane_robustness_v0.json",
    },
    {
        "stage_index": 5,
        "stage_name": "dependency_map",
        "source_file": "temporal_collapse_topology_dependency_map_v0.json",
    },
    {
        "stage_index": 6,
        "stage_name": "dependency_boundary",
        "source_file": "temporal_collapse_topology_dependency_boundary_v0.json",
    },
    {
        "stage_index": 7,
        "stage_name": "boundary_phase_diagram",
        "source_file": "temporal_collapse_topology_boundary_phase_diagram_v0.json",
    },
]


WEIGHTS = {
    "transition_density": 0.20,
    "drift_progression": 0.20,
    "boundary_proximity": 0.25,
    "collapse_similarity": 0.25,
    "irreversibility_proxy": 0.10,
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


def extract_stage_observation(stage: dict) -> dict:
    """
    Extracts a bounded structural observation from one ordered Level 2 stage.

    This is trajectory-native in the sense that each observation is inserted
    into a fixed ordered chain and then analyzed through transitions and
    progression across the chain.
    """

    path = RESULTS_DIR / stage["source_file"]
    payload = safe_load_json(path)

    if payload.get("missing"):
        return {
            "stage_index": stage["stage_index"],
            "stage_name": stage["stage_name"],
            "source_file": f"results/{stage['source_file']}",
            "source_status": "MISSING",
            "status_signature": "MISSING",
            "numeric_mean": 0.0,
            "numeric_range": 0.0,
            "check_ratio": 1.0,
            "fail_ratio": 0.0,
            "boundary_signal": 0.60,
            "collapse_signal": 0.30,
        }

    if payload.get("load_error"):
        return {
            "stage_index": stage["stage_index"],
            "stage_name": stage["stage_name"],
            "source_file": f"results/{stage['source_file']}",
            "source_status": "LOAD_ERROR",
            "status_signature": "LOAD_ERROR",
            "numeric_mean": 0.0,
            "numeric_range": 0.0,
            "check_ratio": 1.0,
            "fail_ratio": 0.0,
            "boundary_signal": 0.70,
            "collapse_signal": 0.40,
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

    if fail_ratio > 0:
        status_signature = "FAILURE_PRESSURE"
    elif check_ratio > 0:
        status_signature = "CHECK_PRESSURE"
    elif pass_count > 0:
        status_signature = "PASS_DOMINANT"
    else:
        status_signature = "UNMARKED"

    boundary_signal = clamp01(
        (0.70 * check_ratio)
        + (0.90 * fail_ratio)
        + (0.30 * numeric_range)
    )

    collapse_signal = clamp01(
        (0.80 * fail_ratio)
        + (0.30 * check_ratio)
    )

    return {
        "stage_index": stage["stage_index"],
        "stage_name": stage["stage_name"],
        "source_file": f"results/{stage['source_file']}",
        "source_status": "LOADED",
        "status_signature": status_signature,
        "numeric_mean": round(numeric_mean, 6),
        "numeric_range": round(numeric_range, 6),
        "check_ratio": round(check_ratio, 6),
        "fail_ratio": round(fail_ratio, 6),
        "boundary_signal": round(boundary_signal, 6),
        "collapse_signal": round(collapse_signal, 6),
    }


def normalized_change_count(values: list[str]) -> float:
    if len(values) < 2:
        return 0.0

    changes = 0

    for previous, current in zip(values, values[1:]):
        if previous != current:
            changes += 1

    return changes / (len(values) - 1)


def compute_transition_density(observations: list[dict]) -> float:
    """
    Measures how often stage signatures change across the ordered chain.
    """

    signatures = [
        str(item["status_signature"])
        for item in observations
    ]

    return clamp01(normalized_change_count(signatures))


def compute_drift_progression(observations: list[dict]) -> float:
    """
    Measures numeric movement across the ordered chain.

    Uses both mean-level movement and range-level movement.
    """

    if len(observations) < 2:
        return 0.0

    numeric_means = [
        float(item["numeric_mean"])
        for item in observations
    ]

    numeric_ranges = [
        float(item["numeric_range"])
        for item in observations
    ]

    mean_step_changes = [
        abs(current - previous)
        for previous, current in zip(numeric_means, numeric_means[1:])
    ]

    range_step_changes = [
        abs(current - previous)
        for previous, current in zip(numeric_ranges, numeric_ranges[1:])
    ]

    mean_change = mean(mean_step_changes) if mean_step_changes else 0.0
    range_change = mean(range_step_changes) if range_step_changes else 0.0

    final_pressure = (
        numeric_means[-1]
        + numeric_ranges[-1]
    ) / 2.0

    return clamp01(
        (0.40 * mean_change)
        + (0.40 * range_change)
        + (0.20 * final_pressure)
    )


def compute_boundary_proximity(observations: list[dict]) -> float:
    """
    Measures maximum and late-stage boundary pressure.
    """

    if not observations:
        return 0.0

    boundary_values = [
        float(item["boundary_signal"])
        for item in observations
    ]

    max_boundary = max(boundary_values)

    late_values = boundary_values[-2:] if len(boundary_values) >= 2 else boundary_values
    late_boundary = mean(late_values)

    return clamp01(
        (0.60 * max_boundary)
        + (0.40 * late_boundary)
    )


def compute_collapse_similarity(observations: list[dict]) -> float:
    """
    Measures whether the ordered chain resembles collapse-like pressure.

    In v2, this is conservative:
    - actual fail/collapse markers dominate
    - repeated CHECK pressure adds weaker collapse pressure
    - strong boundary signal contributes only partially
    """

    if not observations:
        return 0.0

    fail_values = [
        float(item["fail_ratio"])
        for item in observations
    ]

    check_values = [
        float(item["check_ratio"])
        for item in observations
    ]

    boundary_values = [
        float(item["boundary_signal"])
        for item in observations
    ]

    max_fail = max(fail_values)
    mean_check = mean(check_values)
    max_boundary = max(boundary_values)

    return clamp01(
        (0.55 * max_fail)
        + (0.25 * mean_check)
        + (0.20 * max_boundary)
    )


def compute_irreversibility_proxy(observations: list[dict]) -> float:
    """
    Minimal trajectory-native irreversibility proxy.

    A chain receives irreversibility pressure when late-stage boundary pressure
    remains high after earlier drift/check pressure has appeared.
    """

    if len(observations) < 2:
        return 0.0

    boundary_values = [
        float(item["boundary_signal"])
        for item in observations
    ]

    check_values = [
        float(item["check_ratio"])
        for item in observations
    ]

    late_boundary = mean(boundary_values[-2:])
    earlier_check = mean(check_values[:-2]) if len(check_values) > 2 else mean(check_values)

    return clamp01(
        (0.70 * late_boundary)
        + (0.30 * earlier_check)
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

    if signals["irreversibility_proxy"] >= 0.50:
        flags.append("irreversibility_proxy")

    return flags


def build_ordered_trajectory() -> list[dict]:
    return [
        extract_stage_observation(stage)
        for stage in ORDERED_LEVEL_2_STAGES
    ]


def analyze_trajectory(observations: list[dict]) -> dict:
    signals = {
        "transition_density": compute_transition_density(observations),
        "drift_progression": compute_drift_progression(observations),
        "boundary_proximity": compute_boundary_proximity(observations),
        "collapse_similarity": compute_collapse_similarity(observations),
        "irreversibility_proxy": compute_irreversibility_proxy(observations),
    }

    risk_score = compute_risk_score(signals)
    risk_regime = classify_regime(risk_score)

    return {
        "risk_regime": risk_regime,
        "risk_score": round(risk_score, 6),
        "gate_action": gate_action_for_regime(risk_regime),
        "dominant_axis": dominant_axis(signals),
        "warning_flags": warning_flags(signals),
        "signals": {
            key: round(value, 6)
            for key, value in signals.items()
        },
    }


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    observations = build_ordered_trajectory()
    trajectory_result = analyze_trajectory(observations)

    payload = {
        "experiment": "temporal_collapse_trajectory_native_validator_v2",
        "status": "v2_trajectory_native",
        "boundary": "ordered Level 2 temporal-collapse stage chain",
        "claim": (
            "This script evaluates Level 3 warning risk across an ordered "
            "temporal-collapse stage trajectory instead of independent snapshots."
        ),
        "ordered_stage_count": len(observations),
        "weights": WEIGHTS,
        "thresholds": THRESHOLDS,
        "trajectory_result": trajectory_result,
        "ordered_observations": observations,
    }

    OUTPUT_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    print("=" * 100)
    print("TEMPORAL COLLAPSE TRAJECTORY-NATIVE VALIDATOR — v2")
    print("=" * 100)

    print()
    print("ORDERED OBSERVATIONS")
    print("=" * 100)

    for item in observations:
        print()
        print(f"stage_index:      {item['stage_index']}")
        print(f"stage_name:       {item['stage_name']}")
        print(f"source_file:      {item['source_file']}")
        print(f"source_status:    {item['source_status']}")
        print(f"status_signature: {item['status_signature']}")
        print(f"numeric_mean:     {item['numeric_mean']}")
        print(f"numeric_range:    {item['numeric_range']}")
        print(f"check_ratio:      {item['check_ratio']}")
        print(f"fail_ratio:       {item['fail_ratio']}")
        print(f"boundary_signal:  {item['boundary_signal']}")
        print(f"collapse_signal:  {item['collapse_signal']}")

    print()
    print("=" * 100)
    print("TRAJECTORY RESULT")
    print("=" * 100)
    print(json.dumps(trajectory_result, indent=2))

    print()
    print("=" * 100)
    print(f"Wrote result file: {OUTPUT_PATH.relative_to(ROOT)}")
    print("=" * 100)


if __name__ == "__main__":
    main()