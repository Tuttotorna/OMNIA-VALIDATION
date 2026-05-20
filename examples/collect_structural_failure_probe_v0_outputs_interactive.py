#!/usr/bin/env python3
"""Interactive collector for Structural Failure Probe v0 model outputs.

This helper edits a JSONL run file one row at a time.

It does not call any model API.
It does not infer truth.
It does not make decisions.

Boundary:
measurement != inference != decision
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
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


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

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

            rows.append(value)

    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def banner(title: str) -> None:
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def small_line() -> None:
    print("-" * 100)


def ask_choice(prompt: str, allowed: set[str], default: str) -> str:
    allowed_upper = {item.upper() for item in allowed}

    while True:
        value = input(f"{prompt} [{default}]: ").strip()

        if not value:
            return default

        value = value.upper()

        if value in allowed_upper:
            return value

        print("Invalid value.")
        print("Allowed values:")

        for item in sorted(allowed_upper):
            print(f"- {item}")


def ask_failure_mode(default: str) -> str:
    while True:
        value = input(f"failure_mode [{default}]: ").strip()

        if not value:
            return default

        if value in FAILURE_MODES:
            return value

        print("Invalid failure_mode.")
        print("Allowed values:")

        for item in sorted(FAILURE_MODES):
            print(f"- {item}")


def read_multiline_until_marker(marker: str = "<<<END>>>") -> str:
    print(f"Paste full model output below. End with a line containing only: {marker}")
    lines: list[str] = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip() == marker:
            break

        lines.append(line)

    return "\n".join(lines).strip()


def first_unfilled_index(rows: list[dict[str, Any]]) -> int | None:
    for index, row in enumerate(rows):
        if not str(row.get("model_raw_output", "")).strip():
            return index

    return None


def print_row_status(rows: list[dict[str, Any]]) -> None:
    total = len(rows)
    filled = sum(1 for row in rows if str(row.get("model_raw_output", "")).strip())
    annotated = sum(
        1
        for row in rows
        if row.get("surface_status") != "UNANNOTATED"
        or row.get("structural_status") != "UNANNOTATED"
    )
    target_cases = sum(
        1
        for row in rows
        if row.get("surface_status") == "PASS" and row.get("structural_status") == "RISK"
    )

    print(f"Rows: {total}")
    print(f"Filled model_raw_output: {filled}/{total}")
    print(f"Annotated rows: {annotated}/{total}")
    print(f"Surface PASS -> Structural RISK cases: {target_cases}")


def show_prompt(row: dict[str, Any], index: int, total: int) -> None:
    banner(f"Prompt {index + 1}/{total} — {row.get('prompt_id', 'UNKNOWN')}")
    print(f"category: {row.get('category', '')}")
    print(f"probe_target: {row.get('probe_target', '')}")
    small_line()
    print(row.get("prompt", ""))
    small_line()
    print(f"current surface_status: {row.get('surface_status', '')}")
    print(f"current structural_status: {row.get('structural_status', '')}")
    print(f"current failure_mode: {row.get('failure_mode', '')}")

    raw = str(row.get("model_raw_output", ""))

    if raw.strip():
        print("\nCurrent model_raw_output excerpt:")
        print(raw[:600] + ("..." if len(raw) > 600 else ""))
    else:
        print("\nCurrent model_raw_output: EMPTY")


def default_failure_mode_for_status(structural_status: str, current: str) -> str:
    if structural_status == "GO":
        return "none"

    if structural_status in {"RISK", "STOP"}:
        if current not in {"none", "unannotated"}:
            return current
        return "false_closure"

    return "unannotated"


def annotate_row(row: dict[str, Any]) -> dict[str, Any]:
    updated = dict(row)
    updated["surface_status"] = ask_choice(
        "surface_status",
        SURFACE_STATUSES,
        str(updated.get("surface_status", "UNANNOTATED")),
    )
    updated["structural_status"] = ask_choice(
        "structural_status",
        STRUCTURAL_STATUSES,
        str(updated.get("structural_status", "UNANNOTATED")),
    )

    structural_status = str(updated["structural_status"])
    current_failure = str(updated.get("failure_mode", "unannotated"))
    default_failure = default_failure_mode_for_status(structural_status, current_failure)

    updated["failure_mode"] = ask_failure_mode(default_failure)

    notes = input("annotation_notes [optional]: ").strip()
    if notes:
        updated["annotation_notes"] = notes

    updated["boundary"] = BOUNDARY

    return updated


def fill_row(row: dict[str, Any]) -> dict[str, Any]:
    updated = dict(row)
    output = read_multiline_until_marker()

    if output:
        updated["model_raw_output"] = output
        updated["output_excerpt"] = output[:500]
    else:
        print("No output pasted. model_raw_output unchanged.")

    annotate_now = input("Annotate this row now? [y/N]: ").strip().lower()

    if annotate_now == "y":
        updated = annotate_row(updated)

    updated["boundary"] = BOUNDARY

    return updated


def validate_with_external_validator(
    validator_path: Path,
    input_path: Path,
    output_path: Path,
) -> int:
    if not validator_path.exists():
        print(f"Validator not found: {validator_path}")
        return 1

    command = [
        sys.executable,
        str(validator_path),
        "--input",
        str(input_path),
        "--output",
        str(output_path),
    ]

    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )

    if completed.stdout.strip():
        print(completed.stdout)

    if completed.stderr.strip():
        print(completed.stderr)

    return completed.returncode


def interactive_loop(
    run_file: Path,
    validator_file: Path,
    report_file: Path,
) -> int:
    rows = read_jsonl(run_file)

    if not rows:
        raise ValueError(f"No rows found in {run_file}")

    index = first_unfilled_index(rows)
    if index is None:
        index = 0

    while True:
        banner("Structural Failure Probe v0 interactive collector")
        print(f"File: {run_file}")
        print(f"Boundary: {BOUNDARY}")
        print("Core distinction: surface-valid output != structurally stable output")
        small_line()
        print_row_status(rows)
        small_line()
        print("Commands:")
        print("  n = next prompt")
        print("  p = previous prompt")
        print("  g = go to prompt number")
        print("  f = fill current prompt")
        print("  a = annotate current prompt only")
        print("  v = validate and write report")
        print("  s = save")
        print("  q = quit")
        small_line()

        show_prompt(rows[index], index, len(rows))

        command = input("\nCommand [f/n/p/g/a/v/s/q]: ").strip().lower() or "f"

        if command == "q":
            write_jsonl(run_file, rows)
            print("Saved before quit.")
            return 0

        if command == "s":
            write_jsonl(run_file, rows)
            print("Saved.")
            continue

        if command == "n":
            index = min(index + 1, len(rows) - 1)
            continue

        if command == "p":
            index = max(index - 1, 0)
            continue

        if command == "g":
            value = input(f"Prompt number 1-{len(rows)}: ").strip()

            if value.isdigit():
                candidate = int(value) - 1

                if 0 <= candidate < len(rows):
                    index = candidate
                else:
                    print("Out of range.")
            else:
                print("Invalid number.")
            continue

        if command == "f":
            rows[index] = fill_row(rows[index])
            write_jsonl(run_file, rows)
            print("Row saved.")

            next_empty = first_unfilled_index(rows)
            if next_empty is not None:
                index = next_empty
            else:
                index = min(index + 1, len(rows) - 1)
            continue

        if command == "a":
            rows[index] = annotate_row(rows[index])
            write_jsonl(run_file, rows)
            print("Annotation saved.")
            continue

        if command == "v":
            write_jsonl(run_file, rows)
            code = validate_with_external_validator(
                validator_file,
                run_file,
                report_file,
            )
            print(f"Validator exit code: {code}")
            continue

        print("Unknown command.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Interactively collect Structural Failure Probe v0 model outputs."
    )
    parser.add_argument(
        "--run-file",
        type=Path,
        default=Path("examples/structural_failure_probe_v0_real_model_outputs_run_001.jsonl"),
    )
    parser.add_argument(
        "--validator",
        type=Path,
        default=Path("examples/validate_structural_failure_probe_v0_model_outputs.py"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("results/structural_failure_probe_v0_real_model_outputs_run_001_validation.json"),
    )
    args = parser.parse_args()

    return interactive_loop(args.run_file, args.validator, args.report)


if __name__ == "__main__":
    raise SystemExit(main())
