from pathlib import Path

from omnia_validation.cli import main


def test_cli_validate_sha256_pass(capsys):
    exit_code = main(
        [
            "validate-sha256",
            "a" * 64,
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "PASS" in captured.out


def test_cli_validate_sha256_fail(capsys):
    exit_code = main(
        [
            "validate-sha256",
            "not-a-valid-hash",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "FAIL" in captured.out


def test_cli_hash_file(tmp_path: Path, capsys):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("omnia", encoding="utf-8")

    exit_code = main(["hash-file", str(file_path)])

    captured = capsys.readouterr()
    digest = captured.out.strip()

    assert exit_code == 0
    assert len(digest) == 64


def test_cli_validate_json(tmp_path: Path, capsys):
    file_path = tmp_path / "sample.json"
    file_path.write_text('{"status": "PASS"}', encoding="utf-8")

    exit_code = main(["validate-json", str(file_path)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"status": "PASS"' in captured.out


def test_cli_validate_jsonl(tmp_path: Path, capsys):
    file_path = tmp_path / "sample.jsonl"
    file_path.write_text('{"id": 1}\n{"id": 2}\n', encoding="utf-8")

    exit_code = main(["validate-json", str(file_path)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"status": "PASS"' in captured.out
    assert '"records": 2' in captured.out