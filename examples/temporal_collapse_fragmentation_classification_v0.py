import json
from pathlib import Path

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_fragmentation_classification_v0.json"
)

CONFIRMATION_WINDOW = 2
PERSISTENCE_WINDOW = 2
RESET_WINDOW = 2

TRAJECTORIES = {
    "clean_pass": [
        "PASS", "PASS", "PASS", "PASS",
        "PASS", "PASS", "PASS", "PASS",
        "PASS", "PASS", "PASS", "PASS",
        "PASS", "PASS", "PASS", "PASS",
    ],

    "global_persistent_collapse": [
        "PASS", "PASS", "RETRY", "ESCALATE",
        "COLLAPSE", "COLLAPSE", "COLLAPSE", "COLLAPSE",
        "COLLAPSE", "COLLAPSE", "COLLAPSE", "COLLAPSE",
        "COLLAPSE", "COLLAPSE", "COLLAPSE", "COLLAPSE",
    ],

    "recovery_relapse_collapse": [
        "PASS", "ESCALATE", "COLLAPSE", "COLLAPSE",
        "PASS", "RETRY", "PASS", "ESCALATE",
        "COLLAPSE", "COLLAPSE", "COLLAPSE", "COLLAPSE",
        "COLLAPSE", "COLLAPSE", "COLLAPSE", "COLLAPSE",
    ],

    "fragmented_local_collapse": [
        "PASS", "ESCALATE", "COLLAPSE", "COLLAPSE",
        "PASS", "COLLAPSE", "COLLAPSE", "PASS",
        "COLLAPSE", "COLLAPSE", "PASS", "COLLAPSE",
        "COLLAPSE", "PASS", "COLLAPSE", "COLLAPSE",
    ],

    "oscillating_nonpersistent": [
        "PASS", "ESCALATE", "COLLAPSE", "PASS",
        "COLLAPSE", "PASS", "COLLAPSE", "PASS",
        "COLLAPSE", "PASS", "COLLAPSE", "PASS",
        "COLLAPSE", "PASS", "COLLAPSE", "PASS",
    ],

    "spike_filtered": [
        "PASS", "COLLAPSE", "PASS", "PASS",
        "PASS", "PASS", "PASS", "PASS",
        "PASS", "PASS", "PASS", "PASS",
        "PASS", "PASS", "PASS", "PASS",
    ],
}


def compute_runs(sequence):
    runs = []
    start = None

    for i, value in enumerate(sequence):

        if value == "COLLAPSE":
            if start is None:
                start = i

        else:
            if start is not None:
                runs.append((start, i - 1))
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

    max_run_length = (
        max(run_lengths)
        if run_lengths else 0
    )

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
        persistence_reset_count
        / max(collapse_run_count, 1)
    )

    global_persistence_detected = any(
        length >= (
            CONFIRMATION_WINDOW +
            PERSISTENCE_WINDOW
        )
        for length in run_lengths
    )

    has_any_collapse = collapse_run_count > 0

    if not has_any_collapse:
        label = "CLEAN_PASS"

    elif (
        collapse_run_count == 1
        and max_run_length == 1
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


def evaluate():

    trajectory_results = []

    all_correct = True

    expected_labels = {
        "clean_pass":
            "CLEAN_PASS",

        "global_persistent_collapse":
            "GLOBAL_PERSISTENT_COLLAPSE",

        "recovery_relapse_collapse":
            "RECOVERY_RELAPSE_COLLAPSE",

        "fragmented_local_collapse":
            "FRAGMENTED_LOCAL_COLLAPSE",

        "oscillating_nonpersistent":
            "OSCILLATING_NONPERSISTENT",

        "spike_filtered":
            "SPIKE_FILTERED",
    }

    for name, sequence in TRAJECTORIES.items():

        result = classify(sequence)

        expected = expected_labels[name]

        passed = (
            result["classification"]
            == expected
        )

        if not passed:
            all_correct = False

        trajectory_results.append({
            "trajectory_name": name,
            "expected_classification": expected,
            "predicted_classification":
                result["classification"],
            "status":
                "PASS" if passed else "CHECK",
            "raw_action_sequence": sequence,
            **result,
        })

    pass_count = sum(
        1
        for item in trajectory_results
        if item["status"] == "PASS"
    )

    check_count = sum(
        1
        for item in trajectory_results
        if item["status"] == "CHECK"
    )

    result = {
        "experiment":
            "temporal_collapse_fragmentation_classification_v0",

        "version":
            VERSION,

        "status":
            "PASS" if all_correct else "CHECK",

        "summary": {
            "trajectory_count":
                len(TRAJECTORIES),

            "pass_trajectory_count":
                pass_count,

            "check_trajectory_count":
                check_count,

            "confirmation_window":
                CONFIRMATION_WINDOW,

            "persistence_window":
                PERSISTENCE_WINDOW,

            "reset_window":
                RESET_WINDOW,

            "supported_classes": [
                "GLOBAL_PERSISTENT_COLLAPSE",
                "RECOVERY_RELAPSE_COLLAPSE",
                "FRAGMENTED_LOCAL_COLLAPSE",
                "OSCILLATING_NONPERSISTENT",
                "SPIKE_FILTERED",
                "CLEAN_PASS",
            ],
        },

        "trajectory_results":
            trajectory_results,
    }

    return result


def main():

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Fragmentation "
        "Classification v0"
    )
    print("=" * 80)

    result = evaluate()

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print()
    print("Status:", result["status"])
    print("Version:", result["version"])

    print()
    print("Summary")
    print("-" * 80)

    for key, value in result["summary"].items():
        print(f"{key}: {value}")

    print()
    print("Trajectory summaries")
    print("-" * 80)

    for item in result["trajectory_results"]:

        print(
            f"{item['trajectory_name']:<35} "
            f"status={item['status']:<5} "
            f"class={item['classification']:<32} "
            f"runs={item['collapse_run_count']} "
            f"max_run={item['max_temporal_collapse_run_length']} "
            f"local={item['local_confirmation_count']} "
            f"global={item['global_persistence_detected']} "
            f"resets={item['persistence_reset_count']} "
            f"fragmentation={item['fragmentation_index']}"
        )

        print(
            "raw="
            + " -> ".join(
                item["raw_action_sequence"]
            )
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if result["status"] == "PASS":
        print(
            "PASS - fragmentation topology "
            "classification successfully "
            "separated persistent, fragmented, "
            "oscillating, spike, and clean regimes."
        )

    else:
        print(
            "CHECK - fragmentation classification "
            "did not fully separate all "
            "collapse topologies."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()