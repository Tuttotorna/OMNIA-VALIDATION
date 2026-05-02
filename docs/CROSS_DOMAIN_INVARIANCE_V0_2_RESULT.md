# Cross-Domain Invariance v0.2 — Result

## Status

```text
PASS

Evidence Level

Level 1 — Toy Demonstration

Experiment

cross_domain_invariance_v0_2

Repository

OMNIA-VALIDATION


---

Purpose

This experiment tests whether normalization-aware structural invariance survives imperfect representation.

The previous clean test:

cross_domain_invariance_v0_1

showed that canonical projection can recover structural family separation when representations are clean.

This v0.2 experiment asks a harder question:

does normalization still preserve structural family separation
when representations contain deterministic noise?


---

Core Boundary

measurement != inference != decision

The experiment measures structural proximity only.

It does not:

infer meaning

prove semantic truth

validate universal invariance

validate the full OMNIA engine

prove production robustness

prove representation-free mathematics



---

Background

The validation chain so far:

v0:
raw signatures failed
representation dominated structure

v0.1:
canonical projection recovered structure
under clean representations

v0.2:
canonical projection is tested under noisy representations

This experiment therefore moves from:

clean invariance

to:

noisy invariance with graceful degradation


---

Core Question

The central question was:

can normalized structural measurement preserve family separation
under imperfect representation?

Secondary question:

does normalized omega degrade as noise increases?

This is important because a useful structural layer should not behave only as a binary clean/fail detector.

It should show degradation.


---

Structural Families

Two toy structural families were tested.

Family A

Two-state alternating structure:

0101010101...

Family B

Four-state cyclic structure:

0123012301...

Each family was encoded in multiple surface representations and deterministic noise levels.


---

Representations

Representations included:

letters_compact
digits_spaced
words_pipe
json_like

Each representation had increasing deterministic corruption.

Noise levels:

0 -> clean
1 -> sparse unknown tokens
2 -> unknown tokens + local swaps
3 -> unknown tokens + swaps + deletions

No randomness was used.


---

Normalization Method

The experiment used a minimal canonical structural projection.

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

lexical identity

separators

JSON formatting

word form

digit form


while preserving:

symbolic order

transition structure

repeated pattern

corruption residue

additional noisy states


Because noisy tokens remain tokens, normalization is not perfect.

This is intentional.


---

Structural Signature

The toy structural signature included:

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
AND
noise_gradient_detected == true

Meaning:

normalized same-family distance must be lower than normalized cross-family distance

normalization must improve the margin over raw measurement

margin must be non-trivial

normalized omega must degrade consistently as noise increases



---

Raw Combined Result

Raw combined distance analysis:

mean_within_structure_distance = 0.933967967498
mean_cross_structure_distance  = 0.98675337939
separation_margin              = 0.052785411892
within_lower_than_cross        = True

Raw measurement produced a small positive separation.

However, the margin was weak.


---

Normalized Combined Result

Normalized combined distance analysis:

mean_within_structure_distance = 0.251457342874
mean_cross_structure_distance  = 0.853630825696
separation_margin              = 0.602173482822
within_lower_than_cross        = True

This is the main result.

Normalization made the structural separation much stronger.


---

Margin Improvement

Raw margin:

0.052785411892

Normalized margin:

0.602173482822

Result:

normalized_margin > raw_margin

Observed:

True

The normalized margin is more than ten times stronger than the raw margin.


---

Projected-Only Result

Projected-only normalized analysis:

mean_within_structure_distance = 0.086805555555
mean_cross_structure_distance  = 0.532930107527
separation_margin              = 0.446124551971
within_lower_than_cross        = True

This confirms that the canonical projected sequences themselves preserved family separation.


---

Noise Gradient Result

Noise gradient:

detected   = True
violations = 0

Family A normalized omega values:

noise 0 -> 0.96612988567
noise 1 -> 0.893159299028
noise 2 -> 0.833831368608
noise 3 -> 0.808991584853

Family B normalized omega values:

noise 0 -> 0.949034393852
noise 1 -> 0.873925162437
noise 2 -> 0.772707465852
noise 3 -> 0.738016108684

In both families:

higher noise
->
lower normalized omega

No monotonicity violations occurred.


---

Observed Cases

Family A

A_letters_compact_noise_0
raw_omega  = 0.96612988567
norm_omega = 0.96612988567

A_digits_spaced_noise_1
raw_omega  = 0.93706422612
norm_omega = 0.893159299028

A_words_pipe_noise_2
raw_omega  = 0.792617282477
norm_omega = 0.833831368608

A_json_like_noise_3
raw_omega  = 0.934418443431
norm_omega = 0.808991584853

Family B

B_letters_compact_noise_0
raw_omega  = 0.949034393852
norm_omega = 0.949034393852

B_digits_spaced_noise_1
raw_omega  = 0.92174247646
norm_omega = 0.873925162437

B_words_pipe_noise_2
raw_omega  = 0.746648115065
norm_omega = 0.772707465852

B_json_like_noise_3
raw_omega  = 0.925570178092
norm_omega = 0.738016108684


---

Interpretation

The experiment shows that normalization-aware measurement preserved structural family separation under deterministic noise.

The important result is not only:

PASS

The important result is:

normalization increased structural separation
while preserving a noise degradation gradient

This means the measurement did not behave as a brittle clean/fail switch.

It behaved more like a graded structural signal.


---

Main Insight

Main insight:

normalization-aware invariance can survive imperfect representation
under controlled toy conditions

This extends the v0.1 result.

v0.1 showed:

clean representation normalization can recover structure

v0.2 shows:

noisy representation normalization can preserve structure
with graceful degradation


---

Why This Matters

This result strengthens the architectural role of a representation layer.

It supports the claim that structural measurement should not be applied directly to raw surface forms when the target is representation-independent structure.

The validation chain now shows:

raw measurement
->
weak or failed invariance

normalization-aware measurement
->
stronger structural separation

This directly supports the ecosystem relationship:

OMNIABASE
->
normalization / representation handling

OMNIA
->
structural measurement

OMNIA-VALIDATION
->
falsification and recovery testing


---

Failure-Recovery-Noise Chain

The cross-domain invariance chain now has three stages.

v0

raw signatures
->
representation dominated structure
->
FAIL / NEGATIVE_RESULT

v0.1

clean canonical projection
->
same-family distance = 0
->
PASS

v0.2

noisy canonical projection
->
same-family distance remains lower than cross-family distance
->
noise gradient detected
->
PASS

This is a stronger validation arc than a single isolated benchmark.


---

What This Experiment Does NOT Prove

This experiment does NOT prove:

universal invariance

semantic truth

full OMNIA correctness

production robustness

adversarial robustness

representation-free mathematics

domain-independent generalization

real-world noise tolerance


The dataset is synthetic.

The normalization layer is hand-built.

The result is still Level 1 evidence.


---

Limitations

The experiment has several limitations:

toy dataset

deterministic synthetic noise

only two structural families

only four representations per family

hand-built normalization

limited noise types

no adversarial corruption

no real-world data

no external reproduction

no full OMNIA engine integration

no learned canonical projection

no larger family space



---

Important Constraint

The result should not be overstated.

Correct claim:

normalization-aware toy measurement preserved structural separation
under deterministic synthetic noise

Incorrect claim:

OMNIA proves universal invariance

Incorrect claim:

OMNIA can ignore representation

The actual lesson is the opposite:

representation must be handled explicitly


---

JSON Result

Generated file:

results/cross_domain_invariance_v0_2.json

Key fields:

{
  "status": "PASS",
  "raw_combined_analysis": {
    "mean_within_structure_distance": 0.933967967498,
    "mean_cross_structure_distance": 0.98675337939,
    "separation_margin": 0.052785411892,
    "within_lower_than_cross": true
  },
  "normalized_combined_analysis": {
    "mean_within_structure_distance": 0.251457342874,
    "mean_cross_structure_distance": 0.853630825696,
    "separation_margin": 0.602173482822,
    "within_lower_than_cross": true
  },
  "noise_gradient": {
    "noise_gradient_detected": true,
    "total_violation_count": 0
  }
}


---

Reproduction Command

Run from repository root:

python examples/cross_domain_invariance_v0_2.py

Expected classification:

PASS

Expected core result:

normalized_margin > raw_margin

and:

noise_gradient_detected = True


---

Colab Reproduction

The experiment was reproduced in a clean Colab environment.

Observed summary:

Status: PASS

Raw margin:
0.052785411892

Normalized margin:
0.602173482822

Noise gradient:
True

Violations:
0

Return code:

0

The experiment executed correctly.


---

Result Classification

Operational classification:

PASS

Reason:

normalization preserved same-family separation
under deterministic noise
and normalized omega degraded consistently with noise level

Evidence level:

Level 1 — Toy Demonstration


---

Main Conclusion

Main conclusion:

normalization-aware structural measurement
can preserve family separation
under imperfect representation
in this controlled toy setup

More compressed:

normalization recovers structure
and noise produces graceful degradation


---

Recommended Next Step

Recommended next experiment:

examples/adversarial_representation_v0.py

Goal:

test whether representation can be constructed
to fool the canonical projection

Possible adversarial attacks:

symbol aliasing

duplicated tokens

reordered labels

fake periodicity

separator abuse

ambiguous token boundaries

same surface statistics with different structure

different surface statistics with same structure


Core next question:

can normalization-aware invariance be broken deliberately?