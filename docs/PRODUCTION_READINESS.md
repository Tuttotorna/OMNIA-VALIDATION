# Production Readiness Notes

Repository: `OMNIA-VALIDATION`

Last hardening pass: `2026-05-21T14:03:44Z`

## Current role

Evidence, traceability, reproducibility and regression control plane.

## Current maturity label

`core`

## Minimum readiness checklist

- [ ] Full test suite runs in GitHub Actions.
- [ ] CI supports Python 3.10, 3.11 and 3.12 where applicable.
- [ ] Runtime dependencies are explicit in `pyproject.toml`.
- [ ] Development dependencies are explicit.
- [ ] Boundary statement is present and consistent.
- [ ] Examples do not imply semantic truth or autonomous decision.
- [ ] Validation artifacts are reproducible.
- [ ] Release tag and package version are aligned.
- [ ] No workflow is stored outside `.github/workflows`.
- [ ] Security-sensitive naming is bounded by clear disclaimers.

## Required public boundary

```text
measurement != inference != decision
```

## Operational interpretation

This repository should be treated as part of a layered system, not as an isolated oracle.

The defensible interpretation is:

```text
output = structural measurement artifact
decision = external responsibility
semantics = outside the measurement contract
```

## Next hardening step

Run:

```bash
python scripts/local_validate.py
```

Then verify that the GitHub Actions workflow passes on the default branch.

<!-- CI_REPAIR_PASS_2026_05_21 -->

## CI repair pass

Last repair pass: `2026-05-21T14:19:12Z`

This pass preserves repository-specific CI assertions while also running the full test suite.

It also avoids accidental local-package shadowing by using `OMNIA_SOURCE_DIR` and by prioritizing the canonical `OMNIA` checkout in CI.

<!-- OMNIA_VALIDATION_CI_ASSERTION_REPAIR_2026_05_21 -->

## OMNIA-VALIDATION CI assertion repair

Last repair pass: `2026-05-21T14:28:34Z`

The CI workflow intentionally includes explicit pytest commands for release audit, DOI audit, first-reader path, commit registration, public entrypoint registration, and registry anchor role-separation tests.

These commands are present because the repository self-validates that critical public-release checks are registered directly in CI before the full suite runs.
