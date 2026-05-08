from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "omnia_validation.cli", *args],
        text=True,
        capture_output=True,
        check=False,
    )


def _result(payload: dict | None = None) -> dict:
    return {
        "experiment": "example_result_v0",
        "status": "CHECK",
        "created_at_utc": "2026-05-07T00:00:00+00:00",
        "boundary": "measurement != inference != decision",
        "payload": payload or {"value": 1},
    }


def test_cli_compare_results_no_regression(tmp_path: Path) -> None:
    previous = tmp_path / "previous.json"
    current = tmp_path / "current.json"

    previous.write_text(json.dumps(_result()), encoding="utf-8")
    current.write_text(json.dumps(_result()), encoding="utf-8")

    result = _run_cli(
        "compare-results",
        "--previous",
        str(previous),
        "--current",
        str(current),
    )

    assert result.returncode == 0

    payload = json.loads(result.stdout)

    assert payload["status"] == "PASS"
    assert payload["schema"] == "result_regression_comparison"
    assert payload["classification"] == "NO_REGRESSION"


def test_cli_compare_results_payload_regression(tmp_path: Path) -> None:
    previous = tmp_path / "previous.json"
    current = tmp_path / "current.json"

    previous.write_text(json.dumps(_result({"value": 1})), encoding="utf-8")
    current.write_text(json.dumps(_result({"value": 2})), encoding="utf-8")

    result = _run_cli(
        "compare-results",
        "--previous",
        str(previous),
        "--current",
        str(current),
    )

    assert result.returncode == 1

    payload = json.loads(result.stdout)

    assert payload["status"] == "FAIL"
    assert payload["schema"] == "result_regression_comparison"
    assert payload["classification"] == "PAYLOAD_REGRESSION"


def test_cli_compare_results_missing_file(tmp_path: Path) -> None:
    existing = tmp_path / "existing.json"
    missing = tmp_path / "missing.json"

    existing.write_text(json.dumps(_result()), encoding="utf-8")

    result = _run_cli(
        "compare-results",
        "--previous",
        str(existing),
        "--current",
        str(missing),
    )

    assert result.returncode == 1

    payload = json.loads(result.stdout)

    assert payload["status"] == "FAIL"
    assert payload["schema"] == "result_regression_comparison"
    assert payload["classification"] == "SCHEMA_REGRESSION"
    assert payload["errors"]


def test_cli_existing_artifact_hash_manifest_compare_passes() -> None:
    result_path = Path("results/artifact_hash_manifest_v0.json")

    if not result_path.exists():
        return

    result = _run_cli(
        "compare-results",
        "--previous",
        str(result_path),
        "--current",
        str(result_path),
    )

    assert result.returncode == 0

    payload = json.loads(result.stdout)

    assert payload["status"] == "PASS"
    assert payload["schema"] == "result_regression_comparison"
    assert payload["classification"] == "NO_REGRESSION"

