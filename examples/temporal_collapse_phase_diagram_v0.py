import json
import os
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "temporal_collapse_phase_diagram_v0.json",
)

CONFIRMATION_WINDOWS = [2, 3, 4, 5, 6]
PERSISTENCE_WINDOWS = [2, 3, 4, 5, 6]
TRAJECTORY_LENGTHS = [8, 10, 12]


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


def temporal_confirmation_action(
    raw_action,
    previous_raw_actions,
    confirmation_window,
):
    if raw_action != "COLLAPSE":
        return raw_action

    recent = previous_raw_actions[-(confirmation_window - 1):]
    confirmed = recent + [raw_action]

    if len(confirmed) < confirmation_window:
        return "ESCALATE"

    if all(action == "COLLAPSE" for action in confirmed):
        return "COLLAPSE"

    return "ESCALATE"


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


def evaluate_state(
    state,
    previous_raw_actions,
    confirmation_window,
):
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
        "effective_signal_gate": effective_signal_gate(
            normalized_effective
        ),
        "recoverability_gate": recoverability_gate(
            recoverability_score
        ),
        "divergence_gate": divergence_gate(divergence),
        "collapse_gate": collapse_gate(
            state["collapse_resistance"]
        ),
        "projection_gate": projection_gate(
            state["projection_stability"]
        ),
    }

    raw_action = structural_arbitration(signal_actions)

    temporal_action = temporal_confirmation_action(
        raw_action=raw_action,
        previous_raw_actions=previous_raw_actions,
        confirmation_window=confirmation_window,
    )

    return {
        "raw_action": raw_action,
        "temporal_action": temporal_action,
    }


def extend_sequence(seed_states, target_length):
    if len(seed_states) > target_length:
        return seed_states[:target_length]

    if len(seed_states) == target_length:
        return list(seed_states)

    states = list(seed_states)
    last = states[-1]

    while len(states) < target_length:
        degraded = build_state(
            raw_count=last["raw_count"],
            non_redundancy=last["non_redundancy"] * 0.92,
            family_balance=last["family_balance"] * 0.92,
            relation_entropy=last["relation_entropy"] * 0.94,
            collapse_resistance=last["collapse_resistance"] * 0.80,
            projection_stability=last["projection_stability"] * 0.80,
        )

        states.append(degraded)
        last = degraded

    return states


def generate_base_trajectories():
    trajectories = {}

    trajectories["stable_control"] = [
        build_state(60, 0.93, 0.88, 0.72, 0.96, 0.95),
        build_state(60, 0.92, 0.88, 0.72, 0.95, 0.94),
        build_state(60, 0.92, 0.87, 0.71, 0.95, 0.94),
        build_state(60, 0.91, 0.87, 0.71, 0.94, 0.93),
        build_state(60, 0.91, 0.86, 0.70, 0.94, 0.93),
        build_state(60, 0.90, 0.86, 0.70, 0.93, 0.92),
        build_state(60, 0.90, 0.85, 0.69, 0.92, 0.91),
        build_state(60, 0.89, 0.85, 0.69, 0.92, 0.91),
    ]

    trajectories["persistent_collapse"] = [
        build_state(100, 0.88, 0.82, 0.70, 0.88, 0.86),
        build_state(100, 0.74, 0.70, 0.68, 0.76, 0.74),
        build_state(100, 0.58, 0.55, 0.63, 0.61, 0.58),
        build_state(100, 0.42, 0.38, 0.57, 0.43, 0.40),
        build_state(100, 0.26, 0.24, 0.50, 0.22, 0.18),
        build_state(100, 0.14, 0.13, 0.44, 0.08, 0.07),
        build_state(100, 0.10, 0.09, 0.40, 0.05, 0.05),
        build_state(100, 0.08, 0.07, 0.36, 0.04, 0.04),
    ]

    trajectories["instant_noise_spike"] = [
        build_state(75, 0.86, 0.82, 0.70, 0.88, 0.86),
        build_state(75, 0.18, 0.15, 0.42, 0.12, 0.10),
        build_state(75, 0.82, 0.78, 0.68, 0.84, 0.82),
        build_state(75, 0.80, 0.76, 0.67, 0.82, 0.80),
        build_state(75, 0.78, 0.74, 0.66, 0.80, 0.78),
        build_state(75, 0.76, 0.72, 0.65, 0.78, 0.76),
        build_state(75, 0.74, 0.70, 0.64, 0.76, 0.74),
        build_state(75, 0.72, 0.68, 0.63, 0.74, 0.72),
    ]

    trajectories["oscillating_nonpersistent"] = [
        build_state(95, 0.80, 0.76, 0.70, 0.82, 0.80),
        build_state(95, 0.34, 0.30, 0.58, 0.38, 0.35),
        build_state(95, 0.70, 0.66, 0.67, 0.72, 0.70),
        build_state(95, 0.28, 0.24, 0.55, 0.30, 0.28),
        build_state(95, 0.62, 0.58, 0.63, 0.64, 0.60),
        build_state(95, 0.12, 0.10, 0.42, 0.08, 0.07),
        build_state(95, 0.58, 0.54, 0.60, 0.58, 0.56),
        build_state(95, 0.56, 0.52, 0.58, 0.56, 0.54),
    ]

    return trajectories


