import json
from pathlib import Path
from statistics import mean

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_threshold_boundary_v0.json"
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

    max_run_length = (
        max(run_lengths)
        if run_lengths
        else 0
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


def make_sequence(length, runs):
    sequence = ["PASS"] * length

    for start, run_length in runs:
        end = min(length, start + run_length)

        for index in range(start, end):
            sequence[index] = "COLLAPSE"

        if start > 0:
            sequence[start - 1] = "ESCALATE"

    return sequence


def generate_boundary_cases():
    cases = []

    # Boundary 1:
    # no collapse vs spike.
    cases.append({
        "case_name": "B00_clean_no_collapse",
        "boundary_family": "clean_vs_spike",
        "expected_classification": "CLEAN_PASS",
        "sequence": make_sequence(12, []),
    })

    cases.append({
        "case_name": "B01_single_spike_len1",
        "boundary_family": "clean_vs_spike",
        "expected_classification": "SPIKE_FILTERED",
        "sequence": make_sequence(12, [(4, 1)]),
    })

    # Boundary 2:
    # spike / oscillation vs local confirmation.
    cases.append({
        "case_name": "B02_single_run_len1_spike",
        "boundary_family": "spike_vs_local_confirmation",
        "expected_classification": "SPIKE_FILTERED",
        "sequence": make_sequence(12, [(4, 1)]),
    })

    cases.append({
        "case_name": "B03_single_run_len2_local",
        "boundary_family": "spike_vs_local_confirmation",
        "expected_classification": "FRAGMENTED_LOCAL_COLLAPSE",
        "sequence": make_sequence(12, [(4, 2)]),
    })

    # Boundary 3:
    # local confirmation vs global persistence.
    cases.append({
        "case_name": "B04_single_run_len3_local_only",
        "boundary_family": "local_vs_global",
        "expected_classification": "FRAGMENTED_LOCAL_COLLAPSE",
        "sequence": make_sequence(14, [(4, 3)]),
    })

    cases.append({
        "case_name": "B05_single_run_len4_global",
        "boundary_family": "local_vs_global",
        "expected_classification": "GLOBAL_PERSISTENT_COLLAPSE",
        "sequence": make_sequence(14, [(4, 4)]),
    })

    # Boundary 4:
    # high fragmentation without local confirmation
    # vs local fragmentation.
    cases.append({
        "case_name": "B06_many_len1_oscillation",
        "boundary_family": "oscillation_vs_fragmentation",
        "expected_classification": "OSCILLATING_NONPERSISTENT",
        "sequence": make_sequence(
            18,
            [
                (2, 1),
                (4, 1),
                (6, 1),
                (8, 1),
                (10, 1),
                (12, 1),
                (14, 1),
            ],
        ),
    })

    cases.append({
        "case_name": "B07_many_len2_fragmented",
        "boundary_family": "oscillation_vs_fragmentation",
        "expected_classification": "FRAGMENTED_LOCAL_COLLAPSE",
        "sequence": make_sequence(
            20,
            [
                (2, 2),
                (5, 2),
                (8, 2),
                (11, 2),
                (14, 2),
            ],
        ),
    })

    # Boundary 5:
    # fragmented local collapse vs recovery-relapse.
    cases.append({
        "case_name": "B08_two_len2_fragmented",
        "boundary_family": "fragmented_vs_recovery_relapse",
        "expected_classification": "FRAGMENTED_LOCAL_COLLAPSE",
        "sequence": make_sequence(
            16,
            [
                (2, 2),
                (8, 2),
            ],
        ),
    })

    cases.append({
        "case_name": "B09_len2_then_len4_relapse",
        "boundary_family": "fragmented_vs_recovery_relapse",
        "expected_classification": "RECOVERY_RELAPSE_COLLAPSE",
        "sequence": make_sequence(
            18,
            [
                (2, 2),
                (8, 4),
            ],
        ),
    })

    # Boundary 6:
    # single global collapse vs relapse global collapse.
    cases.append({
        "case_name": "B10_single_global_run",
        "boundary_family": "global_vs_recovery_relapse",
        "expected_classification": "GLOBAL_PERSISTENT_COLLAPSE",
        "sequence": make_sequence(
            18,
            [
                (5, 7),
            ],
        ),
    })

    cases.append({
        "case_name": "B11_two_runs_second_global",
        "boundary_family": "global_vs_recovery_relapse",
        "expected_classification": "RECOVERY_RELAPSE_COLLAPSE",
        "sequence": make_sequence(
            18,
            [
                (2, 2),
                (8, 7),
            ],
        ),
    })

    # Boundary 7:
    # exact global threshold.
    cases.append({
        "case_name": "B12_global_threshold_minus_1",
        "boundary_family": "exact_global_threshold",
        "expected_classification": "FRAGMENTED_LOCAL_COLLAPSE",
        "sequence": make_sequence(
            16,
            [
                (5, GLOBAL_PERSISTENCE_THRESHOLD - 1),
            ],
        ),
    })

    cases.append({
        "case_name": "B13_global_threshold_exact",
        "boundary_family": "exact_global_threshold",
        "expected_classification": "GLOBAL_PERSISTENT_COLLAPSE",
        "sequence": make_sequence(
            16,
            [
                (5, GLOBAL_PERSISTENCE_THRESHOLD),
            ],
        ),
    })

    # Boundary 8:
    # dense oscillation vs dense local fragments.
    cases.append({
        "case_name": "B14_dense_len1_oscillation",
        "boundary_family": "dense_oscillation_vs_dense_fragmentation",
        "expected_classification": "OSCILLATING_NONPERSISTENT",
        "sequence": make_sequence(
            22,
            [
                (2, 1),
                (4, 1),
                (6, 1),
                (8, 1),
                (10, 1),
                (12, 1),
                (14, 1),
                (16, 1),
                (18, 1),
            ],
        ),
    })

    cases.append({
        "case_name": "B15_dense_len2_fragmentation",
        "boundary_family": "dense_oscillation_vs_dense_fragmentation",
        "expected_classification": "FRAGMENTED_LOCAL_COLLAPSE",
        "sequence": make_sequence(
            24,
            [
                (2, 2),
                (5, 2),
                (8, 2),
                (11, 2),
                (14, 2),
                (17, 2),
                (20, 2),
            ],
        ),
    })

    return cases


def evaluate_case(case):
    result = classify(case["sequence"])

    status = (
        "PASS"
        if result["classification"] == case["expected_classification"]
        else "CHECK"
    )

    return {
        "case_name": case["case_name"],
        "boundary_family": case["boundary_family"],
        "expected_classification": case["expected_classification"],
        "predicted_classification": result["classification"],
        "status": status,
        "sequence_length": len(case["sequence"]),
        "raw_action_sequence": case["sequence"],
        **result,
    }


def summarize_by_boundary_family(case_results):
    summary = {}

    for item in case_results:
        family = item["boundary_family"]

        if family not in summary:
            summary[family] = {
                "case_count": 0,
                "pass_count": 0,
                "check_count": 0,
                "pass_rate": 0.0,
            }

        summary[family]["case_count"] += 1

        if item["status"] == "PASS":
            summary[family]["pass_count"] += 1
        else:
            summary[family]["check_count"] += 1

    for values in summary.values():
        values["pass_rate"] = (
            values["pass_count"] / values["case_count"]
            if values["case_count"]
            else 0.0
        )

    return summary


def main():
    cases = generate_boundary_cases()

    case_results = [
        evaluate_case(case)
        for case in cases
    ]

    pass_case_count = sum(
        1
        for item in case_results
        if item["status"] == "PASS"
    )

    check_case_count = len(case_results) - pass_case_count

    family_summary = summarize_by_boundary_family(case_results)

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

    summary = {
        "case_count": len(case_results),
        "pass_case_count": pass_case_count,
        "check_case_count": check_case_count,
        "pass_rate": (
            pass_case_count / len(case_results)
            if case_results
            else 0.0
        ),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "supported_classes": SUPPORTED_CLASSES,
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
                for item in family_summary.values()
            )
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_threshold_boundary_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "boundary_family_summary": family_summary,
        "case_results": case_results,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_threshold_boundary_v0.py"
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
        "Temporal Collapse Topology Threshold Boundary v0"
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
    print("Boundary family summary")
    print("-" * 80)

    for family, values in family_summary.items():
        print(
            f"{family:<45} "
            f"cases={values['case_count']} "
            f"pass={values['pass_count']} "
            f"check={values['check_count']} "
            f"rate={values['pass_rate']}"
        )

    print()
    print("Boundary case summaries")
    print("-" * 80)

    for item in case_results:
        print(
            f"{item['case_name']:<35} "
            f"status={item['status']:<5} "
            f"expected={item['expected_classification']:<32} "
            f"predicted={item['predicted_classification']:<32} "
            f"runs={item['collapse_run_count']} "
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
            "PASS - topology threshold boundaries remained "
            "consistent across tested boundary cases."
        )
    else:
        print(
            "CHECK - topology threshold boundaries exposed "
            "classification instability."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()