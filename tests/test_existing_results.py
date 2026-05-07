from pathlib import Path

import pytest

from omnia_validation.io import read_json

RESULTS_DIR = Path("results")


def result_files() -> list[Path]:
    if not RESULTS_DIR.exists():
        return []

    return sorted(RESULTS_DIR.glob("*.json"))


@pytest.mark.parametrize("path", result_files())
def test_existing_result_file_is_valid_json(path: Path):
    data = read_json(path)

    assert isinstance(data, dict)