from pathlib import Path

from omnia_validation.hashing import is_sha256_hex
from omnia_validation.metadata import file_metadata, result_envelope, utc_now_iso


def test_utc_now_iso_returns_utc_timestamp():
    timestamp = utc_now_iso()

    assert timestamp.endswith("+00:00")
    assert "T" in timestamp


def test_file_metadata(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("omnia", encoding="utf-8")

    metadata = file_metadata(file_path)

    assert metadata["path"] == str(file_path)
    assert metadata["size_bytes"] == 5
    assert is_sha256_hex(metadata["sha256"])


def test_result_envelope():
    payload = {"record_count": 1}

    result = result_envelope(
        experiment="example_validator_v0",
        status="PASS",
        payload=payload,
    )

    assert result["experiment"] == "example_validator_v0"
    assert result["status"] == "PASS"
    assert result["boundary"] == "measurement != inference != decision"
    assert result["payload"] == payload
    assert result["created_at_utc"].endswith("+00:00")