from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REGISTRY_JSON = ROOT / "docs" / "ecosystem_backbone_compliance_registry.json"
REGISTRY_MD = ROOT / "docs" / "ECOSYSTEM_BACKBONE_COMPLIANCE_REGISTRY.md"
DOC = ROOT / "docs" / "FIRST_READER_PATH_COMMITS.md"
FIRST_READER = ROOT / "docs" / "FIRST_READER_PATH.md"
ENTRYPOINT = ROOT / "docs" / "MBX01_LON_ECOSYSTEM_ENTRYPOINT.md"
MAP = ROOT / "docs" / "ECOSYSTEM_MAP.md"
STATUS = ROOT / "docs" / "ECOSYSTEM_STATUS.md"
README = ROOT / "README.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"

OMNIA_VALIDATION_FIRST_READER_COMMIT = "83fa07f"
LON_MIRROR_FIRST_READER_COMMIT = "4dd5cb5"
LON_MIRROR_ROOT_REFERENCE_COMMIT = "22a320d"
LON_MIRROR_PUBLIC_ENTRYPOINT_COMMIT = "f74b799"

OMNIA_VALIDATION_FIRST_READER_URL = "https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/FIRST_READER_PATH.md"
LON_MIRROR_FIRST_READER_URL = "https://github.com/Tuttotorna/lon-mirror/blob/main/docs/FIRST_READER_PATH.md"


def test_first_reader_path_commit_doc_exists():
    assert DOC.exists()


def test_first_reader_path_commit_doc_contains_required_fragments():
    text = DOC.read_text(encoding="utf-8")

    required_fragments = [
        "First Reader Path Commit Registration",
        OMNIA_VALIDATION_FIRST_READER_COMMIT,
        LON_MIRROR_FIRST_READER_COMMIT,
        LON_MIRROR_ROOT_REFERENCE_COMMIT,
        LON_MIRROR_PUBLIC_ENTRYPOINT_COMMIT,
        OMNIA_VALIDATION_FIRST_READER_URL,
        LON_MIRROR_FIRST_READER_URL,
        "latest_public_commit",
        "latest_first_reader_path_commit",
        "OMNIA measurement",
        "BoundaryCertificate",
        "omnia-limit validate_certificate()",
        "OMNIA-VALIDATION ValidationEnvelope",
        "measurement != validation",
        "validation != orchestration",
        "orchestration != decision",
        "decision != measurement",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing


def test_registry_json_records_first_reader_path_commits_without_breaking_public_entrypoint_commit():
    data = json.loads(REGISTRY_JSON.read_text(encoding="utf-8"))

    by_repo = {
        entry["repository"]: entry
        for entry in data["repositories"]
    }

    assert "OMNIA-VALIDATION" in by_repo
    assert "lon-mirror" in by_repo

    omnia_validation = by_repo["OMNIA-VALIDATION"]
    lon_mirror = by_repo["lon-mirror"]

    assert omnia_validation["first_reader_path_commit"] == OMNIA_VALIDATION_FIRST_READER_COMMIT
    assert omnia_validation["first_reader_path_link"] == OMNIA_VALIDATION_FIRST_READER_URL
    assert omnia_validation["latest_public_commit"] == OMNIA_VALIDATION_FIRST_READER_COMMIT

    assert lon_mirror["commit"] == LON_MIRROR_ROOT_REFERENCE_COMMIT
    assert lon_mirror["public_root_reference_commit"] == LON_MIRROR_ROOT_REFERENCE_COMMIT
    assert lon_mirror["public_entrypoint_commit"] == LON_MIRROR_PUBLIC_ENTRYPOINT_COMMIT
    assert lon_mirror["latest_public_commit"] == LON_MIRROR_PUBLIC_ENTRYPOINT_COMMIT
    assert lon_mirror["first_reader_path_commit"] == LON_MIRROR_FIRST_READER_COMMIT
    assert lon_mirror["first_reader_path_link"] == LON_MIRROR_FIRST_READER_URL
    assert lon_mirror["latest_first_reader_path_commit"] == LON_MIRROR_FIRST_READER_COMMIT


def test_registry_counts_still_match_entries():
    data = json.loads(REGISTRY_JSON.read_text(encoding="utf-8"))
    entries = data["repositories"]
    counts = data["counts"]

    expected_by_status = {}
    expected_by_role = {}

    for entry in entries:
        expected_by_status[entry["status"]] = expected_by_status.get(entry["status"], 0) + 1
        expected_by_role[entry["role"]] = expected_by_role.get(entry["role"], 0) + 1

    assert counts["total_entries"] == len(entries)
    assert counts["by_status"] == expected_by_status
    assert counts["by_role"] == expected_by_role


def test_public_docs_link_to_first_reader_path_commits():
    files = [
        REGISTRY_MD,
        FIRST_READER,
        ENTRYPOINT,
        MAP,
        STATUS,
        README,
    ]

    for path in files:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert OMNIA_VALIDATION_FIRST_READER_COMMIT in text
        assert LON_MIRROR_FIRST_READER_COMMIT in text
        assert OMNIA_VALIDATION_FIRST_READER_URL in text
        assert LON_MIRROR_FIRST_READER_URL in text


def test_ci_runs_first_reader_path_commit_registration_test():
    assert CI.exists()
    text = CI.read_text(encoding="utf-8")
    assert "python -m pytest -q tests/test_first_reader_path_commit_registration.py" in text


def test_first_reader_path_boundary_is_preserved():
    text = DOC.read_text(encoding="utf-8")

    required_boundaries = [
        "first-reader path != validation",
        "first-reader path != measurement",
        "first-reader path != orchestration",
        "first-reader path != decision",
        "It does not validate.",
        "It does not measure.",
        "It does not orchestrate.",
        "It does not decide.",
        "It does not emit semantic truth.",
    ]

    missing = [boundary for boundary in required_boundaries if boundary not in text]
    assert not missing
