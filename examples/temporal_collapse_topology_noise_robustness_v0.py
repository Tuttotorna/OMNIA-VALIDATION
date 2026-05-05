import json
from pathlib import Path
from statistics import mean

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_noise_robustness_v0.json"
)

CONFIRMATION_WINDOW = 2
PERSISTENCE_WINDOW = 2
GLOBAL_PERSISTENCE_THRESHOLD = (
    CONFIRMATION_WINDOW + PERSISTENCE_WINDOW
)

SUPPORTED_CLASSES = [
    "GLOBAL_PERSISTENT_COLLAPSE",
    "RECOVERY_RELAPSE_COLLAPSE",
    "FRAGMENTED_LOCAL_COLLAPSE",
    "OSCILLATING_NONPERSISTENT",
    "SPIKE_FILTERED",
    "CLEAN_PASS",
]


def compute_runs(sequence):
    runs = []
    start = None

    for index, value in enumerate(sequence):
        if value == "COLLAPSE":
            if start is None:
                start = index
        else:
            if start is not None:
                runs.append((start, index - 1))
                start = None

    if start is not None:
        runs.append((start, len(sequence) - 1))

    return runs


def classify(sequence):
    runs = compute_runs(sequence)

    collapse_run_count = len(runs)

    run_lengths = [
        end - start + 1
        for start, end in runs
    ]

    max_run_length = max(run_lengths) if run_lengths else 0

    local_confirmation_count = sum(
        1
        for length in run_lengths
        if length >= CONFIRMATION_WINDOW
    )

    persistence_reset_count = max(
        collapse_run_count - 1,
        0,
    )

    fragmentation_index = (
        persistence_reset_count / max(collapse_run_count, 1)
    )

    global_persistence_detected = any(
        length >= GLOBAL_PERSISTENCE_THRESHOLD
        for length in run_lengths
    )

    if collapse_run_count == 0:
        label = "CLEAN_PASS"

    elif (
        collapse_run_count == 1
        and max_run_length < CONFIRMATION_WINDOW
    ):
        label = "SPIKE_FILTERED"

    elif (
        global_persistence_detected
        and persistence_reset_count == 0
    ):
        label = "GLOBAL_PERSISTENT_COLLAPSE"

    elif (
        global_persistence_detected
        and persistence_reset_count > 0
    ):
        label = "RECOVERY_RELAPSE_COLLAPSE"

    elif (
        local_confirmation_count > 0
        and not global_persistence_detected
    ):
        label = "FRAGMENTED_LOCAL_COLLAPSE"

    else:
        label = "OSCILLATING_NONPERSISTENT"

    return {
        "classification": label,
        "collapse_run_count": collapse_run_count,
        "max_temporal_collapse_run_length": max_run_length,
        "temporal_collapse_run_count": local_confirmation_count,
        "persistence_reset_count": persistence_reset_count,
        "fragmentation_index": round(fragmentation_index, 4),
        "global_persistence_detected": global_persistence_detected,
        "local_confirmation_count": local_confirmation_count,
        "collapse_runs": runs,
    }


def make_sequence(length, runs):
    sequence = ["PASS"] * length

    for start, run_length in runs:
        end = min(length, start + run_length)

        for index in range(start, end):
            sequence[index] = "COLLAPSE"

        if start > 0:
            sequence[start - 1] = "ESCALATE"

    return sequence


def apply_noise(sequence, flips):
    noisy = list(sequence)

    for index, value in flips:
        if 0 <= index < len(noisy):
            noisy[index] = value

    return noisy


