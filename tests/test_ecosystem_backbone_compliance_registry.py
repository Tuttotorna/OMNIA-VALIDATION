from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ECOSYSTEM_BACKBONE_COMPLIANCE_REGISTRY.md"
JSON_REGISTRY = ROOT / "docs" / "ecosystem_backbone_compliance_registry.json"


def test_ecosystem_backbone_registry_doc_exists():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")

    required_fragments = [
        "OMNIA Ecosystem Backbone Compliance Registry",
        "OMNIA measurement",
        "BoundaryCertificate",
        "omnia-limit validate_certificate()",
        "OMNIA-VALIDATION ValidationEnvelope",
        "measurement != validation",
        "validation != orchestration",
        "orchestration != decision",
        "decision != measurement",
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

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing


def test_ecosystem_backbone_registry_json_exists_and_has_required_repositories():
    assert JSON_REGISTRY.exists()
    data = json.loads(JSON_REGISTRY.read_text(encoding="utf-8"))

    assert data["registry_name"] == "OMNIA Ecosystem Backbone Compliance Registry"
    assert data["registry_owner"] == "OMNIA-VALIDATION"

    repositories = {entry["repository"] for entry in data["repositories"]}

    required_repositories = {
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
    }

    assert required_repositories.issubset(repositories)


def test_registry_preserves_layer_separation_rules():
    data = json.loads(JSON_REGISTRY.read_text(encoding="utf-8"))
    rules = set(data["non_equivalence_rules"])

    assert "measurement != validation" in rules
    assert "validation != orchestration" in rules
    assert "orchestration != decision" in rules
    assert "decision != measurement" in rules
    assert "observation != decision" in rules
    assert "domain adaptation != backbone redefinition" in rules


def test_no_satellite_is_marked_as_backbone_core():
    data = json.loads(JSON_REGISTRY.read_text(encoding="utf-8"))
    backbone_core_allowed = {"OMNIA", "omnia-limit", "OMNIA-VALIDATION"}

    for entry in data["repositories"]:
        if entry["status"] == "backbone_core":
            assert entry["repository"] in backbone_core_allowed


def test_every_entry_has_contract_role_and_forbidden_boundaries():
    data = json.loads(JSON_REGISTRY.read_text(encoding="utf-8"))

    for entry in data["repositories"]:
        assert entry["repository"]
        assert entry["role"]
        assert entry["status"] in {"backbone_core", "satellite_compliant"}
        assert entry["commit"]
        assert entry["responsibility"]
        assert isinstance(entry["forbidden"], list)
        assert entry["forbidden"]


def test_registry_counts_match_entries():
    data = json.loads(JSON_REGISTRY.read_text(encoding="utf-8"))
    entries = data["repositories"]
    counts = data["counts"]

    assert counts["total_entries"] == len(entries)

    expected_by_status = {}
    expected_by_role = {}

    for entry in entries:
        expected_by_status[entry["status"]] = expected_by_status.get(entry["status"], 0) + 1
        expected_by_role[entry["role"]] = expected_by_role.get(entry["role"], 0) + 1

    assert counts["by_status"] == expected_by_status
    assert counts["by_role"] == expected_by_role
