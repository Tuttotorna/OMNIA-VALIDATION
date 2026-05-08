"""Command-line interface for OMNIA-VALIDATION.

Boundary:
    measurement != inference != decision

The CLI validates artifact structure, schema shape, and traceability signals.
It does not validate semantic truth, scientific correctness, or production safety.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from omnia_validation.hashing import compute_file_sha256, is_valid_sha256
from omnia_validation.manifest import validate_artifact_manifest
from omnia_validation.regression import compare_result_files
from omnia_validation.schemas import validate_result_envelope


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=False))


def _is_jsonl_path(path: Path) -> bool:
    return path.suffix.lower() == ".jsonl"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[Any]:
    records: list[Any] = []

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue

        try:
            records.append(json.loads(stripped))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {line_number}: {exc}") from exc

    return records


def _validate_json_file(path: Path) -> list[str]:
    if not path.exists():
        return [f"file does not exist: {path}"]

    if path.is_dir():
        return [f"path is a directory: {path}"]

    try:
        if _is_jsonl_path(path):
            _read_jsonl(path)
        else:
            _read_json(path)
    except Exception as exc:
        return [f"invalid JSON artifact: {exc}"]

    return []


def cmd_validate_sha256(args: argparse.Namespace) -> int:
    if is_valid_sha256(args.value):
        print("PASS")
        return 0

    print("FAIL")
    return 1


def cmd_hash_file(args: argparse.Namespace) -> int:
    path = Path(args.path)

    if not path.exists():
        _print_json(
            {
                "status": "FAIL",
                "errors": [f"file does not exist: {args.path}"],
            }
        )
        return 1

    if path.is_dir():
        _print_json(
            {
                "status": "FAIL",
                "errors": [f"path is a directory: {args.path}"],
            }
        )
        return 1

    print(compute_file_sha256(path))
    return 0


def cmd_validate_json(args: argparse.Namespace) -> int:
    path = Path(args.path)
    errors = _validate_json_file(path)

    if errors:
        _print_json(
            {
                "status": "FAIL",
                "errors": errors,
            }
        )
        return 1

    if _is_jsonl_path(path):
        records = _read_jsonl(path)
        _print_json(
            {
                "status": "PASS",
                "records": len(records),
            }
        )
        return 0

    _print_json(
        {
            "status": "PASS",
        }
    )
    return 0


def cmd_validate_result(args: argparse.Namespace) -> int:
    path = Path(args.path)

    json_errors = _validate_json_file(path)
    if json_errors:
        _print_json(
            {
                "status": "FAIL",
                "errors": json_errors,
            }
        )
        return 1

    if _is_jsonl_path(path):
        _print_json(
            {
                "status": "FAIL",
                "errors": ["validate-result expects a JSON object, not JSONL"],
            }
        )
        return 1

    result = _read_json(path)
    errors = validate_result_envelope(result)

    if errors:
        _print_json(
            {
                "status": "FAIL",
                "errors": errors,
            }
        )
        return 1

    _print_json(
        {
            "status": "PASS",
            "schema": "result_envelope",
        }
    )
    return 0


def cmd_validate_manifest(args: argparse.Namespace) -> int:
    path = Path(args.path)

    json_errors = _validate_json_file(path)
    if json_errors:
        _print_json(
            {
                "status": "FAIL",
                "errors": json_errors,
            }
        )
        return 1

    if _is_jsonl_path(path):
        _print_json(
            {
                "status": "FAIL",
                "errors": ["validate-manifest expects a JSON object, not JSONL"],
            }
        )
        return 1

    manifest = _read_json(path)
    errors = validate_artifact_manifest(
        manifest,
        base_dir=args.base_dir,
        require_existing_files=args.require_existing_files,
        verify_hashes=args.verify_hashes,
    )

    if errors:
        _print_json(
            {
                "status": "FAIL",
                "errors": errors,
            }
        )
        return 1

    _print_json(
        {
            "status": "PASS",
            "schema": "artifact_manifest",
        }
    )
    return 0


def cmd_compare_results(args: argparse.Namespace) -> int:
    previous_path = Path(args.previous)
    current_path = Path(args.current)

    errors: list[str] = []

    if not previous_path.exists():
        errors.append(f"previous file does not exist: {args.previous}")

    if not current_path.exists():
        errors.append(f"current file does not exist: {args.current}")

    if errors:
        _print_json(
            {
                "status": "FAIL",
                "schema": "result_regression_comparison",
                "classification": "SCHEMA_REGRESSION",
                "errors": errors,
            }
        )
        return 1

    comparison = compare_result_files(previous_path, current_path)
    classification = comparison["payload"]["classification"]

    _print_json(
        {
            "status": comparison["status"],
            "schema": "result_regression_comparison",
            "classification": classification,
            "payload": comparison["payload"],
        }
    )

    if comparison["status"] == "FAIL":
        return 1

    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omnia-validation",
        description="OMNIA-VALIDATION artifact, schema, hash, and manifest checks.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_sha256 = subparsers.add_parser(
        "validate-sha256",
        help="Validate SHA-256 hexadecimal format.",
    )
    validate_sha256.add_argument("value")
    validate_sha256.set_defaults(func=cmd_validate_sha256)

    hash_file = subparsers.add_parser(
        "hash-file",
        help="Compute SHA-256 for a file.",
    )
    hash_file.add_argument("path")
    hash_file.set_defaults(func=cmd_hash_file)

    validate_json = subparsers.add_parser(
        "validate-json",
        help="Validate JSON or JSONL parseability.",
    )
    validate_json.add_argument("path")
    validate_json.set_defaults(func=cmd_validate_json)

    validate_result = subparsers.add_parser(
        "validate-result",
        help="Validate canonical OMNIA-VALIDATION result envelope.",
    )
    validate_result.add_argument("path")
    validate_result.set_defaults(func=cmd_validate_result)

    validate_manifest = subparsers.add_parser(
        "validate-manifest",
        help="Validate artifact hash manifest structure and optional hashes.",
    )
    validate_manifest.add_argument("path")
    validate_manifest.add_argument(
        "--base-dir",
        default=".",
        help="Base directory used to resolve artifact paths.",
    )
    validate_manifest.add_argument(
        "--require-existing-files",
        action="store_true",
        help="Require every artifact path in the manifest to exist.",
    )
    validate_manifest.add_argument(
        "--verify-hashes",
        action="store_true",
        help="Require every artifact hash to match the current file bytes.",
    )
    validate_manifest.set_defaults(func=cmd_validate_manifest)

    compare_results = subparsers.add_parser(
        "compare-results",
        help="Compare two OMNIA-VALIDATION result artifacts.",
    )
    compare_results.add_argument(
        "--previous",
        required=True,
        help="Previous result JSON file.",
    )
    compare_results.add_argument(
        "--current",
        required=True,
        help="Current result JSON file.",
    )
    compare_results.set_defaults(func=cmd_compare_results)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
