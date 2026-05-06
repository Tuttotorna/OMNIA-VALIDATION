import itertools
import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_boundary_cycle_v0.json"
)

CONFIRMATION_WINDOW = 2
PERSISTENCE_WINDOW = 2
GLOBAL_PERSISTENCE_THRESHOLD = (
    CONFIRMATION_WINDOW + PERSISTENCE_WINDOW
)

MAX_MUTATION_DEPTH = 4

SUPPORTED_CLASSES = [
    "GLOBAL_PERSISTENT_COLLAPSE",
    "RECOVERY_RELAPSE_COLLAPSE",
    "FRAGMENTED_LOCAL_COLLAPSE",
    "OSCILLATING_NONPERSISTENT",
    "SPIKE_FILTERED",
    "CLEAN_PASS",
]

BOUNDARY_A = "OSCILLATING_NONPERSISTENT"
BOUNDARY_B = "FRAGMENTED_LOCAL_COLLAPSE"

NOISE_COMPONENT = [
    "CLEAN_PASS",
    "SPIKE_FILTERED",
    "OSCILLATING_NONPERSISTENT",
]

COLLAPSE_COMPONENT = [
    "FRAGMENTED_LOCAL_COLLAPSE",
    "GLOBAL_PERSISTENT_COLLAPSE",
    "RECOVERY_RELAPSE_COLLAPSE",
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


def base_case_variants():
    variants = {}

    variants["oscillating_nonpersistent"] = [
        make_sequence(14, [(3, 1), (6, 1), (9, 1)]),
        make_sequence(18, [(4, 1), (8, 1), (12, 1)]),
        make_sequence(22, [(5, 1), (10, 1), (15, 1)]),
        make_sequence(26, [(6, 1), (12, 1), (18, 1)]),
        make_sequence(30, [(7, 1), (14, 1), (21, 1)]),
    ]

    variants["fragmented_local_collapse"] = [
        make_sequence(18, [(3, 2), (7, 2), (11, 2)]),
        make_sequence(22, [(4, 2), (9, 2), (14, 2)]),
        make_sequence(26, [(5, 2), (11, 2), (17, 2)]),
        make_sequence(30, [(6, 2), (13, 2), (20, 2)]),
        make_sequence(34, [(7, 2), (15, 2), (23, 2)]),
    ]

    return variants


def mutate_sequence(sequence, mutations):
    mutated = list(sequence)

    for index, new_value in mutations:
        if 0 <= index < len(mutated):
            mutated[index] = new_value

    return mutated


def candidate_mutations(sequence, depth):
    indices = list(range(len(sequence)))

    if depth < 1:
        raise ValueError("Mutation depth must be >= 1.")

    if depth > MAX_MUTATION_DEPTH:
        raise ValueError("Mutation depth exceeds MAX_MUTATION_DEPTH.")

    for selected_indices in itertools.combinations(indices, depth):
        replacement_options = []

        for index in selected_indices:
            old_value = sequence[index]

            replacement_options.append([
                value
                for value in MUTATION_VALUES
                if value != old_value
            ])

        for replacement_values in itertools.product(*replacement_options):
            yield [
                (index, new_value)
                for index, new_value in zip(
                    selected_indices,
                    replacement_values,
                )
            ]


def find_transition_profile(sequence, target_class):
    source_metrics = classify(sequence)
    source_class = source_metrics["classification"]

    checked_by_depth = {
        str(depth): 0
        for depth in range(1, MAX_MUTATION_DEPTH + 1)
    }

    target_example_count_by_depth = {
        str(depth): 0
        for depth in range(1, MAX_MUTATION_DEPTH + 1)
    }

    example_by_depth = {}

    for depth in range(1, MAX_MUTATION_DEPTH + 1):
        for mutations in candidate_mutations(sequence, depth):
            checked_by_depth[str(depth)] += 1

            mutated = mutate_sequence(sequence, mutations)
            target_metrics = classify(mutated)

            if target_metrics["classification"] != target_class:
                continue

            depth_key = str(depth)
            target_example_count_by_depth[depth_key] += 1

            if depth_key not in example_by_depth:
                example_by_depth[depth_key] = {
                    "mutations": mutations,
                    "sequence": mutated,
                    "metrics": target_metrics,
                }

    hit_depths = [
        int(depth)
        for depth, count in target_example_count_by_depth.items()
        if count > 0
    ]

    minimum_transition_depth = (
        min(hit_depths)
        if hit_depths
        else None
    )

    total_examples = sum(target_example_count_by_depth.values())

    return {
        "source_class": source_class,
        "target_class": target_class,
        "source_metrics": source_metrics,
        "checked_by_depth": checked_by_depth,
        "target_example_count_by_depth": target_example_count_by_depth,
        "minimum_transition_depth": minimum_transition_depth,
        "total_examples": total_examples,
        "example_by_depth": example_by_depth,
    }


def build_variant_cycle(variant_index, variants_by_case):
    oscillating_sequence = variants_by_case[
        "oscillating_nonpersistent"
    ][variant_index]

    fragmented_sequence = variants_by_case[
        "fragmented_local_collapse"
    ][variant_index]

    forward_profile = find_transition_profile(
        oscillating_sequence,
        BOUNDARY_B,
    )

    reverse_profile = find_transition_profile(
        fragmented_sequence,
        BOUNDARY_A,
    )

    forward_depth = forward_profile["minimum_transition_depth"]
    reverse_depth = reverse_profile["minimum_transition_depth"]

    forward_examples = forward_profile["total_examples"]
    reverse_examples = reverse_profile["total_examples"]

    if forward_depth is not None and reverse_depth is not None:
        cycle_detected = True
        cycle_depth_sum = forward_depth + reverse_depth
        cycle_depth_asymmetry = abs(forward_depth - reverse_depth)
        cycle_density_ratio = (
            forward_examples / max(reverse_examples, 1)
        )
        boundary_cycle_index = (
            (1 / cycle_depth_sum)
            * min(forward_examples, reverse_examples)
            / max(forward_examples, reverse_examples, 1)
        )
    else:
        cycle_detected = False
        cycle_depth_sum = None
        cycle_depth_asymmetry = None
        cycle_density_ratio = None
        boundary_cycle_index = 0.0

    return {
        "variant_index": variant_index,
        "forward": {
            "from_class": BOUNDARY_A,
            "to_class": BOUNDARY_B,
            "sequence_length": len(oscillating_sequence),
            "raw_action_sequence": oscillating_sequence,
            "profile": forward_profile,
        },
        "reverse": {
            "from_class": BOUNDARY_B,
            "to_class": BOUNDARY_A,
            "sequence_length": len(fragmented_sequence),
            "raw_action_sequence": fragmented_sequence,
            "profile": reverse_profile,
        },
        "cycle_detected": cycle_detected,
        "cycle_depth_sum": cycle_depth_sum,
        "cycle_depth_asymmetry": cycle_depth_asymmetry,
        "cycle_density_ratio": cycle_density_ratio,
        "boundary_cycle_index": boundary_cycle_index,
    }


def summarize_cycles(variant_results):
    cycle_detected_values = [
        item["cycle_detected"]
        for item in variant_results
    ]

    forward_depths = [
        item["forward"]["profile"]["minimum_transition_depth"]
        for item in variant_results
        if item["forward"]["profile"]["minimum_transition_depth"]
        is not None
    ]

    reverse_depths = [
        item["reverse"]["profile"]["minimum_transition_depth"]
        for item in variant_results
        if item["reverse"]["profile"]["minimum_transition_depth"]
        is not None
    ]

    cycle_depth_sums = [
        item["cycle_depth_sum"]
        for item in variant_results
        if item["cycle_depth_sum"] is not None
    ]

    cycle_asymmetries = [
        item["cycle_depth_asymmetry"]
        for item in variant_results
        if item["cycle_depth_asymmetry"] is not None
    ]

    forward_examples = [
        item["forward"]["profile"]["total_examples"]
        for item in variant_results
    ]

    reverse_examples = [
        item["reverse"]["profile"]["total_examples"]
        for item in variant_results
    ]

    cycle_indices = [
        item["boundary_cycle_index"]
        for item in variant_results
    ]

    forward_depth_stable = (
        len(set(forward_depths)) == 1
        if forward_depths
        else False
    )

    reverse_depth_stable = (
        len(set(reverse_depths)) == 1
        if reverse_depths
        else False
    )

    all_cycles_detected = all(cycle_detected_values)

    expected_cycle_detected = (
        all_cycles_detected
        and forward_depth_stable
        and reverse_depth_stable
        and forward_depths
        and reverse_depths
        and forward_depths[0] == 1
        and reverse_depths[0] == 3
    )

    return {
        "all_cycles_detected": all_cycles_detected,
        "cycle_detected_values": cycle_detected_values,
        "forward_depths": forward_depths,
        "reverse_depths": reverse_depths,
        "forward_depth_stable": forward_depth_stable,
        "reverse_depth_stable": reverse_depth_stable,
        "cycle_depth_sums": cycle_depth_sums,
        "cycle_depth_sum_mean": (
            mean(cycle_depth_sums)
            if cycle_depth_sums
            else None
        ),
        "cycle_depth_sum_std": (
            pstdev(cycle_depth_sums)
            if len(cycle_depth_sums) > 1
            else 0.0
        ),
        "cycle_asymmetries": cycle_asymmetries,
        "cycle_asymmetry_mean": (
            mean(cycle_asymmetries)
            if cycle_asymmetries
            else None
        ),
        "cycle_asymmetry_std": (
            pstdev(cycle_asymmetries)
            if len(cycle_asymmetries) > 1
            else 0.0
        ),
        "forward_examples": forward_examples,
        "reverse_examples": reverse_examples,
        "forward_example_total": sum(forward_examples),
        "reverse_example_total": sum(reverse_examples),
        "forward_example_mean": mean(forward_examples),
        "reverse_example_mean": mean(reverse_examples),
        "cycle_indices": cycle_indices,
        "boundary_cycle_index_mean": mean(cycle_indices),
        "boundary_cycle_index_std": (
            pstdev(cycle_indices)
            if len(cycle_indices) > 1
            else 0.0
        ),
        "expected_cycle_detected": expected_cycle_detected,
    }


def main():
    variants_by_case = base_case_variants()

    variant_count = min(
        len(items)
        for items in variants_by_case.values()
    )

    variant_results = []

    for variant_index in range(variant_count):
        variant_results.append(
            build_variant_cycle(
                variant_index,
                variants_by_case,
            )
        )

    cycle_summary = summarize_cycles(variant_results)

    summary = {
        "variant_count": variant_count,
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "max_mutation_depth": MAX_MUTATION_DEPTH,
        "boundary_cycle": (
            f"{BOUNDARY_A}<->{BOUNDARY_B}"
        ),
        "forward_transition": (
            f"{BOUNDARY_A}->{BOUNDARY_B}"
        ),
        "reverse_transition": (
            f"{BOUNDARY_B}->{BOUNDARY_A}"
        ),
        "all_cycles_detected": (
            cycle_summary["all_cycles_detected"]
        ),
        "expected_cycle_detected": (
            cycle_summary["expected_cycle_detected"]
        ),
        "forward_depths": cycle_summary["forward_depths"],
        "reverse_depths": cycle_summary["reverse_depths"],
        "forward_depth_stable": (
            cycle_summary["forward_depth_stable"]
        ),
        "reverse_depth_stable": (
            cycle_summary["reverse_depth_stable"]
        ),
        "cycle_depth_sums": cycle_summary["cycle_depth_sums"],
        "cycle_depth_sum_mean": (
            cycle_summary["cycle_depth_sum_mean"]
        ),
        "cycle_depth_asymmetries": (
            cycle_summary["cycle_asymmetries"]
        ),
        "cycle_asymmetry_mean": (
            cycle_summary["cycle_asymmetry_mean"]
        ),
        "forward_example_total": (
            cycle_summary["forward_example_total"]
        ),
        "reverse_example_total": (
            cycle_summary["reverse_example_total"]
        ),
        "forward_example_mean": (
            cycle_summary["forward_example_mean"]
        ),
        "reverse_example_mean": (
            cycle_summary["reverse_example_mean"]
        ),
        "boundary_cycle_index_mean": (
            cycle_summary["boundary_cycle_index_mean"]
        ),
        "boundary_cycle_index_std": (
            cycle_summary["boundary_cycle_index_std"]
        ),
    }

    status = (
        "PASS"
        if (
            summary["all_cycles_detected"]
            and summary["forward_depth_stable"]
            and summary["reverse_depth_stable"]
            and summary["expected_cycle_detected"]
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_boundary_cycle_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "cycle_summary": cycle_summary,
        "variant_results": variant_results,
        "interpretation": (
            "This experiment measures whether the basin boundary "
            "forms a stable reversible cycle between "
            "OSCILLATING_NONPERSISTENT and FRAGMENTED_LOCAL_COLLAPSE."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_boundary_cycle_v0.py"
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
        "Temporal Collapse Topology Boundary Cycle v0"
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
    print("Variant cycle summaries")
    print("-" * 80)

    for item in variant_results:
        forward_profile = item["forward"]["profile"]
        reverse_profile = item["reverse"]["profile"]

        print(
            f"variant={item['variant_index']} "
            f"cycle={item['cycle_detected']} "
            f"forward_depth={forward_profile['minimum_transition_depth']} "
            f"reverse_depth={reverse_profile['minimum_transition_depth']} "
            f"forward_examples={forward_profile['total_examples']} "
            f"reverse_examples={reverse_profile['total_examples']} "
            f"depth_sum={item['cycle_depth_sum']} "
            f"asymmetry={item['cycle_depth_asymmetry']} "
            f"cycle_index={item['boundary_cycle_index']}"
        )

    print()
    print("Depth distributions")
    print("-" * 80)

    for item in variant_results:
        forward_profile = item["forward"]["profile"]
        reverse_profile = item["reverse"]["profile"]

        print(
            f"variant={item['variant_index']} "
            f"forward_counts="
            f"{forward_profile['target_example_count_by_depth']} "
            f"reverse_counts="
            f"{reverse_profile['target_example_count_by_depth']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - basin-boundary cycle detected: "
            "OSCILLATING_NONPERSISTENT and FRAGMENTED_LOCAL_COLLAPSE "
            "form a stable reversible boundary cycle."
        )
    else:
        print(
            "CHECK - basin-boundary cycle was not fully stable "
            "under tested variants."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()