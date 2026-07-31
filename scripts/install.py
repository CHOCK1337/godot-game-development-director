#!/usr/bin/env python3
"""Install self-contained Skills and optional project-scoped Codex agents."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any

PACKAGE_VERSION = "0.1.0-alpha.1"
ROOT_SKILL_NAME = "directing-godot-game-feel"
PRESET_ALIASES = {
    "core": "director",
    "skills-only": "modules",
    "godot-content-team": "full",
}
CANONICAL_PRESETS = {"director", "modules", "full"}
SUPPORTED_PRESETS = CANONICAL_PRESETS | set(PRESET_ALIASES)
SUPPORTED_TARGETS = {"codex", "portable"}


def _copy_file(src: Path, dst: Path, *, force: bool, dry_run: bool) -> int:
    if dst.exists():
        if dst.read_bytes() == src.read_bytes():
            return 0
        if not force:
            raise FileExistsError(f"Refusing to overwrite existing file without --force: {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return 1


def _copy_tree(src: Path, dst: Path, *, force: bool, dry_run: bool) -> int:
    copied = 0
    for path in sorted(item for item in src.rglob("*") if item.is_file()):
        rel = path.relative_to(src)
        if "__pycache__" in rel.parts or path.suffix == ".pyc":
            continue
        copied += _copy_file(path, dst / rel, force=force, dry_run=dry_run)
    return copied


def _load_generator(source: Path):
    path = source / "scripts/generate_codex_agents.py"
    spec = importlib.util.spec_from_file_location("godot_director_agent_generator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load Codex agent generator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _available_skills(source: Path) -> dict[str, Path]:
    return {
        skill_file.parent.name: skill_file.parent
        for skill_file in sorted((source / "skills").glob("*/SKILL.md"))
    }


def install(
    source: Path,
    destination: Path,
    *,
    preset: str = "godot-content-team",
    target_runtime: str = "codex",
    force: bool = False,
    dry_run: bool = False,
    write_agents_md: bool = False,
    install_codex_agents: bool | None = None,
) -> dict[str, Any]:
    source = source.resolve()
    destination = destination.resolve()
    if preset not in SUPPORTED_PRESETS:
        raise ValueError(f"Unknown preset {preset!r}; choose from {sorted(SUPPORTED_PRESETS)}")
    if target_runtime not in SUPPORTED_TARGETS:
        raise ValueError(f"Unknown target {target_runtime!r}; choose from {sorted(SUPPORTED_TARGETS)}")
    if not (source / "SKILL.md").is_file():
        raise FileNotFoundError(f"Not a package root: {source}")

    effective = PRESET_ALIASES.get(preset, preset)
    available = _available_skills(source)
    if ROOT_SKILL_NAME not in available:
        raise FileNotFoundError(f"Missing packaged director Skill: skills/{ROOT_SKILL_NAME}")

    if effective == "director":
        selected_names = [ROOT_SKILL_NAME]
    elif effective == "modules":
        selected_names = sorted(name for name in available if name != ROOT_SKILL_NAME)
    else:
        selected_names = sorted(available)

    skills_root = destination / ".agents/skills"
    copied = 0
    for name in selected_names:
        copied += _copy_tree(
            available[name],
            skills_root / name,
            force=force,
            dry_run=dry_run,
        )

    if install_codex_agents is None:
        install_codex_agents = target_runtime == "codex" and effective == "full"
    if install_codex_agents and target_runtime != "codex":
        raise ValueError("Codex custom agents can only be installed for --target codex")

    codex_agents_installed = 0
    codex_agent_names: list[str] = []
    if install_codex_agents:
        result = _load_generator(source).generate_agents(
            source,
            destination / ".codex/agents",
            force=force,
            dry_run=dry_run,
        )
        codex_agents_installed = result["agents_generated"]
        codex_agent_names = result["agent_names"]
        copied += result["copied_files"]

    agents_created = False
    if write_agents_md:
        if target_runtime != "codex":
            raise ValueError("--write-agents-md requires --target codex")
        source_agents = source / "codex/AGENTS.md.example"
        target_agents = destination / "AGENTS.md"
        # A project policy belongs to the project. Never replace an existing one,
        # including when --force is used for package-owned files.
        if not target_agents.exists():
            copied += _copy_file(source_agents, target_agents, force=False, dry_run=dry_run)
            agents_created = True

    receipt = {
        "package": "godot-game-development-director",
        "version": PACKAGE_VERSION,
        "preset": preset,
        "effective_preset": effective,
        "target_runtime": target_runtime,
        "copied_files": copied,
        "skills_installed": len(selected_names),
        "skill_names": selected_names,
        "codex_agents_installed": codex_agents_installed,
        "codex_agent_names": codex_agent_names,
        "agents_md_requested": write_agents_md,
        "agents_md_created": agents_created,
    }
    if not dry_run:
        receipt_path = destination / ".agents/godot-game-development-director-install.json"
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--preset", default="godot-content-team", choices=sorted(SUPPORTED_PRESETS))
    parser.add_argument("--target", dest="target_runtime", default="codex", choices=sorted(SUPPORTED_TARGETS))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--write-agents-md",
        action="store_true",
        help="Copy the optional project routing policy only when AGENTS.md is absent",
    )
    agent_group = parser.add_mutually_exclusive_group()
    agent_group.add_argument("--with-codex-agents", dest="install_codex_agents", action="store_true")
    agent_group.add_argument("--without-codex-agents", dest="install_codex_agents", action="store_false")
    parser.set_defaults(install_codex_agents=None)
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    result = install(
        source,
        args.destination,
        preset=args.preset,
        target_runtime=args.target_runtime,
        force=args.force,
        dry_run=args.dry_run,
        write_agents_md=args.write_agents_md,
        install_codex_agents=args.install_codex_agents,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
