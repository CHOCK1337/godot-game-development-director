# 示例：战斗动作、玩法与 BGM 跨域编排

## 症状
攻击有冲击，但战斗仍像素材拼接；BGM 每次敌人靠近就切换，频繁抽动。

## 路由
- gameplay-core-loop：攻击成本、反制和失败学习。
- action-dynamics：startup/active/recovery 与受击。
- encounter-pacing：稳定的压力状态。
- interactive-music：状态轴和转场。
- godot-integration / godot-audio-integration：事件与播放器。

## 根因
音乐直接读取最近敌人距离；动作 hit frame、碰撞和 SFX 各自有时间源；玩家只有连续攻击，没有暴露成本。

## 修复
1. CombatResolver 成为 `combat.hit.confirmed` 权威生产者。
2. EncounterDirector 用威胁数量、视线、玩家资源和持续时间计算 low/medium/high，并加入滞回。
3. BGM 只消费稳定 intensity；命中由短 SFX/VFX 表达，不切换持续音乐。
4. 普攻增加 whiff recovery，敌人攻击提供可读反制，形成进攻/退出决策。
