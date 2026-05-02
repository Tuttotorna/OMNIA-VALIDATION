#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Cross-Domain Invariance v0.1

Purpose:
    Repeat the failed cross_domain_invariance_v0 experiment, but introduce
    a minimal canonical structural projection before distance measurement.

v0 result:
    FAIL / NEGATIVE_RESULT

Reason:
    Naive structural signatures were dominated by representation format.

v0.1 question:
    Can a minimal normalization layer make structural family identity more
    visible than representation style?

Core boundary:
    measurement != inference != decision

Core hypothesis:
    raw representation distance may fail,
    but normalized structural projection may recover partial invariance.

PASS condition:
    normalized_within_distance < normalized_cross_distance
    and normalized_margin > raw_margin
    and normalized_margin > 0.05
"""

from __future__ import annotations

import json
import math
import re
import zlib
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional


EXPERIMENT_NAME = "cross_domain_invariance_v0_1"
DOMAIN = "normalization_aware_cross_domain_structural_invariance"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "cross_domain_invariance_v0_1.json"


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


def unique_symbol_ratio(text: str) -> float:
    """
    Ratio of unique symbols to total symbols.

    Lower ratio usually indicates stronger repeated symbolic structure.
    """
    if not text:
        return 0.0

    return len(set(text)) / len(text)


def periodicity_score(text: str, max_period: int = 8) -> float:
    """
    Detect simple periodicity.

    Returns score in [0, 1].
    Higher score means stronger match to some small repeating period.
    """
    if len(text) < 2:
        return 0.0

    best = 0.0

    for period in range(1, min(max_period, len(text)) + 1):
        matches = 0
        comparisons = 0

        for i in range(period, len(text)):
            comparisons += 1
            if text[i] == text[i - period]:
                matches += 1

        if comparisons:
            best = max(best, matches / comparisons)

    return best


def transition_cardinality_score(text: str) -> float:
    """
    Measure whether transition vocabulary is small relative to sequence length.

    A perfectly cyclic sequence has few transition types repeated many times.
    """
    if len(text) < 2:
        return 0.0

    transitions = [text[i:i + 2] for i in range(len(text) - 1)]
    unique_transitions = len(set(transitions))

    score = 1.0 - (unique_transitions / max(len(transitions), 1))
    return max(0.0, min(1.0, score))


def structural_signature(text: str) -> Dict[str, float]:
    """
    Produce a deterministic structural signature.

    This is still a toy proxy.

    v0.1 adds symbolic-periodic features that are less dependent on surface
    token style once canonical projection has been applied.
    """
    entropy = shannon_entropy(text)
    ratio = compression_ratio(text)
    repetition = normalized_repetition_score(text, n=3)
    transition = transition_regular_score(text)
    unique_ratio = unique_symbol_ratio(text)
    periodicity = periodicity_score(text, max_period=8)
    transition_cardinality = transition_cardinality_score(text)

    compressibility = max(0.0, min(1.0, 1.0 - ratio))
    low_unique = max(0.0, min(1.0, 1.0 - unique_ratio))

    omega_proxy = max(
        0.0,
        min(
            1.0,
            (
                0.18 * compressibility
                + 0.18 * repetition
                + 0.18 * transition
                + 0.18 * low_unique
                + 0.19 * periodicity
                + 0.09 * transition_cardinality
            ),
        ),
    )

    return {
        "entropy": round(entropy, 12),
        "compression_ratio": round(ratio, 12),
        "repetition_score": round(repetition, 12),
        "transition_regular_score": round(transition, 12),
        "unique_symbol_ratio": round(unique_ratio, 12),
        "periodicity_score": round(periodicity, 12),
        "transition_cardinality_score": round(transition_cardinality, 12),
        "omega_proxy": round(omega_proxy, 12),
    }


# ---------------------------------------------------------------------
# Case construction
# ---------------------------------------------------------------------

def build_cases() -> List[Dict[str, Any]]:
    """
    Build representations of two structural families.

    Family A:
        two-state alternating pattern.

    Family B:
        four-state cyclic pattern.

    Representations differ by alphabet, separators, words, and JSON-like form.
    """
    return [
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
# Canonical structural projection
# ---------------------------------------------------------------------

def tokenize_representation(text: str) -> List[str]:
    """
    Extract structural tokens from mixed representations.

    This is a minimal hand-built normalization layer.

    It intentionally removes:
        - separators
        - punctuation
        - JSON formatting
        - lexical surface form

    It preserves:
        - repeated symbolic sequence order
        - distinct token identity
    """
    # JSON-like numeric payloads: {"x":0}, {"s":4}
    json_numbers = re.findall(r':\s*([A-Za-z0-9_]+)\s*}', text)
    if json_numbers:
        return json_numbers

    # Pipe-separated words.
    if "|" in text:
        return [token.strip() for token in text.split("|") if token.strip()]

    # Space-separated symbols / digits.
    if " " in text:
        return [token.strip() for token in text.split() if token.strip()]

    # Compact letters/digits.
    return list(text)


def canonical_project(text: str) -> str:
    """
    Convert any representation into a canonical structural sequence.

    Example:
        ABABAB       -> 010101
        1 0 1 0     -> 010101
        left|right  -> 010101
        {"x":0},{"x":1} -> 010101

    The projection maps first-seen token to 0, next unseen token to 1, etc.

    This removes lexical identity while preserving symbolic transition order.
    """
    tokens = tokenize_representation(text)

    mapping: Dict[str, str] = {}
    next_id = 0
    projected = []

    for token in tokens:
        if token not in mapping:
            mapping[token] = str(next_id)
            next_id += 1

        projected.append(mapping[token])

    # Use no separators to preserve compact structural sequence.
    return "".join(projected)


# ---------------------------------------------------------------------
# Distance geometry
# ---------------------------------------------------------------------

RAW_SIGNATURE_KEYS = [
    "entropy",
    "compression_ratio",
    "repetition_score",
    "transition_regular_score",
    "unique_symbol_ratio",
    "periodicity_score",
    "transition_cardinality_score",
    "omega_proxy",
]

NORMALIZED_SIGNATURE_KEYS = RAW_SIGNATURE_KEYS


def vectorize(signature: Dict[str, float], keys: List[str]) -> List[float]:
    return [signature[key] for key in keys]


def euclidean_distance(a: List[float], b: List[float]) -> float:
    total = 0.0
    for x, y in zip(a, b):
        total += (x - y) ** 2
    return math.sqrt(total)


def measure_cases(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    measured = []

    for case in cases:
        raw_text = case["text"]
        normalized_text = canonical_project(raw_text)

        raw_signature = structural_signature(raw_text)
        normalized_signature = structural_signature(normalized_text)

        measured.append({
            "case_id": case["case_id"],
            "family": case["family"],
            "representation": case["representation"],
            "raw_signature": raw_signature,
            "normalized_text": normalized_text,
            "normalized_signature": normalized_signature,
        })

    return measured


def compute_pairwise_distances(
    measured: List[Dict[str, Any]],
    signature_key: str,
    keys: List[str],
) -> List[Dict[str, Any]]:
    pairs = []

    for left, right in combinations(measured, 2):
        left_vec = vectorize(left[signature_key], keys)
        right_vec = vectorize(right[signature_key], keys)
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
    raw_pairs = compute_pairwise_distances(
        measured,
        signature_key="raw_signature",
        keys=RAW_SIGNATURE_KEYS,
    )
    normalized_pairs = compute_pairwise_distances(
        measured,
        signature_key="normalized_signature",
        keys=NORMALIZED_SIGNATURE_KEYS,
    )

    raw_analysis = analyze_distances(raw_pairs)
    normalized_analysis = analyze_distances(normalized_pairs)

    normalized_margin = normalized_analysis["separation_margin"]
    raw_margin = raw_analysis["separation_margin"]

    pass_condition = (
        normalized_analysis["within_lower_than_cross"] is True
        and normalized_margin > raw_margin
        and normalized_margin > 0.05
    )

    weak_condition = (
        normalized_analysis["within_lower_than_cross"] is True
        and normalized_margin > raw_margin
    )

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
            "Normalization-aware test of whether structural family identity "
            "becomes more visible after canonical projection."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "cases": measured,
        "raw_pairwise_distances": raw_pairs,
        "normalized_pairwise_distances": normalized_pairs,
        "raw_analysis": raw_analysis,
        "normalized_analysis": normalized_analysis,
        "pass_condition": (
            "normalized_within_lower_than_cross == true and "
            "normalized_margin > raw_margin and normalized_margin > 0.05"
        ),
        "status": status,
        "interpretation": (
            "PASS means canonical projection improved structural invariance "
            "enough that same-family representations were closer than cross-family "
            "representations with non-trivial margin."
            if status == "PASS"
            else
            "WEAK_PASS means canonical projection improved invariance but not "
            "strongly enough for the full threshold."
            if status == "WEAK_PASS"
            else
            "FAIL means canonical projection did not recover same-family closeness "
            "under this toy signature."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy normalization experiment.",
            "The canonical projection is hand-built.",
            "Only two structural families are tested.",
            "Only four representations per family are tested.",
            "No universal invariance claim is made.",
            "No semantic correctness is evaluated.",
            "No external reproduction is included yet.",
        ],
        "reproduction_command": "python examples/cross_domain_invariance_v0_1.py",
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
    print("OMNIA-VALIDATION — Cross-Domain Invariance v0.1")
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
            f"raw_omega={item['raw_signature']['omega_proxy']} "
            f"norm_omega={item['normalized_signature']['omega_proxy']}"
        )

    print()
    print("Raw distance analysis:")
    raw = result["raw_analysis"]
    print(
        "  mean within-structure distance: "
        f"{raw['mean_within_structure_distance']}"
    )
    print(
        "  mean cross-structure distance:  "
        f"{raw['mean_cross_structure_distance']}"
    )
    print(
        "  separation margin:              "
        f"{raw['separation_margin']}"
    )
    print(
        "  within lower than cross:        "
        f"{raw['within_lower_than_cross']}"
    )

    print()
    print("Normalized distance analysis:")
    norm = result["normalized_analysis"]
    print(
        "  mean within-structure distance: "
        f"{norm['mean_within_structure_distance']}"
    )
    print(
        "  mean cross-structure distance:  "
        f"{norm['mean_cross_structure_distance']}"
    )
    print(
        "  separation margin:              "
        f"{norm['separation_margin']}"
    )
    print(
        "  within lower than cross:        "
        f"{norm['within_lower_than_cross']}"
    )

    print()
    print("Improvement:")
    print(f"  raw margin:        {raw['separation_margin']}")
    print(f"  normalized margin: {norm['separation_margin']}")
    print(
        "  normalized > raw:  "
        f"{norm['separation_margin'] > raw['separation_margin']}"
    )

    print()
    print("Pass condition:")
    print(f"  {result['pass_condition']}")

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()