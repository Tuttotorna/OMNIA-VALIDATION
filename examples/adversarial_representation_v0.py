#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Adversarial Representation v0

Purpose:
    Test whether a minimal canonical projection can be broken by adversarial
    representation design.

Previous chain:
    cross_domain_invariance_v0:
        raw representation dominated structure
        -> FAIL / NEGATIVE_RESULT

    cross_domain_invariance_v0_1:
        clean canonical projection recovered structure
        -> PASS

    cross_domain_invariance_v0_2:
        canonical projection survived deterministic noise
        -> PASS

This experiment asks:
    Can the canonical projection be fooled deliberately?

Core boundary:
    measurement != inference != decision

Adversarial failure modes:
    false_merge:
        different structures become identical or near-identical after projection

    false_split:
        same structure becomes different after projection

PASS / FAIL interpretation:
    This repository is falsification-oriented.

    If adversarial attacks are found, that is not useless failure.
    It is useful boundary evidence.

Operational classification:
    PASS:
        attacks were detected and documented clearly.

    WEAK_PASS:
        partial attack evidence was detected.

    FAIL:
        attack logic did not expose meaningful boundary behavior.
"""

from __future__ import annotations

import json
import math
import re
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


EXPERIMENT_NAME = "adversarial_representation_v0"
DOMAIN = "adversarial_representation_against_canonical_projection"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "adversarial_representation_v0.json"


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
# Canonical projection under test
# ---------------------------------------------------------------------

def tokenize_representation(text: str) -> List[str]:
    """
    Extract structural tokens from mixed representations.

    This is the same minimal hand-built normalization idea used in previous
    cross-domain invariance experiments.

    Known weakness:
        It is order-of-first-appearance based.
        Therefore token identity is discarded.
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

    Example:
        A B A B -> 0101
        X Y X Y -> 0101

    This intentionally removes lexical identity.

    This property can be useful for invariance.
    It can also be attacked.
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
# Distance helpers
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


def combined_distance(left_text: str, right_text: str) -> Dict[str, float]:
    """
    Compare two texts after canonical projection.
    """
    left_projected = canonical_project(left_text)
    right_projected = canonical_project(right_text)

    left_signature = structural_signature(left_projected)
    right_signature = structural_signature(right_projected)

    signature_distance = euclidean_distance(
        vectorize(left_signature),
        vectorize(right_signature),
    )
    projected_edit = normalized_edit_distance(left_projected, right_projected)

    combined = 0.65 * signature_distance + 0.35 * projected_edit

    return {
        "signature_distance": round(signature_distance, 12),
        "projected_edit_distance": round(projected_edit, 12),
        "combined_distance": round(combined, 12),
        "left_projected": left_projected,
        "right_projected": right_projected,
        "left_omega_proxy": left_signature["omega_proxy"],
        "right_omega_proxy": right_signature["omega_proxy"],
    }


# ---------------------------------------------------------------------
# Adversarial cases
# ---------------------------------------------------------------------

