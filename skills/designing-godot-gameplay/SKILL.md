---
name: designing-godot-gameplay
description: Use when a Godot game's mechanics, core loop, combat rules, progression, economy, encounters, difficulty, onboarding, rewards, or player choices feel generic, overloaded, shallow, arbitrary, repetitive, or disconnected from the intended experience.
---

# Designing Godot Gameplay

## 原则

玩法不是功能数量，而是玩家在规则和反馈下反复做出的有意义决策。每个机制必须回答：玩家看见什么、能做什么、为什么现在做、付出什么、状态如何变化、如何知道结果、下一步决策是什么。

## 工作流

1. 写一句核心体验，不使用“有趣、沉浸、爽”。
2. 建立 `输入 → 规则 → 状态变化 → 反馈 → 下一决策`。
3. 列出 3–7 个核心 verbs，删除不改变决策的功能。
4. 检查风险/收益、资源、反制、失败学习和恢复。
5. 检查循环的短期、中期、长期层级是否互相支持。
6. 映射 Godot 状态、数据资源、事件、UI、动画和音频。
7. 写可证伪试玩假设、指标和回滚条件。

## 强制输出

- 核心体验与目标玩家行为。
- 核心循环与 verbs。
- 每个关键机制的规则、成本、反馈、反制和失败。
- 资源 faucet/sink 与成长边界。
- Godot 状态/资源/事件落点。
- 试玩计划与通过/失败阈值。

## 禁止

- 用奖励频率代替决策质量。
- 用轻微数值差伪装 build 选择。
- 用敌人血量和伤害上涨代替难度设计。
- 在没有数据时断言玩家会喜欢、留存会提高。

## 与 v5 专项 Skill 的边界

关卡拓扑、空间可读性、全局难度模型、程序生成、seed 与 Roguelike 随机变化应加载 `designing-godot-levels-balance-randomness`；本 Skill 继续负责核心循环、机制语义、经济和玩家选择。
