from pathlib import Path

from omnia_validation.io import read_json, read_jsonl, write_json, write_jsonl


def test_json_roundtrip(tmp_path: Path):
    path = tmp_path / "result.json"
    data = {"status": "PASS", "value": 1}

    write_json(path, data)

    assert read_json(path) == data


def test_jsonl_roundtrip(tmp_path: Path):
    path = tmp_path / "records.jsonl"
    records = [{"id": "a", "value": 1}, {"id": "b", "value": 2}]

    write_jsonl(path, records)

    assert read_jsonl(path) == records