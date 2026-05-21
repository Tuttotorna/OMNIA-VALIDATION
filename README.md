# OMNIA-VALIDATION

<!-- ZENODO DOI:START -->

## DOI

[![DOI](https://zenodo.org/badge/1227176782.svg)](https://zenodo.org/badge/latestdoi/1227176782)

Zenodo DOI badge for this repository.

Repository: Tuttotorna/OMNIA-VALIDATION
GitHub repository id: 1227176782
Latest release DOI: pending Zenodo publication or resolved dynamically by Zenodo badge

<!-- ZENODO DOI:END -->


## DOI

[![DOI](https://zenodo.org/badge/1227176782.svg)](https://zenodo.org/badge/latestdoi/1227176782)

Release DOI: [10.5281/zenodo.20083830](https://doi.org/10.5281/zenodo.20083830)

GitHub release: [OMNIA-VALIDATION v1.0.0 release](https://github.com/Tuttotorna/OMNIA-VALIDATION/releases/tag/v1.0.0)

## Start here

From a clean environment:

    git clone [OMNIA-VALIDATION.git](https://github.com/Tuttotorna/OMNIA-VALIDATION.git)
    cd OMNIA-VALIDATION
    python -m pip install -e .
    pytest

If the repository has optional example runners, run them after tests pass.

The point is not to believe the framework.

The point is to inspect the artifacts.

---

## What this repository is

OMNIA-VALIDATION is the evidence layer of MB-X.01 / OMNIA.

It should contain:

- reproducible validation cases;
- regression tests;
- artifact contracts;
- failure examples;
- public reports;
- boundary documents;
- minimal commands that reviewers can run without understanding the whole ecosystem.

The public path is:

    run tests -> inspect artifacts -> read reports -> trace claims

---

## What this repository is not

OMNIA-VALIDATION does not:

- infer semantic truth;
- decide whether a system is correct;
- replace external judgment;
- prove consciousness;
- perform security scanning;
- perform cryptographic attacks;
- recover keys;
- turn structural measurements into final decisions.

It validates artifacts and claims inside a declared boundary.

---

## Showroom principle

A validation repository must not read like a manifesto.

It must behave like a showroom.

A first-time visitor should see:

    one command
    one artifact
    one failure mode
    one report
    one boundary

The correct public demonstration is:

    surface correctness can pass
    structural stability can fail
    the failure must be inspectable

---

## Minimal validation shape

Every validation case should ideally expose:

| Field | Meaning |
|---|---|
| input | What was measured |
| transformation | What changed |
| expected boundary | What should remain stable or admissible |
| measured output | What OMNIA or related tools produced |
| artifact | Where the result is stored |
| result | pass / flag / fail / inconclusive |
| rationale | Why this result matters structurally |
| limitation | What the result does not prove |

---

## Recommended reading order

1. [docs/SHOWROOM.md](docs/SHOWROOM.md)
2. [docs/VALIDATION_PROTOCOL.md](docs/VALIDATION_PROTOCOL.md)
3. [docs/ARTIFACT_CONTRACT.md](docs/ARTIFACT_CONTRACT.md)
4. [docs/FAILURE_EXAMPLES.md](docs/FAILURE_EXAMPLES.md)
5. [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md)
6. [docs/BOUNDARY.md](docs/BOUNDARY.md)

---

## Ecosystem entry point

For the full ecosystem map, start here:

[lon-mirror](https://github.com/Tuttotorna/lon-mirror)

---

## Related repositories

| Repository | Role |
|---|---|
| [lon-mirror](https://github.com/Tuttotorna/lon-mirror) | Canonical public entry point |
| [OMNIA-VALIDATION](https://github.com/Tuttotorna/OMNIA-VALIDATION) | Public validation showroom |
| [OMNIA](https://github.com/Tuttotorna/OMNIA) | Core structural measurement engine |
| [OMNIABASE](https://github.com/Tuttotorna/OMNIABASE) | Representation invariance foundation |
| [omnia-limit](https://github.com/Tuttotorna/omnia-limit) | Stop / continue boundary layer |
| [OMNIA-RADAR](https://github.com/Tuttotorna/OMNIA-RADAR) | Structural signal detection layer |
| [OMNIA-INVARIANCE](https://github.com/Tuttotorna/OMNIA-INVARIANCE) | Structural invariance layer |
| [OMNIA-CONSTANT](https://github.com/Tuttotorna/OMNIA-CONSTANT) | Structural constant candidate layer |
| [OMNIAMIND](https://github.com/Tuttotorna/OMNIAMIND) | Structural cognition orchestration layer |
| [OMNIA-THREE-BODY](https://github.com/Tuttotorna/OMNIA-THREE-BODY) | Dynamic divergence stress test |
| [OMNIA-SECURITY](https://github.com/Tuttotorna/OMNIA-SECURITY) | Bounded structural security diagnostics |
| [OMNIA-CRYPTO](https://github.com/Tuttotorna/OMNIA-CRYPTO) | Bounded structural crypto diagnostics |

---

## Boundary and smoke-test required terms

    measurement != inference != decision
    test -> output -> artifact -> failure/fragility -> report

---

## License

MIT.

<!-- OMNIA ECOSYSTEM BACKBONE STATUS:START -->
## Current ecosystem backbone status

OMNIA-VALIDATION is the control-plane registry for the current OMNIA ecosystem backbone.

```text
OMNIA measurement
  -> BoundaryCertificate
  -> omnia-limit validate_certificate()
  -> OMNIA-VALIDATION ValidationEnvelope
  -> CI regression
  -> satellite compliant producer / adapter / consumer / observer
```

Current registry state:

```text
total registered entries: 14
backbone core entries:    5
satellite compliant:      9
```

Protected separation rules:

```text
measurement != validation
validation != orchestration
orchestration != decision
decision != measurement
observation != decision
domain adaptation != backbone redefinition
```

Public status document:

```text
docs/ECOSYSTEM_STATUS.md
```

Executable registry:

```text
docs/ecosystem_backbone_compliance_registry.json
```

Registry tests:

```text
tests/test_ecosystem_backbone_compliance_registry.py
tests/test_ecosystem_status_documentation.py
```

<!-- OMNIA ECOSYSTEM BACKBONE STATUS:END -->

<!-- OMNIA ECOSYSTEM MAP:START -->
## Ecosystem map

For a fast public overview of the full OMNIA ecosystem, start here:

- [OMNIA Ecosystem Map](docs/ECOSYSTEM_MAP.md)

This map explains the canonical backbone, the core repositories, the compliant satellites, and the role-separation rules that prevent layer collapse.

<!-- OMNIA ECOSYSTEM MAP:END -->

<!-- MB-X.01 LON ECOSYSTEM ENTRYPOINT:START -->
## MB-X.01 / L.O.N. ecosystem entry point

For a first public orientation to the full MB-X.01 / Logical Origin Node ecosystem, start here:

- [MB-X.01 / L.O.N. Ecosystem Entry Point](docs/MBX01_LON_ECOSYSTEM_ENTRYPOINT.md)

This entry point explains the ecosystem identity, the canonical backbone, the core repositories, the compliant satellites, and the strict role-separation rule:

    measurement != validation != orchestration != decision
<!-- MB-X.01 LON ECOSYSTEM ENTRYPOINT:END -->

<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:START -->
## lon-mirror root reference link

The public root reference side of the MB-X.01 / L.O.N. ecosystem is exposed by lon-mirror:

https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

Verified lon-mirror commit:

22a320d

Role:

root_reference_observer

Boundary:

observation != decision
<!-- LON-MIRROR PUBLIC ROOT REFERENCE LINK:END -->

<!-- LON-MIRROR PUBLIC ENTRYPOINT REGISTRATION:START -->
## lon-mirror public entry point

The `lon-mirror` root reference observer now exposes a public entry point.

registry_commit: 22a320d
public_entrypoint_commit: f74b799
public_entrypoint_link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/PUBLIC_ENTRYPOINT.md
root_reference_link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/MBX01_LON_ROOT_REFERENCE_LINK.md

This closes the public path from `OMNIA-VALIDATION` to the `lon-mirror` first-reader doorway while preserving the boundary:

measurement != validation != orchestration != decision
<!-- LON-MIRROR PUBLIC ENTRYPOINT REGISTRATION:END -->

<!-- FIRST READER PATH:START -->
## First reader path

For a non-technical first orientation, start here:

- First reader path: docs/FIRST_READER_PATH.md
- First reader path URL: https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/FIRST_READER_PATH.md
- lon-mirror public entry point: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/PUBLIC_ENTRYPOINT.md

Thirty-second model:

OMNIA measures.
omnia-limit validates the boundary certificate.
OMNIA-VALIDATION validates the control-plane envelope.
OMNIAMIND orchestrates.
Satellites adapt, observe, or consume.
lon-mirror acts as root reference observer.

Boundary:

measurement != validation != orchestration != decision

Patch anchors:

OMNIA-VALIDATION commit: 2e7e63c
lon-mirror commit: f74b799
<!-- FIRST READER PATH:END -->

<!-- FIRST READER PATH COMMIT REGISTRATION:START -->
## First reader path commits

The public first-reader path commits are now registered.

OMNIA-VALIDATION:
  first_reader_path_commit: 83fa07f
  first_reader_path_link: https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/FIRST_READER_PATH.md

lon-mirror:
  first_reader_path_commit: 4dd5cb5
  first_reader_path_link: https://github.com/Tuttotorna/lon-mirror/blob/main/docs/FIRST_READER_PATH.md
  public_entrypoint_commit: f74b799
  latest_public_commit: f74b799

Boundary:
  first-reader path != validation
  first-reader path != measurement
  first-reader path != orchestration
  first-reader path != decision
<!-- FIRST READER PATH COMMIT REGISTRATION:END -->

<!-- REGISTRY ANCHOR ROLE SEPARATION:START -->
## Registry anchor role separation

OMNIA-VALIDATION now protects the distinction between commit identity and registry role identity.

    Commit equality is not role equality.
    Commit divergence is optional.
    Role divergence is mandatory.

Role policy document:

    https://github.com/Tuttotorna/OMNIA-VALIDATION/blob/main/docs/REGISTRY_ANCHOR_ROLE_SEPARATION.md

Protected role anchors:

    OMNIA-VALIDATION registry_role: validator_backbone_core
    OMNIA-VALIDATION first_reader_path_role: first_reader_surface
    lon-mirror registry_role: root_reference_observer
    lon-mirror first_reader_path_role: first_reader_surface

Boundary:

    registry topology != BoundaryCertificate
    first-reader path != validation
    first-reader path != measurement
    first-reader path != orchestration
    first-reader path != decision
<!-- REGISTRY ANCHOR ROLE SEPARATION:END -->
