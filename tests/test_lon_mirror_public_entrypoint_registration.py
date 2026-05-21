from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REGISTRY_JSON = ROOT / "docs" / "ecosystem_backbone_compliance_registry.json"
REGISTRY_MD = ROOT / "docs" / "ECOSYSTEM_BACKBONE_COMPLIANCE_REGISTRY.md"
DOC = ROOT / "docs" / "LON_MIRROR_PUBLIC_ENTRYPOINT_LINK.md"
ENTRYPOINT = ROOT / "docs" / "MBX01_LON_ECOSYSTEM_ENTRYPOINT.md"
MAP = ROOT / "docs" / "ECOSYSTEM_MAP.md"
STATUS = ROOT / "docs" / "ECOSYSTEM_STATUS.md"
README = ROOT / "README.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"

PUBLIC_ENTRYPOINT_URL = "https://github.com/Tuttotorna/lon-mirror/blob/main/docs/PUBLIC_ENTRYPOINT.md"
ROOT_REFERENCE_URL = "https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md"
EXPECTED_PUBLIC_COMMIT = "f74b799"
EXPECTED_ROOT_REFERENCE_COMMIT = "22a320d"


def test_lon_mirror_public_entrypoint_doc_exists():
    assert DOC.exists()


def test_lon_mirror_public_entrypoint_doc_contains_required_fragments():
    text = DOC.read_text(encoding="utf-8")
    required_fragments = [
        "lon-mirror Public Entry Point Registration",
        "root_reference_observer",
        "satellite_compliant",
        EXPECTED_PUBLIC_COMMIT,
        EXPECTED_ROOT_REFERENCE_COMMIT,
        PUBLIC_ENTRYPOINT_URL,
        ROOT_REFERENCE_URL,
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


def test_registry_json_records_lon_mirror_public_entrypoint_without_breaking_root_reference_commit():
    data = json.loads(REGISTRY_JSON.read_text(encoding="utf-8"))
    matches = [
        entry
        for entry in data["repositories"]
        if entry.get("repository") == "lon-mirror"
    ]
    assert len(matches) == 1
    entry = matches[0]
    assert entry["commit"] == EXPECTED_ROOT_REFERENCE_COMMIT
    assert entry["commit"].startswith(EXPECTED_ROOT_REFERENCE_COMMIT[:7])
    assert entry["role"] == "root_reference_observer"
    assert entry["status"] == "satellite_compliant"
    assert entry["public_entrypoint_commit"] == EXPECTED_PUBLIC_COMMIT
    assert entry["public_entrypoint_link"] == PUBLIC_ENTRYPOINT_URL
    assert entry["public_root_reference_commit"] == EXPECTED_ROOT_REFERENCE_COMMIT
    assert entry["public_root_reference_link"] == ROOT_REFERENCE_URL
    assert entry["latest_public_commit"] == EXPECTED_PUBLIC_COMMIT


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


def test_public_entrypoint_backlinks_exist_in_public_docs():
    files = [
        REGISTRY_MD,
        ENTRYPOINT,
        MAP,
        STATUS,
        README,
    ]
    for path in files:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert PUBLIC_ENTRYPOINT_URL in text
        assert ROOT_REFERENCE_URL in text
        assert EXPECTED_PUBLIC_COMMIT in text
        assert EXPECTED_ROOT_REFERENCE_COMMIT in text


def test_registry_markdown_contains_public_entrypoint_registration():
    text = REGISTRY_MD.read_text(encoding="utf-8")
    required_fragments = [
        "lon-mirror public entry point registration",
        EXPECTED_PUBLIC_COMMIT,
        EXPECTED_ROOT_REFERENCE_COMMIT,
        PUBLIC_ENTRYPOINT_URL,
        ROOT_REFERENCE_URL,
        "root_reference_observer",
        "satellite_compliant",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing


def test_ci_runs_lon_mirror_public_entrypoint_registration_test():
    assert CI.exists()
    text = CI.read_text(encoding="utf-8")
    assert "python -m pytest -q tests/test_lon_mirror_public_entrypoint_registration.py" in text
