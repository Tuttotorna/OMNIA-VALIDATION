from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

README = ROOT / "README.md"
REGISTRY = ROOT / "docs" / "DOI_REGISTRY.md"
FINAL_AUDIT_DOC = ROOT / "docs" / "MBX01_LON_FINAL_RELEASE_AUDIT.md"

THIS_REPOSITORY = "Tuttotorna/OMNIA-VALIDATION"
OMNIA_REPOSITORY = "Tuttotorna/OMNIA"
OMNIA_DOI = "10.5281/zenodo.20322683"
EXPECTED_RELEASE_TAG = "v2026.05.22"
EXPECTED_RELEASE_COMMIT = "e98a397"
EXPECTED_RELEASE_DOI = "10.5281/zenodo.20325096"

def extract_registry_value(text, key):
    match = re.search(rf"{key}:\s*([^\n`]+)", text)
    return match.group(1).strip() if match else None

def test_doi_registry_exists():
    assert REGISTRY.exists()

def test_registry_binds_current_final_audit_doi_to_exact_repository():
    text = REGISTRY.read_text(encoding="utf-8")
    assert f"repository: {THIS_REPOSITORY}" in text
    assert f"release_tag: {EXPECTED_RELEASE_TAG}" in text
    assert f"release_commit: {EXPECTED_RELEASE_COMMIT}" in text
    assert f"release_doi: {EXPECTED_RELEASE_DOI}" in text
    assert extract_registry_value(text, "release_doi") == EXPECTED_RELEASE_DOI

def test_omnia_validation_does_not_reuse_omnia_doi():
    text = REGISTRY.read_text(encoding="utf-8")
    release_doi = extract_registry_value(text, "release_doi")
    assert release_doi == EXPECTED_RELEASE_DOI
    assert release_doi != OMNIA_DOI

def test_ownership_rule_is_documented():
    combined = (
        README.read_text(encoding="utf-8")
        + "\n"
        + REGISTRY.read_text(encoding="utf-8")
        + "\n"
        + FINAL_AUDIT_DOC.read_text(encoding="utf-8")
    )
    required = [
        "OMNIA != OMNIA-VALIDATION",
        "OMNIA DOI != OMNIA-VALIDATION DOI",
        "exact repository identity is required for DOI ownership",
        "repo_name substring match is forbidden for DOI ownership",
    ]
    missing = [fragment for fragment in required if fragment not in combined]
    assert not missing

def test_release_role_is_final_ecosystem_audit_snapshot():
    text = REGISTRY.read_text(encoding="utf-8")
    assert "release_role: final_ecosystem_audit_snapshot" in text
    assert "final_audit_doc: docs/MBX01_LON_FINAL_RELEASE_AUDIT.md" in text
