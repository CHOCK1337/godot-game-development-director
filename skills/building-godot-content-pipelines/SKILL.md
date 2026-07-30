---
name: building-godot-content-pipelines
description: Use when Godot quests, dialogue, enemies, items, levels, assets, save data, editor tools, imports, IDs, migrations, validation, or content iteration are scattered, fragile, repetitive, or hard to test.
---

# Building Godot Content Pipelines

## Core rule

Content scales through stable data contracts and tooling, not copied scenes and magic strings.

## Requirements

- Stable content IDs; no persistent NodePath identity.
- Custom Resources for authored data; Nodes for runtime presence.
- One authority for mutable state; semantic events for consumers.
- Versioned save schema with sequential migrations, atomic replacement and backup.
- Editor/batch validators for missing refs, duplicate IDs, graph reachability and budgets.
- Diagnostic context: content ID, version, seed, state and event.

Validate with `scripts/validate_save_schema.py` and domain validators before multiplying content.
