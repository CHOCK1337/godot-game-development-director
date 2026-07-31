---
name: designing-npc-ai-simulation
description: Use when Godot enemies, companions, crowds, schedules, perception, pathfinding, behavior trees, utility AI, or simulated characters feel stupid, omniscient, unreadable, repetitive, stuck, or expensive. 当 NPC 感知、知识、决策、导航或恢复需要可解释状态合同时使用。
---

# Designing NPC AI & Simulation

## Boundary / 边界

Own perception, knowledge/memory, decision selection, intent commitment, recovery, schedules, and simulation budgets. Action owns motion readability; Navigation owns path queries; character controllers own movement; animation consumes intent.

负责 NPC 看见什么、记住什么、为什么选择、如何恢复；不把寻路、物理移动、动画和决策混成一个黑箱。

## Required evidence / 所需证据

- Reproducible scene, NPC ID, stimuli, current state, selected intent, target, scores, cooldown, and path status.
- Collision/navigation layers, crowd count, target hardware, save/re-entry behavior, and failure video/log.
- Explicit statement of what the NPC is allowed to know and how that knowledge decays.

## Core rule / 核心原则

Good game AI is legible and recoverable, not maximally intelligent. Separate perception, memory, decision, action, movement and animation.

## Workflow / 工作流

1. State what the NPC may know and how knowledge decays.
2. Choose FSM/BT/Utility/planning only after defining decisions.
3. Give every state exit, interruption and fallback.
4. Separate Navigation path query, avoidance, physics movement and animation.
5. Expose reason, target, score, stimulus, cooldown and path status in debug output.
6. Test impossible paths, target loss, crowd pressure, low FPS, save/load and scene re-entry.

## Required output / 强制输出

Knowledge table; state/decision graph; transition triggers and interrupts; intent/action contract; navigation and movement ownership; debug trace fields; CPU/update budget; failure/recovery matrix; save/re-entry tests; rollback.

Use `scripts/validate_npc_ai_spec.py` before implementation.
