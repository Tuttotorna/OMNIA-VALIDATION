from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ECOSYSTEM_MAP.md"
README = ROOT / "README.md"


def test_ecosystem_map_doc_exists():
    assert DOC.exists()


def test_ecosystem_map_contains_canonical_backbone():
    text = DOC.read_text(encoding="utf-8")

    required_fragments = [
        "OMNIA Ecosystem Map",
        "OMNIA measurement",
        "BoundaryCertificate",
        "omnia-limit validate_certificate()",
        "OMNIA-VALIDATION ValidationEnvelope",
        "CI regression",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing


def test_ecosystem_map_contains_core_repositories():
    text = DOC.read_text(encoding="utf-8")

    required_repositories = [
        "OMNIA",
        "omnia-limit",
        "OMNIA-VALIDATION",
    ]

    missing = [repo for repo in required_repositories if repo not in text]
    assert not missing


def test_ecosystem_map_contains_compliant_satellites():
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


def test_ecosystem_map_preserves_layer_separation_rules():
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


def test_ecosystem_map_rejects_overclaiming():
    text = DOC.read_text(encoding="utf-8")

    required_boundaries = [
        "semantic truth",
        "final mathematical truth",
        "final physical truth",
        "absolute constancy",
        "security approval",
        "governance decisions",
        "consciousness",
        "agency",
        "meaning interpretation",
    ]

    missing = [boundary for boundary in required_boundaries if boundary not in text]
    assert not missing


def test_readme_links_to_ecosystem_map():
    assert README.exists()

    text = README.read_text(encoding="utf-8")

    required_fragments = [
        "<!-- OMNIA ECOSYSTEM MAP:START -->",
        "<!-- OMNIA ECOSYSTEM MAP:END -->",
        "docs/ECOSYSTEM_MAP.md",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing
