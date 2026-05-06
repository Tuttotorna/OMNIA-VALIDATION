import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_threshold_sensitivity_v0.json"
)

CONFIRMATION_WINDOWS = [2, 3, 4]
PERSISTENCE_WINDOW = 2

SUPPORTED_CLASSES = [
    "GLOBAL_PERSISTENT_COLLAPSE",
    "RECOVERY_RELAPSE_COLLAPSE",
    "FRAGMENTED_LOCAL_COLLAPSE",
    "OSCILLATING_NONPERSISTENT",
    "SPIKE_FILTERED",
    "CLEAN_PASS",
]

TARGET_CLASS = "OSCILLATING_NONPERSISTENT"

FRAME_VALUES = [
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


def classify(sequence, confirmation_window):
    persistence_threshold = confirmation_window + PERSISTENCE_WINDOW

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
        if length >= confirmation_window
    )

    persistence_reset_count = max(
        collapse_run_count - 1,
        0,
    )

    fragmentation_index = (
        persistence_reset_count / max(collapse_run_count, 1)
    )

    global_persistence_detected = any(
        length >= persistence_threshold
        for length in run_lengths
    )

    if collapse_run_count == 0:
        label = "CLEAN_PASS"

    elif (
        collapse_run_count == 1
        and max_run_length < confirmation_window
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
        "confirmation_window": confirmation_window,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": persistence_threshold,
        "collapse_run_count": collapse_run_count,
        "run_lengths": run_lengths,
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


def threshold_sensitivity_specs():
    return [
        {
            "name": "three_runs_len_2",
            "length": 28,
            "runs": [(5, 2), (12, 2), (19, 2)],
        },
        {
            "name": "three_runs_len_3",
            "length": 34,
            "runs": [(5, 3), (14, 3), (23, 3)],
        },
        {
            "name": "three_runs_len_4",
            "length": 40,
            "runs": [(5, 4), (16, 4), (27, 4)],
        },
        {
            "name": "four_runs_len_2",
            "length": 34,
            "runs": [(4, 2), (10, 2), (16, 2), (22, 2)],
        },
        {
            "name": "four_runs_len_3",
            "length": 42,
            "runs": [(4, 3), (13, 3), (22, 3), (31, 3)],
        },
        {
            "name": "four_runs_len_4",
            "length": 48,
            "runs": [(4, 4), (15, 4), (26, 4), (37, 4)],
        },
        {
            "name": "mixed_2_3_4",
            "length": 40,
            "runs": [(5, 2), (14, 3), (25, 4)],
        },
        {
            "name": "mixed_1_2_3_4",
            "length": 44,
            "runs": [(4, 1), (10, 2), (18, 3), (28, 4)],
        },
        {
            "name": "long_single_run",
            "length": 30,
            "runs": [(8, 7)],
        },
        {
            "name": "relapse_two_long_runs",
            "length": 40,
            "runs": [(6, 5), (24, 5)],
        },
        {
            "name": "all_spikes_len_1",
            "length": 32,
            "runs": [(4, 1), (8, 1), (12, 1), (16, 1), (20, 1)],
        },
        {
            "name": "mixed_threshold_boundary",
            "length": 46,
            "runs": [(5, 2), (13, 3), (23, 4), (35, 5)],
        },
    ]


def safe_mean(values):
    return mean(values) if values else None


def safe_std(values):
    return pstdev(values) if len(values) > 1 else 0.0


def pairwise_spacings(values):
    if len(values) < 2:
        return []

    return [
        values[index + 1] - values[index]
        for index in range(len(values) - 1)
    ]


def geometry_features(length, runs):
    run_lengths = [
        run_length
        for _start, run_length in runs
    ]

    starts = [
        start
        for start, _run_length in runs
    ]

    total_collapse_frames = sum(run_lengths)
    collapse_run_count = len(runs)

    spacings = pairwise_spacings(starts)

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

    return {
        "trajectory_length": length,
        "collapse_run_count": collapse_run_count,
        "run_lengths": run_lengths,
        "run_length_mean": safe_mean(run_lengths),
        "run_length_std": safe_std(run_lengths),
        "max_run_length": max(run_lengths) if run_lengths else 0,
        "min_run_length": min(run_lengths) if run_lengths else 0,
        "total_collapse_frames": total_collapse_frames,
        "collapse_density_global": (
            total_collapse_frames / max(length, 1)
        ),
        "collapse_density_span": (
            total_collapse_frames / max(occupied_span, 1)
        ),
        "run_count_density": (
            collapse_run_count / max(length, 1)
        ),
        "run_start_positions": starts,
        "run_spacing_values": spacings,
        "run_spacing_mean": safe_mean(spacings),
        "run_spacing_std": safe_std(spacings),
        "occupied_span": occupied_span,
        "front_loading_ratio": front_loading_ratio,
        "back_loading_ratio": back_loading_ratio,
        "geometry_load_bias": abs(
            front_loading_ratio - back_loading_ratio
        ),
        "mass_per_run": (
            total_collapse_frames / max(collapse_run_count, 1)
        ),
    }


def thresholded_reducible_mass(runs, confirmation_window):
    threshold_below_confirmation = confirmation_window - 1

    return sum(
        max(0, run_length - threshold_below_confirmation)
        for _start, run_length in runs
    )


def predicted_target_after_threshold_escape(runs, confirmation_window):
    threshold_below_confirmation = confirmation_window - 1

    reduced_lengths = [
        min(run_length, threshold_below_confirmation)
        for _start, run_length in runs
    ]

    nonzero_runs = [
        length
        for length in reduced_lengths
        if length > 0
    ]

    if len(nonzero_runs) == 0:
        return "CLEAN_PASS"

    if len(nonzero_runs) == 1:
        if nonzero_runs[0] < confirmation_window:
            return "SPIKE_FILTERED"

    if all(length < confirmation_window for length in nonzero_runs):
        return "OSCILLATING_NONPERSISTENT"

    return "UNRESOLVED"


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


def build_records():
    records = []

    for variant_index, spec in enumerate(threshold_sensitivity_specs()):
        sequence = make_sequence(
            spec["length"],
            spec["runs"],
        )

        features = geometry_features(
            spec["length"],
            spec["runs"],
        )

        threshold_results = []

        for confirmation_window in CONFIRMATION_WINDOWS:
            source_metrics = classify(
                sequence,
                confirmation_window,
            )

            minimum_target_depth = thresholded_reducible_mass(
                spec["runs"],
                confirmation_window,
            )

            predicted_target = predicted_target_after_threshold_escape(
                spec["runs"],
                confirmation_window,
            )

            formula_target_matches = (
                predicted_target == TARGET_CLASS
            )

            threshold_results.append({
                "confirmation_window": confirmation_window,
                "persistence_window": PERSISTENCE_WINDOW,
                "global_persistence_threshold": (
                    confirmation_window + PERSISTENCE_WINDOW
                ),
                "source_class": source_metrics["classification"],
                "source_metrics": source_metrics,
                "minimum_target_depth": minimum_target_depth,
                "predicted_target_after_minimal_escape": predicted_target,
                "target_reachable_by_formula": formula_target_matches,
                "analytical_rule": (
                    "minimum_target_depth = "
                    "sum(max(0, run_length - "
                    "(confirmation_window - 1)))"
                ),
            })

        records.append({
            "variant_index": variant_index,
            "geometry_name": spec["name"],
            "trajectory_length": spec["length"],
            "runs": spec["runs"],
            "raw_action_sequence": sequence,
            "features": features,
            "threshold_results": threshold_results,
            "method": "threshold_parametric_analytical_rule",
        })

    return records


def flatten_threshold_records(records):
    flat = []

    for record in records:
        for item in record["threshold_results"]:
            flat.append({
                "variant_index": record["variant_index"],
                "geometry_name": record["geometry_name"],
                "features": record["features"],
                "runs": record["runs"],
                "confirmation_window": item["confirmation_window"],
                "source_class": item["source_class"],
                "minimum_target_depth": item["minimum_target_depth"],
                "predicted_target_after_minimal_escape": (
                    item["predicted_target_after_minimal_escape"]
                ),
                "target_reachable_by_formula": (
                    item["target_reachable_by_formula"]
                ),
            })

    return flat


def summarize_by_threshold(flat_records):
    summary = {}

    for confirmation_window in CONFIRMATION_WINDOWS:
        items = [
            item
            for item in flat_records
            if item["confirmation_window"] == confirmation_window
        ]

        depths = [
            item["minimum_target_depth"]
            for item in items
        ]

        source_classes = [
            item["source_class"]
            for item in items
        ]

        target_matches = [
            item["target_reachable_by_formula"]
            for item in items
        ]

        class_counts = {}

        for class_name in source_classes:
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        summary[str(confirmation_window)] = {
            "confirmation_window": confirmation_window,
            "record_count": len(items),
            "minimum_target_depths": depths,
            "minimum_target_depth_values": sorted(set(depths)),
            "minimum_target_depth_mean": safe_mean(depths),
            "minimum_target_depth_std": safe_std(depths),
            "source_class_counts": class_counts,
            "target_reachable_count": sum(
                1 for value in target_matches if value
            ),
            "target_reachable_rate": (
                sum(1 for value in target_matches if value)
                / max(len(target_matches), 1)
            ),
        }

    return summary


def summarize_by_geometry(records):
    geometry_summary = {}

    for record in records:
        depths = [
            item["minimum_target_depth"]
            for item in record["threshold_results"]
        ]

        classes = [
            item["source_class"]
            for item in record["threshold_results"]
        ]

        depth_by_threshold = {
            str(item["confirmation_window"]): item["minimum_target_depth"]
            for item in record["threshold_results"]
        }

        class_by_threshold = {
            str(item["confirmation_window"]): item["source_class"]
            for item in record["threshold_results"]
        }

        monotonic_nonincreasing = all(
            depths[index + 1] <= depths[index]
            for index in range(len(depths) - 1)
        )

        geometry_summary[record["geometry_name"]] = {
            "variant_index": record["variant_index"],
            "depths_by_threshold": depth_by_threshold,
            "classes_by_threshold": class_by_threshold,
            "depth_values": depths,
            "class_values": classes,
            "depth_monotonic_nonincreasing": monotonic_nonincreasing,
            "depth_drop_2_to_4": (
                depth_by_threshold["2"] - depth_by_threshold["4"]
            ),
            "features": record["features"],
        }

    return geometry_summary


def feature_correlations(flat_records):
    feature_keys = [
        "trajectory_length",
        "collapse_run_count",
        "run_length_mean",
        "run_length_std",
        "max_run_length",
        "min_run_length",
        "total_collapse_frames",
        "collapse_density_global",
        "collapse_density_span",
        "run_count_density",
        "run_spacing_mean",
        "run_spacing_std",
        "occupied_span",
        "front_loading_ratio",
        "back_loading_ratio",
        "geometry_load_bias",
        "mass_per_run",
    ]

    correlations = {}

    for confirmation_window in CONFIRMATION_WINDOWS:
        items = [
            item
            for item in flat_records
            if item["confirmation_window"] == confirmation_window
        ]

        threshold_corrs = {}

        for key in feature_keys:
            xs = [
                item["features"][key]
                for item in items
                if item["features"][key] is not None
            ]

            ys = [
                item["minimum_target_depth"]
                for item in items
                if item["features"][key] is not None
            ]

            threshold_corrs[key] = pearson_correlation(xs, ys)

        correlations[str(confirmation_window)] = threshold_corrs

    return correlations


def validate_parametric_rule(records):
    failures = []

    for record in records:
        run_lengths = [
            run_length
            for _start, run_length in record["runs"]
        ]

        for item in record["threshold_results"]:
            confirmation_window = item["confirmation_window"]

            expected_depth = sum(
                max(0, run_length - (confirmation_window - 1))
                for run_length in run_lengths
            )

            if expected_depth != item["minimum_target_depth"]:
                failures.append({
                    "geometry_name": record["geometry_name"],
                    "confirmation_window": confirmation_window,
                    "expected_depth": expected_depth,
                    "observed_depth": item["minimum_target_depth"],
                })

    return {
        "parametric_rule_holds": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
    }


def summarize(records):
    flat = flatten_threshold_records(records)

    by_threshold = summarize_by_threshold(flat)
    by_geometry = summarize_by_geometry(records)
    correlations = feature_correlations(flat)
    rule_validation = validate_parametric_rule(records)

    monotonic_count = sum(
        1
        for item in by_geometry.values()
        if item["depth_monotonic_nonincreasing"]
    )

    all_depths_monotonic = (
        monotonic_count == len(by_geometry)
    )

    class_transition_count = sum(
        1
        for item in by_geometry.values()
        if len(set(item["class_values"])) > 1
    )

    depth_values_all = [
        item["minimum_target_depth"]
        for item in flat
    ]

    target_reachable_count = sum(
        1
        for item in flat
        if item["target_reachable_by_formula"]
    )

    strongest_features_by_threshold = {}

    for threshold, corr_map in correlations.items():
        strongest_feature = None
        strongest_abs_corr = -1

        for key, value in corr_map.items():
            if value is None:
                continue

            abs_corr = abs(value)

            if abs_corr > strongest_abs_corr:
                strongest_abs_corr = abs_corr
                strongest_feature = key

        strongest_features_by_threshold[threshold] = {
            "strongest_feature": strongest_feature,
            "strongest_abs_correlation": strongest_abs_corr,
        }

    threshold_parametric_law_detected = (
        rule_validation["parametric_rule_holds"]
        and all_depths_monotonic
        and target_reachable_count == len(flat)
    )

    return {
        "record_count": len(records),
        "flat_record_count": len(flat),
        "thresholds": CONFIRMATION_WINDOWS,
        "target_class": TARGET_CLASS,
        "depth_values_all": sorted(set(depth_values_all)),
        "target_reachable_count": target_reachable_count,
        "target_reachable_rate": (
            target_reachable_count / max(len(flat), 1)
        ),
        "by_threshold": by_threshold,
        "by_geometry": by_geometry,
        "feature_correlations_by_threshold": correlations,
        "strongest_features_by_threshold": strongest_features_by_threshold,
        "all_depths_monotonic_nonincreasing": all_depths_monotonic,
        "monotonic_geometry_count": monotonic_count,
        "class_transition_count": class_transition_count,
        "parametric_rule_validation": rule_validation,
        "threshold_parametric_law_detected": (
            threshold_parametric_law_detected
        ),
        "generalized_rule": (
            "minimum_target_depth = "
            "sum(max(0, run_length - "
            "(confirmation_window - 1)))"
        ),
    }


def compact_record(record):
    return {
        "variant_index": record["variant_index"],
        "geometry_name": record["geometry_name"],
        "trajectory_length": record["trajectory_length"],
        "runs": record["runs"],
        "features": record["features"],
        "threshold_results": [
            {
                "confirmation_window": item["confirmation_window"],
                "global_persistence_threshold": (
                    item["global_persistence_threshold"]
                ),
                "source_class": item["source_class"],
                "minimum_target_depth": item["minimum_target_depth"],
                "predicted_target_after_minimal_escape": (
                    item["predicted_target_after_minimal_escape"]
                ),
                "target_reachable_by_formula": (
                    item["target_reachable_by_formula"]
                ),
            }
            for item in record["threshold_results"]
        ],
        "method": record["method"],
    }


def main():
    records = build_records()
    analysis = summarize(records)

    status = (
        "PASS"
        if analysis["threshold_parametric_law_detected"]
        else "CHECK"
    )

    summary = {
        "variant_count": len(records),
        "flat_record_count": analysis["flat_record_count"],
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_windows": CONFIRMATION_WINDOWS,
        "persistence_window": PERSISTENCE_WINDOW,
        "target_class": TARGET_CLASS,
        "depth_values_all": analysis["depth_values_all"],
        "target_reachable_rate": analysis["target_reachable_rate"],
        "all_depths_monotonic_nonincreasing": (
            analysis["all_depths_monotonic_nonincreasing"]
        ),
        "class_transition_count": analysis["class_transition_count"],
        "parametric_rule_holds": (
            analysis["parametric_rule_validation"][
                "parametric_rule_holds"
            ]
        ),
        "threshold_parametric_law_detected": (
            analysis["threshold_parametric_law_detected"]
        ),
        "generalized_rule": analysis["generalized_rule"],
        "method": "threshold_parametric_analytical_rule",
    }

    payload = {
        "experiment": (
            "temporal_collapse_topology_threshold_sensitivity_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "threshold_sensitivity_summary": analysis,
        "geometry_records": [
            compact_record(record)
            for record in records
        ],
        "interpretation": (
            "This experiment tests whether the reducible-collapse-mass "
            "rule remains coherent when CONFIRMATION_WINDOW changes."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_threshold_sensitivity_v0.py"
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
        "Temporal Collapse Topology Threshold Sensitivity v0"
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
    print("By threshold")
    print("-" * 80)

    for threshold, values in analysis["by_threshold"].items():
        print(
            f"confirmation_window={threshold} "
            f"depth_values={values['minimum_target_depth_values']} "
            f"mean_depth={values['minimum_target_depth_mean']} "
            f"std={values['minimum_target_depth_std']} "
            f"class_counts={values['source_class_counts']} "
            f"target_rate={values['target_reachable_rate']}"
        )

    print()
    print("Geometry records")
    print("-" * 80)

    for record in records:
        depth_map = {
            item["confirmation_window"]: item["minimum_target_depth"]
            for item in record["threshold_results"]
        }

        class_map = {
            item["confirmation_window"]: item["source_class"]
            for item in record["threshold_results"]
        }

        print(
            f"variant={record['variant_index']} "
            f"geometry={record['geometry_name']} "
            f"runs={record['features']['run_lengths']} "
            f"mass={record['features']['total_collapse_frames']} "
            f"depths={depth_map} "
            f"classes={class_map}"
        )

    print()
    print("Strongest features by threshold")
    print("-" * 80)

    for threshold, values in (
        analysis["strongest_features_by_threshold"].items()
    ):
        print(
            f"confirmation_window={threshold} "
            f"strongest_feature={values['strongest_feature']} "
            f"abs_corr={values['strongest_abs_correlation']}"
        )

    print()
    print("Rule validation")
    print("-" * 80)

    rule_validation = analysis["parametric_rule_validation"]

    print("parametric_rule_holds:", rule_validation["parametric_rule_holds"])
    print("failure_count:", rule_validation["failure_count"])

    if rule_validation["failures"]:
        print("failures:", rule_validation["failures"])

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - threshold-parametric reversibility law detected: "
            "minimum target depth followed the generalized "
            "thresholded reducible-collapse-mass rule."
        )
    else:
        print(
            "CHECK - threshold-parametric reversibility law was not "
            "fully confirmed under tested thresholds."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()