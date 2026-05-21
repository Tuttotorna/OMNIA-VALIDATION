from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MBX01_LON_ECOSYSTEM_ENTRYPOINT.md"
README = ROOT / "README.md"


def test_mbx01_lon_entrypoint_doc_exists():
    assert DOC.exists()


def test_mbx01_lon_entrypoint_contains_identity_terms():
    text = DOC.read_text(encoding="utf-8")

    required_fragments = [
        "MB-X.01 / L.O.N. Ecosystem Entry Point",
        "MB-X.01",
        "Logical Origin Node",
        "L.O.N.",
        "root reference",
        "structural-validation ecosystem",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing


def test_mbx01_lon_entrypoint_contains_canonical_backbone():
    text = DOC.read_text(encoding="utf-8")

    required_fragments = [
        "OMNIA measurement",
        "BoundaryCertificate",
        "omnia-limit validate_certificate()",
        "OMNIA-VALIDATION ValidationEnvelope",
        "CI regression",
        "compliant producer / adapter / consumer / observer",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing


def test_mbx01_lon_entrypoint_contains_core_repositories():
    text = DOC.read_text(encoding="utf-8")

    required_repositories = [
        "OMNIA",
        "omnia-limit",
        "OMNIA-VALIDATION",
    ]

    missing = [repo for repo in required_repositories if repo not in text]
    assert not missing


def test_mbx01_lon_entrypoint_contains_compliant_satellites():
    text = DOC.read_text(encoding="utf-8")

    required_satellites = [
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

    missing = [repo for repo in required_satellites if repo not in text]
    assert not missing


def test_mbx01_lon_entrypoint_preserves_layer_separation_rules():
    text = DOC.read_text(encoding="utf-8")

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


def test_mbx01_lon_entrypoint_rejects_overclaiming():
    text = DOC.read_text(encoding="utf-8")

    required_boundaries = [
        "semantic truth",
        "final mathematical truth",
        "final physical truth",
        "absolute constancy",
        "security approval",
        "crypto correctness",
        "governance decisions",
        "consciousness",
        "agency",
        "meaning interpretation",
    ]

    missing = [boundary for boundary in required_boundaries if boundary not in text]
    assert not missing


def test_mbx01_lon_entrypoint_links_to_existing_public_docs_and_tests():
    text = DOC.read_text(encoding="utf-8")

    required_paths = [
        "docs/ECOSYSTEM_MAP.md",
        "docs/ECOSYSTEM_STATUS.md",
        "docs/ECOSYSTEM_BACKBONE_COMPLIANCE_REGISTRY.md",
        "docs/ecosystem_backbone_compliance_registry.json",
        "tests/test_end_to_end_backbone.py",
        "tests/test_ecosystem_backbone_compliance_registry.py",
        "tests/test_ecosystem_map_documentation.py",
        "tests/test_mbx01_lon_entrypoint_documentation.py",
    ]

    missing = [path for path in required_paths if path not in text]
    assert not missing


def test_readme_links_to_mbx01_lon_entrypoint():
    assert README.exists()

    text = README.read_text(encoding="utf-8")

    required_fragments = [
        "<!-- MB-X.01 LON ECOSYSTEM ENTRYPOINT:START -->",
        "<!-- MB-X.01 LON ECOSYSTEM ENTRYPOINT:END -->",
        "docs/MBX01_LON_ECOSYSTEM_ENTRYPOINT.md",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing
