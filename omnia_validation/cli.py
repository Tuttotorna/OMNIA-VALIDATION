"""Command line interface for OMNIA-VALIDATION."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .hashing import is_sha256_hex, sha256_file
from .io import read_json, read_jsonl
from .schemas import validate_result_envelope


def _cmd_hash_file(args: argparse.Namespace) -> int:
    digest = sha256_file(args.path)
    print(digest)
    return 0


def _cmd_validate_sha256(args: argparse.Namespace) -> int:
    if is_sha256_hex(args.value):
        print("PASS")
        return 0

    print("FAIL")
    return 1


def _cmd_validate_json(args: argparse.Namespace) -> int:
    path = Path(args.path)

    try:
        if path.suffix == ".jsonl":
            records = read_jsonl(path)
            print(json.dumps({"status": "PASS", "records": len(records)}, indent=2))
            return 0

        read_json(path)
        print(json.dumps({"status": "PASS"}, indent=2))
        return 0

    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 1


def _cmd_validate_result(args: argparse.Namespace) -> int:
    path = Path(args.path)

    try:
        result = read_json(path)
        errors = validate_result_envelope(result)

        if errors:
            print(
                json.dumps(
                    {
                        "status": "FAIL",
                        "errors": errors,
                    },
                    indent=2,
                )
            )
            return 1

        print(
            json.dumps(
                {
                    "status": "PASS",
                    "schema": "result_envelope",
                },
                indent=2,
            )
        )
        return 0

    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omnia-validation",
        description="Reusable utilities for OMNIA-VALIDATION artifacts.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    hash_parser = subparsers.add_parser("hash-file", help="Compute SHA-256 for a file")
    hash_parser.add_argument("path")
    hash_parser.set_defaults(func=_cmd_hash_file)

    sha_parser = subparsers.add_parser(
        "validate-sha256",
        help="Validate a SHA-256 hexadecimal string",
    )
    sha_parser.add_argument("value")
    sha_parser.set_defaults(func=_cmd_validate_sha256)

    json_parser = subparsers.add_parser(
        "validate-json",
        help="Validate that a .json or .jsonl file is parseable",
    )
    json_parser.add_argument("path")
    json_parser.set_defaults(func=_cmd_validate_json)

    result_parser = subparsers.add_parser(
        "validate-result",
        help="Validate a result JSON file against the canonical result envelope schema",
    )
    result_parser.add_argument("path")
    result_parser.set_defaults(func=_cmd_validate_result)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())