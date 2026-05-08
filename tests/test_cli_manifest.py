from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from omnia_validation.hashing import compute_file_sha256


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "omnia_validation.cli", *args],
        text=True,
        capture_output=True,
        check=False,
    )


def _valid_manifest(tmp_path: Path) -> dict:
    artifact = tmp_path / "example.jsonl"
    artifact.write_text('{"ok": true}\n', encoding="utf-8")

    return {
        "experiment": "artifact_hash_manifest_v0",
        "status": "CHECK",
        "created_at_utc": "2026-05-07T00:00:00+00:00",
        "boundary": "measurement != inference != decision",
        "payload": {
            "manifest_version": "v0",
            "manifest_scope": "tmp",
            "artifact_count": 1,
            "hash_algorithm": "sha256",
            "artifacts": [
                {
                    "artifact_path": "example.jsonl",
                    "artifact_role": "source_output",
                    "sha256": compute_file_sha256(artifact),
                    "size_bytes": artifact.stat().st_size,
                    "recorded_by": "test_cli_manifest",
                }
            ],
        },
    }


def test_cli_validate_manifest_passes_for_valid_manifest(tmp_path: Path) -> None:
    manifest = _valid_manifest(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = _run_cli(
        "validate-manifest",
        str(manifest_path),
        "--base-dir",
        str(tmp_path),
        "--verify-hashes",
    )

    assert result.returncode == 0
    assert json.loads(result.stdout) == {
        "status": "PASS",
        "schema": "artifact_manifest",
    }


def test_cli_validate_manifest_fails_for_bad_manifest(tmp_path: Path) -> None:
    manifest = _valid_manifest(tmp_path)
    manifest["payload"]["hash_algorithm"] = "md5"

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = _run_cli("validate-manifest", str(manifest_path))

    assert result.returncode == 1

    payload = json.loads(result.stdout)

    assert payload["status"] == "FAIL"
    assert "payload.hash_algorithm must be: sha256" in payload["errors"]


def test_cli_existing_artifact_hash_manifest_passes() -> None:
    manifest_path = Path("results/artifact_hash_manifest_v0.json")

    if not manifest_path.exists():
        return

    result = _run_cli(
        "validate-manifest",
        str(manifest_path),
        "--verify-hashes",
    )

    assert result.returncode == 0
    assert json.loads(result.stdout) == {
        "status": "PASS",
        "schema": "artifact_manifest",
    }
