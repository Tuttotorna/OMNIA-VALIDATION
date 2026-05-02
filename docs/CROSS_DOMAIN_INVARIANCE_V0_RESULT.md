# Cross-Domain Invariance v0 — Result

## Status

```text
FAIL

Operational Classification

NEGATIVE_RESULT

Evidence Level

Level 1 — Toy Demonstration

Experiment

cross_domain_invariance_v0

Repository

OMNIA-VALIDATION


---

Purpose

This experiment tests a central OMNIA hypothesis:

can structural similarity survive representation change?

The experiment attempts a minimal toy test of:

structural invariance under transformation

Core question:

does the same structure remain closer to itself
across different representations
than to a different structure?

This is one of the most conceptually important directions in the OMNIA ecosystem.


---

Core Boundary

measurement != inference != decision

The experiment measures structural proximity only.

It does not:

infer semantic meaning

prove identity

validate truth

prove universal invariance



---

Core Validation Question

The validation question was:

is within-structure distance lower
than cross-structure distance?

Expected behavior:

same structure
+
different representation
->
smaller distance

and:

different structure
->
larger distance

The experiment failed this criterion.


---

Structural Families

Two structural families were created.


---

Family A

Alternating binary structure:

ABABABAB...

Represented as:

compact letters

spaced digits

word pairs

JSON-like encoding



---

Family B

Four-step cyclic structure:

ABCDABCD...

Represented as:

compact letters

spaced digits

directional words

JSON-like encoding



---

Experimental Goal

The goal was to test whether:

structure dominates representation

Observed result:

representation dominated structure

This is the central result of the experiment.


---

Structural Signature

The toy structural signature included:

entropy
compression_ratio
repetition_score
transition_regular_score
token_length_regular_score
omega_proxy

Important:

this is not the full OMNIA engine

This is only a toy proxy.


---

Distance Geometry

Each case produced a structural signature vector.

Pairwise Euclidean distances were computed between all representations.

Distances were separated into:

within-structure distances

and:

cross-structure distances

Expected:

within < cross

Observed:

within > cross


---

PASS Criterion

Original pass condition:

mean_within_structure_distance
<
mean_cross_structure_distance

AND

separation_margin > 0.05


---

Observed Result

Observed metrics:

mean_within_structure_distance = 1.283698217317
mean_cross_structure_distance  = 1.103052460455
separation_margin              = -0.180645756862
within_to_cross_ratio          = 1.163768962346
within lower than cross        = False

Result:

FAIL

Operational classification:

NEGATIVE_RESULT


---

Central Failure

The experiment falsified the naive invariance assumption.

Observed behavior:

same structure across representations
was NOT consistently closer
than different structures

This means:

representation dominated structure

under the v0 toy signature.


---

Important Observation

The most revealing distances were:

A_words_pipe <-> B_json_like
distance = 0.097660499358
same_family = False

and:

A_json_like <-> B_json_like
distance = 0.125870144477
same_family = False

while some same-family distances were much larger:

A_letters_compact <-> A_words_pipe
distance = 2.335689067235
same_family = True

This is extremely important.

It means:

surface representation style
can overwhelm structural family identity

in the toy signature space.


---

Main Insight

Main observed insight:

naive structural signatures are not representation-invariant

This is the central result of the experiment.


---

Stronger Interpretation

A stronger interpretation is:

without normalization,
representation beats structure

This is likely one of the deepest outcomes so far in the repository.

Because it exposes exactly where naive measurement fails.


---

Why This Result Is Valuable

This is NOT a useless failure.

This is a high-value negative result.

Reason:

the experiment exposed a real limitation
instead of producing fake success

That is scientifically valuable.

The experiment discovered a real boundary:

representation-sensitive metrics
do not automatically recover structural invariance


---

Why This Matters For OMNIA

This result directly supports the conceptual need for:

representation normalization

and potentially:

OMNIABASE

because raw representations distort measured geometry.

The experiment therefore strengthens the conceptual direction:

invariance requires transformation-aware normalization


---

Failure Boundary Exposed

The experiment exposes a major boundary:

structural similarity
!=
representation similarity

and also:

high repetition
!=
same structure

because many representations can independently produce:

high repetition

high compressibility

high regularity


without sharing the same deeper structure.


---

Observed Cases

Observed omega_proxy values:

A_letters_compact -> 0.710798086822
A_digits_spaced   -> 0.972408876476
A_words_pipe      -> 0.97692651516
A_json_like       -> 0.984986050708

B_letters_compact -> 0.694894260467
B_digits_spaced   -> 0.956563120155
B_words_pipe      -> 0.964553648505
B_json_like       -> 0.979759838933

Observation:

representation format strongly altered scores

even within the same structural family.


---

Representation Dominance

The strongest pattern in the experiment was:

compact letter representations
behaved very differently
from spaced / tokenized / JSON-like representations

This produced large within-family distances.

Meanwhile:

tokenized representations across different families
often remained close

because the toy metrics captured formatting regularities more strongly than abstract structure.


---

What The Experiment Does NOT Prove

This experiment does NOT prove:

OMNIA fails

structural invariance is impossible

representation invariance cannot exist

transformation-aware metrics are impossible

OMNIABASE is invalid

structural geometry is meaningless


It only proves:

the v0 toy signature failed to preserve invariance
across representation changes


---

Why The Failure Is Honest

An important property of this repository is emerging:

not all experiments succeed

This is good.

The repository now contains:

PASS

WEAK_PASS

FAIL

NEGATIVE_RESULT


which is much more credible than universal success.


---

Most Important Conclusion

Most important conclusion:

naive structural metrics are heavily representation-sensitive

This is probably the strongest conclusion produced so far by the repository.


---

Technical Interpretation

The v0 signature mainly captured:

surface regularity

rather than:

abstract transformation-invariant structure

Therefore:

representation geometry
overpowered
structural family geometry


---

Why OMNIABASE Becomes Relevant

This failure strongly motivates:

representation normalization

including:

base normalization

token normalization

separator normalization

structural projection

representation-independent coordinate systems


This is conceptually aligned with:

OMNIABASE

because the failure emerged from representation dependence itself.


---

Limitations

The experiment has several limitations:

toy signatures only

no true structural normalization

Euclidean distance only

only two structural families

only four representations per family

no transformation learning

no graph structure

no symbolic equivalence mapping

no multi-base normalization

no latent structural projection

no trajectory analysis

no adversarial robustness testing



---

Result Classification

Operational classification:

NEGATIVE_RESULT

Reason:

same-structure representations
were not closer than cross-structure representations

and:

representation effects dominated the measured geometry


---

JSON Result

Generated file:

results/cross_domain_invariance_v0.json

Key fields:

{
  "status": "FAIL",
  "analysis": {
    "mean_within_structure_distance": 1.283698217317,
    "mean_cross_structure_distance": 1.103052460455,
    "separation_margin": -0.180645756862,
    "within_to_cross_ratio": 1.163768962346,
    "within_lower_than_cross": false
  }
}


---

Reproduction Command

Run from repository root:

python examples/cross_domain_invariance_v0.py

Expected classification:

FAIL

Expected operational interpretation:

NEGATIVE_RESULT


---

Colab Reproduction

The experiment was reproduced successfully in a clean Colab environment.

Observed summary:

Status: FAIL

Mean within-structure distance:
1.283698217317

Mean cross-structure distance:
1.103052460455

Within lower than cross:
False

Return code:

0

The experiment executed correctly.


---

Next Step

Recommended next experiment:

examples/cross_domain_invariance_v0_1.py

Core goal:

introduce representation normalization
before structural distance measurement

Recommended additions:

token normalization

separator normalization

alphabet projection

representation stripping

base-independent encoding

symbolic canonicalization

normalized transition geometry

structure-first distance metrics


Core next question:

can invariance emerge
after representation normalization?