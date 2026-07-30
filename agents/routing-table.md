# Agent Routing Table v6 — Content Team

只派会改变最终结论的专家。Content Production 负责范围；Content QA 和 QA Acceptance 在合并后运行。超过 6 个专家时分两波。

| 触发标签/症状 | 必派专家 | 条件专家 |
|---|---|---|
| vertical_slice/content_scope/milestone/feature_freeze | content-production-scope | 所有受影响内容专家 |
| quest/story/branching_dialogue/cutscene/worldbuilding | narrative-quest-cinematics | content-architecture-save-tools, level-design-architecture, sound-design-voice-mix |
| npc_ai/perception/behavior_tree/utility_ai/crowd/schedule | npc-ai-simulation | action-dynamics, encounter-pacing, godot-integration |
| gameplay_camera/combat_camera/lock_on/occlusion/shake/FOV | gameplay-camera-composition | action-dynamics, ux-accessibility-localization, godot-integration |
| shader_budget/LOD/overdraw/texture_budget/draw_calls/particles | technical-art-rendering | asset-style, godot-integration |
| SFX/footstep/foley/VO/spatial_audio/ambience | sound-design-voice-mix | godot-audio-integration, narrative-quest-cinematics |
| HUD/menu/subtitles/input_remap/reduced_motion/localization | ux-accessibility-localization | gameplay-camera-composition, sound-design-voice-mix, godot-integration |
| save_schema/migration/stable_id/content_pipeline/editor_tool | content-architecture-save-tools | godot-integration, narrative-quest-cinematics |
| content_qa/softlock_test/save_regression/content_matrix | content-qa-automation（合并后） | 对应内容专家 |
| walk/run/turn/foot_sliding/floaty | locomotion-grounding | godot-integration |
| jump/climb/attack/shoot/cast/hit/death | action-dynamics | godot-integration, encounter-pacing |
| idle/gaze/face/hand/prop/cloth | acting-interaction | asset-style |
| core_loop/player_verb/controls/game_feel/onboarding | gameplay-core-loop | godot-integration |
| economy/resource/reward/progression/build/crafting/loot | systems-economy-progression | gameplay-core-loop, playtest-analysis |
| encounter/enemy_mix/wave/pacing/boss_phase | encounter-pacing | action-dynamics, interactive-music, balance-difficulty, npc-ai-simulation |
| level_design/layout/critical_path/landmark/gate/visibility | level-design-architecture | encounter-pacing, narrative-quest-cinematics, godot-integration |
| balance/difficulty_curve/fairness/TTK/DDA | balance-difficulty | gameplay-core-loop, encounter-pacing, playtest-analysis |
| procedural_generation/random_level/seed/WFC/grammar | procedural-generation-randomness | level-design-architecture, godot-integration |
| roguelike/run_variation/mutator/random_event/reroll/pity | replayability-run-variation | procedural-generation-randomness, systems-economy-progression |
| adaptive_music/BGM/stem/stinger/motif | interactive-music | godot-audio-integration |
| audio_bus/ducking/AudioStream/music_runtime | godot-audio-integration | interactive-music, sound-design-voice-mix |
| mesh/texture/material/VFX/UI/icon/sprite/AI taste | asset-style | technical-art-rendering, godot-integration |
| playtest/telemetry/seed_outlier/path_diversity | playtest-analysis | 对应设计专家 |

## 关键边界

- Production：范围、依赖、冻结；不替代专业判断。
- Narrative：故事/任务状态；Architecture：数据/保存；Level：空间。
- NPC AI：决定做什么；Action：动作怎么读；Encounter：何时出现多少。
- Camera：保留决策信息；不拥有战斗规则。
- Sound Design：SFX/VO；Interactive Music：BGM 状态；Godot Audio：运行时。
- Technical Art：性能预算；Asset Style：审美/反 AI 味。
- Content QA：结构和回归；QA Acceptance：最终跨域门禁。

## 典型组合

### 任务分支、守卫 AI、演出和存档一起坏
第一波：`content-production-scope + narrative-quest-cinematics + npc-ai-simulation + content-architecture-save-tools`  
第二波：`action-dynamics + gameplay-camera-composition + sound-design-voice-mix + godot-integration`  
合并后：`content-qa-automation → qa-acceptance`

### 画面有 AI 味并且低端掉帧
`asset-style + technical-art-rendering + ux-accessibility-localization + godot-integration → content QA → QA`

### 只有“游戏内容还不完整”
先派 `content-production-scope` 建立内容支柱、Vertical Slice、范围和缺口矩阵；不要启动全部专家。
