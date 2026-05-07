# OMNIA-VALIDATION — Legacy Status Mapping

## Purpose

This document explains how legacy result statuses should be treated inside OMNIA-VALIDATION.

Historical result files may contain status values created before the canonical result schema was introduced.

The canonical result schema now allows only:

```text
PASS
CHECK
FAIL
```

Core boundary:

```text
measurement != inference != decision
```

---

## 1. Summary

Legacy result files may contain older status values such as:

```text
passed
stable
unstable
DRIFT
STABLE
CRITICAL
WATCH
v15_external_source_hash_strengthened
collapse-like
```

These values are historical.

They should not be erased.

They should not be blindly converted into canonical `PASS`, `CHECK`, or `FAIL`.

Instead, they are preserved inside:

```text
payload.legacy_status
```

inside the normalized result copies stored in:

```text
results_enveloped/
```

---

## 2. Canonical Status Vocabulary

The current canonical result envelope allows only:

```text
PASS
CHECK
FAIL
```

Meaning:

```text
PASS  -> the tested structural condition survived this validation step
CHECK -> partial instability, ambiguity, boundary condition, or normalization state
FAIL  -> collapse, mismatch, invalid artifact, or validation failure
```

This vocabulary is intentionally small.

It is designed to make validation results comparable.

---

## 3. Legacy Status Is Not Deleted

When a legacy result is wrapped into the canonical envelope, the original status is preserved.

Example legacy result:

```json
{
  "status": "v15_external_source_hash_strengthened",
  "trajectory_count": 20,
  "event_count": 100
}
```

Wrapped result:

```json
{
  "experiment": "temporal_collapse_external_source_hash_strengthening_validator_v15",
  "status": "CHECK",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "boundary": "measurement != inference != decision",
  "payload": {
    "legacy_status": "v15_external_source_hash_strengthened",
    "legacy_result": {
      "status": "v15_external_source_hash_strengthened",
      "trajectory_count": 20,
      "event_count": 100
    }
  }
}
```

The wrapper status is:

```text
CHECK
```

The legacy status is preserved as:

```text
payload.legacy_status
```

---

## 4. Why Wrapper Status Is CHECK

Wrapped legacy files use:

```text
status: CHECK
```

Reason:

```text
wrapping is format normalization
wrapping is not scientific revalidation
```

The wrapper confirms:

```text
this legacy artifact now has a canonical envelope
```

It does not confirm:

```text
the original experiment has been scientifically rerun
the old status is equivalent to PASS
the result is production-safe
the interpretation is final
```

Using `PASS` for all wrappers would overstate the operation.

---

## 5. Why Automatic Mapping Is Dangerous

A legacy status may not mean the same thing as a canonical status.

Example:

```text
DRIFT
```

could mean:

```text
a measured structural regime
```

not:

```text
a validation failure
```

Example:

```text
CRITICAL
```

could mean:

```text
high local structural risk
```

not necessarily:

```text
invalid artifact
```

Example:

```text
v15_external_source_hash_strengthened
```

could mean:

```text
a named successful validator state
```

not directly:

```text
PASS
```

Therefore, blind mapping is unsafe.

---

## 6. Recommended Mapping Discipline

Any mapping from legacy status to canonical status must be:

```text
explicit
documented
domain-specific
validator-specific when needed
non-destructive
auditable
```

A mapping must not silently replace the original legacy status.

The original value must remain preserved.

---

## 7. Safe Default Rule

Safe default rule:

```text
legacy wrapper status = CHECK
```

This means:

```text
the file was normalized
the original status was preserved
the result was not scientifically revalidated
```

This is the current rule used by:

```text
examples/wrap_legacy_results_in_envelope.py
```

---

## 8. Possible Future Mapping Table

A future mapping may use a table like this:

```text
legacy_status                         canonical_status     confidence
passed                                PASS                 medium
stable                                PASS                 medium
STABLE                                PASS                 medium
DRIFT                                 CHECK                high
WATCH                                 CHECK                high
CRITICAL                              CHECK                high
collapse-like                         CHECK                medium
invalid_artifact                      FAIL                 high
hash_mismatch                         FAIL                 high
```

This table is not yet enforced.

It is only a possible future direction.

---

## 9. Why DRIFT Is Not Automatically FAIL

