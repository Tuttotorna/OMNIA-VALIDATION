from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REGISTRY_JSON = ROOT / "docs" / "ecosystem_backbone_compliance_registry.json"
DOC = ROOT / "docs" / "REGISTRY_ANCHOR_ROLE_SEPARATION.md"
REGISTRY_MD = ROOT / "docs" / "ECOSYSTEM_BACKBONE_COMPLIANCE_REGISTRY.md"
ENTRYPOINT = ROOT / "docs" / "MBX01_LON_ECOSYSTEM_ENTRYPOINT.md"
MAP = ROOT / "docs" / "ECOSYSTEM_MAP.md"
STATUS = ROOT / "docs" / "ECOSYSTEM_STATUS.md"
FIRST_READER_COMMITS = ROOT / "docs" / "FIRST_READER_PATH_COMMITS.md"
FIRST_READER_PATH = ROOT / "docs" / "FIRST_READER_PATH.md"
README = ROOT / "README.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"

OMNIA_VALIDATION_CONTROL_PLANE_COMMIT = "60e4385"
OMNIA_VALIDATION_PUBLIC_COMMIT = "83fa07f"
OMNIA_VALIDATION_FIRST_READER_COMMIT = "83fa07f"

LON_MIRROR_ROOT_REFERENCE_COMMIT = "22a320d"
LON_MIRROR_PUBLIC_ENTRYPOINT_COMMIT = "f74b799"
LON_MIRROR_FIRST_READER_COMMIT = "4dd5cb5"

ROLE_POLICY = "commit_equality_allowed_role_divergence_required"


def load_registry():
    assert REGISTRY_JSON.exists()
    return json.loads(REGISTRY_JSON.read_text(encoding="utf-8"))


def by_repository():
    data = load_registry()
    return {
        entry["repository"]: entry
        for entry in data["repositories"]
    }


def test_registry_anchor_role_separation_doc_exists():
    assert DOC.exists()


def test_registry_anchor_role_separation_doc_contains_axioms():
    text = DOC.read_text(encoding="utf-8")

    required_fragments = [
        "Registry Anchor Role Separation",
        "Commit equality is not role equality.",
        "Commit divergence is optional.",
        "Role divergence is mandatory.",
        "A commit hash is not a role.",
        "A registry field is not a certificate.",
        "A public anchor is not a first-reader anchor.",
        "A first-reader anchor is not a validation anchor.",
        "A validation anchor is not a measurement anchor.",
        "registry topology != BoundaryCertificate",
        "commit identity != role identity",
        "first-reader path != validation",
        "first-reader path != measurement",
        "first-reader path != orchestration",
        "first-reader path != decision",
    ]

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing


def test_omnia_validation_registry_anchor_roles_are_separated():
    entries = by_repository()
    assert "OMNIA-VALIDATION" in entries

    entry = entries["OMNIA-VALIDATION"]

    assert entry["registry_control_plane_commit"] == OMNIA_VALIDATION_CONTROL_PLANE_COMMIT
    assert entry["latest_public_commit"] == OMNIA_VALIDATION_PUBLIC_COMMIT
    assert entry["first_reader_path_commit"] == OMNIA_VALIDATION_FIRST_READER_COMMIT
    assert entry["latest_first_reader_path_commit"] == OMNIA_VALIDATION_FIRST_READER_COMMIT
    assert entry["registry_role"] == "validator_backbone_core"
    assert entry["first_reader_path_role"] == "first_reader_surface"
    assert entry["public_anchor_role"] == "public_documentation_surface"
    assert entry["anchor_role_policy"] == ROLE_POLICY

    assert entry["registry_role"] != entry["first_reader_path_role"]

    if entry["latest_public_commit"] == entry["first_reader_path_commit"]:
        assert entry["registry_role"] != entry["first_reader_path_role"]


def test_lon_mirror_registry_anchor_roles_are_separated_without_breaking_previous_contracts():
    entries = by_repository()
    assert "lon-mirror" in entries

    entry = entries["lon-mirror"]

    assert entry["commit"] == LON_MIRROR_ROOT_REFERENCE_COMMIT
    assert entry["public_root_reference_commit"] == LON_MIRROR_ROOT_REFERENCE_COMMIT
    assert entry["public_entrypoint_commit"] == LON_MIRROR_PUBLIC_ENTRYPOINT_COMMIT
    assert entry["latest_public_commit"] == LON_MIRROR_PUBLIC_ENTRYPOINT_COMMIT
    assert entry["first_reader_path_commit"] == LON_MIRROR_FIRST_READER_COMMIT
    assert entry["latest_first_reader_path_commit"] == LON_MIRROR_FIRST_READER_COMMIT

    assert entry["registry_role"] == "root_reference_observer"
    assert entry["first_reader_path_role"] == "first_reader_surface"
    assert entry["public_anchor_role"] == "public_entrypoint_surface"
    assert entry["anchor_role_policy"] == ROLE_POLICY

    assert entry["registry_role"] != entry["first_reader_path_role"]


def test_first_reader_enabled_entries_have_role_policy():
    data = load_registry()

    for entry in data["repositories"]:
        if "first_reader_path_commit" not in entry:
            continue

        repo = entry["repository"]

        assert "first_reader_path_role" in entry, f"Missing first_reader_path_role in {repo}"
        assert "anchor_role_policy" in entry, f"Missing anchor_role_policy in {repo}"
        assert entry["anchor_role_policy"] == ROLE_POLICY, f"Bad anchor_role_policy in {repo}"

        if "registry_role" in entry:
            assert entry["registry_role"] != entry["first_reader_path_role"], f"Role collapse in {repo}"


def test_registry_role_separation_is_documented_in_public_docs():
    required_files = [
        REGISTRY_MD,
        ENTRYPOINT,
        MAP,
        STATUS,
        FIRST_READER_COMMITS,
        FIRST_READER_PATH,
        README,
    ]

    required_fragments = [
        "Commit equality is not role equality.",
        "Commit divergence is optional.",
        "Role divergence is mandatory.",
        "first-reader path != validation",
        "first-reader path != measurement",
        "first-reader path != orchestration",
        "first-reader path != decision",
        "https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/REGISTRY_ANCHOR_ROLE_SEPARATION.md",
    ]

    for path in required_files:
        assert path.exists(), f"Missing required public doc: {path}"
        text = path.read_text(encoding="utf-8")
        missing = [fragment for fragment in required_fragments if fragment not in text]
        assert not missing, f"{path} missing fragments: {missing}"


def test_ci_runs_registry_anchor_role_separation_test():
    assert CI.exists()
    text = CI.read_text(encoding="utf-8")
    assert "python -m pytest -q tests/test_registry_anchor_role_separation.py" in text
