# Cross-Domain Invariance v0.1 — Result

## Status

```text
PASS

Evidence Level

Level 1 — Toy Demonstration

Experiment

cross_domain_invariance_v0_1

Repository

OMNIA-VALIDATION


---

Purpose

This experiment repeats the failed cross_domain_invariance_v0 test, but adds a minimal canonical structural projection before distance measurement.

The goal is to test whether structural family identity becomes visible after removing surface representation effects.

Core question:

can normalization recover structural invariance
that was hidden by representation?


---

Core Boundary

measurement != inference != decision

The experiment measures structural proximity only.

It does not:

infer meaning

prove semantic truth

validate universal invariance

validate the full OMNIA engine

prove representation-free mathematics



---

Background

The previous experiment:

cross_domain_invariance_v0

produced:

FAIL / NEGATIVE_RESULT

Main finding:

without normalization,
representation dominates structure

In v0, same-family representations were farther apart than cross-family representations.

That failure motivated this v0.1 test.


---

Core Change From v0

The key addition in v0.1 is:

canonical structural projection

Pipeline:

raw representation
->
token extraction
->
first-seen-symbol mapping
->
canonical sequence
->
structural signature
->
distance analysis

The projection removes:

lexical surface form

separators

JSON formatting

word identity

digit identity


while preserving:

symbolic order

transition structure

number of distinct states

repeated sequence pattern



---

Canonical Projection Example

Family A representations:

ABABAB...
1 0 1 0...
left|right|left|right...
{"x":0},{"x":1}...

all become:

010101010101...

Family B representations:

ABCDABCD...
1 2 3 4...
north|east|south|west...
{"s":1},{"s":2},{"s":3},{"s":4}...

all become:

012301230123...

This is the key normalization step.


---

Structural Families

Family A

Two-state alternating structure:

010101...

Family B

Four-state cyclic structure:

01230123...

The experiment tests whether these families become distinguishable after canonical projection.


---

Structural Signature

The v0.1 toy structural signature included:

entropy
compression_ratio
repetition_score
transition_regular_score
unique_symbol_ratio
periodicity_score
transition_cardinality_score
omega_proxy

Important:

this is not the full OMNIA engine

This is a toy normalization-aware structural proxy.


---

PASS Criterion

The pass condition was:

normalized_within_lower_than_cross == true
AND
normalized_margin > raw_margin
AND
normalized_margin > 0.05

Meaning:

same-family distance must become lower than cross-family distance

normalized geometry must improve over raw geometry

the improvement must have non-trivial margin



---

Raw Result

Before canonical projection:

mean_within_structure_distance = 1.19856921513
mean_cross_structure_distance  = 1.073203798097
separation_margin              = -0.125365417032
within_lower_than_cross        = False

Interpretation:

raw representation failed

The same failure mode from v0 remained visible:

representation dominates structure


---

Normalized Result

After canonical projection:

mean_within_structure_distance = 0.0
mean_cross_structure_distance  = 1.001258557732
separation_margin              = 1.001258557732
within_lower_than_cross        = True

Interpretation:

normalization recovered structural family separation

The same-structure representations collapsed into identical canonical forms.

Different structures remained separated.


---

Margin Improvement

Raw margin:

-0.125365417032

Normalized margin:

1.001258557732

Improvement:

normalized_margin > raw_margin

Result:

True

This is the strongest evidence in the experiment.


---

Observed Canonical Forms

Family A

All A representations normalized to:

010101010101010101010101010101...

Family B

All B representations normalized to:

012301230123012301230123012301...

This means the projection removed representation differences while preserving structural family identity.


---

Observed Omega Values

Raw omega values varied by representation:

A_letters_compact -> 0.96612988567
A_digits_spaced   -> 0.97541242909
A_words_pipe      -> 0.825141710974
A_json_like       -> 0.962356286022

B_letters_compact -> 0.949034393852
B_digits_spaced   -> 0.960223930942
B_words_pipe      -> 0.814181313735
B_json_like       -> 0.957654078506

After normalization:

A_* -> 0.96612988567
B_* -> 0.949034393852

This confirms that representation-specific variation was removed.


---

Main Result

The main result is:

canonical projection converted a FAIL into a PASS

More precisely:

raw geometry:
same-family distance > cross-family distance

normalized geometry:
same-family distance = 0
cross-family distance > 0


---

Main Insight

Main insight:

representation normalization can recover structural invariance
that naive raw signatures fail to detect

This is one of the strongest results so far in OMNIA-VALIDATION.


---

Why This Matters

This experiment directly supports the need for a representation layer before structural measurement.

It connects:

OMNIABASE
->
normalization / representation handling

with:

OMNIA
->
structural measurement

and:

OMNIA-VALIDATION
->
falsification and recovery testing

The result shows that raw measurement can fail, while normalized measurement can recover structure.


---

What This Experiment Does NOT Prove

This experiment does NOT prove:

universal invariance

semantic truth

full OMNIA correctness

representation-free mathematics

domain-independent generalization

robust invariance under adversarial transformations


The canonical projection is hand-built.

The test is small.

The result is only a toy demonstration.


---

Limitations

The experiment has several limitations:

toy dataset

only two structural families

only four representations per family

hand-built normalization

no learned projection

no noisy representations

no partial corruption

no adversarial representation

no real-world data

no external reproduction

no full OMNIA engine integration



---

Why The Result Is Still Important

The result is important because it shows the full validation arc:

v0:
naive measurement failed

v0.1:
normalization-aware measurement passed

This gives a concrete experimental chain:

failure
->
diagnosis
->
normalization
->
recovery

That is a strong research pattern.


---

Failure-Recovery Chain

v0

raw signatures
->
representation dominates
->
FAIL / NEGATIVE_RESULT

v0.1

canonical projection
->
representation removed
->
structure becomes visible
->
PASS

This is exactly the kind of chain OMNIA-VALIDATION should preserve.


---

JSON Result

Generated file:

results/cross_domain_invariance_v0_1.json

Key fields:

{
  "status": "PASS",
  "raw_analysis": {
    "mean_within_structure_distance": 1.19856921513,
    "mean_cross_structure_distance": 1.073203798097,
    "separation_margin": -0.125365417032,
    "within_lower_than_cross": false
  },
  "normalized_analysis": {
    "mean_within_structure_distance": 0.0,
    "mean_cross_structure_distance": 1.001258557732,
    "separation_margin": 1.001258557732,
    "within_lower_than_cross": true
  }
}


---

Reproduction Command

Run from repository root:

python examples/cross_domain_invariance_v0_1.py

Expected classification:

PASS

Expected core result:

normalized_margin > raw_margin

and:

within_lower_than_cross = True

after normalization.


---

Colab Reproduction

The experiment was reproduced in a clean Colab environment.

Observed summary:

Status: PASS

Raw margin:
-0.125365417032

Normalized margin:
1.001258557732

Normalized margin > raw margin:
True

Normalized within lower than cross:
True

Return code:

0

The experiment executed correctly.


---

Result Classification

Operational classification:

PASS

Reason:

canonical projection recovered structural family separation
after raw representation geometry failed

Evidence level:

Level 1 — Toy Demonstration


---

Main Conclusion

Main conclusion:

normalization is not optional

For representation-sensitive structural measurement, normalization is part of the measurement architecture.

Without normalization:

representation can dominate structure

With canonical projection:

structural family identity can become measurable


---

Recommended Next Step

Recommended next experiment:

examples/cross_domain_invariance_v0_2.py

Goal:

test whether normalization still works
when representations contain noise,
partial corruption,
or non-perfect mapping

Possible additions:

noisy tokens

missing symbols

extra separators

partial corruption

symbol swaps

longer families

multiple structural classes

imperfect canonicalization


Core next question:

does normalization recover structure
only in clean toy cases,
or also under noisy representation?