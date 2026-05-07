from pathlib import Path

from omnia_validation.hashing import is_sha256_hex, sha256_file, sha256_text


def test_sha256_text_is_valid_sha256():
    digest = sha256_text("omnia")

    assert is_sha256_hex(digest)
    assert len(digest) == 64


def test_sha256_text_is_deterministic():
    assert sha256_text("omnia") == sha256_text("omnia")


def test_sha256_file(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("omnia", encoding="utf-8")

    assert sha256_file(file_path) == sha256_text("omnia")


def test_is_sha256_hex():
    assert is_sha256_hex("a" * 64)
    assert is_sha256_hex("A" * 64)
    assert not is_sha256_hex("a" * 63)
    assert not is_sha256_hex("g" * 64)