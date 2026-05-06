import itertools
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_escape_depth_stability_v0.json"
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

EXPECTED_ESCAPE_DEPTHS = {
    "FRAGMENTED_LOCAL_COLLAPSE": 3,
    "GLOBAL_PERSISTENT_COLLAPSE": 4,
    "RECOVERY_RELAPSE_COLLAPSE": 4,
}

EXPECTED_ESCAPE_TARGET = "OSCILLATING_NONPERSISTENT"

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

    variants["fragmented_local_collapse"] = [
        make_sequence(18, [(3, 2), (7, 2), (11, 2)]),
        make_sequence(22, [(4, 2), (9, 2), (14, 2)]),
        make_sequence(26, [(5, 2), (11, 2), (17, 2)]),
        make_sequence(30, [(6, 2), (13, 2), (20, 2)]),
        make_sequence(34, [(7, 2), (15, 2), (23, 2)]),
    ]

    variants["global_persistent_collapse"] = [
        make_sequence(18, [(6, 8)]),
        make_sequence(22, [(8, 8)]),
        make_sequence(26, [(10, 8)]),
        make_sequence(30, [(12, 8)]),
        make_sequence(34, [(14, 8)]),
    ]

    variants["recovery_relapse_collapse"] = [
        make_sequence(20, [(3, 2), (10, 6)]),
        make_sequence(24, [(4, 2), (12, 6)]),
        make_sequence(28, [(5, 2), (14, 6)]),
        make_sequence(32, [(6, 2), (16, 6)]),
        make_sequence(36, [(7, 2), (18, 6)]),
    ]

    return variants


def component_for_class(class_name):
    if class_name in NOISE_COMPONENT:
        return "NOISE_COMPONENT"

    if class_name in COLLAPSE_COMPONENT:
        return "COLLAPSE_COMPONENT"

    return "UNKNOWN_COMPONENT"


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


def find_escape_profile(sequence, max_depth=MAX_MUTATION_DEPTH):
    source_metrics = classify(sequence)
    source_class = source_metrics["classification"]
    source_component = component_for_class(source_class)

    checked_by_depth = {
        str(depth): 0
        for depth in range(1, max_depth + 1)
    }

    escapes_by_depth = {
        str(depth): []
        for depth in range(1, max_depth + 1)
    }

    if source_component != "COLLAPSE_COMPONENT":
        return {
            "source_class": source_class,
            "source_component": source_component,
            "source_metrics": source_metrics,
            "checked_by_depth": checked_by_depth,
            "escapes_by_depth": escapes_by_depth,
            "minimum_escape_depth": None,
            "escape_targets": [],
            "escape_example_count": 0,
            "escape_example_count_by_depth": {
                str(depth): 0
                for depth in range(1, max_depth + 1)
            },
        }

    escape_map = {}

    for depth in range(1, max_depth + 1):
        for mutations in candidate_mutations(sequence, depth):
            checked_by_depth[str(depth)] += 1

            mutated = mutate_sequence(sequence, mutations)
            target_metrics = classify(mutated)
            target_class = target_metrics["classification"]
            target_component = component_for_class(target_class)

            if target_component != "NOISE_COMPONENT":
                continue

            key = (
                source_class,
                target_class,
                depth,
            )

            if key not in escape_map:
                escape_map[key] = {
                    "from_class": source_class,
                    "to_class": target_class,
                    "escape_depth": depth,
                    "example_mutations": mutations,
                    "example_sequence": mutated,
                    "example_metrics": target_metrics,
                    "example_count": 1,
                }
            else:
                escape_map[key]["example_count"] += 1

    for escape in escape_map.values():
        escapes_by_depth[str(escape["escape_depth"])].append(escape)

    all_escapes = list(escape_map.values())

    escape_depths = [
        escape["escape_depth"]
        for escape in all_escapes
    ]

    minimum_escape_depth = (
        min(escape_depths)
        if escape_depths
        else None
    )

    escape_targets = sorted({
        escape["to_class"]
        for escape in all_escapes
    })

    escape_example_count_by_depth = {}

    for depth in range(1, max_depth + 1):
        depth_key = str(depth)

        escape_example_count_by_depth[depth_key] = sum(
            escape["example_count"]
            for escape in escapes_by_depth[depth_key]
        )

    escape_example_count = sum(
        escape_example_count_by_depth.values()
    )

    return {
        "source_class": source_class,
        "source_component": source_component,
        "source_metrics": source_metrics,
        "checked_by_depth": checked_by_depth,
        "escapes_by_depth": escapes_by_depth,
        "minimum_escape_depth": minimum_escape_depth,
        "escape_targets": escape_targets,
        "escape_example_count": escape_example_count,
        "escape_example_count_by_depth": escape_example_count_by_depth,
    }


