from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "MBX01_LON_FINAL_RELEASE_AUDIT.md"
README = ROOT / "README.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"

EXPECTED_MAPPING = [
    "Tuttotorna/lon-mirror -> 10.5281/zenodo.20322678",
    "Tuttotorna/OMNIABASE -> 10.5281/zenodo.20322682",
    "Tuttotorna/OMNIA -> 10.5281/zenodo.20322683",
    "Tuttotorna/omnia-limit -> 10.5281/zenodo.20322684",
    "Tuttotorna/OMNIA-RADAR -> 10.5281/zenodo.20322686",
    "Tuttotorna/OMNIA-SECURITY -> 10.5281/zenodo.20322688",
    "Tuttotorna/OMNIA-CRYPTO -> 10.5281/zenodo.20322691",
    "Tuttotorna/OMNIAMIND -> 10.5281/zenodo.20322692",
    "Tuttotorna/OMNIA-THREE-BODY -> 10.5281/zenodo.20322693",
    "Tuttotorna/OMNIA-INVARIANCE -> 10.5281/zenodo.20322694",
    "Tuttotorna/OMNIA-CONSTANT -> 10.5281/zenodo.20322695",
    "Tuttotorna/OMNIA-VALIDATION -> 10.5281/zenodo.20322696",
]

EXPECTED_DOIS = [
    "10.5281/zenodo.20322678",
    "10.5281/zenodo.20322682",
    "10.5281/zenodo.20322683",
    "10.5281/zenodo.20322684",
    "10.5281/zenodo.20322686",
    "10.5281/zenodo.20322688",
    "10.5281/zenodo.20322691",
    "10.5281/zenodo.20322692",
    "10.5281/zenodo.20322693",
    "10.5281/zenodo.20322694",
    "10.5281/zenodo.20322695",
    "10.5281/zenodo.20322696",
]

TEST_COMMAND = "python -m pytest -q tests/test_final_release_audit.py"


def test_final_release_audit_doc_exists():
    assert DOC.exists()


def test_final_release_audit_records_clean_status():
    text = DOC.read_text(encoding="utf-8")
    required = [
        "audit_status: clean",
        "repositories_audited: 12",
        "clean_repositories: 12",
        "repositories_with_issues: 0",
        "No duplicate DOI values detected.",
        "No duplicate GitHub repository ids detected.",
        "OMNIA and OMNIA-VALIDATION DOI ownership is separated correctly.",
        "Non-pair repositories are not forced to carry OMNIA/OMNIA-VALIDATION-specific ownership language.",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_final_release_audit_records_all_expected_dois():
    text = DOC.read_text(encoding="utf-8")
    missing_mapping = [fragment for fragment in EXPECTED_MAPPING if fragment not in text]
    assert not missing_mapping

    dois_seen = re.findall(r"10\.\d{4,9}/zenodo\.\d+", text)
    for doi in EXPECTED_DOIS:
        assert doi in dois_seen

    assert len(set(EXPECTED_DOIS)) == len(EXPECTED_DOIS)


def test_omnia_and_omnia_validation_are_separated():
    text = DOC.read_text(encoding="utf-8")
    required = [
        "Tuttotorna/OMNIA -> 10.5281/zenodo.20322683",
        "Tuttotorna/OMNIA-VALIDATION -> 10.5281/zenodo.20322696",
        "OMNIA != OMNIA-VALIDATION",
        "OMNIA DOI != OMNIA-VALIDATION DOI",
        "exact repository identity is required for DOI ownership",
        "repo_name substring match is forbidden for DOI ownership",
        "DOI ownership != substring match",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_boundary_is_preserved():
    text = DOC.read_text(encoding="utf-8")
    required = [
        "A DOI is not a measurement.",
        "A DOI is not validation.",
        "A DOI is not orchestration.",
        "A DOI is not a decision.",
        "measurement != validation",
        "validation != orchestration",
        "orchestration != decision",
        "decision != measurement",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_readme_links_final_audit_doc():
    text = README.read_text(encoding="utf-8")
    required = [
        "<!-- MB-X.01 LON FINAL RELEASE AUDIT:START -->",
        "<!-- MB-X.01 LON FINAL RELEASE AUDIT:END -->",
        "docs/MBX01_LON_FINAL_RELEASE_AUDIT.md",
        "Repositories audited: 12",
        "Clean repositories: 12",
        "Repositories with issues: 0",
        "No duplicate DOI values detected.",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_ci_runs_final_release_audit_test():
    assert CI.exists()
    assert TEST_COMMAND in CI.read_text(encoding="utf-8")
