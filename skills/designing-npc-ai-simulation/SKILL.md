---
name: designing-npc-ai-simulation
description: Use when Godot enemies, companions, crowds, schedules, perception, pathfinding, behavior trees, utility AI, or simulated characters feel stupid, omniscient, unreadable, repetitive, stuck, or expensive.
---

# Designing NPC AI & Simulation

## Core rule

Good game AI is legible and recoverable, not maximally intelligent. Separate perception, memory, decision, action, movement and animation.

## Workflow

1. State what the NPC may know and how knowledge decays.
2. Choose FSM/BT/Utility/planning only after defining decisions.
3. Give every state exit, interruption and fallback.
4. Separate Navigation path query, avoidance, physics movement and animation.
5. Expose reason, target, score, stimulus, cooldown and path status in debug output.
6. Test impossible paths, target loss, crowd pressure, low FPS, save/load and scene re-entry.

Use `scripts/validate_npc_ai_spec.py` before implementation.
