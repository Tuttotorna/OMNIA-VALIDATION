<!-- OMNIA_VALIDATION_RUNNER_TOP_START -->

# OMNIA-VALIDATION

## Concrete entrypoint: OMNIA Validation Runner

This repository now has a direct operational tool:

    python -m omnia_validation_runner.cli --input examples/sample_validation_cases.jsonl --out-dir report

It solves a concrete problem:

    given validation cases with expected outputs and observed outputs,
    produce a reproducible validation report,
    detect mismatches and silent failures,
    write JSON/CSV/HTML outputs,
    and optionally fail CI when the validation boundary is crossed.

In short:

    validation cases -> measurement -> report -> CI gate

## What problem does it solve?

AI validation often fails because results are scattered across logs, notebooks, screenshots, or informal notes.

This tool turns validation into a reproducible operation.

It answers:

    How many cases were evaluated?
    Which cases passed?
    Which cases failed?
    Which cases look correct on the surface but violate the expected answer?
    Which cases are silent failures?
    Which suite should block deployment?

The rest of this repository explains the OMNIA validation path.

The runner is the practical entrypoint.

## Install

Clone the repository:

    git clone https://github.com/Tuttotorna/OMNIA-VALIDATION.git
    cd OMNIA-VALIDATION

Install locally:

    pip install -e .

The runner only uses the Python standard library.

## Run

Run the sample validation suite:

    python -m omnia_validation_runner.cli --input examples/sample_validation_cases.jsonl --out-dir report

Run and fail if any failed case exists:

    python -m omnia_validation_runner.cli --input examples/sample_validation_cases.jsonl --out-dir report --fail-on-failed

Run and fail only on silent failures:

    python -m omnia_validation_runner.cli --input examples/sample_validation_cases.jsonl --out-dir report --fail-on-silent-failure

## Input format

The runner accepts JSONL.

Required fields:

    case_id
    expected
    observed

Optional fields:

    suite
    input
    surface_status
    notes

Example:

    {"case_id":"math_001","suite":"demo","input":"2+2","expected":"4","observed":"4","surface_status":"ok"}
    {"case_id":"math_002","suite":"demo","input":"2+3","expected":"5","observed":"6","surface_status":"ok"}

## Output

The runner writes:

    report.json
    report.csv
    report.html
    failures.jsonl
    silent_failures.jsonl
    certificate.json

Meaning:

    report.json
    Full structured validation result.

    report.csv
    Spreadsheet-friendly case summary.

    report.html
    Human-readable validation report.

    failures.jsonl
    One JSON object per failed case.

    silent_failures.jsonl
    One JSON object per silent failure case.

    certificate.json
    Reproducibility certificate with aggregate metrics.

## CI gate

The runner can fail automatically:

    python -m omnia_validation_runner.cli --input examples/sample_validation_cases.jsonl --out-dir report --fail-on-failed

Exit codes:

    0 = validation completed, no blocking condition
    2 = failed cases detected
    3 = silent failures detected

## What this is not

This is not a model.

It does not generate answers.

It does not decide truth.

It does not replace human review.

It provides one concrete, reproducible operation:

    read validation cases
    compare expected vs observed
    detect failures and silent failures
    produce reports
    optionally fail CI

## Why the rest of the repository still matters

The rest of the repository documents the validation logic, protocols, examples, and research path.

The code above is the entrypoint.

The repository below is the derivation path.

<!-- OMNIA_VALIDATION_RUNNER_TOP_END -->

---

<!-- DOI OWNERSHIP AUDIT:START -->

## DOI ownership audit

This repository uses strict DOI ownership by exact repository identity.

OMNIA != OMNIA-VALIDATION
OMNIA DOI != OMNIA-VALIDATION DOI
repo_name substring match is forbidden for DOI ownership
exact repository identity is required for DOI ownership
this_repository: Tuttotorna/OMNIA-VALIDATION
this_repository_doi: 10.5281/zenodo.20322696
other_repository: Tuttotorna/OMNIA
other_repository_doi: 10.5281/zenodo.20322683

<!-- DOI OWNERSHIP AUDIT:END -->

<!-- MB-X.01 LON RELEASE:START -->

## MB-X.01 / L.O.N. release state

Repository: Tuttotorna/OMNIA-VALIDATION
Release tag: v2026.05.22
Release commit: e98a397
Release DOI: 10.5281/zenodo.20325096

Boundary:

measurement != validation
validation != orchestration
orchestration != decision
decision != measurement

<!-- MB-X.01 LON RELEASE:END -->

# OMNIA-VALIDATION

<!-- ZENODO DOI:START -->

## DOI

[![DOI](https://zenodo.org/badge/DOI/10.5281%2Fzenodo.20325096.svg)](https://doi.org/10.5281/zenodo.20325096)

Zenodo DOI badge for this repository.

Repository: Tuttotorna/OMNIA-VALIDATION
GitHub repository id: 1227176782
Release tag: v2026.05.22
Release commit: e98a397
Latest release DOI: 10.5281/zenodo.20325096

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
## Conceptual architecture

- [Ecosystem Conceptual Architecture](docs/ECOSYSTEM_CONCEPTUAL_ARCHITECTURE.md)
## Release candidate

- [v0.2.0 — Ecosystem Validation Snapshot Release](docs/RELEASE_v0.2.0.md)

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

<!-- MB-X.01 LON FINAL RELEASE AUDIT:START -->

## Final MB-X.01 / L.O.N. release audit

The final release audit for the MB-X.01 / L.O.N. ecosystem is recorded here:

```text
docs/MBX01_LON_FINAL_RELEASE_AUDIT.md
```

Final audit state:

```text
Repositories audited: 12
Clean repositories: 12
Repositories with issues: 0
No duplicate DOI values detected.
No duplicate GitHub repository ids detected.
OMNIA DOI != OMNIA-VALIDATION DOI
```

<!-- MB-X.01 LON FINAL RELEASE AUDIT:END -->

<!-- MB-X.01 LON FINAL AUDIT RELEASE DOI:START -->

## Final audit release DOI

The final MB-X.01 / L.O.N. ecosystem audit has been archived as a dedicated OMNIA-VALIDATION release.

repository: Tuttotorna/OMNIA-VALIDATION
release_tag: v2026.05.22
release_commit: e98a397
release_doi: 10.5281/zenodo.20325096
zenodo_record_url: https://zenodo.org/records/20325096
release_role: final_ecosystem_audit_snapshot
final_audit_doc: docs/MBX01_LON_FINAL_RELEASE_AUDIT.md
repositories_audited: 12
clean_repositories: 12
repositories_with_issues: 0
duplicate_doi_values: none
duplicate_github_repository_ids: none
A DOI identifies an archived release snapshot.
A DOI is not a measurement.
A DOI is not validation.
A DOI is not orchestration.
A DOI is not a decision.

<!-- MB-X.01 LON FINAL AUDIT RELEASE DOI:END -->

<!-- OMNIA_ECOSYSTEM_BOUNDARY_V1 -->

## Ecosystem Boundary

```text
measurement != inference != decision
```

This repository is part of the MB-X.01 / OMNIA ecosystem. Its outputs must be read as structural measurement, validation, detection, orchestration or adapter artifacts according to the repository role. They are not autonomous semantic truth claims and they do not make external decisions.
