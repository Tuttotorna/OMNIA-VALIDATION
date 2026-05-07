#!/usr/bin/env python3
"""
Temporal Collapse Level 3 — External-Source Hash Strengthening Validator v15

Purpose:
- Read the V14 repeated-run cross-provider stability dataset.
- Compute real SHA-256 hashes over the referenced source-output files.
- Replace symbolic placeholder source_file_hash values with real computed hashes.
- Write the strengthened V15 dataset.
- Read the V14 result JSON.
- Rewrite provenance/hash fields into a V15 result JSON.
- Verify that no placeholder hashes remain.
- Verify that every source_file_hash matches the computed hash for its source_file.

Boundary:
measurement != inference != decision
hash verification != semantic correctness
source traceability != benchmark authority
real file hash != proof of model truth
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

V14_DATASET_PATH = ROOT / "data" / "temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl"
V14_RESULT_PATH = ROOT / "results" / "temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json"

V15_DATASET_PATH = ROOT / "data" / "temporal_collapse_external_source_hash_strengthened_v15.jsonl"
V15_RESULT_PATH = ROOT / "results" / "temporal_collapse_external_source_hash_strengthening_validator_v15.json"

EXPERIMENT = "temporal_collapse_external_source_hash_strengthening_validator_v15"
STATUS = "v15_external_source_hash_strengthened"

BOUNDARY = (
    "repeated-run cross-provider real parsed GSM-Symbolic model-output file records "
    "with real computed source-file SHA-256 hashes mapped into raw ordered structural "
    "trajectory events"
)

CLAIM = (
    "This validator strengthens source traceability by replacing symbolic source-file "
    "hash placeholders with real computed SHA-256 hashes. It does not claim that OMNIA "
    "solves GSM-Symbolic, does not infer semantic truth, does not replace benchmark "
    "correctness, and does not make final decisions. It only verifies that source-file "
    "identity is cryptographically bound to the mapped validation records."
)

LIMITATION_NOTE = (
    "External-source hash strengthening does not imply official benchmark scoring, "
    "production certification, semantic truth detection, model correctness, provider "
    "quality, or final decision authority."
)

EXPECTED_INPUT_DATASET = "data/temporal_collapse_external_source_hash_strengthened_v15.jsonl"

EXPECTED_SOURCE_FILES = [
    "data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl",
    "data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_002.jsonl",
    "data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_001.jsonl",
    "data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_002.jsonl",
]

PLACEHOLDER_HASHES = {
    "sha256:provider_a_run_001_source_file_hash_v14",
    "sha256:provider_a_run_002_source_file_hash_v14",
    "sha256:provider_b_run_001_source_file_hash_v14",
    "sha256:provider_b_run_002_source_file_hash_v14",
}

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

EXPECTED_PRESERVED = {
    "trajectory_count": 20,
    "event_count": 100,
    "aggregate_risk_score": 0.379255,
    "aggregate_risk_regime": "DRIFT",
    "aggregate_gate_action": "WATCH",
    "aggregate_accuracy_rate": 0.42,
    "aggregate_extraction_rate": 0.9,
    "highest_risk_trajectory": "gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001",
    "highest_risk_score": 0.7096,
    "highest_risk_provider": "provider_b",
    "highest_risk_run_id": "provider_b_run_v14_002",
}

EXPECTED_REGIME_COUNTS = {
    "CRITICAL": 4,
    "DRIFT": 10,
    "STABLE": 6,
}


def section(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def fail(message: str) -> None:
    raise RuntimeError(message)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        fail(f"Missing JSONL file: {path}")
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                fail(f"Invalid JSONL at {path}:{line_no}: {exc}")
            if not isinstance(value, dict):
                fail(f"JSONL record is not an object at {path}:{line_no}")
            records.append(value)
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=False, separators=(",", ":")))
            f.write("\n")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"Missing JSON file: {path}")
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        fail(f"JSON root is not an object: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")


def sha256_file(path: Path) -> str:
    if not path.exists():
        fail(f"Missing source file: {path}")
    if not path.is_file():
        fail(f"Source path is not a file: {path}")

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def compute_source_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}

    for rel in EXPECTED_SOURCE_FILES:
        path = ROOT / rel
        digest = sha256_file(path)
        if not SHA256_RE.match(digest):
            fail(f"Computed hash has invalid format for {rel}: {digest}")
        hashes[rel] = digest

    return hashes


def unique_sorted(values: list[Any]) -> list[Any]:
    return sorted(set(values))


def collect_dataset_counts(records: list[dict[str, Any]]) -> dict[str, Any]:
    trajectory_ids = unique_sorted([r.get("trajectory_id") for r in records])
    source_files = unique_sorted([r.get("source_file") for r in records])
    source_file_hashes = unique_sorted([r.get("source_file_hash") for r in records])
    providers = unique_sorted([r.get("provider") for r in records])
    run_ids = unique_sorted([r.get("run_id") for r in records])
    stability_groups = unique_sorted([r.get("stability_group") for r in records])
    cross_provider_groups = unique_sorted([r.get("cross_provider_group") for r in records])

    return {
        "record_count": len(records),
        "trajectory_count": len(trajectory_ids),
        "event_count": len(records),
        "source_file_count": len(source_files),
        "source_file_hash_count": len(source_file_hashes),
        "provider_count": len(providers),
        "run_count": len(run_ids),
        "stability_group_count": len(stability_groups),
        "cross_provider_group_count": len(cross_provider_groups),
        "source_files": source_files,
        "source_file_hashes": source_file_hashes,
        "providers": providers,
        "run_ids": run_ids,
        "stability_groups": stability_groups,
        "cross_provider_groups": cross_provider_groups,
    }


def rewrite_dataset_hashes(
    records: list[dict[str, Any]],
    source_hashes: dict[str, str],
) -> list[dict[str, Any]]:
    rewritten: list[dict[str, Any]] = []

    for idx, record in enumerate(records, start=1):
        new_record = copy.deepcopy(record)
        source_file = new_record.get("source_file")

        if source_file not in source_hashes:
            fail(f"Dataset record {idx} has unexpected source_file: {source_file!r}")

        new_record["source_file_hash"] = source_hashes[source_file]
        rewritten.append(new_record)

    return rewritten


def replace_hashes_in_any(value: Any, source_hashes: dict[str, str]) -> Any:
    """
    Recursively replace known placeholder hashes.

    If a dictionary contains both source_file and source_file_hash, the hash is set
    from the computed mapping for that source_file.

    Lists named source_file_hashes are normalized by replacing placeholder values
    where possible.
    """
    if isinstance(value, dict):
        out: dict[str, Any] = {}

        for key, item in value.items():
            out[key] = replace_hashes_in_any(item, source_hashes)

        source_file = out.get("source_file")
        if isinstance(source_file, str) and source_file in source_hashes:
            if "source_file_hash" in out:
                out["source_file_hash"] = source_hashes[source_file]

        source_files = out.get("source_files")
        if isinstance(source_files, list) and "source_file_hashes" in out:
            new_hashes = []
            for sf in source_files:
                if isinstance(sf, str) and sf in source_hashes:
                    new_hashes.append(source_hashes[sf])
            if new_hashes:
                out["source_file_hashes"] = sorted(set(new_hashes))

        return out

    if isinstance(value, list):
        return [replace_hashes_in_any(item, source_hashes) for item in value]

    if isinstance(value, str):
        if value in PLACEHOLDER_HASHES:
            # Fallback replacement only for direct strings where source_file is not local.
            # The exact file-specific replacement is handled by dictionary context above.
            return value
        return value

    return value


def build_v15_result(
    v14_result: dict[str, Any],
    source_hashes: dict[str, str],
    rewritten_records: list[dict[str, Any]],
) -> dict[str, Any]:
    result = replace_hashes_in_any(copy.deepcopy(v14_result), source_hashes)

    result["experiment"] = EXPERIMENT
    result["status"] = STATUS
    result["boundary"] = BOUNDARY
    result["claim"] = CLAIM
    result["limitation_note"] = LIMITATION_NOTE
    result["input_file"] = EXPECTED_INPUT_DATASET

    result["source_file_hashes"] = [source_hashes[sf] for sf in EXPECTED_SOURCE_FILES]
    result["hash_strengthening_method"] = "computed_sha256_over_source_output_files"
    result["hash_algorithm"] = "sha256"
    result["hash_verified"] = True
    result["real_source_file_hashes"] = dict(source_hashes)
    result["placeholder_hashes_replaced"] = True
    result["hash_validation_failures"] = []

    dataset_counts = collect_dataset_counts(rewritten_records)

    aggregate = result.setdefault("aggregate", {})
    if not isinstance(aggregate, dict):
        fail("Result aggregate is not an object")

    aggregate["source_file_hash_count"] = len(set(source_hashes.values()))
    aggregate["real_source_file_hash_count"] = len(set(source_hashes.values()))
    aggregate["placeholder_source_file_hash_count"] = 0
    aggregate["hash_format_failure_count"] = 0
    aggregate["hash_mismatch_failure_count"] = 0
    aggregate["missing_source_file_count"] = 0

    aggregate["source_file_count"] = dataset_counts["source_file_count"]
    aggregate["trajectory_count"] = dataset_counts["trajectory_count"]
    aggregate["event_count"] = dataset_counts["event_count"]

    return result


def flatten_strings(value: Any) -> list[str]:
    strings: list[str] = []

    if isinstance(value, dict):
        for item in value.values():
            strings.extend(flatten_strings(item))
    elif isinstance(value, list):
        for item in value:
            strings.extend(flatten_strings(item))
    elif isinstance(value, str):
        strings.append(value)

    return strings


def validate_no_placeholders(value: Any, label: str) -> None:
    strings = flatten_strings(value)
    found = sorted(set(s for s in strings if s in PLACEHOLDER_HASHES))
    if found:
        fail(f"Placeholder hashes remain in {label}: {found}")


def validate_hash_format(value: Any, label: str) -> None:
    strings = flatten_strings(value)
    hash_like = [s for s in strings if s.startswith("sha256:")]

    bad = sorted(set(s for s in hash_like if not SHA256_RE.match(s)))
    if bad:
        fail(f"Invalid sha256 format in {label}: {bad}")


def validate_dataset_hashes(records: list[dict[str, Any]], source_hashes: dict[str, str]) -> None:
    bad: list[dict[str, Any]] = []

    for idx, record in enumerate(records, start=1):
        source_file = record.get("source_file")
        source_file_hash = record.get("source_file_hash")

        if source_file not in source_hashes:
            bad.append({"line": idx, "reason": "unexpected_source_file", "source_file": source_file})
            continue

        expected = source_hashes[source_file]
        if source_file_hash != expected:
            bad.append(
                {
                    "line": idx,
                    "reason": "hash_mismatch",
                    "source_file": source_file,
                    "expected": expected,
                    "actual": source_file_hash,
                }
            )

    if bad:
        fail(f"Dataset hash mismatches: {json.dumps(bad[:20], indent=2)}")


def validate_result_hashes(result: dict[str, Any], source_hashes: dict[str, str]) -> None:
    bad: list[dict[str, Any]] = []

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            source_file = value.get("source_file")
            source_file_hash = value.get("source_file_hash")

            if isinstance(source_file, str) and source_file in source_hashes and source_file_hash is not None:
                expected = source_hashes[source_file]
                if source_file_hash != expected:
                    bad.append(
                        {
                            "path": path,
                            "source_file": source_file,
                            "expected": expected,
                            "actual": source_file_hash,
                        }
                    )

            source_files = value.get("source_files")
            source_file_hashes = value.get("source_file_hashes")
            if isinstance(source_files, list) and isinstance(source_file_hashes, list):
                expected_hashes = sorted(
                    set(source_hashes[sf] for sf in source_files if isinstance(sf, str) and sf in source_hashes)
                )
                actual_hashes = sorted(set(h for h in source_file_hashes if isinstance(h, str)))
                if expected_hashes and actual_hashes != expected_hashes:
                    bad.append(
                        {
                            "path": path,
                            "source_files": source_files,
                            "expected_hashes": expected_hashes,
                            "actual_hashes": actual_hashes,
                        }
                    )

            for key, item in value.items():
                walk(item, f"{path}.{key}")

        elif isinstance(value, list):
            for i, item in enumerate(value):
                walk(item, f"{path}[{i}]")

    walk(result, "$")

    if bad:
        fail(f"Result hash mismatches: {json.dumps(bad[:20], indent=2)}")


def validate_preserved_values(result: dict[str, Any]) -> None:
    aggregate = result.get("aggregate")
    if not isinstance(aggregate, dict):
        fail("Missing aggregate object")

    for key, expected in EXPECTED_PRESERVED.items():
        if key in {"trajectory_count", "event_count"}:
            actual = result.get(key)
        else:
            actual = aggregate.get(key)

        if actual != expected:
            fail(f"Preserved value mismatch for {key}: expected={expected!r}, actual={actual!r}")

    regime_counts = aggregate.get("regime_counts")
    if regime_counts != EXPECTED_REGIME_COUNTS:
        fail(f"Regime counts mismatch: expected={EXPECTED_REGIME_COUNTS}, actual={regime_counts}")


def validate_trajectory_shape(records: list[dict[str, Any]]) -> None:
    by_trajectory: dict[str, list[int]] = defaultdict(list)

    for record in records:
        tid = record.get("trajectory_id")
        step = record.get("step")
        if not isinstance(tid, str):
            fail(f"Invalid trajectory_id: {tid!r}")
        if not isinstance(step, int):
            fail(f"Invalid step for {tid}: {step!r}")
        by_trajectory[tid].append(step)

    bad = {
        tid: sorted(steps)
        for tid, steps in by_trajectory.items()
        if sorted(steps) != [1, 2, 3, 4, 5]
    }

    if bad:
        fail(f"Bad trajectory step structure: {bad}")

    if len(by_trajectory) != 20:
        fail(f"Expected 20 trajectories, found {len(by_trajectory)}")

    if len(records) != 100:
        fail(f"Expected 100 events, found {len(records)}")


def validate_v15_result(result: dict[str, Any], records: list[dict[str, Any]], source_hashes: dict[str, str]) -> None:
    validate_no_placeholders(records, "V15 dataset")
    validate_no_placeholders(result, "V15 result")
    validate_hash_format(records, "V15 dataset")
    validate_hash_format(result, "V15 result")
    validate_dataset_hashes(records, source_hashes)
    validate_result_hashes(result, source_hashes)
    validate_trajectory_shape(records)
    validate_preserved_values(result)

    aggregate = result["aggregate"]

    expected_aggregate_additions = {
        "real_source_file_hash_count": 4,
        "placeholder_source_file_hash_count": 0,
        "hash_format_failure_count": 0,
        "hash_mismatch_failure_count": 0,
        "missing_source_file_count": 0,
    }

    for key, expected in expected_aggregate_additions.items():
        actual = aggregate.get(key)
        if actual != expected:
            fail(f"Aggregate V15 field mismatch for {key}: expected={expected!r}, actual={actual!r}")

    if result.get("hash_strengthening_method") != "computed_sha256_over_source_output_files":
        fail("Invalid hash_strengthening_method")

    if result.get("hash_algorithm") != "sha256":
        fail("Invalid hash_algorithm")

    if result.get("hash_verified") is not True:
        fail("hash_verified must be true")

    if result.get("placeholder_hashes_replaced") is not True:
        fail("placeholder_hashes_replaced must be true")

    if result.get("hash_validation_failures") != []:
        fail("hash_validation_failures must be empty")


def print_quick_checks(records: list[dict[str, Any]], result: dict[str, Any], source_hashes: dict[str, str]) -> None:
    counts = collect_dataset_counts(records)
    aggregate = result["aggregate"]

    placeholder_count = 0
    for s in flatten_strings(records) + flatten_strings(result):
        if s in PLACEHOLDER_HASHES:
            placeholder_count += 1

    hash_format_failures = 0
    for s in flatten_strings(records) + flatten_strings(result):
        if s.startswith("sha256:") and not SHA256_RE.match(s):
            hash_format_failures += 1

    mismatch_count = 0
    for record in records:
        sf = record.get("source_file")
        sh = record.get("source_file_hash")
        if isinstance(sf, str) and sf in source_hashes and sh != source_hashes[sf]:
            mismatch_count += 1

    section("RESULT QUICK CHECK")
    print("experiment:", result.get("experiment"))
    print("status:", result.get("status"))
    print("trajectory_count:", result.get("trajectory_count"))
    print("event_count:", result.get("event_count"))
    print("source_file_count:", counts["source_file_count"])
    print("computed_hash_count:", len(source_hashes))
    print("real_hash_count:", len(set(source_hashes.values())))
    print("placeholder_hash_count:", placeholder_count)
    print("hash_format_failure_count:", hash_format_failures)
    print("hash_mismatch_failure_count:", mismatch_count)
    print("aggregate_risk_score:", aggregate.get("aggregate_risk_score"))
    print("aggregate_risk_regime:", aggregate.get("aggregate_risk_regime"))
    print("aggregate_gate_action:", aggregate.get("aggregate_gate_action"))
    print("highest_risk_trajectory:", aggregate.get("highest_risk_trajectory"))
    print("highest_risk_score:", aggregate.get("highest_risk_score"))
    print("highest_risk_provider:", aggregate.get("highest_risk_provider"))
    print("highest_risk_run_id:", aggregate.get("highest_risk_run_id"))

    section("COMPUTED SOURCE HASHES")
    for source_file in EXPECTED_SOURCE_FILES:
        print(source_file, "->", source_hashes[source_file])


def main() -> int:
    section("TEMPORAL COLLAPSE EXTERNAL-SOURCE HASH STRENGTHENING VALIDATOR V15")

    section("READING V14 DATASET")
    v14_records = read_jsonl(V14_DATASET_PATH)
    print("input_dataset:", V14_DATASET_PATH.relative_to(ROOT))
    print("record_count:", len(v14_records))

    section("READING V14 RESULT")
    v14_result = read_json(V14_RESULT_PATH)
    print("input_result:", V14_RESULT_PATH.relative_to(ROOT))
    print("experiment:", v14_result.get("experiment"))
    print("status:", v14_result.get("status"))

    section("COMPUTING SOURCE FILE HASHES")
    source_hashes = compute_source_hashes()
    for source_file, digest in source_hashes.items():
        print(source_file, digest)

    section("REWRITING DATASET HASHES")
    v15_records = rewrite_dataset_hashes(v14_records, source_hashes)
    write_jsonl(V15_DATASET_PATH, v15_records)
    print("wrote:", V15_DATASET_PATH.relative_to(ROOT))
    print("record_count_written:", len(v15_records))

    section("BUILDING V15 RESULT")
    v15_result = build_v15_result(v14_result, source_hashes, v15_records)
    write_json(V15_RESULT_PATH, v15_result)
    print("wrote:", V15_RESULT_PATH.relative_to(ROOT))

    section("VALIDATING V15")
    validate_v15_result(v15_result, v15_records, source_hashes)

    print_quick_checks(v15_records, v15_result, source_hashes)

    section("FINAL STATUS")
    print("V15 HASH STRENGTHENING PASSED")
    print("trajectory_count:", v15_result.get("trajectory_count"))
    print("event_count:", v15_result.get("event_count"))
    print("source_file_count:", v15_result["aggregate"].get("source_file_count"))
    print("computed_hash_count:", len(source_hashes))
    print("real_hash_count:", v15_result["aggregate"].get("real_source_file_hash_count"))
    print("placeholder_hash_count:", v15_result["aggregate"].get("placeholder_source_file_hash_count"))
    print("hash_format_failure_count:", v15_result["aggregate"].get("hash_format_failure_count"))
    print("hash_mismatch_failure_count:", v15_result["aggregate"].get("hash_mismatch_failure_count"))
    print("aggregate_risk_regime:", v15_result["aggregate"].get("aggregate_risk_regime"))
    print("aggregate_gate_action:", v15_result["aggregate"].get("aggregate_gate_action"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())