def build_cases() -> List[Dict[str, Any]]:
    """
    Build adversarial cases against first-seen canonical projection.

    false_merge:
        Different intended structures collapse into same projected form.

    false_split:
        Same intended structure becomes different projected form because
        token boundary / token identity is manipulated.
    """
    repeats = 32

    cases: List[Dict[str, Any]] = []

    # ------------------------------------------------------------
    # FALSE MERGE ATTACKS
    # ------------------------------------------------------------

    # Different semantic labels, same two-token alternation.
    # Canonical projection discards labels, so both become 0101...
    cases.append({
        "case_id": "false_merge_A_temperature",
        "attack_type": "false_merge",
        "expected_failure": True,
        "intended_structure": "temperature_hot_cold_alternation",
        "text": "|".join(["hot", "cold"] * repeats),
        "description": "Alternating hot/cold labels.",
    })

    cases.append({
        "case_id": "false_merge_B_finance",
        "attack_type": "false_merge",
        "expected_failure": True,
        "intended_structure": "finance_buy_sell_alternation",
        "text": "|".join(["buy", "sell"] * repeats),
        "description": "Alternating buy/sell labels; different intended domain but same token pattern.",
    })

    # Different magnitude meaning, same first-seen pattern.
    cases.append({
        "case_id": "false_merge_C_low_high",
        "attack_type": "false_merge",
        "expected_failure": True,
        "intended_structure": "low_high_alternation",
        "text": " ".join(["low", "high"] * repeats),
        "description": "Low/high alternation.",
    })

    cases.append({
        "case_id": "false_merge_D_zero_extreme",
        "attack_type": "false_merge",
        "expected_failure": True,
        "intended_structure": "zero_extreme_alternation",
        "text": " ".join(["zero", "extreme"] * repeats),
        "description": "Zero/extreme alternation; same formal pattern but different magnitude semantics.",
    })

    # ------------------------------------------------------------
    # FALSE SPLIT ATTACKS
    # ------------------------------------------------------------

    # Same intended alternating structure, but one representation introduces
    # fresh aliases for the same conceptual states.
    cases.append({
        "case_id": "false_split_A_clean",
        "attack_type": "false_split",
        "expected_failure": True,
        "intended_structure": "same_binary_alternation",
        "text": "|".join(["left", "right"] * repeats),
        "description": "Clean binary alternation.",
    })

    # Same left/right structure, but left has aliases L1/L2/L3 and right has R1/R2/R3.
    # First-seen projection treats aliases as new states, so it becomes more complex.
    alias_tokens = []
    left_aliases = ["left_a", "left_b", "left_c"]
    right_aliases = ["right_a", "right_b", "right_c"]
    for i in range(repeats):
        alias_tokens.append(left_aliases[i % len(left_aliases)])
        alias_tokens.append(right_aliases[i % len(right_aliases)])

    cases.append({
        "case_id": "false_split_B_aliases",
        "attack_type": "false_split",
        "expected_failure": True,
        "intended_structure": "same_binary_alternation",
        "text": "|".join(alias_tokens),
        "description": "Same binary alternation with adversarial aliases.",
    })

    # Same intended ABCD cycle, but aliases expand each state into multiple surface tokens.
    cases.append({
        "case_id": "false_split_C_clean_cycle",
        "attack_type": "false_split",
        "expected_failure": True,
        "intended_structure": "same_four_cycle",
        "text": "|".join(["north", "east", "south", "west"] * repeats),
        "description": "Clean four-state cycle.",
    })

    cycle_alias_tokens = []
    aliases = {
        "north": ["north_a", "north_b"],
        "east": ["east_a", "east_b"],
        "south": ["south_a", "south_b"],
        "west": ["west_a", "west_b"],
    }
    base_cycle = ["north", "east", "south", "west"]
    for i in range(repeats):
        for state in base_cycle:
            cycle_alias_tokens.append(aliases[state][i % 2])

    cases.append({
        "case_id": "false_split_D_alias_cycle",
        "attack_type": "false_split",
        "expected_failure": True,
        "intended_structure": "same_four_cycle",
        "text": "|".join(cycle_alias_tokens),
        "description": "Same four-state cycle with adversarial aliases.",
    })

    # ------------------------------------------------------------
    # CONTROL CASES
    # ------------------------------------------------------------

    cases.append({
        "case_id": "control_binary_clean_1",
        "attack_type": "control",
        "expected_failure": False,
        "intended_structure": "binary_alternation",
        "text": "|".join(["A", "B"] * repeats),
        "description": "Control binary alternation.",
    })

    cases.append({
        "case_id": "control_binary_clean_2",
        "attack_type": "control",
        "expected_failure": False,
        "intended_structure": "binary_alternation",
        "text": " ".join(["1", "0"] * repeats),
        "description": "Control equivalent binary alternation.",
    })

    cases.append({
        "case_id": "control_four_cycle_1",
        "attack_type": "control",
        "expected_failure": False,
        "intended_structure": "four_cycle",
        "text": "|".join(["A", "B", "C", "D"] * repeats),
        "description": "Control four-cycle.",
    })

    cases.append({
        "case_id": "control_four_cycle_2",
        "attack_type": "control",
        "expected_failure": False,
        "intended_structure": "four_cycle",
        "text": " ".join(["1", "2", "3", "4"] * repeats),
        "description": "Control equivalent four-cycle.",
    })

    return cases


