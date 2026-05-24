import json
import subprocess
import sys

from omnia_validation_runner.core import (
    evaluate_cases,
    evaluate_case,
    extract_last_number,
    normalize_text,
    read_jsonl,
    ValidationCase,
)


def test_normalize_text():
    assert normalize_text("  Hello   WORLD ") == "hello world"


def test_extract_last_number():
    assert extract_last_number("Final answer: 42") == "42"
    assert extract_last_number("a 1 b 2.5") == "2.5"
    assert extract_last_number("none") is None


def test_evaluate_case_exact_pass():
    case = ValidationCase(
        case_id="c1",
        suite="s",
        input="",
        expected="yes",
        observed=" yes ",
        surface_status="ok",
        notes="",
    )
    result = evaluate_case(case)
    assert result.status == "PASS"
    assert result.silent_failure is False


def test_evaluate_case_numeric_pass():
    case = ValidationCase(
        case_id="c1",
        suite="s",
        input="",
        expected="42",
        observed="Final answer: 42",
        surface_status="ok",
        notes="",
    )
    result = evaluate_case(case)
    assert result.status == "NUMERIC_PASS"


def test_evaluate_case_silent_failure():
    case = ValidationCase(
        case_id="c1",
        suite="s",
        input="",
        expected="deny",
        observed="approve",
        surface_status="ok",
        notes="",
    )
    result = evaluate_case(case)
    assert result.status == "SILENT_FAILURE"
    assert result.silent_failure is True


def test_read_jsonl_and_evaluate(tmp_path):
    p = tmp_path / "cases.jsonl"
    p.write_text(
        '{"case_id":"a","expected":"1","observed":"1","surface_status":"ok"}\n'
        '{"case_id":"b","expected":"2","observed":"3","surface_status":"failed"}\n',
        encoding="utf-8",
    )

    cases = read_jsonl(str(p))
    result = evaluate_cases(cases)

    assert result["summary"]["total_cases"] == 2
    assert result["summary"]["passed_cases"] == 1
    assert result["summary"]["failed_cases"] == 1
    assert "certificate" in result


def test_cli_writes_reports(tmp_path):
    input_path = tmp_path / "cases.jsonl"
    out_dir = tmp_path / "report"

    input_path.write_text(
        '{"case_id":"a","expected":"1","observed":"1","surface_status":"ok"}\n'
        '{"case_id":"b","expected":"2","observed":"3","surface_status":"ok"}\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "omnia_validation_runner.cli",
            "--input",
            str(input_path),
            "--out-dir",
            str(out_dir),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0
    assert (out_dir / "report.json").exists()
    assert (out_dir / "report.csv").exists()
    assert (out_dir / "report.html").exists()
    assert (out_dir / "failures.jsonl").exists()
    assert (out_dir / "silent_failures.jsonl").exists()
    assert (out_dir / "certificate.json").exists()

    report = json.loads((out_dir / "report.json").read_text(encoding="utf-8"))
    assert report["summary"]["total_cases"] == 2
    assert report["summary"]["silent_failures"] == 1


def test_cli_fail_on_failed(tmp_path):
    input_path = tmp_path / "cases.jsonl"
    out_dir = tmp_path / "report"

    input_path.write_text(
        '{"case_id":"a","expected":"1","observed":"2","surface_status":"failed"}\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "omnia_validation_runner.cli",
            "--input",
            str(input_path),
            "--out-dir",
            str(out_dir),
            "--fail-on-failed",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 2


def test_cli_fail_on_silent_failure(tmp_path):
    input_path = tmp_path / "cases.jsonl"
    out_dir = tmp_path / "report"

    input_path.write_text(
        '{"case_id":"a","expected":"deny","observed":"approve","surface_status":"ok"}\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "omnia_validation_runner.cli",
            "--input",
            str(input_path),
            "--out-dir",
            str(out_dir),
            "--fail-on-silent-failure",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 3