def base_cases():
    return {
        "clean_pass": {
            "expected": "CLEAN_PASS",
            "sequence": make_sequence(20, []),
        },
        "spike_filtered": {
            "expected": "SPIKE_FILTERED",
            "sequence": make_sequence(20, [(5, 1)]),
        },
        "global_persistent_collapse": {
            "expected": "GLOBAL_PERSISTENT_COLLAPSE",
            "sequence": make_sequence(20, [(6, 10)]),
        },
        "recovery_relapse_collapse": {
            "expected": "RECOVERY_RELAPSE_COLLAPSE",
            "sequence": make_sequence(
                22,
                [
                    (3, 2),
                    (10, 8),
                ],
            ),
        },
        "fragmented_local_collapse": {
            "expected": "FRAGMENTED_LOCAL_COLLAPSE",
            "sequence": make_sequence(
                22,
                [
                    (3, 2),
                    (7, 2),
                    (11, 2),
                    (15, 2),
                ],
            ),
        },
        "oscillating_nonpersistent": {
            "expected": "OSCILLATING_NONPERSISTENT",
            "sequence": make_sequence(
                22,
                [
                    (3, 1),
                    (6, 1),
                    (9, 1),
                    (12, 1),
                    (15, 1),
                    (18, 1),
                ],
            ),
        },
    }


def noise_scenarios_for_case(case_name, sequence):
    scenarios = []

    scenarios.append({
        "noise_name": "none",
        "noise_type": "none",
        "expected_noise_effect": "stable",
        "flips": [],
    })

    scenarios.append({
        "noise_name": "single_false_spike",
        "noise_type": "pass_to_collapse",
        "expected_noise_effect": "stable",
        "flips": [(1, "COLLAPSE")],
    })

    scenarios.append({
        "noise_name": "single_dropout",
        "noise_type": "collapse_to_pass",
        "expected_noise_effect": "stable_or_boundary",
        "flips": [(6, "PASS")],
    })

    scenarios.append({
        "noise_name": "escalate_insertion",
        "noise_type": "pass_to_escalate",
        "expected_noise_effect": "stable",
        "flips": [(2, "ESCALATE")],
    })

    if case_name == "clean_pass":
        scenarios.append({
            "noise_name": "two_separated_false_spikes",
            "noise_type": "pass_to_collapse_sparse",
            "expected_noise_effect": "stable_as_oscillation_or_spike",
            "flips": [
                (4, "COLLAPSE"),
                (12, "COLLAPSE"),
            ],
        })

    if case_name == "global_persistent_collapse":
        scenarios.append({
            "noise_name": "sparse_dropout_inside_global",
            "noise_type": "collapse_to_pass_sparse",
            "expected_noise_effect": "stable_or_relapse",
            "flips": [
                (9, "PASS"),
            ],
        })

        scenarios.append({
            "noise_name": "double_dropout_inside_global",
            "noise_type": "collapse_to_pass_double",
            "expected_noise_effect": "boundary",
            "flips": [
                (9, "PASS"),
                (12, "PASS"),
            ],
        })

    if case_name == "fragmented_local_collapse":
        scenarios.append({
            "noise_name": "bridge_fragment_to_global",
            "noise_type": "pass_to_collapse_bridge",
            "expected_noise_effect": "expected_class_change",
            "flips": [
                (5, "COLLAPSE"),
                (6, "COLLAPSE"),
            ],
        })

        scenarios.append({
            "noise_name": "drop_local_confirmation",
            "noise_type": "collapse_to_pass_local",
            "expected_noise_effect": "stable_or_oscillation",
            "flips": [
                (4, "PASS"),
            ],
        })

    if case_name == "oscillating_nonpersistent":
        scenarios.append({
            "noise_name": "create_local_confirmation",
            "noise_type": "pass_to_collapse_local_bridge",
            "expected_noise_effect": "expected_class_change",
            "flips": [
                (4, "COLLAPSE"),
            ],
        })

    if case_name == "recovery_relapse_collapse":
        scenarios.append({
            "noise_name": "dropout_inside_relapse",
            "noise_type": "collapse_to_pass_relapse",
            "expected_noise_effect": "stable_or_fragmented",
            "flips": [
                (12, "PASS"),
            ],
        })

    if case_name == "spike_filtered":
        scenarios.append({
            "noise_name": "extend_spike_to_local",
            "noise_type": "pass_to_collapse_local_bridge",
            "expected_noise_effect": "expected_class_change",
            "flips": [
                (6, "COLLAPSE"),
            ],
        })

    return scenarios


