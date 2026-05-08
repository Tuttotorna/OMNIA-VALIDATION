"""Build artifact_hash_manifest_v0 for OMNIA-VALIDATION.

This script generates:

    results/artifact_hash_manifest_v0.json

Current scope:

    data/source_outputs/

Boundary:

    measurement != inference != decision

Hashing proves byte-level artifact identity.
Hashing does not prove semantic correctness, scientific truth, or production safety.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from omnia_validation.hashing import compute_file_sha256
from omnia_validation.manifest import require_valid_artifact_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]

SOURCE_OUTPUTS_DIR = REPO_ROOT / "data" / "source_outputs"
OUTPUT_PATH = REPO_ROOT / "results" / "artifact_hash_manifest_v0.json"

MANIFEST_EXPERIMENT = "artifact_hash_manifest_v0"
MANIFEST_VERSION = "v0"
MANIFEST_SCOPE = "data/source_outputs"

SOURCE_VALIDATOR = "temporal_collapse_external_source_hash_strengthening_validator_v15"
SOURCE_VALIDATOR_RESULT = (
    "results/temporal_collapse_external_source_hash_strengthening_validator_v15.json"
)
SOURCE_VALIDATOR_DATA = (
    "data/temporal_collapse_external_source_hash_strengthened_v15.jsonl"
)


def utc_now_iso() -> str:
    """Return current UTC timestamp in ISO-8601 format."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def infer_provider_and_run(path: Path) -> tuple[str | None, str | None]:
    """Infer source provider and run label from known V14/V15 source-output names."""

    name = path.name

    if "provider_a_run_001" in name:
        return "provider_a", "provider_a_run_v14_001"

    if "provider_a_run_002" in name:
        return "provider_a", "provider_a_run_v14_002"

    if "provider_b_run_001" in name:
        return "provider_b", "provider_b_run_v14_001"

    if "provider_b_run_002" in name:
        return "provider_b", "provider_b_run_v14_002"

    return None, None


def build_artifact_entry(path: Path) -> dict[str, Any]:
    """Build one artifact entry."""

    relative_path = path.relative_to(REPO_ROOT).as_posix()
    provider, run_id = infer_provider_and_run(path)

    entry: dict[str, Any] = {
        "artifact_path": relative_path,
        "artifact_role": "source_output",
        "sha256": compute_file_sha256(path),
        "size_bytes": path.stat().st_size,
        "recorded_by": MANIFEST_EXPERIMENT,
        "source_validator": SOURCE_VALIDATOR,
        "notes": "Real SHA-256 hash computed from current repository file.",
    }

    if provider is not None:
        entry["source_provider"] = provider

    if run_id is not None:
        entry["source_run"] = run_id

    return entry


def build_manifest() -> dict[str, Any]:
    """Build the canonical artifact hash manifest."""

    artifacts = []

    if SOURCE_OUTPUTS_DIR.exists():
        for path in sorted(SOURCE_OUTPUTS_DIR.glob("*.jsonl")):
            artifacts.append(build_artifact_entry(path))

    manifest: dict[str, Any] = {
        "experiment": MANIFEST_EXPERIMENT,
        "status": "CHECK",
        "created_at_utc": utc_now_iso(),
        "boundary": "measurement != inference != decision",
        "payload": {
            "manifest_version": MANIFEST_VERSION,
            "manifest_scope": MANIFEST_SCOPE,
            "manifest_status": "generated_manifest",
            "artifact_count": len(artifacts),
            "hash_algorithm": "sha256",
            "hash_format": "64 lowercase hexadecimal characters",
            "source_validator": SOURCE_VALIDATOR,
            "source_validator_result": SOURCE_VALIDATOR_RESULT,
            "source_validator_data": SOURCE_VALIDATOR_DATA,
            "traceability_summary": {
                "source_file_count": len(artifacts),
                "computed_hash_count": len(artifacts),
                "real_hash_count": len(artifacts),
                "placeholder_hash_count": 0,
                "hash_format_failure_count": 0,
                "hash_mismatch_failure_count": 0,
                "missing_source_file_count": 0,
            },
            "status_reason": (
                "CHECK because this manifest records source-output artifact "
                "hashes for a bounded scope only. Hashes are real SHA-256 "
                "values computed from current files, but repository-wide "
                "artifact coverage is not yet present."
            ),
            "artifacts": artifacts,
            "missing_artifacts": [],
            "interpretation": {
                "correct": [
                    "hash match means artifact byte identity is preserved",
                    "hash presence improves source traceability",
                    "this manifest records source-output hashes",
                ],
                "incorrect": [
                    "hash presence proves semantic correctness",
                    "hash match proves scientific truth",
                    "hash traceability certifies production safety",
                ],
            },
            "current_limitations": [
                "repository-wide artifact coverage is not yet present",
                "this manifest currently covers only data/source_outputs/",
                "hashing does not prove semantic correctness",
            ],
        },
    }

    return manifest


def main() -> int:
    """Build, validate, and write the manifest."""

    manifest = build_manifest()

    require_valid_artifact_manifest(
        manifest,
        base_dir=REPO_ROOT,
        verify_hashes=True,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )

    print("artifact_hash_manifest_v0")
    print(f"scope: {MANIFEST_SCOPE}")
    print(f"artifact_count: {manifest['payload']['artifact_count']}")
    print(f"output: {OUTPUT_PATH.relative_to(REPO_ROOT).as_posix()}")
    print("status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())