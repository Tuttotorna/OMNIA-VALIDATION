"""Artifact manifest validation helpers for OMNIA-VALIDATION.

Boundary:
    measurement != inference != decision

A valid hash proves artifact byte-level identity only when the computed hash
matches the recorded hash.

It does not prove semantic correctness, scientific truth, or production safety.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omnia_validation.hashing import compute_file_sha256, is_valid_sha256
from omnia_validation.schemas import validate_result_envelope

VALID_ARTIFACT_ROLES = {
    "dataset",
    "source_output",
    "model_output",
    "validator_script",
    "result",
    "enveloped_result",
    "manifest",
    "documentation",
    "configuration",
    "benchmark_input",
    "benchmark_output",
}


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_artifact_entry(
    entry: dict[str, Any],
    *,
    base_dir: str | Path = ".",
    require_existing_file: bool = False,
    verify_hash: bool = False,
) -> list[str]:
    """Validate one artifact entry from a manifest."""

    errors: list[str] = []

    if not isinstance(entry, dict):
        return ["artifact entry must be an object"]

    artifact_path = entry.get("artifact_path")
    artifact_role = entry.get("artifact_role")
    sha256 = entry.get("sha256")

    if not _is_non_empty_string(artifact_path):
        errors.append("artifact_path must be a non-empty string")

    if not _is_non_empty_string(artifact_role):
        errors.append("artifact_role must be a non-empty string")
    elif artifact_role not in VALID_ARTIFACT_ROLES:
        allowed = ", ".join(sorted(VALID_ARTIFACT_ROLES))
        errors.append(f"artifact_role must be one of: {allowed}")

    if not _is_non_empty_string(sha256):
        errors.append("sha256 must be a non-empty string")
    elif not is_valid_sha256(sha256):
        errors.append("sha256 must be a valid SHA-256 hexadecimal string")

    if artifact_path and isinstance(artifact_path, str):
        path = Path(base_dir) / artifact_path

        if require_existing_file and not path.exists():
            errors.append(f"artifact does not exist: {artifact_path}")

        if verify_hash:
            if not path.exists():
                errors.append(
                    "artifact does not exist for hash verification: "
                    f"{artifact_path}"
                )
            elif path.is_dir():
                errors.append(f"artifact path is a directory: {artifact_path}")
            elif isinstance(sha256, str) and is_valid_sha256(sha256):
                computed = compute_file_sha256(path)
                if computed != sha256:
                    errors.append(
                        f"sha256 mismatch for {artifact_path}: "
                        f"expected {sha256}, computed {computed}"
                    )

    return errors


def validate_artifact_manifest(
    manifest: dict[str, Any],
    *,
    base_dir: str | Path = ".",
    require_existing_files: bool = False,
    verify_hashes: bool = False,
) -> list[str]:
    """Validate an artifact hash manifest."""

    errors: list[str] = []

    envelope_errors = validate_result_envelope(manifest)
    errors.extend(envelope_errors)

    if not isinstance(manifest, dict):
        return errors or ["manifest must be an object"]

    payload = manifest.get("payload")
    if not isinstance(payload, dict):
        errors.append("payload must be an object")
        return errors

    manifest_version = payload.get("manifest_version")
    manifest_scope = payload.get("manifest_scope")
    artifact_count = payload.get("artifact_count")
    hash_algorithm = payload.get("hash_algorithm")
    artifacts = payload.get("artifacts")

    if not _is_non_empty_string(manifest_version):
        errors.append("payload.manifest_version must be a non-empty string")

    if not _is_non_empty_string(manifest_scope):
        errors.append("payload.manifest_scope must be a non-empty string")

    if not isinstance(artifact_count, int):
        errors.append("payload.artifact_count must be an integer")
    elif artifact_count < 0:
        errors.append("payload.artifact_count must be >= 0")

    if hash_algorithm != "sha256":
        errors.append("payload.hash_algorithm must be: sha256")

    if not isinstance(artifacts, list):
        errors.append("payload.artifacts must be a list")
        return errors

    if isinstance(artifact_count, int) and artifact_count != len(artifacts):
        errors.append(
            "payload.artifact_count must match len(payload.artifacts): "
            f"{artifact_count} != {len(artifacts)}"
        )

    for index, entry in enumerate(artifacts):
        entry_errors = validate_artifact_entry(
            entry,
            base_dir=base_dir,
            require_existing_file=require_existing_files or verify_hashes,
            verify_hash=verify_hashes,
        )
        for error in entry_errors:
            errors.append(f"payload.artifacts[{index}]: {error}")

    return errors


def is_valid_artifact_manifest(
    manifest: dict[str, Any],
    *,
    base_dir: str | Path = ".",
    require_existing_files: bool = False,
    verify_hashes: bool = False,
) -> bool:
    """Return True if the artifact manifest passes validation."""

    return not validate_artifact_manifest(
        manifest,
        base_dir=base_dir,
        require_existing_files=require_existing_files,
        verify_hashes=verify_hashes,
    )


def require_valid_artifact_manifest(
    manifest: dict[str, Any],
    *,
    base_dir: str | Path = ".",
    require_existing_files: bool = False,
    verify_hashes: bool = False,
) -> None:
    """Raise ValueError if the artifact manifest is invalid."""

    errors = validate_artifact_manifest(
        manifest,
        base_dir=base_dir,
        require_existing_files=require_existing_files,
        verify_hashes=verify_hashes,
    )

    if errors:
        raise ValueError("invalid artifact manifest: " + "; ".join(errors))
