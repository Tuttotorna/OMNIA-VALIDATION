#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Semantic vs Structural Separation v0

Purpose:
    Minimal controlled experiment showing that semantic correctness and
    structural stability are separable axes.

This experiment does NOT prove semantic truth.

It uses manually labeled toy cases to test whether a structural proxy can
separate structural stability from semantic correctness.

Core boundary:
    structural validity != semantic correctness
    measurement != inference != decision

Expected behavior:
    - semantically correct + structurally stable      -> high structural score
    - semantically wrong + structurally stable        -> high structural score
    - semantically correct + structurally unstable    -> lower structural score
    - semantically wrong + structurally unstable      -> lower structural score

PASS condition:
    Structural scores must group by structural stability,
    not by semantic correctness.
"""

from __future__ import annotations

import json
import math
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


EXPERIMENT_NAME = "semantic_vs_structural_separation_v0"
DOMAIN = "semantic_structural_axis_separation"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "semantic_vs_structural_separation_v0.json"


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

    Lower values usually indicate more compressible structure.
    Higher values usually indicate weaker repeated/compressible structure.
    """
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


def line_contract_score(text: str) -> float:
    """
    Measure whether text follows a simple repeated answer contract.

    Expected contract:
        answer=<value>

    Stable outputs repeat a clean contract.
    Unstable outputs mix formats, clauses, fragments, or noise.

    This is a structural contract check only.
    It does not know whether the answer value is semantically correct.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        return 0.0

    valid = 0
    for line in lines:
        if line.startswith("answer=") and len(line.split("=", 1)[1].strip()) > 0:
            valid += 1

    return valid / len(lines)


def structural_signature(text: str) -> Dict[str, float]:
    """
    Produce a minimal deterministic structural signature.

    This is NOT the full OMNIA engine.

    It is a toy structural proxy used only for validation of axis separation.
    """
    entropy = shannon_entropy(text)
    ratio = compression_ratio(text)
    repetition = normalized_repetition_score(text, n=3)
    contract = line_contract_score(text)

    compressibility = max(0.0, min(1.0, 1.0 - ratio))

    omega_proxy = max(
        0.0,
        min(
            1.0,
            (
                0.35 * compressibility
                + 0.35 * repetition
                + 0.30 * contract
            ),
        ),
    )

    return {
        "entropy": round(entropy, 12),
        "compression_ratio": round(ratio, 12),
        "repetition_score": round(repetition, 12),
        "contract_score": round(contract, 12),
        "omega_proxy": round(omega_proxy, 12),
    }


# ---------------------------------------------------------------------
# Toy cases
# ---------------------------------------------------------------------

def build_cases() -> List[Dict[str, Any]]:
    """
    Build four controlled toy cases.

    Semantic labels are manually assigned from the toy question:

        2 + 2 = ?

    Correct answer:
        4

    Structural labels are assigned from output form:
        stable   -> repeated clean contract
        unstable -> broken/mixed/inconsistent form

    The structural metric is not allowed to inspect semantic correctness.
    """
    return [
        {
            "case_id": "correct_structurally_stable",
            "semantic_correct": True,
            "structurally_stable": True,
            "expected_answer": "4",
            "text": "\n".join([
                "answer=4",
                "answer=4",
                "answer=4",
                "answer=4",
                "answer=4",
                "answer=4",
                "answer=4",
                "answer=4",
            ]),
        },
        {
            "case_id": "wrong_structurally_stable",
            "semantic_correct": False,
            "structurally_stable": True,
            "expected_answer": "4",
            "text": "\n".join([
                "answer=5",
                "answer=5",
                "answer=5",
                "answer=5",
                "answer=5",
                "answer=5",
                "answer=5",
                "answer=5",
            ]),
        },
        {
            "case_id": "correct_structurally_unstable",
            "semantic_correct": True,
            "structurally_stable": False,
            "expected_answer": "4",
            "text": "\n".join([
                "answer=4",
                "final: 4",
                "4",
                "the answer is four",
                "2+2 -> 4",
                "value=4",
                "answer = 4 maybe",
                "result four",
            ]),
        },
        {
            "case_id": "wrong_structurally_unstable",
            "semantic_correct": False,
            "structurally_stable": False,
            "expected_answer": "4",
            "text": "\n".join([
                "answer=5",
                "final: 9",
                "three",
                "2+2 -> 7",
                "value=false",
                "maybe 11",
                "answer = dog",
                "result unknown",
            ]),
        },
    ]


# ---------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------

def measure_cases(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    measured = []

    for case in cases:
        signature = structural_signature(case["text"])

        measured.append({
            "case_id": case["case_id"],
            "semantic_correct": case["semantic_correct"],
            "structurally_stable": case["structurally_stable"],
            "expected_answer": case["expected_answer"],
            "signature": signature,
        })

    return measured


def mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def group_scores(measured: List[Dict[str, Any]]) -> Dict[str, Any]:
    stable_scores = [
        item["signature"]["omega_proxy"]
        for item in measured
        if item["structurally_stable"] is True
    ]

    unstable_scores = [
        item["signature"]["omega_proxy"]
        for item in measured
        if item["structurally_stable"] is False
    ]

    semantic_correct_scores = [
        item["signature"]["omega_proxy"]
        for item in measured
        if item["semantic_correct"] is True
    ]

    semantic_wrong_scores = [
        item["signature"]["omega_proxy"]
        for item in measured
        if item["semantic_correct"] is False
    ]

    stable_mean = mean(stable_scores)
    unstable_mean = mean(unstable_scores)
    semantic_correct_mean = mean(semantic_correct_scores)
    semantic_wrong_mean = mean(semantic_wrong_scores)

    return {
        "by_structure": {
            "stable_scores": stable_scores,
            "unstable_scores": unstable_scores,
            "stable_mean": round(stable_mean, 12),
            "unstable_mean": round(unstable_mean, 12),
            "separation": round(stable_mean - unstable_mean, 12),
        },
        "by_semantics": {
            "semantic_correct_scores": semantic_correct_scores,
            "semantic_wrong_scores": semantic_wrong_scores,
            "semantic_correct_mean": round(semantic_correct_mean, 12),
            "semantic_wrong_mean": round(semantic_wrong_mean, 12),
            "separation": round(abs(semantic_correct_mean - semantic_wrong_mean), 12),
        },
    }


def evaluate_axis_separation(groups: Dict[str, Any]) -> Dict[str, Any]:
    """
    PASS condition:
        structural separation > semantic separation

    This means the toy structural metric groups cases more strongly by
    structural stability than by semantic correctness.

    This is the desired result because the metric is structural, not semantic.
    """
    structural_sep = groups["by_structure"]["separation"]
    semantic_sep = groups["by_semantics"]["separation"]

    structure_dominates = structural_sep > semantic_sep

    return {
        "criterion": "structural_separation > semantic_separation",
        "structural_separation": structural_sep,
        "semantic_separation": semantic_sep,
        "structure_dominates": structure_dominates,
    }


def build_result(measured: List[Dict[str, Any]]) -> Dict[str, Any]:
    groups = group_scores(measured)
    axis_check = evaluate_axis_separation(groups)

    status = "PASS" if axis_check["structure_dominates"] else "FAIL"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Minimal controlled experiment showing that semantic correctness "
            "and structural stability are separable axes."
        ),
        "core_boundary": "structural validity != semantic correctness; measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "cases": measured,
        "groups": groups,
        "axis_separation_check": axis_check,
        "status": status,
        "interpretation": (
            "PASS means the toy structural proxy grouped cases more strongly by "
            "structural stability than by semantic correctness. It does not "
            "prove semantic truth and does not validate the full OMNIA engine."
            if status == "PASS"
            else
            "FAIL means the toy structural proxy did not separate structural "
            "stability from semantic correctness under this configuration."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy demonstration.",
            "Semantic labels are manually assigned.",
            "The structural proxy is intentionally minimal.",
            "The result does not prove semantic truth detection.",
            "The result does not generalize across domains.",
            "No adversarial examples are included yet.",
        ],
        "reproduction_command": "python examples/semantic_vs_structural_separation_v0.py",
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
    print("OMNIA-VALIDATION — Semantic vs Structural Separation v0")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Claim level: {result['claim_level']}")
    print()

    print("Case scores:")
    for item in result["cases"]:
        print(
            f"  {item['case_id']:36s} "
            f"semantic_correct={str(item['semantic_correct']):5s} "
            f"structurally_stable={str(item['structurally_stable']):5s} "
            f"omega_proxy={item['signature']['omega_proxy']}"
        )

    print()
    print("Group means:")
    print(
        "  structurally stable mean:   "
        f"{result['groups']['by_structure']['stable_mean']}"
    )
    print(
        "  structurally unstable mean: "
        f"{result['groups']['by_structure']['unstable_mean']}"
    )
    print(
        "  semantic correct mean:      "
        f"{result['groups']['by_semantics']['semantic_correct_mean']}"
    )
    print(
        "  semantic wrong mean:        "
        f"{result['groups']['by_semantics']['semantic_wrong_mean']}"
    )

    print()
    print("Axis separation:")
    print(
        "  structural separation: "
        f"{result['axis_separation_check']['structural_separation']}"
    )
    print(
        "  semantic separation:   "
        f"{result['axis_separation_check']['semantic_separation']}"
    )
    print(
        "  structure dominates:   "
        f"{result['axis_separation_check']['structure_dominates']}"
    )

    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()