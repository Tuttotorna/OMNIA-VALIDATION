#!/usr/bin/env python3
"""Analyze Structural Failure Probe v0 annotated model results.

This script does not call any model.

It analyzes already-collected, manually or externally annotated JSONL rows.

Boundary:
measurement != inference != decision
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_SURFACE = {"PASS", "FAIL"}
ALLOWED_STRUCTURAL = {"GO", "RISK", "STOP"}
ALLOWED_FAILURE_MODES = {
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

BOUNDARY = "measurement != inference != decision"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()

            if not stripped:
                continue

            value = json.loads(stripped)

            if not isinstance(value, dict):
                raise ValueError(f"Line {line_number} is not a JSON object")

            records.append(value)

    return records


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def pct(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def validate_record(record: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []

    required = [
        "model_id",
        "prompt_id",
        "surface_status",
        "structural_status",
        "failure_mode",
    ]

    for key in required:
        if key not in record:
            errors.append(f"row {index}: missing {key}")

    surface_status = record.get("surface_status")
    structural_status = record.get("structural_status")
    failure_mode = record.get("failure_mode")

    if surface_status not in ALLOWED_SURFACE:
        errors.append(f"row {index}: invalid surface_status={surface_status!r}")

    if structural_status not in ALLOWED_STRUCTURAL:
        errors.append(f"row {index}: invalid structural_status={structural_status!r}")

    if failure_mode not in ALLOWED_FAILURE_MODES:
        errors.append(f"row {index}: invalid failure_mode={failure_mode!r}")

    if structural_status == "GO" and failure_mode != "none":
        errors.append(f"row {index}: structural_status GO should use failure_mode none")

    if structural_status in {"RISK", "STOP"} and failure_mode == "none":
        errors.append(f"row {index}: structural_status {structural_status} should include a failure_mode")

    return errors


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(records)

    surface_pass = [r for r in records if r["surface_status"] == "PASS"]
    surface_fail = [r for r in records if r["surface_status"] == "FAIL"]
    structural_go = [r for r in records if r["structural_status"] == "GO"]
    structural_risk = [r for r in records if r["structural_status"] == "RISK"]
    structural_stop = [r for r in records if r["structural_status"] == "STOP"]

    surface_pass_structure_risk = [
        r
        for r in records
        if r["surface_status"] == "PASS" and r["structural_status"] == "RISK"
    ]

    surface_pass_structure_stop = [
        r
        for r in records
        if r["surface_status"] == "PASS" and r["structural_status"] == "STOP"
    ]

    silent_failures = surface_pass_structure_risk + surface_pass_structure_stop

    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_prompt: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for record in records:
        by_model[str(record["model_id"])].append(record)
        by_prompt[str(record["prompt_id"])].append(record)

    model_summary = {}
    for model_id, model_records in sorted(by_model.items()):
        model_total = len(model_records)
        model_surface_pass_structure_risk = [
            r
            for r in model_records
            if r["surface_status"] == "PASS" and r["structural_status"] == "RISK"
        ]
        model_surface_pass_structure_stop = [
            r
            for r in model_records
            if r["surface_status"] == "PASS" and r["structural_status"] == "STOP"
        ]
        model_silent_failures = model_surface_pass_structure_risk + model_surface_pass_structure_stop

        model_summary[model_id] = {
            "records": model_total,
            "surface_pass_rate": pct(
                sum(1 for r in model_records if r["surface_status"] == "PASS"),
                model_total,
            ),
            "structural_go_rate": pct(
                sum(1 for r in model_records if r["structural_status"] == "GO"),
                model_total,
            ),
            "structural_risk_rate": pct(
                sum(1 for r in model_records if r["structural_status"] == "RISK"),
                model_total,
            ),
            "structural_stop_rate": pct(
                sum(1 for r in model_records if r["structural_status"] == "STOP"),
                model_total,
            ),
            "surface_pass_structure_risk_rate": pct(
                len(model_surface_pass_structure_risk),
                model_total,
            ),
            "silent_failure_rate": pct(len(model_silent_failures), model_total),
            "failure_mode_counts": dict(
                sorted(Counter(str(r["failure_mode"]) for r in model_records).items())
            ),
        }

    prompt_summary = {}
    for prompt_id, prompt_records in sorted(by_prompt.items()):
        prompt_total = len(prompt_records)
        prompt_summary[prompt_id] = {
            "records": prompt_total,
            "surface_pass_structure_risk_rate": pct(
                sum(
                    1
                    for r in prompt_records
                    if r["surface_status"] == "PASS"
                    and r["structural_status"] == "RISK"
                ),
                prompt_total,
            ),
            "silent_failure_rate": pct(
                sum(
                    1
                    for r in prompt_records
                    if r["surface_status"] == "PASS"
                    and r["structural_status"] in {"RISK", "STOP"}
                ),
                prompt_total,
            ),
            "failure_mode_counts": dict(
                sorted(Counter(str(r["failure_mode"]) for r in prompt_records).items())
            ),
        }

    return {
        "artifact_type": "structural_failure_probe_v0_report",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "boundary": BOUNDARY,
        "central_distinction": "surface-valid output != structurally stable output",
        "status": "PASS",
        "records": total,
        "metrics": {
            "surface_pass_rate": pct(len(surface_pass), total),
            "surface_fail_rate": pct(len(surface_fail), total),
            "structural_go_rate": pct(len(structural_go), total),
            "structural_risk_rate": pct(len(structural_risk), total),
            "structural_stop_rate": pct(len(structural_stop), total),
            "surface_pass_structure_risk_rate": pct(
                len(surface_pass_structure_risk),
                total,
            ),
            "surface_pass_structure_stop_rate": pct(
                len(surface_pass_structure_stop),
                total,
            ),
            "silent_failure_rate": pct(len(silent_failures), total),
        },
        "failure_mode_counts": dict(
            sorted(Counter(str(r["failure_mode"]) for r in records).items())
        ),
        "model_summary": model_summary,
        "prompt_summary": prompt_summary,
        "non_claims": [
            "semantic truth",
            "final correctness",
            "model ranking finality",
            "safety certification",
            "deployment approval",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze Structural Failure Probe v0 annotated JSONL results."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Annotated model results JSONL.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output report JSON path.",
    )
    args = parser.parse_args()

    records = read_jsonl(args.input)

    errors: list[str] = []
    for index, record in enumerate(records, start=1):
        errors.extend(validate_record(record, index))

    if errors:
        report = {
            "artifact_type": "structural_failure_probe_v0_report",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "boundary": BOUNDARY,
            "status": "FAIL",
            "errors": errors,
        }
        write_json(args.output, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = summarize(records)
    write_json(args.output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
