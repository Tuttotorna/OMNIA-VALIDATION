import itertools
import json
from pathlib import Path
from statistics import mean

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_phase_transition_v0.json"
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

MUTATION_VALUES = [
    "PASS",
    "ESCALATE",
    "COLLAPSE",
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


def base_cases():
    return {
        "clean_pass": {
            "sequence": make_sequence(12, []),
        },
        "spike_filtered": {
            "sequence": make_sequence(12, [(5, 1)]),
        },
        "oscillating_nonpersistent": {
            "sequence": make_sequence(
                14,
                [
                    (3, 1),
                    (6, 1),
                    (9, 1),
                ],
            ),
        },
        "fragmented_local_collapse": {
            "sequence": make_sequence(
                18,
                [
                    (3, 2),
                    (7, 2),
                    (11, 2),
                ],
            ),
        },
        "global_persistent_collapse": {
            "sequence": make_sequence(
                18,
                [
                    (6, 8),
                ],
            ),
        },
        "recovery_relapse_collapse": {
            "sequence": make_sequence(
                20,
                [
                    (3, 2),
                    (10, 6),
                ],
            ),
        },
    }


def mutate_sequence(sequence, mutations):
    mutated = list(sequence)

    for index, new_value in mutations:
        if 0 <= index < len(mutated):
            mutated[index] = new_value

    return mutated


def candidate_single_mutations(sequence):
    mutations = []

    for index, old_value in enumerate(sequence):
        for new_value in MUTATION_VALUES:
            if new_value != old_value:
                mutations.append(
                    [(index, new_value)]
                )

    return mutations


def candidate_double_mutations(sequence):
    mutations = []

    indices = list(range(len(sequence)))

    for i, j in itertools.combinations(indices, 2):
        old_i = sequence[i]
        old_j = sequence[j]

        possible_i = [
            value
            for value in MUTATION_VALUES
            if value != old_i
        ]

        possible_j = [
            value
            for value in MUTATION_VALUES
            if value != old_j
        ]

        for value_i in possible_i:
            for value_j in possible_j:
                mutations.append(
                    [
                        (i, value_i),
                        (j, value_j),
                    ]
                )

    return mutations


def find_min_transition(sequence, max_mutation_depth=2):
    base_result = classify(sequence)
    base_class = base_result["classification"]

    search_layers = []

    if max_mutation_depth >= 1:
        search_layers.append(
            (1, candidate_single_mutations(sequence))
        )

    if max_mutation_depth >= 2:
        search_layers.append(
            (2, candidate_double_mutations(sequence))
        )

    checked_mutation_count = 0

    for depth, mutation_sets in search_layers:
        transition_examples = []

        for mutations in mutation_sets:
            checked_mutation_count += 1

            mutated = mutate_sequence(sequence, mutations)
            mutated_result = classify(mutated)
            mutated_class = mutated_result["classification"]

            if mutated_class != base_class:
                transition_examples.append({
                    "mutation_depth": depth,
                    "mutations": mutations,
                    "from_class": base_class,
                    "to_class": mutated_class,
                    "mutated_sequence": mutated,
                    "mutated_metrics": mutated_result,
                })

                if len(transition_examples) >= 5:
                    break

        if transition_examples:
            return {
                "base_classification": base_class,
                "base_metrics": base_result,
                "minimum_transition_depth": depth,
                "transition_found": True,
                "checked_mutation_count": checked_mutation_count,
                "transition_examples": transition_examples,
            }

    return {
        "base_classification": base_class,
        "base_metrics": base_result,
        "minimum_transition_depth": None,
        "transition_found": False,
        "checked_mutation_count": checked_mutation_count,
        "transition_examples": [],
    }


def evaluate():
    cases = base_cases()

    case_results = []

    for case_name, case_data in cases.items():
        transition_result = find_min_transition(
            case_data["sequence"],
            max_mutation_depth=2,
        )

        tsi = (
            transition_result["minimum_transition_depth"]
            if transition_result["transition_found"]
            else None
        )

        case_results.append({
            "case_name": case_name,
            "sequence_length": len(case_data["sequence"]),
            "raw_action_sequence": case_data["sequence"],
            "topology_stability_index": tsi,
            **transition_result,
        })

    transition_found_count = sum(
        1
        for item in case_results
        if item["transition_found"]
    )

    no_transition_found_count = (
        len(case_results) - transition_found_count
    )

    tsi_values = [
        item["topology_stability_index"]
        for item in case_results
        if item["topology_stability_index"] is not None
    ]

    class_to_tsi = {
        item["base_classification"]:
            item["topology_stability_index"]
        for item in case_results
    }

    summary = {
        "case_count": len(case_results),
        "transition_found_count": transition_found_count,
        "no_transition_found_count": no_transition_found_count,
        "transition_found_rate": (
            transition_found_count / len(case_results)
            if case_results
            else 0.0
        ),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "max_mutation_depth": 2,
        "supported_classes": SUPPORTED_CLASSES,
        "topology_stability_index_definition": (
            "minimum number of frame mutations required "
            "to induce a topology class transition"
        ),
        "mean_topology_stability_index": (
            mean(tsi_values)
            if tsi_values
            else None
        ),
        "min_topology_stability_index": (
            min(tsi_values)
            if tsi_values
            else None
        ),
        "max_topology_stability_index": (
            max(tsi_values)
            if tsi_values
            else None
        ),
        "class_to_topology_stability_index": class_to_tsi,
    }

    status = (
        "PASS"
        if transition_found_count == len(case_results)
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_phase_transition_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "case_results": case_results,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_phase_transition_v0.py"
        ),
    }

    return payload


def main():
    result = evaluate()

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULTS_PATH.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Topology Phase Transition v0"
    )
    print("=" * 80)
    print()

    print("Status:", result["status"])
    print("Version:", result["version"])

    print()
    print("Summary")
    print("-" * 80)

    for key, value in result["summary"].items():
        print(f"{key}: {value}")

    print()
    print("Case summaries")
    print("-" * 80)

    for item in result["case_results"]:
        examples = item["transition_examples"]

        if examples:
            first = examples[0]
            target = first["to_class"]
            mutations = first["mutations"]
        else:
            target = None
            mutations = []

        print(
            f"{item['case_name']:<35} "
            f"base={item['base_classification']:<32} "
            f"transition={item['transition_found']} "
            f"TSI={item['topology_stability_index']} "
            f"to={target} "
            f"mutations={mutations} "
            f"checked={item['checked_mutation_count']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if result["status"] == "PASS":
        print(
            "PASS - minimum topology phase-transition "
            "depth was found for all tested classes."
        )
    else:
        print(
            "CHECK - not all topology classes transitioned "
            "within the tested mutation depth."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()