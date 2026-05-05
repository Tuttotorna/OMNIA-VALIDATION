import itertools
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_basin_escape_v0.json"
)

CONFIRMATION_WINDOW = 2
PERSISTENCE_WINDOW = 2
GLOBAL_PERSISTENCE_THRESHOLD = (
    CONFIRMATION_WINDOW + PERSISTENCE_WINDOW
)

MAX_MUTATION_DEPTH = 3

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


def find_basin_escapes_from_sequence(sequence, max_depth=MAX_MUTATION_DEPTH):
    source_metrics = classify(sequence)
    source_class = source_metrics["classification"]
    source_component = component_for_class(source_class)

    escapes = {}

    checked_by_depth = {
        str(depth): 0
        for depth in range(1, max_depth + 1)
    }

    if source_component != "COLLAPSE_COMPONENT":
        return {
            "source_class": source_class,
            "source_component": source_component,
            "source_metrics": source_metrics,
            "checked_by_depth": checked_by_depth,
            "escapes": [],
        }

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
            )

            if key not in escapes:
                escapes[key] = {
                    "from_class": source_class,
                    "to_class": target_class,
                    "escape_depth": depth,
                    "example_mutations": mutations,
                    "example_sequence": mutated,
                    "example_metrics": target_metrics,
                    "example_count": 1,
                }
            else:
                escapes[key]["example_count"] += 1

                if depth < escapes[key]["escape_depth"]:
                    escapes[key]["escape_depth"] = depth
                    escapes[key]["example_mutations"] = mutations
                    escapes[key]["example_sequence"] = mutated
                    escapes[key]["example_metrics"] = target_metrics

    return {
        "source_class": source_class,
        "source_component": source_component,
        "source_metrics": source_metrics,
        "checked_by_depth": checked_by_depth,
        "escapes": list(escapes.values()),
    }


def build_variant_escapes(variant_index, variants_by_case):
    source_results = []
    escape_map = {}

    for case_name, sequences in variants_by_case.items():
        sequence = sequences[variant_index]

        result = find_basin_escapes_from_sequence(
            sequence,
            max_depth=MAX_MUTATION_DEPTH,
        )

        source_results.append({
            "case_name": case_name,
            "variant_index": variant_index,
            "source_class": result["source_class"],
            "source_component": result["source_component"],
            "source_metrics": result["source_metrics"],
            "sequence_length": len(sequence),
            "raw_action_sequence": sequence,
            "checked_by_depth": result["checked_by_depth"],
            "escape_count": len(result["escapes"]),
            "escapes": result["escapes"],
        })

        for escape in result["escapes"]:
            key = (
                escape["from_class"],
                escape["to_class"],
            )

            if key not in escape_map:
                escape_map[key] = {
                    "from_class": escape["from_class"],
                    "to_class": escape["to_class"],
                    "escape_depth": escape["escape_depth"],
                    "example_count": escape["example_count"],
                    "source_case_names": [case_name],
                    "example_mutations": escape["example_mutations"],
                    "example_sequence": escape["example_sequence"],
                    "example_metrics": escape["example_metrics"],
                }
            else:
                escape_map[key]["example_count"] += (
                    escape["example_count"]
                )

                if escape["escape_depth"] < escape_map[key]["escape_depth"]:
                    escape_map[key]["escape_depth"] = escape["escape_depth"]
                    escape_map[key]["example_mutations"] = (
                        escape["example_mutations"]
                    )
                    escape_map[key]["example_sequence"] = (
                        escape["example_sequence"]
                    )
                    escape_map[key]["example_metrics"] = (
                        escape["example_metrics"]
                    )

                if case_name not in escape_map[key]["source_case_names"]:
                    escape_map[key]["source_case_names"].append(case_name)

    escapes = list(escape_map.values())

    target_counts = defaultdict(int)
    target_example_counts = defaultdict(int)
    source_to_targets = defaultdict(list)
    source_to_depths = defaultdict(list)

    for escape in escapes:
        target_counts[escape["to_class"]] += 1
        target_example_counts[escape["to_class"]] += (
            escape["example_count"]
        )

        source_to_targets[escape["from_class"]].append(
            escape["to_class"]
        )

        source_to_depths[escape["from_class"]].append(
            escape["escape_depth"]
        )

    if target_example_counts:
        dominant_escape_target = max(
            target_example_counts,
            key=lambda key: (
                target_example_counts[key],
                target_counts[key],
            ),
        )
    else:
        dominant_escape_target = None

    return {
        "variant_index": variant_index,
        "source_results": source_results,
        "escapes": escapes,
        "escape_count": len(escapes),
        "target_counts": dict(target_counts),
        "target_example_counts": dict(target_example_counts),
        "source_to_targets": {
            key: sorted(set(value))
            for key, value in source_to_targets.items()
        },
        "source_to_escape_depths": {
            key: value
            for key, value in source_to_depths.items()
        },
        "dominant_escape_target": dominant_escape_target,
    }


