# Repository Agent Instructions

## Purpose

Maintain a modular, evidence-driven game-development Skill and Agent library. Preserve the boundary between engine-independent design knowledge and Godot integration details.

## Before editing

1. Read `SKILL.md`, the relevant module Skill, and `agents/routing-table.md`.
2. Select the smallest relevant specialist set.
3. Do not let multiple agents edit the same shared resource concurrently.
4. Add or update tests before changing routing, contracts, validators, or mandatory behavior.

## Required validation

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_public_release.py
python tests/validate_package.py
python -m unittest discover -s tests -v
```

## Repository rules

- No credentials, private project files, or unlicensed third-party assets.
- No large copied passages from external sources; link and summarize.
- GDScript claims require a live Godot check. Otherwise state that validation is static.
- Keep public versions in SemVer. Internal historical version numbers are not public releases.
- Generated files in `dist/` are release assets and are not committed by default.
- Publishing, tagging, pushing, deleting, and changing repository visibility require explicit human approval.
