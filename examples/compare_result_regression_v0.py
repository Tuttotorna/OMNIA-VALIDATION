"""Compare two OMNIA-VALIDATION result artifacts.

Boundary:
    measurement != inference != decision

This script classifies structural result differences.
It does not validate semantic truth or scientific correctness.
"""

from __future__ import annotations

import argparse
import json

from omnia_validation.regression import compare_result_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare two OMNIA-VALIDATION result artifacts.",
    )
    parser.add_argument("--previous", required=True)
    parser.add_argument("--current", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    comparison = compare_result_files(args.previous, args.current)

    print(json.dumps(comparison, indent=2, sort_keys=False))

    if comparison["status"] == "FAIL":
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

