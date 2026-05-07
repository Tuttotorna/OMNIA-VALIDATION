# Temporal Collapse Level 3 — Index V0

## Status

**ACTIVE**

This index tracks the Level 3 temporal-collapse validation chain.

Level 3 focuses on raw ordered structural trajectory events, repeated-run behavior, cross-provider behavior, collapse-like boundary proximity, and external-source traceability.

---

## Boundary

```text
Temporal Collapse Level 3 is a structural warning layer.

It measures ordered trajectory behavior.
It measures drift.
It measures boundary proximity.
It measures collapse-like structural signatures.
It measures repeated-run stability.
It measures cross-provider disagreement.
It strengthens source traceability.

It does not infer semantic truth.
It does not replace benchmark correctness.
It does not claim official benchmark scoring.
It does not claim that OMNIA solves GSM-Symbolic.
It does not make final decisions.
```

Core boundary:

```text
measurement != inference != decision
```

---

## Current Validation Chain

```text
V13: cross-provider disagreement validator
V14: repeated-run cross-provider stability validator
V15: external source hash strengthening validator
```

---

## Level 3 Purpose

Level 3 exists to test whether structured outputs remain stable under ordered perturbation, repeated runs, and provider variation.

The target is not “answer correctness” alone.

The target is structural behavior:

```text
Does the trajectory remain stable?
Does it drift?
Does it approach a boundary?
Does it become critical?
Does it collapse?
Does behavior differ across providers?
Does behavior remain stable across repeated runs?
Can the source trail be verified?
```

---

## Canonical Level 3 Objects

### Raw Ordered Structural Event

A Level 3 event is one ordered record inside a trajectory.

Each event may include:

```text
trajectory_id
step
template_id
question_id
variant_type
provider
model_name
model_version
run_id
run_index
run_group_id
response_id
source_file
source_file_hash
raw_question_hash
raw_output_hash
answer_extraction_method
expected_answer
model_final_answer
is_correct
signature
cluster
delta
iri
boundary_distance
phase
source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
source_record_reference
mapping_method
stability_group
cross_provider_group
cross_provider_role
mapping_notes
```

### Raw Ordered Structural Trajectory

A trajectory is an ordered sequence of events.

In the current GSM-Symbolic Level 3 chain:

```text
events_per_trajectory: 5
trajectory_count_v14_v15: 20
event_count_v14_v15: 100
```

### Structural Signals

Level 3 validators compute or preserve structural signals such as:

```text
transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal
```

### Risk Regimes

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
```

### Gate Actions

```text
PASS
WATCH
ESCALATE
```

The gate action is a warning recommendation only.

It is not a final decision.

---

## V13 — Cross-Provider Disagreement Validator

### File

```text
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13.md
```

### Result File

```text
results/temporal_collapse_cross_provider_disagreement_validator_v13.json
```

### Result Documentation

```text
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13_RESULT.md
```

### Purpose

V13 introduces cross-provider disagreement measurement.

It checks whether structurally similar tasks produce different risk behavior across provider mappings.

### Structural Role

```text
V13 = provider disagreement detection
```

### Boundary

```text
V13 does not prove which provider is correct.
V13 does not infer semantic truth.
V13 does not replace benchmark scoring.
V13 only measures structural disagreement.
```

---

## V14 — Repeated-Run Cross-Provider Stability Validator

### Validator Documentation

```text
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14.md
```

### Validator Script

```text
examples/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.py
```

### Dataset

```text
data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl
```

### Result File

```text
results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json
```

### Result Documentation

```text
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14_RESULT.md
```

### Purpose

V14 extends Level 3 by adding repeated-run and cross-provider stability structure.

It maps repeated-run real parsed GSM-Symbolic model-output file records into raw ordered structural trajectories.

### Structural Role

```text
V14 = repeated-run + cross-provider structural stability mapping
```

### V14 Summary

```text
experiment: temporal_collapse_repeated_run_cross_provider_stability_validator_v14
status: v14_repeated_run_cross_provider_stability_mapping
trajectory_count: 20
event_count: 100
provider_count: 2
run_count: 4
source_file_count: 4
stability_group_count: 10
cross_provider_group_count: 5
```

### V14 Aggregate Result

```text
aggregate_risk_score: 0.379255
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.42
aggregate_extraction_rate: 0.9
```

### V14 Regime Counts

```text
CRITICAL: 4
DRIFT: 10
STABLE: 6
```

### V14 Highest-Risk Trajectory

```text
gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
```

### V14 Highest-Risk Score

```text
0.7096
```

### V14 Highest-Risk Provider

```text
provider_b
```

### V14 Highest-Risk Run

```text
provider_b_run_v14_002
```

### V14 Boundary

```text
V14 does not claim official GSM-Symbolic scoring.
V14 does not claim that OMNIA solves GSM-Symbolic.
V14 does not infer semantic truth.
V14 does not make final decisions.
V14 measures structural trajectory behavior only.
```

---

## V15 — External Source Hash Strengthening Validator

### Validator Documentation

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15.md
```

### Validator Script

```text
examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py
```

