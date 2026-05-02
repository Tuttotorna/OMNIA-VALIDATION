#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Projection Boundary Map v0

Purpose:
    Build a minimal taxonomy of failure modes for first-seen canonical projection.

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

This experiment moves from isolated adversarial examples to boundary mapping.

Core boundary:
    measurement != inference != decision

Core question:
    Which projection assumptions break under which attack families?

Output:
    attack_family
    projection_assumption_broken
    expected_effect
    observed_effect
    severity
    detectable

PASS condition:
    - at least four attack families are evaluated
    - at least three distinct boundary effects are detected
    - clean controls remain valid
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


EXPERIMENT_NAME = "projection_boundary_map_v0"
DOMAIN = "projection_failure_boundary_mapping"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "projection_boundary_map_v0.json"


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
# Canonical projection under test
# ---------------------------------------------------------------------

def tokenize_representation(text: str) -> List[str]:
    json_values = re.findall(r'"v"\s*:\s*"?([A-Za-z0-9_]+)"?\s*}', text)
    if json_values:
        return json_values

    if "|" in text:
        return [token.strip() for token in text.split("|") if token.strip()]

    if " " in text:
        return [token.strip() for token in text.split() if token.strip()]

    return list(text)


def canonical_project(text: str) -> str:
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


def compare_projected(left_text: str, right_text: str) -> Dict[str, Any]:
    left_projected = canonical_project(left_text)
    right_projected = canonical_project(right_text)

    left_signature = structural_signature(left_projected)
    right_signature = structural_signature(right_projected)

    signature_distance = euclidean_distance(
        vectorize(left_signature),
        vectorize(right_signature),
    )
    edit_distance = normalized_edit_distance(left_projected, right_projected)

    combined_distance = 0.65 * signature_distance + 0.35 * edit_distance

    return {
        "left_projected": left_projected,
        "right_projected": right_projected,
        "left_projected_preview": left_projected[:64],
        "right_projected_preview": right_projected[:64],
        "left_omega_proxy": left_signature["omega_proxy"],
        "right_omega_proxy": right_signature["omega_proxy"],
        "signature_distance": round(signature_distance, 12),
        "projected_edit_distance": round(edit_distance, 12),
        "combined_distance": round(combined_distance, 12),
    }


# ---------------------------------------------------------------------
# Boundary cases
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


def json_like(tokens: List[str]) -> str:
    return ",".join(f'{{"v":"{token}"}}' for token in tokens)


