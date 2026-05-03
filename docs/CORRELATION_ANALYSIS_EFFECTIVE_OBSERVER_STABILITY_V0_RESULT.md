# Correlation Analysis: Effective Observer Count Stability v0 — Result

## Status

```text
Status: PASS
Version: 0.1.0
Claim level: Level 2 — Controlled Experiment


---

Purpose

This experiment tests whether effective_observer_count remains a better recoverability predictor than raw observer count across multiple random seeds.

The previous correlation experiment used one random seed.

This experiment checks seed stability.

Core question:

does effective_count outperform raw_count
as a recoverability predictor across repeated randomized runs?

Core boundary:

measurement != inference != decision


---

Experiment File

examples/correlation_analysis_effective_observer_stability_v0.py

Result file:

results/correlation_analysis_effective_observer_stability_v0.json

Reproduction command:

python examples/correlation_analysis_effective_observer_stability_v0.py


---

Experimental Setup

seed_count = 20
systems_per_seed = 500
total_systems = 10,000

For each seed, the script generated randomized observer systems.

For each seed, it measured:

corr(raw_count, recoverability)

and:

corr(effective_count, recoverability)

Both Pearson and Spearman correlations were computed.

The improvement was defined as:

effective_correlation - raw_correlation


---

Summary Result

Status: PASS
positive_seed_count = 20
negative_seed_count = 0

effective_count outperformed raw_count on every tested seed.


---

Aggregate Results

mean_pearson_improvement:
0.141311664052

min_pearson_improvement:
0.109912781431

max_pearson_improvement:
0.160282682147

mean_spearman_improvement:
0.170348625395

min_spearman_improvement:
0.139765807063

max_spearman_improvement:
0.201344197377

The minimum improvements were positive.

That means no tested seed reversed the result.


---

Main Finding

The advantage of effective_observer_count was stable across all tested seeds.

The result is not a single-seed artifact.

Correct conclusion:

effective_observer_count is a seed-stable stronger predictor
of recoverability than raw observer count
inside this synthetic observer-system generator


---

Compact Seed Summary

seed=0   pearson_improvement=0.124399284557  spearman_improvement=0.159788127153
seed=1   pearson_improvement=0.131107382544  spearman_improvement=0.163266317065
seed=2   pearson_improvement=0.127162801557  spearman_improvement=0.157259957040
seed=3   pearson_improvement=0.149868360387  spearman_improvement=0.193078564314
seed=4   pearson_improvement=0.155332521643  spearman_improvement=0.179302893212
seed=5   pearson_improvement=0.151145261496  spearman_improvement=0.178443017772
seed=6   pearson_improvement=0.140430634555  spearman_improvement=0.157779895120
seed=7   pearson_improvement=0.137798340714  spearman_improvement=0.168225696903
seed=8   pearson_improvement=0.137698722584  spearman_improvement=0.163637934552
seed=9   pearson_improvement=0.109912781431  spearman_improvement=0.139765807063
seed=10  pearson_improvement=0.145131202186  spearman_improvement=0.181087156349
seed=11  pearson_improvement=0.157582034664  spearman_improvement=0.175442237769
seed=12  pearson_improvement=0.149904858976  spearman_improvement=0.166124152497
seed=13  pearson_improvement=0.151957292717  spearman_improvement=0.185734534938
seed=14  pearson_improvement=0.136140286187  spearman_improvement=0.180436273745
seed=15  pearson_improvement=0.156845833086  spearman_improvement=0.158196728787
seed=16  pearson_improvement=0.120165781038  spearman_improvement=0.164224976900
seed=17  pearson_improvement=0.153137018713  spearman_improvement=0.177981255925
seed=18  pearson_improvement=0.130230199859  spearman_improvement=0.155852783411
seed=19  pearson_improvement=0.160282682147  spearman_improvement=0.201344197377


---

Interpretation

Raw observer count measures only quantity.

It does not measure:

family balance
non-redundancy
collapse resistance
effective structural diversity

effective_observer_count includes structural penalties.

That is why it remains more predictive than raw count across the tested seeds.

The result supports this narrower claim:

observer quantity alone is weaker than effective observer structure
for predicting recoverability in this synthetic setting


---

Relation To Previous Results

Earlier validation path:

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

This moves the evidence from:

single-run evidence

to:

seed-stability evidence


---

What This Confirms

This experiment supports:

effective_count is more informative than raw_count

the correlation advantage is stable across tested seeds

the result is not dependent on seed 42

nominal observer quantity is insufficient

observer structure matters


---

What This Does Not Prove

This experiment does not prove:

effective_count equals recoverability

effective_count is universally valid

recoverability is fully solved

OMNIA is generally correct

observer geometry is complete

the result transfers to real-world datasets

It only shows a stable correlation advantage inside the tested synthetic generator.


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

It evaluates only a structural measurement relation inside a controlled synthetic experiment.


---

Limitations

This is not the full OMNIA engine.

This is a synthetic randomized experiment.

The generator is simplified.

Recoverability remains a proxy.

Only 20 seeds were tested.

Each seed used 500 systems.

No external dataset was used.

No semantic truth is evaluated.

No universal recoverability claim is made.

The metric may still be coupled to the synthetic generator design.


---

Result Classification

Recommended classification:

PASS

Evidence level:

Level 2 — Controlled Experiment

Reason:

defined generator
defined seed sweep
defined metrics
defined comparison rule
defined reproduction command
saved JSON result

Not yet Level 3 because no independent baseline family or external dataset is included.


---

Required Next Step

The next step should test adversarial failure cases for the correlation itself.

Recommended file:

examples/correlation_analysis_effective_observer_adversarial_v0.py

Purpose:

construct systems where effective_count appears high
but recoverability is low

Required adversarial cases:

high_raw_high_duplicate
high_effective_low_projection_stability
family_balanced_projection_collapsed
high_entropy_low_recovery
coverage_without_independence
independence_without_coverage

Main question:

where does effective_count stop predicting recoverability?


---

Final Result

PASS — effective_count outperformed raw_count across all tested seeds.

Correct final conclusion:

effective_observer_count is a seed-stable stronger predictor
of recoverability than raw observer count
inside the tested synthetic observer-system generator.