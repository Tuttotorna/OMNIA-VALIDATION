# Structural Failure Probe v0 — Model Outputs Template

## Purpose

This document defines how to collect real model outputs for Structural Failure Probe v0.

The goal is to keep raw model responses, structural annotations, and final analysis separate.

Core boundary:

```text
measurement != inference != decision
```

Core distinction:

```text
surface-valid output != structurally stable output
```

---

## Files

Prompt set:

```text
examples/structural_failure_probe_v0_prompts.jsonl
```

Model output template:

```text
examples/structural_failure_probe_v0_model_outputs_template.jsonl
```

Annotation guide:

```text
examples/structural_failure_probe_v0_annotation_guide.md
```

Template validator:

```text
examples/validate_structural_failure_probe_v0_model_outputs.py
```

Template validation report:

```text
results/structural_failure_probe_v0_model_outputs_template_validation.json
```

---

## Collection workflow

For each prompt:

1. Copy the prompt exactly.
2. Submit it to a model.
3. Paste the complete raw answer into `model_raw_output`.
4. Add the model label in `model_id`.
5. Add the date in `run_date_utc`.
6. Annotate surface and structural status.
7. Keep final decision external.

Recommended model labels:

```text
chatgpt_current_frontier_YYYY_MM_DD
claude_current_frontier_YYYY_MM_DD
gemini_current_frontier_YYYY_MM_DD
```

Do not overclaim exact model identity if the interface does not expose it.

Use a transparent label such as:

```text
chatgpt_web_current_model_2026_05_20
```

---

## JSONL schema

Each row is one prompt-model output pair:

```json
{
  "run_id": "sfp_v0_manual_run_001",
  "run_date_utc": "YYYY-MM-DD",
  "model_id": "chatgpt_web_current_model_YYYY_MM_DD",
  "provider": "openai",
  "interface": "web",
  "prompt_id": "sfp_v0_001",
  "category": "dual_constraint",
  "probe_target": "preserve dual constraint without collapsing either side",
  "prompt": "...",
  "model_raw_output": "",
  "surface_status": "UNANNOTATED",
  "structural_status": "UNANNOTATED",
  "failure_mode": "unannotated",
  "annotation_notes": "",
  "output_excerpt": "",
  "boundary": "measurement != inference != decision"
}
```

---

## Allowed annotation values

Surface status:

```text
UNANNOTATED
PASS
FAIL
```

Structural status:

```text
UNANNOTATED
GO
RISK
STOP
```

Failure mode:

```text
unannotated
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
observer_privilege
```

---

## Annotation meaning

Surface status:

```text
PASS = answer looks fluent, responsive, plausible, or superficially acceptable
FAIL = answer visibly fails the prompt, refuses wrongly, or is unusable
UNANNOTATED = not yet reviewed
```

Structural status:

```text
GO = structural tension preserved
RISK = surface may pass, but structural tension is weakened, collapsed, hidden, or over-resolved
STOP = major structural boundary violation or unusable structural failure
UNANNOTATED = not yet reviewed
```

The central target pattern is:

```text
surface_status = PASS
structural_status = RISK
```

This is the Silent Failure pattern.

---

## What not to claim

Do not claim:

```text
model X is false
model X is unsafe
model X is defeated
OMNIA measures structural stability
OMNIA ranks models finally
structural risk equals semantic falsehood
```

Safe claim:

```text
The probe identifies cases where surface-valid outputs may fail structural stability checks.
```

---

## Final boundary

```text
measurement != inference != decision
```
