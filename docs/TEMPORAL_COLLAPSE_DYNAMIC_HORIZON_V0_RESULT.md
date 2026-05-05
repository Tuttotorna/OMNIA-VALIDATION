# Temporal Collapse Dynamic Horizon v0 — Result

## Status

```text
Status: CHECK
Version: 0.1.0
Claim level: Level 2 — Dynamic Temporal Horizon Robustness
```

---

## Purpose

This experiment tests whether the corrected critical horizon rule remains stable under non-stationary temporal dynamics.

The previous corrected rule was exact inside clean synthetic trajectories:

```text
critical_horizon =
first_raw_collapse +
confirmation_window +
persistence_window - 2
```

This experiment asks a harder question:

```text
does the critical horizon remain predictable
when temporal structure becomes unstable?
```

Core boundary:

```text
measurement != arbitration != decision
```

This experiment does not evaluate semantic truth.

It evaluates dynamic temporal collapse observability.

---

## Experiment File

```text
examples/temporal_collapse_dynamic_horizon_v0.py
```

Result file:

```text
results/temporal_collapse_dynamic_horizon_v0.json
```

Reproduction command:

```text
python examples/temporal_collapse_dynamic_horizon_v0.py
```

---

## Summary Result

```text
Status: CHECK
Version: 0.1.0

trajectory_count = 8
trajectory_length = 16

confirmation_window = 2
persistence_window = 2

pass_trajectory_count = 7
check_trajectory_count = 1

observable_persistence_count = 5

mean_horizon_error = 1.2
max_abs_horizon_error = 6

mean_persistence_reset_count = 0.75
max_persistence_reset_count = 4

mean_horizon_fragmentation = 1.5
max_horizon_fragmentation = 5
```

The result is CHECK.

The corrected static horizon rule remains exact in clean and delayed regimes.

It breaks under recovery-then-relapse dynamics.

---

## Main Finding

The central finding is:

```text
window arithmetic consistency
!=
dynamic temporal robustness
```

The corrected rule remains exact when collapse evolves cleanly.

It also survives delayed onset and dual-regime collapse.

But it fails when an early collapse is followed by recovery and then later relapse.

That means the critical horizon must be reset or reinterpreted when temporal structure contains recovery.

---

## Tested Dynamic Families

The experiment tested eight trajectory families:

```text
clean_monotonic
drifting_onset
instant_spike_recovery
oscillating_collapse
recovery_then_relapse
fragmented_persistence
dual_regime_collapse
delayed_secondary_collapse
```

These families deliberately move beyond clean monotonic degradation.

They introduce spikes, oscillation, recovery, fragmentation, and multiple collapse regimes.

---

## Static Rule Under Test

The corrected static rule is:

```text
critical_horizon =
first_raw_collapse +
confirmation_window +
persistence_window - 2
```

This rule was previously validated under clean synthetic temporal dynamics.

This experiment tests whether the same rule survives unstable temporal structure.

---

## Trajectory Results

### clean_monotonic

```text
status = PASS

raw_first = 4
temporal_first = 5
predicted = 6
observed = 6
error = 0

fragments = 1
resets = 0
```

Raw sequence:

```text
PASS -> PASS -> RETRY -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> PASS -> RETRY -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
clean monotonic collapse preserves the corrected horizon rule
```

The predicted and observed horizons match exactly.

---

### drifting_onset

```text
status = PASS

raw_first = 6
temporal_first = 7
predicted = 8
observed = 8
error = 0

fragments = 1
resets = 0
```

Raw sequence:

```text
PASS -> PASS -> PASS -> RETRY -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> PASS -> PASS -> RETRY -> ESCALATE -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
delayed raw collapse onset does not break the horizon rule
```

The formula remains exact when raw collapse starts later.

---

### instant_spike_recovery

```text
status = PASS

raw_first = 1
temporal_first = None
predicted = None
observed = None
error = None

fragments = 0
resets = 0
```

Raw sequence:

```text
PASS -> COLLAPSE -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS
```

Temporal sequence:

```text
PASS -> ESCALATE -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS -> PASS
```

