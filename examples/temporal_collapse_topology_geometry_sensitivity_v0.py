import itertools
import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_geometry_sensitivity_v0.json"
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

SOURCE_CLASS = "FRAGMENTED_LOCAL_COLLAPSE"
TARGET_CLASS = "OSCILLATING_NONPERSISTENT"

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


def geometry_specs():
    return [
        {
            "name": "compact_low_spacing",
            "length": 18,
            "runs": [(3, 2), (7, 2), (11, 2)],
            "expected_reverse_depth": 3,
        },
        {
            "name": "medium_shifted_spacing",
            "length": 22,
            "runs": [(4, 2), (9, 2), (14, 2)],
            "expected_reverse_depth": 3,
        },
        {
            "name": "wide_spacing",
            "length": 26,
            "runs": [(5, 2), (11, 2), (17, 2)],
            "expected_reverse_depth": 3,
        },
        {
            "name": "long_sparse_spacing",
            "length": 34,
            "runs": [(6, 2), (15, 2), (24, 2)],
            "expected_reverse_depth": 3,
        },
        {
            "name": "front_loaded_geometry",
            "length": 28,
            "runs": [(2, 2), (6, 2), (10, 2)],
            "expected_reverse_depth": 3,
        },
        {
            "name": "back_loaded_geometry",
            "length": 32,
            "runs": [(16, 2), (21, 2), (26, 2)],
            "expected_reverse_depth": 3,
        },
        {
            "name": "four_spike_oscillation",
            "length": 30,
            "runs": [(4, 2), (9, 2), (14, 2), (19, 2)],
            "expected_reverse_depth": 4,
        },
        {
            "name": "dense_fragmented_geometry",
            "length": 28,
            "runs": [(4, 2), (8, 2), (12, 2), (16, 2)],
            "expected_reverse_depth": 4,
        },
        {
            "name": "very_dense_four_run_geometry",
            "length": 24,
            "runs": [(3, 2), (6, 2), (9, 2), (12, 2)],
            "expected_reverse_depth": 4,
        },
        {
            "name": "sparse_four_run_geometry",
            "length": 36,
            "runs": [(4, 2), (12, 2), (20, 2), (28, 2)],
            "expected_reverse_depth": 4,
        },
    ]


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


def run_start_positions(runs):
    return [
        start
        for start, _length in runs
    ]


def run_center_positions(runs):
    return [
        start + ((length - 1) / 2)
        for start, length in runs
    ]


def pairwise_spacings(values):
    if len(values) < 2:
        return []

    return [
        values[index + 1] - values[index]
        for index in range(len(values) - 1)
    ]


def safe_mean(values):
    return mean(values) if values else None


def safe_std(values):
    return pstdev(values) if len(values) > 1 else 0.0


def geometry_features(length, runs):
    run_lengths = [
        run_length
        for _start, run_length in runs
    ]

    starts = run_start_positions(runs)
    centers = run_center_positions(runs)
    spacings = pairwise_spacings(starts)
    center_spacings = pairwise_spacings(centers)

    total_collapse_frames = sum(run_lengths)
    collapse_run_count = len(runs)

    first_start = min(starts) if starts else None
    last_start = max(starts) if starts else None

    span = (
        (last_start - first_start) + 1
        if first_start is not None and last_start is not None
        else 0
    )

    occupied_span = (
        max(start + run_length for start, run_length in runs)
        - min(start for start, _run_length in runs)
        if runs
        else 0
    )

    front_mass = 0
    back_mass = 0

    midpoint = length / 2

    for start, run_length in runs:
        for index in range(start, start + run_length):
            if index < midpoint:
                front_mass += 1
            else:
                back_mass += 1

    front_loading_ratio = (
        front_mass / max(total_collapse_frames, 1)
    )

    back_loading_ratio = (
        back_mass / max(total_collapse_frames, 1)
    )

    density_global = (
        total_collapse_frames / max(length, 1)
    )

    density_span = (
        total_collapse_frames / max(occupied_span, 1)
    )

    run_count_density = (
        collapse_run_count / max(length, 1)
    )

    spacing_mean = safe_mean(spacings)
    spacing_std = safe_std(spacings)

    center_spacing_mean = safe_mean(center_spacings)
    center_spacing_std = safe_std(center_spacings)

    compactness_score = (
        1 / max(spacing_mean, 1)
        if spacing_mean is not None
        else 0.0
    )

    geometry_load_bias = abs(front_loading_ratio - back_loading_ratio)

    return {
        "trajectory_length": length,
        "collapse_run_count": collapse_run_count,
        "run_lengths": run_lengths,
        "total_collapse_frames": total_collapse_frames,
        "collapse_density_global": density_global,
        "collapse_density_span": density_span,
        "run_count_density": run_count_density,
        "run_start_positions": starts,
        "run_center_positions": centers,
        "run_spacing_values": spacings,
        "run_spacing_mean": spacing_mean,
        "run_spacing_std": spacing_std,
        "center_spacing_values": center_spacings,
        "center_spacing_mean": center_spacing_mean,
        "center_spacing_std": center_spacing_std,
        "first_run_start": first_start,
        "last_run_start": last_start,
        "run_start_span": span,
        "occupied_span": occupied_span,
        "front_loading_ratio": front_loading_ratio,
        "back_loading_ratio": back_loading_ratio,
        "geometry_load_bias": geometry_load_bias,
        "compactness_score": compactness_score,
    }


