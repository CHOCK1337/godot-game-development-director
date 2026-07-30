# Example: Roguelite Level Feels Random but Repetitive

## Brief
地图每局不同，但玩家总走同一路；少数 seed 资源断供；第三房间难度波动大。

## Wave 1
- Level Design：检查拓扑、支路价值、地标和恢复位置。
- Balance：分技能层检查第三房间 challenge budget 与资源底线。
- PCG：检查 hard invariants、seed streams、验证和 repair。
- Run Variation：检查内容池、anti-repeat、run arc 和选择差异。
- Systems/Economy：检查奖励和构筑是否让支路有真实价值。

## Synthesis
1. 关键路径与高价值奖励绑定，支路只是更长，没有策略价值。
2. `loot` 与 `encounter` 共用全局 RNG；添加装饰随机调用会改变资源序列。
3. recovery room 只是软目标，没有 hard invariant；seed 9999 在 Boss 前无恢复。

## Priority Fixes
- 将 `recovery_before_boss` 升为 hard invariant，并提供 insert-room repair。
- 拆分 layout/encounter/loot/decor RNG streams，记录 seed 与 generator version。
- 将支路价值改为 utility build 或捷径，避免纯数值奖励支配路线。

## Acceptance
- 500 个 seed 无不可达或 Boss 前零恢复。
- competent 玩家 seed 完成率标准差低于项目阈值。
- path diversity 上升，但主路识别时间不恶化。
