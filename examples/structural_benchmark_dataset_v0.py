#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Structural Benchmark Dataset v0

Purpose:
    Generate the first minimal OMNIA-native structural benchmark dataset.

This script creates:

    data/structural_benchmark_dataset_v0.jsonl
    results/structural_benchmark_dataset_v0_summary.json

The dataset contains paired structural cases for:

    STRUCTURAL_EQUIVALENT
    STRUCTURAL_NEAR_EQUIVALENT
    STRUCTURAL_DIFFERENT
    FALSE_MERGE_TRAP
    FALSE_SPLIT_TRAP
    PARTIAL_DRIFT

Core boundary:
    measurement != inference != decision

Claim level:
    Level 1 — Dataset Seed

Important:
    This dataset does not validate OMNIA by itself.
    It provides a reproducible test space for future measurement experiments.
"""

from __future__ import annotations

import json
import math
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


EXPERIMENT_NAME = "structural_benchmark_dataset_v0"
DOMAIN = "omnia_native_structural_benchmark_seed"
VERSION = "0.1.0"

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"

DATASET_PATH = DATA_DIR / "structural_benchmark_dataset_v0.jsonl"
SUMMARY_PATH = RESULTS_DIR / "structural_benchmark_dataset_v0_summary.json"


PAIR_TYPES = [
    "STRUCTURAL_EQUIVALENT",
    "STRUCTURAL_NEAR_EQUIVALENT",
    "STRUCTURAL_DIFFERENT",
    "FALSE_MERGE_TRAP",
    "FALSE_SPLIT_TRAP",
    "PARTIAL_DRIFT",
]


FAMILIES = [
    "binary_alternation",
    "four_cycle",
    "triple_cycle",
    "nested_blocks",
    "run_length_gradient",
    "mirror_sequence",
]


# ---------------------------------------------------------------------
# Small structural helpers
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


def compact(tokens: List[str]) -> str:
    return "".join(tokens)


def json_like(tokens: List[str], field: str = "v", meta: str | None = None) -> str:
    objects = []

    for token in tokens:
        if meta is None:
            objects.append(f'{{"{field}":"{token}"}}')
        else:
            objects.append(f'{{"meta":"{meta}","{field}":"{token}"}}')

    return ",".join(objects)


def words(tokens: List[str]) -> str:
    mapping = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "A": "alpha",
        "B": "beta",
        "C": "gamma",
        "D": "delta",
        "X": "xray",
        "Y": "yankee",
        "Z": "zulu",
    }

    return "|".join(mapping.get(token, token) for token in tokens)


def alias_tokens(tokens: List[str], aliases_per_symbol: int = 3) -> List[str]:
    counters: Dict[str, int] = {}
    out = []

    for token in tokens:
        idx = counters.get(token, 0)
        counters[token] = idx + 1

        alias_id = idx % aliases_per_symbol
        out.append(f"{token}_{alias_id}")

    return out


def local_swaps(tokens: List[str], stride: int = 17) -> List[str]:
    out = list(tokens)

    for i in range(stride, len(out) - 1, stride):
        out[i], out[i + 1] = out[i + 1], out[i]

    return out


def sparse_unknown_injection(tokens: List[str], stride: int = 19) -> List[str]:
    out = list(tokens)

    for i in range(stride, len(out), stride):
        out[i] = f"UNK{i}"

    return out


def delete_sparse(tokens: List[str], stride: int = 23) -> List[str]:
    return [
        token
        for i, token in enumerate(tokens)
        if i % stride != 0
    ]


def rotate_symbols(tokens: List[str], mapping: Dict[str, str]) -> List[str]:
    return [mapping.get(token, token) for token in tokens]


def mirror(tokens: List[str]) -> List[str]:
    return list(tokens) + list(reversed(tokens))


# ---------------------------------------------------------------------
# Structural family generators
# ---------------------------------------------------------------------

def family_binary_alternation(length: int = 64) -> List[str]:
    return repeat(["0", "1"], length // 2)


def family_four_cycle(length: int = 64) -> List[str]:
    return repeat(["0", "1", "2", "3"], length // 4)


def family_triple_cycle(length: int = 63) -> List[str]:
    return repeat(["0", "1", "2"], length // 3)


def family_nested_blocks() -> List[str]:
    return repeat(["A", "A", "B", "B", "C", "C", "B", "B"], 8)


def family_run_length_gradient() -> List[str]:
    out: List[str] = []

    for run_length in range(1, 9):
        out.extend(["A"] * run_length)
        out.extend(["B"] * run_length)

    return out


def family_mirror_sequence() -> List[str]:
    seed = ["A", "B", "C", "D", "C", "B"]
    return mirror(repeat(seed, 5))


def family_tokens(family: str) -> List[str]:
    if family == "binary_alternation":
        return family_binary_alternation()

    if family == "four_cycle":
        return family_four_cycle()

    if family == "triple_cycle":
        return family_triple_cycle()

    if family == "nested_blocks":
        return family_nested_blocks()

    if family == "run_length_gradient":
        return family_run_length_gradient()

    if family == "mirror_sequence":
        return family_mirror_sequence()

    raise ValueError(f"Unknown family: {family}")


# ---------------------------------------------------------------------
# Baseline toy signatures for dataset summary only
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


def unique_symbol_ratio(text: str) -> float:
    if not text:
        return 0.0

    return len(set(text)) / len(text)


def simple_signature(text: str) -> Dict[str, float]:
    return {
        "length": float(len(text)),
        "entropy": round(shannon_entropy(text), 12),
        "compression_ratio": round(compression_ratio(text), 12),
        "unique_symbol_ratio": round(unique_symbol_ratio(text), 12),
    }


# ---------------------------------------------------------------------
# Record builders
# ---------------------------------------------------------------------

def make_record(
    case_id: str,
    family: str,
    pair_type: str,
    expected_relation: str,
    left_text: str,
    right_text: str,
    generator: str,
    attack_family: str | None = None,
    noise_level: int = 0,
    notes: str = "",
) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "version": VERSION,
        "family": family,
        "pair_type": pair_type,
        "expected_relation": expected_relation,
        "left_text": left_text,
        "right_text": right_text,
        "metadata": {
            "generator": generator,
            "attack_family": attack_family,
            "noise_level": noise_level,
            "notes": notes,
        },
        "reference": {
            "core_boundary": "measurement != inference != decision",
            "claim_level": "Level 1 — Dataset Seed",
            "semantic_truth_evaluated": False,
        },
    }


def build_structural_equivalent_records() -> List[Dict[str, Any]]:
    records = []

    for idx, family in enumerate(FAMILIES, start=1):
        tokens = family_tokens(family)

        left = pipe(tokens)
        right = spaced(rotate_symbols(
            tokens,
            {
                "0": "A",
                "1": "B",
                "2": "C",
                "3": "D",
                "A": "X",
                "B": "Y",
                "C": "Z",
                "D": "W",
            },
        ))

        records.append(make_record(
            case_id=f"eq_{idx:03d}_{family}",
            family=family,
            pair_type="STRUCTURAL_EQUIVALENT",
            expected_relation="same_structure_different_representation",
            left_text=left,
            right_text=right,
            generator="equivalent_symbol_renaming",
            attack_family=None,
            noise_level=0,
            notes="Different surface symbols preserve the same structural sequence.",
        ))

    return records


def build_structural_near_equivalent_records() -> List[Dict[str, Any]]:
    records = []

    for idx, family in enumerate(FAMILIES, start=1):
        tokens = family_tokens(family)

        left = pipe(tokens)
        perturbed = sparse_unknown_injection(tokens, stride=19)

        records.append(make_record(
            case_id=f"near_{idx:03d}_{family}",
            family=family,
            pair_type="STRUCTURAL_NEAR_EQUIVALENT",
            expected_relation="same_base_structure_with_sparse_noise",
            left_text=left,
            right_text=pipe(perturbed),
            generator="sparse_unknown_injection",
            attack_family="SPARSE_UNKNOWN_INJECTION",
            noise_level=1,
            notes="Sparse deterministic unknown tokens should create mild degradation.",
        ))

    return records


def build_structural_different_records() -> List[Dict[str, Any]]:
    pairs = [
        ("binary_alternation", "four_cycle"),
        ("binary_alternation", "nested_blocks"),
        ("four_cycle", "run_length_gradient"),
        ("triple_cycle", "mirror_sequence"),
        ("nested_blocks", "mirror_sequence"),
        ("run_length_gradient", "binary_alternation"),
    ]

    records = []

    for idx, (left_family, right_family) in enumerate(pairs, start=1):
        left_tokens = family_tokens(left_family)
        right_tokens = family_tokens(right_family)

        records.append(make_record(
            case_id=f"diff_{idx:03d}_{left_family}_vs_{right_family}",
            family=f"{left_family}_vs_{right_family}",
            pair_type="STRUCTURAL_DIFFERENT",
            expected_relation="different_structure",
            left_text=pipe(left_tokens),
            right_text=pipe(right_tokens),
            generator="cross_family_pairing",
            attack_family=None,
            noise_level=0,
            notes="Different structural families should remain separated.",
        ))

    return records


def build_false_merge_trap_records() -> List[Dict[str, Any]]:
    records = []

    # Same formal alternation, different intended domain.
    records.append(make_record(
        case_id="fm_001_temperature_vs_finance",
        family="binary_alternation_domain_collision",
        pair_type="FALSE_MERGE_TRAP",
        expected_relation="different_intent_same_projection_pattern",
        left_text=pipe(repeat(["hot", "cold"], 32)),
        right_text=pipe(repeat(["buy", "sell"], 32)),
        generator="many_to_one_domain_collision",
        attack_family="MANY_TO_ONE_COLLAPSE",
        noise_level=0,
        notes="First-seen projection collapses both into 0101 despite different intended domains.",
    ))

    records.append(make_record(
        case_id="fm_002_periodicity_spoofing",
        family="periodicity_collision",
        pair_type="FALSE_MERGE_TRAP",
        expected_relation="different_intent_same_periodicity",
        left_text=spaced(repeat(["0", "1"], 32)),
        right_text=spaced(repeat(["open", "close"], 32)),
        generator="periodicity_spoofing",
        attack_family="PERIODICITY_SPOOFING",
        noise_level=0,
        notes="Different intent shares the same period.",
    ))

    records.append(make_record(
        case_id="fm_003_json_field_erasure",
        family="metadata_erasure_collision",
        pair_type="FALSE_MERGE_TRAP",
        expected_relation="different_metadata_same_value_sequence",
        left_text=json_like(repeat(["0", "1"], 32), field="v", meta="sensor_A"),
        right_text=json_like(repeat(["0", "1"], 32), field="v", meta="sensor_B"),
        generator="json_metadata_collision",
        attack_family="JSON_FIELD_ERASURE",
        noise_level=0,
        notes="Projection that ignores metadata can merge distinct sources.",
    ))

    records.append(make_record(
        case_id="fm_004_low_high_vs_zero_extreme",
        family="magnitude_semantics_collision",
        pair_type="FALSE_MERGE_TRAP",
        expected_relation="different_magnitude_intent_same_alternation",
        left_text=spaced(repeat(["low", "high"], 32)),
        right_text=spaced(repeat(["zero", "extreme"], 32)),
        generator="semantic_magnitude_collision",
        attack_family="MANY_TO_ONE_COLLAPSE",
        noise_level=0,
        notes="Structure alone cannot recover magnitude semantics.",
    ))

    return records


def build_false_split_trap_records() -> List[Dict[str, Any]]:
    records = []

    binary = family_tokens("binary_alternation")
    four = family_tokens("four_cycle")
    nested = family_tokens("nested_blocks")

    records.append(make_record(
        case_id="fs_001_alias_inflation_binary",
        family="binary_alternation",
        pair_type="FALSE_SPLIT_TRAP",
        expected_relation="same_structure_alias_inflated",
        left_text=pipe(binary),
        right_text=pipe(alias_tokens(binary, aliases_per_symbol=3)),
        generator="alias_inflation",
        attack_family="ALIAS_INFLATION",
        noise_level=2,
        notes="Same binary structure appears as higher-cardinality state space.",
    ))

    records.append(make_record(
        case_id="fs_002_cardinality_inflation_cycle",
        family="four_cycle",
        pair_type="FALSE_SPLIT_TRAP",
        expected_relation="same_structure_cardinality_inflated",
        left_text=pipe(four),
        right_text=pipe(alias_tokens(four, aliases_per_symbol=2)),
        generator="cardinality_inflation",
        attack_family="CARDINALITY_INFLATION",
        noise_level=2,
        notes="Same four-cycle becomes eight symbolic aliases.",
    ))

    records.append(make_record(
        case_id="fs_003_separator_attack",
        family="word_pair_alternation",
        pair_type="FALSE_SPLIT_TRAP",
        expected_relation="same_structure_token_boundary_removed",
        left_text=pipe(repeat(["ab", "cd"], 32)),
        right_text=compact(repeat(["ab", "cd"], 32)),
        generator="separator_attack",
        attack_family="SEPARATOR_ATTACK",
        noise_level=1,
        notes="Removing separators changes tokenization topology.",
    ))

    records.append(make_record(
        case_id="fs_004_nested_alias_split",
        family="nested_blocks",
        pair_type="FALSE_SPLIT_TRAP",
        expected_relation="same_nested_structure_alias_inflated",
        left_text=pipe(nested),
        right_text=pipe(alias_tokens(nested, aliases_per_symbol=2)),
        generator="nested_alias_inflation",
        attack_family="ALIAS_INFLATION",
        noise_level=2,
        notes="Nested structure is preserved conceptually but split by aliases.",
    ))

    return records


def build_partial_drift_records() -> List[Dict[str, Any]]:
    records = []

    for idx, family in enumerate(FAMILIES, start=1):
        tokens = family_tokens(family)

        drifted = local_swaps(tokens, stride=17)
        drifted = delete_sparse(drifted, stride=29)

        records.append(make_record(
            case_id=f"drift_{idx:03d}_{family}",
            family=family,
            pair_type="PARTIAL_DRIFT",
            expected_relation="same_family_local_order_drift",
            left_text=pipe(tokens),
            right_text=pipe(drifted),
            generator="local_swap_plus_sparse_delete",
            attack_family="LOCAL_SWAP_DRIFT",
            noise_level=2,
            notes="Local swaps and sparse deletion produce partial structural drift.",
        ))

    return records


def build_dataset() -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    records.extend(build_structural_equivalent_records())
    records.extend(build_structural_near_equivalent_records())
    records.extend(build_structural_different_records())
    records.extend(build_false_merge_trap_records())
    records.extend(build_false_split_trap_records())
    records.extend(build_partial_drift_records())

    return records


# ---------------------------------------------------------------------
# Dataset validation and summary
# ---------------------------------------------------------------------

def validate_record(record: Dict[str, Any]) -> List[str]:
    errors = []

    required_top = [
        "case_id",
        "version",
        "family",
        "pair_type",
        "expected_relation",
        "left_text",
        "right_text",
        "metadata",
        "reference",
    ]

    for key in required_top:
        if key not in record:
            errors.append(f"missing_top_key:{key}")

    if record.get("pair_type") not in PAIR_TYPES:
        errors.append("invalid_pair_type")

    if not isinstance(record.get("left_text"), str) or not record.get("left_text"):
        errors.append("invalid_left_text")

    if not isinstance(record.get("right_text"), str) or not record.get("right_text"):
        errors.append("invalid_right_text")

    metadata = record.get("metadata", {})
    if not isinstance(metadata, dict):
        errors.append("invalid_metadata")
    else:
        for key in ["generator", "attack_family", "noise_level", "notes"]:
            if key not in metadata:
                errors.append(f"missing_metadata_key:{key}")

    return errors


def summarize_dataset(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    pair_type_counts = Counter(record["pair_type"] for record in records)
    family_counts = Counter(record["family"] for record in records)

    attack_counts = Counter(
        record["metadata"]["attack_family"]
        for record in records
        if record["metadata"]["attack_family"] is not None
    )

    noise_counts = Counter(
        str(record["metadata"]["noise_level"])
        for record in records
    )

    validation_errors = {
        record["case_id"]: validate_record(record)
        for record in records
    }

    invalid_records = {
        case_id: errors
        for case_id, errors in validation_errors.items()
        if errors
    }

    left_signatures = [
        simple_signature(record["left_text"])
        for record in records
    ]

    right_signatures = [
        simple_signature(record["right_text"])
        for record in records
    ]

    avg_left_length = (
        sum(sig["length"] for sig in left_signatures) / len(left_signatures)
        if left_signatures
        else 0.0
    )

    avg_right_length = (
        sum(sig["length"] for sig in right_signatures) / len(right_signatures)
        if right_signatures
        else 0.0
    )

    return {
        "experiment_name": EXPERIMENT_NAME,
        "version": VERSION,
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "domain": DOMAIN,
        "purpose": "Generate a minimal OMNIA-native structural benchmark dataset.",
        "core_boundary": "measurement != inference != decision",
        "claim_level": "Level 1 — Dataset Seed",
        "dataset_path": str(DATASET_PATH.relative_to(ROOT)),
        "record_count": len(records),
        "pair_type_counts": dict(sorted(pair_type_counts.items())),
        "family_count": len(family_counts),
        "family_counts": dict(sorted(family_counts.items())),
        "attack_family_counts": dict(sorted(attack_counts.items())),
        "noise_level_counts": dict(sorted(noise_counts.items())),
        "avg_left_text_length": round(avg_left_length, 6),
        "avg_right_text_length": round(avg_right_length, 6),
        "validation": {
            "valid": len(invalid_records) == 0,
            "invalid_record_count": len(invalid_records),
            "invalid_records": invalid_records,
        },
        "limitations": [
            "This is not the full OMNIA engine.",
            "This is a synthetic benchmark seed.",
            "Expected relations are manually assigned.",
            "No semantic truth is evaluated.",
            "No external reproduction is included yet.",
            "The dataset is small by design.",
        ],
    }


def write_jsonl(path: Path, records: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    records = build_dataset()
    summary = summarize_dataset(records)

    write_jsonl(DATASET_PATH, records)

    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("OMNIA-VALIDATION — Structural Benchmark Dataset v0")
    print("=" * 80)
    print(f"Status: {'PASS' if summary['validation']['valid'] else 'FAIL'}")
    print(f"Claim level: {summary['claim_level']}")
    print(f"Dataset path: {summary['dataset_path']}")
    print(f"Summary path: {SUMMARY_PATH.relative_to(ROOT)}")
    print()

    print("Record count:")
    print(f"  {summary['record_count']}")

    print()
    print("Pair type counts:")
    for pair_type, count in summary["pair_type_counts"].items():
        print(f"  {pair_type:28s} {count}")

    print()
    print("Attack family counts:")
    for attack_family, count in summary["attack_family_counts"].items():
        print(f"  {attack_family:28s} {count}")

    print()
    print("Noise level counts:")
    for noise_level, count in summary["noise_level_counts"].items():
        print(f"  {noise_level:28s} {count}")

    print()
    print("Validation:")
    print(f"  valid:                {summary['validation']['valid']}")
    print(f"  invalid_record_count: {summary['validation']['invalid_record_count']}")

    if summary["validation"]["invalid_records"]:
        print()
        print("Invalid records:")
        for case_id, errors in summary["validation"]["invalid_records"].items():
            print(f"  {case_id}: {errors}")

    print()
    print(f"Dataset saved to: {DATASET_PATH}")
    print(f"Summary saved to: {SUMMARY_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()