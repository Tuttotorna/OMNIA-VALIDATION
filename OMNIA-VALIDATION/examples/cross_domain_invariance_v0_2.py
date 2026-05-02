#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Cross-Domain Invariance v0.2

Purpose:
    Test whether normalization-aware structural invariance survives imperfect
    representation.

v0 result:
    FAIL / NEGATIVE_RESULT
    Raw signatures were dominated by representation format.

v0.1 result:
    PASS
    Clean canonical projection recovered perfect same-family separation.

v0.2 question:
    Does normalization still recover structure when representations are noisy,
    partially corrupted, or imperfectly projected?

Core boundary:
    measurement != inference != decision

Core hypothesis:
    Normalization should not require perfect inputs.
    If structural invariance is meaningful, partial degradation should produce
    graceful degradation rather than total collapse.

PASS condition:
    normalized_within_distance < normalized_cross_distance
    and normalized_margin > raw_margin
    and normalized_margin > 0.05
    and noise_gradient_detected == true
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
from typing import Any, Dict, List


EXPERIMENT_NAME = "cross_domain_invariance_v0_2"
DOMAIN = "noisy_normalization_aware_cross_domain_structural_invariance"
VERSION = "0.2.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "cross_domain_invariance_v0_2.json"


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
    """Measure repeated n-gram structure."""
    if len(text) < n:
        return 0.0

    grams = [text[i:i + n] for i in range(len(text) - n + 1)]
    counts = Counter(grams)

    repeated = sum(count - 1 for count in counts.values() if count > 1)
    possible = max(len(grams) - 1, 1)

    return repeated / possible


def transition_regular_score(text: str) -> float:
    """Measure repeated adjacent transitions."""
    if len(text) < 2:
        return 0.0

    transitions = [text[i:i + 2] for i in range(len(text) - 1)]
    counts = Counter(transitions)

    repeated = sum(count - 1 for count in counts.values() if count > 1)
    possible = max(len(transitions) - 1, 1)

    return repeated / possible


def unique_symbol_ratio(text: str) -> float:
    """Ratio of unique symbols to total symbols."""
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
    """
    if len(text) < 2:
        return 0.0

    transitions = [text[i:i + 2] for i in range(len(text) - 1)]
    unique_transitions = len(set(transitions))

    score = 1.0 - (unique_transitions / max(len(transitions), 1))
    return max(0.0, min(1.0, score))


def structural_signature(text: str) -> Dict[str, float]:
    """
    Produce a deterministic toy structural signature.

    This is not the full OMNIA engine.
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

