#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Perturbation Consistency v0

Purpose:
    Minimal controlled experiment testing whether increasing perturbation
    produces consistent structural degradation.

This experiment does NOT prove OMNIA correct.

It tests only whether a toy structural proxy responds coherently to a
controlled perturbation ladder.

Core boundary:
    measurement != inference != decision

Expected behavior:
    larger perturbation
    ->
    lower structural stability

PASS condition:
    omega_proxy decreases monotonically or near-monotonically as perturbation
    level increases.
"""

from __future__ import annotations

import json
import math
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


EXPERIMENT_NAME = "perturbation_consistency_v0"
DOMAIN = "controlled_perturbation_ladder"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "perturbation_consistency_v0.json"


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
    """
    Compute compressed_size / original_size.

    Lower values usually indicate more repeated/compressible structure.
    Higher values usually indicate weaker compressible structure.
    """
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
    Measure simple local transition regularity.

    If a sequence repeats a predictable motif, adjacent character transitions
    repeat often.

    This is a structural proxy only.
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

    This is NOT the full OMNIA engine.

    It is a toy proxy for perturbation consistency testing.
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
# Perturbation ladder
# ---------------------------------------------------------------------

def build_base_sequence() -> str:
    """
    Build a highly structured base sequence.
    """
    return "ABCD" * 64


def perturb_sequence(base: str, level: int) -> str:
    """
    Apply deterministic perturbations.

    level 0 -> no perturbation
    level 1 -> sparse local substitutions
    level 2 -> more substitutions
    level 3 -> substitutions + local reversals
    level 4 -> substitutions + reversals + noise blocks
    level 5 -> heavy deterministic disruption

    No randomness is used.
    """
    chars = list(base)
    length = len(chars)

    if level == 0:
        return base

    # deterministic replacement alphabet
    replacements = "XYZQ"

    if level >= 1:
        for i in range(0, length, 64):
            chars[i] = replacements[(i // 64) % len(replacements)]

    if level >= 2:
        for i in range(16, length, 48):
            chars[i] = replacements[(i // 48 + 1) % len(replacements)]

    if level >= 3:
        for start in range(32, length, 64):
            end = min(start + 8, length)
            chars[start:end] = reversed(chars[start:end])

    if level >= 4:
        noise = list("QZXV")
        for start in range(24, length, 40):
            for offset, value in enumerate(noise):
                idx = start + offset
                if idx < length:
                    chars[idx] = value

    if level >= 5:
        deterministic_noise = (
            "Q7mZp1LxR9vT2nK8sB5cH0uD4eW6yA3"
            "jF2pN9qR7xL1vC8mZ5tB0sK4hD6wY3"
        )
        repeated_noise = (deterministic_noise * ((length // len(deterministic_noise)) + 1))[:length]
        chars = list(repeated_noise)

    return "".join(chars)


def build_perturbation_ladder() -> List[Dict[str, Any]]:
    """
    Create controlled perturbation levels.
    """
    base = build_base_sequence()

    ladder = []
    for level in range(0, 6):
        text = perturb_sequence(base, level)
        ladder.append({
            "level": level,
            "label": f"perturbation_level_{level}",
            "text": text,
            "signature": structural_signature(text),
        })

    return ladder


# ---------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------

def check_monotonic_degradation(values: List[float]) -> Dict[str, Any]:
    """
    Check whether values decrease monotonically or near-monotonically.

    Strict monotonicity:
        v[i] >= v[i+1] for every adjacent pair

    Near monotonicity:
        allows one minor local violation with tolerance <= 0.02

    This is useful because compression proxies can produce tiny discrete artifacts.
    """
    violations = []

    for i in range(len(values) - 1):
        current_value = values[i]
        next_value = values[i + 1]

        if next_value > current_value:
            violations.append({
                "index": i,
                "current": current_value,
                "next": next_value,
                "increase": round(next_value - current_value, 12),
            })

    strict_monotonic = len(violations) == 0

    minor_violations = [
        item for item in violations
        if item["increase"] <= 0.02
    ]

    near_monotonic = (
        strict_monotonic
        or (
            len(violations) <= 1
            and len(minor_violations) == len(violations)
        )
    )

    return {
        "values": values,
        "strict_monotonic_decrease": strict_monotonic,
        "near_monotonic_decrease": near_monotonic,
        "violation_count": len(violations),
        "violations": violations,
    }


def compute_degradation(ladder: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute degradation from level 0 to final level.
    """
    values = [item["signature"]["omega_proxy"] for item in ladder]

    initial = values[0]
    final = values[-1]
    absolute_drop = initial - final

    relative_drop = absolute_drop / initial if initial != 0 else 0.0

    monotonicity = check_monotonic_degradation(values)

    return {
        "initial_omega_proxy": round(initial, 12),
        "final_omega_proxy": round(final, 12),
        "absolute_drop": round(absolute_drop, 12),
        "relative_drop": round(relative_drop, 12),
        "monotonicity": monotonicity,
    }


