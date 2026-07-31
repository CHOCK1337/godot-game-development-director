---
name: authoring-narrative-quests-cinematics
description: Use when Godot narrative, dialogue, quests, branching choices, character continuity, environmental storytelling, cutscenes, or story state can soft-lock, contradict gameplay, or feel generic and AI-written. 当任务状态、角色知识、对白后果或演出交接需要可验证设计时使用。
---

# Authoring Narrative, Quests & Cinematics

## Boundary / 边界

Own story meaning, character knowledge, quest topology, dialogue conditions, and cinematic state commits. Do not own save-file mechanics, level topology, NPC decision architecture, camera implementation, or audio runtime; publish contracts for those owners.

负责故事含义、角色知识、任务图、对白条件和演出提交点；存档实现、关卡空间、NPC 决策、镜头和音频运行时由对应领域负责。

## Required evidence / 所需证据

- Quest graph or current objectives, stable IDs, and authoritative state source.
- Speaker knowledge, intent, relationship, reveal, and previous player actions.
- Save/reload, abandon, skip, re-entry, fail, and sequence-break behavior.
- Target languages, subtitle/VO constraints, and cinematic handoff points.

If these are absent, produce a capture matrix before rewriting content.

## Core rule / 核心原则

Narrative content must be grounded in world state and player action. Different words without different knowledge, cost, consequence or future state are not meaningful branches.

## Contract / 合同

- Quest graph: start, objectives, branches, terminal/fail states and re-entry.
- Stable IDs: quest, node, line, character, item and location.
- State ownership: one authority; UI, dialogue and save consume it.
- Dialogue: speaker knowledge, intent, relationship, reveal and localization context.
- Cinematics: gameplay handoff, skip/recovery, camera, animation, VO/SFX and state commit.

## Godot ownership / Godot 落点

- Authored quest/dialogue data belongs in versioned Resources or external content data with stable IDs.
- One quest authority mutates state; UI, dialogue, world gates, save, camera, and audio consume semantic events.
- Commit irreversible state before/after a cinematic at one explicit boundary, with idempotent skip and reload recovery.

## Required output / 强制输出

Quest graph; knowledge/condition table; line and node IDs; state owner; cinematic commit/skip/recovery table; localization context; affected Godot resources/events; automated graph checks; manual sequence-break matrix; rollback.

## Validation / 验证

Run `scripts/validate_quest_spec.py` and test abandon, reload, sequence break, skipped cutscene, missing item, dead NPC and localized dialogue expansion.
