# OMNIA Problem Statement and Examples

This document answers the external question:

```text
What concrete problem is OMNIA trying to solve?
```

Short answer:

```text
OMNIA detects cases where an output is correct in one observed form
but structurally unstable under controlled transformations.
```

Compressed version:

```text
Correct once does not mean stable.
```

Core boundary:

```text
measurement != inference != decision
```

OMNIA is not a model.
OMNIA is not a judge.
OMNIA is not a semantic truth engine.
OMNIA is a post-hoc structural measurement layer.

---

## 1. The practical problem

Most LLM evaluation pipelines ask a question like:

```text
Did the model give the correct answer?
```

That is necessary, but incomplete.

A model can answer correctly in one surface form and fail when the same underlying task is transformed.

Examples of transformations:

```text
rephrasing
reordering
adding irrelevant clauses
changing representation
changing numeric base
changing symbolic form
changing context order
changing surface syntax
```

The practical failure looks like this:

```text
base_surface_correct: true
all_surface_correct: false
```

Meaning:

```text
The original answer passed.
The transformed variants exposed instability.
```

This is the gap OMNIA targets.

---

## 2. What normal evaluation misses

Normal evaluation often observes one answer under one form.

Example:

```text
Prompt A -> Model output -> Correct
```

This can hide structural fragility.

OMNIA asks a different question:

```text
If the same underlying task is transformed,
does the output remain structurally compatible?
```

So the evaluation changes from:

```text
single observed correctness
```

to:

```text
stability across controlled transformations
```

This matters because real deployed systems do not receive only one clean canonical prompt.

They receive:

```text
paraphrases
longer contexts
irrelevant additions
different orderings
different representations
user-specific formulations
domain-specific noise
```

A model that is correct only in the original form may still be fragile in deployment.

---

## 3. Minimal example

Original task:

```text
A box contains 3 red balls and 2 blue balls.
How many balls are in the box?
```

Expected answer:

```text
5
```

Model output:

```text
There are 5 balls in the box.
```

Surface evaluation:

```text
base_surface_correct: true
```

Now transform the same task.

Transformation 1: reordering

```text
A box contains 2 blue balls and 3 red balls.
How many balls are in the box?
```

Transformation 2: irrelevant clause

```text
A box contains 3 red balls and 2 blue balls.
The box is on a wooden table.
How many balls are in the box?
```

Transformation 3: representation shift

```text
A box contains three red balls and two blue balls.
How many balls are in the box?
```

If the model fails one or more transformed variants, the result becomes:

```text
base_surface_correct: true
all_surface_correct: false
```

OMNIA-style interpretation:

```text
The answer was correct in the base form,
but the behavior was structurally unstable under transformation.
```

Signal:

```text
FRAGILE
```

---

## 4. Concrete use case

A team already has a normal LLM evaluation pipeline.

Their existing pipeline checks:

```text
accuracy
exact match
semantic similarity
human preference
unit tests
benchmark score
```

OMNIA does not replace that pipeline.

OMNIA adds a post-hoc structural robustness layer next to it.

Typical workflow:

```text
1. Take an evaluated model output.
2. Generate or provide controlled transformations of the same task.
3. Run the same model or system on transformed variants.
4. Compare structural compatibility across outputs.
5. Emit an evidence package.
6. Let the downstream quality gate decide what to do.
```

The output is not a deployment decision.

The output is evidence.

---

## 5. What OMNIA outputs

A contract-compatible OMNIA validation run emits:

```text
certificate.json
failures.jsonl
summary.md
exit_code
```

Example certificate status:

```text
PASS
STRUCTURAL_FAILURE
LIMIT_REACHED
INVALID_INPUT
INCOMPLETE_EVIDENCE
INTERNAL_ERROR
```

Example exit codes:

```text
0 = PASS
1 = INTERNAL_ERROR
2 = STRUCTURAL_FAILURE
3 = LIMIT_REACHED
4 = INVALID_INPUT
5 = INCOMPLETE_EVIDENCE
```

Example interpretation:

```text
Exit 2 means the measured structure failed the configured structural gate.
It does not mean the semantic answer is false.
It does not mean deployment is forbidden.
It means structural evidence should block or trigger review according to the surrounding governance policy.
```

---

## 6. Transformation operators

This section defines the minimal operator vocabulary used by the examples.

An operator is a controlled change applied to the observed task or representation.

The goal is not to change the underlying task.

