# Cross-Gate Disagreement Analysis v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Cross-Gate Signal Conflict Analysis


---

Purpose

This experiment measures disagreement between multiple structural gate signals.

Previous experiments showed that a recoverability gate can behave coherently under synthetic, adversarial, randomized, and external-style proxy conditions.

This experiment asks a deeper question:

what happens when structural signals disagree?

Core boundary:

measurement != inference != decision


---

Experiment File

examples/cross_gate_disagreement_analysis_v0.py

Result file:

results/cross_gate_disagreement_analysis_v0.json

Reproduction command:

python examples/cross_gate_disagreement_analysis_v0.py


---

Summary Result

Status: PASS
Version: 0.1.0

system_count = 1500
random_seed = 271828

high_disagreement_count = 864
medium_disagreement_count = 613
low_disagreement_count = 23

contradiction_count = 555
unanimous_count = 0

mean_unique_action_count = 3.051333333333
mean_severity_spread = 2.930666666667
mean_severity_variance = 1.370826666667

The experiment exposed measurable signal conflict regimes.


---

Arbitration Action Distribution

COLLAPSE = 213
ESCALATE = 656
FLAG = 1
PASS = 153
RETRY = 477

The dominant arbitration result was:

ESCALATE

This is structurally important.

It means many systems were not simply good or bad.

They had conflicting structural signals.


---

Source Profile Distribution

external_clean = 168
external_fragile = 185
external_mixed = 184
external_noisy = 208
external_outlier = 207
external_redundant = 188
external_shifted = 184
external_sparse = 176

The population used external-style profiles rather than the earlier internally aligned synthetic generator.


---

Disagreement Counts

high_disagreement_count = 864
medium_disagreement_count = 613
low_disagreement_count = 23

Most systems showed medium or high disagreement.

This confirms that independent structural gates do not collapse into one identical signal.


---

Contradiction Count

contradiction_count = 555

This counts cases where at least one gate voted:

PASS

while another gate voted:

COLLAPSE

That is the strongest form of cross-gate contradiction.


---

Unanimous Count

unanimous_count = 0

No tested system produced perfect agreement across all gates.

This confirms that the signal family is not redundant.


---

Mean Severity Spread By Profile

external_clean = 1.946428571429
external_fragile = 3.075675675676
external_mixed = 3.108695652174
external_noisy = 2.658653846154
external_outlier = 3.314009661836
external_redundant = 3.675531914894
external_shifted = 3.320652173913
external_sparse = 2.198863636364

The strongest disagreement appeared in:

external_redundant
external_shifted
external_outlier

The weakest disagreement appeared in:

external_clean
external_sparse

This is coherent.

Cleaner and sparser profiles generate less cross-gate conflict.

Redundant, shifted, and outlier profiles generate stronger conflict.


---

Mean Variance By Profile

external_clean = 0.880000000000
external_fragile = 1.613837837838
external_mixed = 1.382173913043
external_noisy = 1.081153846154
external_outlier = 1.712077294686
external_redundant = 1.840000000000
external_shifted = 1.446956521739
external_sparse = 0.932272727273

Again, the strongest variance appears in structurally unstable or distorted profiles.


---

Mean Spread By Arbitration

COLLAPSE = 3.267605633803
ESCALATE = 3.751524390244
FLAG = 2.000000000000
PASS = 1.915032679739
RETRY = 1.979035639413

ESCALATE has the highest mean spread.

That is correct behavior.

High cross-gate disagreement should not be treated as ordinary PASS, RETRY, or FLAG.

It should be escalated.


---

Mean Variance By Arbitration

COLLAPSE = 1.949295774648
ESCALATE = 1.762926829268
FLAG = 0.640000000000
PASS = 0.875294117647
RETRY = 0.733752620545

COLLAPSE and ESCALATE carry the highest internal variance.

This means severe outcomes often come from nontrivial signal conflict, not simple unanimity.


---

Gate Action Distributions

Effective Signal Gate

COLLAPSE = 863
RETRY = 447
FLAG = 170
PASS = 20

The effective-count signal is very conservative.

It collapses many systems because normalized effective signal is often low.

Recoverability Gate

PASS = 164
FLAG = 946
RETRY = 340
COLLAPSE = 50

Recoverability is less collapse-heavy and more flag-heavy.

