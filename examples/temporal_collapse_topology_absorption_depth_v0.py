import itertools
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_absorption_depth_v0.json"
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
    ]

    variants["global_persistent_collapse"] = [
        make_sequence(18, [(6, 8)]),
        make_sequence(22, [(8, 8)]),
        make_sequence(26, [(10, 8)]),
    ]

    variants["recovery_relapse_collapse"] = [
        make_sequence(20, [(3, 2), (10, 6)]),
        make_sequence(24, [(4, 2), (12, 6)]),
        make_sequence(28, [(5, 2), (14, 6)]),
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

    escape_example_count = sum(
        escape["example_count"]
        for escape in all_escapes
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
    }


def build_variant_profiles(variant_index, variants_by_case):
    source_profiles = []
    class_profiles = defaultdict(list)

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
            "escapes_by_depth": profile["escapes_by_depth"],
            "minimum_escape_depth": profile["minimum_escape_depth"],
            "escape_targets": profile["escape_targets"],
            "escape_example_count": profile["escape_example_count"],
        }

        source_profiles.append(record)
        class_profiles[profile["source_class"]].append(record)

    return {
        "variant_index": variant_index,
        "source_profiles": source_profiles,
        "class_profiles": dict(class_profiles),
    }


def summarize_absorption_depth(variant_results):
    class_summary = {}

    for class_name in COLLAPSE_COMPONENT:
        minimum_escape_depths = []
        escape_example_counts = []
        escape_targets = []
        absorbing_variant_count = 0
        reversible_variant_count = 0

        depth_hit_counts = {
            str(depth): 0
            for depth in range(1, MAX_MUTATION_DEPTH + 1)
        }

        depth_example_totals = {
            str(depth): 0
            for depth in range(1, MAX_MUTATION_DEPTH + 1)
        }

        for variant in variant_results:
            records = variant["class_profiles"].get(class_name, [])

            for record in records:
                min_depth = record["minimum_escape_depth"]

                if min_depth is None:
                    absorbing_variant_count += 1
                else:
                    reversible_variant_count += 1
                    minimum_escape_depths.append(min_depth)

                escape_example_counts.append(
                    record["escape_example_count"]
                )

                escape_targets.extend(record["escape_targets"])

                for depth, escapes in record["escapes_by_depth"].items():
                    if escapes:
                        depth_hit_counts[depth] += 1

                    depth_example_totals[depth] += sum(
                        escape["example_count"]
                        for escape in escapes
                    )

        total_variant_count = (
            absorbing_variant_count + reversible_variant_count
        )

        reversible_rate = (
            reversible_variant_count / total_variant_count
            if total_variant_count
            else 0.0
        )

        absorbing_rate = (
            absorbing_variant_count / total_variant_count
            if total_variant_count
            else 0.0
        )

        mean_minimum_escape_depth = (
            mean(minimum_escape_depths)
            if minimum_escape_depths
            else None
        )

        minimum_observed_escape_depth = (
            min(minimum_escape_depths)
            if minimum_escape_depths
            else None
        )

        escape_depth_std = (
            pstdev(minimum_escape_depths)
            if len(minimum_escape_depths) > 1
            else 0.0
        )

        total_escape_examples = sum(escape_example_counts)

        reversibility_index = (
            reversible_rate / max(mean_minimum_escape_depth or 99, 1)
        )

        absorbing_state_index = (
            absorbing_rate
            + (
                1 / (1 + total_escape_examples)
                if total_escape_examples >= 0
                else 0.0
            )
        )

        class_summary[class_name] = {
            "variant_count": total_variant_count,
            "absorbing_variant_count": absorbing_variant_count,
            "reversible_variant_count": reversible_variant_count,
            "absorbing_rate": absorbing_rate,
            "reversible_rate": reversible_rate,
            "minimum_escape_depths": minimum_escape_depths,
            "minimum_observed_escape_depth": (
                minimum_observed_escape_depth
            ),
            "mean_minimum_escape_depth": (
                mean_minimum_escape_depth
            ),
            "escape_depth_std": escape_depth_std,
            "unique_escape_targets": sorted(set(escape_targets)),
            "escape_example_counts": escape_example_counts,
            "total_escape_examples": total_escape_examples,
            "depth_hit_counts": depth_hit_counts,
            "depth_example_totals": depth_example_totals,
            "reversibility_index": reversibility_index,
            "absorbing_state_index": absorbing_state_index,
            "is_absorbing_under_test": reversible_variant_count == 0,
            "is_reversible_under_test": reversible_variant_count > 0,
        }

    reversible_classes = [
        class_name
        for class_name, values in class_summary.items()
        if values["is_reversible_under_test"]
    ]

    absorbing_classes = [
        class_name
        for class_name, values in class_summary.items()
        if values["is_absorbing_under_test"]
    ]

    stratification_detected = (
        "FRAGMENTED_LOCAL_COLLAPSE" in reversible_classes
        and "GLOBAL_PERSISTENT_COLLAPSE" in absorbing_classes
        and "RECOVERY_RELAPSE_COLLAPSE" in absorbing_classes
    )

    return {
        "class_summary": class_summary,
        "reversible_classes": reversible_classes,
        "absorbing_classes": absorbing_classes,
        "stratification_detected": stratification_detected,
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

    absorption = summarize_absorption_depth(variant_results)

    class_summary = absorption["class_summary"]

    summary = {
        "variant_count": variant_count,
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "max_mutation_depth": MAX_MUTATION_DEPTH,
        "noise_component": NOISE_COMPONENT,
        "collapse_component": COLLAPSE_COMPONENT,
        "reversible_classes": absorption["reversible_classes"],
        "absorbing_classes": absorption["absorbing_classes"],
        "stratification_detected": (
            absorption["stratification_detected"]
        ),
        "fragmented_min_escape_depth": (
            class_summary["FRAGMENTED_LOCAL_COLLAPSE"][
                "minimum_observed_escape_depth"
            ]
        ),
        "global_persistent_min_escape_depth": (
            class_summary["GLOBAL_PERSISTENT_COLLAPSE"][
                "minimum_observed_escape_depth"
            ]
        ),
        "recovery_relapse_min_escape_depth": (
            class_summary["RECOVERY_RELAPSE_COLLAPSE"][
                "minimum_observed_escape_depth"
            ]
        ),
        "fragmented_reversibility_index": (
            class_summary["FRAGMENTED_LOCAL_COLLAPSE"][
                "reversibility_index"
            ]
        ),
        "global_persistent_absorbing_state_index": (
            class_summary["GLOBAL_PERSISTENT_COLLAPSE"][
                "absorbing_state_index"
            ]
        ),
        "recovery_relapse_absorbing_state_index": (
            class_summary["RECOVERY_RELAPSE_COLLAPSE"][
                "absorbing_state_index"
            ]
        ),
    }

    status = (
        "PASS"
        if absorption["stratification_detected"]
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_absorption_depth_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "class_absorption_summary": class_summary,
        "variant_results": variant_results,
        "interpretation": (
            "This experiment measures internal stratification of "
            "the confirmed-collapse basin by comparing reversible "
            "and absorbing collapse-side classes under mutation "
            "depth up to 4."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_absorption_depth_v0.py"
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
        "Temporal Collapse Topology Absorption Depth v0"
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
    print("Class absorption summary")
    print("-" * 80)

    for class_name, values in class_summary.items():
        print(
            f"{class_name:<32} "
            f"absorbing_rate={values['absorbing_rate']} "
            f"reversible_rate={values['reversible_rate']} "
            f"min_escape={values['minimum_observed_escape_depth']} "
            f"mean_escape={values['mean_minimum_escape_depth']} "
            f"escape_std={values['escape_depth_std']} "
            f"targets={values['unique_escape_targets']} "
            f"examples={values['total_escape_examples']} "
            f"rev_index={values['reversibility_index']} "
            f"abs_index={values['absorbing_state_index']}"
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
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - collapse-basin internal stratification detected: "
            "FRAGMENTED_LOCAL_COLLAPSE was reversible while deeper "
            "collapse states remained absorbing under tested mutations."
        )
    else:
        print(
            "CHECK - collapse-basin internal stratification was not "
            "cleanly separated under tested mutations."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()