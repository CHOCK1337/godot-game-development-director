# Godot Game Development Director

**Version:** `v0.1.0-alpha.1` · **Status:** public preview · **License:** Apache-2.0

Godot Game Development Director is a bilingual, evidence-driven package for coordinating playable game-content work. It combines **one cross-domain director Skill, 8 modular Skills, 27 specialist roles, one orchestrator, structured contracts, deterministic validators, and Godot-oriented implementation examples**.

It covers gameplay, levels, balance, procedural generation, replayability, narrative, quests, NPC AI, camera, rendering, sound, interactive music, UX, accessibility, localization, content data, saves, tools, and content QA.

> This package does not replace human creative direction, real player testing, professional accessibility review, or verification inside the target Godot project.

[中文说明](README.zh-CN.md) · [Release notes](RELEASE_NOTES.md) · [Release guide](docs/RELEASE_GUIDE.zh-CN.md) · [Roadmap](ROADMAP.md)

## Why this revision is stricter

Earlier guidance could route almost any Godot request through the whole team. This revision makes the boundaries executable:

- the director activates for cross-domain ownership and shared-state problems, not every Godot task;
- each module has its own UI metadata and positive, indirect, incomplete-evidence, and negative routing evaluations;
- installed Skills are self-contained, so documented relative scripts and references still exist after installation;
- installation presets have distinct scopes and a receipt that Doctor verifies;
- project `AGENTS.md` is opt-in and is never silently overwritten;
- the full Codex preset generates 28 project-scoped custom agents from the canonical role files;
- all 9 shipped GDScript examples are compiled and smoke-tested with pinned Godot 4.6.3 in CI;
- release Actions are commit-pinned, archives are attested, and existing tags/releases are immutable.

## What is included

- **27 specialist agent definitions** with bounded responsibilities
- **1 orchestrator** for routing, synthesis, shared ownership, and acceptance
- **1 cross-domain director + 8 modular Skills**
- Skill UI metadata and 36 balanced routing evaluation cases
- JSON contracts and examples for gameplay, events, levels, balance, generation, quests, NPC AI, accessibility, content budgets, and saves
- installation, diagnosis, routing, audit, analysis, validation, and deterministic release tools
- 9 GDScript integration examples plus a live-engine headless fixture
- checklists, templates, knowledge notes, pressure scenarios, and regression tests
- Codex plugin metadata and an optional project policy template

## Installation

Install validation dependencies first:

```bash
python -m pip install -r requirements-dev.txt
```

Recommended full Codex project installation:

```bash
python scripts/install.py \
  --target codex \
  --preset full \
  --destination /path/to/your/godot-project

python scripts/doctor.py /path/to/your/godot-project
```

The `full` preset installs 9 Skills under `.agents/skills/` and 28 project-scoped Codex agents under `.codex/agents/`.

| Preset | Installed scope |
|---|---|
| `director` | cross-domain director only |
| `modules` | 8 independent domain Skills, without the director |
| `full` | director + 8 modules; also installs project Codex agents when `--target codex` |

Legacy aliases remain compatible: `core → director`, `skills-only → modules`, and `godot-content-team → full`.

To copy the optional routing policy when the project does not already have one, add `--write-agents-md`. Existing `AGENTS.md` files are preserved even with `--force`.

The repository is also shaped as a Codex plugin through `.codex-plugin/plugin.json`; its 9 discoverable Skills live under `skills/`.

## How to use it

For a cross-domain request, name the director explicitly:

```text
Use $directing-godot-game-feel to review the second phase of this boss.
The quest flag, guard AI, camera, music, and save state disagree after reload.
Route only the necessary domains and give me owners, implementation order,
automated checks, human acceptance thresholds, and rollback.
```

For a narrow task, invoke a module directly, for example:

```text
Use $designing-npc-ai-simulation to diagnose why this guard knows the
player position through walls and freezes after an invalid path.
```

The director should select the smallest relevant team. Specialists that share quest state, save schema, events, seeds, topology, resources, or files must be sequenced rather than writing concurrently.

## Validation

Repository and regression gates:

```bash
python scripts/validate_public_release.py
python tests/validate_package.py
python -m unittest discover -s tests -v
```

Live Godot validation:

```bash
python scripts/run_godot_validation.py --godot /path/to/godot4
```

CI downloads the official `Godot_v4.6.3-stable_linux.x86_64.zip`, verifies its pinned SHA-256, compiles every shipped `.gd` file, and runs deterministic smoke assertions. This proves syntax and the included smoke contracts in that engine build; it does not prove compatibility with every Godot 4.x release or every game architecture.

## Main entry points

- `SKILL.md` — source director contract
- `skills/` — plugin-ready director plus 8 self-contained modules
- `agents/orchestrator.md` and `agents/routing-table.md` — canonical team roles and routing
- `scripts/install.py` and `scripts/doctor.py` — scoped installation and integrity diagnosis
- `scripts/generate_codex_agents.py` — project custom-agent adapter
- `scripts/validate_skill_references.py` and `scripts/validate_skill_evals.py` — Skill integrity gates
- `tests/godot_fixture/` — real-engine compilation and smoke fixture
- `codex/AGENTS.md.example` — optional project policy template

## Build a release attachment

```bash
python scripts/build_release.py --version v0.1.0-alpha.1 --clean
```

Output:

```text
dist/godot-game-development-director-v0.1.0-alpha.1.zip
dist/SHA256SUMS
```

The builder uses sorted paths and fixed ZIP timestamps. The release workflow requires an existing tag pointing to the validated commit, refuses to replace an existing GitHub Release, and attests the ZIP.

## Scope and limitations

This preview focuses on game-content development. Store publishing, console certification, marketing, legal advice, privacy compliance, LiveOps, payments, and production online backends are out of scope.

The GDScript files are adaptation examples, not universal plugins. Real acceptance still requires the target project, its exact Godot version, representative saves, target devices, language/input/accessibility matrices, and human playtesting.

## Contributing, security, and license

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Do not submit private project data, credentials, commercial-game copies, unlicensed assets, or substantial copyrighted source material. Review runtime permissions and retain human approval for publishing, pushing, deletion, visibility changes, and credential access; see [SECURITY.md](SECURITY.md).

The repository is licensed under Apache-2.0. External sources remain the property of their owners; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [SOURCES.md](SOURCES.md).

Godot is a trademark of the Godot Foundation. This independent community project is not affiliated with or endorsed by the Godot Foundation.
