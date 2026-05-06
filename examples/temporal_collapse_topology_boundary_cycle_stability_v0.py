import itertools
import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_boundary_cycle_stability_v0.json"
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


def base_geometry_variants():
    variants = []

    specs = [
        {
            "name": "compact_low_spacing",
            "oscillating": {
                "length": 14,
                "runs": [(3, 1), (6, 1), (9, 1)],
            },
            "fragmented": {
                "length": 18,
                "runs": [(3, 2), (7, 2), (11, 2)],
            },
        },
        {
            "name": "medium_shifted_spacing",
            "oscillating": {
                "length": 18,
                "runs": [(4, 1), (8, 1), (12, 1)],
            },
            "fragmented": {
                "length": 22,
                "runs": [(4, 2), (9, 2), (14, 2)],
            },
        },
        {
            "name": "wide_spacing",
            "oscillating": {
                "length": 22,
                "runs": [(5, 1), (10, 1), (15, 1)],
            },
            "fragmented": {
                "length": 26,
                "runs": [(5, 2), (11, 2), (17, 2)],
            },
        },
        {
            "name": "long_sparse_spacing",
            "oscillating": {
                "length": 30,
                "runs": [(6, 1), (14, 1), (22, 1)],
            },
            "fragmented": {
                "length": 34,
                "runs": [(6, 2), (15, 2), (24, 2)],
            },
        },
        {
            "name": "front_loaded_geometry",
            "oscillating": {
                "length": 24,
                "runs": [(2, 1), (5, 1), (9, 1)],
            },
            "fragmented": {
                "length": 28,
                "runs": [(2, 2), (6, 2), (10, 2)],
            },
        },
        {
            "name": "back_loaded_geometry",
            "oscillating": {
                "length": 28,
                "runs": [(15, 1), (19, 1), (23, 1)],
            },
            "fragmented": {
                "length": 32,
                "runs": [(16, 2), (21, 2), (26, 2)],
            },
        },
        {
            "name": "four_spike_oscillation",
            "oscillating": {
                "length": 26,
                "runs": [(4, 1), (8, 1), (12, 1), (16, 1)],
            },
            "fragmented": {
                "length": 30,
                "runs": [(4, 2), (9, 2), (14, 2), (19, 2)],
            },
        },
        {
            "name": "dense_fragmented_geometry",
            "oscillating": {
                "length": 24,
                "runs": [(4, 1), (7, 1), (10, 1), (13, 1)],
            },
            "fragmented": {
                "length": 28,
                "runs": [(4, 2), (8, 2), (12, 2), (16, 2)],
            },
        },
    ]

    for spec in specs:
        oscillating_sequence = make_sequence(
            spec["oscillating"]["length"],
            spec["oscillating"]["runs"],
        )

        fragmented_sequence = make_sequence(
            spec["fragmented"]["length"],
            spec["fragmented"]["runs"],
        )

        oscillating_class = classify(oscillating_sequence)["classification"]
        fragmented_class = classify(fragmented_sequence)["classification"]

        if oscillating_class != BOUNDARY_A:
            raise ValueError(
                f"{spec['name']} oscillating source classified as "
                f"{oscillating_class}, expected {BOUNDARY_A}."
            )

        if fragmented_class != BOUNDARY_B:
            raise ValueError(
                f"{spec['name']} fragmented source classified as "
                f"{fragmented_class}, expected {BOUNDARY_B}."
            )

        variants.append({
            "name": spec["name"],
            "oscillating_sequence": oscillating_sequence,
            "fragmented_sequence": fragmented_sequence,
            "oscillating_runs": spec["oscillating"]["runs"],
            "fragmented_runs": spec["fragmented"]["runs"],
        })

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


def build_geometry_cycle(variant_index, variant):
    forward_profile = find_transition_profile(
        variant["oscillating_sequence"],
        BOUNDARY_B,
    )

    reverse_profile = find_transition_profile(
        variant["fragmented_sequence"],
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
        "geometry_name": variant["name"],
        "oscillating_runs": variant["oscillating_runs"],
        "fragmented_runs": variant["fragmented_runs"],
        "oscillating_sequence_length": len(
            variant["oscillating_sequence"]
        ),
        "fragmented_sequence_length": len(
            variant["fragmented_sequence"]
        ),
        "forward": {
            "from_class": BOUNDARY_A,
            "to_class": BOUNDARY_B,
            "raw_action_sequence": variant["oscillating_sequence"],
            "profile": forward_profile,
        },
        "reverse": {
            "from_class": BOUNDARY_B,
            "to_class": BOUNDARY_A,
            "raw_action_sequence": variant["fragmented_sequence"],
            "profile": reverse_profile,
        },
        "cycle_detected": cycle_detected,
        "cycle_depth_sum": cycle_depth_sum,
        "cycle_depth_asymmetry": cycle_depth_asymmetry,
        "cycle_density_ratio": cycle_density_ratio,
        "boundary_cycle_index": boundary_cycle_index,
    }


