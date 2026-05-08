from __future__ import annotations

import json
from pathlib import Path

import pytest

from omnia_validation.hashing import compute_file_sha256
from omnia_validation.manifest import (
    VALID_ARTIFACT_ROLES,
    is_valid_artifact_manifest,
    require_valid_artifact_manifest,
    validate_artifact_entry,
    validate_artifact_manifest,
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
            "manifest_scope": "data/source_outputs",
            "artifact_count": 1,
            "hash_algorithm": "sha256",
            "artifacts": [
                {
                    "artifact_path": "example.jsonl",
                    "artifact_role": "source_output",
                    "sha256": compute_file_sha256(artifact),
                    "size_bytes": artifact.stat().st_size,
                    "recorded_by": "artifact_hash_manifest_v0",
                }
            ],
        },
    }


def test_valid_artifact_roles_are_present() -> None:
    assert "source_output" in VALID_ARTIFACT_ROLES
    assert "dataset" in VALID_ARTIFACT_ROLES
    assert "result" in VALID_ARTIFACT_ROLES
    assert "manifest" in VALID_ARTIFACT_ROLES


def test_validate_artifact_entry_accepts_valid_entry(tmp_path: Path) -> None:
    artifact = tmp_path / "example.jsonl"
    artifact.write_text("hello\n", encoding="utf-8")

    entry = {
        "artifact_path": "example.jsonl",
        "artifact_role": "source_output",
        "sha256": compute_file_sha256(artifact),
    }

    assert validate_artifact_entry(entry, base_dir=tmp_path) == []


def test_validate_artifact_entry_rejects_missing_required_fields() -> None:
    errors = validate_artifact_entry({})

    assert "artifact_path must be a non-empty string" in errors
    assert "artifact_role must be a non-empty string" in errors
    assert "sha256 must be a non-empty string" in errors


def test_validate_artifact_entry_rejects_invalid_role() -> None:
    entry = {
        "artifact_path": "example.jsonl",
        "artifact_role": "truth_oracle",
        "sha256": "a" * 64,
    }

    errors = validate_artifact_entry(entry)

    assert any("artifact_role must be one of" in error for error in errors)


def test_validate_artifact_entry_rejects_invalid_sha256() -> None:
    entry = {
        "artifact_path": "example.jsonl",
        "artifact_role": "source_output",
        "sha256": "not-a-hash",
    }

    errors = validate_artifact_entry(entry)

    assert "sha256 must be a valid SHA-256 hexadecimal string" in errors


def test_validate_artifact_entry_can_require_existing_file() -> None:
    entry = {
        "artifact_path": "missing.jsonl",
        "artifact_role": "source_output",
        "sha256": "a" * 64,
    }

    errors = validate_artifact_entry(
        entry,
        base_dir=".",
        require_existing_file=True,
    )

    assert "artifact does not exist: missing.jsonl" in errors


def test_validate_artifact_entry_can_verify_hash(tmp_path: Path) -> None:
    artifact = tmp_path / "example.jsonl"
    artifact.write_text("hello\n", encoding="utf-8")

    entry = {
        "artifact_path": "example.jsonl",
        "artifact_role": "source_output",
        "sha256": compute_file_sha256(artifact),
    }

    errors = validate_artifact_entry(
        entry,
        base_dir=tmp_path,
        verify_hash=True,
    )

    assert errors == []


def test_validate_artifact_entry_detects_hash_mismatch(tmp_path: Path) -> None:
    artifact = tmp_path / "example.jsonl"
    artifact.write_text("hello\n", encoding="utf-8")

    entry = {
        "artifact_path": "example.jsonl",
        "artifact_role": "source_output",
        "sha256": "a" * 64,
    }

    errors = validate_artifact_entry(
        entry,
        base_dir=tmp_path,
        verify_hash=True,
    )

    assert any("sha256 mismatch for example.jsonl" in error for error in errors)


def test_validate_artifact_manifest_accepts_valid_manifest(tmp_path: Path) -> None:
    manifest = _valid_manifest(tmp_path)

    assert validate_artifact_manifest(manifest, base_dir=tmp_path) == []
    assert is_valid_artifact_manifest(manifest, base_dir=tmp_path)


