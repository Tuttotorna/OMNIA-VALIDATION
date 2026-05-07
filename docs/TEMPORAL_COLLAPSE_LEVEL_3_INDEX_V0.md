# Temporal Collapse Level 3 — Index v0

## Purpose

This index tracks the Temporal Collapse Level 3 validation chain.

Level 3 is the raw trajectory warning layer.

It maps ordered structural events into trajectory-level risk measurements.

It does not solve benchmark tasks.

It does not infer semantic truth.

It does not replace benchmark correctness.

It does not make final decisions.

## Boundary

```text
measurement != inference != decision

structural warning != semantic correctness

risk_score != truth

gate_action != final authority

Level 3 definition

Temporal Collapse Level 3 measures structural warning behavior across ordered raw trajectory events.

Each trajectory is treated as a sequence.

The validator reads event-level fields such as:

step
signature
cluster
delta
iri
boundary_distance
phase

It then computes structural warning signals such as:

transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal

The output is a trajectory-level warning result:

risk_score
risk_regime
gate_action
dominant_axis
warning_flags
transition_evidence

Core risk regimes

Regime	Meaning

STABLE	low structural warning
DRIFT	structural instability or warning pressure
CRITICAL	collapse-like or high-risk structural behavior


Core gate actions

Gate action	Meaning

PASS	no immediate structural warning
WATCH	structural warning present
ESCALATE	high structural warning


Core thresholds

{
  "STABLE": 0.25,
  "DRIFT": 0.5,
  "CRITICAL": 0.75
}

Core weights

{
  "transition_density": 0.2,
  "drift_progression": 0.2,
  "boundary_proximity": 0.25,
  "collapse_similarity": 0.25,
  "irreversibility_signal": 0.1
}

Validation chain

Level 3 raw trajectory events
        |
        v
Temporal Collapse validator
        |
        v
trajectory-level warning results
        |
        v
aggregate warning profile
        |
        v
external decision layer

Important limitation

Level 3 does not claim that a model is correct or incorrect.

Level 3 measures structural behavior under ordered trajectory progression.

Correctness fields may be preserved as evidence.

Extraction fields may be preserved as evidence.

Provider fields may be preserved as evidence.

Run fields may be preserved as evidence.

But the structural risk score remains a warning measurement only.


---

Version map

V0 — Foundation

Scope

Initial Level 3 index and conceptual boundary.

Files

docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md

Status

active index


---

V1 — Raw trajectory warning mechanism

Scope

Initial raw trajectory collapse-warning formulation.

Purpose

Define how ordered structural events can be converted into trajectory-level warning measurements.

Boundary

raw structural trajectory warning only


---

V2 — Expanded warning evidence

Scope

Added richer transition evidence and warning-axis separation.

Purpose

Separate structural signal families instead of compressing all instability into one opaque score.

Signal families

transition_density
drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal


---

V3 — Gate action layer

Scope

Added explicit gate action mapping.

Purpose

Keep measurement separate from decision while allowing an external system to consume warning states.

Gate action space

PASS
WATCH
ESCALATE


---

V4 — Structural boundary clarification

Scope

Clarified that Level 3 is not semantic scoring.

Boundary

risk_score != correctness
risk_score != truth
risk_score != proof


---

V5 — Dataset mapping discipline

Scope

Introduced stricter mapping discipline from raw records to ordered structural events.

Purpose

Prevent uncontrolled narrative interpretation during validation.


---

V6 — Aggregate profile

Scope

Added aggregate-level reporting.

Aggregate fields

aggregate_risk_score
aggregate_risk_regime
aggregate_gate_action
regime_counts
highest_risk_trajectory
highest_risk_score


---

V7 — Source traceability

Scope

Added stronger source traceability fields.

Purpose

Preserve provenance for each trajectory event and result.

Traceability fields

source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
mapping_method
source_file
source_file_hash


---

V8 — Model-output mapping

Scope

Mapped model-output records into ordered structural trajectory events.

Purpose

Allow the Level 3 mechanism to operate on parsed real model-output-style records while preserving boundary constraints.

Boundary

model output record != semantic judgment


---

V9 — Correctness and extraction evidence

Scope

Added correctness and answer-extraction evidence.

Purpose

Preserve benchmark-facing evidence without letting it become the structural score itself.

Evidence fields

expected_answer
model_final_answer
is_correct
answer_extraction_method
correctness_profile
extraction_profile


---

V10 — GSM-Symbolic compatibility layer

Scope

Added GSM-Symbolic-style template and variant organization.

Purpose

Map GSM-Symbolic-style variants into ordered trajectories.

Preserved fields

template_id
question_id
variant_type
expected_answer
model_final_answer
is_correct


---

V11 — Real parsed source-output discipline

Scope

Strengthened real parsed model-output source discipline.

Purpose

Require file-level source fields, hash placeholders, source record references, and mapping notes.

Status

superseded by V12+


---

V12 — Multi-source real GSM-Symbolic model-output validator

Validator document

docs/TEMPORAL_COLLAPSE_MULTI_SOURCE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V12.md

Result document

docs/TEMPORAL_COLLAPSE_MULTI_SOURCE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V12_RESULT.md

Dataset

data/temporal_collapse_multi_source_real_gsm_symbolic_model_outputs_v12.jsonl

Result file

results/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.json

Scope

V12 applies the Level 3 raw trajectory warning mechanism to multi-source real parsed GSM-Symbolic model-output file records.

Boundary

multi-source real parsed GSM-Symbolic model-output file records mapped into raw ordered structural trajectory events

Status

PASSED

Core result

trajectory_count: 10
event_count: 50
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH

Purpose

V12 established that Level 3 can process multiple source-output files while preserving source independence fields, source references, correctness evidence, and extraction evidence.

Limitation

V12 does not claim official GSM-Symbolic scoring.

V12 does not claim semantic truth detection.

V12 does not make final decisions.


---

V13 — Cross-provider disagreement validator

Validator document

docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13.md

Result document

docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13_RESULT.md

Dataset

data/temporal_collapse_cross_provider_disagreement_v13.jsonl

Result file

results/temporal_collapse_cross_provider_disagreement_validator_v13.json

Scope

V13 applies the Level 3 raw trajectory warning mechanism to cross-provider real parsed GSM-Symbolic model-output file records.

Boundary

cross-provider real parsed GSM-Symbolic model-output file records mapped into raw ordered structural trajectory events

Status

PASSED

Core result

trajectory_count: 10
event_count: 50
aggregate_risk_score: 0.385325
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.4
aggregate_extraction_rate: 0.9
highest_risk_trajectory: gsm_symbolic_cross_provider_provider_b_collapse_like_001
highest_risk_score: 0.714417
highest_risk_provider: provider_b

Regime counts

{
  "CRITICAL": 2,
  "DRIFT": 5,
  "STABLE": 3
}

Providers

provider_a
provider_b

Cross-provider groups

gsm_symbolic_template_001_cross_provider_group
gsm_symbolic_template_002_cross_provider_group
gsm_symbolic_template_003_cross_provider_group
gsm_symbolic_template_004_cross_provider_group
gsm_symbolic_template_005_cross_provider_group

Main contribution

V13 adds cross-provider disagreement mapping.

It preserves provider identity, model identity, source-file identity, answer extraction, correctness fields, and cross-provider grouping.

The important addition is that Level 3 can compare structural warning behavior across provider-separated trajectories.

Observed pattern

stable template      -> both providers STABLE
drift template       -> provider disagreement appears
borderline template  -> both DRIFT, accuracy disagreement
critical template    -> both DRIFT
collapse-like        -> both CRITICAL, extraction disagreement

Limitation

V13 does not prove provider quality.

V13 does not certify benchmark performance.

V13 does not infer semantic truth.

V13 only reports structural warning behavior under the mapped trajectory mechanism.


---

V14 — Repeated-run cross-provider stability validator

Validator document

docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14.md

Result document

docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14_RESULT.md

Dataset

data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl

Result file

results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json

Scope

V14 applies the Level 3 raw trajectory warning mechanism to repeated-run cross-provider real parsed GSM-Symbolic model-output file records.

Boundary

repeated-run cross-provider real parsed GSM-Symbolic model-output file records mapped into raw ordered structural trajectory events

Status

PASSED

Core result

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

Regime counts

{
  "CRITICAL": 4,
  "DRIFT": 10,
  "STABLE": 6
}

Providers

provider_a
provider_b

Runs

provider_a_run_v14_001
provider_a_run_v14_002
provider_b_run_v14_001
provider_b_run_v14_002

Source files

data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_002.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_001.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_002.jsonl

Stability groups

gsm_symbolic_template_001_provider_a_repeated_run_group
gsm_symbolic_template_001_provider_b_repeated_run_group
gsm_symbolic_template_002_provider_a_repeated_run_group
gsm_symbolic_template_002_provider_b_repeated_run_group
gsm_symbolic_template_003_provider_a_repeated_run_group
gsm_symbolic_template_003_provider_b_repeated_run_group
gsm_symbolic_template_004_provider_a_repeated_run_group
gsm_symbolic_template_004_provider_b_repeated_run_group
gsm_symbolic_template_005_provider_a_repeated_run_group
gsm_symbolic_template_005_provider_b_repeated_run_group

Cross-provider groups

gsm_symbolic_template_001_cross_provider_repeated_run_group
gsm_symbolic_template_002_cross_provider_repeated_run_group
gsm_symbolic_template_003_cross_provider_repeated_run_group
gsm_symbolic_template_004_cross_provider_repeated_run_group
gsm_symbolic_template_005_cross_provider_repeated_run_group

Main contribution

V14 adds repeated-run stability on top of cross-provider comparison.

V13 asked whether structural warning behavior differs across providers.

V14 asks whether the structural warning behavior remains stable across repeated runs for the same provider and template.

This is a stronger validation step because it tests whether the warning profile is reproducible inside the mapped repeated-run structure.

Repeated-run stability result

The repeated-run risk spreads are small across all stability groups.

max repeated-run risk spread: 0.00315
min repeated-run risk spread: 0.00035

No repeated-run stability group shows risk-regime disagreement.

repeated_run_risk_regime_disagreement: false

Cross-provider result

Cross-provider differences remain visible.

The strongest divergence appears in the drift template group.

template_002 cross_provider_risk_spread: 0.06775
template_002 risk_regime_disagreement: true
template_002 accuracy_disagreement: true

The collapse-like group remains the strongest warning region.

template_005 highest_risk_provider: provider_b
template_005 highest_risk_run_id: provider_b_run_v14_002
template_005 highest_risk_score: 0.7096
template_005 risk_regime: CRITICAL

Observed pattern

stable template      -> low risk, full accuracy, full extraction
drift template       -> provider-level disagreement
borderline template  -> DRIFT with accuracy disagreement
critical template    -> high DRIFT, boundary proximity
collapse-like        -> CRITICAL, extraction failure, highest risk

Limitation

V14 does not prove model robustness.

V14 does not certify benchmark performance.

V14 does not infer semantic truth.

V14 does not make final decisions.

V14 only reports repeated-run and cross-provider structural warning behavior under the mapped trajectory mechanism.


---

Result comparison

V12 to V14

Version	Trajectories	Events	Main addition

V12	10	50	multi-source mapping
V13	10	50	cross-provider disagreement
V14	20	100	repeated-run stability


Aggregate comparison

Version	Risk score	Regime	Gate

V13	0.385325	DRIFT	WATCH
V14	0.379255	DRIFT	WATCH


Highest-risk comparison

Version	Provider	Score	Trajectory

V13	provider_b	0.714417	gsm_symbolic_cross_provider_provider_b_collapse_like_001
V14	provider_b	0.7096	gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001


Interpretation of comparison

V14 preserves the same broad warning profile as V13 while adding repeated-run stability.

The aggregate risk remains in DRIFT.

The highest-risk region remains provider_b collapse-like behavior.

The collapse-like trajectories remain CRITICAL.

The repeated-run spreads are very small, which supports stability of the mapped warning profile across repeated runs.


---

Canonical Level 3 boundary statement

Temporal Collapse Level 3 is a post-hoc structural warning layer.

It measures ordered structural trajectory behavior.

It does not solve the task.

It does not infer semantic truth.

It does not replace correctness scoring.

It does not make final decisions.

It reports warning measurements that an external decision layer may use.


---

Current canonical file set

Documentation

docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
docs/TEMPORAL_COLLAPSE_MULTI_SOURCE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V12.md
docs/TEMPORAL_COLLAPSE_MULTI_SOURCE_REAL_GSM_SYMBOLIC_MODEL_OUTPUT_VALIDATOR_V12_RESULT.md
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13.md
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13_RESULT.md
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14.md
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14_RESULT.md

Data

data/temporal_collapse_multi_source_real_gsm_symbolic_model_outputs_v12.jsonl
data/temporal_collapse_cross_provider_disagreement_v13.jsonl
data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl

Results

results/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.json
results/temporal_collapse_cross_provider_disagreement_validator_v13.json
results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json

Validators

examples/temporal_collapse_multi_source_real_gsm_symbolic_model_output_validator_v12.py
examples/temporal_collapse_cross_provider_disagreement_validator_v13.py
examples/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.py


---

Current highest validation level

V14 — Repeated-run cross-provider stability validator

Current status

PASSED

Current aggregate state

aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH

Current strongest warning

trajectory: gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
provider: provider_b
run_id: provider_b_run_v14_002
risk_score: 0.7096
risk_regime: CRITICAL
gate_action: ESCALATE


---

Next logical extensions

V15 — External-source hash strengthening

Replace placeholder source-file hashes with real computed hashes.

Purpose:

strengthen source traceability

Expected addition:

real sha256 file hashes
hash verification check
hash mismatch failure mode

V16 — Real benchmark reference binding

Bind each mapped record more tightly to a public benchmark reference.

Purpose:

reduce ambiguity between synthetic mapping and externally documentable benchmark-derived records

Expected addition:

benchmark_reference_url
benchmark_commit_or_snapshot
template_source_reference
question_source_reference

V17 — Provider/model anonymization protocol

Formalize provider/model anonymization.

Purpose:

separate structural validation from vendor claims

Expected addition:

provider_alias_policy
model_alias_policy
non-identification boundary

V18 — Full replay validator

Add a replay validator that regenerates dataset, result, and summaries from a clean repository clone.

Purpose:

make the validation chain reproducible from zero

Expected addition:

single clean-run script
dataset validation
result validation
summary validation
boundary assertions


---

Final boundary

Level 3 measures structural warning behavior.

It does not claim truth.

It does not claim correctness.

It does not claim model understanding.

It does not claim benchmark authority.

It does not decide.

It measures.