def inject_deterministic_noise(tokens: List[str], noise_level: int) -> List[str]:
    """
    Add deterministic corruption to a token sequence.

    noise_level:
        0 -> clean
        1 -> sparse unknown tokens
        2 -> unknown tokens + local swaps
        3 -> unknown tokens + swaps + deletions
        4 -> stronger corruption

    No randomness is used.
    """
    if noise_level <= 0:
        return list(tokens)

    corrupted = list(tokens)

    unknown_cycle = ["UNK_A", "UNK_B", "UNK_C", "UNK_D"]

    if noise_level >= 1:
        for idx in range(11, len(corrupted), 37):
            corrupted[idx] = unknown_cycle[(idx // 37) % len(unknown_cycle)]

    if noise_level >= 2:
        for idx in range(7, len(corrupted) - 1, 29):
            corrupted[idx], corrupted[idx + 1] = corrupted[idx + 1], corrupted[idx]

    if noise_level >= 3:
        remove = set(range(13, len(corrupted), 31))
        corrupted = [
            token
            for idx, token in enumerate(corrupted)
            if idx not in remove
        ]

    if noise_level >= 4:
        for idx in range(5, len(corrupted), 17):
            corrupted[idx] = unknown_cycle[(idx // 17 + 1) % len(unknown_cycle)]

    return corrupted


def encode_tokens(tokens: List[str], representation: str) -> str:
    """
    Encode canonical tokens into different surface representations.
    """
    if representation == "letters_compact":
        mapping = {
            "0": "A",
            "1": "B",
            "2": "C",
            "3": "D",
            "UNK_A": "X",
            "UNK_B": "Y",
            "UNK_C": "Z",
            "UNK_D": "W",
        }
        return "".join(mapping.get(token, "?") for token in tokens)

    if representation == "digits_spaced":
        mapping = {
            "0": "1",
            "1": "0",
            "2": "2",
            "3": "3",
            "UNK_A": "9",
            "UNK_B": "8",
            "UNK_C": "7",
            "UNK_D": "6",
        }
        return " ".join(mapping.get(token, "NA") for token in tokens)

    if representation == "words_pipe":
        mapping = {
            "0": "left",
            "1": "right",
            "2": "up",
            "3": "down",
            "UNK_A": "noise_alpha",
            "UNK_B": "noise_beta",
            "UNK_C": "noise_gamma",
            "UNK_D": "noise_delta",
        }
        return "|".join(mapping.get(token, "unknown") for token in tokens)

    if representation == "json_like":
        mapping = {
            "0": '{"v":0}',
            "1": '{"v":1}',
            "2": '{"v":2}',
            "3": '{"v":3}',
            "UNK_A": '{"v":"noise_a"}',
            "UNK_B": '{"v":"noise_b"}',
            "UNK_C": '{"v":"noise_c"}',
            "UNK_D": '{"v":"noise_d"}',
        }
        return ",".join(mapping.get(token, '{"v":"unknown"}') for token in tokens)

    raise ValueError(f"Unknown representation: {representation}")


def build_family_tokens(family: str, repeats: int = 48) -> List[str]:
    """
    Build canonical structural token sequences.

    A_alternating:
        010101...

    B_cyclic:
        01230123...
    """
    if family == "A_alternating":
        return ["0", "1"] * repeats

    if family == "B_cyclic":
        return ["0", "1", "2", "3"] * (repeats // 2)

    raise ValueError(f"Unknown family: {family}")


def build_cases() -> List[Dict[str, Any]]:
    """
    Build noisy cross-representation cases.

    Each family appears in four representations.
    Each representation receives a deterministic corruption level.

    This prevents v0.1 from being perfectly clean.
    """
    representations = [
        ("letters_compact", 0),
        ("digits_spaced", 1),
        ("words_pipe", 2),
        ("json_like", 3),
    ]

    cases = []

    for family in ["A_alternating", "B_cyclic"]:
        base_tokens = build_family_tokens(family)

        for representation, noise_level in representations:
            noisy_tokens = inject_deterministic_noise(base_tokens, noise_level)
            text = encode_tokens(noisy_tokens, representation)

            short_family = "A" if family == "A_alternating" else "B"

            cases.append({
                "case_id": f"{short_family}_{representation}_noise_{noise_level}",
                "family": family,
                "representation": representation,
                "noise_level": noise_level,
                "canonical_tokens": noisy_tokens,
                "text": text,
            })

    return cases


# ---------------------------------------------------------------------
# Canonical structural projection
# ---------------------------------------------------------------------

def tokenize_representation(text: str) -> List[str]:
    """
    Extract structural tokens from mixed representations.

    This is a minimal hand-built normalization layer.
    """
    json_values = re.findall(r'"v"\s*:\s*"?([A-Za-z0-9_]+)"?\s*}', text)
    if json_values:
        return json_values

    if "|" in text:
        return [token.strip() for token in text.split("|") if token.strip()]

    if " " in text:
        return [token.strip() for token in text.split() if token.strip()]

    return list(text)


def canonical_project(text: str) -> str:
    """
    Convert representation into canonical first-seen symbolic sequence.

    This removes lexical identity while preserving symbolic order.

    Because noisy tokens are real tokens, they remain as additional symbols.
    Therefore normalization is not perfect under corruption.
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

    return "".join(projected)


# ---------------------------------------------------------------------
# Distance geometry
# ---------------------------------------------------------------------

SIGNATURE_KEYS = [
    "entropy",
    "compression_ratio",
    "repetition_score",
    "transition_regular_score",
    "unique_symbol_ratio",
    "periodicity_score",
    "transition_cardinality_score",
    "omega_proxy",
]


def vectorize(signature: Dict[str, float]) -> List[float]:
    return [signature[key] for key in SIGNATURE_KEYS]


def euclidean_distance(a: List[float], b: List[float]) -> float:
    total = 0.0
    for x, y in zip(a, b):
        total += (x - y) ** 2
    return math.sqrt(total)


def normalized_edit_distance(a: str, b: str) -> float:
    """
    Compute deterministic normalized Levenshtein distance.

    Used for direct projected-sequence comparison.
    """
    if a == b:
        return 0.0

    if not a:
        return 1.0 if b else 0.0

    if not b:
        return 1.0

    previous = list(range(len(b) + 1))

    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            substitute_cost = previous[j - 1] + (0 if ca == cb else 1)
            current.append(min(insert_cost, delete_cost, substitute_cost))
        previous = current

    distance = previous[-1]
    return distance / max(len(a), len(b))


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
            "noise_level": case["noise_level"],
            "raw_signature": raw_signature,
            "normalized_text": normalized_text,
            "normalized_signature": normalized_signature,
        })

    return measured


def compute_pairwise_distances(
    measured: List[Dict[str, Any]],
    signature_key: str,
) -> List[Dict[str, Any]]:
    pairs = []

    for left, right in combinations(measured, 2):
        left_vec = vectorize(left[signature_key])
        right_vec = vectorize(right[signature_key])
        signature_distance = euclidean_distance(left_vec, right_vec)

        projected_distance = normalized_edit_distance(
            left["normalized_text"],
            right["normalized_text"],
        )

        same_family = left["family"] == right["family"]

        pairs.append({
            "left": left["case_id"],
            "right": right["case_id"],
            "left_family": left["family"],
            "right_family": right["family"],
            "same_family": same_family,
            "signature_distance": round(signature_distance, 12),
            "projected_edit_distance": round(projected_distance, 12),
            "combined_distance": round(
                0.65 * signature_distance + 0.35 * projected_distance,
                12,
            ),
        })

    return pairs


def mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def analyze_distances(
    pairs: List[Dict[str, Any]],
    distance_key: str,
) -> Dict[str, Any]:
    within = [
        pair[distance_key]
        for pair in pairs
        if pair["same_family"] is True
    ]

    cross = [
        pair[distance_key]
        for pair in pairs
        if pair["same_family"] is False
    ]

    within_mean = mean(within)
    cross_mean = mean(cross)
    margin = cross_mean - within_mean
    ratio = within_mean / cross_mean if cross_mean != 0 else None

    return {
        "distance_key": distance_key,
        "within_structure_distances": within,
        "cross_structure_distances": cross,
        "mean_within_structure_distance": round(within_mean, 12),
        "mean_cross_structure_distance": round(cross_mean, 12),
        "separation_margin": round(margin, 12),
        "within_to_cross_ratio": round(ratio, 12) if ratio is not None else None,
        "within_lower_than_cross": within_mean < cross_mean,
    }


def analyze_noise_gradient(measured: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Check whether normalized omega degrades as noise level increases.

    This is tested separately inside each family.
    """
    by_family: Dict[str, List[Dict[str, Any]]] = {}

    for item in measured:
        by_family.setdefault(item["family"], []).append(item)

    family_results = {}

    for family, items in by_family.items():
        sorted_items = sorted(items, key=lambda x: x["noise_level"])
        values = [
            item["normalized_signature"]["omega_proxy"]
            for item in sorted_items
        ]

        decreases = []
        violations = []

        for i in range(len(values) - 1):
            current_value = values[i]
            next_value = values[i + 1]

            if next_value <= current_value:
                decreases.append(True)
            else:
                decreases.append(False)
                violations.append({
                    "from_noise": sorted_items[i]["noise_level"],
                    "to_noise": sorted_items[i + 1]["noise_level"],
                    "current": current_value,
                    "next": next_value,
                    "increase": round(next_value - current_value, 12),
                })

        family_results[family] = {
            "noise_levels": [item["noise_level"] for item in sorted_items],
            "normalized_omega_values": values,
            "non_increasing": all(decreases) if decreases else True,
            "violation_count": len(violations),
            "violations": violations,
        }

    total_violations = sum(
        result["violation_count"]
        for result in family_results.values()
    )

    return {
        "family_results": family_results,
        "noise_gradient_detected": total_violations == 0,
        "total_violation_count": total_violations,
    }


def build_result(measured: List[Dict[str, Any]]) -> Dict[str, Any]:
    raw_pairs = compute_pairwise_distances(
        measured,
        signature_key="raw_signature",
    )
    normalized_pairs = compute_pairwise_distances(
        measured,
        signature_key="normalized_signature",
    )

    raw_combined = analyze_distances(raw_pairs, "combined_distance")
    normalized_combined = analyze_distances(normalized_pairs, "combined_distance")

    raw_signature_only = analyze_distances(raw_pairs, "signature_distance")
    normalized_signature_only = analyze_distances(
        normalized_pairs,
        "signature_distance",
    )
    normalized_projected_only = analyze_distances(
        normalized_pairs,
        "projected_edit_distance",
    )

    noise_gradient = analyze_noise_gradient(measured)

    raw_margin = raw_combined["separation_margin"]
    normalized_margin = normalized_combined["separation_margin"]

    pass_condition = (
        normalized_combined["within_lower_than_cross"] is True
        and normalized_margin > raw_margin
        and normalized_margin > 0.05
        and noise_gradient["noise_gradient_detected"] is True
    )

    weak_condition = (
        normalized_combined["within_lower_than_cross"] is True
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
            "Noisy normalization-aware test of whether structural family identity "
            "remains measurable under imperfect representation."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "cases": measured,
        "raw_pairwise_distances": raw_pairs,
        "normalized_pairwise_distances": normalized_pairs,
        "raw_combined_analysis": raw_combined,
        "normalized_combined_analysis": normalized_combined,
        "raw_signature_only_analysis": raw_signature_only,
        "normalized_signature_only_analysis": normalized_signature_only,
        "normalized_projected_only_analysis": normalized_projected_only,
        "noise_gradient": noise_gradient,
        "pass_condition": (
            "normalized_within_lower_than_cross == true and "
            "normalized_margin > raw_margin and normalized_margin > 0.05 and "
            "noise_gradient_detected == true"
        ),
        "status": status,
        "interpretation": (
            "PASS means normalization preserved family separation under noisy "
            "representations and degradation followed the noise gradient."
            if status == "PASS"
            else
            "WEAK_PASS means normalization improved family separation, but one "
            "or more strength conditions failed."
            if status == "WEAK_PASS"
            else
            "FAIL means noisy normalization did not recover family separation "
            "under this toy setup."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy noisy normalization experiment.",
            "The normalization layer is hand-built.",
            "Only two structural families are tested.",
            "Only four representations per family are tested.",
            "Noise is deterministic and synthetic.",
            "No universal invariance claim is made.",
            "No semantic correctness is evaluated.",
            "No external reproduction is included yet.",
        ],
        "reproduction_command": "python examples/cross_domain_invariance_v0_2.py",
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
    print("OMNIA-VALIDATION — Cross-Domain Invariance v0.2")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Claim level: {result['claim_level']}")
    print()

    print("Cases:")
    for item in result["cases"]:
        print(
            f"  {item['case_id']:32s} "
            f"family={item['family']:15s} "
            f"noise={item['noise_level']} "
            f"raw_omega={item['raw_signature']['omega_proxy']} "
            f"norm_omega={item['normalized_signature']['omega_proxy']} "
            f"norm={item['normalized_text'][:32]}"
        )

    print()
    print("Raw combined distance analysis:")
    raw = result["raw_combined_analysis"]
    print(f"  mean within:        {raw['mean_within_structure_distance']}")
    print(f"  mean cross:         {raw['mean_cross_structure_distance']}")
    print(f"  margin:             {raw['separation_margin']}")
    print(f"  within < cross:     {raw['within_lower_than_cross']}")

    print()
    print("Normalized combined distance analysis:")
    norm = result["normalized_combined_analysis"]
    print(f"  mean within:        {norm['mean_within_structure_distance']}")
    print(f"  mean cross:         {norm['mean_cross_structure_distance']}")
    print(f"  margin:             {norm['separation_margin']}")
    print(f"  within < cross:     {norm['within_lower_than_cross']}")

    print()
    print("Projected-only normalized analysis:")
    projected = result["normalized_projected_only_analysis"]
    print(f"  mean within:        {projected['mean_within_structure_distance']}")
    print(f"  mean cross:         {projected['mean_cross_structure_distance']}")
    print(f"  margin:             {projected['separation_margin']}")
    print(f"  within < cross:     {projected['within_lower_than_cross']}")

    print()
    print("Noise gradient:")
    noise = result["noise_gradient"]
    print(f"  detected:           {noise['noise_gradient_detected']}")
    print(f"  violations:         {noise['total_violation_count']}")
    for family, family_result in noise["family_results"].items():
        print(
            f"  {family}: values={family_result['normalized_omega_values']} "
            f"non_increasing={family_result['non_increasing']} "
            f"violations={family_result['violation_count']}"
        )

    print()
    print("Improvement:")
    print(f"  raw margin:         {raw['separation_margin']}")
    print(f"  normalized margin:  {norm['separation_margin']}")
    print(
        "  normalized > raw:   "
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