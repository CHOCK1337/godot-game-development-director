# Level, Balance, and Randomness Extension Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend Godot Game Feel Director v4 with level architecture, balance/difficulty, procedural generation, and replayability/run-variation capabilities.

**Architecture:** Add four isolated specialists behind the existing orchestrator, one independently installable Skill, three JSON contracts, deterministic validation/analysis tools, and Codex-ready routing guidance. Existing encounter pacing remains responsible for local dramatic rhythm; new specialists own spatial structure, global balance, generation correctness, and run variety.

**Tech Stack:** Markdown Agent Skills, YAML routing configuration, JSON Schema, Python 3 standard library, Godot 4 GDScript examples.

## Global Constraints

- Use Godot stable documentation as the technical baseline.
- Random systems must be reproducible through explicit seeds and RNG state.
- No specialist writes shared Godot resources concurrently.
- Keep hard generator invariants separate from soft scoring objectives.
- Every difficulty adaptation requires an observable trigger, bounded intervention, cooldown, player-respect rule and rollback condition.

---

### Task 1: RED tests for package and routing

**Files:**
- Modify: `tests/validate_package.py`
- Modify: `tests/test_dispatch_plan.py`

- [ ] Require 18 specialists and new Skill/Agent/schema/script files.
- [ ] Add routing tests for level architecture, difficulty balance, PCG and run variation.
- [ ] Run tests and confirm failure due to missing implementation.

### Task 2: Specialists, Skill and knowledge base

**Files:**
- Create: `skills/designing-godot-levels-balance-randomness/SKILL.md`
- Create: `agents/specialists/level-design-architecture.md`
- Create: `agents/specialists/balance-difficulty.md`
- Create: `agents/specialists/procedural-generation-randomness.md`
- Create: `agents/specialists/replayability-run-variation.md`
- Create: `knowledge/21-level-design-architecture.md`
- Create: `knowledge/22-balance-difficulty-models.md`
- Create: `knowledge/23-procedural-generation-randomness.md`
- Create: `knowledge/24-replayability-run-variation.md`
- Create: `knowledge/25-godot-level-generation.md`
- Create: `knowledge/26-level-randomness-ai-taste-atlas.md`

- [ ] Define non-overlapping responsibilities and output contracts.
- [ ] Encode research-backed design rules and Godot mappings.

### Task 3: Structured specifications and validators

**Files:**
- Create: `agents/level-spec.schema.json`
- Create: `agents/balance-model.schema.json`
- Create: `agents/generator-spec.schema.json`
- Create: `scripts/validate_level_spec.py`
- Create: `scripts/validate_balance_model.py`
- Create: `scripts/validate_generator_spec.py`
- Test: `tests/test_validate_level_spec.py`
- Test: `tests/test_validate_balance_model.py`
- Test: `tests/test_validate_generator_spec.py`

- [ ] Write failing validator tests.
- [ ] Implement minimum validators.
- [ ] Verify tests pass.

### Task 4: Randomness and telemetry tooling

**Files:**
- Create: `scripts/audit_random_table.py`
- Create: `scripts/analyze_level_runs.py`
- Test: `tests/test_audit_random_table.py`
- Test: `tests/test_analyze_level_runs.py`

- [ ] Test streak risk, zero-weight entries and probability normalization.
- [ ] Test seed outlier, room-death concentration and path-diversity reporting.
- [ ] Implement and verify.

### Task 5: Routing and orchestration integration

**Files:**
- Modify: `scripts/build_dispatch_plan.py`
- Modify: `agents/godot-game-feel-swarm.yaml`
- Modify: `agents/routing-table.md`
- Modify: `agents/orchestrator.md`
- Modify: `agents/portable-orchestrator-prompt.md`
- Modify: `workflows/cross-discipline-pipeline.md`

- [ ] Add tag sets and shared-dependency rules.
- [ ] Preserve minimal-agent routing and six-agent wave limit.
- [ ] Verify routing tests.

### Task 6: Templates, checklists, examples and Codex adapter

**Files:**
- Create: `templates/level-spec.md`
- Create: `templates/balance-model.template.json`
- Create: `templates/generator-spec.template.json`
- Create: `templates/run-variation-plan.md`
- Create: `checklists/level-design.md`
- Create: `checklists/balance-difficulty.md`
- Create: `checklists/procedural-generation.md`
- Create: `checklists/run-variation.md`
- Create: `examples/13-level-spec.json`
- Create: `examples/14-balance-model.json`
- Create: `examples/15-generator-spec.json`
- Create: `examples/16-level-runs.csv`
- Create: `examples/17-level-randomness-orchestration.md`
- Create: `examples/18-dispatch-brief-level-random.json`
- Create: `scripts/godot_seeded_generation_context.gd`
- Create: `codex/AGENTS.md.example`
- Create: `codex/config.toml.example`

- [ ] Provide runnable examples and installation guidance.

### Task 7: Documentation, sources, manifest and full verification

**Files:**
- Modify: `README.md`
- Modify: `SKILL.md`
- Modify: `SOURCES.md`
- Modify: `CHANGELOG.md`
- Modify: `MANIFEST.json`
- Modify: `tests/validate_package.py`

- [ ] Run all unit tests.
- [ ] Parse all JSON/YAML and compile all Python scripts.
- [ ] Run every validator against examples.
- [ ] Build ZIP, verify archive and compute SHA-256.
