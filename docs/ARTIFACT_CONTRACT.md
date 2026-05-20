# Artifact Contract

This document defines what a validation artifact should contain.

OMNIA-VALIDATION exists to make claims inspectable.

An artifact is useful only if a reviewer can understand what produced it and what it does not prove.

---

## Minimal artifact schema

A validation artifact should contain:

    {
      "case_id": "stable-case-id",
      "input": "...",
      "transformation": "...",
      "measurement": {...},
      "result": "pass | flag | fail | inconclusive",
      "artifact_version": "v0",
      "generated_at": "ISO-8601 timestamp",
      "boundary": "measurement != inference != decision",
      "limitation": "What this artifact does not prove"
    }

---

## JSONL recommendation

For datasets and result streams, prefer JSONL.

One object per line.

Advantages:

- easy to diff;
- easy to append;
- easy to audit;
- easy to parse;
- compatible with small and large validation sets.

---

## Required discipline

Do not overwrite raw results without preserving provenance.

Do not mix generated explanations with raw measurements unless clearly separated.

Do not use a validation artifact as a semantic truth certificate.

---

## Artifact categories

Suggested artifact categories:

    artifacts/raw/
    artifacts/processed/
    artifacts/reports/
    artifacts/failures/
    artifacts/regressions/

If the repository later grows, this structure prevents confusion.

