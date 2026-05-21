# Ecosystem Backbone Registry CI

## Status

The OMNIA-VALIDATION CI workflow now runs the ecosystem backbone compliance registry test.

This makes the registry part of the executable validation surface instead of leaving it as passive documentation.

## Registry test

~~~text
python -m pytest -q tests/test_ecosystem_backbone_compliance_registry.py
~~~

## Purpose

The registry test protects the declared backbone state:

~~~text
OMNIA measurement
  -> BoundaryCertificate
  -> omnia-limit validate_certificate()
  -> OMNIA-VALIDATION ValidationEnvelope
  -> CI regression
  -> satellite compliant producer / adapter / consumer / observer
~~~

## Protected layer rules

~~~text
measurement != validation
validation != orchestration
orchestration != decision
decision != measurement
observation != decision
domain adaptation != backbone redefinition
~~~

## Required behavior

CI must fail if:

~~~text
1. The registry markdown is missing.
2. The registry JSON is missing.
3. A required ecosystem repository is missing from the registry.
4. A satellite is marked as backbone core.
5. Any registry entry lacks role, status, commit, responsibility, or forbidden-boundary declarations.
6. Registry counts no longer match entries.
7. Layer-separation rules are removed.
~~~

## Boundary

This CI step does not create a new backbone contract.

It only verifies that the registry remains aligned with the existing canonical contract.
