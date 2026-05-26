# OMNIA Evidence Contract v1

Canonical evidence contract for the OMNIA / MB-X.01 ecosystem.

This document defines the minimum operational interface required for any OMNIA-compatible validation runner, gate, auditor, fragility checker, limit checker, radar layer, or structural measurement envelope.

The purpose is not to merge repositories.

The purpose is to allow independent repositories to produce a common, auditable evidence format.

```text
federated repositories
+ common evidence contract
+ stable exit codes
+ reproducible metadata
= industrial quality gate compatibility
```

---

## 1. Core boundary

OMNIA-compatible systems must preserve this boundary:

```text
measurement != inference != decision
```

Expanded:

```text
OMNIA measures structural behavior.
OMNIA does not infer semantic truth.
OMNIA does not decide deployment.
OMNIA does not replace human or organizational responsibility.
```

A compliant runner may produce:

```text
PASS
STRUCTURAL_FAILURE
LIMIT_REACHED
INVALID_INPUT
INCOMPLETE_EVIDENCE
INTERNAL_ERROR
```

A compliant runner must not claim:

```text
this answer is true
this model is safe
this system should be deployed
this decision is correct
```

The output is evidence, not judgment.

---

## 2. Required files

A compliant run SHOULD be organized as:

```text
input.jsonl
run_config.json
certificate.json
failures.jsonl
summary.md
```

Minimum valid evidence package:

```text
certificate.json
```

Recommended full evidence package:

```text
input.jsonl
run_config.json
certificate.json
failures.jsonl
summary.md
logs/
artifacts/
```

---

## 3. Input contract: input.jsonl

Input must use JSON Lines.

Each line represents one measurement case.

Minimum fields:

```json
{
  "case_id": "case-001",
  "input": "raw input or structured payload",
  "output": "system output to be measured"
}
```

Recommended fields:

```json
{
  "case_id": "case-001",
  "input": "raw input or structured payload",
  "output": "system output to be measured",
  "expected": null,
  "metadata": {
    "source": "manual",
    "domain": "general",
    "created_at": "2026-05-26T00:00:00Z"
  }
}
```

Rules:

```text
case_id must be stable within a run.
input must preserve the observed input.
output must preserve the observed output.
expected is optional.
metadata is optional.
No semantic coercion is required by this contract.
```

---

## 4. Run configuration contract: run_config.json

Minimum fields:

```json
{
  "contract_version": "omnia-evidence-contract/v1",
  "runner": {
    "name": "omnia-validation-runner",
    "version": "0.1.0"
  },
  "mode": "structural_measurement",
  "thresholds": {},
  "modules": []
}
```

Recommended fields:

```json
{
  "contract_version": "omnia-evidence-contract/v1",
  "runner": {
    "name": "omnia-validation-runner",
    "version": "0.1.0",
    "repository": "https://github.com/Tuttotorna/OMNIA-VALIDATION"
  },
  "mode": "structural_measurement",
  "modules": [
    "omnia",
    "omnia-limit",
    "omnia-radar",
    "omnia-fragility-checker"
  ],
  "thresholds": {
    "omega_min": null,
    "sei_max": null,
    "iri_max": null,
    "fragility_max": null
  },
  "reproducibility": {
    "python_version": null,
    "platform": null,
    "git_commit": null,
    "created_at": null
  }
}
```

---

## 5. Certificate contract: certificate.json

The certificate is the canonical machine-readable output.

Minimum fields:

```json
{
  "contract_version": "omnia-evidence-contract/v1",
  "run_id": "run-001",
  "status": "PASS",
  "exit_code": 0,
  "summary": {
    "total_cases": 1,
    "passed_cases": 1,
    "failed_cases": 0,
    "limit_reached_cases": 0,
    "invalid_cases": 0
  },
  "boundary": {
    "measurement_not_inference": true,
    "measurement_not_decision": true,
    "semantic_truth_claim": false
  }
}
```

Required status values:

```text
PASS
STRUCTURAL_FAILURE
LIMIT_REACHED
INVALID_INPUT
INCOMPLETE_EVIDENCE
INTERNAL_ERROR
```

---

## 6. Failure contract: failures.jsonl

Failure output must also use JSON Lines.

Each line represents one failed or flagged case.

Minimum fields:

```json
{
  "case_id": "case-001",
  "failure_type": "STRUCTURAL_FAILURE",
  "message": "Structural instability detected."
}
```

Recommended fields:

```json
{
  "case_id": "case-001",
  "failure_type": "STRUCTURAL_FAILURE",
  "message": "Structural instability detected.",
  "signals": {
    "omega": null,
    "sei": null,
    "iri": null,
    "fragility": null
  },
  "module": "omnia-fragility-checker",
  "evidence": {
    "before": null,
    "after": null,
    "delta": null
  }
}
```