def has_persistent_collapse(actions, persistence_window):
    for index in range(len(actions) - persistence_window + 1):
        window = actions[index:index + persistence_window]

        if all(action == "COLLAPSE" for action in window):
            return True

    return False


def first_temporal_collapse(actions):
    for index, action in enumerate(actions):
        if action == "COLLAPSE":
            return index

    return None


def first_persistent_collapse(actions, persistence_window):
    for index in range(len(actions) - persistence_window + 1):
        window = actions[index:index + persistence_window]

        if all(action == "COLLAPSE" for action in window):
            return index + persistence_window - 1

    return None


def evaluate_trajectory(
    states,
    confirmation_window,
    persistence_window,
):
    previous_raw_actions = []

    raw_actions = []
    temporal_actions = []

    for state in states:
        result = evaluate_state(
            state=state,
            previous_raw_actions=previous_raw_actions,
            confirmation_window=confirmation_window,
        )

        raw_actions.append(result["raw_action"])
        temporal_actions.append(result["temporal_action"])

        previous_raw_actions.append(result["raw_action"])

    return {
        "raw_actions": raw_actions,
        "temporal_actions": temporal_actions,
        "first_temporal_collapse": first_temporal_collapse(
            temporal_actions
        ),
        "first_persistent_collapse": first_persistent_collapse(
            temporal_actions,
            persistence_window,
        ),
        "persistent_collapse": has_persistent_collapse(
            temporal_actions,
            persistence_window,
        ),
    }


def evaluate_cell(
    confirmation_window,
    persistence_window,
    trajectory_length,
):
    base_trajectories = generate_base_trajectories()

    trajectories = {
        name: extend_sequence(states, trajectory_length)
        for name, states in base_trajectories.items()
    }

    trajectory_results = {}

    for name, states in trajectories.items():
        trajectory_results[name] = evaluate_trajectory(
            states=states,
            confirmation_window=confirmation_window,
            persistence_window=persistence_window,
        )

    stable = trajectory_results["stable_control"]
    persistent = trajectory_results["persistent_collapse"]
    spike = trajectory_results["instant_noise_spike"]
    oscillating = trajectory_results["oscillating_nonpersistent"]

    stable_pass = "COLLAPSE" not in stable["temporal_actions"]
    persistent_confirmed = persistent["persistent_collapse"]
    spike_filtered = "COLLAPSE" not in spike["temporal_actions"]
    oscillating_filtered = not oscillating["persistent_collapse"]

    status = (
        "PASS"
        if (
            stable_pass
            and persistent_confirmed
            and spike_filtered
            and oscillating_filtered
        )
        else "CHECK"
    )

    return {
        "confirmation_window": confirmation_window,
        "persistence_window": persistence_window,
        "trajectory_length": trajectory_length,
        "status": status,
        "stable_pass": stable_pass,
        "persistent_confirmed": persistent_confirmed,
        "spike_filtered": spike_filtered,
        "oscillating_filtered": oscillating_filtered,
        "first_temporal_collapse": persistent["first_temporal_collapse"],
        "first_persistent_collapse": (
            persistent["first_persistent_collapse"]
        ),
        "persistent_temporal_sequence": (
            persistent["temporal_actions"]
        ),
    }


