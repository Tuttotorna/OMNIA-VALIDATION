import json
import os
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "temporal_collapse_confirmation_v0.json",
)

CONFIRMATION_WINDOW = 2


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


def compute_divergence(normalized_effective, recoverability_score):
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


def temporal_confirmation_action(raw_action, previous_raw_actions):
    if raw_action != "COLLAPSE":
        return raw_action

    recent = previous_raw_actions[-(CONFIRMATION_WINDOW - 1):]
    confirmed = recent + [raw_action]

    if len(confirmed) < CONFIRMATION_WINDOW:
        return "ESCALATE"

    if all(action == "COLLAPSE" for action in confirmed):
        return "COLLAPSE"

    return "ESCALATE"


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


def evaluate_state(trajectory_name, step, state, previous_raw_actions):
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

    raw_arbitration_action = structural_arbitration(signal_actions)

    temporal_arbitration_action = temporal_confirmation_action(
        raw_action=raw_arbitration_action,
        previous_raw_actions=previous_raw_actions,
    )

    disagreement = compute_disagreement(signal_actions)

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
        "raw_arbitration_action": raw_arbitration_action,
        "temporal_arbitration_action": temporal_arbitration_action,
        "unique_action_count": disagreement["unique_action_count"],
        "severity_spread": disagreement["severity_spread"],
        "severity_variance": disagreement["severity_variance"],
        "mean_severity": disagreement["mean_severity"],
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


def first_step_with_action(states, action, key):
    for item in states:
        if item[key] == action:
            return item["step"]

    return None


def count_action(states, action, key):
    return sum(
        1
        for item in states
        if item[key] == action
    )


def has_temporal_collapse_persistence(states):
    actions = [
        item["temporal_arbitration_action"]
        for item in states
    ]

    for index in range(len(actions) - 1):
        if actions[index] == "COLLAPSE" and actions[index + 1] == "COLLAPSE":
            return True

    return False


def count_raw_single_frame_collapses_filtered(states):
    count = 0

    for index, item in enumerate(states):
        if item["raw_arbitration_action"] != "COLLAPSE":
            continue

        previous_is_collapse = (
            index > 0
            and states[index - 1]["raw_arbitration_action"] == "COLLAPSE"
        )

        next_is_collapse = (
            index < len(states) - 1
            and states[index + 1]["raw_arbitration_action"] == "COLLAPSE"
        )

        if not previous_is_collapse and not next_is_collapse:
            count += 1

    return count


def count_temporal_filtered_collapses(states):
    return sum(
        1
        for item in states
        if item["raw_arbitration_action"] == "COLLAPSE"
        and item["temporal_arbitration_action"] != "COLLAPSE"
    )