def build_boundary_tests() -> List[Dict[str, Any]]:
    """
    Build test pairs that map projection assumptions to attack families.

    Each pair has:
        control text
        attacked text
        intended relation
        expected effect
    """
    tests: List[Dict[str, Any]] = []

    # 1. MANY_TO_ONE_COLLAPSE
    tests.append({
        "test_id": "many_to_one_collapse_binary_domains",
        "attack_family": "MANY_TO_ONE_COLLAPSE",
        "projection_assumption_broken": "token_identity_is_disposable",
        "expected_effect": "false_merge",
        "left_intended_structure": "hot_cold_alternation",
        "right_intended_structure": "buy_sell_alternation",
        "left_text": pipe(repeat(["hot", "cold"], 32)),
        "right_text": pipe(repeat(["buy", "sell"], 32)),
        "expected_detectable": True,
    })

    # 2. ALIAS_INFLATION
    alias_binary = []
    left_aliases = ["left_a", "left_b", "left_c"]
    right_aliases = ["right_a", "right_b", "right_c"]
    for i in range(32):
        alias_binary.append(left_aliases[i % 3])
        alias_binary.append(right_aliases[i % 3])

    tests.append({
        "test_id": "alias_inflation_binary",
        "attack_family": "ALIAS_INFLATION",
        "projection_assumption_broken": "stable_symbol_identity",
        "expected_effect": "false_split",
        "left_intended_structure": "binary_alternation",
        "right_intended_structure": "binary_alternation",
        "left_text": pipe(repeat(["left", "right"], 32)),
        "right_text": pipe(alias_binary),
        "expected_detectable": True,
    })

    # 3. CARDINALITY_INFLATION
    cycle_alias = []
    base_cycle = ["north", "east", "south", "west"]
    alias_map = {
        "north": ["north_a", "north_b"],
        "east": ["east_a", "east_b"],
        "south": ["south_a", "south_b"],
        "west": ["west_a", "west_b"],
    }
    for i in range(32):
        for state in base_cycle:
            cycle_alias.append(alias_map[state][i % 2])

    tests.append({
        "test_id": "cardinality_inflation_cycle",
        "attack_family": "CARDINALITY_INFLATION",
        "projection_assumption_broken": "state_cardinality_is_stable",
        "expected_effect": "false_split",
        "left_intended_structure": "four_cycle",
        "right_intended_structure": "four_cycle",
        "left_text": pipe(repeat(base_cycle, 32)),
        "right_text": pipe(cycle_alias),
        "expected_detectable": True,
    })

    # 4. SEPARATOR_ATTACK
    # Same underlying tokens, but compact form destroys intended token boundaries.
    # first-seen projection sees characters rather than tokens.
    tests.append({
        "test_id": "separator_attack_token_boundary",
        "attack_family": "SEPARATOR_ATTACK",
        "projection_assumption_broken": "token_boundaries_are_reliable",
        "expected_effect": "false_split",
        "left_intended_structure": "word_pair_alternation",
        "right_intended_structure": "word_pair_alternation",
        "left_text": pipe(repeat(["ab", "cd"], 32)),
        "right_text": "".join(repeat(["ab", "cd"], 32)),
        "expected_detectable": True,
    })

    # 5. PERIODICITY_SPOOFING
    # Different intended structures are engineered to share strong periodicity.
    tests.append({
        "test_id": "periodicity_spoofing_same_period",
        "attack_family": "PERIODICITY_SPOOFING",
        "projection_assumption_broken": "periodicity_implies_structural_equivalence",
        "expected_effect": "false_merge",
        "left_intended_structure": "binary_state_transition",
        "right_intended_structure": "two_phase_process",
        "left_text": spaced(repeat(["0", "1"], 32)),
        "right_text": spaced(repeat(["open", "close"], 32)),
        "expected_detectable": True,
    })

    # 6. LOCAL_SWAP_DRIFT
    # Same structure with local swaps. Projection should remain close but not identical.
    drift_tokens = repeat(["A", "B", "C", "D"], 32)
    for idx in range(7, len(drift_tokens) - 1, 23):
        drift_tokens[idx], drift_tokens[idx + 1] = drift_tokens[idx + 1], drift_tokens[idx]

    tests.append({
        "test_id": "local_swap_drift_cycle",
        "attack_family": "LOCAL_SWAP_DRIFT",
        "projection_assumption_broken": "local_order_is_stable",
        "expected_effect": "partial_split",
        "left_intended_structure": "four_cycle",
        "right_intended_structure": "four_cycle",
        "left_text": pipe(repeat(["A", "B", "C", "D"], 32)),
        "right_text": pipe(drift_tokens),
        "expected_detectable": True,
    })

    # 7. JSON_FIELD_ERASURE
    # Tokenizer only extracts the v field, so different metadata is erased.
    tests.append({
        "test_id": "json_field_erasure",
        "attack_family": "JSON_FIELD_ERASURE",
        "projection_assumption_broken": "ignored_fields_are_irrelevant",
        "expected_effect": "false_merge",
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
        "expected_detectable": True,
    })

    # 8. CONTROL_EQUIVALENT_BINARY
    tests.append({
        "test_id": "control_equivalent_binary",
        "attack_family": "CONTROL",
        "projection_assumption_broken": "none",
        "expected_effect": "correct_merge",
        "left_intended_structure": "binary_alternation",
        "right_intended_structure": "binary_alternation",
        "left_text": pipe(repeat(["A", "B"], 32)),
        "right_text": spaced(repeat(["1", "0"], 32)),
        "expected_detectable": True,
    })

    # 9. CONTROL_SEPARATE_BINARY_CYCLE
    tests.append({
        "test_id": "control_separate_binary_cycle",
        "attack_family": "CONTROL",
        "projection_assumption_broken": "none",
        "expected_effect": "correct_split",
        "left_intended_structure": "binary_alternation",
        "right_intended_structure": "four_cycle",
        "left_text": pipe(repeat(["A", "B"], 32)),
        "right_text": pipe(repeat(["A", "B", "C", "D"], 32)),
        "expected_detectable": True,
    })

    return tests


