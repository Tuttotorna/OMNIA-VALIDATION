import itertools
import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_reversibility_index_v0.json"
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

    escape_example_count_by_depth = {
        str(depth): 0
        for depth in range(1, max_depth + 1)
    }

    escape_targets_by_depth = {
        str(depth): []
        for depth in range(1, max_depth + 1)
    }

    if source_component != "COLLAPSE_COMPONENT":
        return {
            "source_class": source_class,
            "source_component": source_component,
            "source_metrics": source_metrics,
            "checked_by_depth": checked_by_depth,
            "minimum_escape_depth": None,
            "escape_targets": [],
            "escape_example_count": 0,
            "escape_example_count_by_depth": (
                escape_example_count_by_depth
            ),
            "escape_targets_by_depth": escape_targets_by_depth,
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
        depth_key = str(escape["escape_depth"])

        escape_example_count_by_depth[depth_key] += (
            escape["example_count"]
        )

        escape_targets_by_depth[depth_key].append(
            escape["to_class"]
        )

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
        escape_example_count_by_depth.values()
    )

    return {
        "source_class": source_class,
        "source_component": source_component,
        "source_metrics": source_metrics,
        "checked_by_depth": checked_by_depth,
        "minimum_escape_depth": minimum_escape_depth,
        "escape_targets": escape_targets,
        "escape_example_count": escape_example_count,
        "escape_example_count_by_depth": escape_example_count_by_depth,
        "escape_targets_by_depth": {
            key: sorted(set(value))
            for key, value in escape_targets_by_depth.items()
        },
    }


def build_variant_profiles(variant_index, variants_by_case):
    source_profiles = []

    for case_name, sequences in variants_by_case.items():
        sequence = sequences[variant_index]

        profile = find_escape_profile(
            sequence,
            max_depth=MAX_MUTATION_DEPTH,
        )

        source_profiles.append({
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
            "escape_targets_by_depth": (
                profile["escape_targets_by_depth"]
            ),
        })

    return {
        "variant_index": variant_index,
        "source_profiles": source_profiles,
    }


def normalize(value, maximum):
    if maximum <= 0:
        return 0.0

    return value / maximum


