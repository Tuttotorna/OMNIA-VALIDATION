import json
from pathlib import Path
from statistics import mean

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_stability_v0.json"
)

CONFIRMATION_WINDOW = 2
PERSISTENCE_WINDOW = 2
RESET_WINDOW = 2

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


def pad_to_length(sequence, length):
    if len(sequence) >= length:
        return sequence[:length]

    return sequence + ["PASS"] * (length - len(sequence))


def make_clean_pass(length):
    return ["PASS"] * length


def make_spike_filtered(length, spike_index):
    sequence = ["PASS"] * length

    if 0 <= spike_index < length:
        sequence[spike_index] = "COLLAPSE"

    return sequence


def make_global_persistent(length, start, collapse_length):
    sequence = ["PASS"] * length

    end = min(length, start + collapse_length)

    for i in range(start, end):
        sequence[i] = "COLLAPSE"

    if start > 0:
        sequence[max(0, start - 1)] = "ESCALATE"

    return sequence


def make_recovery_relapse(
    length,
    first_start,
    first_length,
    gap_length,
    second_length,
):
    sequence = ["PASS"] * length

    first_end = min(length, first_start + first_length)

    for i in range(first_start, first_end):
        sequence[i] = "COLLAPSE"

    second_start = first_end + gap_length
    second_end = min(length, second_start + second_length)

    if first_start > 0:
        sequence[first_start - 1] = "ESCALATE"

    if second_start > 0 and second_start < length:
        sequence[second_start - 1] = "ESCALATE"

    for i in range(second_start, second_end):
        sequence[i] = "COLLAPSE"

    return sequence


def make_fragmented_local(
    length,
    first_start,
    run_length,
    gap_length,
    repeat_count,
):
    sequence = ["PASS"] * length

    cursor = first_start

    for _ in range(repeat_count):
        if cursor >= length:
            break

        end = min(length, cursor + run_length)

        for i in range(cursor, end):
            sequence[i] = "COLLAPSE"

        if cursor > 0:
            sequence[cursor - 1] = "ESCALATE"

        cursor = end + gap_length

    return sequence


def make_oscillating_nonpersistent(
    length,
    first_start,
    gap_length,
):
    sequence = ["PASS"] * length

    cursor = first_start

    while cursor < length:
        sequence[cursor] = "COLLAPSE"

        if cursor > 0:
            sequence[cursor - 1] = "ESCALATE"

        cursor += gap_length + 1

    return sequence


def generate_cases():
    cases = []

    for length in [12, 16, 20]:
        cases.append({
            "case_name": f"clean_pass_L{length}",
            "expected_classification": "CLEAN_PASS",
            "family": "clean_pass",
            "sequence": make_clean_pass(length),
        })

    for length in [12, 16, 20]:
        for spike_index in [1, length // 2, length - 2]:
            cases.append({
                "case_name": (
                    f"spike_filtered_L{length}_i{spike_index}"
                ),
                "expected_classification": "SPIKE_FILTERED",
                "family": "spike_filtered",
                "sequence": make_spike_filtered(
                    length,
                    spike_index,
                ),
            })

    for length in [12, 16, 20]:
        for start in [2, 4, 6]:
            collapse_length = max(
                CONFIRMATION_WINDOW + PERSISTENCE_WINDOW,
                length - start,
            )

            cases.append({
                "case_name": (
                    f"global_persistent_L{length}_s{start}"
                ),
                "expected_classification": (
                    "GLOBAL_PERSISTENT_COLLAPSE"
                ),
                "family": "global_persistent_collapse",
                "sequence": make_global_persistent(
                    length,
                    start,
                    collapse_length,
                ),
            })

    for length in [16, 20]:
        for gap_length in [2, 3, 4]:
            cases.append({
                "case_name": (
                    f"recovery_relapse_L{length}_gap{gap_length}"
                ),
                "expected_classification": (
                    "RECOVERY_RELAPSE_COLLAPSE"
                ),
                "family": "recovery_relapse_collapse",
                "sequence": make_recovery_relapse(
                    length=length,
                    first_start=2,
                    first_length=2,
                    gap_length=gap_length,
                    second_length=length,
                ),
            })

    for length in [16, 20]:
        for gap_length in [1, 2, 3]:
            cases.append({
                "case_name": (
                    f"fragmented_local_L{length}_gap{gap_length}"
                ),
                "expected_classification": (
                    "FRAGMENTED_LOCAL_COLLAPSE"
                ),
                "family": "fragmented_local_collapse",
                "sequence": make_fragmented_local(
                    length=length,
                    first_start=2,
                    run_length=CONFIRMATION_WINDOW,
                    gap_length=gap_length,
                    repeat_count=8,
                ),
            })

    for length in [16, 20]:
        for gap_length in [1, 2, 3]:
            cases.append({
                "case_name": (
                    f"oscillating_nonpersistent_L{length}_gap{gap_length}"
                ),
                "expected_classification": (
                    "OSCILLATING_NONPERSISTENT"
                ),
                "family": "oscillating_nonpersistent",
                "sequence": make_oscillating_nonpersistent(
                    length=length,
                    first_start=2,
                    gap_length=gap_length,
                ),
            })

    return cases


def evaluate_case(case):
    classification = classify(case["sequence"])

    passed = (
        classification["classification"]
        == case["expected_classification"]
    )

    return {
        "case_name": case["case_name"],
        "family": case["family"],
        "expected_classification": (
            case["expected_classification"]
        ),
        "predicted_classification": (
            classification["classification"]
        ),
        "status": "PASS" if passed else "CHECK",
        "sequence_length": len(case["sequence"]),
        "raw_action_sequence": case["sequence"],
        **classification,
    }


def summarize_by_family(case_results):
    families = {}

    for item in case_results:
        family = item["family"]

        if family not in families:
            families[family] = {
                "case_count": 0,
                "pass_count": 0,
                "check_count": 0,
                "pass_rate": 0.0,
                "expected_classification": (
                    item["expected_classification"]
                ),
            }

        families[family]["case_count"] += 1

        if item["status"] == "PASS":
            families[family]["pass_count"] += 1
        else:
            families[family]["check_count"] += 1

    for family in families.values():
        family["pass_rate"] = (
            family["pass_count"] / family["case_count"]
            if family["case_count"]
            else 0.0
        )

    return families


def main():
    cases = generate_cases()

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

    family_summary = summarize_by_family(case_results)

    fragmentation_values = [
        item["fragmentation_index"]
        for item in case_results
    ]

    max_runs_values = [
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
        "reset_window": RESET_WINDOW,
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
            mean(max_runs_values)
            if max_runs_values
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
                family["pass_rate"] == 1.0
                for family in family_summary.values()
            )
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_stability_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "family_summary": family_summary,
        "case_results": case_results,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_stability_v0.py"
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
        "Temporal Collapse Topology Stability v0"
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
    print("Family summary")
    print("-" * 80)

    for family, values in family_summary.items():
        print(
            f"{family:<35} "
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
            "PASS - temporal collapse topology classification "
            "remained stable under trajectory perturbations."
        )
    else:
        print(
            "CHECK - temporal collapse topology classification "
            "was unstable under trajectory perturbations."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()