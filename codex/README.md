# Codex Setup

## Recommended installation

From the package root:

```bash
python scripts/install.py \
  --target codex \
  --preset godot-content-team \
  --destination /path/to/your-godot-project

python scripts/doctor.py /path/to/your-godot-project
```

The installer copies the root Skill and all module Skills under `.agents/skills/` and copies `codex/AGENTS.md.example` to the project root as `AGENTS.md` when no project policy exists.

## Manual installation

1. Copy the root package under `.agents/skills/directing-godot-game-feel/` or another Skill directory recognized by your Codex setup.
2. Copy each module directory from `skills/` into `.agents/skills/`.
3. Copy `AGENTS.md.example` to the Godot project root as `AGENTS.md` and adjust paths if needed.
4. Give a normal task description. The root Skill and project policy tell Codex to triage and select specialists automatically; manual `@agent` naming is not required.
5. Specialists analyze isolated domains. The main thread owns shared edits and final verification.

If the runtime has no subagent feature, follow `workflows/sequential-fallback.md`. For a no-Agent workflow, use `workflows/manual-no-agent.md`.

Exact runtime configuration can change. This package relies on portable prompts, Skill discovery, deterministic routing, and `AGENTS.md` rather than undocumented custom-agent formats.
