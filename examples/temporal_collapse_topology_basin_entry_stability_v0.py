import itertools
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_basin_entry_stability_v0.json"
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

    variants["clean_pass"] = [
        make_sequence(12, []),
        make_sequence(16, []),
        make_sequence(20, []),
        make_sequence(24, []),
        make_sequence(28, []),
    ]

    variants["spike_filtered"] = [
        make_sequence(12, [(3, 1)]),
        make_sequence(16, [(6, 1)]),
        make_sequence(20, [(9, 1)]),
        make_sequence(24, [(12, 1)]),
        make_sequence(28, [(15, 1)]),
    ]

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


def find_basin_entries_from_sequence(sequence, max_depth=MAX_MUTATION_DEPTH):
    source_metrics = classify(sequence)
    source_class = source_metrics["classification"]
    source_component = component_for_class(source_class)

    entries = {}

    checked_by_depth = {
        str(depth): 0
        for depth in range(1, max_depth + 1)
    }

    if source_component != "NOISE_COMPONENT":
        return {
            "source_class": source_class,
            "source_component": source_component,
            "source_metrics": source_metrics,
            "checked_by_depth": checked_by_depth,
            "entries": [],
        }

    for depth in range(1, max_depth + 1):
        for mutations in candidate_mutations(sequence, depth):
            checked_by_depth[str(depth)] += 1

            mutated = mutate_sequence(sequence, mutations)
            target_metrics = classify(mutated)
            target_class = target_metrics["classification"]
            target_component = component_for_class(target_class)

            if target_component != "COLLAPSE_COMPONENT":
                continue

            key = (
                source_class,
                target_class,
            )

            if key not in entries:
                entries[key] = {
                    "from_class": source_class,
                    "to_class": target_class,
                    "entry_depth": depth,
                    "example_mutations": mutations,
                    "example_sequence": mutated,
                    "example_metrics": target_metrics,
                    "example_count": 1,
                }
            else:
                entries[key]["example_count"] += 1

                if depth < entries[key]["entry_depth"]:
                    entries[key]["entry_depth"] = depth
                    entries[key]["example_mutations"] = mutations
                    entries[key]["example_sequence"] = mutated
                    entries[key]["example_metrics"] = target_metrics

    return {
        "source_class": source_class,
        "source_component": source_component,
        "source_metrics": source_metrics,
        "checked_by_depth": checked_by_depth,
        "entries": list(entries.values()),
    }


def build_variant_entries(variant_index, variants_by_case):
    source_results = []
    entry_map = {}

    for case_name, sequences in variants_by_case.items():
        sequence = sequences[variant_index]

        result = find_basin_entries_from_sequence(
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
            "entry_count": len(result["entries"]),
            "entries": result["entries"],
        })

        for entry in result["entries"]:
            key = (
                entry["from_class"],
                entry["to_class"],
            )

            if key not in entry_map:
                entry_map[key] = {
                    "from_class": entry["from_class"],
                    "to_class": entry["to_class"],
                    "entry_depth": entry["entry_depth"],
                    "example_count": entry["example_count"],
                    "source_case_names": [case_name],
                    "example_mutations": entry["example_mutations"],
                    "example_sequence": entry["example_sequence"],
                    "example_metrics": entry["example_metrics"],
                }
            else:
                entry_map[key]["example_count"] += (
                    entry["example_count"]
                )

                if entry["entry_depth"] < entry_map[key]["entry_depth"]:
                    entry_map[key]["entry_depth"] = entry["entry_depth"]
                    entry_map[key]["example_mutations"] = (
                        entry["example_mutations"]
                    )
                    entry_map[key]["example_sequence"] = (
                        entry["example_sequence"]
                    )
                    entry_map[key]["example_metrics"] = (
                        entry["example_metrics"]
                    )

                if case_name not in entry_map[key]["source_case_names"]:
                    entry_map[key]["source_case_names"].append(case_name)

    entries = list(entry_map.values())

    target_counts = defaultdict(int)
    target_example_counts = defaultdict(int)
    source_to_targets = defaultdict(list)
    source_to_depths = defaultdict(list)

    for entry in entries:
        target_counts[entry["to_class"]] += 1
        target_example_counts[entry["to_class"]] += (
            entry["example_count"]
        )

        source_to_targets[entry["from_class"]].append(
            entry["to_class"]
        )

        source_to_depths[entry["from_class"]].append(
            entry["entry_depth"]
        )

    if target_example_counts:
        dominant_entry_class = max(
            target_example_counts,
            key=lambda key: (
                target_example_counts[key],
                target_counts[key],
            ),
        )
    else:
        dominant_entry_class = None

    return {
        "variant_index": variant_index,
        "source_results": source_results,
        "entries": entries,
        "entry_count": len(entries),
        "target_counts": dict(target_counts),
        "target_example_counts": dict(target_example_counts),
        "source_to_targets": {
            key: sorted(set(value))
            for key, value in source_to_targets.items()
        },
        "source_to_entry_depths": {
            key: value
            for key, value in source_to_depths.items()
        },
        "dominant_entry_class": dominant_entry_class,
    }