Interpretation:

```text
single-frame collapse spike remains filtered
```

The spike does not become persistent collapse.

This confirms the anti-panic behavior of the temporal layer.

---

### oscillating_collapse

```text
status = PASS

raw_first = 2
temporal_first = None
predicted = None
observed = None
error = None

fragments = 0
resets = 0
```

Raw sequence:

```text
PASS -> ESCALATE -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS -> COLLAPSE -> PASS
```

Temporal sequence:

```text
PASS -> ESCALATE -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS -> ESCALATE -> PASS
```

Interpretation:

```text
oscillating collapse does not automatically become persistent collapse
```

This is correct behavior.

Collapse must persist.

Repeated isolated collapse frames are not enough.

---

### recovery_then_relapse

```text
status = CHECK

raw_first = 2
temporal_first = 3
predicted = 4
observed = 10
error = 6

fragments = 2
resets = 1
```

Raw sequence:

```text
PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> PASS -> RETRY -> PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> PASS -> RETRY -> PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
recovery after early collapse breaks the static first-collapse horizon rule
```

The initial collapse at step 2 produced temporal collapse at step 3, but recovery interrupted persistence.

Persistent collapse only became observable after relapse.

The original prediction used the first raw collapse onset:

```text
predicted = 4
```

But the observed persistent collapse occurred at:

```text
observed = 10
```

This produces:

```text
error = 6
```

This is the main CHECK case.

---

### fragmented_persistence

```text
status = PASS

raw_first = 2
temporal_first = 3
predicted = 4
observed = None
error = None

fragments = 5
resets = 4
```

Raw sequence:

```text
PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE -> PASS -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> PASS -> ESCALATE -> COLLAPSE -> PASS -> ESCALATE -> COLLAPSE -> PASS -> ESCALATE -> COLLAPSE -> PASS -> ESCALATE -> COLLAPSE
```

Interpretation:

```text
fragmented collapse creates repeated local confirmations
but no persistent collapse run
```

This is not a failure.

It shows high fragmentation:

```text
fragments = 5
resets = 4
```

The system avoids turning fragmented local collapse into persistent global collapse.

---

### dual_regime_collapse

```text
status = PASS

raw_first = 3
temporal_first = 4
predicted = 5
observed = 5
error = 0

fragments = 2
resets = 1
```

Raw sequence:

```text
PASS -> PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> PASS -> PASS -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> PASS -> PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
dual collapse regimes remain predictable when the first regime already becomes persistent
```

The first regime confirms persistence before recovery appears.

So the corrected rule still matches the first persistent horizon.

---

### delayed_secondary_collapse

```text
status = PASS

raw_first = 3
temporal_first = 10
predicted = 11
observed = 11
error = 0

fragments = 1
resets = 0
```

Raw sequence:

