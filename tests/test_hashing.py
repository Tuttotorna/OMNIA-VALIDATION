from pathlib import Path

from omnia_validation.hashing import is_sha256_hex, sha256_file, sha256_text


def test_sha256_text_known_value():
    assert (
        sha256_text("omnia")
        == "dbdbad7d872b8f534753c9ae1b8d19b0af5c3978ec507d5893f675c2f37adf4e"
    )


def test_sha256_file(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("omnia", encoding="utf-8")

    assert sha256_file(file_path) == sha256_text("omnia")


def test_is_sha256_hex():
    assert is_sha256_hex("a" * 64)
    assert is_sha256_hex("A" * 64)
    assert not is_sha256_hex("a" * 63)
    assert not is_sha256_hex("g" * 64)