---
name: authoring-narrative-quests-cinematics
description: Use when Godot narrative, dialogue, quests, branching choices, character continuity, environmental storytelling, cutscenes, or story state can soft-lock, contradict gameplay, or feel generic and AI-written.
---

# Authoring Narrative, Quests & Cinematics

## Core rule

Narrative content must be grounded in world state and player action. Different words without different knowledge, cost, consequence or future state are not meaningful branches.

## Contract

- Quest graph: start, objectives, branches, terminal/fail states and re-entry.
- Stable IDs: quest, node, line, character, item and location.
- State ownership: one authority; UI, dialogue and save consume it.
- Dialogue: speaker knowledge, intent, relationship, reveal and localization context.
- Cinematics: gameplay handoff, skip/recovery, camera, animation, VO/SFX and state commit.

## Validation

Run `scripts/validate_quest_spec.py` and test abandon, reload, sequence break, skipped cutscene, missing item, dead NPC and localized dialogue expansion.