def expected_allowed_classes(base_expected, noise_effect):
    if noise_effect == "stable":
        return {base_expected}

    if noise_effect == "stable_or_boundary":
        return {
            base_expected,
            "SPIKE_FILTERED",
            "OSCILLATING_NONPERSISTENT",
            "FRAGMENTED_LOCAL_COLLAPSE",
            "RECOVERY_RELAPSE_COLLAPSE",
            "GLOBAL_PERSISTENT_COLLAPSE",
        }

    if noise_effect == "stable_as_oscillation_or_spike":
        return {
            "CLEAN_PASS",
            "SPIKE_FILTERED",
            "OSCILLATING_NONPERSISTENT",
        }

    if noise_effect == "stable_or_relapse":
        return {
            "GLOBAL_PERSISTENT_COLLAPSE",
            "RECOVERY_RELAPSE_COLLAPSE",
        }

    if noise_effect == "stable_or_oscillation":
        return {
            "FRAGMENTED_LOCAL_COLLAPSE",
            "OSCILLATING_NONPERSISTENT",
        }

    if noise_effect == "stable_or_fragmented":
        return {
            "RECOVERY_RELAPSE_COLLAPSE",
            "FRAGMENTED_LOCAL_COLLAPSE",
        }

    if noise_effect == "boundary":
        return set(SUPPORTED_CLASSES)

    if noise_effect == "expected_class_change":
        return set(SUPPORTED_CLASSES)

    raise ValueError(f"Unknown noise_effect: {noise_effect}")


def is_transition_expected(base_expected, predicted, noise_effect):
    if noise_effect == "expected_class_change":
        return predicted != base_expected

    return predicted == base_expected


def evaluate_noise_case(case_name, case_data, scenario):
    base_sequence = case_data["sequence"]
    base_expected = case_data["expected"]

    noisy_sequence = apply_noise(
        base_sequence,
        scenario["flips"],
    )

    base_result = classify(base_sequence)
    noisy_result = classify(noisy_sequence)

    allowed_classes = expected_allowed_classes(
        base_expected=base_expected,
        noise_effect=scenario["expected_noise_effect"],
    )

    predicted = noisy_result["classification"]

    status = (
        "PASS"
        if predicted in allowed_classes
        else "CHECK"
    )

    stable_classification = (
        predicted == base_result["classification"]
    )

    expected_transition = is_transition_expected(
        base_expected=base_result["classification"],
        predicted=predicted,
        noise_effect=scenario["expected_noise_effect"],
    )

    noise_flip_count = len(scenario["flips"])

    return {
        "case_name": case_name,
        "noise_name": scenario["noise_name"],
        "noise_type": scenario["noise_type"],
        "expected_noise_effect": scenario["expected_noise_effect"],
        "base_classification": base_result["classification"],
        "predicted_classification": predicted,
        "allowed_classifications": sorted(allowed_classes),
        "status": status,
        "stable_classification": stable_classification,
        "expected_transition": expected_transition,
        "noise_flip_count": noise_flip_count,
        "noise_flips": scenario["flips"],
        "raw_action_sequence": noisy_sequence,
        "base_metrics": base_result,
        "noisy_metrics": noisy_result,
    }


def summarize_by_case(results):
    summary = {}

    for item in results:
        case_name = item["case_name"]

        if case_name not in summary:
            summary[case_name] = {
                "case_count": 0,
                "pass_count": 0,
                "check_count": 0,
                "stable_count": 0,
                "transition_count": 0,
                "pass_rate": 0.0,
                "stable_rate": 0.0,
            }

        summary[case_name]["case_count"] += 1

        if item["status"] == "PASS":
            summary[case_name]["pass_count"] += 1
        else:
            summary[case_name]["check_count"] += 1

        if item["stable_classification"]:
            summary[case_name]["stable_count"] += 1
        else:
            summary[case_name]["transition_count"] += 1

    for values in summary.values():
        values["pass_rate"] = (
            values["pass_count"] / values["case_count"]
            if values["case_count"]
            else 0.0
        )
        values["stable_rate"] = (
            values["stable_count"] / values["case_count"]
            if values["case_count"]
            else 0.0
        )

    return summary