The goal is to test whether the model behavior remains structurally stable when the task is presented differently.

### 6.1 Rephrase

Preserves the task but changes wording.

```text
T_rephrase(x)
```

Example:

```text
Original:
How many balls are in the box?

Rephrased:
What is the total number of balls in the box?
```

Expected structural behavior:

```text
The answer should remain compatible.
```

---

### 6.2 Reorder

Preserves the task but changes the order of information.

```text
T_reorder(x)
```

Example:

```text
Original:
3 red balls and 2 blue balls

Reordered:
2 blue balls and 3 red balls
```

Expected structural behavior:

```text
The answer should remain compatible.
```

---

### 6.3 Add irrelevant clause

Adds information that should not affect the answer.

```text
T_irrelevant(x)
```

Example:

```text
Original:
A box contains 3 red balls and 2 blue balls.

Transformed:
A box contains 3 red balls and 2 blue balls.
The box is on a wooden table.
```

Expected structural behavior:

```text
The answer should remain compatible.
```

---

### 6.4 Representation shift

Changes the representation while preserving the underlying task.

```text
T_repr(x)
```

Example:

```text
Original:
3 red balls and 2 blue balls

Representation shift:
three red balls and two blue balls
```

Expected structural behavior:

```text
The answer should remain compatible.
```

---

### 6.5 Numeric base shift

Changes numeric representation.

```text
T_base_b(x)
```

Example:

```text
Base 10:
4

Base 2:
100
```

Expected structural behavior:

```text
The represented quantity should remain compatible.
```

This operator is especially relevant to OMNIABASE.

---

### 6.6 Symbolic form shift

Changes symbolic presentation while preserving the underlying structure.

```text
T_symbolic(x)
```

Example:

```text
Original:
2 + 3

Symbolic shift:
a + b where a = 2 and b = 3
```

Expected structural behavior:

```text
The result should remain compatible.
```

---

## 7. Minimal formal view

Let:

```text
x = original task
y = model output
T_i = controlled transformation
M = model or system under test
```

Normal evaluation observes:

```text
M(x) -> y
```

OMNIA-style structural validation observes:

```text
M(x)
M(T_1(x))
M(T_2(x))
...
M(T_n(x))
```

Then it asks:

```text
Are the outputs structurally compatible across the transformation family?
```

Compressed:

```text
stable(M, x, {T_i}) = compatible(M(x), M(T_i(x))) for all i
```

If the base output is correct but compatibility breaks:

```text
correct(M(x)) = true
stable(M, x, {T_i}) = false
```

Then the case is:

```text
surface-correct but structurally fragile
```

---

## 8. Where OMNIA fits

OMNIA fits after generation and before deployment decision.

```text
input
  -> model/system output
  -> normal evaluation
  -> OMNIA structural validation
  -> evidence package
  -> external quality gate / human review / CI policy
```

OMNIA does not replace:

```text
benchmarks
unit tests
human review
red teaming
formal verification
domain-specific validation
governance
```

OMNIA adds:

```text
post-hoc structural robustness evidence
```

---

## 9. Target domains

Primary domains:

```text
LLM evaluation
robustness testing
failure-mode detection
silent failure detection
pre-deployment quality gates
regression testing
model comparison under perturbation
```

Secondary domains:

```text
representation analysis
multi-base observation
symbolic reasoning stability
pipeline auditing
structural drift detection
```

---

## 10. What OMNIA does not claim

OMNIA does not claim:

```text
the answer is true
the model understands
the system is safe
the model should be deployed
the model should not be deployed
the benchmark is solved
```

OMNIA claims only:

```text
under the configured transformations and checks,
the observed structure remained stable
```

or:

```text
under the configured transformations and checks,
the observed structure became unstable
```

That is the boundary.

---

## 11. Minimal external explanation

For an outside viewer, the simplest explanation is:

```text
OMNIA is a structural robustness layer for AI evaluation.

It checks whether outputs that look correct in one form remain stable
when the same task is transformed.

If correctness passes but stability breaks, OMNIA emits a fragility signal.
```

Even shorter:

```text
OMNIA tests whether a correct answer is also structurally stable.
```

---

## 12. One-line problem statement

```text
Current LLM evaluation can miss outputs that are correct once
but unstable under controlled transformations.
```

OMNIA addresses that gap by producing:

```text
auditable structural evidence
```

not:

```text
semantic judgment
```

Final boundary:

```text
measurement != inference != decision
```