def summarize_by_length(cell_results):
    summaries = {}

    for trajectory_length in TRAJECTORY_LENGTHS:
        subset = [
            item
            for item in cell_results
            if item["trajectory_length"] == trajectory_length
        ]

        pass_count = sum(
            1
            for item in subset
            if item["status"] == "PASS"
        )

        check_count = len(subset) - pass_count

        first_persistent_steps = [
            item["first_persistent_collapse"]
            for item in subset
            if item["first_persistent_collapse"] is not None
        ]

        summaries[str(trajectory_length)] = {
            "cell_count": len(subset),
            "pass_count": pass_count,
            "check_count": check_count,
            "pass_rate": safe_div(pass_count, len(subset)),
            "mean_first_persistent_collapse": (
                mean(first_persistent_steps)
                if first_persistent_steps
                else None
            ),
        }

    return summaries


def summarize_by_window(cell_results):
    summaries = {}

    for confirmation_window in CONFIRMATION_WINDOWS:
        subset = [
            item
            for item in cell_results
            if item["confirmation_window"] == confirmation_window
        ]

        pass_count = sum(
            1
            for item in subset
            if item["status"] == "PASS"
        )

        summaries[f"cw{confirmation_window}"] = {
            "cell_count": len(subset),
            "pass_count": pass_count,
            "check_count": len(subset) - pass_count,
            "pass_rate": safe_div(pass_count, len(subset)),
        }

    return summaries


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    cell_results = []

    for trajectory_length in TRAJECTORY_LENGTHS:
        for confirmation_window in CONFIRMATION_WINDOWS:
            for persistence_window in PERSISTENCE_WINDOWS:
                cell_results.append(
                    evaluate_cell(
                        confirmation_window=confirmation_window,
                        persistence_window=persistence_window,
                        trajectory_length=trajectory_length,
                    )
                )

    total_cell_count = len(cell_results)

    pass_cell_count = sum(
        1
        for item in cell_results
        if item["status"] == "PASS"
    )

    check_cell_count = total_cell_count - pass_cell_count

    safe_cell_count = sum(
        1
        for item in cell_results
        if (
            item["stable_pass"]
            and item["spike_filtered"]
            and item["oscillating_filtered"]
        )
    )

    confirmed_cells = [
        item
        for item in cell_results
        if item["persistent_confirmed"]
    ]

    first_persistent_values = [
        item["first_persistent_collapse"]
        for item in confirmed_cells
        if item["first_persistent_collapse"] is not None
    ]

    summary = {
        "trajectory_lengths": TRAJECTORY_LENGTHS,
        "confirmation_windows": CONFIRMATION_WINDOWS,
        "persistence_windows": PERSISTENCE_WINDOWS,
        "total_cell_count": total_cell_count,
        "pass_cell_count": pass_cell_count,
        "check_cell_count": check_cell_count,
        "pass_rate": safe_div(pass_cell_count, total_cell_count),
        "safe_cell_count": safe_cell_count,
        "safety_rate": safe_div(safe_cell_count, total_cell_count),
        "persistent_confirmed_count": len(confirmed_cells),
        "persistent_confirmed_rate": safe_div(
            len(confirmed_cells),
            total_cell_count,
        ),
        "mean_first_persistent_collapse": (
            mean(first_persistent_values)
            if first_persistent_values
            else None
        ),
        "by_trajectory_length": summarize_by_length(cell_results),
        "by_confirmation_window": summarize_by_window(cell_results),
    }

    status = (
        "PASS"
        if (
            summary["safety_rate"] == 1.0
            and summary["pass_rate"] >= 0.50
            and summary["persistent_confirmed_rate"] >= 0.50
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "cell_results": cell_results,
        "reproduction_command": (
            "python examples/temporal_collapse_phase_diagram_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION - Temporal Collapse Phase Diagram v0")
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)

    print()
    print("Summary")
    print("-" * 80)

    for key, value in summary.items():
        if key in {
            "by_trajectory_length",
            "by_confirmation_window",
        }:
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

    print()
    print("Phase cells")
    print("-" * 80)

    for item in cell_results:
        print(
            f"L={item['trajectory_length']:<2} "
            f"cw={item['confirmation_window']} "
            f"pw={item['persistence_window']} "
            f"status={item['status']:<5} "
            f"safe={item['stable_pass'] and item['spike_filtered'] and item['oscillating_filtered']} "
            f"persistent={item['persistent_confirmed']} "
            f"first_temporal={item['first_temporal_collapse']} "
            f"first_persistent={item['first_persistent_collapse']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - temporal phase diagram exposed a stable "
            "observability boundary."
        )
    else:
        print(
            "CHECK - temporal phase diagram did not expose enough "
            "stable observability."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()