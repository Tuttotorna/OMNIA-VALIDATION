from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS_DOC = ROOT / "docs" / "ECOSYSTEM_STATUS.md"
README = ROOT / "README.md"
REGISTRY_JSON = ROOT / "docs" / "ecosystem_backbone_compliance_registry.json"


def test_ecosystem_status_doc_exists_and_names_canonical_chain():
    assert STATUS_DOC.exists()

    text = STATUS_DOC.read_text(encoding="utf-8")

    required_fragments = [
        "OMNIA Ecosystem Status",
        "OMNIA measurement",
        "BoundaryCertificate",
        "omnia-limit validate_certificate()",
        "OMNIA-VALIDATION ValidationEnvelope",
        "CI regression",
        "satellite compliant producer / adapter / consumer / observer",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing


def test_ecosystem_status_doc_preserves_layer_separation():
    text = STATUS_DOC.read_text(encoding="utf-8")

    required_rules = [
        "measurement != validation",
        "validation != orchestration",
        "orchestration != decision",
        "decision != measurement",
        "observation != decision",
        "domain adaptation != backbone redefinition",
    ]

    missing = [rule for rule in required_rules if rule not in text]
    assert not missing


def test_ecosystem_status_doc_lists_required_repositories():
    text = STATUS_DOC.read_text(encoding="utf-8")

    required_repositories = [
        "OMNIA",
        "omnia-limit",
        "OMNIA-VALIDATION",
        "OMNIAMIND",
        "OMNIA-RADAR",
        "OMNIA-INVARIANCE",
        "OMNIA-CRYPTO",
        "OMNIA-SECURITY",
        "OMNIA-CONSTANT",
        "OMNIA-THREE-BODY",
        "OMNIABASE",
        "lon-mirror",
    ]

    missing = [repo for repo in required_repositories if repo not in text]
    assert not missing


def test_readme_contains_public_backbone_status_section():
    assert README.exists()

    text = README.read_text(encoding="utf-8")

    required_fragments = [
        "<!-- OMNIA ECOSYSTEM BACKBONE STATUS:START -->",
        "<!-- OMNIA ECOSYSTEM BACKBONE STATUS:END -->",
        "Current ecosystem backbone status",
        "docs/ECOSYSTEM_STATUS.md",
        "docs/ecosystem_backbone_compliance_registry.json",
        "tests/test_ecosystem_backbone_compliance_registry.py",
        "tests/test_ecosystem_status_documentation.py",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing


def test_status_doc_and_registry_counts_are_consistent():
    import json

    assert REGISTRY_JSON.exists()

    data = json.loads(REGISTRY_JSON.read_text(encoding="utf-8"))
    text = STATUS_DOC.read_text(encoding="utf-8")

    assert f"total registered entries: {data['counts']['total_entries']}" in text
    assert f"backbone core entries:    {data['counts']['by_status'].get('backbone_core', 0)}" in text
    assert f"satellite compliant:      {data['counts']['by_status'].get('satellite_compliant', 0)}" in text
