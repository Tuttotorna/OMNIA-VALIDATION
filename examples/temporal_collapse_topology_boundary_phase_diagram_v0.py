import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

INPUT_RESULTS_PATH = Path(
    "results/temporal_collapse_topology_dependency_boundary_v0.json"
)

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_boundary_phase_diagram_v0.json"
)

PHASE_ORDER = [
    "STABLE_ZONE",
    "DRIFT_ZONE",
    "CRITICAL_ZONE",
]

PHASE_FROM_DEPENDENCY_CLASS = {
    "STABLE_SUPPORT": "STABLE_ZONE",
    "MODERATE_RANK_DRIFT": "DRIFT_ZONE",
    "CRITICAL_TOP6_LOSS": "CRITICAL_ZONE",
    "CRITICAL_ORDER_INVERSION": "CRITICAL_ZONE",
    "CRITICAL_ABSENCE": "CRITICAL_ZONE",
}


def safe_mean(values):
    return mean(values) if values else None


def safe_std(values):
    return pstdev(values) if len(values) > 1 else 0.0


def load_dependency_boundary_result():
    if not INPUT_RESULTS_PATH.exists():
        raise FileNotFoundError(
            f"Missing input result file: {INPUT_RESULTS_PATH}"
        )

    return json.loads(INPUT_RESULTS_PATH.read_text(encoding="utf-8"))


def classify_phase(record):
    dependency_class = record.get("dependency_class")
    return PHASE_FROM_DEPENDENCY_CLASS.get(
        dependency_class,
        "UNKNOWN_ZONE",
    )


def phase_severity(phase):
    if phase == "STABLE_ZONE":
        return 0

    if phase == "DRIFT_ZONE":
        return 1

    if phase == "CRITICAL_ZONE":
        return 2

    return 99


def compact_record(record):
    return {
        "scenario_name": record.get("scenario_name"),
        "scenario_type": record.get("scenario_type"),
        "boundary_axis": record.get("boundary_axis"),
        "boundary_distance": record.get("boundary_distance"),
        "status": record.get("status"),
        "strict_status": record.get("strict_status"),
        "dependency_class": record.get("dependency_class"),
        "phase_zone": record.get("phase_zone"),
        "impact_score": record.get("impact_score"),
        "expected_dominant_rank": record.get("expected_dominant_rank"),
        "expected_second_rank": record.get("expected_second_rank"),
        "dominant_cluster_id": record.get("dominant_cluster_id"),
        "second_cluster_id": record.get("second_cluster_id"),
    }


def build_phase_records(dependency_payload):
    records = []

    for raw in dependency_payload.get("scenario_results", []):
        record = dict(raw)
        record["phase_zone"] = classify_phase(record)
        record["phase_severity"] = phase_severity(record["phase_zone"])
        records.append(record)

    return records


def summarize_by_phase(records):
    by_phase = {}

    for phase in PHASE_ORDER + ["UNKNOWN_ZONE"]:
        by_phase[phase] = {
            "phase_zone": phase,
            "record_count": 0,
            "scenario_names": [],
            "boundary_axes": [],
            "scenario_types": [],
            "dependency_classes": [],
            "boundary_distances": [],
            "impact_scores": [],
            "dominant_ranks": [],
            "second_ranks": [],
        }

    for record in records:
        phase = record["phase_zone"]

        if phase not in by_phase:
            by_phase[phase] = {
                "phase_zone": phase,
                "record_count": 0,
                "scenario_names": [],
                "boundary_axes": [],
                "scenario_types": [],
                "dependency_classes": [],
                "boundary_distances": [],
                "impact_scores": [],
                "dominant_ranks": [],
                "second_ranks": [],
            }

        item = by_phase[phase]
        item["record_count"] += 1
        item["scenario_names"].append(record.get("scenario_name"))
        item["boundary_axes"].append(record.get("boundary_axis"))
        item["scenario_types"].append(record.get("scenario_type"))
        item["dependency_classes"].append(record.get("dependency_class"))

        distance = record.get("boundary_distance")
        impact = record.get("impact_score")
        dominant_rank = record.get("expected_dominant_rank")
        second_rank = record.get("expected_second_rank")

        if distance is not None:
            item["boundary_distances"].append(distance)

        if impact is not None:
            item["impact_scores"].append(impact)

        if dominant_rank is not None:
            item["dominant_ranks"].append(dominant_rank)

        if second_rank is not None:
            item["second_ranks"].append(second_rank)

    for item in by_phase.values():
        item["boundary_axis_values"] = sorted(
            value
            for value in set(item["boundary_axes"])
            if value is not None
        )
        item["scenario_type_values"] = sorted(
            value
            for value in set(item["scenario_types"])
            if value is not None
        )
        item["dependency_class_values"] = sorted(
            value
            for value in set(item["dependency_classes"])
            if value is not None
        )
        item["minimum_boundary_distance"] = (
            min(item["boundary_distances"])
            if item["boundary_distances"]
            else None
        )
        item["maximum_boundary_distance"] = (
            max(item["boundary_distances"])
            if item["boundary_distances"]
            else None
        )
        item["impact_score_mean"] = safe_mean(item["impact_scores"])
        item["impact_score_std"] = safe_std(item["impact_scores"])
        item["impact_score_max"] = (
            max(item["impact_scores"])
            if item["impact_scores"]
            else None
        )
        item["dominant_rank_mean"] = safe_mean(item["dominant_ranks"])
        item["second_rank_mean"] = safe_mean(item["second_ranks"])

    return {
        phase: item
        for phase, item in by_phase.items()
        if item["record_count"] > 0
    }


