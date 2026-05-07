# Temporal Collapse Level 3 — External Source Hash Strengthening Validator V15 Result

## Status

**PASSED**

V15 successfully strengthens the V14 repeated-run cross-provider stability validation by replacing symbolic source-file hash placeholders with real computed SHA-256 hashes.

This closes the main external-source traceability weakness left in V14.

---

## Validator

```text
examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py

Input Dataset

data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl

Input Result

results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json

Output Dataset

data/temporal_collapse_external_source_hash_strengthened_v15.jsonl

Output Result

results/temporal_collapse_external_source_hash_strengthening_validator_v15.json


---

Purpose

V15 exists for one precise reason:

replace placeholder source-file hashes with real computed source-file hashes

V14 already mapped repeated-run cross-provider GSM-Symbolic model-output records into raw ordered structural trajectories.

However, V14 still used symbolic source_file_hash values such as:

sha256:provider_a_run_001_source_file_hash_v14

Those placeholders were structurally useful, but not externally strong.

V15 computes the real SHA-256 digest of each source-output file and rewrites the mapped records using those real hashes.


---

Boundary

This is an external-source hash strengthening validator.
It does not change the structural risk logic.
It does not change the V14 trajectory mapping.
It does not claim semantic truth.
It does not claim official GSM-Symbolic scoring.
It does not claim that OMNIA solves GSM-Symbolic.
It does not make final decisions.

V15 strengthens traceability only.

The measurement boundary remains:

measurement != inference != decision


---

Source Files Strengthened

V15 computed real SHA-256 hashes for 4 source-output files.

data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl
sha256:24d7177cea63e44e2616c0d4546ed65fd824719f7fc4030b9a52130c1bf4e00c

data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_002.jsonl
sha256:602676324b4335e7cb670d6884cbe5e978dacac59889dbc362252440d706dc2e

data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_001.jsonl
sha256:5ab1f8a6bf24f266a8dbf4e4e952be749db66ae66156bff0835d44088bb8ac5a

data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_002.jsonl
sha256:5399edf34ba661ece7b6f0855df09ecad7d895a74951bd8bec56ad8074dd9010


---

Validation Summary

experiment: temporal_collapse_external_source_hash_strengthening_validator_v15
status: v15_external_source_hash_strengthened
trajectory_count: 20
event_count: 100
source_file_count: 4
computed_hash_count: 4
real_hash_count: 4
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0

The important part is:

real_hash_count: 4
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0

This means every source-file hash used by the strengthened dataset/result is now tied to the actual file content.


---

Aggregate Result Preserved From V14

V15 does not modify the structural risk calculation.

The aggregate V14 measurement remains preserved:

aggregate_risk_score: 0.379255
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.42
aggregate_extraction_rate: 0.9

Regime counts:

CRITICAL: 4
DRIFT: 10
STABLE: 6

Highest-risk trajectory:

gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001

Highest-risk score:

0.7096

Highest-risk provider:

provider_b

Highest-risk run:

provider_b_run_v14_002


---

Structural Interpretation

V15 confirms that the repeated-run cross-provider result remains structurally consistent after source-file hash strengthening.

The core V14 observation is unchanged:

Repeated-run variation remains small.
Cross-provider differences remain visible.
Collapse-like trajectories remain the highest-risk cases.
The aggregate regime remains DRIFT.
The aggregate gate action remains WATCH.

The strengthened hashes make the source trail harder to dismiss because the validation now binds each mapped record to real source-file content digests.


---

What V15 Adds Over V14

V14 established:

repeated-run cross-provider structural stability mapping

V15 adds:

real external source-file hash verification

In practical terms:

V14 = structural repeated-run / cross-provider measurement
V15 = V14 + real source-file hash traceability


---

Why This Matters

Without real source-file hashes, a critic can say:

The mapping is documented, but the source-file identity is only symbolic.

After V15, that objection is reduced.

Now the validation contains:

source file path
computed SHA-256 digest
hash verification status
placeholder replacement status
mismatch failure count
format failure count

The result is still not a semantic proof.

But it is a stronger structural evidence chain.


---

Commit Reference

6b8120e Add v15 external source hash strengthened validation

Committed files:

examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py
data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
results/temporal_collapse_external_source_hash_strengthening_validator_v15.json


---

Final Result

V15 HASH STRENGTHENING PASSED

V15 successfully strengthens the Level 3 temporal-collapse validation chain by converting symbolic source-file hash placeholders into real computed SHA-256 source-file hashes while preserving the V14 structural measurement result.

The validation chain now has stronger external-source traceability:

V13: cross-provider disagreement mapping
V14: repeated-run cross-provider stability mapping
V15: real external source-file hash strengthening