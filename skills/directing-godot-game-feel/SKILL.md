---
name: directing-godot-game-feel
description: Use when a Godot request crosses multiple content disciplines, needs coordinated specialist ownership, or requires one evidence-backed plan spanning gameplay, levels, narrative, NPC AI, presentation, audio, accessibility, content data, save compatibility, and QA. 当 Godot 问题跨多个内容领域并需要统一编排、接口与验收时使用。
---

# Directing Godot Game Development Content

## Purpose / 用途

Coordinate a minimum sufficient Godot content team around one player-visible outcome. This is the cross-domain director; for a single well-bounded domain, use the matching module Skill directly.

围绕一个可观察的玩家结果，编排最小且足够的 Godot 内容团队。本 Skill 负责跨领域问题；若任务只属于一个明确领域，应直接使用对应模块 Skill。

This package does not cover publishing, storefronts, ratings, marketing, legal, privacy, LiveOps, or online-service operations.

## Trigger boundary / 触发边界

Use this director when at least one condition is true:

- The change crosses two or more authoritative domains, such as quest state + save migration, combat event + camera/audio/UI, or procedural level + balance + QA.
- Several specialists may edit shared state, resources, events, scenes, or files and need ownership sequencing.
- The request asks for a vertical slice, whole-game content review, coordinated polish pass, or end-to-end acceptance plan.
- Evidence is incomplete and the work first needs triage, scope, and a verification plan.

Do not use it merely because the project is made with Godot. Do not activate every specialist for a narrow question.

## Before acting / 行动前

1. Read `references/orchestration-routing.md` for routing, wave order, and conflict rules.
2. Read `references/domain-resource-map.md` only for the domains selected for this task.
3. Read `references/output-contracts.md` before producing the final handoff.
4. If executable dispatch JSON is useful, run `scripts/build_dispatch_plan.py`.

## Evidence packet / 证据包

Collect only evidence that can change the decision:

- Player goal, affected flow, expected and observed result.
- Reproduction steps, Godot version, target devices, scene/resource/script paths.
- Relevant video, screenshots, logs, profiler data, state graphs, save samples, cue sheets, localization/input matrices, or playtest notes.
- Known owners, shared files, frozen interfaces, compatibility constraints, and rollback point.

Label each consequential statement as observed, inferred, proposed, or unknown. Never invent player preference, performance, accessibility coverage, or completion status.

## Orchestration workflow / 编排流程

1. **Frame** — Write one observable player outcome and explicit in/out scope.
2. **Triage** — Identify at most three blocking root causes and the evidence behind them.
3. **Route** — Select only specialists whose conclusions could materially change the result.
4. **Own** — Assign one authority for every mutable state, event, resource, and shared file.
5. **Sequence** — Resolve state contracts and shared interfaces before parallel presentation work.
6. **Implement** — Map decisions to Godot Resources, Nodes, events, tools, and migration steps.
7. **Verify** — Run static validators, headless/scene smoke checks where available, device/language/input matrices, and targeted human playtests.
8. **Accept** — Content QA runs after integration; final QA checks cross-domain behavior and rollback readiness.

## Hard rules / 硬规则

- Content Production owns scope and freeze criteria, not every domain conclusion.
- Narrative owns story/quest meaning; Content Architecture owns persistence and data schema; Level Design owns topology; Encounter Design owns local pressure; NPC AI owns knowledge and decisions.
- Camera, audio, VFX, UI, and music consume authoritative semantic events; they do not infer gameplay truth independently.
- Agents sharing quest state, NPC knowledge, save schema, event contracts, seeds, topology, or the same files do not write in parallel.
- Technical Art uses measured budgets and target profiles. Asset Style owns aesthetic coherence and anti-template judgment.
- Generated or AI-assisted content remains provenance-tracked, editable, and subject to the same review and acceptance gates.
- A passing static check is not a claim of player quality. A passing build is not a substitute for the specified playtest.

## Execution modes / 执行模式

- **Single:** one domain; route to one module and return a compact contract.
- **Parallel Lite:** 2–3 independent domains after shared interfaces are frozen.
- **Parallel Full:** 4–6 independent domains with explicit owners and merge order.
- **Two Waves:** more than 6 domains, or any task with scope/state/schema dependencies.
- **Sequential/Manual:** runtime has no agent support or the same files cannot be safely shared.

## Output contract / 输出合同

For a single-domain request, return four sections:

1. Evidence-backed diagnosis and unknowns.
2. Targeted change, owner, and Godot boundary.
3. Automated and human validation with pass/fail thresholds.
4. Risk, rollback, and deferred work.

For cross-domain work, return nine sections:

1. Player outcome and in/out scope.
2. Evidence table with confidence and unknowns.
3. Up to three blocking root causes.
4. Player causal chain and authoritative event/state contract.
5. Selected domain contracts and owners.
6. Godot implementation boundaries, shared-file risks, and migration order.
7. Content/performance budgets, degradation behavior, and asset needs.
8. Automated checks, human tests, acceptance thresholds, and rollback.
9. Backlog and explicit cuts.

Follow the user's language. Use bilingual field labels only when requested or when the artifact will be shared across Chinese- and English-speaking collaborators. Keep stable machine-readable keys in English.

The final judgment must return to actual player behavior, world/quest state, NPC legibility, audiovisual information, accessibility, budgets, save compatibility, and observed playtesting.