### Input Dataset

```text
data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl
```

### Input Result

```text
results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json
```

### Output Dataset

```text
data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
```

### Output Result

```text
results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

### Result Documentation

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15_RESULT.md
```

### Purpose

V15 strengthens the V14 source trail.

V14 used symbolic `source_file_hash` placeholders.

V15 computes real SHA-256 hashes for the source-output files and rewrites the strengthened dataset with those real hashes.

### Structural Role

```text
V15 = V14 + real external source-file hash traceability
```

### V15 Summary

```text
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
```

### V15 Aggregate Result Preserved From V14

```text
aggregate_risk_score: 0.379255
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.42
aggregate_extraction_rate: 0.9
```

### V15 Highest-Risk Trajectory

```text
gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
```

### V15 Highest-Risk Score

```text
0.7096
```

### V15 Highest-Risk Provider

```text
provider_b
```

### V15 Highest-Risk Run

```text
provider_b_run_v14_002
```

### V15 Computed Source Hashes

```text
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl
sha256:24d7177cea63e44e2616c0d4546ed65fd824719f7fc4030b9a52130c1bf4e00c
```

```text
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_002.jsonl
sha256:602676324b4335e7cb670d6884cbe5e978dacac59889dbc362252440d706dc2e
```

```text
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_001.jsonl
sha256:5ab1f8a6bf24f266a8dbf4e4e952be749db66ae66156bff0835d44088bb8ac5a
```

```text
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_002.jsonl
sha256:5399edf34ba661ece7b6f0855df09ecad7d895a74951bd8bec56ad8074dd9010
```

### V15 Boundary

```text
V15 strengthens source traceability only.
V15 does not change the V14 structural risk logic.
V15 does not change the V14 trajectory mapping.
V15 does not infer semantic truth.
V15 does not claim official GSM-Symbolic scoring.
V15 does not claim that OMNIA solves GSM-Symbolic.
V15 does not make final decisions.
```

---

## Source Independence Chain

The current Level 3 chain uses the following source-independence fields:

```text
source_independence: external_source_verified
independence_method: repeated_run_cross_provider_stability_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name: GSM-Symbolic
source_record_type: repeated_run_real_model_output_file
mapping_method: repeated_run_real_model_output_file_to_trajectory
```

V15 strengthens this chain by replacing symbolic file hashes with real SHA-256 digests.

---

## Evidence Chain

The current Level 3 evidence chain is:

```text
1. Raw source-output files exist.
2. Source-output files have computed SHA-256 hashes.
3. Source records are mapped into ordered structural events.
4. Ordered structural events form trajectories.
5. Trajectories are grouped by provider.
6. Trajectories are grouped by repeated run.
7. Trajectories are grouped by cross-provider template group.
8. Structural risk signals are computed.
9. Repeated-run stability is summarized.
10. Cross-provider disagreement is summarized.
11. Aggregate structural risk is reported.
12. Boundary limitations are preserved.
```

---

## Current Level 3 Files

### Documentation

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13.md
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13_RESULT.md
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14.md
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14_RESULT.md
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15.md
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15_RESULT.md
```

### Scripts

```text
examples/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.py
examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py
```

### Datasets

```text
data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl
data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
```

### Source Outputs

```text
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_002.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_002.jsonl
```

### Results

```text
results/temporal_collapse_cross_provider_disagreement_validator_v13.json
results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json
results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

---

## Current Aggregate Level 3 Reading

The current strongest validated Level 3 result is V15.

V15 preserves the V14 structural measurement while strengthening source-file hash traceability.

The current aggregate reading is:

```text
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
highest_risk_regime: CRITICAL
highest_risk_provider: provider_b
highest_risk_run_id: provider_b_run_v14_002
highest_risk_trajectory: gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
highest_risk_score: 0.7096
```

Interpretation:

```text
The full repeated-run cross-provider set is not globally collapsed.
The aggregate condition is DRIFT.
The correct gate action is WATCH.
The highest-risk local trajectories are CRITICAL.
Collapse-like behavior appears locally, especially in template_005.
Provider-level differences remain visible.
Repeated-run variation is small.
Source-file hash traceability is now strengthened.
```

---

## Important Non-Claims

This repository does not claim:

```text
OMNIA solves GSM-Symbolic.
OMNIA replaces mathematical reasoning.
OMNIA replaces benchmark correctness.
OMNIA detects semantic truth.
OMNIA proves model intelligence.
OMNIA proves model failure.
OMNIA certifies production safety.
OMNIA makes final decisions.
```

It claims only:

```text
OMNIA measures structural behavior under ordered transformations and source-traceable validation conditions.
```

---

## Level 3 Summary

```text
V13 detects cross-provider disagreement.
V14 adds repeated-run cross-provider stability mapping.
V15 strengthens external source-file hash traceability.
```

Current chain:

```text
V13 -> V14 -> V15
```

Current status:

```text
ACTIVE
```

Current strongest result:

```text
V15 HASH STRENGTHENING PASSED
```

Current boundary:

```text
structural warning measurement only
```

Final invariant:

```text
measurement != inference != decision
```