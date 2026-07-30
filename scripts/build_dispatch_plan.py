#!/usr/bin/env python3
"""Build a deterministic, explainable dispatch plan for Godot content-development work."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

LOCOMOTION={"walk","run","sprint","strafe","backpedal","start","stop","turn","slope","stairs","foot_sliding","floaty"}
ACTION={"jump","land","climb","vault","swim","fly","attack","block","dodge","shoot","reload","cast","hit","death","stiff_impact"}
ACTING={"idle","emote","dialogue","gaze","face","hand","prop","interaction","cloth","hair","tail"}
GODOT={"retarget","root_motion","animationtree","characterbody","ik","import","network","runtime","state_transition","event_bus","godot","navigationagent","custom_resource"}
ASSET={"mesh","texture","material","vfx","ui","icon","sprite","spritesheet","scene_asset","visual_ai_taste","character_animation"}
GAMEPLAY_CORE={"core_loop","player_verb","controls","game_feel","feedback","onboarding","risk_reward","combat_loop","exploration_loop","puzzle_loop","agency","mastery","responsiveness"}
SYSTEMS={"economy","resource","reward","progression","build","crafting","loot","loot_table","currency","upgrade","unlock","meta_progression"}
ENCOUNTER={"encounter","enemy_mix","pacing","difficulty","boss_phase","level_flow","wave","objective","challenge_curve"}
MUSIC={"adaptive_music","bgm","combat_music","exploration_music","boss_music","stem","stinger","motif","loop","music_state","horizontal_resequencing","vertical_remix","music_asset_ai_taste"}
AUDIO={"audio_bus","ducking","audiostream","audio_transition","music_runtime","sfx_mix","dialogue_mix","audio_server","audio"}
PLAYTEST={"playtest","telemetry","session_csv","funnel","death_reason","choice_rate","music_transition_rate","level_runs","seed_outlier","path_diversity"}
LEVEL={"level_design","layout","critical_path","branching","landmark","gating","traversal_flow","topology","arena","puzzle_space","level_flow","spawn_layout","visibility","shortcut","level_architecture"}
BALANCE={"balance","difficulty_curve","challenge_budget","fairness","ttk","damage_model","survivability","win_rate","skill_band","dda","dynamic_difficulty","parameter_tuning","intensity_curve","balance_model"}
PROCGEN={"procedural_generation","pcg","random_level","dungeon_generation","seed","generation","wave_generation","random_map","grammar","wfc","noise","generator","constraint_generation","procedural_level"}
REPLAY={"replayability","run_variation","roguelike","roguelite","mutator","random_event","draft","encounter_pool","loot_table","reroll","pity","run_seed","possibility_space","anti_repeat","run_director"}

CONTENT_PRODUCTION={"vertical_slice","content_scope","scope","milestone","content_milestone","feature_freeze","content_freeze","content_pillars","definition_of_done","dependency_map","cut_list"}
NARRATIVE={"narrative","story","worldbuilding","quest","quest_graph","branching_dialogue","dialogue_tree","cutscene","cinematics","environmental_storytelling","character_arc","lore","conversation"}
NPC_AI={"npc_ai","enemy_ai","companion_ai","perception","behavior_tree","utility_ai","fsm","ai_state","crowd","schedule","simulation","target_selection","squad_ai"}
CAMERA={"camera","gameplay_camera","combat_camera","follow_camera","lock_on_camera","aim_camera","camera_occlusion","camera_shake","fov","camera_composition","springarm"}
TECH_ART={"technical_art","shader_budget","lod","overdraw","texture_budget","draw_calls","triangle_budget","particle_budget","render_budget","lighting_budget","shadow_budget","atlas","multimesh","occlusion"}
SOUND={"sfx","sound_design","footstep_sfx","foley","voice_over","vo","spatial_audio","ambience","ui_sound","weapon_sound","monster_sound","audio_cue","voice_mix","dialogue_audio"}
UX={"ux","hud","menu","accessibility","subtitles","captions","input_remap","reduced_motion","screen_reader","localization","i18n","rtl","cjk","text_expansion","focus_order","tutorial_ui"}
CONTENT_ARCH={"content_architecture","save_state","save_schema","save_migration","save_load","content_pipeline","editor_tool","editor_plugin","stable_id","data_driven","content_validator","resource_schema","content_import"}
CONTENT_QA={"content_qa","quest_test","ai_test","localization_test","save_regression","content_matrix","softlock_test","camera_test","audio_test","content_coverage"}

NEW_CONTENT_SPECIALISTS={
    "content-production-scope","narrative-quest-cinematics","npc-ai-simulation",
    "gameplay-camera-composition","technical-art-rendering","sound-design-voice-mix",
    "ux-accessibility-localization","content-architecture-save-tools",
}

def _norm(values: Any)->set[str]:
    if not values: return set()
    if isinstance(values,str): values=[values]
    return {str(v).strip().lower().replace(" ","_") for v in values}

def build_plan(brief:dict[str,Any])->dict[str,Any]:
    action=_norm(brief.get("action_tags")); symptoms=_norm(brief.get("symptoms"))
    technical=_norm(brief.get("technical_tags")); assets=_norm(brief.get("asset_tags"))
    gameplay=_norm(brief.get("gameplay_tags")); audio=_norm(brief.get("audio_tags"))
    data=_norm(brief.get("data_tags")); content=_norm(brief.get("content_tags"))
    all_tags=action|symptoms|technical|assets|gameplay|audio|data|content
    specialists=[]; preprocessing=[]; reasons=[]; warnings=[]; shared=[]

    evidence=str(brief.get("evidence_quality","unknown")).lower()
    if evidence in {"raw","mixed","unknown"} and brief.get("multiple_sources",False):
        preprocessing.append("evidence-intake"); reasons.append("多个未标准化证据需要先建立 source_id、状态和时间索引")
    if bool(brief.get("reference_gap")):
        preprocessing.append("reference-research"); reasons.append("缺少可用参考或需要核对当前资料")

    # Existing domains: preserve v5 ordering for compatibility.
    if all_tags & LOCOMOTION: specialists.append("locomotion-grounding"); reasons.append("存在移动、接地、脚滑或转停问题")
    if all_tags & ACTION: specialists.append("action-dynamics"); reasons.append("存在战斗、穿越、跳跃或冲击动作")
    if all_tags & ACTING: specialists.append("acting-interaction"); reasons.append("存在表演、交互、面部或次级运动")
    if all_tags & GAMEPLAY_CORE: specialists.append("gameplay-core-loop"); reasons.append("需要审查核心循环、verbs、输入、反馈或风险收益")
    if all_tags & SYSTEMS: specialists.append("systems-economy-progression"); reasons.append("涉及资源、奖励、经济、构筑或长期成长")
    if all_tags & ENCOUNTER: specialists.append("encounter-pacing"); reasons.append("涉及敌人组合、局部遭遇节奏、波次或 Boss 阶段")
    if all_tags & LEVEL: specialists.append("level-design-architecture"); reasons.append("涉及关卡拓扑、关键路径、地标、门锁、视线或空间功能")
    if all_tags & BALANCE: specialists.append("balance-difficulty"); reasons.append("涉及全局平衡、挑战维度、难度曲线、公平性或动态难度")
    if all_tags & PROCGEN: specialists.append("procedural-generation-randomness"); reasons.append("涉及 seed、程序生成、随机地图、约束、验证或生成器性能")
    if all_tags & REPLAY: specialists.append("replayability-run-variation"); reasons.append("涉及 Roguelike 局内变化、随机事件、内容池、反重复或重玩性")
    if all_tags & MUSIC: specialists.append("interactive-music"); reasons.append("涉及 BGM 身份、音乐状态、stem、stinger 或转场")
    if all_tags & AUDIO: specialists.append("godot-audio-integration"); reasons.append("涉及 Godot 音频资源、总线、ducking 或运行时转场")

    # v6 content-production domains.
    if all_tags & CONTENT_PRODUCTION: specialists.append("content-production-scope"); reasons.append("涉及内容支柱、Vertical Slice、里程碑、冻结或范围控制")
    if all_tags & NARRATIVE: specialists.append("narrative-quest-cinematics"); reasons.append("涉及世界观、任务图、分支对话、角色连续性或演出")
    if all_tags & NPC_AI: specialists.append("npc-ai-simulation"); reasons.append("涉及 NPC 感知、知识、决策、行为树、群体或模拟")
    if all_tags & CAMERA: specialists.append("gameplay-camera-composition"); reasons.append("涉及跟随、瞄准、锁定、遮挡、镜头冲击或运动舒适度")
    if assets & TECH_ART or all_tags & TECH_ART: specialists.append("technical-art-rendering"); reasons.append("涉及资源/Shader/渲染预算、LOD、过绘、灯光或低端降级")
    if audio & SOUND or all_tags & SOUND: specialists.append("sound-design-voice-mix"); reasons.append("涉及 SFX、Foley、脚步、VO、空间音频、环境或动态混音")
    if all_tags & UX: specialists.append("ux-accessibility-localization"); reasons.append("涉及 HUD、菜单、输入、字幕、无障碍、本地化或文本布局")
    if all_tags & CONTENT_ARCH: specialists.append("content-architecture-save-tools"); reasons.append("涉及数据驱动内容、稳定 ID、存档版本/迁移、编辑器工具或验证器")

    needs_godot=bool(brief.get("needs_godot_implementation")) or bool(all_tags & GODOT)
    godot_design_sets=LOCOMOTION|ACTION|ACTING|GAMEPLAY_CORE|SYSTEMS|ENCOUNTER|LEVEL|BALANCE|PROCGEN|REPLAY|NARRATIVE|NPC_AI|CAMERA|CONTENT_ARCH|GODOT
    if needs_godot and (all_tags & godot_design_sets):
        specialists.append("godot-integration"); reasons.append("需要区分设计、内容、Godot 状态和运行时责任")
    if needs_godot and (all_tags & MUSIC) and "godot-audio-integration" not in specialists:
        specialists.append("godot-audio-integration"); reasons.append("互动音乐需要 Godot 音频实现判断")
    if needs_godot and (all_tags & SOUND) and "godot-audio-integration" not in specialists:
        specialists.append("godot-audio-integration"); reasons.append("SFX/VO/空间音频需要 Godot 播放器、bus 与并发实现判断")
    if assets & ASSET or "visual_ai_taste" in symptoms:
        specialists.append("asset-style"); reasons.append("包含视觉素材或非动作 AI 味审查")

    specialists=list(dict.fromkeys(specialists)); preprocessing=list(dict.fromkeys(preprocessing))

    # Existing shared facts.
    if "locomotion-grounding" in specialists and "godot-integration" in specialists: shared.append("foot contact / root motion / runtime velocity 必须在合并阶段统一归因")
    if "action-dynamics" in specialists and "godot-integration" in specialists: shared.append("hit frame / collision / cancel window 必须共享同一事件时间轴")
    if "action-dynamics" in specialists and "gameplay-core-loop" in specialists: shared.append("动作承诺、输入响应、成本和反制必须由同一玩法语义裁决")
    if "encounter-pacing" in specialists and "interactive-music" in specialists: shared.append("encounter intensity / boss phase 必须成为稳定音乐状态，不直接绑定瞬时数值")
    if "interactive-music" in specialists and "godot-audio-integration" in specialists: shared.append("音乐状态、量化转场、stem 同步和 fallback 必须使用同一状态表")
    if "systems-economy-progression" in specialists and "gameplay-core-loop" in specialists: shared.append("奖励与成长必须强化核心决策，而不是形成独立数值循环")
    if "asset-style" in specialists and "action-dynamics" in specialists: shared.append("VFX 与动作 impact 不得分别优化后失去同步")
    if "level-design-architecture" in specialists and "encounter-pacing" in specialists: shared.append("关键路径、视线、出生、恢复区和 encounter slot 必须共享同一空间职责图")
    if "level-design-architecture" in specialists and "procedural-generation-randomness" in specialists: shared.append("生成器必须保留关卡 hard invariants；多样性不能破坏可达性、门锁顺序和空间可读性")
    if "balance-difficulty" in specialists and "gameplay-core-loop" in specialists: shared.append("参数目标必须服务核心决策；不得用数值上涨代替新反制或策略")
    if "balance-difficulty" in specialists and "encounter-pacing" in specialists: shared.append("全局挑战预算与局部强度波形必须分层，恢复段不得被 DDA 或波次系统覆盖")
    if "procedural-generation-randomness" in specialists and "godot-integration" in specialists: shared.append("seed/state、生成版本、线程边界、SceneTree 实例化和 Navigation 同步必须统一")
    if "replayability-run-variation" in specialists and "systems-economy-progression" in specialists: shared.append("随机奖励、reroll、pity 与 meta progression 必须共享同一资源和保底规则")
    if "replayability-run-variation" in specialists and "procedural-generation-randomness" in specialists: shared.append("run arc 决定内容 slot，生成器只在兼容池内采样，不能从全池无条件抽取")

    # v6 shared facts.
    if "narrative-quest-cinematics" in specialists and "content-architecture-save-tools" in specialists:
        shared.append("Quest Graph、dialogue condition、cutscene commit 与 save migration 必须共享稳定 quest/node/state keys")
    if "narrative-quest-cinematics" in specialists and "level-design-architecture" in specialists:
        shared.append("任务目标、门锁、地标和 sequence break 必须共享同一空间/世界状态")
    if "npc-ai-simulation" in specialists and "action-dynamics" in specialists:
        shared.append("NPC decision、attack commitment、animation anticipation 和 cancel rules 必须共享同一行为语义")
    if "npc-ai-simulation" in specialists and "godot-integration" in specialists:
        shared.append("perception、decision、Navigation path/avoidance、CharacterBody movement 和 animation ownership 必须分层")
    if "gameplay-camera-composition" in specialists and "action-dynamics" in specialists:
        shared.append("camera impulse 只能消费命中/受击事件，不得替代动作和碰撞的权威时间")
    if "gameplay-camera-composition" in specialists and "ux-accessibility-localization" in specialists:
        shared.append("camera shake、FOV、bobbing、自动旋转和 reduced-motion 设置必须共用一份玩家配置")
    if "sound-design-voice-mix" in specialists and "godot-audio-integration" in specialists:
        shared.append("Audio Cue、event serial、bus、priority、concurrency、spatialization 和 fallback 必须使用同一 cue sheet")
    if "sound-design-voice-mix" in specialists and "narrative-quest-cinematics" in specialists:
        shared.append("VO line_id、speaker、subtitle key、cutscene timing 和 quest state commit 必须一致")
    if "technical-art-rendering" in specialists and "asset-style" in specialists:
        shared.append("性能降级先删除装饰层，必须保留项目形状语言、玩法轮廓和关键信号")
    if "technical-art-rendering" in specialists and "ux-accessibility-localization" in specialists:
        shared.append("reduced effects、对比度、文本清晰度和低端渲染配置不得互相覆盖")
    if "content-production-scope" in specialists and len(specialists)>1:
        shared.append("Content Production 只裁决范围、依赖和冻结，不覆盖专业专家的事实判断")

    post=["orchestrator-synthesis"]
    has_playtest=bool(brief.get("has_playtest_data")) or bool(all_tags & PLAYTEST)
    if has_playtest:
        post.append("playtest-analysis"); reasons.append("存在试玩/遥测数据，可在合并假设后进行验证")
    needs_content_qa=bool(brief.get("needs_content_qa")) or bool(all_tags & CONTENT_QA)
    if needs_content_qa:
        post.append("content-qa-automation"); reasons.append("需要任务、NPC、镜头、音频、语言、存档或内容预算回归")
    post.append("qa-acceptance")

    if not specialists and not preprocessing:
        mode="single"; warnings.append("标签不足；单 Agent 应先生成证据采样、核心循环草图和分支诊断")
    elif len(specialists)<=2 and len(preprocessing)<=1:
        mode="parallel_lite" if len(specialists)>=2 else "single"
    else:
        mode="parallel_full"
    if len(specialists)>6: warnings.append("并行专家超过默认上限 6；按共享依赖拆为两波，先定范围/状态/合同，再做表现与实现")

    return {"mode":mode,"preprocessing":preprocessing,"parallel_specialists":specialists,
            "postprocessing":post,"reasons":reasons,"shared_dependencies":shared,"warnings":warnings}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("brief",type=Path); ap.add_argument("--pretty",action="store_true"); ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    try:
        brief=json.loads(args.brief.read_text(encoding="utf-8"))
        if not isinstance(brief,dict): raise ValueError("brief must be a JSON object")
        text=json.dumps(build_plan(brief),ensure_ascii=False,indent=2 if args.pretty else None)
        if args.output: args.output.write_text(text+"\n",encoding="utf-8")
        else: print(text)
        return 0
    except (OSError,json.JSONDecodeError,ValueError) as exc:
        ap.error(str(exc)); return 2
if __name__=="__main__": raise SystemExit(main())
