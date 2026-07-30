# Godot Game Development Director v6 Content Team Design

## Goal

把 v5 的动作、玩法、关卡、随机、音乐与工程审查团队，扩展为可覆盖完整游戏内容生产的 27 专家团队，同时明确排除发行、商店、评级、营销、隐私合规、LiveOps 和线上服务。

## New domains

1. Content Production & Scope：内容支柱、范围、里程碑、依赖和冻结标准。
2. Narrative / Quest / Cinematics：世界观、任务图、对话、演出和叙事状态。
3. NPC AI & Simulation：感知、决策、导航、群体和调试可解释性。
4. Gameplay Camera & Composition：跟随、瞄准、遮挡、震动、镜头语言和运动舒适度。
5. Technical Art & Rendering：资源预算、材质/Shader、LOD、灯光、粒子和性能。
6. Sound Design / Voice / Mix：SFX、Foley、环境、对白、空间化和动态混音。
7. UX / Accessibility / Localization：HUD、菜单、输入、字幕、减少运动、文本膨胀和多语言。
8. Content Architecture / Save / Tools：数据驱动资源、存档版本、迁移、编辑器工具和内容验证。
9. Content QA Automation：任务软锁、NPC 状态、内容覆盖、输入/语言/分辨率和回归矩阵。

## Architecture

- Root Orchestrator routes the smallest relevant team.
- Specialists analyze isolated domains and do not concurrently edit shared Godot resources.
- Shared contracts cover quest graph, NPC AI, content budget, accessibility/localization and save schema.
- Content Production owns scope conflicts; Orchestrator owns synthesis; Content QA and QA Acceptance run after synthesis.
- Codex implicit use is supported through root Skill descriptions and an AGENTS.md routing policy; manual @agent is not required.

## Verification

- Unit tests for every new validator and router branch.
- JSON Schema validation for examples.
- Full legacy v5 test suite must remain green.
- Package validator requires exactly 27 specialists.
- ZIP integrity and manifest hash verification.
- GDScript examples receive static review only because the current environment has no Godot executable.
