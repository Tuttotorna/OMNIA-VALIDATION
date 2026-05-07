from pathlib import Path

import pytest

from omnia_validation.io import read_json
from omnia_validation.schemas import validate_result_envelope

ENVELOPED_RESULTS_DIR = Path("results_enveloped")


def enveloped_result_files() -> list[Path]:
    if not ENVELOPED_RESULTS_DIR.exists():
        return []

    return sorted(ENVELOPED_RESULTS_DIR.glob("*.json"))


@pytest.mark.parametrize("path", enveloped_result_files())
def test_enveloped_result_file_is_valid_envelope(path: Path):
    result = read_json(path)
    errors = validate_result_envelope(result)

    assert errors == []