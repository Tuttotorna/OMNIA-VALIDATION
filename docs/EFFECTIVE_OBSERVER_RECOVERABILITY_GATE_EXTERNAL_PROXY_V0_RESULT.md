# OMNIA-VALIDATION — Effective Observer Recoverability Gate External Proxy v0

## Objective

Evaluate gate behavior under external-style distribution shift.

Unlike previous validations based on internally aligned synthetic populations, this experiment introduces:

- heterogeneous external-style profiles
- shifted statistical distributions
- noisy and contradictory regimes
- fragile and outlier structures
- proxy labels generated independently from gate thresholds

The purpose is not maximizing PASS rate.

The purpose is measuring:

```text
gate robustness under external distribution shift


---

Configuration

Version

0.1.0

Random Seed

314159

System Count

1500

External Profiles

external_clean
external_noisy
external_shifted
external_sparse
external_redundant
external_fragile
external_mixed
external_outlier


---

Global Results

Status

CHECK

Alignment

match_count        = 1449
mismatch_count     = 51
proxy_alignment    = 0.966

Failure Counts

false_pass_count       = 0
false_collapse_count   = 18

Interpretation:

No false PASS occurred.

The observed failure mode is over-collapse bias,
not unsafe acceptance.


---

Gate Action Distribution

COLLAPSE : 188
ESCALATE : 10
FLAG     : 1271
PASS     : 15
RETRY    : 16


---

External Proxy Label Distribution

COLLAPSE : 173
ESCALATE : 8
FLAG     : 1280
PASS     : 27
RETRY    : 12


---

Source Profile Distribution

external_clean       : 189
external_fragile     : 185
external_mixed       : 183
external_noisy       : 202
external_outlier     : 180
external_redundant   : 202
external_shifted     : 191
external_sparse      : 168


---

Mean Metrics

Global Means

mean_external_risk_score      = 0.475237751285
mean_divergence               = 0.457220810255
mean_recoverability_score     = 0.538456058996
mean_normalized_effective     = 0.081235248742


---

Mean External Risk By Gate Action

COLLAPSE : 0.658291717206
ESCALATE : 0.355881799389
FLAG     : 0.450393282796
PASS     : 0.155627970594
RETRY    : 0.672167756635

Observation:

PASS systems exhibit the lowest external risk.

COLLAPSE and RETRY systems exhibit the highest external risk.


---

Mean Divergence By Gate Action

COLLAPSE : 0.367464236929
ESCALATE : 0.635861197210
FLAG     : 0.473604610421
PASS     : 0.309938916779
RETRY    : 0.236798954414

Observation:

ESCALATE behavior correlates with the highest divergence regimes.


---

Mean Risk By External Profile

external_clean       : 0.230159450472
external_fragile     : 0.658645956890
external_mixed       : 0.490469267661
external_noisy       : 0.513222904397
external_outlier     : 0.511328412917
external_redundant   : 0.547043387884
external_shifted     : 0.511186610072
external_sparse      : 0.320842648168

Observation:

external_fragile produced the highest risk profile.


---

Important Structural Finding

The dominant mismatch pattern was:

gate_action            = COLLAPSE
external_proxy_label   = FLAG

This indicates:

over-collapse bias

under external fragility conditions.

Critically:

false PASS count = 0

Therefore the gate remained conservative under distribution shift.


---

Interpretation

This experiment exposed a real structural limitation:

the gate tends to overestimate collapse
when facing external fragile distributions

However:

unsafe acceptance did not emerge

This is structurally preferable to the opposite failure mode.


---

Structural Conclusion

The experiment demonstrates:

high external proxy alignment
under heterogeneous distribution shift

while also exposing:

conservative collapse bias

The resulting CHECK status is therefore:

informative

not invalidating.

The experiment successfully identified a measurable boundary condition of the gate.


---

Reproduction

python examples/effective_observer_recoverability_gate_external_proxy_v0.py