Divergence Gate

PASS = 2
RETRY = 130
FLAG = 1347
ESCALATE = 21

Divergence is overwhelmingly sensitive.

It flags most systems.

Collapse Gate

PASS = 967
RETRY = 297
FLAG = 110
COLLAPSE = 126

Collapse resistance is permissive compared to effective signal.

Projection Gate

PASS = 887
RETRY = 395
FLAG = 121
COLLAPSE = 97

Projection stability is also relatively permissive.


---

Important Finding

The gates are not redundant.

They disagree strongly.

The most important measured facts are:

unanimous_count = 0
contradiction_count = 555
mean_unique_action_count = 3.051333333333
mean_severity_spread = 2.930666666667

This supports the need for:

multi-signal structural arbitration

rather than:

single-threshold gating


---

Interpretation

This experiment shows that structural gate signals can point in different directions.

For example, a system can have:

low effective signal
high collapse resistance
high projection stability
high divergence

Such a system is not simply good or bad.

It is structurally conflicted.

The correct action is often:

ESCALATE

not because the system is definitely collapsed, but because the measurement signals disagree strongly.


---

What This Confirms

This experiment supports:

cross-gate disagreement is measurable

signal families are non-redundant

high disagreement regimes exist

PASS/COLLAPSE contradictions occur

ESCALATE is useful as an arbitration action

external-style profiles expose signal conflict

single scalar confidence is structurally insufficient


---

What This Does Not Prove

This experiment does not prove:

the arbitration rule is optimal

the gate family is complete

the thresholds are universal

the synthetic external-style generator represents real systems

semantic correctness is measured

OMNIA is generally correct

It only shows that the tested gate family exposes measurable cross-signal disagreement.


---

Boundary Statement

This experiment does not evaluate:

truth
meaning
semantic correctness
intelligence
causality
observer optimality
real-world reliability
full OMNIA correctness

It evaluates disagreement among structural gate signals.


---

Limitations

This is not the full OMNIA engine.

The profiles are still synthetic external-style profiles.

The arbitration rule is hand-defined.

The severity mapping is hand-defined.

Only 1500 systems were tested.

Only one random seed was used.

No external real-world dataset was used.

No semantic truth is evaluated.


---

Result Classification

Recommended classification:

PASS

Evidence level:

Level 2 — Cross-Gate Signal Conflict Analysis

Reason:

defined signal gates
defined severity mapping
defined disagreement metrics
defined arbitration action
defined reproduction command
saved JSON result
1500 systems tested
high disagreement regimes found
contradiction regimes found
ESCALATE regimes found

Not yet Level 3 because the generator is synthetic and the arbitration rule is not externally validated.


---

Relation To Previous Results

Validation path:

Effective Observer Count v0
→ raw_count != effective_count

Recoverability Effective Observer v0
→ flawed recoverability proxy exposed

Recoverability Effective Observer v1
→ proxy corrected

Correlation Analysis v0
→ effective_count beats raw_count on one seed

Correlation Stability v0
→ effective_count beats raw_count across 20 seeds

Correlation Adversarial v0
→ effective_count boundary exposed

Recoverability Gate v0
→ adversarial boundary cases detected by multi-signal gate

Recoverability Gate Stability v0
→ gate remains stable under threshold perturbation

Recoverability Gate Adversarial v0
→ gate resists direct adversarial probes after correction

Recoverability Gate Randomized v0
→ gate behaves coherently across 1000 synthetic systems

Recoverability Gate Randomized Stability v0
→ gate behavior remains stable across 20 seeds and 20000 systems

Recoverability Gate External Proxy v0
→ external-style shift exposes conservative over-collapse bias

Cross-Gate Disagreement Analysis v0
→ multi-signal conflict regimes are measurable


---

Required Next Step

The next logical step is arbitration stability.

Recommended file:

examples/cross_gate_disagreement_stability_v0.py

Purpose:

test whether cross-gate disagreement and arbitration behavior
remain stable across many random seeds

Main question:

does the measured signal conflict persist across populations?


---

Final Result

PASS — cross-gate disagreement analysis exposed measurable signal conflict regimes.

Correct final conclusion:

the gate signals are non-redundant,
cross-gate contradictions are measurable,
and structural arbitration is justified.