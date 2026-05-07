# Temporal Collapse Level 3 — External-Source Hash Strengthening Validator v15

## Status

`SPECIFICATION`

## Validator name

```text
temporal_collapse_external_source_hash_strengthening_validator_v15

Purpose

V15 strengthens the Level 3 validation chain by replacing placeholder source-file hashes with real computed SHA-256 hashes.

V14 validated repeated-run cross-provider stability, but its source-file hashes were still symbolic placeholders.

V15 makes source traceability stronger by requiring every referenced source-output file to have a real hash computed from the actual file content.

Boundary

measurement != inference != decision

hash verification != semantic correctness

source traceability != benchmark authority

real file hash != proof of model truth

Scope

V15 applies to the repeated-run cross-provider stability source files introduced in V14.

It checks that every source_file_hash field is no longer a placeholder.

It computes the SHA-256 hash of each referenced source file.

It verifies that mapped event records, result summaries, and source summaries use the same real hash values.

Input dataset

data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl

Input result file

results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json

Source files to hash

data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_002.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_002.jsonl

Placeholder hashes to replace

sha256:provider_a_run_001_source_file_hash_v14
sha256:provider_a_run_002_source_file_hash_v14
sha256:provider_b_run_001_source_file_hash_v14
sha256:provider_b_run_002_source_file_hash_v14

Required output dataset

data/temporal_collapse_external_source_hash_strengthened_v15.jsonl

Required output result file

results/temporal_collapse_external_source_hash_strengthening_validator_v15.json

Required result document

docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15_RESULT.md

What V15 must verify

V15 must verify that:

all source files exist
all source files are readable
all source files have real SHA-256 hashes
all placeholder hashes are replaced
all dataset event records use real hashes
all result-level source_file_hashes use real hashes
all source summaries use real hashes
all provider summaries use real hashes
all run summaries use real hashes
all trajectory results use real hashes

Hash format

Every hash must use this format:

sha256:<64 lowercase hexadecimal characters>

Example:

sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

Invalid hash values

The validator must reject these:

sha256:provider_a_run_001_source_file_hash_v14
sha256:provider_a_run_002_source_file_hash_v14
sha256:provider_b_run_001_source_file_hash_v14
sha256:provider_b_run_002_source_file_hash_v14

It must also reject any value that does not match:

^sha256:[0-9a-f]{64}$

Source-file hash mapping

The validator must build this mapping:

source_file -> real computed sha256 hash

Expected source-file keys:

data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_002.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_002.jsonl

Dataset rewrite rule

For every event record in:

data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl

V15 must read:

source_file

Then replace:

source_file_hash

with the real computed hash for that source file.

The rewritten dataset must be saved as:

data/temporal_collapse_external_source_hash_strengthened_v15.jsonl

Result rewrite rule

For the result file:

results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json

V15 must rewrite hash fields into a new V15 result file.

The original V14 result file must remain unchanged.

The V15 result file must update:

experiment
status
boundary
claim
limitation_note
input_file
source_file_hashes
aggregate.source_file_hash_count
source_summary[*].source_file_hashes
provider_summary[*].source_file_hashes
run_summary[*].source_file_hashes
results[*].source_file_hash
results[*].transition_evidence.source_file_hash

V15 experiment value

temporal_collapse_external_source_hash_strengthening_validator_v15

V15 status value

v15_external_source_hash_strengthened

V15 boundary

repeated-run cross-provider real parsed GSM-Symbolic model-output file records with real computed source-file SHA-256 hashes mapped into raw ordered structural trajectory events

V15 claim

This validator strengthens source traceability by replacing symbolic source-file hash placeholders with real computed SHA-256 hashes.

It does not claim that OMNIA solves GSM-Symbolic.

It does not infer semantic truth.

It does not replace benchmark correctness.

It does not make final decisions.

It only verifies that source-file identity is cryptographically bound to the mapped validation records.

V15 limitation note

External-source hash strengthening does not imply official benchmark scoring, production certification, semantic truth detection, model correctness, provider quality, or final decision authority.

Expected preserved values

V15 must preserve the V14 structural result values unless hash replacement changes only provenance fields.

Expected preserved aggregate values:

trajectory_count: 20
event_count: 100
aggregate_risk_score: 0.379255
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.42
aggregate_extraction_rate: 0.9
highest_risk_trajectory: gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
highest_risk_score: 0.7096
highest_risk_provider: provider_b
highest_risk_run_id: provider_b_run_v14_002

Expected preserved regime counts:

{
  "CRITICAL": 4,
  "DRIFT": 10,
  "STABLE": 6
}

Expected strengthened values

V15 must report:

source_file_count: 4
source_file_hash_count: 4
real_source_file_hash_count: 4
placeholder_source_file_hash_count: 0
hash_format_failures: 0
hash_mismatch_failures: 0
missing_source_files: 0

Required aggregate additions

The V15 result must add these aggregate fields:

real_source_file_hash_count
placeholder_source_file_hash_count
hash_format_failure_count
hash_mismatch_failure_count
missing_source_file_count

Required top-level additions

The V15 result must add:

hash_strengthening_method
hash_algorithm
hash_verified
real_source_file_hashes
placeholder_hashes_replaced
hash_validation_failures

Expected values:

{
  "hash_strengthening_method": "computed_sha256_over_source_output_files",
  "hash_algorithm": "sha256",
  "hash_verified": true,
  "placeholder_hashes_replaced": true,
  "hash_validation_failures": []
}

Failure conditions

The validator must fail if:

any required source file is missing
any source file cannot be read
any computed hash is not sha256:<64 hex chars>
any placeholder hash remains in the V15 dataset
any placeholder hash remains in the V15 result
any event source_file_hash does not match its source_file
any result source_file_hash does not match its source_file
any source_file_hash_count is not 4
any trajectory_count changes from 20
any event_count changes from 100

Validation checks

The validator must print:

source_file_count
computed_hash_count
real_hash_count
placeholder_hash_count
hash_format_failure_count
hash_mismatch_failure_count
trajectory_count
event_count
aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action

Expected terminal success output

V15 HASH STRENGTHENING PASSED

Expected final state:

trajectory_count: 20
event_count: 100
source_file_count: 4
computed_hash_count: 4
real_hash_count: 4
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH

Relation to V14

V14 established repeated-run cross-provider stability.

V15 does not change the warning measurement.

V15 strengthens provenance.

The core transition is:

V14: source_file_hash placeholders
V15: real computed source_file_hash values

Relation to Level 3

Level 3 measures structural warning behavior.

V15 does not add a new warning axis.

V15 adds stronger source binding for the same mapped warning chain.

Canonical boundary statement

Temporal Collapse Level 3 remains a post-hoc structural warning layer.

V15 strengthens file provenance only.

It does not convert structural warning into semantic truth.

It does not convert benchmark evidence into final authority.

It does not decide.

It verifies source-file hash integrity.

Next expected files

After this specification, the next files are:

examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py
data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15_RESULT.md

Final boundary

hashes strengthen traceability.

They do not prove truth.

They do not prove correctness.

They do not prove model understanding.

They only bind mapped records to concrete source-file content.