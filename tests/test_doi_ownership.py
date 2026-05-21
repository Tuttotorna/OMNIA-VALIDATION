from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

README = ROOT / "README.md"
DOI_REGISTRY = ROOT / "docs" / "DOI_REGISTRY.md"
AUDIT_DOC = ROOT / "docs" / "DOI_OWNERSHIP_AUDIT.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"

THIS_REPOSITORY = "Tuttotorna/OMNIA-VALIDATION"
OTHER_REPOSITORY = "Tuttotorna/OMNIA"
EXPECTED_DOI = "10.5281/zenodo.20322696"
OTHER_DOI = "10.5281/zenodo.20322683"
TEST_COMMAND = "python -m pytest -q tests/test_doi_ownership.py"


def extract_registry_value(text, key):
    pattern = rf"{key}:\s*([^\n`]+)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def test_doi_registry_and_audit_exist():
    assert DOI_REGISTRY.exists()
    assert AUDIT_DOC.exists()


def test_registry_binds_expected_doi_to_exact_repository():
    text = DOI_REGISTRY.read_text(encoding="utf-8")
    assert f"repository: {THIS_REPOSITORY}" in text
    assert f"release_doi: {EXPECTED_DOI}" in text
    assert f"this_repository: {THIS_REPOSITORY}" in text
    assert f"this_repository_doi: {EXPECTED_DOI}" in text
    assert f"other_repository: {OTHER_REPOSITORY}" in text
    assert f"other_repository_doi: {OTHER_DOI}" in text


def test_release_doi_is_not_other_repository_doi():
    text = DOI_REGISTRY.read_text(encoding="utf-8")
    release_doi = extract_registry_value(text, "release_doi")
    assert release_doi == EXPECTED_DOI
    assert release_doi != OTHER_DOI


def test_readme_contains_expected_doi_and_boundary():
    text = README.read_text(encoding="utf-8")
    required = [
        EXPECTED_DOI,
        "OMNIA != OMNIA-VALIDATION",
        "OMNIA DOI != OMNIA-VALIDATION DOI",
        "repo_name substring match is forbidden for DOI ownership",
        "exact repository identity is required for DOI ownership",
        "DOI ownership != substring match",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_audit_doc_contains_resolved_status():
    text = AUDIT_DOC.read_text(encoding="utf-8")
    required = [
        "audit_status: resolved",
        f"target_repository: {THIS_REPOSITORY}",
        f"resolved_target_doi: {EXPECTED_DOI}",
        "ownership_status: strict_exact_repository_match",
        "10.5281/zenodo.20322683",
        "10.5281/zenodo.20322696",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_ci_runs_doi_ownership_test():
    assert CI.exists()
    assert TEST_COMMAND in CI.read_text(encoding="utf-8")
