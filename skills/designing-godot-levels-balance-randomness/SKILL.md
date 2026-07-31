---
name: designing-godot-levels-balance-randomness
description: Use when a Godot game's levels, difficulty curve, combat balance, procedural generation, roguelike runs, random events, loot tables, map variation, fairness, replayability, or challenge intensity feel arbitrary, repetitive, unreadable, unfair, unstable, or impossible to tune. 当拓扑、难度、seed、硬约束和局内变化需要可复现验收时使用。
---

# Designing Godot Levels, Balance, and Randomness

## 边界 / Boundary

负责空间拓扑、全局挑战模型、随机约束、seed 可复现和局内变化池；核心机制语义、任务故事、NPC 决策和运行时表现由对应领域负责。

开始前必须取得玩家能力边界、目标强度、拓扑/生成表示、失败 seed、参数版本和分层运行数据。无法复现的“随机不公平”先补 seed 与遥测，不先调概率。

## 核心原则

随机不是设计的替代品。先定义玩家能力、空间语法、硬约束、挑战目标和失败可读性，再让随机系统在安全的可能性空间内变化。

## 责任拆分

- **Level Architecture**：关键路径、支路、地标、门锁、视线、空间功能、教学和恢复。
- **Balance & Difficulty**：挑战维度、技能分层、数值边界、难度曲线、公平性和适应策略。
- **Procedural Generation**：seed、表示法、生成管线、硬约束、验证、修复、fallback 和 expressive range。
- **Run Variation**：遭遇池、随机事件、构筑草案、mutator、anti-repeat、pity/reroll 和局内叙事。

## 工作流

1. 写可观察的体验目标与玩家能力边界。
2. 建立关卡拓扑：起点、目标、关键路径、支路、门锁、恢复和地标。
3. 把强度拆成信息、决策、执行、资源和协作维度；不要只提高血量和伤害。
4. 给每个随机系统写硬约束、概率、冷却、保底、反重复和可复现 seed。
5. 先生成抽象结构，再验证可玩性与公平，再修复，最后装饰和实例化。
6. 用多 seed 试玩、遥测和 expressive-range 指标检查偏置、坏种子和内容坍缩。
7. 映射到 Godot 的 `RandomNumberGenerator`、`TileMapLayer`、`GridMap`、`AStarGrid2D`、Navigation、Resource、PackedScene 和事件系统。

## 强制输出

- 关卡拓扑与空间职责。
- 强度曲线及恢复段。
- 平衡目标、指标、参数边界和回滚条件。
- 随机系统的 seed、权重、约束、冷却、保底与反重复规则。
- 生成管线：represent → generate → validate → repair → decorate → instantiate。
- 坏种子复现信息与安全 fallback。
- 试玩假设、样本分层、通过阈值和失败阈值。
- 参数/内容版本、owner、受影响路径、回滚和明确 fallback。

## 禁止

- 以“每局不同”代替有意义的策略差异。
- 生成后才检查路径可达、钥匙顺序、出生安全或资源下限。
- 无限重试直到“碰巧可用”。必须有次数上限和确定性 fallback。
- 暗中修改命中规则、敌人读招或玩家已掌握的机制来制造动态难度。
- 只看平均完成率，忽略坏 seed、极端尾部、路径单一和死亡热点。
