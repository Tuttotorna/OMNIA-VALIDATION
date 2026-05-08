from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from omnia_validation.manifest import validate_artifact_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR = REPO_ROOT / "examples" / "build_artifact_hash_manifest_v0.py"
STABLE_TIMESTAMP = "2026-05-07T00:00:00+00:00"


def _run_generator(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GENERATOR), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_build_artifact_hash_manifest_stable_timestamp(tmp_path: Path) -> None:
    source_dir = tmp_path / "source_outputs"
    source_dir.mkdir()

    (source_dir / "a.jsonl").write_text('{"id": 1}\n', encoding="utf-8")
    (source_dir / "b.jsonl").write_text('{"id": 2}\n', encoding="utf-8")

    output_path = tmp_path / "manifest.json"

    result = _run_generator(
        "--source-dir",
        str(source_dir),
        "--output",
        str(output_path),
        "--base-dir",
        str(tmp_path),
        "--stable-timestamp",
    )

    assert result.returncode == 0, result.stderr
    assert output_path.exists()

    manifest = json.loads(output_path.read_text(encoding="utf-8"))

    assert manifest["created_at_utc"] == STABLE_TIMESTAMP
    assert manifest["payload"]["artifact_count"] == 2

    errors = validate_artifact_manifest(
        manifest,
        base_dir=tmp_path,
        verify_hashes=True,
    )

    assert errors == []


def test_build_artifact_hash_manifest_created_at_override(tmp_path: Path) -> None:
    source_dir = tmp_path / "source_outputs"
    source_dir.mkdir()

    (source_dir / "a.jsonl").write_text('{"id": 1}\n', encoding="utf-8")

    output_path = tmp_path / "manifest.json"
    created_at = "2030-01-01T00:00:00+00:00"

    result = _run_generator(
        "--source-dir",
        str(source_dir),
        "--output",
        str(output_path),
        "--base-dir",
        str(tmp_path),
        "--created-at",
        created_at,
    )

    assert result.returncode == 0, result.stderr

    manifest = json.loads(output_path.read_text(encoding="utf-8"))

    assert manifest["created_at_utc"] == created_at
    assert manifest["payload"]["artifact_count"] == 1


def test_build_artifact_hash_manifest_reproducible_with_stable_timestamp(
    tmp_path: Path,
) -> None:
    source_dir = tmp_path / "source_outputs"
    source_dir.mkdir()

    (source_dir / "a.jsonl").write_text('{"id": 1}\n', encoding="utf-8")

    output_path = tmp_path / "manifest.json"

    first = _run_generator(
        "--source-dir",
        str(source_dir),
        "--output",
        str(output_path),
        "--base-dir",
        str(tmp_path),
        "--stable-timestamp",
    )

    assert first.returncode == 0, first.stderr

    first_content = output_path.read_text(encoding="utf-8")

    second = _run_generator(
        "--source-dir",
        str(source_dir),
        "--output",
        str(output_path),
        "--base-dir",
        str(tmp_path),
        "--stable-timestamp",
    )

    assert second.returncode == 0, second.stderr

    second_content = output_path.read_text(encoding="utf-8")

    assert first_content == second_content
