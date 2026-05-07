# Temporal Collapse Level 3 — Final Summary V0

## Status

**ACTIVE SUMMARY**

This document summarizes the current Temporal Collapse Level 3 validation chain.

Current chain:

```text
V13 -> V14 -> V15
```

Current strongest result:

```text
V15 HASH STRENGTHENING PASSED
```

Current boundary:

```text
structural warning measurement only
```

Core invariant:

```text
measurement != inference != decision
```

---

## What Level 3 Tests

Temporal Collapse Level 3 tests whether ordered model-output trajectories remain structurally stable under variation.

It does not test only whether an answer is correct.

It tests structural behavior across:

```text
ordered perturbation
trajectory drift
boundary proximity
collapse-like signatures
provider variation
repeated runs
source-file traceability
```

The central question is:

```text
Does a system remain structurally stable when the task is changed, repeated, or observed across providers?
```

---

## What Level 3 Does Not Claim

Level 3 does not claim:

```text
OMNIA solves GSM-Symbolic.
OMNIA replaces benchmark correctness.
OMNIA detects semantic truth.
OMNIA proves model intelligence.
OMNIA proves model failure.
OMNIA certifies production safety.
OMNIA makes final decisions.
```

Level 3 only claims:

```text
OMNIA measures structural behavior under ordered transformations and traceable validation conditions.
```

---

## Why This Matters

A model can look correct on one surface output and still be structurally fragile.

A model can answer correctly at the beginning of a trajectory and then drift under small variations.

A model can remain correct across repeated runs but differ across providers.

A model can preserve extraction for some cases and lose extraction near collapse-like boundary conditions.

Level 3 measures these behaviors as ordered structural signals.

It does not explain why the model behaves that way.

It measures that the behavior occurred.

---

## Validation Chain

## V13 — Cross-Provider Disagreement

V13 introduced cross-provider disagreement measurement.

It tested whether structurally related trajectories show different behavior across provider mappings.

Structural role:

```text
V13 = provider disagreement detection
```

V13 helped establish that provider-level structural differences can be measured without claiming which provider is semantically correct.

Relevant files:

```text
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13.md
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13_RESULT.md
results/temporal_collapse_cross_provider_disagreement_validator_v13.json
```

Boundary:

```text
V13 measures disagreement.
V13 does not decide truth.
```

---

## V14 — Repeated-Run Cross-Provider Stability

V14 extended the chain by adding repeated-run structure.

It mapped repeated-run cross-provider GSM-Symbolic model-output records into ordered structural trajectories.

Structural role:

```text
V14 = repeated-run + cross-provider structural stability mapping
```

V14 measured:

```text
20 trajectories
100 ordered events
2 providers
4 runs
10 stability groups
5 cross-provider groups
```

Relevant files:

```text
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14.md
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14_RESULT.md
examples/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.py
data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl
results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json
```

V14 aggregate result:

```text
aggregate_risk_score: 0.379255
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.42
aggregate_extraction_rate: 0.9
```

V14 regime counts:

```text
CRITICAL: 4
DRIFT: 10
STABLE: 6
```

Highest-risk V14 trajectory:

```text
gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
```

Highest-risk score:

```text
0.7096
```

V14 showed that repeated-run variation was small, while cross-provider differences remained visible.

Boundary:

```text
V14 measures structural repeated-run and cross-provider behavior.
V14 does not claim official benchmark scoring.
V14 does not claim semantic truth.
```

---

## V15 — External Source Hash Strengthening

V15 strengthened V14 by replacing symbolic source-file hash placeholders with real computed SHA-256 hashes.

Structural role:

```text
V15 = V14 + real external source-file hash traceability
```

V15 did not change the V14 risk calculation.

It strengthened the source trail.

Relevant files:

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15.md
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15_RESULT.md
examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py
data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

V15 validation result:

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

Important result:

```text
real_hash_count: 4
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0
```

This means the source-file hashes are now real computed SHA-256 digests, not symbolic placeholders.

---

## V15 Computed Source Hashes

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