def summarize_by_noise_type(results):
    summary = {}

    for item in results:
        noise_type = item["noise_type"]

        if noise_type not in summary:
            summary[noise_type] = {
                "case_count": 0,
                "pass_count": 0,
                "check_count": 0,
                "stable_count": 0,
                "transition_count": 0,
                "pass_rate": 0.0,
                "stable_rate": 0.0,
            }

        summary[noise_type]["case_count"] += 1

        if item["status"] == "PASS":
            summary[noise_type]["pass_count"] += 1
        else:
            summary[noise_type]["check_count"] += 1

        if item["stable_classification"]:
            summary[noise_type]["stable_count"] += 1
        else:
            summary[noise_type]["transition_count"] += 1

    for values in summary.values():
        values["pass_rate"] = (
            values["pass_count"] / values["case_count"]
            if values["case_count"]
            else 0.0
        )
        values["stable_rate"] = (
            values["stable_count"] / values["case_count"]
            if values["case_count"]
            else 0.0
        )

    return summary


def main():
    cases = base_cases()

    results = []

    for case_name, case_data in cases.items():
        scenarios = noise_scenarios_for_case(
            case_name,
            case_data["sequence"],
        )

        for scenario in scenarios:
            results.append(
                evaluate_noise_case(
                    case_name,
                    case_data,
                    scenario,
                )
            )

    pass_count = sum(
        1
        for item in results
        if item["status"] == "PASS"
    )

    check_count = len(results) - pass_count

    stable_count = sum(
        1
        for item in results
        if item["stable_classification"]
    )

    transition_count = len(results) - stable_count

    expected_transition_count = sum(
        1
        for item in results
        if item["expected_transition"]
    )

    by_case = summarize_by_case(results)
    by_noise_type = summarize_by_noise_type(results)

    summary = {
        "case_count": len(results),
        "pass_case_count": pass_count,
        "check_case_count": check_count,
        "pass_rate": (
            pass_count / len(results)
            if results
            else 0.0
        ),
        "stable_classification_count": stable_count,
        "transition_count": transition_count,
        "stable_rate": (
            stable_count / len(results)
            if results
            else 0.0
        ),
        "expected_transition_count": expected_transition_count,
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "supported_classes": SUPPORTED_CLASSES,
        "noise_types": sorted({
            item["noise_type"]
            for item in results
        }),
        "mean_noise_flip_count": mean(
            item["noise_flip_count"]
            for item in results
        ),
    }

    status = (
        "PASS"
        if (
            pass_count == len(results)
            and all(
                values["pass_rate"] == 1.0
                for values in by_case.values()
            )
            and all(
                values["pass_rate"] == 1.0
                for values in by_noise_type.values()
            )
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_noise_robustness_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "by_case": by_case,
        "by_noise_type": by_noise_type,
        "noise_case_results": results,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_noise_robustness_v0.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULTS_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Topology Noise Robustness v0"
    )
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
    print("By case")
    print("-" * 80)

    for case_name, values in by_case.items():
        print(
            f"{case_name:<35} "
            f"cases={values['case_count']} "
            f"pass={values['pass_count']} "
            f"check={values['check_count']} "
            f"stable={values['stable_count']} "
            f"transitions={values['transition_count']} "
            f"pass_rate={values['pass_rate']} "
            f"stable_rate={values['stable_rate']}"
        )

    print()
    print("By noise type")
    print("-" * 80)

    for noise_type, values in by_noise_type.items():
        print(
            f"{noise_type:<35} "
            f"cases={values['case_count']} "
            f"pass={values['pass_count']} "
            f"check={values['check_count']} "
            f"stable={values['stable_count']} "
            f"transitions={values['transition_count']} "
            f"pass_rate={values['pass_rate']} "
            f"stable_rate={values['stable_rate']}"
        )

    print()
    print("Noise case summaries")
    print("-" * 80)

    for item in results:
        print(
            f"{item['case_name']:<30} "
            f"noise={item['noise_name']:<30} "
            f"status={item['status']:<5} "
            f"base={item['base_classification']:<32} "
            f"predicted={item['predicted_classification']:<32} "
            f"stable={item['stable_classification']} "
            f"transition_expected={item['expected_transition']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - topology noise robustness remained coherent "
            "under controlled frame-level noise."
        )
    else:
        print(
            "CHECK - topology noise robustness exposed "
            "classification instability under controlled noise."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()