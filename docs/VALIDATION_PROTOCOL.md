# Validation Protocol

This document defines the validation shape expected in OMNIA-VALIDATION.

The repository validates artifacts, not metaphysical claims.

Canonical boundary:

    measurement != inference != decision

---

## Validation unit

A validation unit should contain:

| Component | Required | Description |
|---|---:|---|
| id | yes | Stable identifier for the case |
| input | yes | Object, output, trace, representation, or trajectory being tested |
| transformation | yes | Perturbation, rewrite, representation shift, or controlled variant |
| measurement | yes | Structural measurement or externally generated score |
| artifact | yes | File or report containing the observable result |
| expected_boundary | yes | Declared condition being tested |
| result | yes | pass, flag, fail, inconclusive |
| limitation | yes | What the result does not prove |
| reproduction | preferred | Command or script to reproduce |
| source | optional | External source or dataset reference |

---

## Result vocabulary

Use a small result vocabulary:

    pass
    flag
    fail
    inconclusive

Meaning:

- pass: the artifact satisfies the declared structural expectation;
- flag: the artifact shows instability or risk requiring inspection;
- fail: the artifact violates the declared boundary;
- inconclusive: the artifact is insufficient or ambiguous.

---

## Claim discipline

A validation result may say:

    this artifact passed the declared structural check.

It must not silently say:

    therefore the system is true.
    therefore the model is intelligent.
    therefore the output is semantically correct.
    therefore the downstream decision is valid.

---

## Reproducibility rule

Every serious validation claim should be traceable to:

    input -> command -> output -> artifact -> report

No artifact, no serious claim.

---

## Failure-first rule

Failure examples are not embarrassing.

They are the strongest part of the repository.

A validation system that only shows success does not build trust.

A validation system that exposes failure modes builds credibility.

