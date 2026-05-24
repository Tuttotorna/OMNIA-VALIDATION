import csv
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ValidationCase:
    case_id: str
    suite: str
    input: str
    expected: str
    observed: str
    surface_status: str
    notes: str


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    suite: str
    status: str
    expected: str
    observed: str
    normalized_expected: str
    normalized_observed: str
    surface_status: str
    silent_failure: bool
    numeric_expected: Optional[str]
    numeric_observed: Optional[str]
    input: str
    notes: str


def normalize_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text.lower()


def extract_last_number(value: Any) -> Optional[str]:
    text = "" if value is None else str(value)
    matches = re.findall(r"[-+]?\d+(?:\.\d+)?", text)
    if not matches:
        return None
    return matches[-1]


def read_jsonl(path: str) -> List[ValidationCase]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    cases = []

    with p.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue

            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSONL at line " + str(line_no) + ": " + str(e))

            for key in ["case_id", "expected", "observed"]:
                if key not in obj:
                    raise ValueError("Missing required field '" + key + "' at line " + str(line_no))

            cases.append(
                ValidationCase(
                    case_id=str(obj.get("case_id", "")).strip(),
                    suite=str(obj.get("suite", "default")).strip() or "default",
                    input=str(obj.get("input", "")),
                    expected=str(obj.get("expected", "")),
                    observed=str(obj.get("observed", "")),
                    surface_status=str(obj.get("surface_status", "")).strip().lower(),
                    notes=str(obj.get("notes", "")),
                )
            )

    if not cases:
        raise ValueError("No validation cases found in " + path)

    return cases


def evaluate_case(case: ValidationCase) -> CaseResult:
    ne = normalize_text(case.expected)
    no = normalize_text(case.observed)

    num_e = extract_last_number(case.expected)
    num_o = extract_last_number(case.observed)

    exact_match = ne == no
    numeric_match = (num_e is not None and num_o is not None and num_e == num_o)

    if exact_match:
        status = "PASS"
    elif numeric_match:
        status = "NUMERIC_PASS"
    else:
        status = "FAIL"

    surface_ok_values = {"ok", "pass", "passed", "valid", "accepted", "surface_ok", "looks_ok"}
    surface_ok = case.surface_status in surface_ok_values
    silent_failure = bool(surface_ok and status == "FAIL")

    if silent_failure:
        status = "SILENT_FAILURE"

    return CaseResult(
        case_id=case.case_id,
        suite=case.suite,
        status=status,
        expected=case.expected,
        observed=case.observed,
        normalized_expected=ne,
        normalized_observed=no,
        surface_status=case.surface_status,
        silent_failure=silent_failure,
        numeric_expected=num_e,
        numeric_observed=num_o,
        input=case.input,
        notes=case.notes,
    )


def evaluate_cases(cases: List[ValidationCase]) -> Dict[str, Any]:
    results = [evaluate_case(c) for c in cases]

    total = len(results)
    passed = sum(1 for r in results if r.status in {"PASS", "NUMERIC_PASS"})
    failed = sum(1 for r in results if r.status in {"FAIL", "SILENT_FAILURE"})
    silent = sum(1 for r in results if r.silent_failure)

    suites = {}
    for r in results:
        if r.suite not in suites:
            suites[r.suite] = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "silent_failures": 0,
            }

        suites[r.suite]["total"] += 1
        if r.status in {"PASS", "NUMERIC_PASS"}:
            suites[r.suite]["passed"] += 1
        if r.status in {"FAIL", "SILENT_FAILURE"}:
            suites[r.suite]["failed"] += 1
        if r.silent_failure:
            suites[r.suite]["silent_failures"] += 1

    summary = {
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": failed,
        "silent_failures": silent,
        "pass_rate": passed / total if total else 0.0,
        "failure_rate": failed / total if total else 0.0,
        "silent_failure_rate": silent / total if total else 0.0,
        "suites": suites,
        "problem_solved": "Produces reproducible validation reports from expected vs observed case files.",
    }

    certificate = {
        "audit_type": "omnia_validation_run",
        "summary": summary,
        "boundary": "measurement only; no semantic truth claim; no decision is made by the tool",
        "input_contract": {
            "format": "JSONL",
            "required_fields": ["case_id", "expected", "observed"],
            "optional_fields": ["suite", "input", "surface_status", "notes"],
        },
        "outputs": [
            "report.json",
            "report.csv",
            "report.html",
            "failures.jsonl",
            "silent_failures.jsonl",
            "certificate.json",
        ],
    }

    return {
        "summary": summary,
        "certificate": certificate,
        "results": [asdict(r) for r in results],
    }


