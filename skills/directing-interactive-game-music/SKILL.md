---
name: directing-interactive-game-music
description: Use when game BGM, adaptive music, combat music, exploration music, boss music, stems, loops, stingers, transitions, or Godot audio behavior feel generic, repetitive, constantly intense, poorly synchronized, abrupt, noisy, or disconnected from gameplay states. 当音乐功能、状态轴、量化转场和声音空间需要可验证映射时使用。
---

# Directing Interactive Game Music

## 边界 / Boundary

负责 BGM 身份、motif、状态轴、水平/垂直结构、stinger、动态范围和留白；Gameplay 产生权威状态，Godot Audio 负责播放器、Bus、并发和运行时消费。

开始前收集 gameplay state/event 时间线、cue/stem 文件、BPM/拍号/loop 点、对白与 SFX 优先级、暂停恢复和频繁抖动案例；只有“更史诗”不足以开始编曲建议。

## 原则

互动配乐不是“给场景配一首歌”，而是把音乐参数映射到有意义、稳定、可预测的游戏状态。音乐必须帮助玩家理解节奏、危险、空间、身份或结果，同时给 SFX、对白和安静留出空间。

## 工作流

1. 定义音乐职责：情绪、信息、身份、节奏或空间。
2. 选择 1–3 个稳定状态轴，例如 intensity、danger、location、narrative phase。
3. 设计水平重组、垂直混音、stinger 或它们的最小组合。
4. 为每个状态定义进入阈值、退出阈值、最短停留、冷却和 fallback。
5. 定义 beat/bar/phrase 转场、stem 同步、loop seam 和响度层级。
6. 映射 Godot 节点、资源、bus、ducking、事件和存档/暂停行为。
7. 在无音乐、仅 SFX、低帧率、频繁状态波动和暂停恢复下验收。

## 强制输出

- 音乐状态图与状态轴。
- stem/段落职责，而不是只有曲风名称。
- 转场表、stinger、滞回和冷却。
- Audio Bus 优先级与 ducking。
- Gameplay Event Contract。
- Godot 实施与 fallback。
- 音乐/事件 owner、受影响资源、可听验收阈值、无音乐降级与回滚。

## 禁止

- 每次数值波动都切歌。
- 全程满配器、满响度、满情绪。
- 用“史诗、电影感、氛围感”代替音乐功能。
- 复制特定作品的旋律、和声进行或独特编曲身份。