```text
PASS -> PASS -> ESCALATE -> COLLAPSE -> PASS -> PASS -> PASS -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Temporal sequence:

```text
PASS -> PASS -> ESCALATE -> ESCALATE -> PASS -> PASS -> PASS -> ESCALATE -> ESCALATE -> ESCALATE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE -> COLLAPSE
```

Interpretation:

```text
delayed secondary collapse remains predictable
because the first raw collapse is not a valid confirmation run
```

The system ignores the insufficient early collapse.

The later valid collapse regime produces the correct horizon.

---

## Why The Result Is CHECK

The global result is CHECK because:

```text
pass_trajectory_count = 7
check_trajectory_count = 1
```

The single CHECK trajectory is:

```text
recovery_then_relapse
```

This trajectory shows that using the first raw collapse onset is insufficient when an early collapse is followed by recovery.

The static rule needs a dynamic reset condition.

---

## What Remained Stable

The following remained stable:

```text
clean monotonic collapse
drifting onset
instant spike filtering
oscillation filtering
dual regime collapse
delayed secondary collapse
fragmented local confirmations
```

The temporal layer did not panic.

It did not transform spikes or oscillations into persistent collapse.

---

## What Broke

The static horizon rule broke under:

```text
recovery then relapse
```

Reason:

```text
first raw collapse was not the correct regime onset
```

The correct horizon should have been computed from the relapse regime, not the first transient collapse episode.

---

## Dynamic Horizon Interpretation

In dynamic temporal systems, the critical horizon should not always be computed from:

```text
first_raw_collapse
```

It should be computed from:

```text
first valid collapse regime
after recovery/reset
```

This introduces the need for a dynamic horizon rule.

---

## Required Dynamic Rule

The next rule should account for resets:

```text
critical_horizon =
valid_regime_start +
confirmation_window +
persistence_window - 2
```

Where:

```text
valid_regime_start
```

means:

```text
the start of a raw collapse run
that is not invalidated by recovery
before persistence can be confirmed
```

This is the real next OMNIATEMPO refinement.

---

## Horizon Fragmentation

```text
mean_horizon_fragmentation = 1.5
max_horizon_fragmentation = 5
```

This measures how many valid or candidate collapse regimes appear in a trajectory.

The highest fragmentation occurs in:

```text
fragmented_persistence
```

with:

```text
fragments = 5
```

This shows that temporal collapse can split into multiple local regimes.

---

## Persistence Reset

```text
mean_persistence_reset_count = 0.75
max_persistence_reset_count = 4
```

This measures how often temporal collapse confirmation is interrupted.

The highest reset count appears in:

```text
fragmented_persistence
```

with:

```text
resets = 4
```

This supports the need for reset-aware temporal logic.

---

## Main Structural Result

The core result is:

```text
the corrected static horizon law is exact
only when the collapse regime remains temporally coherent
```

When collapse recovers and relapses, the horizon must be recalculated.

So the next stage is not simply “longer trajectories”.

The next stage is:

```text
regime-aware temporal horizon detection
```

---

## Relation To Previous Result

The previous experiment validated:

```text
critical_horizon =
first_raw_collapse +
confirmation_window +
persistence_window - 2
```

This experiment shows the boundary of that law.

It remains valid when:

```text
the first raw collapse belongs to the persistent regime
```

It fails when:

```text
the first raw collapse belongs to a transient regime
that later recovers
```

---

## Relation To OMNIATEMPO

This experiment strengthens OMNIATEMPO.

It shows that temporal measurement must distinguish:

```text
collapse event
collapse regime
collapse recovery
collapse relapse
persistent collapse
```

A single event is not enough.

OMNIATEMPO must measure temporal regimes, not isolated labels.

---

## Relation To TDelta

This experiment refines the TDelta direction.

A simple divergence time is not sufficient if the system can recover and relapse.

Instead, OMNIATEMPO needs:

```text
regime-specific divergence time
```

Possible future quantities:

```text
TΔ_first
TΔ_persistent
TΔ_recovered
TΔ_relapse
TΔ_final
```

The current CHECK exposes why those distinctions matter.

---

## What This Confirms

This experiment supports:

```text
static critical horizon remains exact for clean monotonic collapse
delayed raw onset remains predictable
instant spikes remain filtered
oscillating collapse remains nonpersistent
fragmented collapse does not become global persistence
dual regime collapse can remain predictable
delayed secondary collapse can remain predictable
recovery then relapse exposes dynamic horizon drift
```

---

## What This Does Not Prove

This experiment does not prove:

```text
universal dynamic horizon predictability
real-world temporal reliability
semantic correctness
causal correctness
full dynamic OMNIATEMPO correctness
full TDelta
full OMNIA correctness
```

It exposes the first boundary of the corrected static horizon law.

---

## Boundary Statement

This experiment does not evaluate:

```text
truth
meaning
semantic correctness
intelligence
causality
real-world reliability
full OMNIA correctness
```

It evaluates:

```text
dynamic temporal collapse observability
under non-stationary temporal structure
```

---

## Limitations

```text
Only 8 dynamic trajectory families were tested.

Trajectory length is fixed at 16.

Confirmation window is fixed at 2.

Persistence window is fixed at 2.

Trajectories are synthetic.

The reset logic is not yet formalized.

No external temporal dataset was used.

