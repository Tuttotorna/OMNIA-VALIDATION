# Failure Examples

Failure examples are a core part of OMNIA-VALIDATION.

The purpose is not to show that every system is bad.

The purpose is to show that surface correctness and structural stability are different things.

---

## Minimal failure pattern

A useful failure example has this shape:

    input appears acceptable
    transformed input remains superficially similar
    measured structure changes or collapses
    artifact records the instability
    report explains the boundary

---

## Example narrative

A model output may look correct to a human reader.

After a controlled transformation, the surface may still look acceptable.

But the structural measurement may show instability, drift, irreversibility, or loss of admissibility.

That result does not automatically mean the output is false.

It means:

    the output is structurally fragile under the declared transformation.

---

## What failure does prove

Failure may prove:

- the declared structural condition was not preserved;
- the artifact violates a stability expectation;
- the case requires inspection;
- surface correctness was insufficient as a validation criterion.

---

## What failure does not prove

Failure does not automatically prove:

- semantic falsehood;
- maliciousness;
- model incompetence;
- physical impossibility;
- final downstream invalidity.

The decision remains external.

---

## Why this matters

Developers trust tools that show where systems fail.

A validation repository with visible failure modes is stronger than one that only shows polished success cases.

