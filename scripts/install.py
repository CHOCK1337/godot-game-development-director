#!/usr/bin/env python3
"""Install the Skill package into a project without modifying project code."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

ROOT_SKILL_NAME = "directing-godot-game-feel"
SUPPORTED_PRESETS = {"godot-content-team", "skills-only", "core"}
SUPPORTED_TARGETS = {"codex", "portable"}

SUPPORT_DIRS = [
    "agents",
    "checklists",
    "examples",
    "knowledge",
    "scripts",
    "templates",
    "workflows",
]
ROOT_SUPPORT_FILES = ["SKILL.md", "SOURCES.md", "NOTICE.md", "THIRD_PARTY_NOTICES.md"]


def _copy_file(src: Path, dst: Path, *, force: bool, dry_run: bool) -> int:
    if dst.exists() and not force:
        if dst.read_bytes() == src.read_bytes():
            return 0
        raise FileExistsError(f"Refusing to overwrite existing file without --force: {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return 1


def _copy_tree(src: Path, dst: Path, *, force: bool, dry_run: bool) -> int:
    copied = 0
    for path in sorted(p for p in src.rglob("*") if p.is_file()):
        rel = path.relative_to(src)
        if "__pycache__" in rel.parts or path.suffix == ".pyc":
            continue
        copied += _copy_file(path, dst / rel, force=force, dry_run=dry_run)
    return copied


def install(
    source: Path,
    destination: Path,
    *,
    preset: str = "godot-content-team",
    target_runtime: str = "codex",
    force: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    source = source.resolve()
    destination = destination.resolve()
    if preset not in SUPPORTED_PRESETS:
        raise ValueError(f"Unknown preset {preset!r}; choose from {sorted(SUPPORTED_PRESETS)}")
    if target_runtime not in SUPPORTED_TARGETS:
        raise ValueError(f"Unknown target {target_runtime!r}; choose from {sorted(SUPPORTED_TARGETS)}")
    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError(f"Not a package root: {source}")

    skills_root = destination / ".agents" / "skills"
    root_skill_dir = skills_root / ROOT_SKILL_NAME
    copied = 0

    # Install a self-contained root Skill bundle so relative references remain valid.
    for filename in ROOT_SUPPORT_FILES:
        path = source / filename
        if path.is_file():
            copied += _copy_file(path, root_skill_dir / filename, force=force, dry_run=dry_run)

    if preset != "skills-only":
        for dirname in SUPPORT_DIRS:
            path = source / dirname
            if path.is_dir():
                copied += _copy_tree(path, root_skill_dir / dirname, force=force, dry_run=dry_run)

    # Install module Skills as individually discoverable Skills.
    module_skills = sorted((source / "skills").glob("*/SKILL.md"))
    for skill_file in module_skills:
        skill_dir = skill_file.parent
        copied += _copy_tree(skill_dir, skills_root / skill_dir.name, force=force, dry_run=dry_run)

    agents_created = False
    if target_runtime == "codex" and preset != "skills-only":
        source_agents = source / "codex" / "AGENTS.md.example"
        target_agents = destination / "AGENTS.md"
        if not target_agents.exists():
            copied += _copy_file(source_agents, target_agents, force=False, dry_run=dry_run)
            agents_created = True

    receipt = {
        "package": "godot-game-development-director",
        "version": "0.1.0-alpha",
        "preset": preset,
        "target_runtime": target_runtime,
        "copied_files": copied,
        "skills_installed": 1 + len(module_skills),
        "agents_md_created": agents_created,
    }
    if not dry_run:
        receipt_path = destination / ".agents" / "godot-game-development-director-install.json"
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--preset", default="godot-content-team", choices=sorted(SUPPORTED_PRESETS))
    parser.add_argument("--target", dest="target_runtime", default="codex", choices=sorted(SUPPORTED_TARGETS))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    result = install(
        source,
        args.destination,
        preset=args.preset,
        target_runtime=args.target_runtime,
        force=args.force,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