def write_json(path: str, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv_report(path: str, result: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "case_id",
        "suite",
        "status",
        "expected",
        "observed",
        "surface_status",
        "silent_failure",
        "numeric_expected",
        "numeric_observed",
        "input",
        "notes",
    ]

    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in result["results"]:
            writer.writerow({k: row.get(k, "") for k in fields})


def html_escape(x: Any) -> str:
    return (
        str(x)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def write_html_report(path: str, result: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    summary = result["summary"]

    rows = []
    for r in result["results"]:
        if r["status"] in {"PASS", "NUMERIC_PASS"}:
            continue
        rows.append(
            "<tr>"
            + "<td>" + html_escape(r["case_id"]) + "</td>"
            + "<td>" + html_escape(r["suite"]) + "</td>"
            + "<td>" + html_escape(r["status"]) + "</td>"
            + "<td>" + html_escape(r["expected"]) + "</td>"
            + "<td>" + html_escape(r["observed"]) + "</td>"
            + "<td>" + html_escape(r["surface_status"]) + "</td>"
            + "<td>" + html_escape(r["silent_failure"]) + "</td>"
            + "</tr>"
        )

    html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>OMNIA Validation Report</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 32px;
      line-height: 1.45;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 8px;
      vertical-align: top;
    }}
    th {{
      background: #f2f2f2;
    }}
    .box {{
      background: #f8f8f8;
      padding: 16px;
      margin-bottom: 24px;
      border: 1px solid #eee;
    }}
  </style>
</head>
<body>
  <h1>OMNIA Validation Report</h1>

  <div class="box">
    <p><b>Total cases:</b> {total_cases}</p>
    <p><b>Passed cases:</b> {passed_cases}</p>
    <p><b>Failed cases:</b> {failed_cases}</p>
    <p><b>Silent failures:</b> {silent_failures}</p>
    <p><b>Pass rate:</b> {pass_rate:.6f}</p>
    <p><b>Failure rate:</b> {failure_rate:.6f}</p>
    <p><b>Silent failure rate:</b> {silent_failure_rate:.6f}</p>
  </div>

  <h2>Failed and Silent Failure Cases</h2>

  <table>
    <tr>
      <th>Case ID</th>
      <th>Suite</th>
      <th>Status</th>
      <th>Expected</th>
      <th>Observed</th>
      <th>Surface Status</th>
      <th>Silent Failure</th>
    </tr>
    {rows}
  </table>

  <h2>Boundary</h2>
  <p>This is a measurement report. It does not claim semantic truth and does not make a deployment decision.</p>
</body>
</html>
""".format(
        total_cases=summary["total_cases"],
        passed_cases=summary["passed_cases"],
        failed_cases=summary["failed_cases"],
        silent_failures=summary["silent_failures"],
        pass_rate=summary["pass_rate"],
        failure_rate=summary["failure_rate"],
        silent_failure_rate=summary["silent_failure_rate"],
        rows="".join(rows),
    )

    p.write_text(html, encoding="utf-8")


def write_jsonl_filtered(path: str, result: Dict[str, Any], mode: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    with p.open("w", encoding="utf-8") as f:
        for r in result["results"]:
            if mode == "failures" and r["status"] not in {"FAIL", "SILENT_FAILURE"}:
                continue
            if mode == "silent_failures" and not r["silent_failure"]:
                continue
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def write_all_reports(out_dir: str, result: Dict[str, Any]) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    write_json(str(out / "report.json"), result)
    write_csv_report(str(out / "report.csv"), result)
    write_html_report(str(out / "report.html"), result)
    write_jsonl_filtered(str(out / "failures.jsonl"), result, "failures")
    write_jsonl_filtered(str(out / "silent_failures.jsonl"), result, "silent_failures")
    write_json(str(out / "certificate.json"), result["certificate"])