# ---------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------

def measure_cases(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    measured = []

    for case in cases:
        projected = canonical_project(case["text"])
        signature = structural_signature(projected)

        measured.append({
            "case_id": case["case_id"],
            "attack_type": case["attack_type"],
            "expected_failure": case["expected_failure"],
            "intended_structure": case["intended_structure"],
            "description": case["description"],
            "projected": projected,
            "projected_preview": projected[:64],
            "projected_length": len(projected),
            "signature": signature,
        })

    return measured


def find_false_merge_attacks(measured: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect different intended structures that collapse to identical projection.
    """
    attacks = []

    merge_candidates = [
        item
        for item in measured
        if item["attack_type"] == "false_merge"
    ]

    for i in range(len(merge_candidates)):
        for j in range(i + 1, len(merge_candidates)):
            left = merge_candidates[i]
            right = merge_candidates[j]

            if left["intended_structure"] == right["intended_structure"]:
                continue

            distances = combined_distance(left["projected"], right["projected"])

            if distances["projected_edit_distance"] == 0.0:
                attacks.append({
                    "attack": "false_merge",
                    "left": left["case_id"],
                    "right": right["case_id"],
                    "left_intended_structure": left["intended_structure"],
                    "right_intended_structure": right["intended_structure"],
                    "projected_edit_distance": distances["projected_edit_distance"],
                    "combined_distance": distances["combined_distance"],
                    "evidence": "different intended structures collapsed to identical canonical projection",
                })

    return attacks


def find_false_split_attacks(measured: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect same intended structure that becomes separated after projection.
    """
    attacks = []

    split_candidates = [
        item
        for item in measured
        if item["attack_type"] == "false_split"
    ]

    for i in range(len(split_candidates)):
        for j in range(i + 1, len(split_candidates)):
            left = split_candidates[i]
            right = split_candidates[j]

            if left["intended_structure"] != right["intended_structure"]:
                continue

            distances = combined_distance(left["projected"], right["projected"])

            if distances["projected_edit_distance"] >= 0.20:
                attacks.append({
                    "attack": "false_split",
                    "left": left["case_id"],
                    "right": right["case_id"],
                    "intended_structure": left["intended_structure"],
                    "projected_edit_distance": distances["projected_edit_distance"],
                    "combined_distance": distances["combined_distance"],
                    "evidence": "same intended structure separated by adversarial aliases",
                })

    return attacks


def analyze_controls(measured: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Verify that basic clean controls still behave as expected.
    """
    controls = [
        item
        for item in measured
        if item["attack_type"] == "control"
    ]

    control_pairs = []

    for i in range(len(controls)):
        for j in range(i + 1, len(controls)):
            left = controls[i]
            right = controls[j]

            same_intended = left["intended_structure"] == right["intended_structure"]
            distances = combined_distance(left["projected"], right["projected"])

            control_pairs.append({
                "left": left["case_id"],
                "right": right["case_id"],
                "same_intended_structure": same_intended,
                "projected_edit_distance": distances["projected_edit_distance"],
                "combined_distance": distances["combined_distance"],
            })

    expected_equivalent_pairs = [
        pair
        for pair in control_pairs
        if pair["same_intended_structure"] is True
    ]

    expected_separate_pairs = [
        pair
        for pair in control_pairs
        if pair["same_intended_structure"] is False
    ]

    equivalent_ok = all(
        pair["projected_edit_distance"] == 0.0
        for pair in expected_equivalent_pairs
    )

    separate_ok = all(
        pair["projected_edit_distance"] > 0.0
        for pair in expected_separate_pairs
    )

    return {
        "control_pairs": control_pairs,
        "equivalent_controls_ok": equivalent_ok,
        "separate_controls_ok": separate_ok,
        "controls_ok": equivalent_ok and separate_ok,
    }


def build_result(measured: List[Dict[str, Any]]) -> Dict[str, Any]:
    false_merge_attacks = find_false_merge_attacks(measured)
    false_split_attacks = find_false_split_attacks(measured)
    control_analysis = analyze_controls(measured)

    attack_count = len(false_merge_attacks) + len(false_split_attacks)

    expected_failure_count = sum(
        1
        for item in measured
        if item["expected_failure"] is True
    )

    # In this adversarial test, detecting attacks is the desired validation outcome.
    # It means the boundary is measurable.
    if attack_count >= 2 and control_analysis["controls_ok"]:
        status = "PASS"
        operational_classification = "BOUNDARY_DETECTED"
    elif attack_count >= 1:
        status = "WEAK_PASS"
        operational_classification = "PARTIAL_BOUNDARY_DETECTED"
    else:
        status = "FAIL"
        operational_classification = "NO_ATTACK_BOUNDARY_DETECTED"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Adversarial test against first-seen canonical projection, searching "
            "for false merge and false split failure modes."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "measured_cases": measured,
        "false_merge_attacks": false_merge_attacks,
        "false_split_attacks": false_split_attacks,
        "control_analysis": control_analysis,
        "attack_count": attack_count,
        "expected_failure_case_count": expected_failure_count,
        "status": status,
        "operational_classification": operational_classification,
        "interpretation": (
            "PASS means adversarial representation attacks were detected while "
            "basic clean controls still behaved as expected. This identifies a "
            "measurable boundary of the canonical projection."
            if status == "PASS"
            else
            "WEAK_PASS means at least one adversarial boundary was detected, but "
            "the evidence is incomplete or controls were not fully clean."
            if status == "WEAK_PASS"
            else
            "FAIL means the adversarial setup did not expose meaningful boundary "
            "behavior."
        ),
        "main_insight": (
            "First-seen canonical projection is useful for clean invariance but "
            "fragile under adversarial token design."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy adversarial representation test.",
            "The canonical projection is hand-built.",
            "Attack cases are synthetic.",
            "Intended structures are manually labeled.",
            "No semantic truth is evaluated.",
            "No universal adversarial robustness claim is made.",
            "No external reproduction is included yet.",
        ],
        "reproduction_command": "python examples/adversarial_representation_v0.py",
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
    print("OMNIA-VALIDATION — Adversarial Representation v0")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Operational classification: {result['operational_classification']}")
    print(f"Claim level: {result['claim_level']}")
    print()

    print("Measured cases:")
    for item in result["measured_cases"]:
        print(
            f"  {item['case_id']:32s} "
            f"attack_type={item['attack_type']:12s} "
            f"omega={item['signature']['omega_proxy']} "
            f"projected={item['projected_preview']}"
        )

    print()
    print("False merge attacks:")
    if result["false_merge_attacks"]:
        for attack in result["false_merge_attacks"]:
            print(
                f"  {attack['left']} <-> {attack['right']} "
                f"edit={attack['projected_edit_distance']} "
                f"combined={attack['combined_distance']}"
            )
    else:
        print("  none detected")

    print()
    print("False split attacks:")
    if result["false_split_attacks"]:
        for attack in result["false_split_attacks"]:
            print(
                f"  {attack['left']} <-> {attack['right']} "
                f"edit={attack['projected_edit_distance']} "
                f"combined={attack['combined_distance']}"
            )
    else:
        print("  none detected")

    print()
    print("Controls:")
    controls = result["control_analysis"]
    print(f"  equivalent_controls_ok: {controls['equivalent_controls_ok']}")
    print(f"  separate_controls_ok:   {controls['separate_controls_ok']}")
    print(f"  controls_ok:            {controls['controls_ok']}")

    print()
    print("Summary:")
    print(f"  attack_count: {result['attack_count']}")
    print(f"  expected_failure_case_count: {result['expected_failure_case_count']}")
    print(f"  result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()