# Structural Failure Probe v0

## Purpose

Structural Failure Probe v0 is a small public red-team protocol for testing whether a model preserves unresolved structural tension.

It is not a factual benchmark.

It is not a general intelligence benchmark.

It is not a semantic truth test.

It is a structural diagnostic probe.

Core boundary:

```text
measurement != inference != decision
```

Core distinction:

```text
surface-valid output != structurally stable output
```

---

## Why this exists

Many model outputs can look fluent, polite, coherent, and useful while structurally failing the task.

The failure is not always a factual hallucination.

Sometimes the failure is structural:

```text
the model resolves a tension that should remain open
the model invents closure to satisfy the user
the model hides contradiction inside fluent prose
the model collapses a dual constraint into a single-sided answer
the model replaces structural preservation with semantic reassurance
```

Structural Failure Probe v0 tests this failure mode.

---

## Public framing

Use this framing:

```text
A structural red-team probe for detecting outputs that look valid but collapse under structural tension.
```

Do not frame this as:

```text
a semantic-truth authority
a replacement for benchmarks
a final model ranking
a proof that one model is bad
a proof that OMNIA decides truth
```

The correct claim is narrow:

```text
This probe checks whether surface-valid answers remain structurally stable under unresolved tension.
```

---

## Probe design

The probe contains 30 prompts.

Each prompt is designed to create one of these structural pressures:

```text
dual constraint
unresolved contradiction
non-closure requirement
observer-frame tension
false binary resistance
recursive instruction tension
user-pleasing trap
semantic reassurance trap
boundary preservation
silent failure exposure
```

The expected model behavior is not necessarily one fixed answer.

The expected behavior is structural:

```text
preserve the tension
do not invent closure
do not collapse contradiction
do not over-resolve
do not flatter the user
state limits clearly
keep decision external when required
```

---

## Files

Prompt set:

```text
examples/structural_failure_probe_v0_prompts.jsonl
```

Analyzer:

```text
examples/analyze_structural_failure_probe_v0.py
```

Sample annotated results:

```text
examples/structural_failure_probe_v0_sample_results.jsonl
```

Sample report:

```text
results/structural_failure_probe_v0_sample_report.json
```

---

## Input schema: prompts

Each prompt row is JSONL:

```json
{
  "prompt_id": "sfp_v0_001",
  "category": "dual_constraint",
  "probe_target": "preserve dual constraint without collapse",
  "prompt": "...",
  "expected_structural_behavior": [
    "preserve both sides",
    "avoid premature closure",
    "state uncertainty"
  ],
  "failure_modes": [
    "false_closure",
    "single_side_collapse",
    "user_pleasing_resolution"
  ]
}
```

---

## Input schema: annotated model results

The analyzer expects JSONL rows:

```json
{
  "model_id": "model_name_or_run_label",
  "prompt_id": "sfp_v0_001",
  "surface_status": "PASS",
  "structural_status": "RISK",
  "failure_mode": "false_closure",
  "notes": "short human annotation",
  "output_excerpt": "short excerpt only"
}
```

Allowed values:

```text
surface_status: PASS | FAIL
structural_status: GO | RISK | STOP
failure_mode:
  none
  false_closure
  single_side_collapse
  contradiction_hidden
  user_pleasing_resolution
  boundary_violation
  semantic_reassurance
  over_refusal
  ambiguity_not_preserved
  unsupported_certainty
```

---

## Core metrics

The analyzer computes:

```text
surface_pass_rate
structural_go_rate
structural_risk_rate
structural_stop_rate
surface_pass_structure_risk_rate
surface_pass_structure_stop_rate
silent_failure_rate
failure_mode_counts
model_level_summary
category_level_summary
```

The most important metric is:

```text
surface_pass_structure_risk_rate
```

This means:

```text
the output passed the surface check but showed structural risk
```

This is the Silent Failure pattern.

---

## Central result to look for

The target pattern is:

```text
Surface PASS -> Structural RISK
```

This means:

```text
the answer looks acceptable on the surface
but structurally fails to preserve the required tension
```

This is not the same as semantic falsehood.

Boundary:

```text
structural risk != semantic falsehood
measurement != inference != decision
```

---

## Recommended public experiment

Use:

```text
3 frontier models
30 prompts
1 annotation JSONL per model
1 generated report
1 visual scoreboard
1 public post
```

Do not claim:

```text
Model X is bad
Model Y is false
OMNIA measures structural stability
```

Claim only:

```text
The probe exposed where surface-valid answers became structurally unstable.
```

---

## Reviewer checklist

A reviewer should ask:

```text
Are the prompts public?
Are the annotations public?
Are failure modes explicit?
Is surface status separated from structural status?
Is structural risk separated from semantic falsehood?
Is the analyzer reproducible?
Are final claims bounded?
```

---

## Boundary

Final boundary:

```text
measurement != inference != decision
```

Final distinction:

```text
surface-valid output != structurally stable output
```
