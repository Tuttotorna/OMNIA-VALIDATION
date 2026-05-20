#!/usr/bin/env python3
"""Validate Structural Failure Probe v0 model output JSONL files.

This script validates schema discipline only.

It does not decide semantic truth.

Boundary:
measurement != inference != decision
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BOUNDARY = "measurement != inference != decision"

SURFACE_STATUSES = {"UNANNOTATED", "PASS", "FAIL"}
STRUCTURAL_STATUSES = {"UNANNOTATED", "GO", "RISK", "STOP"}
FAILURE_MODES = {
    "unannotated",
    "none",
    "false_closure",
    "single_side_collapse",
    "contradiction_hidden",
    "user_pleasing_resolution",
    "boundary_violation",
    "semantic_reassurance",
    "over_refusal",
    "ambiguity_not_preserved",
    "unsupported_certainty",
    "observer_privilege",
}

REQUIRED_FIELDS = [
    "run_id",
    "run_date_utc",
    "model_id",
    "provider",
    "interface",
    "prompt_id",
    "category",
    "probe_target",
    "prompt",
    "model_raw_output",
    "surface_status",
    "structural_status",
    "failure_mode",
    "annotation_notes",
    "output_excerpt",
    "boundary",
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()

            if not stripped:
                continue

            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {line_number}: invalid JSON: {exc}") from exc

            if not isinstance(value, dict):
                raise ValueError(f"line {line_number}: row must be a JSON object")

            records.append(value)

    return records


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def validate_record(record: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"row {index}: missing field {field}")

    surface_status = record.get("surface_status")
    structural_status = record.get("structural_status")
    failure_mode = record.get("failure_mode")

    if surface_status not in SURFACE_STATUSES:
        errors.append(f"row {index}: invalid surface_status={surface_status!r}")

    if structural_status not in STRUCTURAL_STATUSES:
        errors.append(f"row {index}: invalid structural_status={structural_status!r}")

    if failure_mode not in FAILURE_MODES:
        errors.append(f"row {index}: invalid failure_mode={failure_mode!r}")

    if record.get("boundary") != BOUNDARY:
        errors.append(f"row {index}: invalid boundary={record.get('boundary')!r}")

    if structural_status == "GO" and failure_mode != "none":
        errors.append(f"row {index}: GO requires failure_mode none")

    if structural_status in {"RISK", "STOP"} and failure_mode in {"none", "unannotated"}:
        errors.append(f"row {index}: RISK/STOP requires concrete failure_mode")

    if structural_status == "UNANNOTATED" and failure_mode != "unannotated":
        errors.append(
            f"row {index}: UNANNOTATED structural_status requires failure_mode unannotated"
        )

    if surface_status == "UNANNOTATED" and structural_status != "UNANNOTATED":
        errors.append(
            f"row {index}: surface UNANNOTATED should keep structural_status UNANNOTATED"
        )

    if not str(record.get("prompt_id", "")).startswith("sfp_v0_"):
        errors.append(f"row {index}: prompt_id must start with sfp_v0_")

    return errors


def summarize(records: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    surface_counts = Counter(str(record.get("surface_status")) for record in records)
    structural_counts = Counter(str(record.get("structural_status")) for record in records)
    failure_counts = Counter(str(record.get("failure_mode")) for record in records)
    model_counts = Counter(str(record.get("model_id")) for record in records)

    surface_pass_structure_risk = sum(
        1
        for record in records
        if record.get("surface_status") == "PASS"
        and record.get("structural_status") == "RISK"
    )

    return {
        "artifact_type": "structural_failure_probe_v0_model_outputs_validation",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "boundary": BOUNDARY,
        "central_distinction": "surface-valid output != structurally stable output",
        "status": "PASS" if not errors else "FAIL",
        "records": len(records),
        "errors": errors,
        "surface_status_counts": dict(sorted(surface_counts.items())),
        "structural_status_counts": dict(sorted(structural_counts.items())),
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "model_counts": dict(sorted(model_counts.items())),
        "surface_pass_structure_risk_count": surface_pass_structure_risk,
        "non_claims": [
            "semantic truth",
            "final model ranking",
            "safety certification",
            "deployment approval",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Structural Failure Probe v0 model output JSONL."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    records = read_jsonl(args.input)

    errors: list[str] = []

    for index, record in enumerate(records, start=1):
        errors.extend(validate_record(record, index))

    report = summarize(records, errors)
    write_json(args.output, report)
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