def summarize_by_axis_and_phase(records):
    table = {}

    for record in records:
        axis = record.get("boundary_axis")
        phase = record.get("phase_zone")

        if axis is None:
            axis = "unknown"

        if axis not in table:
            table[axis] = {}

        if phase not in table[axis]:
            table[axis][phase] = {
                "boundary_axis": axis,
                "phase_zone": phase,
                "record_count": 0,
                "scenario_names": [],
                "dependency_classes": [],
                "boundary_distances": [],
                "impact_scores": [],
            }

        item = table[axis][phase]
        item["record_count"] += 1
        item["scenario_names"].append(record.get("scenario_name"))
        item["dependency_classes"].append(record.get("dependency_class"))

        distance = record.get("boundary_distance")
        impact = record.get("impact_score")

        if distance is not None:
            item["boundary_distances"].append(distance)

        if impact is not None:
            item["impact_scores"].append(impact)

    for axis_items in table.values():
        for item in axis_items.values():
            item["dependency_class_values"] = sorted(
                value
                for value in set(item["dependency_classes"])
                if value is not None
            )
            item["minimum_boundary_distance"] = (
                min(item["boundary_distances"])
                if item["boundary_distances"]
                else None
            )
            item["maximum_boundary_distance"] = (
                max(item["boundary_distances"])
                if item["boundary_distances"]
                else None
            )
            item["impact_score_mean"] = safe_mean(item["impact_scores"])
            item["impact_score_max"] = (
                max(item["impact_scores"])
                if item["impact_scores"]
                else None
            )

    return table


def summarize_distance_phase_map(records):
    distance_map = {}

    for record in records:
        axis = record.get("boundary_axis")
        distance = record.get("boundary_distance")
        phase = record.get("phase_zone")

        if axis is None:
            axis = "unknown"

        if distance is None:
            continue

        axis_map = distance_map.setdefault(axis, {})
        distance_key = str(distance)

        if distance_key not in axis_map:
            axis_map[distance_key] = {
                "boundary_axis": axis,
                "boundary_distance": distance,
                "record_count": 0,
                "phase_counts": {
                    "STABLE_ZONE": 0,
                    "DRIFT_ZONE": 0,
                    "CRITICAL_ZONE": 0,
                    "UNKNOWN_ZONE": 0,
                },
                "dominant_phase": None,
                "scenario_names": [],
                "impact_scores": [],
            }

        item = axis_map[distance_key]
        item["record_count"] += 1
        item["phase_counts"][phase] = item["phase_counts"].get(phase, 0) + 1
        item["scenario_names"].append(record.get("scenario_name"))

        impact = record.get("impact_score")

        if impact is not None:
            item["impact_scores"].append(impact)

    for axis_map in distance_map.values():
        for item in axis_map.values():
            ordered = sorted(
                item["phase_counts"].items(),
                key=lambda pair: (
                    pair[1],
                    phase_severity(pair[0]),
                    pair[0],
                ),
                reverse=True,
            )

            item["dominant_phase"] = ordered[0][0] if ordered else None
            item["impact_score_mean"] = safe_mean(item["impact_scores"])
            item["impact_score_max"] = (
                max(item["impact_scores"])
                if item["impact_scores"]
                else None
            )

    return distance_map


