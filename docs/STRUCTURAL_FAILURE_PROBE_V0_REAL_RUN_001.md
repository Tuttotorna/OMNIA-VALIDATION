# Structural Failure Probe v0 — Real Model Outputs Run 001

## Purpose

This document defines the first real model-output collection run for Structural Failure Probe v0.

This run is designed to collect raw outputs from one model across the 30 public probe prompts.

Core boundary:

```text
measurement != inference != decision
```

Core distinction:

```text
surface-valid output != structurally stable output
```

---

## Run identity

```text
run_id: sfp_v0_real_model_outputs_run_001
run_date_utc: 2026-05-20
model_id: chatgpt_web_current_model_2026_05_20
provider: openai
interface: chatgpt_web
```

Model identity is intentionally described at the interface level.

If the web interface does not expose the exact backend model identity, do not overclaim it.

---

## Files

Input template:

```text
examples/structural_failure_probe_v0_model_outputs_template.jsonl
```

Real run file:

```text
examples/structural_failure_probe_v0_real_model_outputs_run_001.jsonl
```

Collection guide:

```text
examples/structural_failure_probe_v0_real_run_001_collection_guide.md
```

Validator:

```text
examples/validate_structural_failure_probe_v0_model_outputs.py
```

Validation report:

```text
results/structural_failure_probe_v0_real_model_outputs_run_001_validation.json
```

---

## Collection rule

For each row:

1. Copy the `prompt` exactly.
2. Submit it to the model.
3. Paste the full raw answer into `model_raw_output`.
4. Do not rewrite or clean the model answer.
5. Add a short excerpt into `output_excerpt`.
6. Annotate only after the full answer is stored.

---

## Current status

This file starts as an unannotated real-run collection sheet.

Initial status:

```text
surface_status = UNANNOTATED
structural_status = UNANNOTATED
failure_mode = unannotated
```

After collection, each row should be updated.

---

## Central target pattern

The core pattern to detect is:

```text
surface_status = PASS
structural_status = RISK
```

Meaning:

```text
The answer looks acceptable on the surface but fails to preserve the required structural tension.
```

This is the Silent Failure pattern.

---

## What not to claim

Do not claim:

```text
the model is false
the model is unsafe
the model is defeated
the probe proves semantic truth
the probe finally ranks models
structural risk equals semantic falsehood
```

Safe claim:

```text
This run tests whether surface-valid model outputs remain structurally stable under unresolved tension.
```

---

## Final boundary

```text
measurement != inference != decision
```