def build_result(ladder: List[Dict[str, Any]]) -> Dict[str, Any]:
    degradation = compute_degradation(ladder)

    pass_condition = (
        degradation["monotonicity"]["near_monotonic_decrease"] is True
        and degradation["absolute_drop"] > 0.25
    )

    status = "PASS" if pass_condition else "FAIL"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Minimal controlled experiment testing whether increasing "
            "perturbation produces consistent structural degradation."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "perturbation_ladder": [
            {
                "level": item["level"],
                "label": item["label"],
                "signature": item["signature"],
            }
            for item in ladder
        ],
        "degradation": degradation,
        "pass_condition": (
            "near_monotonic_decrease == true and absolute_drop > 0.25"
        ),
        "status": status,
        "interpretation": (
            "PASS means the toy structural proxy decreases consistently under "
            "the controlled perturbation ladder. It does not prove OMNIA correct "
            "and does not validate semantic truth."
            if status == "PASS"
            else
            "FAIL means the toy structural proxy did not degrade consistently "
            "under the controlled perturbation ladder."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy perturbation ladder.",
            "The omega_proxy is only a minimal structural proxy.",
            "No semantic correctness is evaluated.",
            "No randomness is used.",
            "No cross-domain generalization is claimed.",
            "No threshold robustness sweep is included yet.",
        ],
        "reproduction_command": "python examples/perturbation_consistency_v0.py",
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    ladder = build_perturbation_ladder()
    result = build_result(ladder)

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("OMNIA-VALIDATION — Perturbation Consistency v0")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Claim level: {result['claim_level']}")
    print()

    print("Perturbation ladder omega_proxy:")
    for item in result["perturbation_ladder"]:
        print(
            f"  level={item['level']} "
            f"omega_proxy={item['signature']['omega_proxy']} "
            f"entropy={item['signature']['entropy']} "
            f"compression_ratio={item['signature']['compression_ratio']}"
        )

    print()
    print("Degradation:")
    print(f"  initial omega_proxy: {result['degradation']['initial_omega_proxy']}")
    print(f"  final omega_proxy:   {result['degradation']['final_omega_proxy']}")
    print(f"  absolute drop:       {result['degradation']['absolute_drop']}")
    print(f"  relative drop:       {result['degradation']['relative_drop']}")

    print()
    print("Monotonicity:")
    mono = result["degradation"]["monotonicity"]
    print(f"  strict monotonic decrease: {mono['strict_monotonic_decrease']}")
    print(f"  near monotonic decrease:   {mono['near_monotonic_decrease']}")
    print(f"  violation count:           {mono['violation_count']}")

    if mono["violations"]:
        print("  violations:")
        for violation in mono["violations"]:
            print(f"    {violation}")

    print()
    print(f"Pass condition: {result['pass_condition']}")
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()

Output atteso:

Status: PASS
near monotonic decrease: True
absolute drop: > 0.25

Questo esperimento resta Level 1 — Toy Demonstration, ma introduce il primo asse dinamico:

perturbation level
->
structural degradation