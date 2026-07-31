#!/usr/bin/env python3
"""Inspect an installed package, including Skill resources and Codex agents."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import tomllib
from pathlib import Path
from typing import Any

FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---(?:\n|$)", re.DOTALL)


def _frontmatter_name(text: str) -> str | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    for line in match.group("body").splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def _load_reference_validator():
    path = Path(__file__).with_name("validate_skill_references.py")
    spec = importlib.util.spec_from_file_location("installed_skill_reference_validator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load Skill reference validator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inspect_installation(destination: Path) -> dict[str, Any]:
    destination = destination.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    skills_root = destination / ".agents/skills"

    receipt_path = destination / ".agents/godot-game-development-director-install.json"
    receipt = None
    if receipt_path.is_file():
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid install receipt: {exc}")
    else:
        warnings.append("Install receipt is missing")

    if not skills_root.is_dir():
        errors.append("Missing .agents/skills directory")
        skill_files: list[Path] = []
    else:
        receipt_skill_names = receipt.get("skill_names", []) if receipt else []
        if receipt_skill_names:
            skill_files = []
            for name in receipt_skill_names:
                path = skills_root / name / "SKILL.md"
                if path.is_file():
                    skill_files.append(path)
                else:
                    errors.append(f"Receipt Skill is missing: {name}")
        else:
            skill_files = sorted(skills_root.glob("*/SKILL.md"))

    reference_validator = _load_reference_validator()
    for skill_file in skill_files:
        text = skill_file.read_text(encoding="utf-8")
        name = _frontmatter_name(text)
        if name is None:
            errors.append(f"Invalid Skill frontmatter: {skill_file.relative_to(destination)}")
        elif name != skill_file.parent.name:
            errors.append(
                f"Skill name/path mismatch: {name!r} != {skill_file.parent.name!r}"
            )
        metadata = skill_file.parent / "agents/openai.yaml"
        if not metadata.is_file():
            errors.append(
                f"Missing Skill UI metadata: {metadata.relative_to(destination)}"
            )
        for issue in reference_validator.validate_skill_directory(skill_file.parent):
            errors.append(f"{skill_file.parent.name}: {issue}")

    if receipt:
        expected_names = receipt.get("skill_names", [])
        installed_names = sorted(path.parent.name for path in skill_files)
        if expected_names and sorted(expected_names) != installed_names:
            errors.append(
                f"Receipt Skill set differs from installation: {expected_names!r} != {installed_names!r}"
            )
        expected_count = receipt.get("skills_installed")
        if expected_count is not None and expected_count != len(skill_files):
            errors.append(
                f"Receipt expected {expected_count} Skills, found {len(skill_files)}"
            )
        if receipt.get("agents_md_requested") and not (destination / "AGENTS.md").is_file():
            errors.append("AGENTS.md was requested but is missing")

    agents_root = destination / ".codex/agents"
    receipt_agent_names = receipt.get("codex_agent_names", []) if receipt else []
    if receipt_agent_names:
        agent_files = []
        for name in receipt_agent_names:
            path = agents_root / f"{name}.toml"
            if path.is_file():
                agent_files.append(path)
            else:
                errors.append(f"Receipt Codex agent is missing: {name}")
    elif receipt and receipt.get("codex_agents_installed", 0) == 0:
        agent_files = []
    else:
        agent_files = sorted(agents_root.glob("*.toml"))
    for path in agent_files:
        try:
            payload = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"Invalid Codex agent {path.relative_to(destination)}: {exc}")
            continue
        for key in ("name", "description", "developer_instructions"):
            if not isinstance(payload.get(key), str) or not payload[key].strip():
                errors.append(
                    f"Codex agent {path.relative_to(destination)} missing non-empty {key}"
                )
    if receipt:
        expected_agents = receipt.get("codex_agents_installed", 0)
        if expected_agents != len(agent_files):
            errors.append(
                f"Receipt expected {expected_agents} Codex agents, found {len(agent_files)}"
            )

    return {
        "destination": str(destination),
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "skills_found": len(skill_files),
        "codex_agents_found": len(agent_files),
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