def summarize_cycle_stability(variant_results):
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

    density_ratios = [
        item["cycle_density_ratio"]
        for item in variant_results
        if item["cycle_density_ratio"] is not None
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

    asymmetry_stable = (
        len(set(cycle_asymmetries)) == 1
        if cycle_asymmetries
        else False
    )

    depth_sum_stable = (
        len(set(cycle_depth_sums)) == 1
        if cycle_depth_sums
        else False
    )

    all_cycles_detected = all(cycle_detected_values)

    expected_cycle_stable = (
        all_cycles_detected
        and forward_depth_stable
        and reverse_depth_stable
        and asymmetry_stable
        and depth_sum_stable
        and forward_depths
        and reverse_depths
        and forward_depths[0] == 1
        and reverse_depths[0] == 3
        and cycle_asymmetries[0] == 2
        and cycle_depth_sums[0] == 4
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
        "cycle_asymmetry_stable": asymmetry_stable,
        "cycle_depth_sum_stable": depth_sum_stable,
        "forward_examples": forward_examples,
        "reverse_examples": reverse_examples,
        "forward_example_total": sum(forward_examples),
        "reverse_example_total": sum(reverse_examples),
        "forward_example_mean": mean(forward_examples),
        "reverse_example_mean": mean(reverse_examples),
        "forward_example_std": (
            pstdev(forward_examples)
            if len(forward_examples) > 1
            else 0.0
        ),
        "reverse_example_std": (
            pstdev(reverse_examples)
            if len(reverse_examples) > 1
            else 0.0
        ),
        "cycle_density_ratios": density_ratios,
        "cycle_density_ratio_mean": (
            mean(density_ratios)
            if density_ratios
            else None
        ),
        "cycle_density_ratio_std": (
            pstdev(density_ratios)
            if len(density_ratios) > 1
            else 0.0
        ),
        "cycle_indices": cycle_indices,
        "boundary_cycle_index_mean": mean(cycle_indices),
        "boundary_cycle_index_std": (
            pstdev(cycle_indices)
            if len(cycle_indices) > 1
            else 0.0
        ),
        "expected_cycle_stable": expected_cycle_stable,
    }


def main():
    variants = base_geometry_variants()

    variant_results = []

    for variant_index, variant in enumerate(variants):
        variant_results.append(
            build_geometry_cycle(
                variant_index,
                variant,
            )
        )

    cycle_summary = summarize_cycle_stability(variant_results)

    summary = {
        "variant_count": len(variant_results),
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
        "expected_cycle_stable": (
            cycle_summary["expected_cycle_stable"]
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
        "cycle_depth_sum_stable": (
            cycle_summary["cycle_depth_sum_stable"]
        ),
        "cycle_depth_asymmetries": (
            cycle_summary["cycle_asymmetries"]
        ),
        "cycle_asymmetry_mean": (
            cycle_summary["cycle_asymmetry_mean"]
        ),
        "cycle_asymmetry_stable": (
            cycle_summary["cycle_asymmetry_stable"]
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
        "cycle_density_ratio_mean": (
            cycle_summary["cycle_density_ratio_mean"]
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
            and summary["expected_cycle_stable"]
            and summary["forward_depth_stable"]
            and summary["reverse_depth_stable"]
            and summary["cycle_asymmetry_stable"]
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_boundary_cycle_stability_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "cycle_summary": cycle_summary,
        "variant_results": variant_results,
        "interpretation": (
            "This experiment stress-tests whether the asymmetric "
            "basin-boundary cycle remains stable under altered "
            "trajectory geometry."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_boundary_cycle_stability_v0.py"
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
        "Temporal Collapse Topology Boundary Cycle Stability v0"
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
            f"geometry={item['geometry_name']} "
            f"cycle={item['cycle_detected']} "
            f"forward_depth={forward_profile['minimum_transition_depth']} "
            f"reverse_depth={reverse_profile['minimum_transition_depth']} "
            f"forward_examples={forward_profile['total_examples']} "
            f"reverse_examples={reverse_profile['total_examples']} "
            f"depth_sum={item['cycle_depth_sum']} "
            f"asymmetry={item['cycle_depth_asymmetry']} "
            f"density_ratio={item['cycle_density_ratio']} "
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
            f"geometry={item['geometry_name']} "
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
            "PASS - boundary-cycle stability detected: "
            "OSCILLATING_NONPERSISTENT and FRAGMENTED_LOCAL_COLLAPSE "
            "kept a stable asymmetric reversible cycle under "
            "altered trajectory geometry."
        )
    else:
        print(
            "CHECK - boundary-cycle stability was not fully confirmed "
            "under altered trajectory geometry."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()