def find_reverse_escape_profile(sequence):
    source_metrics = classify(sequence)

    if source_metrics["classification"] != SOURCE_CLASS:
        raise ValueError(
            "Source sequence must classify as "
            f"{SOURCE_CLASS}, got {source_metrics['classification']}."
        )

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

            if target_metrics["classification"] != TARGET_CLASS:
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

    minimum_reverse_depth = (
        min(hit_depths)
        if hit_depths
        else None
    )

    reverse_example_total = sum(
        target_example_count_by_depth.values()
    )

    return {
        "source_class": SOURCE_CLASS,
        "target_class": TARGET_CLASS,
        "source_metrics": source_metrics,
        "checked_by_depth": checked_by_depth,
        "target_example_count_by_depth": target_example_count_by_depth,
        "minimum_reverse_depth": minimum_reverse_depth,
        "reverse_example_total": reverse_example_total,
        "example_by_depth": example_by_depth,
    }


def pearson_correlation(xs, ys):
    if len(xs) != len(ys) or len(xs) < 2:
        return None

    mean_x = mean(xs)
    mean_y = mean(ys)

    numerator = sum(
        (x - mean_x) * (y - mean_y)
        for x, y in zip(xs, ys)
    )

    denominator_x = sum(
        (x - mean_x) ** 2
        for x in xs
    )

    denominator_y = sum(
        (y - mean_y) ** 2
        for y in ys
    )

    denominator = (denominator_x * denominator_y) ** 0.5

    if denominator == 0:
        return None

    return numerator / denominator


def binary_group_stats(records, key):
    depth3_values = [
        record["features"][key]
        for record in records
        if record["minimum_reverse_depth"] == 3
        and record["features"][key] is not None
    ]

    depth4_values = [
        record["features"][key]
        for record in records
        if record["minimum_reverse_depth"] == 4
        and record["features"][key] is not None
    ]

    return {
        "feature": key,
        "depth3_mean": safe_mean(depth3_values),
        "depth3_std": safe_std(depth3_values),
        "depth4_mean": safe_mean(depth4_values),
        "depth4_std": safe_std(depth4_values),
        "mean_difference_depth4_minus_depth3": (
            safe_mean(depth4_values) - safe_mean(depth3_values)
            if depth3_values and depth4_values
            else None
        ),
        "depth3_values": depth3_values,
        "depth4_values": depth4_values,
    }


def infer_depth_rule(features):
    collapse_run_count = features["collapse_run_count"]

    if collapse_run_count >= 4:
        return 4

    return 3