No semantic ground truth exists.
```

---

## Result Classification

Recommended classification:

```text
CHECK
```

Evidence level:

```text
Level 2 — Dynamic Temporal Horizon Robustness
```

Reason:

```text
8 dynamic trajectories tested

7 trajectories passed

1 trajectory exposed horizon drift

static rule remained exact in clean/delayed regimes

spikes and oscillations were filtered

fragmentation and resets were measured

recovery-then-relapse broke first-collapse prediction
```

This is not a failed result.

It is a boundary diagnosis.

---

## Relation To Previous Results

Validation path:

```text
Effective Observer Count v0
-> raw_count != effective_count

Recoverability Effective Observer v0
-> flawed recoverability proxy exposed

Recoverability Effective Observer v1
-> proxy corrected

Correlation Analysis v0
-> effective_count beats raw_count

Correlation Stability v0
-> correlation stability verified

Correlation Adversarial v0
-> adversarial boundary exposed

Recoverability Gate v0
-> multi-signal gate detects instability

Recoverability Gate Stability v0
-> threshold stability verified

Recoverability Gate Adversarial v0
-> adversarial resistance improved

Recoverability Gate Randomized v0
-> coherent randomized behavior

Recoverability Gate Randomized Stability v0
-> stable randomized behavior

Recoverability Gate External Proxy v0
-> external-style shift exposes mismatch

Cross-Gate Disagreement Analysis v0
-> signal conflict regimes measured

Cross-Gate Disagreement Stability v0
-> conflict remains stable across populations

Cross-Gate Real Dataset Proxy v0
-> mild proxy dataset under-stressed

Cross-Gate Real Dataset Proxy Stressed v0
-> stronger disagreement achieved without confirmed collapse

Cross-Gate Real Dataset Proxy Collapse v0
-> arbitration COLLAPSE appears under multi-gate confirmed pressure

Collapse Confirmation Stability v0
-> collapse remains present but confirmation-source identity is perturbation-sensitive

Collapse Confirmation Source Swap v0
-> collapse remains stable when confirmation source changes

Temporal Collapse Degradation v0
-> temporal degradation is measurable but single-frame collapse requires confirmation

Temporal Collapse Confirmation v0
-> transient collapse is filtered but persistence requires longer trajectories

Temporal Collapse Persistence v0
-> persistent collapse confirmed while transient collapse is filtered

Temporal Collapse Persistence Stability v0
-> persistence stable under mild window variation but scale-sensitive under strict windows

Temporal Collapse Phase Diagram v0
-> temporal observability boundary mapped across trajectory length and window space

Temporal Collapse Critical Horizon v0
-> first horizon law exposed systematic offset

Temporal Collapse Critical Horizon Corrected v0
-> corrected horizon law matches all observable clean-regime pairs

Temporal Collapse Dynamic Horizon v0
-> recovery and relapse expose the need for reset-aware horizon logic
```

---

## Required Next Step

Recommended next experiment:

```text
examples/temporal_collapse_regime_reset_v0.py
```

Purpose:

```text
define and test reset-aware critical horizon logic
```

Main question:

```text
can the horizon rule be restored
by computing it from the first valid collapse regime
instead of the first raw collapse frame?
```

Required rule:

```text
dynamic_critical_horizon =
valid_regime_start +
confirmation_window +
persistence_window - 2
```

Where:

```text
valid_regime_start
```

is the start of a collapse run that is not invalidated by recovery before persistence confirmation.

Required checks:

```text
recovery_then_relapse becomes PASS

clean_monotonic remains PASS

drifting_onset remains PASS

instant_spike_recovery remains PASS

oscillating_collapse remains PASS

fragmented_persistence remains nonpersistent

dual_regime_collapse remains PASS

delayed_secondary_collapse remains PASS
```

Expected result:

```text
dynamic horizon error returns to 0
after reset-aware regime detection
```

---

## Final Result

```text
CHECK — dynamic horizon exposed temporal instability under non-stationary structure.
```

Correct final conclusion:

```text
the corrected static horizon law is exact for coherent collapse regimes,
but recovery and relapse require reset-aware temporal horizon logic.
```