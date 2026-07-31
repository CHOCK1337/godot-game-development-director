---
name: building-godot-content-pipelines
description: Use when Godot quests, dialogue, enemies, items, levels, assets, save data, editor tools, imports, IDs, migrations, validation, or content iteration are scattered, fragile, repetitive, or hard to test. 当内容数据、稳定 ID、存档迁移和制作工具需要统一合同与回归门禁时使用。
---

# Building Godot Content Pipelines

## Boundary / 边界

Own content schemas, stable identity, persistence, migrations, authoring tools, batch validation, and observability. Do not decide quest meaning, combat balance, visual style, or level topology.

负责内容 Schema、稳定身份、持久化、迁移、制作工具、批量验证和可观察性；不替代叙事、平衡、美术或关卡专业判断。

## Required evidence / 所需证据

- Representative current and legacy content/save files.
- Current schema versions, IDs, references, load order, and mutation owners.
- Authoring/import workflow, failure logs, target platforms, and compatibility promise.
- The exact cold-start/reload path; database or file repair alone is not acceptance.

## Core rule / 核心原则

Content scales through stable data contracts and tooling, not copied scenes and magic strings.

## Requirements / 要求

- Stable content IDs; no persistent NodePath identity.
- Custom Resources for authored data; Nodes for runtime presence.
- One authority for mutable state; semantic events for consumers.
- Versioned save schema with sequential migrations, atomic replacement and backup.
- Editor/batch validators for missing refs, duplicate IDs, graph reachability and budgets.
- Diagnostic context: content ID, version, seed, state and event.

## Migration gate / 迁移门禁

For every version step define input fixture, pure transform, validation, backup, atomic replacement, unknown-key behavior, failure recovery, and a real reopen check. Never skip directly across untested versions.

## Required output / 强制输出

Schema and owner table; stable-ID policy; sequential migration graph; authoring/import flow; validator list; observability fields; affected files; compatibility matrix; cold-reopen acceptance; rollback and backup restoration.

Validate with `scripts/validate_save_schema.py` and domain validators before multiplying content.
