#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Cross-Domain Invariance v0

Purpose:
    Minimal controlled experiment testing whether the same structural pattern
    remains closer to itself across different representations than to a different
    structural pattern.

This experiment is a toy test of:

    structural invariance under transformation

It does NOT prove universal invariance.

It does NOT validate the full OMNIA engine.

Core boundary:
    measurement != inference != decision

Core question:
    Is within-structure distance lower than cross-structure distance?

Expected behavior:
    same structure / different representation
    ->
    smaller distance

    different structure
    ->
    larger distance

PASS condition:
    mean_within_structure_distance < mean_cross_structure_distance
"""

from __future__ import annotations

import json
import math
import zlib
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Tuple


EXPERIMENT_NAME = "cross_domain_invariance_v0"
DOMAIN = "cross_domain_structural_invariance"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "cross_domain_invariance_v0.json"


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


def normalized_repetition_score(text: str, n: int = 3) -> float:
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
    Measure local transition repetition.
    """
    if len(text) < 2:
        return 0.0

    transitions = [text[i:i + 2] for i in range(len(text) - 1)]
    counts = Counter(transitions)

    repeated = sum(count - 1 for count in counts.values() if count > 1)
    possible = max(len(transitions) - 1, 1)

    return repeated / possible


def token_length_regular_score(text: str) -> float:
    """
    Measure regularity of token lengths.

    This provides a representation-tolerant signal:
    many equivalent structural encodings preserve repeated length patterns.
    """
    tokens = [
        token.strip()
        for token in text.replace(",", " ").replace("|", " ").replace(";", " ").split()
        if token.strip()
    ]

    if len(tokens) < 2:
        return 0.0

    lengths = [len(token) for token in tokens]
    counts = Counter(lengths)

    repeated = sum(count - 1 for count in counts.values() if count > 1)
    possible = max(len(lengths) - 1, 1)

    return repeated / possible


def structural_signature(text: str) -> Dict[str, float]:
    """
    Produce a minimal deterministic structural signature.

    This is not the full OMNIA engine.

    It is a toy proxy for cross-representation invariance testing.
    """
    entropy = shannon_entropy(text)
    ratio = compression_ratio(text)
    repetition = normalized_repetition_score(text, n=3)
    transition = transition_regular_score(text)
    token_regular = token_length_regular_score(text)

    compressibility = max(0.0, min(1.0, 1.0 - ratio))

    omega_proxy = max(
        0.0,
        min(
            1.0,
            (
                0.25 * compressibility
                + 0.25 * repetition
                + 0.25 * transition
                + 0.25 * token_regular
            ),
        ),
    )

    return {
        "entropy": round(entropy, 12),
        "compression_ratio": round(ratio, 12),
        "repetition_score": round(repetition, 12),
        "transition_regular_score": round(transition, 12),
        "token_length_regular_score": round(token_regular, 12),
        "omega_proxy": round(omega_proxy, 12),
    }


# ---------------------------------------------------------------------
# Structural patterns and representations
# ---------------------------------------------------------------------

def build_cases() -> List[Dict[str, Any]]:
    """
    Build multiple representations of two structural families.

    Family A:
        ABAB alternating pattern.

    Family B:
        ABCD cyclic pattern.

    Representations differ by symbols, separators, tokenization, and encoding style.
    """
    return [
        # Family A — alternating binary structure
        {
            "case_id": "A_letters_compact",
            "family": "A_alternating",
            "representation": "letters_compact",
            "text": "AB" * 48,
        },
        {
            "case_id": "A_digits_spaced",
            "family": "A_alternating",
            "representation": "digits_spaced",
            "text": " ".join(["1", "0"] * 48),
        },
        {
            "case_id": "A_words_pipe",
            "family": "A_alternating",
            "representation": "words_pipe",
            "text": "|".join(["left", "right"] * 48),
        },
        {
            "case_id": "A_json_like",
            "family": "A_alternating",
            "representation": "json_like",
            "text": ",".join(['{"x":0}', '{"x":1}'] * 48),
        },

        # Family B — four-step cyclic structure
        {
            "case_id": "B_letters_compact",
            "family": "B_cyclic",
            "representation": "letters_compact",
            "text": "ABCD" * 24,
        },
        {
            "case_id": "B_digits_spaced",
            "family": "B_cyclic",
            "representation": "digits_spaced",
            "text": " ".join(["1", "2", "3", "4"] * 24),
        },
        {
            "case_id": "B_words_pipe",
            "family": "B_cyclic",
            "representation": "words_pipe",
            "text": "|".join(["north", "east", "south", "west"] * 24),
        },
        {
            "case_id": "B_json_like",
            "family": "B_cyclic",
            "representation": "json_like",
            "text": ",".join(['{"s":1}', '{"s":2}', '{"s":3}', '{"s":4}'] * 24),
        },
    ]


# ---------------------------------------------------------------------
# Distance geometry
# ---------------------------------------------------------------------

