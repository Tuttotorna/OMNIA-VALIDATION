# OMNIA-VALIDATION — Code of Conduct

## Purpose

This document defines the expected conduct for contributors, reviewers, maintainers, and users of OMNIA-VALIDATION.

OMNIA-VALIDATION is a structural validation, falsification, perturbation testing, and reproducibility layer.

Core boundary:

```text
measurement != inference != decision
```

The project welcomes rigorous criticism.

It does not welcome personal attacks, harassment, credential exposure, or unsupported overclaims.

---

## 1. Core Principle

This project is built around falsification pressure.

That means disagreement is expected.

Acceptable disagreement:

```text
this result is not reproducible
this schema is too weak
this status mapping is unsafe
this claim overreaches the evidence
this validator needs stronger controls
this boundary is not documented clearly
```

Unacceptable conduct:

```text
personal attacks
insults
harassment
threats
credential sharing
deliberate misrepresentation
bad-faith disruption
pressure to hide negative results
pressure to overstate results
```

Criticism should target claims, artifacts, schemas, methods, scripts, and documentation.

It should not target a person.

---

## 2. Expected Behavior

Expected behavior:

```text
be precise
cite files and commands
separate evidence from interpretation
preserve boundary language
report failures honestly
respect negative results
avoid unsupported claims
avoid semantic overreach
avoid personal attacks
```

When reporting a problem, prefer:

```text
file path
command run
observed output
expected output
reason for concern
```

Example:

```text
results_enveloped/example.json fails validate-result because payload is not an object.
```

Better than:

```text
this repository is wrong
```

---

## 3. Boundary Discipline

All contributors should preserve the project boundary:

```text
measurement != inference != decision
```

Do not convert structural measurements into unsupported claims about:

```text
semantic truth
model intelligence
consciousness
production safety
universal validity
final correctness
domain-independent guarantees
```

Strong claims require strong evidence.

Unsupported overclaiming is not acceptable maintenance behavior.

---

## 4. Negative Results

Negative results are part of OMNIA-VALIDATION.

Do not pressure maintainers or contributors to remove:

```text
CHECK results
DRIFT regimes
CRITICAL local behavior
weak correlations
failed hypotheses
boundary instability
metric collapse
reproducibility failures
```

These artifacts may be scientifically useful.

A falsification-oriented repository becomes stronger when failure boundaries remain visible.

---

## 5. Result Review Conduct

When reviewing validation results, focus on:

```text
schema validity
payload structure
source traceability
hash consistency
reproducibility
PASS/CHECK/FAIL logic
legacy status preservation
boundary claims
documentation consistency
```

Avoid claiming more than the result supports.

A result artifact may show structural behavior.

It does not automatically prove semantic correctness.

---

## 6. Pull Request Conduct

Pull requests should be clear and reviewable.

A pull request should include:

```text
summary of changes
files affected
tests run
schema impact if any
result artifact impact if any
documentation impact if any
boundary check
```

If a pull request changes result artifacts, explain why.

Historical results should not be rewritten casually.

---

## 7. Issue Conduct

Issues should be specific.

Use the available issue templates when possible:

```text
bug report
validation result review
documentation issue
```

Include:

```text
file paths
commands
outputs
expected behavior
actual behavior
environment details when relevant
```

Do not use issues for harassment, spam, unrelated promotion, or unsupported accusations.

---

## 8. Credential Safety

Never post or commit:

```text
GitHub tokens
API keys
passwords
private credentials
private keys
secret URLs
```

If a credential is accidentally exposed:

```text
revoke it immediately
rotate affected secrets
remove the credential from the repository
notify maintainers if needed
```

Credential exposure is treated as urgent.

---

## 9. Respectful Technical Language

Technical criticism can be direct.

It should remain specific.

Acceptable:

```text
The current validator does not prove this claim.
The result should be CHECK, not PASS.
The schema does not enforce this payload field.
The README overstates the current evidence.
```

Unacceptable:

```text
personal insults
mockery
threats
identity attacks
harassment
bad-faith repetition
```

---

## 10. Enforcement

Maintainers may respond to violations by:

```text
requesting edits
closing issues
deleting abusive comments
blocking abusive users
rejecting pull requests
reporting platform abuse
```

Severity depends on the behavior.

Good-faith mistakes should be corrected.

Bad-faith harassment or credential exposure may require immediate action.

---

## 11. Scope

This code of conduct applies to project spaces including:

```text
repository issues
pull requests
comments
documentation discussions
release discussions
related public project discussions
```

The project boundary remains:

```text
measurement != inference != decision
```

---

## 12. Non-Goal

This document does not require agreement with OMNIA-VALIDATION claims.

Critical review is welcome.

The goal is to keep criticism precise, evidence-based, reproducible, and non-abusive.

Final boundary:

```text
measurement != inference != decision
```