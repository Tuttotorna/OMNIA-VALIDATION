"""Build artifact_hash_manifest_v0 for OMNIA-VALIDATION.

This script generates:

    results/artifact_hash_manifest_v0.json

Default scope:

    data/source_outputs/

Boundary:

    measurement != inference != decision

Hashing proves byte-level artifact identity.
Hashing does not prove semantic correctness, scientific truth, or production safety.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from omnia_validation.hashing import compute_file_sha256
from omnia_validation.manifest import require_valid_artifact_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SOURCE_OUTPUTS_DIR = REPO_ROOT / "data" / "source_outputs"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "results" / "artifact_hash_manifest_v0.json"

MANIFEST_EXPERIMENT = "artifact_hash_manifest_v0"
MANIFEST_VERSION = "v0"
MANIFEST_SCOPE = "data/source_outputs"
STABLE_TIMESTAMP = "2026-05-07T00:00:00+00:00"

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


def resolve_path(value: str | Path, *, default_base: Path = REPO_ROOT) -> Path:
    """Resolve a user path.

    Relative paths are interpreted relative to the repository root.
    Absolute paths are preserved.
    """

    path = Path(value)

    if path.is_absolute():
        return path

    return default_base / path


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


def relative_artifact_path(path: Path, base_dir: Path) -> str:
    """Return artifact path relative to base_dir."""

    return path.resolve().relative_to(base_dir.resolve()).as_posix()


def display_path(path: Path) -> str:
    """Return a readable path for CLI output.

    If the path is inside the repository, print it relative to the repository.
    Otherwise, print the absolute/as-posix path.

    This keeps tests working when output paths are temporary directories.
    """

    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def build_artifact_entry(path: Path, *, base_dir: Path) -> dict[str, Any]:
    """Build one artifact entry."""

    provider, run_id = infer_provider_and_run(path)

    entry: dict[str, Any] = {
        "artifact_path": relative_artifact_path(path, base_dir),
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


def select_created_at(*, created_at: str | None, stable_timestamp: bool) -> str:
    """Select manifest timestamp."""

    if created_at:
        return created_at

    if stable_timestamp:
        return STABLE_TIMESTAMP

    return utc_now_iso()


def build_manifest(
    *,
    source_dir: Path,
    base_dir: Path,
    created_at: str,
) -> dict[str, Any]:
    """Build the canonical artifact hash manifest."""

    artifacts = []

    if source_dir.exists():
        for path in sorted(source_dir.glob("*.jsonl")):
            artifacts.append(build_artifact_entry(path, base_dir=base_dir))

    manifest: dict[str, Any] = {
        "experiment": MANIFEST_EXPERIMENT,
        "status": "CHECK",
        "created_at_utc": created_at,
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


def build_parser() -> argparse.ArgumentParser:
    """Build command-line parser."""

    parser = argparse.ArgumentParser(
        description="Build OMNIA-VALIDATION artifact hash manifest v0.",
    )

    parser.add_argument(
        "--source-dir",
        default=str(DEFAULT_SOURCE_OUTPUTS_DIR.relative_to(REPO_ROOT)),
        help="Directory containing source-output JSONL files.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH.relative_to(REPO_ROOT)),
        help="Output manifest JSON path.",
    )
    parser.add_argument(
        "--base-dir",
        default=str(REPO_ROOT),
        help="Base directory used for artifact_path values and validation.",
    )
    parser.add_argument(
        "--created-at",
        default=None,
        help="Explicit created_at_utc timestamp for deterministic manifests.",
    )
    parser.add_argument(
        "--stable-timestamp",
        action="store_true",
        help=f"Use stable timestamp: {STABLE_TIMESTAMP}",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Build, validate, and write the manifest."""

    parser = build_parser()
    args = parser.parse_args(argv)

    source_dir = resolve_path(args.source_dir)
    output_path = resolve_path(args.output)
    base_dir = resolve_path(args.base_dir)

    created_at = select_created_at(
        created_at=args.created_at,
        stable_timestamp=args.stable_timestamp,
    )

    manifest = build_manifest(
        source_dir=source_dir,
        base_dir=base_dir,
        created_at=created_at,
    )

    require_valid_artifact_manifest(
        manifest,
        base_dir=base_dir,
        verify_hashes=True,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )

    print("artifact_hash_manifest_v0")
    print(f"scope: {MANIFEST_SCOPE}")
    print(f"created_at_utc: {created_at}")
    print(f"artifact_count: {manifest['payload']['artifact_count']}")
    print(f"output: {display_path(output_path)}")
    print("status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
