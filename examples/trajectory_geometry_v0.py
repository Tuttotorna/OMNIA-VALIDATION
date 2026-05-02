#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Trajectory Geometry v0

Purpose:
    Minimal controlled experiment for measuring structural evolution across
    perturbation space.

This experiment moves from static scoring to trajectory behavior.

It does NOT prove OMNIA correct.

It tests whether a deterministic perturbation trajectory produces measurable
trajectory features such as:

    - degradation slope
    - collapse point
    - stability plateau
    - curvature / acceleration
    - final residual structure

Core boundary:
    measurement != inference != decision

Expected behavior:
    As perturbation level increases, structural coherence should decrease.
    The trajectory should expose more information than a single final score.

PASS condition:
    - trajectory is reproducible
    - omega_proxy decreases near-monotonically
    - at least one trajectory feature is detected
"""

from __future__ import annotations

import json
import math
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


EXPERIMENT_NAME = "trajectory_geometry_v0"
DOMAIN = "structural_trajectory_geometry"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "trajectory_geometry_v0.json"


# ---------------------------------------------------------------------
# Minimal deterministic structural metrics
# ---------------------------------------------------------------------

def shannon_entropy(text: str) -> float:
    """Compute character-level Shannon entropy."""
    if not text:
        return 0.0

    counts = Counter(text)
    total = len(text)

    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy


def compression_ratio(text: str) -> float:
    """Compute compressed_size / original_size."""
    if not text:
        return 0.0

    raw = text.encode("utf-8")
    compressed = zlib.compress(raw, level=9)

    return len(compressed) / len(raw)


def normalized_repetition_score(text: str, n: int = 4) -> float:
    """
    Measure repeated n-gram structure.

    0 -> no repeated n-gram excess
    1 -> strong repeated structure
    """
    if len(text) < n:
        return 0.0

    grams = [text[i:i + n] for i in range(len(text) - n + 1)]
    counts = Counter(grams)

    repeated = sum(count - 1 for count in counts.values() if count > 1)
    possible = max(len(grams) - 1, 1)

    return repeated / possible


def transition_regular_score(text: str) -> float:
    """
    Measure local transition regularity.

    Predictable repeated motifs create repeated adjacent transitions.
    """
    if len(text) < 2:
        return 0.0

    transitions = [text[i:i + 2] for i in range(len(text) - 1)]
    counts = Counter(transitions)

    repeated = sum(count - 1 for count in counts.values() if count > 1)
    possible = max(len(transitions) - 1, 1)

    return repeated / possible


def structural_signature(text: str) -> Dict[str, float]:
    """
    Produce a minimal deterministic structural signature.

    This is not the full OMNIA engine.

    It is a toy proxy for trajectory geometry testing.
    """
    entropy = shannon_entropy(text)
    ratio = compression_ratio(text)
    repetition = normalized_repetition_score(text, n=4)
    transition = transition_regular_score(text)

    compressibility = max(0.0, min(1.0, 1.0 - ratio))

    omega_proxy = max(
        0.0,
        min(
            1.0,
            (
                0.35 * compressibility
                + 0.35 * repetition
                + 0.30 * transition
            ),
        ),
    )

    return {
        "entropy": round(entropy, 12),
        "compression_ratio": round(ratio, 12),
        "repetition_score": round(repetition, 12),
        "transition_regular_score": round(transition, 12),
        "omega_proxy": round(omega_proxy, 12),
    }


# ---------------------------------------------------------------------
# Perturbation trajectory
# ---------------------------------------------------------------------

def build_base_sequence() -> str:
    """
    Build a highly structured base sequence.
    """
    return "ABCD" * 96


def deterministic_noise(length: int) -> str:
    """
    Build deterministic pseudo-noise without randomness.
    """
    seed = (
        "Q7mZp1LxR9vT2nK8sB5cH0uD4eW6yA3"
        "jF2pN9qR7xL1vC8mZ5tB0sK4hD6wY3"
        "Z8aQ1rT6uP3vM9xL2nC7bH5dK0sW4"
    )
    return (seed * ((length // len(seed)) + 1))[:length]


def perturb_sequence(base: str, level: int, max_level: int) -> str:
    """
    Deterministically perturb a structured sequence.

    The perturbation grows with level.

    No randomness is used.

    Higher levels replace progressively larger windows with deterministic noise,
    plus local reversals and substitution patterns.
    """
    if level <= 0:
        return base

    chars = list(base)
    length = len(chars)
    noise = deterministic_noise(length)

    fraction = level / max_level
    replacement_span = int(length * fraction * 0.65)

    # Replace deterministic positions with noise.
    # Use stride changes to avoid purely contiguous damage.
    stride = max(2, int(18 - 14 * fraction))

    replaced = 0
    for i in range(0, length, stride):
        if replaced >= replacement_span:
            break
        chars[i] = noise[i]
        replaced += 1

    # Add local block replacements for higher levels.
    if level >= max_level * 0.35:
        block_size = max(4, int(4 + 12 * fraction))
        block_gap = max(16, int(64 - 40 * fraction))

        for start in range(block_gap // 2, length, block_gap):
            end = min(start + block_size, length)
            for idx in range(start, end):
                chars[idx] = noise[idx]

    # Add local reversals for middle/high levels.
    if level >= max_level * 0.50:
        rev_size = max(4, int(6 + 14 * fraction))
        rev_gap = max(20, int(72 - 36 * fraction))

        for start in range(rev_gap, length, rev_gap):
            end = min(start + rev_size, length)
            chars[start:end] = reversed(chars[start:end])

    # Heavy collapse regime near the end.
    if level >= max_level * 0.80:
        collapse_fraction = (level - max_level * 0.80) / (max_level * 0.20)
        collapse_span = int(length * collapse_fraction * 0.60)

        for idx in range(collapse_span):
            chars[idx] = noise[idx]

    return "".join(chars)


def build_trajectory(max_level: int = 20) -> List[Dict[str, Any]]:
    """
    Build structural measurements across perturbation levels.
    """
    base = build_base_sequence()

    trajectory = []
    for level in range(max_level + 1):
        text = perturb_sequence(base, level, max_level)
        signature = structural_signature(text)

        trajectory.append({
            "level": level,
            "perturbation_fraction": round(level / max_level, 6),
            "signature": signature,
        })

    return trajectory


# ---------------------------------------------------------------------
# Trajectory analysis
# ---------------------------------------------------------------------

def omega_values(trajectory: List[Dict[str, Any]]) -> List[float]:
    return [item["signature"]["omega_proxy"] for item in trajectory]


def first_differences(values: List[float]) -> List[float]:
    return [
        round(values[i + 1] - values[i], 12)
        for i in range(len(values) - 1)
    ]


def second_differences(values: List[float]) -> List[float]:
    first = first_differences(values)
    return [
        round(first[i + 1] - first[i], 12)
        for i in range(len(first) - 1)
    ]


def check_near_monotonic(values: List[float], tolerance: float = 0.025) -> Dict[str, Any]:
    """
    Check near-monotonic decrease.

    Allows small local increases caused by discrete compression artifacts.
    """
    violations = []

    for i in range(len(values) - 1):
        current_value = values[i]
        next_value = values[i + 1]

        if next_value > current_value + tolerance:
            violations.append({
                "index": i,
                "current": current_value,
                "next": next_value,
                "increase": round(next_value - current_value, 12),
            })

    return {
        "near_monotonic_decrease": len(violations) == 0,
        "tolerance": tolerance,
        "violation_count": len(violations),
        "violations": violations,
    }


def detect_collapse_point(
    values: List[float],
    drop_threshold: float = 0.10,
) -> Optional[Dict[str, Any]]:
    """
    Detect the first large local drop.

    Collapse point is defined as the first adjacent drop >= drop_threshold.
    """
    for i in range(len(values) - 1):
        drop = values[i] - values[i + 1]

        if drop >= drop_threshold:
            return {
                "from_level": i,
                "to_level": i + 1,
                "drop": round(drop, 12),
                "threshold": drop_threshold,
            }

    return None


def detect_plateaus(
    values: List[float],
    slope_tolerance: float = 0.01,
    min_length: int = 3,
) -> List[Dict[str, Any]]:
    """
    Detect approximate stability plateaus.

    A plateau is a run of at least min_length adjacent points where local changes
    are small.
    """
    plateaus = []
    start = None

    diffs = first_differences(values)

    for i, diff in enumerate(diffs):
        if abs(diff) <= slope_tolerance:
            if start is None:
                start = i
        else:
            if start is not None:
                end = i
                point_count = end - start + 1
                if point_count >= min_length:
                    plateaus.append({
                        "from_level": start,
                        "to_level": end,
                        "point_count": point_count,
                    })
                start = None

    if start is not None:
        end = len(values) - 1
        point_count = end - start + 1
        if point_count >= min_length:
            plateaus.append({
                "from_level": start,
                "to_level": end,
                "point_count": point_count,
            })

    return plateaus


def detect_curvature(second: List[float]) -> Dict[str, Any]:
    """
    Summarize second-difference behavior.

    Negative/positive second differences indicate trajectory acceleration changes.
    """
    if not second:
        return {
            "max_positive_curvature": 0.0,
            "max_negative_curvature": 0.0,
            "curvature_events": [],
        }

    max_positive = max(second)
    max_negative = min(second)

    events = []
    for index, value in enumerate(second):
        if abs(value) >= 0.04:
            events.append({
                "index": index,
                "value": value,
            })

    return {
        "max_positive_curvature": round(max_positive, 12),
        "max_negative_curvature": round(max_negative, 12),
        "curvature_event_count": len(events),
        "curvature_events": events,
    }


def analyze_trajectory(trajectory: List[Dict[str, Any]]) -> Dict[str, Any]:
    values = omega_values(trajectory)
    first = first_differences(values)
    second = second_differences(values)

    initial = values[0]
    final = values[-1]
    absolute_drop = initial - final
    relative_drop = absolute_drop / initial if initial else 0.0

    monotonicity = check_near_monotonic(values)
    collapse_point = detect_collapse_point(values)
    plateaus = detect_plateaus(values)
    curvature = detect_curvature(second)

    detected_features = []

    if monotonicity["near_monotonic_decrease"]:
        detected_features.append("near_monotonic_decrease")

    if collapse_point is not None:
        detected_features.append("collapse_point")

    if plateaus:
        detected_features.append("stability_plateau")

    if curvature["curvature_event_count"] > 0:
        detected_features.append("curvature_events")

    if absolute_drop > 0.25:
        detected_features.append("substantial_degradation")

    return {
        "omega_values": values,
        "first_differences": first,
        "second_differences": second,
        "initial_omega_proxy": round(initial, 12),
        "final_omega_proxy": round(final, 12),
        "absolute_drop": round(absolute_drop, 12),
        "relative_drop": round(relative_drop, 12),
        "monotonicity": monotonicity,
        "collapse_point": collapse_point,
        "plateaus": plateaus,
        "curvature": curvature,
        "detected_features": detected_features,
        "detected_feature_count": len(detected_features),
    }


def build_result(trajectory: List[Dict[str, Any]]) -> Dict[str, Any]:
    analysis = analyze_trajectory(trajectory)

    pass_condition = (
        analysis["monotonicity"]["near_monotonic_decrease"] is True
        and analysis["detected_feature_count"] >= 1
        and analysis["absolute_drop"] > 0.20
    )

    status = "PASS" if pass_condition else "WEAK_PASS"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Minimal controlled experiment for measuring structural evolution "
            "across perturbation space."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "trajectory": trajectory,
        "analysis": analysis,
        "pass_condition": (
            "near_monotonic_decrease == true and "
            "detected_feature_count >= 1 and absolute_drop > 0.20"
        ),
        "status": status,
        "interpretation": (
            "PASS means the toy trajectory shows reproducible structural "
            "evolution with detectable trajectory features. It does not prove "
            "OMNIA correct and does not validate semantic truth."
            if status == "PASS"
            else
            "WEAK_PASS means some trajectory behavior was detected, but the "
            "full pass condition was not strongly satisfied."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy trajectory experiment.",
            "The omega_proxy is only a minimal structural proxy.",
            "No semantic correctness is evaluated.",
            "No randomness is used.",
            "No cross-domain generalization is claimed.",
            "No external reproduction is included yet.",
        ],
        "reproduction_command": "python examples/trajectory_geometry_v0.py",
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    trajectory = build_trajectory(max_level=20)
    result = build_result(trajectory)

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("OMNIA-VALIDATION — Trajectory Geometry v0")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Claim level: {result['claim_level']}")
    print()

    print("Trajectory omega_proxy:")
    for item in result["trajectory"]:
        level = item["level"]
        fraction = item["perturbation_fraction"]
        omega = item["signature"]["omega_proxy"]
        entropy = item["signature"]["entropy"]
        ratio = item["signature"]["compression_ratio"]

        print(
            f"  level={level:02d} "
            f"fraction={fraction:.3f} "
            f"omega_proxy={omega} "
            f"entropy={entropy} "
            f"compression_ratio={ratio}"
        )

    print()
    print("Trajectory analysis:")
    analysis = result["analysis"]
    print(f"  initial omega_proxy:     {analysis['initial_omega_proxy']}")
    print(f"  final omega_proxy:       {analysis['final_omega_proxy']}")
    print(f"  absolute drop:           {analysis['absolute_drop']}")
    print(f"  relative drop:           {analysis['relative_drop']}")
    print(f"  near monotonic decrease: {analysis['monotonicity']['near_monotonic_decrease']}")
    print(f"  violation count:         {analysis['monotonicity']['violation_count']}")

    print()
    print("Detected features:")
    if analysis["detected_features"]:
        for feature in analysis["detected_features"]:
            print(f"  - {feature}")
    else:
        print("  (none)")

    print()
    print("Collapse point:")
    if analysis["collapse_point"] is None:
        print("  none detected")
    else:
        print(f"  {analysis['collapse_point']}")

    print()
    print("Plateaus:")
    if analysis["plateaus"]:
        for plateau in analysis["plateaus"]:
            print(f"  {plateau}")
    else:
        print("  none detected")

    print()
    print("Curvature:")
    print(
        f"  events: {analysis['curvature']['curvature_event_count']} "
        f"max_positive={analysis['curvature']['max_positive_curvature']} "
        f"max_negative={analysis['curvature']['max_negative_curvature']}"
    )

    print()
    print(f"Pass condition: {result['pass_condition']}")
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()