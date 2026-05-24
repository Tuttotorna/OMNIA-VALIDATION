import argparse
import sys
from pathlib import Path

from .core import evaluate_cases, read_jsonl, write_all_reports


def main():
    parser = argparse.ArgumentParser(
        prog="omnia-validation-runner",
        description="Run reproducible OMNIA validation reports from JSONL case files.",
    )

    parser.add_argument("--input", required=True, help="JSONL file with validation cases.")
    parser.add_argument("--out-dir", default="validation_report", help="Output directory.")
    parser.add_argument("--fail-on-failed", action="store_true", help="Exit with code 2 if failed cases exist.")
    parser.add_argument("--fail-on-silent-failure", action="store_true", help="Exit with code 3 if silent failures exist.")

    args = parser.parse_args()

    cases = read_jsonl(args.input)
    result = evaluate_cases(cases)
    write_all_reports(args.out_dir, result)

    s = result["summary"]

    print("")
    print("OMNIA VALIDATION RUN")
    print("====================")
    print(f"input:                 {args.input}")
    print(f"total_cases:           {s['total_cases']}")
    print(f"passed_cases:          {s['passed_cases']}")
    print(f"failed_cases:          {s['failed_cases']}")
    print(f"silent_failures:       {s['silent_failures']}")
    print(f"pass_rate:             {s['pass_rate']:.6f}")
    print(f"failure_rate:          {s['failure_rate']:.6f}")
    print(f"silent_failure_rate:   {s['silent_failure_rate']:.6f}")
    print("")
    print(f"WROTE: {Path(args.out_dir) / 'report.json'}")
    print(f"WROTE: {Path(args.out_dir) / 'report.csv'}")
    print(f"WROTE: {Path(args.out_dir) / 'report.html'}")
    print(f"WROTE: {Path(args.out_dir) / 'failures.jsonl'}")
    print(f"WROTE: {Path(args.out_dir) / 'silent_failures.jsonl'}")
    print(f"WROTE: {Path(args.out_dir) / 'certificate.json'}")
    print("")

    if args.fail_on_silent_failure and s["silent_failures"] > 0:
        sys.exit(3)

    if args.fail_on_failed and s["failed_cases"] > 0:
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