def build_geometry_records():
    records = []

    for variant_index, spec in enumerate(geometry_specs()):
        sequence = make_sequence(
            spec["length"],
            spec["runs"],
        )

        metrics = classify(sequence)

        if metrics["classification"] != SOURCE_CLASS:
            raise ValueError(
                f"{spec['name']} classified as "
                f"{metrics['classification']}, expected {SOURCE_CLASS}."
            )

        features = geometry_features(
            spec["length"],
            spec["runs"],
        )

        escape_profile = find_reverse_escape_profile(sequence)

        minimum_reverse_depth = escape_profile["minimum_reverse_depth"]

        predicted_depth_rule = infer_depth_rule(features)

        record = {
            "variant_index": variant_index,
            "geometry_name": spec["name"],
            "trajectory_length": spec["length"],
            "runs": spec["runs"],
            "raw_action_sequence": sequence,
            "source_classification": metrics,
            "features": features,
            "expected_reverse_depth": spec["expected_reverse_depth"],
            "predicted_reverse_depth_rule": predicted_depth_rule,
            "minimum_reverse_depth": minimum_reverse_depth,
            "reverse_depth_matched_expected": (
                minimum_reverse_depth == spec["expected_reverse_depth"]
            ),
            "reverse_depth_matched_rule": (
                minimum_reverse_depth == predicted_depth_rule
            ),
            "reverse_example_total": (
                escape_profile["reverse_example_total"]
            ),
            "reverse_example_count_by_depth": (
                escape_profile["target_example_count_by_depth"]
            ),
            "checked_by_depth": escape_profile["checked_by_depth"],
        }

        records.append(record)

    return records


def summarize_geometry_sensitivity(records):
    reverse_depths = [
        record["minimum_reverse_depth"]
        for record in records
    ]

    expected_depths = [
        record["expected_reverse_depth"]
        for record in records
    ]

    predicted_depths = [
        record["predicted_reverse_depth_rule"]
        for record in records
    ]

    matched_expected_count = sum(
        1
        for record in records
        if record["reverse_depth_matched_expected"]
    )

    matched_rule_count = sum(
        1
        for record in records
        if record["reverse_depth_matched_rule"]
    )

    depth3_records = [
        record
        for record in records
        if record["minimum_reverse_depth"] == 3
    ]

    depth4_records = [
        record
        for record in records
        if record["minimum_reverse_depth"] == 4
    ]

    feature_keys = [
        "trajectory_length",
        "collapse_run_count",
        "total_collapse_frames",
        "collapse_density_global",
        "collapse_density_span",
        "run_count_density",
        "run_spacing_mean",
        "run_spacing_std",
        "center_spacing_mean",
        "center_spacing_std",
        "run_start_span",
        "occupied_span",
        "front_loading_ratio",
        "back_loading_ratio",
        "geometry_load_bias",
        "compactness_score",
    ]

    feature_group_stats = {
        key: binary_group_stats(records, key)
        for key in feature_keys
    }

    feature_correlations = {}

    for key in feature_keys:
        xs = [
            record["features"][key]
            for record in records
            if record["features"][key] is not None
        ]

        ys = [
            record["minimum_reverse_depth"]
            for record in records
            if record["features"][key] is not None
        ]

        feature_correlations[key] = pearson_correlation(xs, ys)

    strongest_feature = None
    strongest_abs_corr = -1

    for key, value in feature_correlations.items():
        if value is None:
            continue

        abs_corr = abs(value)

        if abs_corr > strongest_abs_corr:
            strongest_abs_corr = abs_corr
            strongest_feature = key

    run_count_rule_accuracy = (
        matched_rule_count / len(records)
        if records
        else 0.0
    )

    expected_match_rate = (
        matched_expected_count / len(records)
        if records
        else 0.0
    )

    reverse_depth_std = (
        pstdev(reverse_depths)
        if len(reverse_depths) > 1
        else 0.0
    )

    geometry_sensitivity_index = (
        reverse_depth_std
        + (1.0 - run_count_rule_accuracy)
        + (len(set(reverse_depths)) - 1)
    )

    run_count_depth4_alignment = all(
        record["features"]["collapse_run_count"] >= 4
        for record in depth4_records
    )

    run_count_depth3_alignment = all(
        record["features"]["collapse_run_count"] == 3
        for record in depth3_records
    )

    simple_rule_confirmed = (
        run_count_rule_accuracy == 1.0
        and run_count_depth4_alignment
        and run_count_depth3_alignment
    )

    return {
        "record_count": len(records),
        "reverse_depths": reverse_depths,
        "expected_reverse_depths": expected_depths,
        "predicted_reverse_depths": predicted_depths,
        "reverse_depth_values": sorted(set(reverse_depths)),
        "reverse_depth_mean": mean(reverse_depths),
        "reverse_depth_std": reverse_depth_std,
        "depth3_count": len(depth3_records),
        "depth4_count": len(depth4_records),
        "depth3_geometries": [
            record["geometry_name"]
            for record in depth3_records
        ],
        "depth4_geometries": [
            record["geometry_name"]
            for record in depth4_records
        ],
        "matched_expected_count": matched_expected_count,
        "expected_match_rate": expected_match_rate,
        "matched_rule_count": matched_rule_count,
        "run_count_rule_accuracy": run_count_rule_accuracy,
        "run_count_depth4_alignment": run_count_depth4_alignment,
        "run_count_depth3_alignment": run_count_depth3_alignment,
        "simple_rule_confirmed": simple_rule_confirmed,
        "feature_group_stats": feature_group_stats,
        "feature_correlations": feature_correlations,
        "strongest_feature": strongest_feature,
        "strongest_abs_correlation": strongest_abs_corr,
        "geometry_sensitivity_index": geometry_sensitivity_index,
        "inferred_rule": (
            "minimum_reverse_depth = 4 when collapse_run_count >= 4; "
            "otherwise minimum_reverse_depth = 3"
        ),
    }