`DRIFT` usually means:

```text
measurable structural movement
```

It does not automatically mean:

```text
the experiment failed
```

A drift result may be scientifically valuable.

It may expose a boundary.

Therefore:

```text
DRIFT -> CHECK
```

is usually safer than:

```text
DRIFT -> FAIL
```

unless the validator defines drift as failure.

---

## 10. Why CRITICAL Is Not Automatically FAIL

`CRITICAL` may mean:

```text
high local risk
```

or:

```text
strong local instability
```

It does not automatically mean:

```text
the file is invalid
the experiment is unusable
the measurement has no value
```

In many OMNIA-VALIDATION experiments, critical local behavior is exactly what the validator is designed to expose.

Therefore:

```text
CRITICAL -> CHECK
```

is often safer than:

```text
CRITICAL -> FAIL
```

unless the validator defines critical behavior as failure.

---

## 11. When FAIL Is Appropriate

Canonical `FAIL` should be used when there is a clear validation failure.

Examples:

```text
invalid JSON
missing required source file
hash mismatch
malformed artifact
unreadable dataset
non-reproducible required output
schema violation in a file expected to be canonical
```

`FAIL` should not be used merely because a result shows instability.

Instability may be the measured phenomenon.

---

## 12. When PASS Is Appropriate

Canonical `PASS` should be used when the tested structural condition survived the validator.

Examples:

```text
hashes match
required files exist
source traceability is complete
schema validation succeeds
expected structural condition is preserved
```

But for legacy wrappers, `PASS` should not be used merely because the original file had a positive-looking legacy status.

The wrapper operation itself is normalization, not revalidation.

---

## 13. When CHECK Is Appropriate

Canonical `CHECK` should be used when:

```text
a boundary condition exists
a result is mixed
a legacy result is normalized but not revalidated
a structural regime is unstable but meaningful
a validator exposes drift or critical local behavior
manual review is appropriate
```

This is why legacy wrapped files currently use:

```text
status: CHECK
```

---

## 14. Current Repository Policy

Current policy:

```text
results/ keeps legacy statuses in original historical files
results_enveloped/ preserves legacy statuses inside payload.legacy_status
wrapped legacy files use canonical status CHECK
no automatic scientific reinterpretation is applied
```

This protects both:

```text
historical evidence
schema compatibility
```

---

## 15. Current Implementation

Current wrapper script:

```text
examples/wrap_legacy_results_in_envelope.py
```

Current wrapper behavior:

```text
infer experiment name from filename
read legacy result JSON
extract legacy status if present
preserve full legacy result inside payload.legacy_result
preserve legacy status inside payload.legacy_status
wrap result in canonical envelope
set wrapper status to CHECK
validate the wrapper envelope
write output to results_enveloped/
```

---

## 16. Current Tests

Current test file:

```text
tests/test_wrap_legacy_results.py
```

The tests verify:

```text
DEFAULT_STATUS is CHECK
experiment name is inferred from filename
legacy status is preserved
missing legacy status becomes null
nested legacy payloads are preserved
wrapper output follows the canonical envelope
legacy PASS does not become wrapper PASS
```

This prevents accidental overclaiming.

---

## 17. Correct Interpretation

Correct interpretation:

```text
legacy_status is historical evidence
wrapper status is normalization status
CHECK means cautious normalization
mapping requires explicit validator-specific logic
```

Incorrect interpretation:

```text
legacy_status can always be converted automatically
legacy PASS means wrapper PASS
legacy CRITICAL means wrapper FAIL
legacy DRIFT means experiment failure
results_enveloped/ scientifically revalidates all legacy results
```

---

## 18. Future Work

Possible future steps:

```text
create validator-specific legacy status maps
document status vocabularies by experiment family
add payload-specific schema validators
add tests for mapping tables
add manual review notes for ambiguous statuses
add per-family normalization summaries
```

Possible future file:

```text
docs/VALIDATOR_STATUS_VOCABULARY.md
```

---

## 19. Non-Goal

This document does not reinterpret historical experiments.

It does not declare all legacy results correct.

It does not define semantic truth.

It does not certify production safety.

It defines a safe policy for preserving and handling legacy status values.

Final boundary:

```text
measurement != inference != decision
```