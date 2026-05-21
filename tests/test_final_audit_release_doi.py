from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

README = ROOT / "README.md"
REGISTRY = ROOT / "docs" / "DOI_REGISTRY.md"
FINAL_AUDIT_DOC = ROOT / "docs" / "MBX01_LON_FINAL_RELEASE_AUDIT.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"

TEST_COMMAND = "python -m pytest -q tests/test_final_audit_release_doi.py"
EXPECTED_TAG = "v2026.05.22"
EXPECTED_COMMIT = "e98a397"
EXPECTED_DOI = "10.5281/zenodo.20325096"

def test_final_audit_release_files_exist():
    assert README.exists()
    assert REGISTRY.exists()
    assert FINAL_AUDIT_DOC.exists()

def test_final_audit_release_registry_is_bound():
    text = REGISTRY.read_text(encoding="utf-8")
    required = [
        "repository: Tuttotorna/OMNIA-VALIDATION",
        f"release_tag: {EXPECTED_TAG}",
        f"release_commit: {EXPECTED_COMMIT}",
        f"release_doi: {EXPECTED_DOI}",
        "release_role: final_ecosystem_audit_snapshot",
        "final_audit_doc: docs/MBX01_LON_FINAL_RELEASE_AUDIT.md",
        "repositories_audited: 12",
        "clean_repositories: 12",
        "repositories_with_issues: 0",
        "duplicate_doi_values: none",
        "duplicate_github_repository_ids: none",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing

def test_final_audit_doc_contains_release_binding():
    text = FINAL_AUDIT_DOC.read_text(encoding="utf-8")
    required = [
        "Final audit release DOI",
        f"release_tag: {EXPECTED_TAG}",
        f"release_commit: {EXPECTED_COMMIT}",
        f"release_doi: {EXPECTED_DOI}",
        "release_role: final_ecosystem_audit_snapshot",
        "final_audit_doc: docs/MBX01_LON_FINAL_RELEASE_AUDIT.md",
        "A DOI identifies an archived release snapshot.",
        "A DOI is not a measurement.",
        "A DOI is not validation.",
        "A DOI is not orchestration.",
        "A DOI is not a decision.",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing

def test_readme_contains_final_release_binding():
    text = README.read_text(encoding="utf-8")
    required = [
        "Final audit release DOI",
        f"release_tag: {EXPECTED_TAG}",
        f"release_commit: {EXPECTED_COMMIT}",
        EXPECTED_DOI,
        "release_role: final_ecosystem_audit_snapshot",
        "final_audit_doc: docs/MBX01_LON_FINAL_RELEASE_AUDIT.md",
        "repositories_audited: 12",
        "clean_repositories: 12",
        "repositories_with_issues: 0",
        "A DOI is not a measurement.",
        "A DOI is not validation.",
        "A DOI is not orchestration.",
        "A DOI is not a decision.",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing

def test_omnia_validation_doi_separation_is_preserved():
    text = REGISTRY.read_text(encoding="utf-8") + "\n" + FINAL_AUDIT_DOC.read_text(encoding="utf-8")
    required = [
        "OMNIA != OMNIA-VALIDATION",
        "OMNIA DOI != OMNIA-VALIDATION DOI",
        "exact repository identity is required for DOI ownership",
        "repo_name substring match is forbidden for DOI ownership",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing

def test_ci_runs_final_audit_release_doi_test():
    assert CI.exists()
    assert TEST_COMMAND in CI.read_text(encoding="utf-8")
