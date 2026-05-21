# OMNIA-VALIDATION

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