# ---------------------------------------------------------------------
# Boundary analysis
# ---------------------------------------------------------------------

def classify_observed_effect(
    intended_same: bool,
    edit_distance: float,
    combined_distance: float,
) -> str:
    """
    Convert observed distances into boundary effect labels.
    """
    identical_projection = edit_distance == 0.0
    near_projection = edit_distance <= 0.10
    far_projection = edit_distance >= 0.25

    if intended_same and identical_projection:
        return "correct_merge"

    if intended_same and near_projection:
        return "partial_split"

    if intended_same and far_projection:
        return "false_split"

    if not intended_same and identical_projection:
        return "false_merge"

    if not intended_same and near_projection:
        return "near_false_merge"

    if not intended_same and far_projection:
        return "correct_split"

    if combined_distance < 0.25:
        return "ambiguous_merge"

    return "ambiguous_boundary"


def severity_from_effect(
    expected_effect: str,
    observed_effect: str,
    edit_distance: float,
    combined_distance: float,
) -> float:
    """
    Compute a toy severity score in [0, 1].

    For false_merge:
        lower distance means more severe collapse.

    For false_split:
        higher distance means more severe split.

    For partial_split:
        mid-distance indicates drift.
    """
    if observed_effect in {"false_merge", "near_false_merge"}:
        return round(max(0.0, min(1.0, 1.0 - combined_distance)), 12)

    if observed_effect == "false_split":
        return round(max(0.0, min(1.0, combined_distance)), 12)

    if observed_effect == "partial_split":
        return round(max(0.0, min(1.0, edit_distance)), 12)

    if observed_effect == "ambiguous_merge":
        return round(max(0.0, min(1.0, 1.0 - combined_distance)), 12)

    if observed_effect == "ambiguous_boundary":
        return round(0.5, 12)

    return 0.0


def analyze_test(test: Dict[str, Any]) -> Dict[str, Any]:
    comparison = compare_projected(test["left_text"], test["right_text"])

    intended_same = (
        test["left_intended_structure"]
        == test["right_intended_structure"]
    )

    observed_effect = classify_observed_effect(
        intended_same=intended_same,
        edit_distance=comparison["projected_edit_distance"],
        combined_distance=comparison["combined_distance"],
    )

    expected_effect = test["expected_effect"]

    detected = observed_effect == expected_effect

    # partial split is acceptable for local drift, because the expected effect
    # itself is a partial degradation rather than a full false split.
    if expected_effect == "partial_split" and observed_effect in {
        "partial_split",
        "false_split",
    }:
        detected = True

    severity = severity_from_effect(
        expected_effect=expected_effect,
        observed_effect=observed_effect,
        edit_distance=comparison["projected_edit_distance"],
        combined_distance=comparison["combined_distance"],
    )

    return {
        "test_id": test["test_id"],
        "attack_family": test["attack_family"],
        "projection_assumption_broken": test["projection_assumption_broken"],
        "left_intended_structure": test["left_intended_structure"],
        "right_intended_structure": test["right_intended_structure"],
        "intended_same": intended_same,
        "expected_effect": expected_effect,
        "observed_effect": observed_effect,
        "detected": detected,
        "severity": severity,
        "projected_edit_distance": comparison["projected_edit_distance"],
        "combined_distance": comparison["combined_distance"],
        "left_omega_proxy": comparison["left_omega_proxy"],
        "right_omega_proxy": comparison["right_omega_proxy"],
        "left_projected_preview": comparison["left_projected_preview"],
        "right_projected_preview": comparison["right_projected_preview"],
    }


def build_boundary_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    non_control = [
        item
        for item in results
        if item["attack_family"] != "CONTROL"
    ]

    control = [
        item
        for item in results
        if item["attack_family"] == "CONTROL"
    ]

    attack_families = sorted(set(item["attack_family"] for item in non_control))
    observed_effects = sorted(set(item["observed_effect"] for item in non_control))
    broken_assumptions = sorted(
        set(item["projection_assumption_broken"] for item in non_control)
    )

    detected = [item for item in non_control if item["detected"] is True]
    undetected = [item for item in non_control if item["detected"] is False]

    control_ok = all(item["detected"] is True for item in control)

    avg_severity = (
        sum(item["severity"] for item in non_control) / len(non_control)
        if non_control
        else 0.0
    )

    max_severity = max((item["severity"] for item in non_control), default=0.0)

    return {
        "attack_family_count": len(attack_families),
        "attack_families": attack_families,
        "observed_effect_count": len(observed_effects),
        "observed_effects": observed_effects,
        "broken_assumption_count": len(broken_assumptions),
        "broken_assumptions": broken_assumptions,
        "detected_boundary_count": len(detected),
        "undetected_boundary_count": len(undetected),
        "control_count": len(control),
        "control_ok": control_ok,
        "average_severity": round(avg_severity, 12),
        "max_severity": round(max_severity, 12),
    }