def compute_phase_boundaries(records):
    phase_boundaries = {}

    for axis in sorted(
        set(record.get("boundary_axis") for record in records)
    ):
        if axis is None:
            continue

        axis_records = [
            record
            for record in records
            if record.get("boundary_axis") == axis
        ]

        item = {
            "boundary_axis": axis,
            "stable_min_distance": None,
            "drift_min_distance": None,
            "critical_min_distance": None,
            "stable_count": 0,
            "drift_count": 0,
            "critical_count": 0,
            "transition_boundary_detected": False,
            "phase_sequence_by_distance": [],
        }

        by_distance = {}

        for record in axis_records:
            distance = record.get("boundary_distance")
            phase = record.get("phase_zone")

            if distance is None:
                continue

            by_distance.setdefault(distance, []).append(phase)

            if phase == "STABLE_ZONE":
                item["stable_count"] += 1

                if (
                    item["stable_min_distance"] is None
                    or distance < item["stable_min_distance"]
                ):
                    item["stable_min_distance"] = distance

            if phase == "DRIFT_ZONE":
                item["drift_count"] += 1

                if (
                    item["drift_min_distance"] is None
                    or distance < item["drift_min_distance"]
                ):
                    item["drift_min_distance"] = distance

            if phase == "CRITICAL_ZONE":
                item["critical_count"] += 1

                if (
                    item["critical_min_distance"] is None
                    or distance < item["critical_min_distance"]
                ):
                    item["critical_min_distance"] = distance

        for distance, phase_values in sorted(by_distance.items()):
            phase_counts = {
                "STABLE_ZONE": phase_values.count("STABLE_ZONE"),
                "DRIFT_ZONE": phase_values.count("DRIFT_ZONE"),
                "CRITICAL_ZONE": phase_values.count("CRITICAL_ZONE"),
            }

            dominant_phase = sorted(
                phase_counts.items(),
                key=lambda pair: (
                    pair[1],
                    phase_severity(pair[0]),
                    pair[0],
                ),
                reverse=True,
            )[0][0]

            item["phase_sequence_by_distance"].append({
                "boundary_distance": distance,
                "phase_counts": phase_counts,
                "dominant_phase": dominant_phase,
            })

        item["transition_boundary_detected"] = (
            item["stable_count"] > 0
            and (
                item["drift_count"] > 0
                or item["critical_count"] > 0
            )
        )

        phase_boundaries[axis] = item

    return phase_boundaries


def select_boundary_extremes(records):
    stable = [
        record
        for record in records
        if record["phase_zone"] == "STABLE_ZONE"
    ]

    drift = [
        record
        for record in records
        if record["phase_zone"] == "DRIFT_ZONE"
    ]

    critical = [
        record
        for record in records
        if record["phase_zone"] == "CRITICAL_ZONE"
    ]

    minimum_critical = sorted(
        critical,
        key=lambda record: (
            record.get("boundary_distance", 999999),
            -record.get("impact_score", 0),
            record.get("scenario_name", ""),
        ),
    )

    maximum_critical = sorted(
        critical,
        key=lambda record: (
            record.get("impact_score", 0),
            -record.get("boundary_distance", 0),
            record.get("scenario_name", ""),
        ),
        reverse=True,
    )

    minimum_drift = sorted(
        drift,
        key=lambda record: (
            record.get("boundary_distance", 999999),
            -record.get("impact_score", 0),
            record.get("scenario_name", ""),
        ),
    )

    stable_low_distance = sorted(
        stable,
        key=lambda record: (
            record.get("boundary_distance", 999999),
            record.get("scenario_name", ""),
        ),
    )

    return {
        "minimum_critical_boundaries": [
            compact_record(record)
            for record in minimum_critical[:10]
        ],
        "maximum_impact_critical_boundaries": [
            compact_record(record)
            for record in maximum_critical[:10]
        ],
        "minimum_drift_boundaries": [
            compact_record(record)
            for record in minimum_drift[:10]
        ],
        "minimum_distance_stable_boundaries": [
            compact_record(record)
            for record in stable_low_distance[:10]
        ],
    }


def build_ascii_phase_diagram(distance_phase_map):
    lines = []

    for axis in sorted(distance_phase_map):
        lines.append(f"{axis}:")

        axis_map = distance_phase_map[axis]

        for distance_key in sorted(
            axis_map,
            key=lambda value: int(value),
        ):
            item = axis_map[distance_key]
            phase_counts = item["phase_counts"]

            stable = phase_counts.get("STABLE_ZONE", 0)
            drift = phase_counts.get("DRIFT_ZONE", 0)
            critical = phase_counts.get("CRITICAL_ZONE", 0)

            lines.append(
                "  "
                f"d={distance_key} "
                f"stable={stable} "
                f"drift={drift} "
                f"critical={critical} "
                f"dominant={item['dominant_phase']}"
            )

    return "\n".join(lines)


