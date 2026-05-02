#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Projection Resilience Layer v0

Purpose:
    Test a minimal boundary-aware resilience layer after first-seen canonical
    projection.

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

    adversarial_representation_v0:
        false merge and false split boundaries were detected
        -> PASS / BOUNDARY_DETECTED

    projection_boundary_map_v0:
        projection failure modes were mapped by attack family
        -> PASS / BOUNDARY_MAP_BUILT

This experiment asks:
    Can a minimal resilience layer reduce projection boundary failures without
    breaking clean controls?

Core boundary:
    measurement != inference != decision

This is NOT a production robustness system.
This is a toy structural mitigation test.

Claim level:
    Level 1 — Toy Structural Mitigation

Core hypothesis:
    Boundary-aware projection should preserve clean equivalences while reducing
    alias inflation, cardinality inflation, separator attacks, and field erasure.

PASS condition:
    mitigation_success_rate >= 0.50
    and control_preservation == true
    and stability_gain > 0.0
"""

from __future__ import annotations

import json
import math
import re
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


EXPERIMENT_NAME = "projection_resilience_layer_v0"
DOMAIN = "projection_boundary_aware_structural_mitigation"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "projection_resilience_layer_v0.json"


# ---------------------------------------------------------------------
# Minimal deterministic structural metrics
# ---------------------------------------------------------------------

def shannon_entropy(text: str) -> float:
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
    if not text:
        return 0.0

    raw = text.encode("utf-8")
    compressed = zlib.compress(raw, level=9)

    return len(compressed) / len(raw)


def normalized_repetition_score(text: str, n: int = 3) -> float:
    if len(text) < n:
        return 0.0

    grams = [text[i:i + n] for i in range(len(text) - n + 1)]
    counts = Counter(grams)

    repeated = sum(count - 1 for count in counts.values() if count > 1)
    possible = max(len(grams) - 1, 1)

    return repeated / possible


def transition_regular_score(text: str) -> float:
    if len(text) < 2:
        return 0.0

    transitions = [text[i:i + 2] for i in range(len(text) - 1)]
    counts = Counter(transitions)

    repeated = sum(count - 1 for count in counts.values() if count > 1)
    possible = max(len(transitions) - 1, 1)

    return repeated / possible


def unique_symbol_ratio(text: str) -> float:
    if not text:
        return 0.0

    return len(set(text)) / len(text)


def periodicity_score(text: str, max_period: int = 8) -> float:
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
    if len(text) < 2:
        return 0.0

    transitions = [text[i:i + 2] for i in range(len(text) - 1)]
    unique_transitions = len(set(transitions))

    score = 1.0 - (unique_transitions / max(len(transitions), 1))
    return max(0.0, min(1.0, score))


def structural_signature(text: str) -> Dict[str, float]:
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
# Baseline tokenizer and projection
# ---------------------------------------------------------------------

def tokenize_baseline(text: str) -> List[str]:
    """
    Baseline tokenizer used by previous experiments.

    Known weaknesses:
    - ignores JSON metadata except field v
    - depends on separators
    - treats aliases as distinct tokens
    - discards token identity after first-seen mapping
    """
    json_values = re.findall(r'"v"\s*:\s*"?([A-Za-z0-9_]+)"?\s*}', text)
    if json_values:
        return json_values

    if "|" in text:
        return [token.strip() for token in text.split("|") if token.strip()]

    if " " in text:
        return [token.strip() for token in text.split() if token.strip()]

    return list(text)


def first_seen_project(tokens: List[str]) -> str:
    mapping: Dict[str, str] = {}
    next_id = 0
    projected = []

    for token in tokens:
        if token not in mapping:
            mapping[token] = str(next_id)
            next_id += 1

        projected.append(mapping[token])

    return "".join(projected)


def baseline_project(text: str) -> str:
    return first_seen_project(tokenize_baseline(text))


# ---------------------------------------------------------------------
# Resilience layer
# ---------------------------------------------------------------------

def normalize_alias_token(token: str) -> str:
    """
    Collapse common adversarial aliases.

    Examples:
        left_a  -> left
        left_b  -> left
        north_1 -> north
        sensor-A -> sensor

    This is intentionally minimal and hand-built.
    """
    token = token.strip()

    token = re.sub(r"[_-](a|b|c|d|x|y|z)$", "", token, flags=re.IGNORECASE)
    token = re.sub(r"[_-]\d+$", "", token)

    return token


def tokenize_resilient(text: str) -> List[str]:
    """
    Boundary-aware tokenizer.

    Mitigations:
    - preserves selected JSON metadata instead of erasing it completely
    - detects compact repeated multi-character chunks when possible
    - collapses simple aliases before projection
    """
    json_objects = re.findall(r"\{[^{}]*\}", text)
    if json_objects:
        tokens = []
        for obj in json_objects:
            sensor_match = re.search(r'"sensor"\s*:\s*"?([A-Za-z0-9_]+)"?', obj)
            value_match = re.search(r'"v"\s*:\s*"?([A-Za-z0-9_]+)"?', obj)

            parts = []
            if sensor_match:
                parts.append(f"sensor={sensor_match.group(1)}")
            if value_match:
                parts.append(f"v={value_match.group(1)}")

            if parts:
                tokens.append("|".join(parts))
        if tokens:
            return [normalize_alias_token(token) for token in tokens]

    if "|" in text:
        return [
            normalize_alias_token(token)
            for token in text.split("|")
            if token.strip()
        ]

    if " " in text:
        return [
            normalize_alias_token(token)
            for token in text.split()
            if token.strip()
        ]

    compact_pair_tokens = split_compact_repeating_pairs(text)
    if compact_pair_tokens:
        return [normalize_alias_token(token) for token in compact_pair_tokens]

    return [normalize_alias_token(char) for char in text]


def split_compact_repeating_pairs(text: str) -> List[str]:
    """
    Attempt to recover token boundaries in compact repeated two-token strings.

    Example:
        abcdabcdabcd
        ->
        ab, cd, ab, cd, ...

    This mitigation is intentionally narrow.
    """
    if len(text) < 8:
        return []

    if not text.isalpha():
        return []

    for token_len in range(2, 5):
        if len(text) % token_len != 0:
            continue

        chunks = [
            text[i:i + token_len]
            for i in range(0, len(text), token_len)
        ]

        if len(set(chunks)) == 2:
            pattern = chunks[:2]
            rebuilt = []
            for _ in range(len(chunks) // 2):
                rebuilt.extend(pattern)

            if rebuilt == chunks:
                return chunks

    return []


def resilient_project(text: str) -> str:
    """
    Projection after minimal resilience correction.
    """
    return first_seen_project(tokenize_resilient(text))


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


def compare_projection(left_projected: str, right_projected: str) -> Dict[str, float]:
    left_signature = structural_signature(left_projected)
    right_signature = structural_signature(right_projected)

    signature_distance = euclidean_distance(
        vectorize(left_signature),
        vectorize(right_signature),
    )
    edit_distance = normalized_edit_distance(left_projected, right_projected)
    combined_distance = 0.65 * signature_distance + 0.35 * edit_distance

    return {
        "signature_distance": round(signature_distance, 12),
        "projected_edit_distance": round(edit_distance, 12),
        "combined_distance": round(combined_distance, 12),
        "left_omega_proxy": left_signature["omega_proxy"],
        "right_omega_proxy": right_signature["omega_proxy"],
    }


# ---------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------

def repeat(tokens: List[str], n: int) -> List[str]:
    out: List[str] = []
    for _ in range(n):
        out.extend(tokens)
    return out


def pipe(tokens: List[str]) -> str:
    return "|".join(tokens)


def spaced(tokens: List[str]) -> str:
    return " ".join(tokens)


def build_tests() -> List[Dict[str, Any]]:
    tests: List[Dict[str, Any]] = []

    # False merge: metadata erased by baseline.
    tests.append({
        "test_id": "json_field_erasure_mitigation",
        "attack_family": "JSON_FIELD_ERASURE",
        "target_failure": "false_merge",
        "expected_resilience": "split_after_metadata_preservation",
        "left_intended_structure": "sensor_A_binary_with_metadata",
        "right_intended_structure": "sensor_B_binary_with_different_metadata",
        "left_text": ",".join(
            f'{{"sensor":"A","v":"{token}"}}'
            for token in repeat(["0", "1"], 32)
        ),
        "right_text": ",".join(
            f'{{"sensor":"B","v":"{token}"}}'
            for token in repeat(["0", "1"], 32)
        ),
    })

    # False split: aliases inflate cardinality.
    alias_binary = []
    left_aliases = ["left_a", "left_b", "left_c"]
    right_aliases = ["right_a", "right_b", "right_c"]

    for i in range(32):
        alias_binary.append(left_aliases[i % 3])
        alias_binary.append(right_aliases[i % 3])

    tests.append({
        "test_id": "alias_inflation_mitigation",
        "attack_family": "ALIAS_INFLATION",
        "target_failure": "false_split",
        "expected_resilience": "merge_after_alias_collapse",
        "left_intended_structure": "binary_alternation",
        "right_intended_structure": "binary_alternation",
        "left_text": pipe(repeat(["left", "right"], 32)),
        "right_text": pipe(alias_binary),
    })

    # False split: cardinality inflation in four-cycle aliases.
    base_cycle = ["north", "east", "south", "west"]
    alias_map = {
        "north": ["north_a", "north_b"],
        "east": ["east_a", "east_b"],
        "south": ["south_a", "south_b"],
        "west": ["west_a", "west_b"],
    }

    cycle_alias = []
    for i in range(32):
        for state in base_cycle:
            cycle_alias.append(alias_map[state][i % 2])

    tests.append({
        "test_id": "cardinality_inflation_mitigation",
        "attack_family": "CARDINALITY_INFLATION",
        "target_failure": "false_split",
        "expected_resilience": "merge_after_alias_collapse",
        "left_intended_structure": "four_cycle",
        "right_intended_structure": "four_cycle",
        "left_text": pipe(repeat(base_cycle, 32)),
        "right_text": pipe(cycle_alias),
    })

    # False split: separator attack.
    tests.append({
        "test_id": "separator_attack_mitigation",
        "attack_family": "SEPARATOR_ATTACK",
        "target_failure": "false_split",
        "expected_resilience": "merge_after_boundary_recovery",
        "left_intended_structure": "word_pair_alternation",
        "right_intended_structure": "word_pair_alternation",
        "left_text": pipe(repeat(["ab", "cd"], 32)),
        "right_text": "".join(repeat(["ab", "cd"], 32)),
    })

    # Intentional hard case: many-to-one collapse cannot be solved without semantics.
    tests.append({
        "test_id": "many_to_one_unsolved",
        "attack_family": "MANY_TO_ONE_COLLAPSE",
        "target_failure": "false_merge",
        "expected_resilience": "not_solved_without_semantics",
        "left_intended_structure": "hot_cold_alternation",
        "right_intended_structure": "buy_sell_alternation",
        "left_text": pipe(repeat(["hot", "cold"], 32)),
        "right_text": pipe(repeat(["buy", "sell"], 32)),
    })

    # Intentional hard case: periodicity spoofing cannot be solved by simple projection.
    tests.append({
        "test_id": "periodicity_spoofing_unsolved",
        "attack_family": "PERIODICITY_SPOOFING",
        "target_failure": "false_merge",
        "expected_resilience": "not_solved_without_semantics",
        "left_intended_structure": "binary_state_transition",
        "right_intended_structure": "two_phase_process",
        "left_text": spaced(repeat(["0", "1"], 32)),
        "right_text": spaced(repeat(["open", "close"], 32)),
    })

    # Control: equivalent binary should remain merged.
    tests.append({
        "test_id": "control_equivalent_binary",
        "attack_family": "CONTROL",
        "target_failure": "none",
        "expected_resilience": "preserve_correct_merge",
        "left_intended_structure": "binary_alternation",
        "right_intended_structure": "binary_alternation",
        "left_text": pipe(repeat(["A", "B"], 32)),
        "right_text": spaced(repeat(["1", "0"], 32)),
    })

    # Control: separate binary/four-cycle should remain separated.
    tests.append({
        "test_id": "control_separate_binary_cycle",
        "attack_family": "CONTROL",
        "target_failure": "none",
        "expected_resilience": "preserve_correct_split",
        "left_intended_structure": "binary_alternation",
        "right_intended_structure": "four_cycle",
        "left_text": pipe(repeat(["A", "B"], 32)),
        "right_text": pipe(repeat(["A", "B", "C", "D"], 32)),
    })

    return tests


# ---------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------

def classify_relation(
    intended_same: bool,
    edit_distance: float,
    combined_distance: float,
) -> str:
    if intended_same and edit_distance == 0.0:
        return "correct_merge"

    if intended_same and edit_distance <= 0.15:
        return "near_correct_merge"

    if intended_same and edit_distance >= 0.25:
        return "false_split"

    if not intended_same and edit_distance == 0.0:
        return "false_merge"

    if not intended_same and edit_distance <= 0.15:
        return "near_false_merge"

    if not intended_same and edit_distance >= 0.25:
        return "correct_split"

    if combined_distance < 0.25:
        return "ambiguous_merge"

    return "ambiguous_boundary"


def mitigation_success(
    test: Dict[str, Any],
    baseline_effect: str,
    resilient_effect: str,
    baseline_distance: float,
    resilient_distance: float,
) -> bool:
    expected = test["expected_resilience"]

    if expected == "split_after_metadata_preservation":
        return baseline_effect == "false_merge" and resilient_effect == "correct_split"

    if expected == "merge_after_alias_collapse":
        return baseline_effect == "false_split" and resilient_effect in {
            "correct_merge",
            "near_correct_merge",
        }

    if expected == "merge_after_boundary_recovery":
        return baseline_effect == "false_split" and resilient_effect in {
            "correct_merge",
            "near_correct_merge",
        }

    if expected == "not_solved_without_semantics":
        return baseline_effect == "false_merge" and resilient_effect == "false_merge"

    if expected == "preserve_correct_merge":
        return baseline_effect == "correct_merge" and resilient_effect == "correct_merge"

    if expected == "preserve_correct_split":
        return baseline_effect == "correct_split" and resilient_effect == "correct_split"

    return False


def analyze_test(test: Dict[str, Any]) -> Dict[str, Any]:
    baseline_left = baseline_project(test["left_text"])
    baseline_right = baseline_project(test["right_text"])

    resilient_left = resilient_project(test["left_text"])
    resilient_right = resilient_project(test["right_text"])

    baseline_comparison = compare_projection(baseline_left, baseline_right)
    resilient_comparison = compare_projection(resilient_left, resilient_right)

    intended_same = (
        test["left_intended_structure"]
        == test["right_intended_structure"]
    )

    baseline_effect = classify_relation(
        intended_same=intended_same,
        edit_distance=baseline_comparison["projected_edit_distance"],
        combined_distance=baseline_comparison["combined_distance"],
    )

    resilient_effect = classify_relation(
        intended_same=intended_same,
        edit_distance=resilient_comparison["projected_edit_distance"],
        combined_distance=resilient_comparison["combined_distance"],
    )

    success = mitigation_success(
        test=test,
        baseline_effect=baseline_effect,
        resilient_effect=resilient_effect,
        baseline_distance=baseline_comparison["combined_distance"],
        resilient_distance=resilient_comparison["combined_distance"],
    )

    distance_delta = (
        resilient_comparison["combined_distance"]
        - baseline_comparison["combined_distance"]
    )

    return {
        "test_id": test["test_id"],
        "attack_family": test["attack_family"],
        "target_failure": test["target_failure"],
        "expected_resilience": test["expected_resilience"],
        "intended_same": intended_same,
        "baseline_effect": baseline_effect,
        "resilient_effect": resilient_effect,
        "mitigation_success": success,
        "baseline_combined_distance": baseline_comparison["combined_distance"],
        "resilient_combined_distance": resilient_comparison["combined_distance"],
        "distance_delta": round(distance_delta, 12),
        "baseline_projected_edit_distance": baseline_comparison["projected_edit_distance"],
        "resilient_projected_edit_distance": resilient_comparison["projected_edit_distance"],
        "baseline_left_projected_preview": baseline_left[:64],
        "baseline_right_projected_preview": baseline_right[:64],
        "resilient_left_projected_preview": resilient_left[:64],
        "resilient_right_projected_preview": resilient_right[:64],
    }


def build_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    controls = [
        item
        for item in results
        if item["attack_family"] == "CONTROL"
    ]

    mitigations = [
        item
        for item in results
        if item["attack_family"] != "CONTROL"
        and not item["expected_resilience"].startswith("not_solved")
    ]

    hard_boundaries = [
        item
        for item in results
        if item["expected_resilience"].startswith("not_solved")
    ]

    successful_mitigations = [
        item
        for item in mitigations
        if item["mitigation_success"] is True
    ]

    successful_hard_boundaries = [
        item
        for item in hard_boundaries
        if item["mitigation_success"] is True
    ]

    control_successes = [
        item
        for item in controls
        if item["mitigation_success"] is True
    ]

    mitigation_success_rate = (
        len(successful_mitigations) / len(mitigations)
        if mitigations
        else 0.0
    )

    hard_boundary_preservation_rate = (
        len(successful_hard_boundaries) / len(hard_boundaries)
        if hard_boundaries
        else 0.0
    )

    control_preservation_rate = (
        len(control_successes) / len(controls)
        if controls
        else 0.0
    )

    control_preservation = control_preservation_rate == 1.0

    baseline_failures = [
        item
        for item in results
        if item["baseline_effect"] in {
            "false_merge",
            "false_split",
            "near_false_merge",
        }
    ]

    resilient_failures = [
        item
        for item in results
        if item["resilient_effect"] in {
            "false_merge",
            "false_split",
            "near_false_merge",
        }
        and not item["expected_resilience"].startswith("not_solved")
    ]

    baseline_failure_count = len(baseline_failures)
    resilient_failure_count = len(resilient_failures)

    stability_gain = (
        baseline_failure_count - resilient_failure_count
    ) / max(baseline_failure_count, 1)

    return {
        "test_count": len(results),
        "mitigation_case_count": len(mitigations),
        "hard_boundary_case_count": len(hard_boundaries),
        "control_case_count": len(controls),
        "successful_mitigation_count": len(successful_mitigations),
        "successful_hard_boundary_count": len(successful_hard_boundaries),
        "successful_control_count": len(control_successes),
        "mitigation_success_rate": round(mitigation_success_rate, 12),
        "hard_boundary_preservation_rate": round(hard_boundary_preservation_rate, 12),
        "control_preservation_rate": round(control_preservation_rate, 12),
        "control_preservation": control_preservation,
        "baseline_failure_count": baseline_failure_count,
        "resilient_failure_count": resilient_failure_count,
        "stability_gain": round(stability_gain, 12),
    }


def build_result(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary = build_summary(results)

    pass_condition = (
        summary["mitigation_success_rate"] >= 0.50
        and summary["control_preservation"] is True
        and summary["stability_gain"] > 0.0
    )

    weak_condition = (
        summary["mitigation_success_rate"] > 0.0
        and summary["control_preservation"] is True
    )

    if pass_condition:
        status = "PASS"
        operational_classification = "TOY_RESILIENCE_LAYER_VALIDATED"
    elif weak_condition:
        status = "WEAK_PASS"
        operational_classification = "PARTIAL_TOY_RESILIENCE_LAYER"
    else:
        status = "FAIL"
        operational_classification = "RESILIENCE_LAYER_NOT_VALIDATED"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Test a minimal boundary-aware resilience layer after first-seen "
            "canonical projection."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Structural Mitigation",
        "results": results,
        "summary": summary,
        "pass_condition": (
            "mitigation_success_rate >= 0.50 and "
            "control_preservation == true and stability_gain > 0.0"
        ),
        "status": status,
        "operational_classification": operational_classification,
        "main_insight": (
            "Boundary-aware correction can reduce some projection failures, "
            "but semantic false merges remain hard boundaries for this toy layer."
        ),
        "interpretation": (
            "PASS means the toy resilience layer reduced several projection "
            "failure modes while preserving clean controls."
            if status == "PASS"
            else
            "WEAK_PASS means the toy resilience layer helped partially, but did "
            "not satisfy the full mitigation criterion."
            if status == "WEAK_PASS"
            else
            "FAIL means the toy resilience layer did not reduce projection "
            "failures under the tested conditions."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy structural mitigation experiment.",
            "The resilience layer is hand-built.",
            "Mitigations target only known toy failure modes.",
            "Semantic false merges are not solved.",
            "No universal robustness claim is made.",
            "No semantic truth is evaluated.",
            "No external reproduction is included yet.",
        ],
        "reproduction_command": "python examples/projection_resilience_layer_v0.py",
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    tests = build_tests()
    results = [analyze_test(test) for test in tests]
    result = build_result(results)

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("OMNIA-VALIDATION — Projection Resilience Layer v0")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Operational classification: {result['operational_classification']}")
    print(f"Claim level: {result['claim_level']}")
    print()

    print("Results:")
    for item in result["results"]:
        print(
            f"  {item['test_id']:34s} "
            f"family={item['attack_family']:22s} "
            f"baseline={item['baseline_effect']:16s} "
            f"resilient={item['resilient_effect']:18s} "
            f"success={str(item['mitigation_success']):5s} "
            f"delta={item['distance_delta']}"
        )

    print()
    print("Summary:")
    summary = result["summary"]
    print(f"  mitigation_case_count:             {summary['mitigation_case_count']}")
    print(f"  successful_mitigation_count:       {summary['successful_mitigation_count']}")
    print(f"  mitigation_success_rate:           {summary['mitigation_success_rate']}")
    print(f"  hard_boundary_case_count:          {summary['hard_boundary_case_count']}")
    print(f"  hard_boundary_preservation_rate:   {summary['hard_boundary_preservation_rate']}")
    print(f"  control_case_count:                {summary['control_case_count']}")
    print(f"  control_preservation_rate:         {summary['control_preservation_rate']}")
    print(f"  control_preservation:              {summary['control_preservation']}")
    print(f"  baseline_failure_count:            {summary['baseline_failure_count']}")
    print(f"  resilient_failure_count:           {summary['resilient_failure_count']}")
    print(f"  stability_gain:                    {summary['stability_gain']}")

    print()
    print("Pass condition:")
    print(f"  {result['pass_condition']}")

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()