def build_result(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary = build_boundary_summary(results)

    pass_condition = (
        summary["attack_family_count"] >= 4
        and summary["observed_effect_count"] >= 3
        and summary["detected_boundary_count"] >= 5
        and summary["control_ok"] is True
    )

    weak_condition = (
        summary["attack_family_count"] >= 3
        and summary["detected_boundary_count"] >= 3
    )

    if pass_condition:
        status = "PASS"
        operational_classification = "BOUNDARY_MAP_BUILT"
    elif weak_condition:
        status = "WEAK_PASS"
        operational_classification = "PARTIAL_BOUNDARY_MAP_BUILT"
    else:
        status = "FAIL"
        operational_classification = "BOUNDARY_MAP_NOT_ESTABLISHED"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Map failure families for first-seen canonical projection by linking "
            "projection assumptions to attack effects."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "boundary_results": results,
        "boundary_summary": summary,
        "pass_condition": (
            "attack_family_count >= 4 and observed_effect_count >= 3 and "
            "detected_boundary_count >= 5 and control_ok == true"
        ),
        "status": status,
        "operational_classification": operational_classification,
        "main_insight": (
            "Projection robustness is not a single property. Different attack "
            "families break different assumptions and produce different failure "
            "signatures."
        ),
        "interpretation": (
            "PASS means a minimal boundary map was built: multiple attack "
            "families, multiple observed effects, and valid controls."
            if status == "PASS"
            else
            "WEAK_PASS means partial boundary mapping succeeded but the full "
            "mapping criterion was not satisfied."
            if status == "WEAK_PASS"
            else
            "FAIL means the experiment did not establish a useful boundary map."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy projection boundary map.",
            "The canonical projection is hand-built.",
            "Attack families are synthetic and manually designed.",
            "Severity is a toy proxy.",
            "No semantic truth is evaluated.",
            "No universal robustness claim is made.",
            "No external reproduction is included yet.",
        ],
        "reproduction_command": "python examples/projection_boundary_map_v0.py",
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    tests = build_boundary_tests()
    boundary_results = [analyze_test(test) for test in tests]
    result = build_result(boundary_results)

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("OMNIA-VALIDATION — Projection Boundary Map v0")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Operational classification: {result['operational_classification']}")
    print(f"Claim level: {result['claim_level']}")
    print()

    print("Boundary results:")
    for item in result["boundary_results"]:
        print(
            f"  {item['test_id']:36s} "
            f"family={item['attack_family']:24s} "
            f"expected={item['expected_effect']:16s} "
            f"observed={item['observed_effect']:18s} "
            f"detected={str(item['detected']):5s} "
            f"severity={item['severity']}"
        )

    print()
    print("Boundary summary:")
    summary = result["boundary_summary"]
    print(f"  attack_family_count:       {summary['attack_family_count']}")
    print(f"  observed_effect_count:     {summary['observed_effect_count']}")
    print(f"  broken_assumption_count:   {summary['broken_assumption_count']}")
    print(f"  detected_boundary_count:   {summary['detected_boundary_count']}")
    print(f"  undetected_boundary_count: {summary['undetected_boundary_count']}")
    print(f"  control_ok:                {summary['control_ok']}")
    print(f"  average_severity:          {summary['average_severity']}")
    print(f"  max_severity:              {summary['max_severity']}")

    print()
    print("Attack families:")
    for family in summary["attack_families"]:
        print(f"  - {family}")

    print()
    print("Observed effects:")
    for effect in summary["observed_effects"]:
        print(f"  - {effect}")

    print()
    print("Broken assumptions:")
    for assumption in summary["broken_assumptions"]:
        print(f"  - {assumption}")

    print()
    print("Pass condition:")
    print(f"  {result['pass_condition']}")

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()