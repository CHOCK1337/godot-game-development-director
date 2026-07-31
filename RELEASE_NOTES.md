# Godot Game Development Director v0.1.0-alpha.1

This hardening preview turns the original broad guidance package into a self-contained, testable Codex Skill/plugin distribution.

## Highlights

- one explicitly invoked cross-domain director plus 8 independently discoverable module Skills
- 27 specialist roles, one orchestrator, and a generator for 28 project-scoped Codex custom agents
- distinct `director`, `modules`, and `full` installation presets with legacy aliases
- opt-in, non-overwriting project `AGENTS.md`
- Codex plugin manifest and per-Skill `agents/openai.yaml`
- 36 balanced routing evals, including negative and incomplete-evidence cases
- relative-reference validation that catches files missing from installed Skills
- Doctor verification of Skill metadata, referenced resources, receipts, and custom-agent TOML
- pinned Godot 4.6.3 live compilation and deterministic smoke checks for all 9 GDScript examples
- commit-pinned GitHub Actions, verified Godot download, release attestation, and immutable release semantics

## Verification gates

- public release structure, UTF-8, forbidden file, and focused secret-pattern checks
- JSON/YAML/TOML and Python syntax parsing
- Skill frontmatter, UI metadata, self-contained references, and balanced routing evals
- package contracts and Python unit tests
- full installation/Doctor regression tests for all presets and legacy aliases
- deterministic ZIP, SHA-256, and CRC checks
- real Godot 4.6.3 headless GDScript compilation and smoke assertions

## Remaining limitations

- live validation covers the pinned Godot 4.6.3 Linux build, not every supported 4.x release or platform
- generated project agents still depend on the target Codex runtime's custom-agent support
- the examples must be adapted to the target project's architecture and authoritative state model
- real player testing and professional accessibility review remain required
- publishing, storefront, legal/privacy, LiveOps, and production online backends remain out of scope
