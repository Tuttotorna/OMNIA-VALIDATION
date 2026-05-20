# Reproducibility

OMNIA-VALIDATION should be easy to run from a clean environment.

The minimum public path is:

    git clone https://github.com/Tuttotorna/OMNIA-VALIDATION.git
    cd OMNIA-VALIDATION
    python -m pip install -e .
    pytest

---

## Reproducibility levels

| Level | Requirement |
|---|---|
| L0 | Repository can be cloned |
| L1 | Tests can be discovered |
| L2 | Tests can be executed |
| L3 | Artifacts can be generated |
| L4 | Reports can be regenerated |
| L5 | Claims can be traced from input to artifact |

The public goal should be L3 or higher.

---

## Expected reviewer experience

A reviewer should not need private context.

A reviewer should be able to run:

    pytest

Then inspect:

    docs/
    artifacts/
    examples/
    reports/

If the repository has no artifacts yet, this should be stated clearly.

---

## Anti-patterns

Avoid:

- undocumented scripts;
- claims without artifacts;
- artifacts without generation commands;
- reports without input references;
- validation language that turns measurement into truth.

---

## Reproducibility statement

Recommended wording:

    This repository validates structural artifacts inside declared boundaries.
    Results are intended to be reproducible, inspectable, and falsifiable.
    They are not semantic truth certificates.

