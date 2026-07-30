# 跨系统 Gameplay Event Contract

## 目的

同一游戏事实只能有一个语义定义。动画、碰撞、VFX、SFX、BGM、镜头、UI 可以各自消费，但不得各自猜时间。

## 事件字段

- `event_id`：稳定语义名，如 `combat.hit.confirmed`。
- `producer`：权威来源。
- `payload`：强度、位置、阵营、目标、阶段等最小数据。
- `timing`：即时或动画时间轴标记。
- `reliability`：本地、网络确认、可预测、可撤销。
- `consumers`：视觉、音频、UI、统计。
- `cooldown/dedupe`：防止重复。
- `fallback`：消费者缺失时核心玩法仍成立。

## 示例因果

输入攻击不是命中事件。推荐分开：
`attack.requested → attack.started → hitbox.active → hit.confirmed → target.staggered → encounter.intensity.changed`

BGM 通常消费稳定的 encounter/intensity 状态，不消费每一次伤害数字；命中由 SFX/VFX/stinger 负责。
