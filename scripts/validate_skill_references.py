#!/usr/bin/env python3
"""Validate relative files explicitly referenced by a Skill entrypoint."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ALLOWED_ROOTS = {
    "agents",
    "assets",
    "checklists",
    "evals",
    "examples",
    "knowledge",
    "references",
    "scripts",
    "templates",
    "workflows",
}
CODE_PATH_RE = re.compile(
    r"`(?P<path>(?:"
    + "|".join(sorted(ALLOWED_ROOTS))
    + r")/[A-Za-z0-9_.@/+-]+)`"
)
LINK_PATH_RE = re.compile(
    r"\[[^\]]+\]\((?P<path>(?:"
    + "|".join(sorted(ALLOWED_ROOTS))
    + r")/[A-Za-z0-9_.@/+#-]+)\)"
)


def referenced_paths(text: str) -> list[str]:
    values = {
        match.group("path").split("#", 1)[0].rstrip(".,;:")
        for pattern in (CODE_PATH_RE, LINK_PATH_RE)
        for match in pattern.finditer(text)
    }
    return sorted(value for value in values if value)


def validate_skill_directory(skill_dir: Path) -> list[str]:
    skill_dir = skill_dir.resolve()
    entrypoint = skill_dir / "SKILL.md"
    if not entrypoint.is_file():
        return [f"Missing Skill entrypoint: {entrypoint}"]

    errors: list[str] = []
    for relative in referenced_paths(entrypoint.read_text(encoding="utf-8")):
        candidate = (skill_dir / relative).resolve()
        try:
            candidate.relative_to(skill_dir)
        except ValueError:
            errors.append(f"Reference escapes Skill directory: {relative}")
            continue
        if not candidate.is_file():
            errors.append(f"Missing referenced file: {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dirs", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = {
        str(path): validate_skill_directory(path)
        for path in args.skill_dirs
    }
    errors = sum(len(items) for items in report.values())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for path, items in report.items():
            print(f"{path}: {'ok' if not items else f'{len(items)} error(s)'}")
            for item in items:
                print(f"  - {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