def test_validate_artifact_manifest_can_verify_hashes(tmp_path: Path) -> None:
    manifest = _valid_manifest(tmp_path)

    assert validate_artifact_manifest(
        manifest,
        base_dir=tmp_path,
        verify_hashes=True,
    ) == []


def test_validate_artifact_manifest_rejects_missing_envelope_fields() -> None:
    manifest = {
        "payload": {
            "manifest_version": "v0",
            "manifest_scope": "data/source_outputs",
            "artifact_count": 0,
            "hash_algorithm": "sha256",
            "artifacts": [],
        }
    }

    errors = validate_artifact_manifest(manifest)

    assert "missing required field: experiment" in errors
    assert "missing required field: status" in errors
    assert "missing required field: created_at_utc" in errors
    assert "missing required field: boundary" in errors


def test_validate_artifact_manifest_rejects_missing_payload_fields() -> None:
    manifest = {
        "experiment": "artifact_hash_manifest_v0",
        "status": "CHECK",
        "created_at_utc": "2026-05-07T00:00:00+00:00",
        "boundary": "measurement != inference != decision",
        "payload": {},
    }

    errors = validate_artifact_manifest(manifest)

    assert "payload.manifest_version must be a non-empty string" in errors
    assert "payload.manifest_scope must be a non-empty string" in errors
    assert "payload.artifact_count must be an integer" in errors
    assert "payload.hash_algorithm must be: sha256" in errors
    assert "payload.artifacts must be a list" in errors


def test_validate_artifact_manifest_rejects_artifact_count_mismatch(tmp_path: Path) -> None:
    manifest = _valid_manifest(tmp_path)
    manifest["payload"]["artifact_count"] = 2

    errors = validate_artifact_manifest(manifest, base_dir=tmp_path)

    assert "payload.artifact_count must match len(payload.artifacts): 2 != 1" in errors


def test_validate_artifact_manifest_rejects_wrong_hash_algorithm(tmp_path: Path) -> None:
    manifest = _valid_manifest(tmp_path)
    manifest["payload"]["hash_algorithm"] = "md5"

    errors = validate_artifact_manifest(manifest, base_dir=tmp_path)

    assert "payload.hash_algorithm must be: sha256" in errors


def test_validate_artifact_manifest_rejects_bad_artifact_entry(tmp_path: Path) -> None:
    manifest = _valid_manifest(tmp_path)
    manifest["payload"]["artifacts"][0]["sha256"] = "bad"

    errors = validate_artifact_manifest(manifest, base_dir=tmp_path)

    assert any(
        error == "payload.artifacts[0]: sha256 must be a valid SHA-256 hexadecimal string"
        for error in errors
    )


def test_require_valid_artifact_manifest_raises(tmp_path: Path) -> None:
    manifest = _valid_manifest(tmp_path)
    manifest["payload"]["artifacts"][0]["artifact_role"] = "truth_oracle"

    with pytest.raises(ValueError, match="invalid artifact manifest"):
        require_valid_artifact_manifest(manifest, base_dir=tmp_path)


def test_existing_artifact_hash_manifest_is_valid() -> None:
    path = Path("results/artifact_hash_manifest_v0.json")

    if not path.exists():
        pytest.skip("results/artifact_hash_manifest_v0.json is not present")

    manifest = json.loads(path.read_text(encoding="utf-8"))

    errors = validate_artifact_manifest(manifest)

    assert errors == []


def test_existing_artifact_hash_manifest_hashes_match_when_files_exist() -> None:
    path = Path("results/artifact_hash_manifest_v0.json")

    if not path.exists():
        pytest.skip("results/artifact_hash_manifest_v0.json is not present")

    manifest = json.loads(path.read_text(encoding="utf-8"))

    missing_paths = [
        entry["artifact_path"]
        for entry in manifest["payload"]["artifacts"]
        if not Path(entry["artifact_path"]).exists()
    ]

    if missing_paths:
        pytest.skip(f"artifact paths not present in checkout: {missing_paths}")

    errors = validate_artifact_manifest(
        manifest,
        verify_hashes=True,
    )

    assert errors == []