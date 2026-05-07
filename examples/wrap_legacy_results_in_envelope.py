"""Wrap legacy result JSON files into canonical OMNIA-VALIDATION envelopes.

This script is non-destructive.

It reads legacy files from:

    results/

and writes canonical wrapped copies into:

    results_enveloped/

It does not modify original result files.

Boundary:
    measurement != inference != decision
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omnia_validation.io import read_json, write_json
from omnia_validation.metadata import result_envelope
from omnia_validation.schemas import require_valid_result_envelope

RESULTS_DIR = Path("results")
OUTPUT_DIR = Path("results_enveloped")
MANIFEST_PATH = OUTPUT_DIR / "legacy_result_envelope_manifest_v0.json"

DEFAULT_STATUS = "CHECK"


def infer_experiment_name(path: Path) -> str:
    """Infer experiment name from result filename."""
    return path.stem


def infer_legacy_status(data: Any) -> Any:
    """Extract legacy status if present."""
    if isinstance(data, dict):
        return data.get("status")
    return None


def wrap_legacy_result(path: Path) -> dict[str, Any]:
    """Wrap one legacy result file into the canonical result envelope."""
    legacy_data = read_json(path)
    experiment = infer_experiment_name(path)
    legacy_status = infer_legacy_status(legacy_data)

    payload = {
        "legacy_result_path": str(path),
        "legacy_status": legacy_status,
        "legacy_result": legacy_data,
        "normalization_note": (
            "Legacy result wrapped into canonical OMNIA-VALIDATION envelope. "
            "The original result file was not modified. "
            "Wrapper status is CHECK because this is format normalization, "
            "not scientific revalidation."
        ),
    }

    wrapped = result_envelope(
        experiment=experiment,
        status=DEFAULT_STATUS,
        payload=payload,
    )

    require_valid_result_envelope(wrapped)

    return wrapped


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result_files = sorted(RESULTS_DIR.glob("*.json")) if RESULTS_DIR.exists() else []

    wrapped_files: list[str] = []
    failed_files: list[dict[str, str]] = []

    for path in result_files:
        if path.name == "result_schema_compliance_audit_v0.json":
            continue

        try:
            wrapped = wrap_legacy_result(path)
            output_path = OUTPUT_DIR / path.name
            write_json(output_path, wrapped)
            wrapped_files.append(str(output_path))
        except Exception as exc:
            failed_files.append(
                {
                    "path": str(path),
                    "error": str(exc),
                }
            )

    manifest_payload = {
        "source_dir": str(RESULTS_DIR),
        "output_dir": str(OUTPUT_DIR),
        "total_source_files": len(result_files),
        "wrapped_count": len(wrapped_files),
        "failed_count": len(failed_files),
        "wrapped_files": wrapped_files,
        "failed_files": failed_files,
        "interpretation": (
            "This manifest describes non-destructive wrapping of legacy result files. "
            "Wrapped files follow the canonical result envelope, while original files "
            "remain untouched."
        ),
    }

    manifest = result_envelope(
        experiment="legacy_result_envelope_manifest_v0",
        status="PASS" if not failed_files else "CHECK",
        payload=manifest_payload,
    )

    require_valid_result_envelope(manifest)
    write_json(MANIFEST_PATH, manifest)

    print("legacy_result_envelope_manifest_v0")
    print(f"source_dir: {RESULTS_DIR}")
    print(f"output_dir: {OUTPUT_DIR}")
    print(f"total_source_files: {len(result_files)}")
    print(f"wrapped_count: {len(wrapped_files)}")
    print(f"failed_count: {len(failed_files)}")
    print(f"manifest: {MANIFEST_PATH}")

    if failed_files:
        print("\nFAILED FILES:")
        for item in failed_files:
            print(f"- {item['path']}: {item['error']}")

    return 0 if not failed_files else 1


if __name__ == "__main__":
    raise SystemExit(main())
