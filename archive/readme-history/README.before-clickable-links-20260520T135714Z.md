# OMNIA-VALIDATION

## DOI

[![DOI](https://zenodo.org/badge/1227176782.svg)](https://zenodo.org/badge/latestdoi/1227176782)

Release DOI:

    10.5281/zenodo.20083830

Zenodo latest DOI link:

    https://doi.org/10.5281/zenodo.20083830

GitHub release:

    https://github.com/Tuttotorna/OMNIA-VALIDATION/releases/tag/v1.0.0

**Public validation showroom for the OMNIA ecosystem.**

This repository exists for one purpose:

    make OMNIA claims testable, inspectable, reproducible, and falsifiable.

It is not the theory hub.

It is not the core measurement engine.

It is not the decision layer.

It is the place where a visitor should be able to see:

    test -> output -> artifact -> failure/fragility -> report

Canonical boundary:

    measurement != inference != decision

---

## Start here

From a clean environment:

    git clone https://github.com/Tuttotorna/OMNIA-VALIDATION.git
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

## Related repositories

| Repository | Role |
|---|---|
| [lon-mirror](https://github.com/Tuttotorna/lon-mirror) | Canonical ecosystem entry point |
| [OMNIA](https://github.com/Tuttotorna/OMNIA) | Core structural measurement engine |
| [OMNIABASE](https://github.com/Tuttotorna/OMNIABASE) | Multi-representation foundation |
| [OMNIA-RADAR](https://github.com/Tuttotorna/OMNIA-RADAR) | Structural signal detection layer |
| [OMNIA-INVARIANCE](https://github.com/Tuttotorna/OMNIA-INVARIANCE) | Transformation and invariance layer |
| [omnia-limit](https://github.com/Tuttotorna/omnia-limit) | Stop / continue boundary layer |
| [OMNIA-CONSTANT](https://github.com/Tuttotorna/OMNIA-CONSTANT) | Stable-region falsification layer |

---

## Ecosystem entry point

For the full ecosystem map, start here:

    https://github.com/Tuttotorna/lon-mirror

---

## License

MIT.

