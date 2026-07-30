#!/usr/bin/env python3
"""Inspect a project installation of Godot Game Development Director."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---(?:\n|$)", re.DOTALL)


def inspect_installation(destination: Path) -> dict[str, Any]:
    destination = destination.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    skills_root = destination / ".agents" / "skills"

    if not skills_root.is_dir():
        errors.append("Missing .agents/skills directory")
        skill_files: list[Path] = []
    else:
        skill_files = sorted(skills_root.glob("*/SKILL.md"))

    for skill_file in skill_files:
        text = skill_file.read_text(encoding="utf-8")
        if not FRONTMATTER_RE.match(text):
            errors.append(f"Invalid Skill frontmatter: {skill_file.relative_to(destination)}")

    root_skill = skills_root / "directing-godot-game-feel" / "SKILL.md"
    if not root_skill.is_file():
        errors.append("Root Skill is not installed")

    if not (destination / "AGENTS.md").is_file():
        warnings.append("No project AGENTS.md found; implicit routing policy may not be active")

    receipt_path = destination / ".agents" / "godot-game-development-director-install.json"
    receipt = None
    if receipt_path.is_file():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid install receipt: {exc}")
    else:
        warnings.append("Install receipt is missing")

    return {
        "destination": str(destination),
        "errors": errors,
        "warnings": warnings,
        "skills_found": len(skill_files),
        "receipt": receipt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = inspect_installation(args.destination)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