def main():
    records = build_geometry_records()
    sensitivity = summarize_geometry_sensitivity(records)

    summary = {
        "variant_count": len(records),
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "max_mutation_depth": MAX_MUTATION_DEPTH,
        "source_class": SOURCE_CLASS,
        "target_class": TARGET_CLASS,
        "reverse_depth_values": (
            sensitivity["reverse_depth_values"]
        ),
        "reverse_depths": sensitivity["reverse_depths"],
        "reverse_depth_mean": sensitivity["reverse_depth_mean"],
        "reverse_depth_std": sensitivity["reverse_depth_std"],
        "depth3_count": sensitivity["depth3_count"],
        "depth4_count": sensitivity["depth4_count"],
        "depth3_geometries": sensitivity["depth3_geometries"],
        "depth4_geometries": sensitivity["depth4_geometries"],
        "simple_rule_confirmed": (
            sensitivity["simple_rule_confirmed"]
        ),
        "inferred_rule": sensitivity["inferred_rule"],
        "run_count_rule_accuracy": (
            sensitivity["run_count_rule_accuracy"]
        ),
        "strongest_feature": sensitivity["strongest_feature"],
        "strongest_abs_correlation": (
            sensitivity["strongest_abs_correlation"]
        ),
        "geometry_sensitivity_index": (
            sensitivity["geometry_sensitivity_index"]
        ),
        "expected_match_rate": sensitivity["expected_match_rate"],
    }

    status = (
        "PASS"
        if (
            sensitivity["simple_rule_confirmed"]
            and sensitivity["expected_match_rate"] == 1.0
            and sensitivity["run_count_rule_accuracy"] == 1.0
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_geometry_sensitivity_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "geometry_sensitivity_summary": sensitivity,
        "geometry_records": records,
        "interpretation": (
            "This experiment measures which trajectory-geometry "
            "features control reverse escape depth from "
            "FRAGMENTED_LOCAL_COLLAPSE to OSCILLATING_NONPERSISTENT."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_geometry_sensitivity_v0.py"
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
        "Temporal Collapse Topology Geometry Sensitivity v0"
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
    print("Geometry records")
    print("-" * 80)

    for record in records:
        features = record["features"]

        print(
            f"variant={record['variant_index']} "
            f"geometry={record['geometry_name']} "
            f"runs={features['collapse_run_count']} "
            f"length={features['trajectory_length']} "
            f"density={features['collapse_density_global']} "
            f"spacing_mean={features['run_spacing_mean']} "
            f"span_density={features['collapse_density_span']} "
            f"front_ratio={features['front_loading_ratio']} "
            f"reverse_depth={record['minimum_reverse_depth']} "
            f"expected={record['expected_reverse_depth']} "
            f"rule={record['predicted_reverse_depth_rule']} "
            f"examples={record['reverse_example_total']}"
        )

    print()
    print("Feature correlations with reverse depth")
    print("-" * 80)

    for key, value in sensitivity["feature_correlations"].items():
        print(f"{key:<32} corr={value}")

    print()
    print("Feature group stats")
    print("-" * 80)

    for key, values in sensitivity["feature_group_stats"].items():
        print(
            f"{key:<32} "
            f"depth3_mean={values['depth3_mean']} "
            f"depth4_mean={values['depth4_mean']} "
            f"diff={values['mean_difference_depth4_minus_depth3']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - geometry-to-reversibility mapping detected: "
            "collapse_run_count controlled the reverse escape depth "
            "shift from 3 to 4 under tested geometries."
        )
    else:
        print(
            "CHECK - geometry-to-reversibility mapping was not fully "
            "resolved under tested geometries."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()