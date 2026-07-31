# Codex Setup / Codex 安装

## Recommended / 推荐

From the package root:

```bash
python scripts/install.py \
  --target codex \
  --preset full \
  --destination /path/to/your-godot-project

python scripts/doctor.py /path/to/your-godot-project
```

This installs 9 self-contained Skills under `.agents/skills/` and 28 project-scoped custom agents under `.codex/agents/`. It does not modify global Codex agents.

该命令会安装 9 个自包含 Skill 和 28 个项目级 Custom Agent，不修改全局 Codex Agent。

The project policy template is optional:

```bash
python scripts/install.py \
  --target codex \
  --preset full \
  --write-agents-md \
  --destination /path/to/your-godot-project
```

`--write-agents-md` only creates `AGENTS.md` when absent. Existing project policy is never overwritten, including with `--force`.

## Presets / 预设

- `director`: cross-domain director only.
- `modules`: 8 independent domain Skills.
- `full`: director, modules, and project custom agents.

Legacy aliases remain accepted: `core`, `skills-only`, and `godot-content-team`.

## Invocation / 调用

The director disables broad implicit activation. Use `$directing-godot-game-feel` for a cross-domain request, or invoke a narrow module such as `$designing-npc-ai-simulation` directly.

总 Skill 不会对所有 Godot 请求隐式触发。跨领域任务使用 `$directing-godot-game-feel`；单领域任务直接使用对应模块。

If the runtime has no subagent feature, use the sequential workflow documented in the installed director references. The main task owns shared edits and final verification.
