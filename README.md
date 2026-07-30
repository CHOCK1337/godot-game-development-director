# Godot Game Development Director

**Version:** `v0.1.0-alpha` · **Status:** public preview · **License:** Apache-2.0

Godot Game Development Director is a modular collection of **game-development Skills, specialist agent definitions, structured contracts, deterministic validators, checklists, examples, and Godot-oriented content-production workflows**.

It focuses on improving playable game content: character motion, gameplay, levels, balance, procedural generation, replayability, narrative, quests, NPC AI, camera, rendering, sound, interactive music, UX, accessibility, localization, save/content pipelines, and content QA.

> This is an experimental workflow and knowledge package. It does not replace human creative direction, real player testing, professional accessibility review, or engine-specific verification in a real project.

[中文说明](README.zh-CN.md) · [Release notes](RELEASE_NOTES.md) · [First-release guide](docs/RELEASE_GUIDE.zh-CN.md) · [Roadmap](ROADMAP.md)

## What is included

- **27 specialist agent definitions** with bounded responsibilities
- **1 orchestrator** for evidence intake, routing, synthesis, and acceptance
- **8 modular Skills** that can also be used without a multi-agent runtime
- structured JSON contracts and examples for gameplay, music, events, levels, balance, generators, quests, NPC AI, accessibility, content budgets, and save schemas
- deterministic routing, audit, analysis, validation, installation, diagnosis, and release-build tools
- Godot GDScript integration examples
- checklists, templates, knowledge notes, pressure scenarios, and regression tests
- a Codex project policy example for implicit Skill use and minimal specialist selection

## Team coverage

```text
Godot Content Orchestrator
├─ Evidence Intake / Reference Research
├─ Content Production & Scope
├─ Character Motion: Locomotion / Action / Acting
├─ Gameplay: Core Loop / Systems / Encounters
├─ Level Design / Balance / PCG / Run Variation
├─ Narrative / Quest / Cinematics
├─ NPC AI / Simulation
├─ Camera / Asset Style / Technical Art
├─ Interactive Music / Sound & Voice / Godot Audio
├─ UX / Accessibility / Localization
├─ Content Architecture / Save / Tools / Godot Integration
└─ Playtest Analysis
             ↓
      Content QA Automation
             ↓
        QA Acceptance
```

The orchestrator should select the smallest relevant set. It should not start all specialists for every request, and specialists should not concurrently edit the same shared Godot resource.

## Quick start

Validate the repository:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_public_release.py
python tests/validate_package.py
python -m unittest discover -s tests -v
```

Install it into a Codex project:

```bash
python scripts/install.py \
  --target codex \
  --preset godot-content-team \
  --destination /path/to/your/godot-project

python scripts/doctor.py /path/to/your/godot-project
```

The installer places discoverable Skills under `.agents/skills/`. If the destination does not already contain `AGENTS.md`, it installs the included project routing policy.

## Example request

You do not need to name every specialist manually:

```text
Review the second phase of this boss encounter. The attack animation lacks weight,
the arena pacing is repetitive, the adaptive music transition is abrupt, and reloading
from a save sometimes restores the wrong boss state. Analyze first, then propose a
prioritized Godot implementation plan with acceptance tests.
```

The root Skill and project policy are designed to route that request to only the relevant domains, synthesize shared event contracts, and keep final edits under one owner.

## Main entry points

- `SKILL.md` — root Skill and mandatory orchestration contract
- `agents/orchestrator.md` — main orchestration role
- `agents/routing-table.md` — specialist routing rules
- `codex/AGENTS.md.example` — Codex project policy example
- `skills/` — 8 independently installable module Skills
- `scripts/build_dispatch_plan.py` — deterministic specialist router
- `scripts/validate_public_release.py` — public repository validator
- `scripts/install.py` / `scripts/doctor.py` — installation and diagnosis
- `tests/` — regression, routing, schema, and tool tests

## Build a GitHub Release attachment

```bash
python scripts/build_release.py --version v0.1.0-alpha --clean
```

Output:

```text
dist/godot-game-development-director-v0.1.0-alpha.zip
dist/SHA256SUMS
```

The release builder uses a sorted file list and fixed ZIP timestamps so identical repository contents produce reproducible archives.

## Scope and maturity

This public preview focuses on game-content development. It does **not** provide complete workflows for store publishing, console certification, marketing, legal advice, privacy compliance, LiveOps, payments, or production online backends.

Validated in this repository:

- package structure and required public files
- Python syntax and unit tests
- JSON and YAML parsing
- structured example contracts
- deterministic archive construction, SHA-256 generation, and ZIP CRC
- basic forbidden-file and high-confidence credential-pattern checks

Not fully validated:

- GDScript examples in every supported Godot version
- behavior across every multi-agent runtime
- production use across all genres and project scales

The included GDScript files are adaptation examples, not universal plugins. Compile and test them in the exact Godot version and project architecture you use.

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Do not submit commercial-game copies, unlicensed assets, private project data, credentials, or substantial copyrighted source material.

Agent runtimes may execute commands and edit files. Review permissions and keep human approval for publishing, pushing, deletion, visibility changes, and credential access. See [SECURITY.md](SECURITY.md).

## License and attribution

The repository is licensed under Apache-2.0. External sources remain the property of their respective owners; this project links to and summarizes them rather than intentionally redistributing source assets. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [SOURCES.md](SOURCES.md).

Godot is a trademark of the Godot Foundation. This independent community project is not affiliated with or endorsed by the Godot Foundation.
