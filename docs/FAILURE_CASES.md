# Failure Cases and Limits

## Purpose

This document makes the failure logic explicit.

OMNIA-VALIDATION is strongest when it records not only positive evidence, but also limits, failures, regressions, and negative controls.

## Core boundary

```text
measurement != inference != decision
validation evidence != semantic truth
```

## Expected failure categories

OMNIA-VALIDATION should expose cases such as:

- schema regression
- status regression
- hash regression
- payload regression
- boundary regression
- expected drift
- observer-dependent instability
- cross-provider disagreement
- source artifact mismatch
- structural collapse under perturbation
- irrecoverable projection loss
- semantic ambiguity outside structural measurement

## Why failures matter

A validation repository that only shows positive results is weak.

A validation repository that records failures is stronger.

Failure cases define the real boundary of the method.

## Current operational examples

Result-regression classifications include:

```text
NO_REGRESSION
EXPECTED_DRIFT
SCHEMA_REGRESSION
STATUS_REGRESSION
BOUNDARY_REGRESSION
PAYLOAD_REGRESSION
HASH_REGRESSION
```

These classifications are structural.

They do not decide semantic truth.

## Safe interpretation

```text
A failure is not always a contradiction of OMNIA.
A failure can identify the boundary of a specific validation regime.
```

## Practical rule

When a result fails:

1. preserve the artifact
2. preserve the input
3. preserve the hash
4. identify the regression class
5. record whether the failure is structural, semantic, procedural, or out of scope
6. avoid converting a structural signal into a final decision
