#!/usr/bin/env python3
"""Generate project-scoped Codex custom-agent TOML files from canonical roles."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

TITLE_RE = re.compile(r"^#\s+(?P<title>.+)$", re.MULTILINE)


def _toml_string(value: str) -> str:
    # JSON strings use the same quoted/escaped subset accepted by TOML.
    return json.dumps(value, ensure_ascii=False)


def _agent_source_files(source: Path) -> list[tuple[str, Path]]:
    result = [("godot_content_orchestrator", source / "agents/orchestrator.md")]
    result.extend(
        (path.stem.replace("-", "_"), path)
        for path in sorted((source / "agents/specialists").glob("*.md"))
    )
    return result


def _render_agent(name: str, source_path: Path, source_root: Path) -> str:
    role = source_path.read_text(encoding="utf-8").strip()
    match = TITLE_RE.search(role)
    title = match.group("title") if match else name.replace("_", " ").title()
    relative = source_path.relative_to(source_root).as_posix()
    description = f"{title}: project-scoped Godot content role generated from {relative}."
    common = (
        f"You are the project-scoped `{name}` role in the Godot content team.\n\n"
        "Use `$directing-godot-game-feel` for shared orchestration rules. "
        "Stay inside the assigned domain, distinguish observed/inferred/proposed/unknown, "
        "do not silently edit shared files, and return evidence, ownership, validation, "
        "risk, and rollback. Static checks do not prove player quality.\n\n"
        "Canonical role instructions follow:\n\n"
        f"{role}\n"
    )
    return (
        f"name = {_toml_string(name)}\n"
        f"description = {_toml_string(description)}\n"
        f"developer_instructions = {_toml_string(common)}\n"
    )


def generate_agents(
    source: Path,
    destination: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    source = source.resolve()
    destination = destination.resolve()
    generated = 0
    copied = 0
    agent_names: list[str] = []
    for name, source_path in _agent_source_files(source):
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing canonical agent role: {source_path}")
        target = destination / f"{name}.toml"
        content = _render_agent(name, source_path, source)
        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if existing == content:
                generated += 1
                agent_names.append(name)
                continue
            if not force:
                raise FileExistsError(
                    f"Refusing to overwrite existing agent without --force: {target}"
                )
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")
        generated += 1
        copied += 1
        agent_names.append(name)
    return {
        "agents_generated": generated,
        "agent_names": agent_names,
        "copied_files": copied,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = generate_agents(
        args.source,
        args.destination,
        force=args.force,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
