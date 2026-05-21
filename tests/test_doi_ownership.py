from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

README = ROOT / "README.md"
DOI_REGISTRY = ROOT / "docs" / "DOI_REGISTRY.md"
AUDIT_DOC = ROOT / "docs" / "DOI_OWNERSHIP_AUDIT.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"

REFERENCE_REPOSITORY = "Tuttotorna/OMNIA"
TARGET_REPOSITORY = "Tuttotorna/OMNIA-VALIDATION"
REFERENCE_DOI = "10.5281/zenodo.20322696"
BAD_DUPLICATE_DOI = "10.5281/zenodo.20322696"
EXPECTED_TARGET_DOI = "pending"

def extract_registry_value(text, key):
    pattern = rf"^{key}:\s*([^\n`]+)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None

def registry_repository_lines(text):
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith("repository:")
    ]

def test_doi_registry_exists():
    assert DOI_REGISTRY.exists()
    assert AUDIT_DOC.exists()

def test_omnia_validation_does_not_reuse_omnia_doi():
    text = DOI_REGISTRY.read_text(encoding="utf-8")
    release_doi = extract_registry_value(text, "release_doi")

    assert release_doi is not None
    assert release_doi != REFERENCE_DOI
    assert release_doi != BAD_DUPLICATE_DOI

def test_pending_or_exact_target_doi_is_explicit():
    text = DOI_REGISTRY.read_text(encoding="utf-8")
    release_doi = extract_registry_value(text, "release_doi")

    if EXPECTED_TARGET_DOI == "pending":
        assert release_doi == "pending"
        assert "pending strict Zenodo ownership verification" in README.read_text(encoding="utf-8")
    else:
        assert release_doi == EXPECTED_TARGET_DOI
        assert EXPECTED_TARGET_DOI in README.read_text(encoding="utf-8")

def test_ownership_rule_is_documented():
    required_fragments = [
        "repo_name substring match is forbidden for DOI ownership",
        "OMNIA != OMNIA-VALIDATION",
        "a DOI must bind to exact repository identity or remain pending",
        "DOI ownership != substring match",
    ]

    for path in [README, DOI_REGISTRY, AUDIT_DOC]:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        missing = [fragment for fragment in required_fragments if fragment not in text]
        assert not missing, f"{path} missing fragments: {missing}"

def test_registry_points_to_target_repository_only():
    text = DOI_REGISTRY.read_text(encoding="utf-8")
    lines = registry_repository_lines(text)

    assert f"repository: {TARGET_REPOSITORY}" in lines
    assert f"repository: {REFERENCE_REPOSITORY}" not in lines

def test_ci_runs_doi_ownership_test():
    assert CI.exists()
    assert "python -m pytest -q tests/test_doi_ownership.py" in CI.read_text(encoding="utf-8")