def evaluate_trajectory(name, states):
    evaluated_states = []
    previous_raw_actions = []

    for index, state in enumerate(states):
        evaluated = evaluate_state(
            trajectory_name=name,
            step=index,
            state=state,
            previous_raw_actions=previous_raw_actions,
        )

        evaluated_states.append(evaluated)
        previous_raw_actions.append(evaluated["raw_arbitration_action"])

    first_raw_collapse_step = first_step_with_action(
        evaluated_states,
        "COLLAPSE",
        "raw_arbitration_action",
    )

    first_temporal_collapse_step = first_step_with_action(
        evaluated_states,
        "COLLAPSE",
        "temporal_arbitration_action",
    )

    first_raw_escalation_step = first_step_with_action(
        evaluated_states,
        "ESCALATE",
        "raw_arbitration_action",
    )

    first_temporal_escalation_step = first_step_with_action(
        evaluated_states,
        "ESCALATE",
        "temporal_arbitration_action",
    )

    raw_single_frame_collapse_count = (
        count_raw_single_frame_collapses_filtered(evaluated_states)
    )

    temporal_filtered_collapse_count = (
        count_temporal_filtered_collapses(evaluated_states)
    )

    persistent_temporal_collapse = has_temporal_collapse_persistence(
        evaluated_states
    )

    instant_spike_filtered = (
        name == "instant_noise_spike"
        and count_action(
            evaluated_states,
            "COLLAPSE",
            "raw_arbitration_action",
        ) >= 1
        and count_action(
            evaluated_states,
            "COLLAPSE",
            "temporal_arbitration_action",
        ) == 0
    )

    control_remained_pass = (
        name == "stable_control"
        and count_action(
            evaluated_states,
            "PASS",
            "temporal_arbitration_action",
        )
        == len(evaluated_states)
    )

    temporal_collapse_after_raw = (
        first_raw_collapse_step is not None
        and first_temporal_collapse_step is not None
        and first_temporal_collapse_step >= first_raw_collapse_step
    )

    temporal_warning_before_collapse = (
        first_temporal_escalation_step is not None
        and first_temporal_collapse_step is not None
        and first_temporal_escalation_step < first_temporal_collapse_step
    )

    trajectory_status = "PASS"

    if name == "stable_control":
        if not control_remained_pass:
            trajectory_status = "CHECK"

    elif name == "instant_noise_spike":
        if not instant_spike_filtered:
            trajectory_status = "CHECK"

    elif name in {
        "slow_decay",
        "projection_first_failure",
        "recoverability_first_failure",
        "delayed_multi_gate_collapse",
    }:
        if first_temporal_collapse_step is None:
            trajectory_status = "CHECK"

        if not temporal_warning_before_collapse:
            trajectory_status = "CHECK"

        if not persistent_temporal_collapse:
            trajectory_status = "CHECK"

    elif name in {
        "oscillating_instability",
        "false_recovery",
    }:
        if first_temporal_escalation_step is None:
            trajectory_status = "CHECK"

        if temporal_filtered_collapse_count < 1:
            trajectory_status = "CHECK"

    return {
        "trajectory_name": name,
        "status": trajectory_status,
        "state_count": len(evaluated_states),
        "first_raw_escalation_step": first_raw_escalation_step,
        "first_temporal_escalation_step": first_temporal_escalation_step,
        "first_raw_collapse_step": first_raw_collapse_step,
        "first_temporal_collapse_step": first_temporal_collapse_step,
        "raw_single_frame_collapse_count": raw_single_frame_collapse_count,
        "temporal_filtered_collapse_count": temporal_filtered_collapse_count,
        "persistent_temporal_collapse": persistent_temporal_collapse,
        "instant_spike_filtered": instant_spike_filtered,
        "control_remained_pass": control_remained_pass,
        "temporal_collapse_after_raw": temporal_collapse_after_raw,
        "temporal_warning_before_collapse": temporal_warning_before_collapse,
        "raw_action_sequence": [
            item["raw_arbitration_action"]
            for item in evaluated_states
        ],
        "temporal_action_sequence": [
            item["temporal_arbitration_action"]
            for item in evaluated_states
        ],
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

    temporal_collapse_trajectories = [
        item
        for item in trajectory_results
        if item["first_temporal_collapse_step"] is not None
    ]

    raw_collapse_trajectories = [
        item
        for item in trajectory_results
        if item["first_raw_collapse_step"] is not None
    ]

    filtered_collapse_total = sum(
        item["temporal_filtered_collapse_count"]
        for item in trajectory_results
    )

    raw_single_frame_collapse_total = sum(
        item["raw_single_frame_collapse_count"]
        for item in trajectory_results
    )

    instant_spike_filtered_count = sum(
        1
        for item in trajectory_results
        if item["instant_spike_filtered"]
    )

    persistent_temporal_collapse_count = sum(
        1
        for item in trajectory_results
        if item["persistent_temporal_collapse"]
    )

    warning_before_collapse_count = sum(
        1
        for item in trajectory_results
        if item["temporal_warning_before_collapse"]
    )

    control_pass_count = sum(
        1
        for item in trajectory_results
        if item["control_remained_pass"]
    )

    summary = {
        "trajectory_count": len(trajectory_results),
        "states_per_trajectory": 6,
        "total_state_count": len(trajectory_results) * 6,
        "confirmation_window": CONFIRMATION_WINDOW,
        "pass_trajectory_count": pass_trajectory_count,
        "check_trajectory_count": check_trajectory_count,
        "raw_collapse_trajectory_count": len(raw_collapse_trajectories),
        "temporal_collapse_trajectory_count": len(
            temporal_collapse_trajectories
        ),
        "filtered_collapse_total": filtered_collapse_total,
        "raw_single_frame_collapse_total": raw_single_frame_collapse_total,
        "instant_spike_filtered_count": instant_spike_filtered_count,
        "persistent_temporal_collapse_count": (
            persistent_temporal_collapse_count
        ),
        "warning_before_collapse_count": warning_before_collapse_count,
        "control_pass_count": control_pass_count,
        "mean_first_raw_collapse_step": (
            mean(
                item["first_raw_collapse_step"]
                for item in raw_collapse_trajectories
            )
            if raw_collapse_trajectories
            else None
        ),
        "mean_first_temporal_collapse_step": (
            mean(
                item["first_temporal_collapse_step"]
                for item in temporal_collapse_trajectories
            )
            if temporal_collapse_trajectories
            else None
        ),
    }

    status = (
        "PASS"
        if (
            pass_trajectory_count == len(trajectory_results)
            and summary["filtered_collapse_total"] >= 2
            and summary["instant_spike_filtered_count"] == 1
            and summary["persistent_temporal_collapse_count"] >= 4
            and summary["warning_before_collapse_count"] >= 4
            and summary["control_pass_count"] == 1
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "trajectory_results": trajectory_results,
        "reproduction_command": (
            "python examples/temporal_collapse_confirmation_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION - Temporal Collapse Confirmation v0")
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
            f"raw_collapse={item['first_raw_collapse_step']} "
            f"temporal_collapse={item['first_temporal_collapse_step']} "
            f"filtered={item['temporal_filtered_collapse_count']} "
            f"persistent={item['persistent_temporal_collapse']} "
            f"spike_filtered={item['instant_spike_filtered']} "
            f"raw={' -> '.join(item['raw_action_sequence'])} "
            f"temporal={' -> '.join(item['temporal_action_sequence'])}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - temporal confirmation filtered transient collapse "
            "and preserved persistent collapse."
        )
    else:
        print(
            "CHECK - temporal confirmation did not separate transient "
            "and persistent collapse."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()