SIGNATURE_KEYS = [
    "entropy",
    "compression_ratio",
    "repetition_score",
    "transition_regular_score",
    "token_length_regular_score",
    "omega_proxy",
]


def vectorize(signature: Dict[str, float]) -> List[float]:
    return [signature[key] for key in SIGNATURE_KEYS]


def euclidean_distance(a: List[float], b: List[float]) -> float:
    total = 0.0
    for x, y in zip(a, b):
        total += (x - y) ** 2
    return math.sqrt(total)


def measure_cases(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    measured = []

    for case in cases:
        signature = structural_signature(case["text"])

        measured.append({
            "case_id": case["case_id"],
            "family": case["family"],
            "representation": case["representation"],
            "signature": signature,
        })

    return measured


def compute_pairwise_distances(measured: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pairs = []

    for left, right in combinations(measured, 2):
        left_vec = vectorize(left["signature"])
        right_vec = vectorize(right["signature"])
        distance = euclidean_distance(left_vec, right_vec)

        same_family = left["family"] == right["family"]

        pairs.append({
            "left": left["case_id"],
            "right": right["case_id"],
            "left_family": left["family"],
            "right_family": right["family"],
            "same_family": same_family,
            "distance": round(distance, 12),
        })

    return pairs


def mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def analyze_distances(pairs: List[Dict[str, Any]]) -> Dict[str, Any]:
    within = [
        pair["distance"]
        for pair in pairs
        if pair["same_family"] is True
    ]

    cross = [
        pair["distance"]
        for pair in pairs
        if pair["same_family"] is False
    ]

    within_mean = mean(within)
    cross_mean = mean(cross)

    margin = cross_mean - within_mean
    ratio = within_mean / cross_mean if cross_mean != 0 else None

    return {
        "within_structure_distances": within,
        "cross_structure_distances": cross,
        "mean_within_structure_distance": round(within_mean, 12),
        "mean_cross_structure_distance": round(cross_mean, 12),
        "separation_margin": round(margin, 12),
        "within_to_cross_ratio": round(ratio, 12) if ratio is not None else None,
        "within_lower_than_cross": within_mean < cross_mean,
    }


def build_result(measured: List[Dict[str, Any]]) -> Dict[str, Any]:
    pairs = compute_pairwise_distances(measured)
    analysis = analyze_distances(pairs)

    pass_condition = (
        analysis["within_lower_than_cross"] is True
        and analysis["separation_margin"] > 0.05
    )

    weak_condition = analysis["within_lower_than_cross"] is True

    if pass_condition:
        status = "PASS"
    elif weak_condition:
        status = "WEAK_PASS"
    else:
        status = "FAIL"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Minimal controlled experiment testing whether the same structural "
            "pattern remains closer to itself across different representations "
            "than to a different structural pattern."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "signature_keys": SIGNATURE_KEYS,
        "cases": measured,
        "pairwise_distances": pairs,
        "analysis": analysis,
        "pass_condition": (
            "mean_within_structure_distance < mean_cross_structure_distance "
            "and separation_margin > 0.05"
        ),
        "status": status,
        "interpretation": (
            "PASS means same-structure representations were closer on average "
            "than cross-structure representations with a non-trivial margin. "
            "This is a toy result and does not prove universal invariance."
            if status == "PASS"
            else
            "WEAK_PASS means same-structure representations were closer on "
            "average, but the margin was weak."
            if status == "WEAK_PASS"
            else
            "FAIL means the toy structural signature did not preserve family "
            "closeness across representations."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy cross-representation experiment.",
            "Only two structural families are tested.",
            "Only four representations per family are tested.",
            "The structural signature is intentionally minimal.",
            "No universal invariance claim is made.",
            "No semantic correctness is evaluated.",
            "No external reproduction is included yet.",
        ],
        "reproduction_command": "python examples/cross_domain_invariance_v0.py",
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    cases = build_cases()
    measured = measure_cases(cases)
    result = build_result(measured)

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("OMNIA-VALIDATION — Cross-Domain Invariance v0")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Claim level: {result['claim_level']}")
    print()

    print("Cases:")
    for item in result["cases"]:
        print(
            f"  {item['case_id']:22s} "
            f"family={item['family']:15s} "
            f"representation={item['representation']:15s} "
            f"omega_proxy={item['signature']['omega_proxy']}"
        )

    print()
    print("Distance analysis:")
    analysis = result["analysis"]
    print(
        "  mean within-structure distance: "
        f"{analysis['mean_within_structure_distance']}"
    )
    print(
        "  mean cross-structure distance:  "
        f"{analysis['mean_cross_structure_distance']}"
    )
    print(
        "  separation margin:              "
        f"{analysis['separation_margin']}"
    )
    print(
        "  within/cross ratio:             "
        f"{analysis['within_to_cross_ratio']}"
    )
    print(
        "  within lower than cross:        "
        f"{analysis['within_lower_than_cross']}"
    )

    print()
    print("Pass condition:")
    print(f"  {result['pass_condition']}")

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()