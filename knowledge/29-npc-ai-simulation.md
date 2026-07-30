# NPC AI & Simulation

## Layering

1. Perception：看见/听见/受击等刺激。
2. Knowledge：已知事实、置信度、最后位置和时间。
3. Decision：状态、BT selector、utility score 或 plan。
4. Action：攻击、搜索、交流、逃离。
5. Locomotion：path query、avoidance、physics。
6. Presentation：动画、VFX、SFX 和台词。

不要让 NavigationAgent 直接决定角色意图；它只帮助路径与避障，角色移动仍由项目脚本负责。

## Readability

玩家应能从姿态、声音、方向和延迟读出 NPC 的观察、决定、承诺和恢复。
