"""Audit existing result files for OMNIA-VALIDATION schema compliance.

This script is diagnostic.

It does not modify files.
It does not fail the repository.
It reports which result JSON files already follow the canonical result envelope.

Boundary:
    measurement != inference != decision
"""

from __future__ import annotations

from pathlib import Path

from omnia_validation.io import read_json, write_json
from omnia_validation.schemas import validate_result_envelope

RESULTS_DIR = Path("results")
AUDIT_OUTPUT_PATH = Path("results/result_schema_compliance_audit_v0.json")


def audit_results(results_dir: Path = RESULTS_DIR) -> dict:
    """Audit JSON result files for canonical result-envelope compliance."""
    result_files = sorted(results_dir.glob("*.json")) if results_dir.exists() else []

    compliant_files: list[str] = []
    non_compliant_files: list[dict] = []
    unreadable_files: list[dict] = []

    for path in result_files:
        if path == AUDIT_OUTPUT_PATH:
            continue

        try:
            data = read_json(path)
        except Exception as exc:
            unreadable_files.append(
                {
                    "path": str(path),
                    "error": str(exc),
                }
            )
            continue

        errors = validate_result_envelope(data)

        if errors:
            non_compliant_files.append(
                {
                    "path": str(path),
                    "errors": errors,
                }
            )
        else:
            compliant_files.append(str(path))

    total_checked = len(compliant_files) + len(non_compliant_files)

    return {
        "experiment": "result_schema_compliance_audit_v0",
        "status": "PASS",
        "boundary": "measurement != inference != decision",
        "payload": {
            "results_dir": str(results_dir),
            "total_json_files_checked": total_checked,
            "compliant_count": len(compliant_files),
            "non_compliant_count": len(non_compliant_files),
            "unreadable_count": len(unreadable_files),
            "compliant_files": compliant_files,
            "non_compliant_files": non_compliant_files,
            "unreadable_files": unreadable_files,
            "interpretation": (
                "This audit checks result-envelope schema compliance only. "
                "Non-compliance means the file is not yet in the canonical "
                "OMNIA-VALIDATION result-envelope format. It does not imply "
                "that the underlying experiment is scientifically invalid."
            ),
        },
    }


def main() -> int:
    audit = audit_results()

    write_json(AUDIT_OUTPUT_PATH, audit)

    payload = audit["payload"]

    print("result_schema_compliance_audit_v0")
    print(f"results_dir: {payload['results_dir']}")
    print(f"total_json_files_checked: {payload['total_json_files_checked']}")
    print(f"compliant_count: {payload['compliant_count']}")
    print(f"non_compliant_count: {payload['non_compliant_count']}")
    print(f"unreadable_count: {payload['unreadable_count']}")
    print(f"output: {AUDIT_OUTPUT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())