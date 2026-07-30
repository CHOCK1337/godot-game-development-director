---
name: directing-godot-game-feel
description: Use when a Godot game's motion, gameplay, levels, balance, procedural generation, narrative, quests, NPC AI, camera, rendering, sound, UX, localization, save/content pipelines, adaptive BGM, VFX, UI, or generated assets feel stiff, generic, unfair, unreadable, repetitive, disconnected, fragile, poorly synchronized, hard to complete, or obviously AI generated.
---

# Directing Godot Game Development Content

## 核心原则

完整内容团队不是 Agent 数量，而是从玩家目标到可验证内容的因果链完整：范围、规则、空间、角色行为、任务状态、动作、镜头、声音、界面、资产预算、存档与测试必须共享同一事实。

本版本只专注游戏内容完善。**不处理发行、商店、评级、营销、法律、隐私、LiveOps 或线上服务。**

## 使用症状

- 角色动作僵硬、滑脚、漂浮、攻击和交互无重量。
- 核心循环浅、机制堆砌、关卡迷路、平衡靠加血、随机玩法是假多样性。
- 剧情像 AI 写作、角色同语气、任务分支无后果、重载后状态错乱或出现软锁。
- NPC 偷看玩家、决策重复、导航卡死、行为无法解释或群体拥堵。
- 相机遮挡、锁定抖动、震动过度、Cutscene 返回后输入/目标错误。
- SFX/脚步/VO 同质、重复触发、混音糊成一团或 BGM 掩盖提示。
- Shader、透明、粒子、灯光、骨骼和纹理没有预算，低端配置删掉玩法信号。
- HUD/菜单不一致、输入不能重映射、字幕/减少运动/本地化缺失。
- 内容散落在场景脚本、ID 不稳定、存档无版本迁移、复制内容越做越脆。
- 内容很多但没有 owner、依赖、冻结、验收和回归矩阵。

## 8 个可独立安装的 Skills

- `skills/designing-godot-gameplay/SKILL.md`
- `skills/directing-interactive-game-music/SKILL.md`
- `skills/designing-godot-levels-balance-randomness/SKILL.md`
- `skills/producing-game-content/SKILL.md`
- `skills/authoring-narrative-quests-cinematics/SKILL.md`
- `skills/designing-npc-ai-simulation/SKILL.md`
- `skills/polishing-game-presentation-accessibility/SKILL.md`
- `skills/building-godot-content-pipelines/SKILL.md`

## 27 个专家职责组

- 证据/参考：Evidence Intake、Reference Research。
- 内容管理：Content Production & Scope。
- 动作：Locomotion、Action、Acting。
- 玩法：Core Loop、Systems/Economy、Encounter/Pacing。
- 关卡与随机：Level Architecture、Balance/Difficulty、Procedural Generation、Run Variation。
- 叙事与角色：Narrative/Quest/Cinematics、NPC AI/Simulation。
- 镜头与表现：Gameplay Camera、Asset Style、Technical Art/Rendering。
- 音频：Interactive Music、Sound Design/Voice/Mix、Godot Audio。
- UX 与内容工程：UX/Accessibility/Localization、Content Architecture/Save/Tools、Godot Integration。
- 验证：Playtest Analysis、Content QA Automation、QA Acceptance。

## 执行模式

1. Single：单一问题域。
2. Parallel Lite：2–3 个独立域。
3. Parallel Full：4–6 个独立域。
4. Two Waves：超过 6 个或存在范围/状态/合同依赖。
5. Sequential/Manual：运行器不支持 Agent。

## 编排硬规则

- 只派会改变最终结论的专家，不为“团队完整”全员启动。
- Content Production 先定义范围和冻结，不覆盖专业结论。
- 共享 Quest State、NPC Knowledge、Save Schema、Event、seed、拓扑、资源或文件的 Agent 不并行写入。
- Narrative 管故事/任务状态；Architecture 管存档/数据；Level 管空间；Encounter 管局部压力；NPC AI 管决策；Action 管动作表达。
- Camera、SFX、VFX、UI 和 BGM 只消费权威事件，不自己推断战斗或任务真相。
- Technical Art 以测量和目标设备预算为依据；Asset Style 负责审美与反 AI 味。
- Content QA 在合并后做结构/回归；QA Acceptance 最后做跨域门禁。
- 缺证据时输出验证方案，不编造玩家偏好、性能、可访问性或内容完成度。

## 内容生产流程

1. **范围**：一句话体验、内容支柱、Must/Should/Could/Won't、Vertical Slice。
2. **证据**：视频、工程、任务图、AI 状态、相机模式、cue sheet、预算、存档和测试数据。
3. **玩家因果链**：`输入 → 规则 → 世界/角色状态 → 表现 → 下一决策`。
4. **内容合同**：Gameplay、Level、Balance、Generator、Quest、NPC AI、Camera、Audio、Accessibility、Save。
5. **Godot 所有权**：Resource、Node、Autoload、Event、Navigation、Audio、UI、Save 与工具。
6. **两波执行**：先定范围/状态/接口，再并行制作表现与实现。
7. **验证**：静态合同、状态遍历、场景 smoke、语言/输入/设置矩阵、预算压力和真人试玩。

## 新增结构化合同

- Quest Spec：节点、边、终点、失败、存档键。
- NPC AI Spec：状态、转移、感知、fallback、调试字段。
- Content Budget：目标设备预算与实测值。
- Accessibility/Localization Spec：语言、字幕、输入、减少运动、文本膨胀和 screen reader。
- Save Schema：版本、逐步迁移、原子写入、备份和未知键策略。

## 最终输出合同

1. 一句话体验与范围判定。
2. 证据表、置信度和未知项。
3. 最多三项阻塞级根因。
4. 玩家因果链和 Gameplay Event Contract。
5. 相关领域合同：Gameplay/Level/Balance/Generator/Quest/NPC/Camera/Audio/UX/Save。
6. Godot 实施边界、共享文件风险和迁移计划。
7. 内容预算、降级策略和素材需求。
8. 自动测试、人工测试、回滚和完成门槛。
9. 明确 backlog 与删除项，不把所有建议都塞进当前版本。

## 入口

- `agents/orchestrator.md`
- `agents/routing-table.md`
- `agents/godot-game-feel-swarm.yaml`
- `scripts/build_dispatch_plan.py`
- `codex/AGENTS.md.example`

最终判断必须回到实际玩家行为、任务/世界状态、NPC 可读性、镜头和声音信息、可访问性、内容预算、存档兼容和真人试玩。