---

## Current Strongest Result

The strongest current Level 3 result is V15.

V15 preserves the V14 structural measurement while strengthening external-source traceability.

Current aggregate result:

```text
aggregate_risk_score: 0.379255
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.42
aggregate_extraction_rate: 0.9
```

Current highest-risk local trajectory:

```text
gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
```

Current highest-risk score:

```text
0.7096
```

Current highest-risk provider:

```text
provider_b
```

Current highest-risk run:

```text
provider_b_run_v14_002
```

---

## Interpretation

The current Level 3 chain supports this structural reading:

```text
The full repeated-run cross-provider set is not globally collapsed.
The aggregate condition is DRIFT.
The aggregate gate action is WATCH.
The highest-risk local trajectories are CRITICAL.
Collapse-like behavior appears locally.
The strongest local collapse-like behavior appears in template_005.
Provider-level differences remain visible.
Repeated-run variation remains small.
Source-file hash traceability is now strengthened.
```

This is a structural warning result.

It is not a semantic verdict.

---

## Core Evidence

The current evidence chain is:

```text
1. Source-output files exist.
2. Source-output files have real computed SHA-256 hashes.
3. Source records are mapped into ordered structural events.
4. Ordered events form trajectories.
5. Trajectories are grouped by repeated run.
6. Trajectories are grouped by provider.
7. Trajectories are grouped by cross-provider template group.
8. Structural signals are computed.
9. Repeated-run stability is summarized.
10. Cross-provider disagreement is summarized.
11. Aggregate structural risk is reported.
12. Source traceability is strengthened.
13. Boundary limitations are preserved.
```

---

## Structural Signals Used

Level 3 uses structural warning signals such as:

```text
transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal
```

These signals do not interpret the semantic meaning of the answer.

They measure the structural behavior of the trajectory.

---

## Risk Regimes

The current Level 3 regime vocabulary is:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
```

In the V14/V15 aggregate result:

```text
aggregate_risk_regime: DRIFT
```

Local high-risk trajectories can still be CRITICAL even when the aggregate regime is DRIFT.

That is the correct reading.

The system is not globally collapsed, but it contains local critical trajectories.

---

## Gate Actions

The current Level 3 gate-action vocabulary is:

```text
PASS
WATCH
ESCALATE
```

In the V14/V15 aggregate result:

```text
aggregate_gate_action: WATCH
```

That means:

```text
do not ignore the structural drift
do not claim global collapse
continue monitoring and inspecting high-risk trajectories
```

For the highest-risk local trajectories, the gate action is:

```text
ESCALATE
```

This is still a warning action, not a final decision.

---

## Why V15 Is Stronger Than V14

V14 already produced a repeated-run cross-provider structural measurement.

But V14 still used symbolic file-hash placeholders.

That left a weakness:

```text
source-file identity was documented, but not cryptographically strengthened
```

V15 reduces that weakness by computing real source-file SHA-256 hashes.

Therefore:

```text
V14 = structural repeated-run / cross-provider measurement
V15 = V14 + real source-file hash traceability
```

V15 does not make the claims larger.

It makes the traceability stronger.

---

## Clean Public Description

A concise public description of Level 3 is:

```text
Temporal Collapse Level 3 measures whether model-output trajectories remain structurally stable across perturbations, repeated runs, and providers.

The current V15 result preserves the V14 aggregate risk measurement while replacing symbolic source-file hash placeholders with real SHA-256 hashes.

Result: aggregate DRIFT / WATCH, with local CRITICAL collapse-like trajectories and strengthened source traceability.

This is measurement only, not semantic truth detection or final decision authority.
```

---

## One-Line Summary

```text
Level 3 shows aggregate DRIFT with local CRITICAL collapse-like trajectories, small repeated-run variation, visible cross-provider differences, and strengthened source-file hash traceability.
```

---

## Final Boundary

```text
OMNIA measures structural behavior.
OMNIA does not infer semantic truth.
OMNIA does not decide.
```

Final invariant:

```text
measurement != inference != decision
```