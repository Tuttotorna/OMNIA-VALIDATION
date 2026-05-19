#!/usr/bin/env python3
"""
OMNIA-VALIDATION — Validate OMNIA Silent Failure Gate pattern

Purpose
-------
This script validates the minimal OMNIA Silent Failure Gate pattern:

    stable_output    -> Surface PASS -> OMNIA GO
    fragile_output   -> Surface PASS -> OMNIA RISK
    collapsed_output -> Surface FAIL -> OMNIA STOP

The central validation target is:

    fragile_output -> Surface PASS -> OMNIA RISK

This script does not validate semantic truth.
It validates reproducibility of a structural result pattern.

Boundary:

    measurement != inference != decision
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


EXPECTED_PATTERN: Dict[str, Dict[str, str]] = {
    "stable_output": {
        "surface_status": "PASS",
        "omnia_status": "GO",
    },
    "fragile_output": {
        "surface_status": "PASS",
        "omnia_status": "RISK",
    },
    "collapsed_output": {
        "surface_status": "FAIL",
        "omnia_status": "STOP",
    },
}

EXPECTED_BOUNDARY = "measurement != inference != decision"

ARTIFACT_TYPE = "omnia_silent_failure_validation_result"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run_command(cmd: List[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Command failed\n"
            f"command: {' '.join(cmd)}\n"
            f"exit_code: {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    return result


def ensure_omnia_repo(omnia_repo: Path, omnia_url: str) -> None:
    if (omnia_repo / "examples" / "silent_failure_gate_demo.py").exists():
        return

    omnia_repo.parent.mkdir(parents=True, exist_ok=True)

    if omnia_repo.exists():
        raise FileNotFoundError(
            f"OMNIA repo path exists but demo file is missing: {omnia_repo}"
        )

    run_command(["git", "clone", omnia_url, str(omnia_repo)])


def extract_machine_readable_results(stdout: str) -> List[Dict[str, Any]]:
    marker = "Machine-readable results:"

    if marker not in stdout:
        raise ValueError("Could not find machine-readable results marker in demo output.")

    after_marker = stdout.split(marker, 1)[1].strip()

    if not after_marker:
        raise ValueError("Machine-readable result section is empty.")

    json_start = after_marker.find("[")

    if json_start < 0:
        raise ValueError("Could not find JSON array in machine-readable result section.")

    json_text = after_marker[json_start:].strip()

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not parse machine-readable JSON: {exc}") from exc

    if not isinstance(parsed, list):
        raise TypeError("Machine-readable result must be a JSON list.")

    return parsed


def normalize_observed_pattern(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
    observed: Dict[str, Dict[str, str]] = {}

    for item in results:
        label = item.get("label")
        surface_status = item.get("surface_status")
        omnia_status = item.get("omnia_status")

        if not isinstance(label, str):
            raise TypeError(f"Result item missing string label: {item}")

        if not isinstance(surface_status, str):
            raise TypeError(f"Result item missing string surface_status: {item}")

        if not isinstance(omnia_status, str):
            raise TypeError(f"Result item missing string omnia_status: {item}")

        observed[label] = {
            "surface_status": surface_status,
            "omnia_status": omnia_status,
        }

    return observed


def validate_pattern(observed: Dict[str, Dict[str, str]]) -> List[str]:
    failures: List[str] = []

    for label, expected_statuses in EXPECTED_PATTERN.items():
        if label not in observed:
            failures.append(f"Missing expected label: {label}")
            continue

        for key, expected_value in expected_statuses.items():
            observed_value = observed[label].get(key)

            if observed_value != expected_value:
                failures.append(
                    f"{label}.{key}: expected {expected_value}, observed {observed_value}"
                )

    unexpected_labels = sorted(set(observed) - set(EXPECTED_PATTERN))

    for label in unexpected_labels:
        failures.append(f"Unexpected label present: {label}")

    return failures


def validate_boundary(results: List[Dict[str, Any]]) -> List[str]:
    failures: List[str] = []

    for item in results:
        label = item.get("label", "<missing-label>")
        boundary = item.get("boundary")

        if boundary != EXPECTED_BOUNDARY:
            failures.append(
                f"{label}.boundary: expected {EXPECTED_BOUNDARY!r}, observed {boundary!r}"
            )

    return failures


def build_artifact(
    omnia_repo: Path,
    demo_file: Path,
    stdout: str,
    stderr: str,
    results: List[Dict[str, Any]],
    observed_pattern: Dict[str, Dict[str, str]],
    failures: List[str],
) -> Dict[str, Any]:
    source_hash = sha256_file(demo_file)
    stdout_hash = sha256_bytes(stdout.encode("utf-8"))
    raw_results_hash = sha256_bytes(
        json.dumps(results, sort_keys=True, ensure_ascii=False).encode("utf-8")
    )

    status = "PASS" if not failures else "FAIL"

    return {
        "artifact_type": ARTIFACT_TYPE,
        "status": status,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "repo": "OMNIA",
            "repo_path": str(omnia_repo),
            "demo_file": "examples/silent_failure_gate_demo.py",
            "demo_file_sha256": source_hash,
        },
        "validation_target": {
            "central_case": "fragile_output",
            "central_expected_pattern": {
                "surface_status": "PASS",
                "omnia_status": "RISK",
            },
            "expected_pattern": EXPECTED_PATTERN,
            "boundary": EXPECTED_BOUNDARY,
        },
        "observed_pattern": observed_pattern,
        "raw_results": results,
        "failures": failures,
        "hashes": {
            "stdout_sha256": stdout_hash,
            "raw_results_sha256": raw_results_hash,
        },
        "interpretation": {
            "valid_claim": (
                "The OMNIA Silent Failure Gate demo reproduced the expected structural "
                "GO/RISK/STOP pattern."
            ),
            "non_claims": [
                "semantic correctness",
                "factual truth",
                "AI safety",
                "deployment approval",
                "benchmark replacement",
            ],
            "boundary": EXPECTED_BOUNDARY,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the OMNIA Silent Failure Gate minimal pattern."
    )
    parser.add_argument(
        "--omnia-repo",
        default="/content/OMNIA",
        help="Path to local OMNIA repository. If missing, it will be cloned.",
    )
    parser.add_argument(
        "--omnia-url",
        default="https://github.com/Tuttotorna/OMNIA.git",
        help="Public OMNIA repository URL used if --omnia-repo is missing.",
    )
    parser.add_argument(
        "--output",
        default="results/omnia_silent_failure_validation_result.json",
        help="Output JSON validation artifact path.",
    )
    args = parser.parse_args()

    omnia_repo = Path(args.omnia_repo).resolve()
    output_path = Path(args.output).resolve()

    ensure_omnia_repo(omnia_repo, args.omnia_url)

    demo_file = omnia_repo / "examples" / "silent_failure_gate_demo.py"

    if not demo_file.exists():
        raise FileNotFoundError(f"Missing OMNIA demo file: {demo_file}")

    run = run_command(
        [sys.executable, "examples/silent_failure_gate_demo.py"],
        cwd=omnia_repo,
    )

    results = extract_machine_readable_results(run.stdout)
    observed_pattern = normalize_observed_pattern(results)

    failures: List[str] = []
    failures.extend(validate_pattern(observed_pattern))
    failures.extend(validate_boundary(results))

    artifact = build_artifact(
        omnia_repo=omnia_repo,
        demo_file=demo_file,
        stdout=run.stdout,
        stderr=run.stderr,
        results=results,
        observed_pattern=observed_pattern,
        failures=failures,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(artifact, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("=" * 80)
    print("OMNIA Silent Failure Pattern Validation")
    print("=" * 80)
    print(f"Status: {artifact['status']}")
    print(f"Output artifact: {output_path}")
    print()
    print("Observed pattern:")
    print(json.dumps(observed_pattern, indent=2, sort_keys=True))
    print()

    if failures:
        print("Failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Validation passed.")
    print()
    print("Central result:")
    print("fragile_output -> Surface PASS -> OMNIA RISK")
    print()
    print("Boundary:")
    print(EXPECTED_BOUNDARY)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
