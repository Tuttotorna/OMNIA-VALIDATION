from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

README = ROOT / "README.md"
ENTRYPOINT = ROOT / "docs" / "MBX01_LON_ECOSYSTEM_ENTRYPOINT.md"
REGISTRY_MD = ROOT / "docs" / "ECOSYSTEM_BACKBONE_COMPLIANCE_REGISTRY.md"
REGISTRY_JSON = ROOT / "docs" / "ecosystem_backbone_compliance_registry.json"
PUBLIC_LINK_DOC = ROOT / "docs" / "LON_MIRROR_ROOT_REFERENCE_PUBLIC_LINK.md"

LON_LINK = "https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md"
EXPECTED_COMMIT = "22a320d"


def test_lon_mirror_root_reference_public_link_doc_exists():
    assert PUBLIC_LINK_DOC.exists()


def test_lon_mirror_root_reference_public_link_doc_contains_required_fragments():
    text = PUBLIC_LINK_DOC.read_text(encoding="utf-8")

    required = [
        "lon-mirror Public Root Reference Link",
        LON_LINK,
        "root_reference_observer",
        "OMNIA measurement",
        "BoundaryCertificate",
        "omnia-limit validate_certificate()",
        "OMNIA-VALIDATION ValidationEnvelope",
        "measurement != validation",
        "validation != orchestration",
        "orchestration != decision",
        "decision != measurement",
        "observation != decision",
        "domain adaptation != backbone redefinition",
        "must not become a validator",
        "must not become a control plane",
        "must not become a governance engine",
        "must not become a decision engine",
        "must not become a semantic-truth engine",
    ]

    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_registry_json_records_lon_mirror_public_root_reference_link():
    data = json.loads(REGISTRY_JSON.read_text(encoding="utf-8"))

    matches = [
        entry for entry in data["repositories"]
        if entry.get("repository") == "lon-mirror"
    ]

    assert matches

    entry = matches[0]

    assert entry["role"] == "root_reference_observer"
    assert entry["status"] == "satellite_compliant"
    assert entry["public_root_reference_link"] == LON_LINK
    assert entry["commit"]
    assert entry["commit"].startswith(EXPECTED_COMMIT[:7])
    assert "semantic truth claim" in entry["forbidden"]
    assert "governance decision" in entry["forbidden"]


def test_registry_markdown_records_lon_mirror_public_root_reference_link():
    text = REGISTRY_MD.read_text(encoding="utf-8")

    required = [
        "<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:START -->",
        "<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:END -->",
        LON_LINK,
        "root_reference_observer",
        "satellite_compliant",
        EXPECTED_COMMIT[:7],
    ]

    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_entrypoint_records_lon_mirror_public_root_reference_link():
    text = ENTRYPOINT.read_text(encoding="utf-8")

    required = [
        "<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:START -->",
        "<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:END -->",
        LON_LINK,
        "root_reference_observer",
        EXPECTED_COMMIT[:7],
        "observation",
        "decision",
    ]

    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_readme_records_lon_mirror_public_root_reference_link():
    text = README.read_text(encoding="utf-8")

    required = [
        "<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:START -->",
        "<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:END -->",
        LON_LINK,
        "root_reference_observer",
        EXPECTED_COMMIT[:7],
    ]

    missing = [fragment for fragment in required if fragment not in text]
    assert not missing


def test_layer_separation_is_preserved_in_public_link_doc():
    text = PUBLIC_LINK_DOC.read_text(encoding="utf-8")

    assert "measurement != validation" in text
    assert "validation != orchestration" in text
    assert "orchestration != decision" in text
    assert "decision != measurement" in text
    assert "observation != decision" in text
    assert "domain adaptation != backbone redefinition" in text