Allowed failure types:

```text
STRUCTURAL_FAILURE
LIMIT_REACHED
INVALID_INPUT
INCOMPLETE_EVIDENCE
INTERNAL_ERROR
```

---

## 7. Exit code policy

Exit codes are part of the contract.

They allow CI/CD systems, industrial quality gates, shell scripts, and external validators to consume OMNIA evidence without parsing human prose.

```text
0 = PASS
1 = INTERNAL_ERROR
2 = STRUCTURAL_FAILURE
3 = LIMIT_REACHED
4 = INVALID_INPUT
5 = INCOMPLETE_EVIDENCE
```

Rules:

```text
Exit 0 means the runner completed and produced PASS evidence.
Exit 1 means the runner itself failed.
Exit 2 means the measured structure failed.
Exit 3 means the limit condition was reached.
Exit 4 means the input was malformed or invalid.
Exit 5 means the run did not produce enough evidence.
```

Important:

```text
Exit 0 does not mean semantic truth.
Exit 0 does not mean deployment approval.
Exit 0 means only that the configured structural gate passed.
```

---

## 8. Minimal CLI interface

A compliant command-line runner SHOULD expose:

```bash
omnia-validate input.jsonl --config run_config.json --out evidence/
```

Expected output directory:

```text
evidence/
  certificate.json
  failures.jsonl
  summary.md
```

Optional flags:

```bash
--strict
--emit-failures
--emit-summary
--contract-version omnia-evidence-contract/v1
--fail-on-limit
--fail-on-incomplete-evidence
```

---

## 9. Quality gate use

A CI/CD system may consume only:

```text
exit_code
certificate.json
```

Example policy:

```text
exit_code == 0 -> allow next pipeline stage
exit_code == 2 -> block deployment
exit_code == 3 -> stop expansion / require review
exit_code == 4 -> reject dataset or input package
exit_code == 5 -> require more evidence
exit_code == 1 -> fix runner or environment
```

This creates a clean separation:

```text
OMNIA produces evidence.
The surrounding governance system decides what to do with it.
```

---

## 10. Repository role alignment

Canonical ecosystem roles:

```text
lon-mirror
  public hub, lineage, boundaries, navigation

OMNIABASE
  multi-representational observation framework

OMNIA
  post-hoc structural measurement engine

omnia-limit
  stop-condition / continuation-boundary layer

OMNIA-RADAR
  structural detection, drift surfacing, residual scanning

OMNIA-VALIDATION
  evidence aggregation, validation runner, certificate layer

OMNIA-MINIMAL
  minimal reproducible demonstration

OMNIA-FRAGILITY-CHECKER
  practical fragility entrypoint for external users

OMNIAMIND
  structural cognition orchestration, not decision

COLLATZ-NATIVE-MATH
  mathematical laboratory for non-classical structural observation
```

---

## 11. Non-goals

This contract does not define:

```text
the full OMNIA metric internals
the mathematical theory of OMNIABASE
a semantic correctness benchmark
a model ranking system
a deployment approval system
a governance policy
```

This contract defines only:

```text
how evidence must be emitted
how failure must be represented
how CI/CD must read the result
where the boundary of the claim is
```

---

## 12. Public positioning

Recommended public formulation:

```text
OMNIA is not a model, not a benchmark, and not a judge.
It is a post-hoc structural measurement layer that produces auditable evidence before deployment decisions.
```

Compressed version:

```text
OMNIA does not say what is true.
OMNIA measures where structure stops holding.
```

---

## 13. Versioning

Current version:

```text
omnia-evidence-contract/v1
```

Backward-compatible changes may add optional fields.

Breaking changes require:

```text
omnia-evidence-contract/v2
```

---

## 14. Compliance checklist

A repository is contract-compatible if it can produce:

```text
[ ] certificate.json
[ ] stable exit code
[ ] boundary declaration
[ ] failure representation when applicable
[ ] reproducibility metadata
[ ] no semantic truth claim
[ ] no deployment decision claim
```

A repository is fully validation-ready if it can produce:

```text
[ ] input.jsonl
[ ] run_config.json
[ ] certificate.json
[ ] failures.jsonl
[ ] summary.md
[ ] CI-readable exit code
[ ] documented CLI command
```

---

## 15. Minimal evidence package example

```text
evidence/
  certificate.json
  failures.jsonl
  summary.md
```

A downstream system should be able to decide pipeline flow using only:

```text
certificate.json.status
certificate.json.exit_code
```

That is the operational minimum.
