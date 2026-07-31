#!/usr/bin/env python3
"""Build a small, deterministic dispatch plan for the installed director Skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROUTES = {
    "gameplay": "designing-godot-gameplay",
    "economy": "designing-godot-gameplay",
    "level": "designing-godot-levels-balance-randomness",
    "balance": "designing-godot-levels-balance-randomness",
    "procedural": "designing-godot-levels-balance-randomness",
    "quest": "authoring-narrative-quests-cinematics",
    "narrative": "authoring-narrative-quests-cinematics",
    "npc": "designing-npc-ai-simulation",
    "music": "directing-interactive-game-music",
    "camera": "polishing-game-presentation-accessibility",
    "audio": "polishing-game-presentation-accessibility",
    "accessibility": "polishing-game-presentation-accessibility",
    "localization": "polishing-game-presentation-accessibility",
    "scope": "producing-game-content",
    "milestone": "producing-game-content",
    "save": "building-godot-content-pipelines",
    "content_pipeline": "building-godot-content-pipelines",
}


def build_plan(brief: dict[str, Any]) -> dict[str, Any]:
    raw = brief.get("domains") or brief.get("tags") or []
    if isinstance(raw, str):
        raw = [raw]
    domains = [str(value).strip().lower().replace(" ", "_") for value in raw]
    skills = list(dict.fromkeys(ROUTES[value] for value in domains if value in ROUTES))
    unknown = sorted({value for value in domains if value not in ROUTES})
    if len(skills) <= 1:
        mode = "single"
    elif len(skills) <= 3:
        mode = "parallel_lite"
    else:
        mode = "two_waves"
    return {
        "mode": mode,
        "selected_skills": skills,
        "unknown_domains": unknown,
        "shared_contracts_required": len(skills) > 1,
        "postprocessing": ["content-qa", "qa-acceptance"] if skills else [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    payload = json.loads(args.brief.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        parser.error("brief must be a JSON object")
    print(json.dumps(build_plan(payload), ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
