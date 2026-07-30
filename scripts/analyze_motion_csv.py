#!/usr/bin/env python3
"""Analyze a Godot motion capture CSV for contact-foot sliding and timing imbalance."""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from pathlib import Path
from typing import Iterable

REQUIRED = {
    "time", "root_x", "root_y", "root_z",
    "left_x", "left_y", "left_z", "right_x", "right_y", "right_z",
    "left_contact", "right_contact",
}


def dist3(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - pos) + ordered[hi] * (pos - lo)


def load_rows(path: Path) -> list[dict[str, float | bool]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
        rows = []
        for index, row in enumerate(reader, start=2):
            try:
                parsed: dict[str, float | bool] = {k: float(row[k]) for k in REQUIRED - {"left_contact", "right_contact"}}
                parsed["left_contact"] = row["left_contact"].strip().lower() in {"1", "true", "yes"}
                parsed["right_contact"] = row["right_contact"].strip().lower() in {"1", "true", "yes"}
                rows.append(parsed)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid numeric value at CSV line {index}: {exc}") from exc
    if len(rows) < 3:
        raise ValueError("At least three samples are required")
    return rows


def contact_runs(rows: list[dict[str, float | bool]], key: str) -> list[float]:
    runs: list[float] = []
    start: float | None = None
    previous_time = float(rows[0]["time"])
    for row in rows:
        t = float(row["time"])
        active = bool(row[key])
        if active and start is None:
            start = t
        elif not active and start is not None:
            runs.append(max(0.0, previous_time - start))
            start = None
        previous_time = t
    if start is not None:
        runs.append(max(0.0, float(rows[-1]["time"]) - start))
    return runs


def analyze(rows: list[dict[str, float | bool]], slide_threshold: float) -> dict:
    speeds = {"left": [], "right": []}
    root_y = [float(r["root_y"]) for r in rows]
    root_horizontal_speed: list[float] = []

    for prev, cur in zip(rows, rows[1:]):
        dt = float(cur["time"]) - float(prev["time"])
        if dt <= 0:
            continue
        p_root = (float(prev["root_x"]), float(prev["root_y"]), float(prev["root_z"]))
        c_root = (float(cur["root_x"]), float(cur["root_y"]), float(cur["root_z"]))
        root_horizontal_speed.append(math.hypot(c_root[0] - p_root[0], c_root[2] - p_root[2]) / dt)
        for side in ("left", "right"):
            if bool(cur[f"{side}_contact"]) and bool(prev[f"{side}_contact"]):
                p = (float(prev[f"{side}_x"]), float(prev[f"{side}_y"]), float(prev[f"{side}_z"]))
                c = (float(cur[f"{side}_x"]), float(cur[f"{side}_y"]), float(cur[f"{side}_z"]))
                speeds[side].append(dist3(p, c) / dt)

    left_runs = contact_runs(rows, "left_contact")
    right_runs = contact_runs(rows, "right_contact")
    left_mean = statistics.fmean(left_runs) if left_runs else 0.0
    right_mean = statistics.fmean(right_runs) if right_runs else 0.0
    denom = max(left_mean, right_mean, 1e-9)
    stance_imbalance = abs(left_mean - right_mean) / denom

    feet = {}
    flags: list[str] = []
    for side in ("left", "right"):
        vals = speeds[side]
        p95 = percentile(vals, 0.95)
        feet[side] = {
            "contact_samples": len(vals),
            "mean_contact_speed": statistics.fmean(vals) if vals else 0.0,
            "p95_contact_speed": p95,
            "max_contact_speed": max(vals, default=0.0),
            "contact_runs": len(left_runs if side == "left" else right_runs),
            "mean_stance_duration": left_mean if side == "left" else right_mean,
        }
        if vals and p95 > slide_threshold:
            flags.append(f"{side} contact-foot sliding exceeds threshold")

    if stance_imbalance > 0.35 and left_runs and right_runs:
        flags.append("left/right stance durations are strongly imbalanced; verify intent or contact labels")

    vertical_range = max(root_y) - min(root_y)
    duration = float(rows[-1]["time"]) - float(rows[0]["time"])
    return {
        "duration": duration,
        "samples": len(rows),
        "root": {
            "mean_horizontal_speed": statistics.fmean(root_horizontal_speed) if root_horizontal_speed else 0.0,
            "vertical_range": vertical_range,
        },
        "feet": feet,
        "stance_duration_imbalance_ratio": stance_imbalance,
        "slide_speed_threshold": slide_threshold,
        "flags": flags,
        "interpretation_note": "Thresholds depend on project scale and contact labeling. Review video and gameplay before changing animation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--slide-speed-threshold", type=float, default=0.04,
                        help="World units per second allowed while a foot is marked in contact (default: 0.04)")
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()
    if args.slide_speed_threshold < 0:
        parser.error("--slide-speed-threshold must be non-negative")
    try:
        report = analyze(load_rows(args.csv_path), args.slide_speed_threshold)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.json_path:
        args.json_path.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