def summarize_entry_stability(variant_results):
    all_entry_keys = sorted({
        f"{entry['from_class']}->{entry['to_class']}"
        for variant in variant_results
        for entry in variant["entries"]
    })

    entry_stability = {}

    for key in all_entry_keys:
        present_variants = []
        depths = []
        example_counts = []

        for variant in variant_results:
            lookup = {
                f"{entry['from_class']}->{entry['to_class']}": entry
                for entry in variant["entries"]
            }

            if key in lookup:
                present_variants.append(variant["variant_index"])
                depths.append(lookup[key]["entry_depth"])
                example_counts.append(lookup[key]["example_count"])

        entry_stability[key] = {
            "present_variant_count": len(present_variants),
            "present_variants": present_variants,
            "persistence_rate": (
                len(present_variants) / len(variant_results)
                if variant_results
                else 0.0
            ),
            "entry_depths": depths,
            "entry_depth_mean": (
                mean(depths)
                if depths
                else None
            ),
            "entry_depth_std": (
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
        variant["dominant_entry_class"]
        for variant in variant_results
    ]

    target_frequency = defaultdict(int)
    target_example_totals = defaultdict(int)

    for variant in variant_results:
        for target, count in variant["target_counts"].items():
            target_frequency[target] += count

        for target, count in variant["target_example_counts"].items():
            target_example_totals[target] += count

    source_entry_stability = {}

    for source_class in NOISE_COMPONENT:
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
                variant["source_to_entry_depths"].get(
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

        source_entry_stability[source_class] = {
            "targets_by_variant": targets_by_variant,
            "unique_targets": sorted(set(flattened_targets)),
            "target_count_by_variant": [
                len(targets)
                for targets in targets_by_variant
            ],
            "entry_depths_by_variant": depths_by_variant,
            "minimum_entry_depth": (
                min(flattened_depths)
                if flattened_depths
                else None
            ),
            "mean_entry_depth": (
                mean(flattened_depths)
                if flattened_depths
                else None
            ),
        }

    return {
        "entry_stability": entry_stability,
        "dominant_entry_values": dominant_values,
        "dominant_entry_stable": (
            len(set(dominant_values)) == 1
        ),
        "target_frequency": dict(target_frequency),
        "target_example_totals": dict(target_example_totals),
        "source_entry_stability": source_entry_stability,
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
            build_variant_entries(
                variant_index,
                variants_by_case,
            )
        )

    stability = summarize_entry_stability(variant_results)

    entry_counts = [
        item["entry_count"]
        for item in variant_results
    ]

    dominant_entry_values = stability["dominant_entry_values"]

    fully_persistent_entries = [
        key
        for key, values in stability["entry_stability"].items()
        if values["persistence_rate"] == 1.0
    ]

    partial_entries = [
        key
        for key, values in stability["entry_stability"].items()
        if values["persistence_rate"] < 1.0
    ]

    fragmented_dominance = (
        stability["dominant_entry_stable"]
        and dominant_entry_values
        and dominant_entry_values[0] == "FRAGMENTED_LOCAL_COLLAPSE"
    )

    canonical_entries = [
        "CLEAN_PASS->FRAGMENTED_LOCAL_COLLAPSE",
        "SPIKE_FILTERED->FRAGMENTED_LOCAL_COLLAPSE",
        "OSCILLATING_NONPERSISTENT->FRAGMENTED_LOCAL_COLLAPSE",
    ]

    canonical_entries_present = all(
        entry in fully_persistent_entries
        for entry in canonical_entries
    )

    fragmented_examples = stability["target_example_totals"].get(
        "FRAGMENTED_LOCAL_COLLAPSE",
        0,
    )

    relapse_examples = stability["target_example_totals"].get(
        "RECOVERY_RELAPSE_COLLAPSE",
        0,
    )

    dominance_ratio = (
        fragmented_examples / max(relapse_examples, 1)
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
        "entry_count_values": entry_counts,
        "mean_entry_count": mean(entry_counts),
        "entry_count_std": (
            pstdev(entry_counts)
            if len(entry_counts) > 1
            else 0.0
        ),
        "dominant_entry_values": dominant_entry_values,
        "dominant_entry_stable": (
            stability["dominant_entry_stable"]
        ),
        "fragmented_local_entry_dominant": fragmented_dominance,
        "fully_persistent_entry_count": len(
            fully_persistent_entries
        ),
        "partial_entry_count": len(partial_entries),
        "fully_persistent_entries": fully_persistent_entries,
        "partial_entries": partial_entries,
        "canonical_entries": canonical_entries,
        "canonical_entries_present": canonical_entries_present,
        "target_frequency": stability["target_frequency"],
        "target_example_totals": (
            stability["target_example_totals"]
        ),
        "fragmented_local_example_total": fragmented_examples,
        "recovery_relapse_example_total": relapse_examples,
        "fragmented_to_relapse_example_ratio": dominance_ratio,
    }

    status = (
        "PASS"
        if (
            fragmented_dominance
            and canonical_entries_present
            and dominance_ratio >= 10
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_basin_entry_stability_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "entry_stability": stability["entry_stability"],
        "source_entry_stability": (
            stability["source_entry_stability"]
        ),
        "variant_results": variant_results,
        "interpretation": (
            "This experiment stress-tests whether "
            "FRAGMENTED_LOCAL_COLLAPSE remains the canonical "
            "basin-entry state under wider trajectory variants "
            "and mutation depth up to 3."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_basin_entry_stability_v0.py"
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
        "Temporal Collapse Topology Basin Entry Stability v0"
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
    print("Entry stability")
    print("-" * 80)

    for key, values in stability["entry_stability"].items():
        print(
            f"{key:<65} "
            f"present={values['present_variant_count']} "
            f"rate={values['persistence_rate']} "
            f"depths={values['entry_depths']} "
            f"depth_std={values['entry_depth_std']} "
            f"examples={values['example_counts']} "
            f"total={values['example_count_total']}"
        )

    print()
    print("Source entry stability")
    print("-" * 80)

    for source_class, values in stability[
        "source_entry_stability"
    ].items():
        print(
            f"{source_class:<32} "
            f"targets={values['targets_by_variant']} "
            f"unique={values['unique_targets']} "
            f"counts={values['target_count_by_variant']} "
            f"min_depth={values['minimum_entry_depth']} "
            f"mean_depth={values['mean_entry_depth']}"
        )

    print()
    print("Variant summaries")
    print("-" * 80)

    for variant in variant_results:
        print(
            f"variant={variant['variant_index']} "
            f"entry_count={variant['entry_count']} "
            f"dominant_entry={variant['dominant_entry_class']} "
            f"target_counts={variant['target_counts']} "
            f"target_examples={variant['target_example_counts']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - basin-entry invariance detected: "
            "FRAGMENTED_LOCAL_COLLAPSE remained the dominant "
            "entry state into confirmed-collapse topology."
        )
    else:
        print(
            "CHECK - basin-entry dominance was not fully invariant "
            "under the widened test space."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()