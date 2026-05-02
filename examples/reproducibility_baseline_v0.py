#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Reproducibility Baseline v0

Purpose:
    Minimal deterministic reproducibility test for structural measurement.

This experiment does NOT prove OMNIA correct.

It tests only whether a simple structural measurement pipeline produces
stable results across repeated runs under fixed conditions.

Core boundary:
    measurement != inference != decision

Expected behavior:
    - same input
    - same transformation
    - same metric
    - repeated runs
    -> identical results

If repeated runs produce different results, the baseline fails.
"""

from __future__ import annotations

import json
import math
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any


EXPERIMENT_NAME = "reproducibility_baseline_v0"
DOMAIN = "minimal_structural_measurement"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_PATH = RESULTS_DIR / "reproducibility_baseline_v0.json"


# ---------------------------------------------------------------------
# Minimal structural metrics
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
    Higher values usually indicate less compressible / more random structure.
    """
    if not text:
        return 0.0

    raw = text.encode("utf-8")
    compressed = zlib.compress(raw, level=9)

    return len(compressed) / len(raw)


def normalized_repetition_score(text: str, n: int = 3) -> float:
    """
    Measure repeated n-gram structure.

    Returns a value in [0, 1] when possible:
        0 -> no repeated n-grams
        1 -> strong repetition dominance
    """
    if len(text) < n:
        return 0.0

    grams = [text[i:i + n] for i in range(len(text) - n + 1)]
    counts = Counter(grams)

    repeated = sum(count - 1 for count in counts.values() if count > 1)
    possible = max(len(grams) - 1, 1)

    return repeated / possible


def structural_signature(text: str) -> Dict[str, float]:
    """
    Produce a minimal deterministic structural signature.

    This is NOT the full OMNIA engine.

    It is a small validation baseline used only to test reproducibility.
    """
    entropy = shannon_entropy(text)
    ratio = compression_ratio(text)
    repetition = normalized_repetition_score(text, n=3)

    # Minimal bounded structural proxy.
    # Higher score means more repeated/compressible structure.
    compressibility = max(0.0, min(1.0, 1.0 - ratio))
    omega_proxy = max(0.0, min(1.0, (compressibility + repetition) / 2.0))

    return {
        "entropy": round(entropy, 12),
        "compression_ratio": round(ratio, 12),
        "repetition_score": round(repetition, 12),
        "omega_proxy": round(omega_proxy, 12),
    }


# ---------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------

def run_single_pass() -> Dict[str, Any]:
    """
    Run one deterministic measurement pass.
    """
    samples = {
        "structured": (
            "ABCDABCDABCDABCDABCDABCDABCDABCD"
            "ABCDABCDABCDABCDABCDABCDABCDABCD"
        ),
        "mildly_perturbed": (
            "ABCDABCDABCDABCDABCDXBCDABCDABCD"
            "ABCDABCDABCDABCDABCDABCDYBCDABCD"
        ),
        "random_like": (
            "Q7mZp1LxR9vT2nK8sB5cH0uD4eW6yA3"
            "jF2pN9qR7xL1vC8mZ5tB0sK4hD6wY3"
        ),
    }

    signatures = {
        name: structural_signature(text)
        for name, text in samples.items()
    }

    return signatures


def compare_runs(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare repeated runs for exact equality.
    """
    if not runs:
        return {
            "stable": False,
            "reason": "no runs executed",
        }

    reference = runs[0]
    mismatches = []

    for index, current in enumerate(runs[1:], start=1):
        if current != reference:
            mismatches.append({
                "run_index": index,
                "reference": reference,
                "current": current,
            })

    return {
        "stable": len(mismatches) == 0,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
    }


def evaluate_structural_order(reference_run: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check a weak expected ordering.

    This is not a universal claim.

    Expected for this toy dataset:
        structured omega_proxy >= mildly_perturbed omega_proxy >= random_like omega_proxy
    """
    structured = reference_run["structured"]["omega_proxy"]
    mildly = reference_run["mildly_perturbed"]["omega_proxy"]
    random_like = reference_run["random_like"]["omega_proxy"]

    order_holds = structured >= mildly >= random_like

    return {
        "expected_order": "structured >= mildly_perturbed >= random_like",
        "observed_values": {
            "structured": structured,
            "mildly_perturbed": mildly,
            "random_like": random_like,
        },
        "order_holds": order_holds,
    }


def build_result(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build final experiment result.
    """
    reproducibility = compare_runs(runs)
    ordering = evaluate_structural_order(runs[0]) if runs else {
        "order_holds": False,
        "reason": "no runs executed",
    }

    pass_condition = (
        reproducibility.get("stable") is True
        and ordering.get("order_holds") is True
    )

    status = "PASS" if pass_condition else "FAIL"

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": (
            "Minimal deterministic reproducibility test for structural measurement."
        ),
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Toy Demonstration",
        "runs_executed": len(runs),
        "metrics": [
            "entropy",
            "compression_ratio",
            "repetition_score",
            "omega_proxy",
        ],
        "reproducibility": reproducibility,
        "structural_ordering": ordering,
        "status": status,
        "interpretation": (
            "PASS means the toy measurement pipeline is deterministic and the "
            "expected toy structural ordering holds. It does not prove OMNIA "
            "correct and does not validate semantic truth."
            if status == "PASS"
            else
            "FAIL means either repeated runs were not stable or the expected "
            "toy structural ordering did not hold."
        ),
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a toy baseline.",
            "The omega_proxy is only a minimal structural proxy.",
            "No semantic correctness is evaluated.",
            "No universal claim is made.",
        ],
        "reproduction_command": "python examples/reproducibility_baseline_v0.py",
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    run_count = 10
    runs = [run_single_pass() for _ in range(run_count)]

    result = build_result(runs)

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("OMNIA-VALIDATION — Reproducibility Baseline v0")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Runs executed: {result['runs_executed']}")
    print(f"Reproducible: {result['reproducibility']['stable']}")
    print()
    print("Observed omega_proxy values:")
    for key, value in result["structural_ordering"]["observed_values"].items():
        print(f"  {key:18s} -> {value}")
    print()
    print(f"Expected order: {result['structural_ordering']['expected_order']}")
    print(f"Order holds: {result['structural_ordering']['order_holds']}")
    print()
    print(f"Result saved to: {RESULTS_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()