def build_variant_profiles(variant_index, variants_by_case):
    source_profiles = []

    for case_name, sequences in variants_by_case.items():
        sequence = sequences[variant_index]

        profile = find_escape_profile(
            sequence,
            max_depth=MAX_MUTATION_DEPTH,
        )

        record = {
            "case_name": case_name,
            "variant_index": variant_index,
            "sequence_length": len(sequence),
            "raw_action_sequence": sequence,
            "source_class": profile["source_class"],
            "source_component": profile["source_component"],
            "source_metrics": profile["source_metrics"],
            "checked_by_depth": profile["checked_by_depth"],
            "minimum_escape_depth": profile["minimum_escape_depth"],
            "escape_targets": profile["escape_targets"],
            "escape_example_count": profile["escape_example_count"],
            "escape_example_count_by_depth": (
                profile["escape_example_count_by_depth"]
            ),
        }

        source_profiles.append(record)

    return {
        "variant_index": variant_index,
        "source_profiles": source_profiles,
    }


def summarize_escape_depth_stability(variant_results):
    class_summary = {}

    for class_name in COLLAPSE_COMPONENT:
        records = []

        for variant in variant_results:
            for record in variant["source_profiles"]:
                if record["source_class"] == class_name:
                    records.append(record)

        minimum_escape_depths = [
            record["minimum_escape_depth"]
            for record in records
            if record["minimum_escape_depth"] is not None
        ]

        escape_targets_by_variant = [
            record["escape_targets"]
            for record in records
        ]

        unique_escape_targets = sorted({
            target
            for targets in escape_targets_by_variant
            for target in targets
        })

        escape_example_counts = [
            record["escape_example_count"]
            for record in records
        ]

        depth_example_totals = {
            str(depth): sum(
                record["escape_example_count_by_depth"][str(depth)]
                for record in records
            )
            for depth in range(1, MAX_MUTATION_DEPTH + 1)
        }

        depth_hit_counts = {
            str(depth): sum(
                1
                for record in records
                if record["escape_example_count_by_depth"][str(depth)] > 0
            )
            for depth in range(1, MAX_MUTATION_DEPTH + 1)
        }

        depth_values_stable = (
            len(set(minimum_escape_depths)) == 1
            if minimum_escape_depths
            else False
        )

        target_stable = all(
            targets == [EXPECTED_ESCAPE_TARGET]
            for targets in escape_targets_by_variant
        )

        expected_depth = EXPECTED_ESCAPE_DEPTHS[class_name]

        expected_depth_matched = (
            depth_values_stable
            and minimum_escape_depths
            and minimum_escape_depths[0] == expected_depth
        )

        class_summary[class_name] = {
            "record_count": len(records),
            "minimum_escape_depths": minimum_escape_depths,
            "minimum_escape_depth_mean": (
                mean(minimum_escape_depths)
                if minimum_escape_depths
                else None
            ),
            "minimum_escape_depth_std": (
                pstdev(minimum_escape_depths)
                if len(minimum_escape_depths) > 1
                else 0.0
            ),
            "expected_escape_depth": expected_depth,
            "expected_depth_matched": expected_depth_matched,
            "escape_depth_stable": depth_values_stable,
            "escape_targets_by_variant": escape_targets_by_variant,
            "unique_escape_targets": unique_escape_targets,
            "expected_target": EXPECTED_ESCAPE_TARGET,
            "escape_target_stable": target_stable,
            "escape_example_counts": escape_example_counts,
            "escape_example_count_mean": (
                mean(escape_example_counts)
                if escape_example_counts
                else 0.0
            ),
            "escape_example_count_std": (
                pstdev(escape_example_counts)
                if len(escape_example_counts) > 1
                else 0.0
            ),
            "escape_example_count_total": sum(
                escape_example_counts
            ),
            "depth_hit_counts": depth_hit_counts,
            "depth_example_totals": depth_example_totals,
        }

    ordering_values = {
        class_name: values["minimum_escape_depths"][0]
        for class_name, values in class_summary.items()
        if values["minimum_escape_depths"]
    }

    expected_ordering_detected = (
        ordering_values.get("FRAGMENTED_LOCAL_COLLAPSE") == 3
        and ordering_values.get("GLOBAL_PERSISTENT_COLLAPSE") == 4
        and ordering_values.get("RECOVERY_RELAPSE_COLLAPSE") == 4
    )

    all_depths_stable = all(
        values["escape_depth_stable"]
        for values in class_summary.values()
    )

    all_targets_stable = all(
        values["escape_target_stable"]
        for values in class_summary.values()
    )

    all_expected_depths_matched = all(
        values["expected_depth_matched"]
        for values in class_summary.values()
    )

    return {
        "class_summary": class_summary,
        "ordering_values": ordering_values,
        "expected_ordering_detected": expected_ordering_detected,
        "all_depths_stable": all_depths_stable,
        "all_targets_stable": all_targets_stable,
        "all_expected_depths_matched": all_expected_depths_matched,
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
            build_variant_profiles(
                variant_index,
                variants_by_case,
            )
        )

    stability = summarize_escape_depth_stability(variant_results)
    class_summary = stability["class_summary"]

    summary = {
        "variant_count": variant_count,
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "max_mutation_depth": MAX_MUTATION_DEPTH,
        "noise_component": NOISE_COMPONENT,
        "collapse_component": COLLAPSE_COMPONENT,
        "expected_escape_target": EXPECTED_ESCAPE_TARGET,
        "expected_escape_depths": EXPECTED_ESCAPE_DEPTHS,
        "ordering_values": stability["ordering_values"],
        "expected_ordering_detected": (
            stability["expected_ordering_detected"]
        ),
        "all_depths_stable": stability["all_depths_stable"],
        "all_targets_stable": stability["all_targets_stable"],
        "all_expected_depths_matched": (
            stability["all_expected_depths_matched"]
        ),
        "fragmented_escape_depth": (
            class_summary["FRAGMENTED_LOCAL_COLLAPSE"][
                "minimum_escape_depths"
            ][0]
        ),
        "global_persistent_escape_depth": (
            class_summary["GLOBAL_PERSISTENT_COLLAPSE"][
                "minimum_escape_depths"
            ][0]
        ),
        "recovery_relapse_escape_depth": (
            class_summary["RECOVERY_RELAPSE_COLLAPSE"][
                "minimum_escape_depths"
            ][0]
        ),
        "fragmented_escape_example_total": (
            class_summary["FRAGMENTED_LOCAL_COLLAPSE"][
                "escape_example_count_total"
            ]
        ),
        "global_persistent_escape_example_total": (
            class_summary["GLOBAL_PERSISTENT_COLLAPSE"][
                "escape_example_count_total"
            ]
        ),
        "recovery_relapse_escape_example_total": (
            class_summary["RECOVERY_RELAPSE_COLLAPSE"][
                "escape_example_count_total"
            ]
        ),
    }

    status = (
        "PASS"
        if (
            summary["expected_ordering_detected"]
            and summary["all_depths_stable"]
            and summary["all_targets_stable"]
            and summary["all_expected_depths_matched"]
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_escape_depth_stability_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "class_escape_depth_stability": class_summary,
        "variant_results": variant_results,
        "interpretation": (
            "This experiment tests whether escape-depth ordering "
            "remains stable under wider trajectory variants."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_escape_depth_stability_v0.py"
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
        "Temporal Collapse Topology Escape Depth Stability v0"
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
    print("Class escape-depth stability")
    print("-" * 80)

    for class_name, values in class_summary.items():
        print(
            f"{class_name:<32} "
            f"depths={values['minimum_escape_depths']} "
            f"expected={values['expected_escape_depth']} "
            f"depth_stable={values['escape_depth_stable']} "
            f"target_stable={values['escape_target_stable']} "
            f"targets={values['unique_escape_targets']} "
            f"examples={values['escape_example_counts']} "
            f"total={values['escape_example_count_total']}"
        )

    print()
    print("Depth distribution")
    print("-" * 80)

    for class_name, values in class_summary.items():
        print(
            f"{class_name:<32} "
            f"depth_hits={values['depth_hit_counts']} "
            f"depth_examples={values['depth_example_totals']}"
        )

    print()
    print("Variant summaries")
    print("-" * 80)

    for variant in variant_results:
        print(f"variant_index={variant['variant_index']}")

        for record in variant.get("source_profiles", []):
            print(
                f"  {record['case_name']:<32} "
                f"class={record['source_class']:<32} "
                f"min_escape={record['minimum_escape_depth']} "
                f"targets={record['escape_targets']} "
                f"examples={record['escape_example_count']}"
            )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - escape-depth ordering stability detected: "
            "FRAGMENTED_LOCAL_COLLAPSE escaped at depth 3 while "
            "GLOBAL_PERSISTENT_COLLAPSE and RECOVERY_RELAPSE_COLLAPSE "
            "escaped at depth 4."
        )
    else:
        print(
            "CHECK - escape-depth ordering stability was not fully "
            "confirmed under tested variants."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()