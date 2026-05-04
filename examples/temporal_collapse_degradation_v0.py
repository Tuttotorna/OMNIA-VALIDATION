import json
import os
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "temporal_collapse_degradation_v0.json",
)


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def safe_div(a, b):
    if b == 0:
        return 0.0
    return a / b


def compute_effective_count(
    raw_count,
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    return max(
        0.0,
        raw_count
        * non_redundancy
        * family_balance
        * (0.5 + 0.5 * relation_entropy)
        * collapse_resistance
        * projection_stability,
    )


def compute_recoverability_score(
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    return clamp(
        0.25 * non_redundancy
        + 0.20 * family_balance
        + 0.15 * relation_entropy
        + 0.20 * collapse_resistance
        + 0.20 * projection_stability
    )


def compute_divergence(
    normalized_effective,
    recoverability_score,
):
    return abs(normalized_effective - recoverability_score)


def effective_signal_gate(normalized_effective):
    if normalized_effective >= 0.45:
        return "PASS"

    if normalized_effective >= 0.20:
        return "FLAG"

    if normalized_effective >= 0.05:
        return "RETRY"

    return "COLLAPSE"


def recoverability_gate(recoverability_score):
    if recoverability_score >= 0.72:
        return "PASS"

    if recoverability_score >= 0.45:
        return "FLAG"

    if recoverability_score >= 0.30:
        return "RETRY"

    return "COLLAPSE"


def divergence_gate(divergence):
    if divergence >= 0.60:
        return "ESCALATE"

    if divergence >= 0.35:
        return "FLAG"

    if divergence >= 0.20:
        return "RETRY"

    return "PASS"


def collapse_gate(collapse_resistance):
    if collapse_resistance < 0.10:
        return "COLLAPSE"

    if collapse_resistance < 0.20:
        return "FLAG"

    if collapse_resistance < 0.45:
        return "RETRY"

    return "PASS"


def projection_gate(projection_stability):
    if projection_stability < 0.10:
        return "COLLAPSE"

    if projection_stability < 0.20:
        return "FLAG"

    if projection_stability < 0.45:
        return "RETRY"

    return "PASS"


def action_severity(action):
    severity = {
        "PASS": 0,
        "RETRY": 1,
        "FLAG": 2,
        "ESCALATE": 3,
        "COLLAPSE": 4,
    }

    return severity[action]


def severity_to_action(severity_value):
    if severity_value >= 3.50:
        return "COLLAPSE"

    if severity_value >= 2.50:
        return "ESCALATE"

    if severity_value >= 1.50:
        return "FLAG"

    if severity_value >= 0.50:
        return "RETRY"

    return "PASS"


def structural_arbitration(signal_actions):
    severities = [
        action_severity(action)
        for action in signal_actions.values()
    ]

    max_severity = max(severities)
    min_severity = min(severities)
    mean_severity = mean(severities)

    spread = max_severity - min_severity

    collapse_votes = sum(
        1
        for action in signal_actions.values()
        if action == "COLLAPSE"
    )

    escalate_votes = sum(
        1
        for action in signal_actions.values()
        if action == "ESCALATE"
    )

    pass_votes = sum(
        1
        for action in signal_actions.values()
        if action == "PASS"
    )

    if collapse_votes >= 2:
        return "COLLAPSE"

    if collapse_votes == 1 and spread >= 3:
        return "ESCALATE"

    if escalate_votes >= 1 and spread >= 2:
        return "ESCALATE"

    if spread >= 3:
        return "ESCALATE"

    if pass_votes >= 3 and max_severity <= 2:
        return "PASS"

    return severity_to_action(mean_severity)


def compute_disagreement(signal_actions):
    severities = [
        action_severity(action)
        for action in signal_actions.values()
    ]

    unique_actions = len(set(signal_actions.values()))
    spread = max(severities) - min(severities)
    mean_severity = mean(severities)

    variance = mean(
        (value - mean_severity) ** 2
        for value in severities
    )

    return {
        "unique_action_count": unique_actions,
        "severity_spread": spread,
        "severity_variance": variance,
        "mean_severity": mean_severity,
    }


def evaluate_state(trajectory_name, step, state):
    raw_count = state["raw_count"]

    effective_count = compute_effective_count(
        raw_count=raw_count,
        non_redundancy=state["non_redundancy"],
        family_balance=state["family_balance"],
        relation_entropy=state["relation_entropy"],
        collapse_resistance=state["collapse_resistance"],
        projection_stability=state["projection_stability"],
    )

    normalized_effective = safe_div(
        effective_count,
        raw_count,
    )

    recoverability_score = compute_recoverability_score(
        non_redundancy=state["non_redundancy"],
        family_balance=state["family_balance"],
        relation_entropy=state["relation_entropy"],
        collapse_resistance=state["collapse_resistance"],
        projection_stability=state["projection_stability"],
    )

    divergence = compute_divergence(
        normalized_effective=normalized_effective,
        recoverability_score=recoverability_score,
    )

    signal_actions = {
        "effective_signal_gate": effective_signal_gate(normalized_effective),
        "recoverability_gate": recoverability_gate(recoverability_score),
        "divergence_gate": divergence_gate(divergence),
        "collapse_gate": collapse_gate(state["collapse_resistance"]),
        "projection_gate": projection_gate(state["projection_stability"]),
    }

    disagreement = compute_disagreement(signal_actions)

    arbitration_action = structural_arbitration(signal_actions)

    collapse_sources = [
        key
        for key, value in signal_actions.items()
        if value == "COLLAPSE"
    ]

    return {
        "trajectory_name": trajectory_name,
        "step": step,
        "raw_count": raw_count,
        "effective_count": effective_count,
        "normalized_effective": normalized_effective,
        "recoverability_score": recoverability_score,
        "divergence": divergence,
        "non_redundancy": state["non_redundancy"],
        "family_balance": state["family_balance"],
        "relation_entropy": state["relation_entropy"],
        "collapse_resistance": state["collapse_resistance"],
        "projection_stability": state["projection_stability"],
        "signal_actions": signal_actions,
        "collapse_sources": collapse_sources,
        "arbitration_action": arbitration_action,
        "unique_action_count": disagreement["unique_action_count"],
        "severity_spread": disagreement["severity_spread"],
        "severity_variance": disagreement["severity_variance"],
        "mean_severity": disagreement["mean_severity"],
    }


def build_state(
    raw_count,
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    return {
        "raw_count": raw_count,
        "non_redundancy": clamp(non_redundancy),
        "family_balance": clamp(family_balance),
        "relation_entropy": clamp(relation_entropy),
        "collapse_resistance": clamp(collapse_resistance),
        "projection_stability": clamp(projection_stability),
    }


def generate_trajectories():
    trajectories = {}

    trajectories["stable_control"] = [
        build_state(60, 0.93, 0.88, 0.72, 0.96, 0.95),
        build_state(60, 0.92, 0.88, 0.72, 0.95, 0.94),
        build_state(60, 0.92, 0.87, 0.71, 0.95, 0.94),
        build_state(60, 0.91, 0.87, 0.71, 0.94, 0.93),
        build_state(60, 0.91, 0.86, 0.70, 0.94, 0.93),
        build_state(60, 0.90, 0.86, 0.70, 0.93, 0.92),
    ]

    trajectories["slow_decay"] = [
        build_state(100, 0.88, 0.82, 0.70, 0.88, 0.86),
        build_state(100, 0.74, 0.70, 0.68, 0.76, 0.74),
        build_state(100, 0.58, 0.55, 0.63, 0.61, 0.58),
        build_state(100, 0.42, 0.38, 0.57, 0.43, 0.40),
        build_state(100, 0.26, 0.24, 0.50, 0.22, 0.18),
        build_state(100, 0.14, 0.13, 0.44, 0.08, 0.07),
    ]

    trajectories["projection_first_failure"] = [
        build_state(90, 0.85, 0.80, 0.70, 0.86, 0.82),
        build_state(90, 0.82, 0.78, 0.69, 0.82, 0.56),
        build_state(90, 0.78, 0.74, 0.67, 0.78, 0.32),
        build_state(90, 0.74, 0.70, 0.65, 0.72, 0.16),
        build_state(90, 0.68, 0.62, 0.62, 0.58, 0.08),
        build_state(90, 0.51, 0.45, 0.56, 0.31, 0.05),
    ]

    trajectories["recoverability_first_failure"] = [
        build_state(110, 0.82, 0.76, 0.70, 0.82, 0.84),
        build_state(110, 0.58, 0.52, 0.66, 0.70, 0.78),
        build_state(110, 0.39, 0.34, 0.58, 0.56, 0.68),
        build_state(110, 0.23, 0.21, 0.51, 0.42, 0.54),
        build_state(110, 0.14, 0.13, 0.43, 0.24, 0.31),
        build_state(110, 0.09, 0.08, 0.36, 0.11, 0.14),
    ]

    trajectories["oscillating_instability"] = [
        build_state(95, 0.80, 0.76, 0.70, 0.82, 0.80),
        build_state(95, 0.34, 0.30, 0.58, 0.38, 0.35),
        build_state(95, 0.70, 0.66, 0.67, 0.72, 0.70),
        build_state(95, 0.28, 0.24, 0.55, 0.30, 0.28),
        build_state(95, 0.62, 0.58, 0.63, 0.64, 0.60),
        build_state(95, 0.12, 0.10, 0.42, 0.08, 0.07),
    ]

    trajectories["false_recovery"] = [
        build_state(80, 0.82, 0.78, 0.70, 0.80, 0.78),
        build_state(80, 0.44, 0.40, 0.62, 0.50, 0.48),
        build_state(80, 0.26, 0.22, 0.55, 0.30, 0.27),
        build_state(80, 0.52, 0.48, 0.64, 0.61, 0.57),
        build_state(80, 0.20, 0.17, 0.48, 0.22, 0.19),
        build_state(80, 0.08, 0.07, 0.35, 0.07, 0.06),
    ]

    trajectories["instant_noise_spike"] = [
        build_state(75, 0.86, 0.82, 0.70, 0.88, 0.86),
        build_state(75, 0.18, 0.15, 0.42, 0.12, 0.10),
        build_state(75, 0.82, 0.78, 0.68, 0.84, 0.82),
        build_state(75, 0.80, 0.76, 0.67, 0.82, 0.80),
        build_state(75, 0.78, 0.74, 0.66, 0.80, 0.78),
        build_state(75, 0.76, 0.72, 0.65, 0.78, 0.76),
    ]

    trajectories["delayed_multi_gate_collapse"] = [
        build_state(120, 0.86, 0.82, 0.72, 0.86, 0.84),
        build_state(120, 0.68, 0.64, 0.68, 0.70, 0.66),
        build_state(120, 0.50, 0.46, 0.61, 0.54, 0.48),
        build_state(120, 0.36, 0.31, 0.55, 0.36, 0.28),
        build_state(120, 0.22, 0.18, 0.47, 0.18, 0.13),
        build_state(120, 0.10, 0.08, 0.36, 0.06, 0.05),
    ]

    return trajectories


def first_step_with_action(states, action):
    for item in states:
        if item["arbitration_action"] == action:
            return item["step"]

    return None


def first_step_at_or_above(states, severity):
    for item in states:
        if action_severity(item["arbitration_action"]) >= severity:
            return item["step"]

    return None


def has_monotonic_severity(states):
    severities = [
        action_severity(item["arbitration_action"])
        for item in states
    ]

    return all(
        later >= earlier
        for earlier, later in zip(severities, severities[1:])
    )


def count_action(states, action):
    return sum(
        1
        for item in states
        if item["arbitration_action"] == action
    )


def evaluate_trajectory(name, states):
    evaluated_states = [
        evaluate_state(
            trajectory_name=name,
            step=index,
            state=state,
        )
        for index, state in enumerate(states)
    ]

    first_escalation_step = first_step_with_action(
        evaluated_states,
        "ESCALATE",
    )

    first_collapse_step = first_step_with_action(
        evaluated_states,
        "COLLAPSE",
    )

    first_non_pass_step = first_step_at_or_above(
        evaluated_states,
        1,
    )

    first_high_risk_step = first_step_at_or_above(
        evaluated_states,
        3,
    )

    collapse_onset_step = first_collapse_step

    escalation_before_collapse = (
        first_escalation_step is not None
        and first_collapse_step is not None
        and first_escalation_step < first_collapse_step
    )

    multi_gate_confirmation_before_collapse = False

    if first_collapse_step is not None:
        for item in evaluated_states:
            if item["step"] >= first_collapse_step:
                break

            if len(item["collapse_sources"]) >= 2:
                multi_gate_confirmation_before_collapse = True

    panic_collapse_count = sum(
        1
        for item in evaluated_states
        if item["arbitration_action"] == "COLLAPSE"
        and item["step"] <= 1
        and name != "instant_noise_spike"
    )

    instant_spike_panic = (
        name == "instant_noise_spike"
        and evaluated_states[1]["arbitration_action"] == "COLLAPSE"
    )

    recovery_after_escalation_count = 0

    for index, item in enumerate(evaluated_states):
        if item["arbitration_action"] == "ESCALATE":
            later = evaluated_states[index + 1:]

            if any(
                action_severity(future["arbitration_action"]) < 3
                for future in later
            ):
                recovery_after_escalation_count += 1

    monotonic = has_monotonic_severity(evaluated_states)

    trajectory_status = "PASS"

    if name == "stable_control":
        if count_action(evaluated_states, "PASS") != len(evaluated_states):
            trajectory_status = "CHECK"

    elif name == "instant_noise_spike":
        if instant_spike_panic:
            trajectory_status = "CHECK"

        if count_action(evaluated_states, "COLLAPSE") > 0:
            trajectory_status = "CHECK"

    elif name in {
        "slow_decay",
        "projection_first_failure",
        "recoverability_first_failure",
        "delayed_multi_gate_collapse",
    }:
        if first_collapse_step is None:
            trajectory_status = "CHECK"

        if first_high_risk_step is None:
            trajectory_status = "CHECK"

        if first_high_risk_step is not None and first_collapse_step is not None:
            if first_high_risk_step > first_collapse_step:
                trajectory_status = "CHECK"

    elif name in {
        "oscillating_instability",
        "false_recovery",
    }:
        if first_high_risk_step is None:
            trajectory_status = "CHECK"

        if recovery_after_escalation_count == 0:
            trajectory_status = "CHECK"

    return {
        "trajectory_name": name,
        "status": trajectory_status,
        "state_count": len(evaluated_states),
        "first_non_pass_step": first_non_pass_step,
        "first_escalation_step": first_escalation_step,
        "collapse_onset_step": collapse_onset_step,
        "first_high_risk_step": first_high_risk_step,
        "escalation_before_collapse": escalation_before_collapse,
        "multi_gate_confirmation_before_collapse": (
            multi_gate_confirmation_before_collapse
        ),
        "panic_collapse_count": panic_collapse_count,
        "instant_spike_panic": instant_spike_panic,
        "recovery_after_escalation_count": recovery_after_escalation_count,
        "trajectory_monotonicity": monotonic,
        "action_sequence": [
            item["arbitration_action"]
            for item in evaluated_states
        ],
        "mean_severity": mean(
            action_severity(item["arbitration_action"])
            for item in evaluated_states
        ),
        "max_severity": max(
            action_severity(item["arbitration_action"])
            for item in evaluated_states
        ),
        "states": evaluated_states,
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    trajectories = generate_trajectories()

    trajectory_results = [
        evaluate_trajectory(name, states)
        for name, states in trajectories.items()
    ]

    pass_trajectory_count = sum(
        1
        for item in trajectory_results
        if item["status"] == "PASS"
    )

    check_trajectory_count = len(trajectory_results) - pass_trajectory_count

    collapse_trajectories = [
        item
        for item in trajectory_results
        if item["collapse_onset_step"] is not None
    ]

    escalation_trajectories = [
        item
        for item in trajectory_results
        if item["first_escalation_step"] is not None
    ]

    escalation_before_collapse_count = sum(
        1
        for item in trajectory_results
        if item["escalation_before_collapse"]
    )

    panic_collapse_total = sum(
        item["panic_collapse_count"]
        for item in trajectory_results
    )

    instant_spike_panic_count = sum(
        1
        for item in trajectory_results
        if item["instant_spike_panic"]
    )

    recovery_after_escalation_total = sum(
        item["recovery_after_escalation_count"]
        for item in trajectory_results
    )

    monotonic_count = sum(
        1
        for item in trajectory_results
        if item["trajectory_monotonicity"]
    )

    summary = {
        "trajectory_count": len(trajectory_results),
        "states_per_trajectory": 6,
        "total_state_count": len(trajectory_results) * 6,
        "pass_trajectory_count": pass_trajectory_count,
        "check_trajectory_count": check_trajectory_count,
        "collapse_trajectory_count": len(collapse_trajectories),
        "escalation_trajectory_count": len(escalation_trajectories),
        "escalation_before_collapse_count": (
            escalation_before_collapse_count
        ),
        "panic_collapse_total": panic_collapse_total,
        "instant_spike_panic_count": instant_spike_panic_count,
        "recovery_after_escalation_total": (
            recovery_after_escalation_total
        ),
        "monotonic_trajectory_count": monotonic_count,
        "mean_collapse_onset_step": (
            mean(
                item["collapse_onset_step"]
                for item in collapse_trajectories
            )
            if collapse_trajectories
            else None
        ),
        "mean_first_escalation_step": (
            mean(
                item["first_escalation_step"]
                for item in escalation_trajectories
            )
            if escalation_trajectories
            else None
        ),
    }

    status = (
        "PASS"
        if (
            pass_trajectory_count == len(trajectory_results)
            and summary["collapse_trajectory_count"] >= 4
            and summary["escalation_trajectory_count"] >= 4
            and summary["panic_collapse_total"] == 0
            and summary["instant_spike_panic_count"] == 0
            and summary["recovery_after_escalation_total"] >= 2
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "trajectory_results": trajectory_results,
        "reproduction_command": (
            "python examples/temporal_collapse_degradation_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION - Temporal Collapse Degradation v0")
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)

    print()
    print("Summary")
    print("-" * 80)

    for key, value in summary.items():
        print(f"{key}: {value}")

    print()
    print("Trajectory summaries")
    print("-" * 80)

    for item in trajectory_results:
        print(
            f"{item['trajectory_name']:<34} "
            f"status={item['status']:<5} "
            f"first_non_pass={item['first_non_pass_step']} "
            f"first_escalate={item['first_escalation_step']} "
            f"collapse_onset={item['collapse_onset_step']} "
            f"recovery_after_esc={item['recovery_after_escalation_count']} "
            f"monotonic={item['trajectory_monotonicity']} "
            f"sequence={' -> '.join(item['action_sequence'])}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - temporal degradation produced coherent collapse dynamics."
        )
    else:
        print(
            "CHECK - temporal degradation did not satisfy collapse dynamics."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()