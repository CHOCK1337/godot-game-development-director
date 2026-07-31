#!/usr/bin/env python3
"""Validate balanced routing evaluations for one or more installable Skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_CATEGORIES = {"direct", "indirect", "incomplete", "negative"}


def validate_skill_evals(skill_dir: Path) -> list[str]:
    skill_dir = skill_dir.resolve()
    path = skill_dir / "evals/evals.json"
    if not path.is_file():
        return ["Missing evals/evals.json"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot parse evals/evals.json: {exc}"]

    errors: list[str] = []
    if payload.get("skill_name") != skill_dir.name:
        errors.append(
            f"skill_name must match directory {skill_dir.name!r}"
        )
    evals = payload.get("evals")
    if not isinstance(evals, list):
        return errors + ["evals must be an array"]

    categories: set[str] = set()
    ids: set[int] = set()
    for index, item in enumerate(evals):
        if not isinstance(item, dict):
            errors.append(f"evals[{index}] must be an object")
            continue
        identifier = item.get("id")
        if not isinstance(identifier, int) or identifier < 1:
            errors.append(f"evals[{index}].id must be a positive integer")
        elif identifier in ids:
            errors.append(f"duplicate eval id: {identifier}")
        else:
            ids.add(identifier)
        category = item.get("category")
        if category not in REQUIRED_CATEGORIES:
            errors.append(f"evals[{index}].category is invalid: {category!r}")
        else:
            categories.add(category)
        for field in ("prompt", "expected_output"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"evals[{index}].{field} must be non-empty")

    if categories != REQUIRED_CATEGORIES:
        errors.append(
            f"eval categories must be exactly {sorted(REQUIRED_CATEGORIES)}, "
            f"found {sorted(categories)}"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dirs", nargs="+", type=Path)
    args = parser.parse_args()
    error_count = 0
    for skill_dir in args.skill_dirs:
        errors = validate_skill_evals(skill_dir)
        error_count += len(errors)
        print(f"{skill_dir}: {'ok' if not errors else f'{len(errors)} error(s)'}")
        for error in errors:
            print(f"  - {error}")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
