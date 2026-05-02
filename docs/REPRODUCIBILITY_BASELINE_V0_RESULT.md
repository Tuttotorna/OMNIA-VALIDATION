# Reproducibility Baseline v0 — Result

## Status

```text
PASS

Evidence Level

Level 1 — Toy Demonstration

Experiment

reproducibility_baseline_v0

Repository

OMNIA-VALIDATION


---

Purpose

This experiment tests whether a minimal structural measurement pipeline produces stable results across repeated runs under fixed conditions.

It does not test the full OMNIA engine.

It does not prove OMNIA correct.

It does not validate semantic truth.

It tests only:

same input
same transformation
same metric
same configuration
repeated runs
->
same measurement output


---

Core Boundary

measurement != inference != decision

The experiment validates deterministic structural measurement behavior only.

Interpretation remains external.

Decision remains external.


---

What Was Tested

The experiment compared three toy input classes:

structured
mildly_perturbed
random_like

Each input was measured using a minimal structural signature composed of:

entropy
compression_ratio
repetition_score
omega_proxy

The measurement was repeated:

10 runs

under fixed deterministic conditions.


---

Expected Behavior

The reproducibility expectation was:

all repeated runs return identical outputs

The structural ordering expectation was:

structured >= mildly_perturbed >= random_like

This ordering is not a universal claim.

It applies only to this toy input set.


---

Observed Result

The experiment produced:

Status: PASS
Runs executed: 10
Reproducible: True
Order holds: True

Observed omega_proxy values:

structured         -> 0.858222336066
mildly_perturbed   -> 0.754354508197
random_like        -> 0.0

The expected ordering held:

structured >= mildly_perturbed >= random_like

No reproducibility mismatch was detected.


---

JSON Result

The generated result file is:

results/reproducibility_baseline_v0.json

Key JSON fields:

{
  "experiment_name": "reproducibility_baseline_v0",
  "version": "0.1.0",
  "domain": "minimal_structural_measurement",
  "claim_level": "Level 1 — Toy Demonstration",
  "runs_executed": 10,
  "status": "PASS",
  "reproducibility": {
    "stable": true,
    "mismatch_count": 0,
    "mismatches": []
  },
  "structural_ordering": {
    "expected_order": "structured >= mildly_perturbed >= random_like",
    "observed_values": {
      "structured": 0.858222336066,
      "mildly_perturbed": 0.754354508197,
      "random_like": 0.0
    },
    "order_holds": true
  }
}


---

Interpretation

This result shows that the toy structural measurement pipeline is deterministic under fixed conditions.

It also shows that, for this controlled toy input set, the minimal omega_proxy preserves the expected structural ordering:

structured
>
mildly_perturbed
>
random_like

This is a basic reproducibility result.

It is not a broad validation of OMNIA.


---

What This Result Does NOT Prove

This result does not prove:

OMNIA is correct

Ω is universally meaningful

structural truth has been established

semantic correctness can be detected

random inputs always score lower

the metric generalizes across domains

the full OMNIA engine has been validated


This is only a first deterministic baseline.


---

Limitations

The experiment has several limitations:

it uses toy inputs

it does not use the full OMNIA engine

omega_proxy is only a minimal structural proxy

no semantic evaluation is performed

no adversarial perturbation is tested

no threshold robustness is tested

no cross-domain behavior is tested

no external reproduction has occurred



---

Failure Conditions

This experiment would fail if:

repeated runs produced different results

or:

structured < mildly_perturbed

or:

mildly_perturbed < random_like

under the current toy configuration.


---

Reproduction Command

Run from repository root:

python examples/reproducibility_baseline_v0.py

Expected summary:

Status: PASS
Reproducible: True
Order holds: True


---

Colab Reproduction

The experiment was reproduced in a clean Colab session.

Observed Colab summary:

Status:       PASS
Reproducible: True
Order holds:  True

Observed omega_proxy values:
  structured         -> 0.858222336066
  mildly_perturbed   -> 0.754354508197
  random_like        -> 0.0

Return code:

0


---

Result Classification

PASS

Reason:

deterministic repeated runs
+
expected toy structural ordering held

Evidence level:

Level 1 — Toy Demonstration


---

Next Validation Step

The next experiment should move from reproducibility to semantic separation.

Recommended next file:

examples/semantic_vs_structural_separation_v0.py

Goal:

show that semantic correctness and structural stability are separable

Expected cases:

semantically wrong but structurally stable
semantically correct but structurally unstable
semantically correct and structurally stable
semantically wrong and structurally unstable

This will test the declared boundary:

structural validity != semantic correctness