def validate_phase_diagram(phase_summary, phase_boundaries):
    failures = []

    if "STABLE_ZONE" not in phase_summary:
        failures.append({
            "reason": "missing_stable_zone",
        })

    if "DRIFT_ZONE" not in phase_summary:
        failures.append({
            "reason": "missing_drift_zone",
        })

    if "CRITICAL_ZONE" not in phase_summary:
        failures.append({
            "reason": "missing_critical_zone",
        })

    for axis, item in phase_boundaries.items():
        if axis in {"family", "threshold"}:
            if item["critical_count"] <= 0:
                failures.append({
                    "reason": "expected_critical_zone_missing",
                    "boundary_axis": axis,
                })

        if axis == "variant":
            if item["critical_count"] != 0:
                failures.append({
                    "reason": "unexpected_variant_critical_zone",
                    "boundary_axis": axis,
                    "critical_count": item["critical_count"],
                })

    return {
        "phase_diagram_validation_holds": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
    }


def main():
    dependency_payload = load_dependency_boundary_result()
    phase_records = build_phase_records(dependency_payload)

    phase_summary = summarize_by_phase(phase_records)
    axis_phase_summary = summarize_by_axis_and_phase(phase_records)
    distance_phase_map = summarize_distance_phase_map(phase_records)
    phase_boundaries = compute_phase_boundaries(phase_records)
    boundary_extremes = select_boundary_extremes(phase_records)
    ascii_phase_diagram = build_ascii_phase_diagram(distance_phase_map)

    validation = validate_phase_diagram(
        phase_summary,
        phase_boundaries,
    )

    dependency_boundary_detected = dependency_payload.get(
        "summary",
        {},
    ).get("dependency_boundary_detected", False)

    phase_diagram_detected = (
        dependency_boundary_detected
        and validation["phase_diagram_validation_holds"]
        and "STABLE_ZONE" in phase_summary
        and "DRIFT_ZONE" in phase_summary
        and "CRITICAL_ZONE" in phase_summary
    )

    status = "PASS" if phase_diagram_detected else "CHECK"

    payload = {
        "experiment": (
            "temporal_collapse_topology_boundary_phase_diagram_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": {
            "input_result_file": str(INPUT_RESULTS_PATH),
            "boundary_scenario_count": len(phase_records),
            "phase_zone_count": len(phase_summary),
            "stable_zone_count": phase_summary.get(
                "STABLE_ZONE",
                {},
            ).get("record_count", 0),
            "drift_zone_count": phase_summary.get(
                "DRIFT_ZONE",
                {},
            ).get("record_count", 0),
            "critical_zone_count": phase_summary.get(
                "CRITICAL_ZONE",
                {},
            ).get("record_count", 0),
            "family_transition_boundary_detected": (
                phase_boundaries.get(
                    "family",
                    {},
                ).get("transition_boundary_detected", False)
            ),
            "threshold_transition_boundary_detected": (
                phase_boundaries.get(
                    "threshold",
                    {},
                ).get("transition_boundary_detected", False)
            ),
            "variant_transition_boundary_detected": (
                phase_boundaries.get(
                    "variant",
                    {},
                ).get("transition_boundary_detected", False)
            ),
            "minimum_critical_distance": min(
                [
                    item["critical_min_distance"]
                    for item in phase_boundaries.values()
                    if item["critical_min_distance"] is not None
                ],
                default=None,
            ),
            "minimum_drift_distance": min(
                [
                    item["drift_min_distance"]
                    for item in phase_boundaries.values()
                    if item["drift_min_distance"] is not None
                ],
                default=None,
            ),
            "phase_diagram_validation_holds": (
                validation["phase_diagram_validation_holds"]
            ),
            "phase_diagram_detected": phase_diagram_detected,
            "method": "boundary_phase_diagram",
        },
        "boundary_phase_diagram_summary": {
            "phase_summary": phase_summary,
            "axis_phase_summary": axis_phase_summary,
            "distance_phase_map": distance_phase_map,
            "phase_boundaries": phase_boundaries,
            "boundary_extremes": boundary_extremes,
            "ascii_phase_diagram": ascii_phase_diagram,
            "phase_diagram_validation": validation,
            "phase_diagram_detected": phase_diagram_detected,
            "phase_rule": (
                "STABLE_SUPPORT -> STABLE_ZONE; "
                "MODERATE_RANK_DRIFT -> DRIFT_ZONE; "
                "CRITICAL_TOP6_LOSS, CRITICAL_ORDER_INVERSION, "
                "and CRITICAL_ABSENCE -> CRITICAL_ZONE."
            ),
        },
        "phase_records": [
            compact_record(record)
            for record in phase_records
        ],
        "interpretation": {
            "main_result": "boundary phase diagram detected",
            "structural_conclusion": (
                "The dependency-boundary landscape separates into "
                "stable, drift, and critical zones. Family and threshold "
                "axes expose transition boundaries; the variant axis remains "
                "stable under tested perturbations."
            ),
            "important_boundary": (
                "This is a structural phase map of boundary behavior, "
                "not a semantic judgment or decision layer."
            ),
        },
        "final_check": {
            "status": status,
            "message": (
                "boundary phase diagram detected"
                if status == "PASS"
                else "boundary phase diagram was not fully confirmed"
            ),
        },
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_boundary_phase_diagram_v0.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Topology Boundary Phase Diagram v0"
    )
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)

    print()
    print("Summary")
    print("-" * 80)

    for key, value in payload["summary"].items():
        print(f"{key}: {value}")

    print()
    print("Phase zones")
    print("-" * 80)

    for phase in PHASE_ORDER:
        item = phase_summary.get(phase)

        if not item:
            continue

        print(
            f"phase={phase:<16} "
            f"records={item['record_count']} "
            f"axes={item['boundary_axis_values']} "
            f"classes={item['dependency_class_values']} "
            f"min_distance={item['minimum_boundary_distance']} "
            f"max_distance={item['maximum_boundary_distance']} "
            f"impact_mean={item['impact_score_mean']} "
            f"impact_max={item['impact_score_max']}"
        )

    print()
    print("Axis / phase matrix")
    print("-" * 80)

    for axis, axis_items in axis_phase_summary.items():
        for phase in PHASE_ORDER:
            item = axis_items.get(phase)

            if not item:
                continue

            print(
                f"axis={axis:<10} "
                f"phase={phase:<16} "
                f"records={item['record_count']} "
                f"min_distance={item['minimum_boundary_distance']} "
                f"max_distance={item['maximum_boundary_distance']} "
                f"impact_mean={item['impact_score_mean']} "
                f"impact_max={item['impact_score_max']}"
            )

    print()
    print("Distance phase map")
    print("-" * 80)
    print(ascii_phase_diagram)

    print()
    print("Phase boundaries")
    print("-" * 80)

    for axis, item in phase_boundaries.items():
        print(
            f"axis={axis:<10} "
            f"stable={item['stable_count']} "
            f"drift={item['drift_count']} "
            f"critical={item['critical_count']} "
            f"stable_min={item['stable_min_distance']} "
            f"drift_min={item['drift_min_distance']} "
            f"critical_min={item['critical_min_distance']} "
            f"transition_boundary={item['transition_boundary_detected']}"
        )

    print()
    print("Minimum critical boundaries")
    print("-" * 80)

    for record in boundary_extremes["minimum_critical_boundaries"]:
        print(
            f"scenario={record['scenario_name']:<64} "
            f"axis={record['boundary_axis']:<10} "
            f"distance={record['boundary_distance']} "
            f"class={record['dependency_class']} "
            f"impact={record['impact_score']} "
            f"dom_rank={record['expected_dominant_rank']} "
            f"sec_rank={record['expected_second_rank']}"
        )

    print()
    print("Maximum-impact critical boundaries")
    print("-" * 80)

    for record in boundary_extremes["maximum_impact_critical_boundaries"]:
        print(
            f"scenario={record['scenario_name']:<64} "
            f"axis={record['boundary_axis']:<10} "
            f"distance={record['boundary_distance']} "
            f"class={record['dependency_class']} "
            f"impact={record['impact_score']} "
            f"dom_rank={record['expected_dominant_rank']} "
            f"sec_rank={record['expected_second_rank']}"
        )

    print()
    print("Minimum drift boundaries")
    print("-" * 80)

    for record in boundary_extremes["minimum_drift_boundaries"]:
        print(
            f"scenario={record['scenario_name']:<64} "
            f"axis={record['boundary_axis']:<10} "
            f"distance={record['boundary_distance']} "
            f"class={record['dependency_class']} "
            f"impact={record['impact_score']} "
            f"dom_rank={record['expected_dominant_rank']} "
            f"sec_rank={record['expected_second_rank']}"
        )

    print()
    print("Validation")
    print("-" * 80)

    print(
        "phase_diagram_validation_holds:",
        validation["phase_diagram_validation_holds"],
    )
    print("failure_count:", validation["failure_count"])

    if validation["failures"]:
        print("failures:", validation["failures"])

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - boundary phase diagram detected: dependency boundaries "
            "separate into stable, drift, and critical zones."
        )
    else:
        print(
            "CHECK - boundary phase diagram was not fully confirmed under "
            "the tested dependency-boundary records."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()