def summarize_reversibility(variant_results):
    class_summary = {}

    raw_density_values = []

    for class_name in COLLAPSE_COMPONENT:
        records = []

        for variant in variant_results:
            for record in variant["source_profiles"]:
                if record["source_class"] == class_name:
                    records.append(record)

        total_escape_examples = sum(
            record["escape_example_count"]
            for record in records
        )

        raw_density_values.append(total_escape_examples)

    max_escape_examples = max(raw_density_values) if raw_density_values else 1

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

        total_escape_examples = sum(escape_example_counts)

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

        minimum_escape_depth = (
            min(minimum_escape_depths)
            if minimum_escape_depths
            else None
        )

        mean_escape_depth = (
            mean(minimum_escape_depths)
            if minimum_escape_depths
            else None
        )

        escape_depth_stable = (
            len(set(minimum_escape_depths)) == 1
            if minimum_escape_depths
            else False
        )

        escape_depth_std = (
            pstdev(minimum_escape_depths)
            if len(minimum_escape_depths) > 1
            else 0.0
        )

        target_stable = all(
            targets == [EXPECTED_ESCAPE_TARGET]
            for targets in escape_targets_by_variant
        )

        target_stability_score = 1.0 if target_stable else 0.0
        depth_stability_score = 1.0 if escape_depth_stable else 0.0

        depth_component = (
            1.0 / minimum_escape_depth
            if minimum_escape_depth
            else 0.0
        )

        density_component = normalize(
            total_escape_examples,
            max_escape_examples,
        )

        reversibility_index = (
            0.45 * depth_component
            + 0.35 * density_component
            + 0.10 * target_stability_score
            + 0.10 * depth_stability_score
        )

        class_summary[class_name] = {
            "record_count": len(records),
            "minimum_escape_depths": minimum_escape_depths,
            "minimum_escape_depth": minimum_escape_depth,
            "mean_escape_depth": mean_escape_depth,
            "escape_depth_std": escape_depth_std,
            "escape_depth_stable": escape_depth_stable,
            "escape_targets_by_variant": escape_targets_by_variant,
            "unique_escape_targets": unique_escape_targets,
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
            "escape_example_count_total": total_escape_examples,
            "depth_hit_counts": depth_hit_counts,
            "depth_example_totals": depth_example_totals,
            "depth_component": depth_component,
            "density_component": density_component,
            "target_stability_component": target_stability_score,
            "depth_stability_component": depth_stability_score,
            "reversibility_index": reversibility_index,
        }

    ranking = sorted(
        COLLAPSE_COMPONENT,
        key=lambda class_name: (
            class_summary[class_name]["reversibility_index"],
            class_summary[class_name]["escape_example_count_total"],
            -class_summary[class_name]["minimum_escape_depth"],
        ),
        reverse=True,
    )

    ranking_with_scores = [
        {
            "rank": index + 1,
            "class_name": class_name,
            "reversibility_index": (
                class_summary[class_name]["reversibility_index"]
            ),
            "minimum_escape_depth": (
                class_summary[class_name]["minimum_escape_depth"]
            ),
            "escape_example_count_total": (
                class_summary[class_name]["escape_example_count_total"]
            ),
            "escape_target": (
                class_summary[class_name]["unique_escape_targets"]
            ),
        }
        for index, class_name in enumerate(ranking)
    ]

    expected_ranking = [
        "FRAGMENTED_LOCAL_COLLAPSE",
        "RECOVERY_RELAPSE_COLLAPSE",
        "GLOBAL_PERSISTENT_COLLAPSE",
    ]

    ranking_matches_expected = ranking == expected_ranking

    return {
        "class_summary": class_summary,
        "ranking": ranking,
        "ranking_with_scores": ranking_with_scores,
        "expected_ranking": expected_ranking,
        "ranking_matches_expected": ranking_matches_expected,
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

    reversibility = summarize_reversibility(variant_results)

    class_summary = reversibility["class_summary"]

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
        "reversibility_index_definition": (
            "0.45*(1/min_escape_depth) + "
            "0.35*(escape_density_normalized) + "
            "0.10*(target_stability) + "
            "0.10*(depth_stability)"
        ),
        "ranking": reversibility["ranking"],
        "expected_ranking": reversibility["expected_ranking"],
        "ranking_matches_expected": (
            reversibility["ranking_matches_expected"]
        ),
        "top_reversible_class": reversibility["ranking"][0],
        "fragmented_reversibility_index": (
            class_summary["FRAGMENTED_LOCAL_COLLAPSE"][
                "reversibility_index"
            ]
        ),
        "global_persistent_reversibility_index": (
            class_summary["GLOBAL_PERSISTENT_COLLAPSE"][
                "reversibility_index"
            ]
        ),
        "recovery_relapse_reversibility_index": (
            class_summary["RECOVERY_RELAPSE_COLLAPSE"][
                "reversibility_index"
            ]
        ),
        "fragmented_escape_depth": (
            class_summary["FRAGMENTED_LOCAL_COLLAPSE"][
                "minimum_escape_depth"
            ]
        ),
        "global_persistent_escape_depth": (
            class_summary["GLOBAL_PERSISTENT_COLLAPSE"][
                "minimum_escape_depth"
            ]
        ),
        "recovery_relapse_escape_depth": (
            class_summary["RECOVERY_RELAPSE_COLLAPSE"][
                "minimum_escape_depth"
            ]
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
            summary["ranking_matches_expected"]
            and summary["top_reversible_class"]
            == "FRAGMENTED_LOCAL_COLLAPSE"
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_reversibility_index_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "class_reversibility_summary": class_summary,
        "ranking_with_scores": reversibility["ranking_with_scores"],
        "variant_results": variant_results,
        "interpretation": (
            "This experiment computes a normalized reversibility "
            "index for collapse-side temporal topology classes."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_reversibility_index_v0.py"
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
        "Temporal Collapse Topology Reversibility Index v0"
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
    print("Ranking")
    print("-" * 80)

    for item in reversibility["ranking_with_scores"]:
        print(
            f"rank={item['rank']} "
            f"class={item['class_name']:<32} "
            f"index={item['reversibility_index']} "
            f"min_escape={item['minimum_escape_depth']} "
            f"examples={item['escape_example_count_total']} "
            f"target={item['escape_target']}"
        )

    print()
    print("Class reversibility summary")
    print("-" * 80)

    for class_name, values in class_summary.items():
        print(
            f"{class_name:<32} "
            f"index={values['reversibility_index']} "
            f"depth={values['minimum_escape_depth']} "
            f"density={values['density_component']} "
            f"target_stable={values['escape_target_stable']} "
            f"depth_stable={values['escape_depth_stable']} "
            f"examples={values['escape_example_count_total']}"
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
            "PASS - collapse-basin reversibility ranking detected: "
            "FRAGMENTED_LOCAL_COLLAPSE ranked highest, followed by "
            "RECOVERY_RELAPSE_COLLAPSE and GLOBAL_PERSISTENT_COLLAPSE."
        )
    else:
        print(
            "CHECK - reversibility ranking did not match the expected "
            "collapse-basin ordering."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()