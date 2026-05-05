import json
from pathlib import Path
from statistics import mean

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_window_sensitivity_v0.json"
)

CONFIRMATION_WINDOWS = [2, 3, 4]
PERSISTENCE_WINDOWS = [2, 3, 4]

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


def classify(sequence, confirmation_window, persistence_window):
    global_threshold = confirmation_window + persistence_window

    runs = compute_runs(sequence)

    collapse_run_count = len(runs)

    run_lengths = [
        end - start + 1
        for start, end in runs
    ]

    max_run_length = (
        max(run_lengths)
        if run_lengths
        else 0
    )

    local_confirmation_count = sum(
        1
        for length in run_lengths
        if length >= confirmation_window
    )

    persistence_reset_count = max(
        collapse_run_count - 1,
        0,
    )

    fragmentation_index = (
        persistence_reset_count / max(collapse_run_count, 1)
    )

    global_persistence_detected = any(
        length >= global_threshold
        for length in run_lengths
    )

    if collapse_run_count == 0:
        label = "CLEAN_PASS"

    elif (
        collapse_run_count == 1
        and max_run_length < confirmation_window
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
        "global_persistence_threshold": global_threshold,
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


def expected_class_for_case(case_type, confirmation_window, persistence_window):
    global_threshold = confirmation_window + persistence_window

    if case_type == "clean":
        return "CLEAN_PASS"

    if case_type == "spike_below_confirmation":
        return "SPIKE_FILTERED"

    if case_type == "single_local_threshold":
        return "FRAGMENTED_LOCAL_COLLAPSE"

    if case_type == "single_global_threshold":
        return "GLOBAL_PERSISTENT_COLLAPSE"

    if case_type == "oscillation_below_confirmation":
        return "OSCILLATING_NONPERSISTENT"

    if case_type == "fragmentation_at_confirmation":
        return "FRAGMENTED_LOCAL_COLLAPSE"

    if case_type == "recovery_relapse_global":
        return "RECOVERY_RELAPSE_COLLAPSE"

    raise ValueError(f"Unknown case_type: {case_type}")


def generate_cases_for_window(confirmation_window, persistence_window):
    global_threshold = confirmation_window + persistence_window

    length = max(24, global_threshold * 4)

    cases = []

    cases.append({
        "case_name": "clean",
        "case_type": "clean",
        "sequence": make_sequence(length, []),
    })

    cases.append({
        "case_name": "spike_below_confirmation",
        "case_type": "spike_below_confirmation",
        "sequence": make_sequence(
            length,
            [(4, max(1, confirmation_window - 1))],
        ),
    })

    cases.append({
        "case_name": "single_local_threshold",
        "case_type": "single_local_threshold",
        "sequence": make_sequence(
            length,
            [(4, confirmation_window)],
        ),
    })

    cases.append({
        "case_name": "single_global_threshold",
        "case_type": "single_global_threshold",
        "sequence": make_sequence(
            length,
            [(4, global_threshold)],
        ),
    })

    oscillation_runs = [
        (2 + index * (confirmation_window + 1), 1)
        for index in range(5)
    ]

    cases.append({
        "case_name": "oscillation_below_confirmation",
        "case_type": "oscillation_below_confirmation",
        "sequence": make_sequence(
            length,
            oscillation_runs,
        ),
    })

    fragmentation_runs = [
        (2 + index * (confirmation_window + 1), confirmation_window)
        for index in range(5)
    ]

    cases.append({
        "case_name": "fragmentation_at_confirmation",
        "case_type": "fragmentation_at_confirmation",
        "sequence": make_sequence(
            length,
            fragmentation_runs,
        ),
    })

    cases.append({
        "case_name": "recovery_relapse_global",
        "case_type": "recovery_relapse_global",
        "sequence": make_sequence(
            length,
            [
                (2, confirmation_window),
                (
                    2 + confirmation_window + persistence_window + 2,
                    global_threshold,
                ),
            ],
        ),
    })

    return cases


def evaluate_case(case, confirmation_window, persistence_window):
    result = classify(
        sequence=case["sequence"],
        confirmation_window=confirmation_window,
        persistence_window=persistence_window,
    )

    expected = expected_class_for_case(
        case_type=case["case_type"],
        confirmation_window=confirmation_window,
        persistence_window=persistence_window,
    )

    status = (
        "PASS"
        if result["classification"] == expected
        else "CHECK"
    )

    return {
        "case_name": (
            f"cw{confirmation_window}_pw{persistence_window}_"
            f"{case['case_name']}"
        ),
        "case_type": case["case_type"],
        "confirmation_window": confirmation_window,
        "persistence_window": persistence_window,
        "global_persistence_threshold": (
            confirmation_window + persistence_window
        ),
        "expected_classification": expected,
        "predicted_classification": result["classification"],
        "status": status,
        "sequence_length": len(case["sequence"]),
        "raw_action_sequence": case["sequence"],
        **result,
    }


def summarize_by_case_type(case_results):
    summary = {}

    for item in case_results:
        case_type = item["case_type"]

        if case_type not in summary:
            summary[case_type] = {
                "case_count": 0,
                "pass_count": 0,
                "check_count": 0,
                "pass_rate": 0.0,
            }

        summary[case_type]["case_count"] += 1

        if item["status"] == "PASS":
            summary[case_type]["pass_count"] += 1
        else:
            summary[case_type]["check_count"] += 1

    for values in summary.values():
        values["pass_rate"] = (
            values["pass_count"] / values["case_count"]
            if values["case_count"]
            else 0.0
        )

    return summary


def summarize_by_window_pair(case_results):
    summary = {}

    for item in case_results:
        key = (
            f"cw{item['confirmation_window']}_"
            f"pw{item['persistence_window']}"
        )

        if key not in summary:
            summary[key] = {
                "confirmation_window": item["confirmation_window"],
                "persistence_window": item["persistence_window"],
                "global_persistence_threshold": (
                    item["global_persistence_threshold"]
                ),
                "case_count": 0,
                "pass_count": 0,
                "check_count": 0,
                "pass_rate": 0.0,
            }

        summary[key]["case_count"] += 1

        if item["status"] == "PASS":
            summary[key]["pass_count"] += 1
        else:
            summary[key]["check_count"] += 1

    for values in summary.values():
        values["pass_rate"] = (
            values["pass_count"] / values["case_count"]
            if values["case_count"]
            else 0.0
        )

    return summary


def main():
    case_results = []

    for confirmation_window in CONFIRMATION_WINDOWS:
        for persistence_window in PERSISTENCE_WINDOWS:
            cases = generate_cases_for_window(
                confirmation_window,
                persistence_window,
            )

            for case in cases:
                case_results.append(
                    evaluate_case(
                        case,
                        confirmation_window,
                        persistence_window,
                    )
                )

    pass_case_count = sum(
        1
        for item in case_results
        if item["status"] == "PASS"
    )

    check_case_count = len(case_results) - pass_case_count

    case_type_summary = summarize_by_case_type(case_results)
    window_pair_summary = summarize_by_window_pair(case_results)

    fragmentation_values = [
        item["fragmentation_index"]
        for item in case_results
    ]

    max_run_values = [
        item["max_temporal_collapse_run_length"]
        for item in case_results
    ]

    local_confirmation_values = [
        item["local_confirmation_count"]
        for item in case_results
    ]

    threshold_values = [
        item["global_persistence_threshold"]
        for item in case_results
    ]

    summary = {
        "case_count": len(case_results),
        "pass_case_count": pass_case_count,
        "check_case_count": check_case_count,
        "pass_rate": (
            pass_case_count / len(case_results)
            if case_results
            else 0.0
        ),
        "confirmation_windows": CONFIRMATION_WINDOWS,
        "persistence_windows": PERSISTENCE_WINDOWS,
        "supported_classes": SUPPORTED_CLASSES,
        "global_persistence_thresholds": sorted(
            set(threshold_values)
        ),
        "mean_fragmentation_index": (
            mean(fragmentation_values)
            if fragmentation_values
            else None
        ),
        "max_fragmentation_index": (
            max(fragmentation_values)
            if fragmentation_values
            else None
        ),
        "mean_max_temporal_collapse_run_length": (
            mean(max_run_values)
            if max_run_values
            else None
        ),
        "mean_local_confirmation_count": (
            mean(local_confirmation_values)
            if local_confirmation_values
            else None
        ),
    }

    status = (
        "PASS"
        if (
            pass_case_count == len(case_results)
            and all(
                item["pass_rate"] == 1.0
                for item in case_type_summary.values()
            )
            and all(
                item["pass_rate"] == 1.0
                for item in window_pair_summary.values()
            )
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_window_sensitivity_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "case_type_summary": case_type_summary,
        "window_pair_summary": window_pair_summary,
        "case_results": case_results,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_window_sensitivity_v0.py"
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
        "Temporal Collapse Topology Window Sensitivity v0"
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
    print("Case type summary")
    print("-" * 80)

    for case_type, values in case_type_summary.items():
        print(
            f"{case_type:<35} "
            f"cases={values['case_count']} "
            f"pass={values['pass_count']} "
            f"check={values['check_count']} "
            f"rate={values['pass_rate']}"
        )

    print()
    print("Window pair summary")
    print("-" * 80)

    for key, values in window_pair_summary.items():
        print(
            f"{key:<10} "
            f"threshold={values['global_persistence_threshold']} "
            f"cases={values['case_count']} "
            f"pass={values['pass_count']} "
            f"check={values['check_count']} "
            f"rate={values['pass_rate']}"
        )

    print()
    print("Case summaries")
    print("-" * 80)

    for item in case_results:
        print(
            f"{item['case_name']:<45} "
            f"status={item['status']:<5} "
            f"expected={item['expected_classification']:<32} "
            f"predicted={item['predicted_classification']:<32} "
            f"cw={item['confirmation_window']} "
            f"pw={item['persistence_window']} "
            f"thr={item['global_persistence_threshold']} "
            f"max_run={item['max_temporal_collapse_run_length']} "
            f"local={item['local_confirmation_count']} "
            f"global={item['global_persistence_detected']} "
            f"frag={item['fragmentation_index']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - topology window sensitivity remained "
            "coherent across confirmation and persistence "
            "window perturbations."
        )
    else:
        print(
            "CHECK - topology window sensitivity exposed "
            "classification instability under window perturbation."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()