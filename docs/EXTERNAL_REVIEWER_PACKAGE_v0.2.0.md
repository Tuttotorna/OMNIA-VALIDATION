# External Reviewer Package — MB-X.01 / OMNIA v0.2.0

## Purpose

This document is for external reviewers.

The goal is not to ask for belief.

The goal is to make the ecosystem checkable.

## Core boundary

    measurement != inference != decision

OMNIA measures structural behavior.

It does not infer semantic truth.

It does not make final decisions.

It does not claim consciousness.

It does not guarantee safety.

## What to review first

Recommended order:

1. `lon-mirror/docs/ECOSYSTEM_CONCEPTUAL_ARCHITECTURE.md`
2. `OMNIA-VALIDATION/docs/ECOSYSTEM_CONCEPTUAL_ARCHITECTURE.md`
3. `OMNIA-VALIDATION/docs/OMNIA_ECOSYSTEM_VALIDATION_SNAPSHOT.md`
4. `OMNIA-VALIDATION/docs/PUBLIC_VALIDATION_PACKAGE.md`
5. `OMNIA/docs/SCOPE.md`
6. `OMNIA/docs/ENGINE_OVERVIEW.md`

## What to verify

Please verify:

- repositories clone correctly;
- local tests pass;
- public claims remain bounded;
- OMNIA is not presented as semantic truth;
- OMNIA-VALIDATION contains reproducibility evidence;
- each repository has a distinct role;
- adapters do not overclaim domain authority;
- the release is technically auditable.

## What to challenge

Please challenge:

- whether the measured signals are useful;
- whether the boundary is clear enough;
- whether the validation protocols are too small;
- whether baseline comparisons are sufficient;
- whether the measurement can detect failures not caught by surface checks;
- whether the ecosystem can be falsified.

## What this release claims

This release claims:

    The ecosystem is organized, locally reproducible, claim-bounded,
    and ready for external technical review.

## What this release does not claim

This release does not claim:

- absolute truth;
- semantic truth;
- scientific finality;
- production certification;
- cryptographic safety;
- artificial consciousness;
- autonomous decision authority.

## Minimal independent check

    git clone https://github.com/Tuttotorna/OMNIA-VALIDATION.git
    cd OMNIA-VALIDATION
    python -m pip install -e .
    python -m pytest -q

For the wider ecosystem, start from:

    https://github.com/Tuttotorna/lon-mirror

## Reviewer output requested

Useful review output includes:

- failed test logs;
- unclear boundary language;
- overclaim examples;
- reproducibility issues;
- proposed falsification datasets;
- baseline suggestions;
- external benchmark suggestions;
- requests for clearer metrics or protocols.

## Final review question

The main question is:

    Does OMNIA measure structural instability that surface correctness misses?
