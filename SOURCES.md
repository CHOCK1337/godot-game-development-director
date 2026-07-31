# Sources and Update Policy

首次整理日期：2026-07-28；发行规范复核：2026-07-31。技术实现必须按项目实际 Godot stable 版本复核；`latest` 文档可能含未进入 stable 的功能。

## Godot 官方文档

### 随机与程序生成基础
- Random number generation：https://docs.godotengine.org/en/stable/tutorials/math/random_number_generation.html
- RandomNumberGenerator：https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html
- FastNoiseLite（按 stable 版本搜索核对）：https://docs.godotengine.org/en/stable/classes/class_fastnoiselite.html

Godot 使用伪随机数；独立 `RandomNumberGenerator` 可维护自己的 seed/state，适合回放、网络、rewind 和问题复现。本包据此要求拆分 layout/encounter/loot/decor RNG streams。

### 2D/3D 关卡与导航
- TileMapLayer：https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html
- AStarGrid2D：https://docs.godotengine.org/en/stable/classes/class_astargrid2d.html
- Navigation overview：https://docs.godotengine.org/en/stable/tutorials/navigation/index.html
- Using NavigationServer：https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationservers.html
- GridMap：https://docs.godotengine.org/en/stable/tutorials/3d/using_gridmaps.html
- Thread-safe APIs：https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html

`TileMapLayer` 的更新会批处理；Navigation 地图变更通常等待物理帧同步；活动 SceneTree 不是线程安全的；同一 `AStarGrid2D` 对象不能由多个线程并发使用。本包据此采用“后台生成纯数据，主线程实例化”的边界。

### 原有动作与音频
- AnimationTree：https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html
- Retargeting 3D Skeletons：https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html
- Audio buses：https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html
- AudioStreamPlayer：https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html

## 游戏设计与程序生成研究

- Hunicke, LeBlanc, Zubek, *MDA: A Formal Approach to Game Design and Game Research*：
  https://users.cs.northwestern.edu/~hunicke/MDA.pdf
- Shaker, Togelius, Nelson, *Procedural Content Generation in Games*（作者开放版本）：
  https://www.pcgbook.com/
- Springer 书目信息与 DOI：https://link.springer.com/book/10.1007/978-3-319-42716-4
- Smith & Whitehead, *Analyzing the Expressive Range of a Level Generator*，DOI：10.1145/1814256.1814260
- Booth / Valve, *The AI Systems of Left 4 Dead*：
  https://cdn.fastly.steamstatic.com/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf
- Zohaib, *Dynamic Difficulty Adjustment (DDA) in Computer Games: A Review*，DOI：10.1155/2018/5681652
- Isaksen & Nealen, *Comparing Player Skill, Game Variants, and Learning Rates Using Survival Analysis*，DOI：10.1609/aiide.v11i5.12846
- Aramini, Lanzi, Loiacono, *An Integrated Framework for AI Assisted Level Design in 2D Platformers*：https://arxiv.org/abs/1804.09153

## 提炼规则

- MDA 用于追踪机制如何产生运行动态和玩家体验，不作为自动设计公式。
- PCG 书将程序生成视为自动或计算机辅助生成关卡、地形、物品、规则、任务等，并强调多类方法与生成器评估。
- Expressive Range Analysis 用于检查输出分布、偏置和可能性空间空洞；指标必须与项目目标有关。
- Left 4 Dead 的公开说明强调 structured unpredictability、强度估计以及峰值/恢复调度，并明确其示例主要调整节奏频率而非简单改变威胁幅度。
- DDA 研究结果并非“自动适配一定更好”。本包因此要求稳定信号、边界、冷却、玩家尊重和回滚。
- 模拟、搜索、Monte Carlo 和 bot 可用于缩小参数范围，但不能替代真人的可读性、策略和信任测试。

## 版权与参考边界

外部关卡、玩法、音乐、动作和素材只用于提炼通用规律。不得复制独特布局、旋律、角色动作、叙事或视觉资产；生成内容使用前核对许可、训练来源声明与商用边界。


## v6 内容制作团队新增来源

### Godot 官方
- NavigationAgent 路径、跟随与避障：https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html
- Runtime file loading/saving 与 FileAccess：https://docs.godotengine.org/en/stable/tutorials/io/runtime_file_loading_and_saving.html
- Godot 文件系统与可写 `user://`：https://docs.godotengine.org/en/stable/tutorials/scripting/filesystem.html
- Custom Resources：https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html
- Audio streams 与 2D/3D 空间音频：https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html
- Audio effects、compressor、limiter 与 ducking：https://docs.godotengine.org/en/stable/tutorials/audio/audio_effects.html
- Screen reader integration：https://docs.godotengine.org/en/stable/tutorials/ui/creating_applications.html
- CPU profiler 与瓶颈测量：https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html

### 专业参考
- Xbox Accessibility Guidelines：https://learn.microsoft.com/en-us/xbox/accessibility/guidelines
- Game AI Pro（行为选择、BT、自动化 AI 测试等免费章节索引）：https://www.gameaipro.com/
- GDC Vault, Technical Tools for Authoring Branching Dialogue：https://www.gdcvault.com/play/1026384/Technical-Tools-for-Authoring-Branching

### Codex 自动技能使用
- OpenAI Codex app：Skills 可显式指定，也可按任务自动使用；支持多 Agent 并行：https://openai.com/index/introducing-the-codex-app/

使用规则：优先官方 stable 文档；网页结论进入知识库前要记录访问日期、Godot 版本和适用范围。只提炼规律，不复制受版权保护的长文本或素材。

## Public repository and release references

Accessed 2026-07-30:

- GitHub releases: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
- Managing GitHub releases: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository
- GitHub community health files: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories
- Adding a repository license: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository
- OpenAI Codex app and Skills: https://openai.com/index/introducing-the-codex-app/
- Running Codex safely: https://openai.com/index/running-codex-safely/

These sources support the repository packaging, release, community-file and agent-permission guidance. Product behavior and documentation may change; re-check official sources before later releases.

## Skill/plugin and verification hardening

Accessed 2026-07-31:

- OpenAI Codex Skills: https://developers.openai.com/codex/skills/
- OpenAI plugin packaging: https://developers.openai.com/plugins/build/plugins
- OpenAI Codex subagents: https://developers.openai.com/codex/subagents/
- Agent Skills specification: https://agentskills.io/specification
- Agent Skills script/resource paths: https://agentskills.io/skill-creation/using-scripts
- Agent Skills evaluation guidance: https://agentskills.io/skill-creation/evaluating-skills
- Godot command-line tutorial: https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- Godot 4.6.3 release assets: https://github.com/godotengine/godot-builds/releases/tag/4.6.3-stable
- GitHub artifact attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- GitHub secure use reference for pinning Actions: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions

这些来源支持 `agents/openai.yaml`、插件清单、项目级 Custom Agent、Skill 自包含相对路径、正负触发评测、真实 Godot headless 门禁、Action 提交固定和 Release attestation。版本号、哈希和运行时格式属于易变化事实，每次发布必须重新核对。