def summarize_escape_stability(variant_results):
    all_escape_keys = sorted({
        f"{escape['from_class']}->{escape['to_class']}"
        for variant in variant_results
        for escape in variant["escapes"]
    })

    escape_stability = {}

    for key in all_escape_keys:
        present_variants = []
        depths = []
        example_counts = []

        for variant in variant_results:
            lookup = {
                f"{escape['from_class']}->{escape['to_class']}": escape
                for escape in variant["escapes"]
            }

            if key in lookup:
                present_variants.append(variant["variant_index"])
                depths.append(lookup[key]["escape_depth"])
                example_counts.append(lookup[key]["example_count"])

        escape_stability[key] = {
            "present_variant_count": len(present_variants),
            "present_variants": present_variants,
            "persistence_rate": (
                len(present_variants) / len(variant_results)
                if variant_results
                else 0.0
            ),
            "escape_depths": depths,
            "escape_depth_mean": (
                mean(depths)
                if depths
                else None
            ),
            "escape_depth_std": (
                pstdev(depths)
                if len(depths) > 1
                else 0.0
            ),
            "example_counts": example_counts,
            "example_count_mean": (
                mean(example_counts)
                if example_counts
                else None
            ),
            "example_count_total": sum(example_counts),
        }

    dominant_values = [
        variant["dominant_escape_target"]
        for variant in variant_results
    ]

    target_frequency = defaultdict(int)
    target_example_totals = defaultdict(int)

    for variant in variant_results:
        for target, count in variant["target_counts"].items():
            target_frequency[target] += count

        for target, count in variant["target_example_counts"].items():
            target_example_totals[target] += count

    source_escape_stability = {}

    for source_class in COLLAPSE_COMPONENT:
        targets_by_variant = []
        depths_by_variant = []

        for variant in variant_results:
            targets_by_variant.append(
                variant["source_to_targets"].get(
                    source_class,
                    [],
                )
            )

            depths_by_variant.append(
                variant["source_to_escape_depths"].get(
                    source_class,
                    [],
                )
            )

        flattened_targets = [
            target
            for targets in targets_by_variant
            for target in targets
        ]

        flattened_depths = [
            depth
            for depths in depths_by_variant
            for depth in depths
        ]

        source_escape_stability[source_class] = {
            "targets_by_variant": targets_by_variant,
            "unique_targets": sorted(set(flattened_targets)),
            "target_count_by_variant": [
                len(targets)
                for targets in targets_by_variant
            ],
            "escape_depths_by_variant": depths_by_variant,
            "minimum_escape_depth": (
                min(flattened_depths)
                if flattened_depths
                else None
            ),
            "mean_escape_depth": (
                mean(flattened_depths)
                if flattened_depths
                else None
            ),
        }

    return {
        "escape_stability": escape_stability,
        "dominant_escape_values": dominant_values,
        "dominant_escape_stable": (
            len(set(dominant_values)) == 1
        ),
        "target_frequency": dict(target_frequency),
        "target_example_totals": dict(target_example_totals),
        "source_escape_stability": source_escape_stability,
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
            build_variant_escapes(
                variant_index,
                variants_by_case,
            )
        )

    stability = summarize_escape_stability(variant_results)

    escape_counts = [
        item["escape_count"]
        for item in variant_results
    ]

    fully_persistent_escapes = [
        key
        for key, values in stability["escape_stability"].items()
        if values["persistence_rate"] == 1.0
    ]

    partial_escapes = [
        key
        for key, values in stability["escape_stability"].items()
        if values["persistence_rate"] < 1.0
    ]

    total_escape_examples = sum(
        stability["target_example_totals"].values()
    )

    total_escape_paths = len(stability["escape_stability"])

    absorbing_basin_score = (
        1 / (1 + total_escape_paths)
    )

    strong_absorption = (
        total_escape_paths == 0
    )

    weak_absorption = (
        total_escape_paths > 0
        and all(
            values["persistence_rate"] < 1.0
            for values in stability["escape_stability"].values()
        )
    )

    summary = {
        "variant_count": variant_count,
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "max_mutation_depth": MAX_MUTATION_DEPTH,
        "noise_component": NOISE_COMPONENT,
        "collapse_component": COLLAPSE_COMPONENT,
        "escape_count_values": escape_counts,
        "mean_escape_count": mean(escape_counts),
        "escape_count_std": (
            pstdev(escape_counts)
            if len(escape_counts) > 1
            else 0.0
        ),
        "fully_persistent_escape_count": len(
            fully_persistent_escapes
        ),
        "partial_escape_count": len(partial_escapes),
        "total_escape_path_count": total_escape_paths,
        "total_escape_example_count": total_escape_examples,
        "fully_persistent_escapes": fully_persistent_escapes,
        "partial_escapes": partial_escapes,
        "dominant_escape_values": (
            stability["dominant_escape_values"]
        ),
        "dominant_escape_stable": (
            stability["dominant_escape_stable"]
        ),
        "target_frequency": stability["target_frequency"],
        "target_example_totals": (
            stability["target_example_totals"]
        ),
        "absorbing_basin_score": absorbing_basin_score,
        "strong_absorption": strong_absorption,
        "weak_absorption": weak_absorption,
    }

    status = (
        "PASS"
        if (
            strong_absorption
            or weak_absorption
            or (
                len(fully_persistent_escapes) == 0
                and absorbing_basin_score >= 0.25
            )
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_basin_escape_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "escape_stability": stability["escape_stability"],
        "source_escape_stability": (
            stability["source_escape_stability"]
        ),
        "variant_results": variant_results,
        "interpretation": (
            "This experiment measures whether confirmed-collapse "
            "topology can escape back to the noise-like component "
            "under controlled mutations."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_basin_escape_v0.py"
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
        "Temporal Collapse Topology Basin Escape v0"
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
    print("Escape stability")
    print("-" * 80)

    for key, values in stability["escape_stability"].items():
        print(
            f"{key:<65} "
            f"present={values['present_variant_count']} "
            f"rate={values['persistence_rate']} "
            f"depths={values['escape_depths']} "
            f"depth_std={values['escape_depth_std']} "
            f"examples={values['example_counts']} "
            f"total={values['example_count_total']}"
        )

    print()
    print("Source escape stability")
    print("-" * 80)

    for source_class, values in stability[
        "source_escape_stability"
    ].items():
        print(
            f"{source_class:<32} "
            f"targets={values['targets_by_variant']} "
            f"unique={values['unique_targets']} "
            f"counts={values['target_count_by_variant']} "
            f"min_depth={values['minimum_escape_depth']} "
            f"mean_depth={values['mean_escape_depth']}"
        )

    print()
    print("Variant summaries")
    print("-" * 80)

    for variant in variant_results:
        print(
            f"variant={variant['variant_index']} "
            f"escape_count={variant['escape_count']} "
            f"dominant_escape={variant['dominant_escape_target']} "
            f"target_counts={variant['target_counts']} "
            f"target_examples={variant['target_example_counts']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        if strong_absorption:
            print(
                "PASS - confirmed-collapse basin behaved as strongly "
                "absorbing: no escape paths were detected."
            )
        elif weak_absorption:
            print(
                "PASS - confirmed-collapse basin behaved as weakly "
                "absorbing: only non-persistent escape paths were detected."
            )
        else:
            print(
                "PASS - confirmed-collapse basin retained partial "
                "absorption under tested mutations."
            )
    else:
        print(
            "CHECK - confirmed-collapse basin exposed stable escape "
            "paths back to noise-like topology."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()