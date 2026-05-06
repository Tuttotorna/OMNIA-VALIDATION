import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.2.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_variable_run_length_v0.json"
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

SOURCE_CLASS_FOCUS = "FRAGMENTED_LOCAL_COLLAPSE"
TARGET_CLASS = "OSCILLATING_NONPERSISTENT"


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


def variable_run_length_specs():
    return [
        {
            "name": "three_runs_mass_6_baseline",
            "length": 26,
            "runs": [(5, 2), (11, 2), (17, 2)],
        },
        {
            "name": "three_runs_mass_9_variable",
            "length": 32,
            "runs": [(5, 3), (13, 3), (21, 3)],
        },
        {
            "name": "three_runs_mass_12_long",
            "length": 38,
            "runs": [(5, 4), (16, 4), (27, 4)],
        },
        {
            "name": "four_runs_mass_4_spikes",
            "length": 26,
            "runs": [(4, 1), (8, 1), (12, 1), (16, 1)],
        },
        {
            "name": "four_runs_mass_8_baseline",
            "length": 30,
            "runs": [(4, 2), (9, 2), (14, 2), (19, 2)],
        },
        {
            "name": "four_runs_mass_12_variable",
            "length": 40,
            "runs": [(4, 3), (13, 3), (22, 3), (31, 3)],
        },
        {
            "name": "two_runs_mass_8_relapse_like",
            "length": 28,
            "runs": [(4, 2), (16, 6)],
        },
        {
            "name": "six_runs_mass_6_spike_family",
            "length": 32,
            "runs": [(3, 1), (7, 1), (11, 1), (15, 1), (19, 1), (23, 1)],
        },
        {
            "name": "five_runs_mass_10_fragmented",
            "length": 42,
            "runs": [(4, 2), (11, 2), (18, 2), (25, 2), (32, 2)],
        },
        {
            "name": "three_runs_mass_8_mixed",
            "length": 34,
            "runs": [(5, 2), (14, 3), (24, 3)],
        },
        {
            "name": "four_runs_mass_7_mixed",
            "length": 34,
            "runs": [(4, 2), (10, 1), (16, 2), (22, 2)],
        },
        {
            "name": "four_runs_mass_10_mixed",
            "length": 42,
            "runs": [(4, 3), (13, 2), (22, 3), (31, 2)],
        },
        {
            "name": "same_mass_8_three_runs",
            "length": 36,
            "runs": [(5, 2), (14, 3), (24, 3)],
        },
        {
            "name": "same_mass_8_four_runs",
            "length": 36,
            "runs": [(4, 2), (11, 2), (18, 2), (25, 2)],
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


def analytical_minimum_depth_to_oscillating(runs):
    """
    Exact shortcut for this classifier.

    To reach OSCILLATING_NONPERSISTENT from a collapse-run sequence,
    all collapse runs must be reduced below CONFIRMATION_WINDOW.

    With CONFIRMATION_WINDOW = 2, each run must become length <= 1.

    Minimum edits needed:
        sum(max(0, run_length - 1))

    If the sequence is already OSCILLATING_NONPERSISTENT, depth = 0.
    """

    run_lengths = [
        run_length
        for _start, run_length in runs
    ]

    if not run_lengths:
        return None

    already_oscillating = (
        len(run_lengths) >= 2
        and all(length < CONFIRMATION_WINDOW for length in run_lengths)
    )

    if already_oscillating:
        return 0

    return sum(
        max(0, run_length - (CONFIRMATION_WINDOW - 1))
        for run_length in run_lengths
    )


def predicted_class_after_minimal_escape(runs):
    escaped_lengths = [
        min(run_length, CONFIRMATION_WINDOW - 1)
        for _start, run_length in runs
    ]

    nonzero_runs = [
        length
        for length in escaped_lengths
        if length > 0
    ]

    if len(nonzero_runs) == 0:
        return "CLEAN_PASS"

    if len(nonzero_runs) == 1:
        return "SPIKE_FILTERED"

    if all(length < CONFIRMATION_WINDOW for length in nonzero_runs):
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

    for variant_index, spec in enumerate(variable_run_length_specs()):
        sequence = make_sequence(
            spec["length"],
            spec["runs"],
        )

        source_metrics = classify(sequence)

        features = geometry_features(
            spec["length"],
            spec["runs"],
        )

        analytical_depth = analytical_minimum_depth_to_oscillating(
            spec["runs"],
        )

        predicted_target = predicted_class_after_minimal_escape(
            spec["runs"],
        )

        record = {
            "variant_index": variant_index,
            "geometry_name": spec["name"],
            "trajectory_length": spec["length"],
            "runs": spec["runs"],
            "raw_action_sequence": sequence,
            "source_class": source_metrics["classification"],
            "source_metrics": source_metrics,
            "features": features,
            "target_class": TARGET_CLASS,
            "minimum_target_depth": analytical_depth,
            "predicted_target_after_minimal_escape": predicted_target,
            "target_reachable_by_formula": (
                predicted_target == TARGET_CLASS
            ),
            "target_example_total": None,
            "method": "analytical_minimum_depth_no_bruteforce",
        }

        records.append(record)

    return records


def feature_correlations(records, feature_keys):
    correlations = {}

    usable_records = [
        record
        for record in records
        if record["minimum_target_depth"] is not None
        and record["target_reachable_by_formula"]
    ]

    for key in feature_keys:
        xs = [
            record["features"][key]
            for record in usable_records
            if record["features"][key] is not None
        ]

        ys = [
            record["minimum_target_depth"]
            for record in usable_records
            if record["features"][key] is not None
        ]

        correlations[key] = pearson_correlation(xs, ys)

    return correlations


def grouped_by_source_class(records):
    grouped = {}

    for record in records:
        source_class = record["source_class"]

        if source_class not in grouped:
            grouped[source_class] = []

        grouped[source_class].append(record)

    summary = {}

    for source_class, items in grouped.items():
        depths = [
            item["minimum_target_depth"]
            for item in items
            if item["minimum_target_depth"] is not None
        ]

        run_counts = [
            item["features"]["collapse_run_count"]
            for item in items
        ]

        collapse_masses = [
            item["features"]["total_collapse_frames"]
            for item in items
        ]

        summary[source_class] = {
            "record_count": len(items),
            "minimum_target_depths": depths,
            "minimum_target_depth_mean": safe_mean(depths),
            "minimum_target_depth_std": safe_std(depths),
            "collapse_run_counts": run_counts,
            "total_collapse_frames": collapse_masses,
            "geometry_names": [
                item["geometry_name"]
                for item in items
            ],
        }

    return summary


def compare_same_run_count(records):
    groups = {}

    for record in records:
        key = record["features"]["collapse_run_count"]

        if key not in groups:
            groups[key] = []

        groups[key].append(record)

    comparison = {}

    for run_count, items in groups.items():
        depths = [
            item["minimum_target_depth"]
            for item in items
            if item["minimum_target_depth"] is not None
        ]

        masses = [
            item["features"]["total_collapse_frames"]
            for item in items
        ]

        run_lengths = [
            item["features"]["run_lengths"]
            for item in items
        ]

        comparison[str(run_count)] = {
            "collapse_run_count": run_count,
            "record_count": len(items),
            "geometry_names": [
                item["geometry_name"]
                for item in items
            ],
            "total_collapse_frames": masses,
            "run_lengths": run_lengths,
            "minimum_target_depths": depths,
            "depth_values": sorted(set(depths)),
            "depth_stable_within_run_count": (
                len(set(depths)) == 1
                if depths
                else False
            ),
        }

    return comparison


def compare_same_mass(records):
    groups = {}

    for record in records:
        key = record["features"]["total_collapse_frames"]

        if key not in groups:
            groups[key] = []

        groups[key].append(record)

    comparison = {}

    for mass, items in groups.items():
        if len(items) < 2:
            continue

        depths = [
            item["minimum_target_depth"]
            for item in items
            if item["minimum_target_depth"] is not None
        ]

        run_counts = [
            item["features"]["collapse_run_count"]
            for item in items
        ]

        comparison[str(mass)] = {
            "total_collapse_frames": mass,
            "record_count": len(items),
            "geometry_names": [
                item["geometry_name"]
                for item in items
            ],
            "collapse_run_counts": run_counts,
            "minimum_target_depths": depths,
            "depth_values": sorted(set(depths)),
            "depth_stable_within_mass": (
                len(set(depths)) == 1
                if depths
                else False
            ),
        }

    return comparison


def summarize(records):
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

    correlations = feature_correlations(records, feature_keys)

    strongest_feature = None
    strongest_abs_corr = -1

    for key, value in correlations.items():
        if value is None:
            continue

        abs_corr = abs(value)

        if abs_corr > strongest_abs_corr:
            strongest_abs_corr = abs_corr
            strongest_feature = key

    same_run_count = compare_same_run_count(records)
    same_mass = compare_same_mass(records)

    source_class_summary = grouped_by_source_class(records)

    same_run_count_depth_varies = any(
        not value["depth_stable_within_run_count"]
        for value in same_run_count.values()
        if value["record_count"] >= 2
    )

    same_mass_depth_varies = any(
        not value["depth_stable_within_mass"]
        for value in same_mass.values()
    )

    reachable_records = [
        record
        for record in records
        if record["target_reachable_by_formula"]
    ]

    depths = [
        record["minimum_target_depth"]
        for record in reachable_records
        if record["minimum_target_depth"] is not None
    ]

    run_counts = [
        record["features"]["collapse_run_count"]
        for record in reachable_records
    ]

    masses = [
        record["features"]["total_collapse_frames"]
        for record in reachable_records
    ]

    run_count_corr = correlations.get("collapse_run_count")
    mass_corr = correlations.get("total_collapse_frames")

    if run_count_corr is None and mass_corr is None:
        dominant_factor = "undetermined"
    elif run_count_corr is None:
        dominant_factor = "total_collapse_frames"
    elif mass_corr is None:
        dominant_factor = "collapse_run_count"
    elif abs(mass_corr) > abs(run_count_corr):
        dominant_factor = "total_collapse_frames"
    elif abs(run_count_corr) > abs(mass_corr):
        dominant_factor = "collapse_run_count"
    else:
        dominant_factor = "tie_run_count_and_mass"

    separation_detected = (
        same_run_count_depth_varies
        or same_mass_depth_varies
        or dominant_factor != "undetermined"
    )

    return {
        "record_count": len(records),
        "reachable_record_count": len(reachable_records),
        "target_depths": depths,
        "target_depth_values": sorted(set(depths)),
        "collapse_run_counts": run_counts,
        "total_collapse_frames": masses,
        "feature_correlations": correlations,
        "strongest_feature": strongest_feature,
        "strongest_abs_correlation": strongest_abs_corr,
        "dominant_factor": dominant_factor,
        "same_run_count_comparison": same_run_count,
        "same_mass_comparison": same_mass,
        "same_run_count_depth_varies": same_run_count_depth_varies,
        "same_mass_depth_varies": same_mass_depth_varies,
        "source_class_summary": source_class_summary,
        "separation_detected": separation_detected,
        "analytical_rule": (
            "minimum_target_depth = "
            "sum(max(0, run_length - 1)) "
            "for transition to OSCILLATING_NONPERSISTENT"
        ),
    }


def compact_record(record):
    return {
        "variant_index": record["variant_index"],
        "geometry_name": record["geometry_name"],
        "source_class": record["source_class"],
        "target_class": record["target_class"],
        "runs": record["runs"],
        "features": record["features"],
        "minimum_target_depth": record["minimum_target_depth"],
        "predicted_target_after_minimal_escape": (
            record["predicted_target_after_minimal_escape"]
        ),
        "target_reachable_by_formula": (
            record["target_reachable_by_formula"]
        ),
        "method": record["method"],
    }


def main():
    records = build_records()
    analysis = summarize(records)

    status = (
        "PASS"
        if analysis["separation_detected"]
        else "CHECK"
    )

    summary = {
        "variant_count": len(records),
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "source_class_focus": SOURCE_CLASS_FOCUS,
        "target_class": TARGET_CLASS,
        "reachable_record_count": analysis["reachable_record_count"],
        "target_depth_values": analysis["target_depth_values"],
        "strongest_feature": analysis["strongest_feature"],
        "strongest_abs_correlation": (
            analysis["strongest_abs_correlation"]
        ),
        "dominant_factor": analysis["dominant_factor"],
        "same_run_count_depth_varies": (
            analysis["same_run_count_depth_varies"]
        ),
        "same_mass_depth_varies": (
            analysis["same_mass_depth_varies"]
        ),
        "separation_detected": analysis["separation_detected"],
        "analytical_rule": analysis["analytical_rule"],
        "bruteforce_removed": True,
    }

    payload = {
        "experiment": (
            "temporal_collapse_topology_variable_run_length_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "variable_run_length_summary": analysis,
        "geometry_records": [
            compact_record(record)
            for record in records
        ],
        "interpretation": (
            "This experiment separates collapse_run_count from "
            "total_collapse_frames by using variable run lengths. "
            "It uses an analytical minimum-depth rule instead of "
            "brute-force mutation enumeration."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_variable_run_length_v0.py"
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
        "Temporal Collapse Topology Variable Run Length v0"
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
            f"source={record['source_class']} "
            f"runs={features['collapse_run_count']} "
            f"lengths={features['run_lengths']} "
            f"mass={features['total_collapse_frames']} "
            f"max_run={features['max_run_length']} "
            f"target_depth={record['minimum_target_depth']} "
            f"target={record['predicted_target_after_minimal_escape']}"
        )

    print()
    print("Feature correlations with target depth")
    print("-" * 80)

    for key, value in analysis["feature_correlations"].items():
        print(f"{key:<32} corr={value}")

    print()
    print("Same run-count comparison")
    print("-" * 80)

    for run_count, value in analysis["same_run_count_comparison"].items():
        print(
            f"run_count={run_count} "
            f"records={value['record_count']} "
            f"masses={value['total_collapse_frames']} "
            f"depths={value['minimum_target_depths']} "
            f"stable={value['depth_stable_within_run_count']} "
            f"geometries={value['geometry_names']}"
        )

    print()
    print("Same mass comparison")
    print("-" * 80)

    for mass, value in analysis["same_mass_comparison"].items():
        print(
            f"mass={mass} "
            f"records={value['record_count']} "
            f"run_counts={value['collapse_run_counts']} "
            f"depths={value['minimum_target_depths']} "
            f"stable={value['depth_stable_within_mass']} "
            f"geometries={value['geometry_names']}"
        )

    print()
    print("Source class summary")
    print("-" * 80)

    for source_class, value in analysis["source_class_summary"].items():
        print(
            f"class={source_class:<32} "
            f"records={value['record_count']} "
            f"depths={value['minimum_target_depths']} "
            f"mean_depth={value['minimum_target_depth_mean']} "
            f"run_counts={value['collapse_run_counts']} "
            f"masses={value['total_collapse_frames']} "
            f"geometries={value['geometry_names']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - run-count vs collapse-mass separation measured "
            "without brute-force enumeration."
        )
    else:
        print(
            "CHECK - run-count vs collapse-mass separation was not "
            "fully resolved under tested cases."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()