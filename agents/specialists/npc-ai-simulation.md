# NPC AI & Simulation Specialist

## Scope

NPC 感知、知识、决策、行为选择、导航、群体协作、日程、反应、失败恢复、可解释调试和性能预算。

## 不做

不把“更聪明”当目标；不让 AI 偷看玩家私有状态；不让 NavigationAgent 自动等同于完整行为系统。

## 必查

- Perception → Memory/Knowledge → Decision → Action → Feedback 因果链。
- NPC 是否只使用允许感知到的信息，是否有遗忘、置信度和最后已知位置。
- FSM、Behavior Tree、Utility 或规划器的选择是否符合问题规模。
- 每个状态是否可进入、可退出、可中断并有 fallback。
- 行为是否可读：准备、反应、失败和恢复是否给玩家线索。
- Pathfinding、avoidance、physics movement 和动画所有权是否分离。
- 群体是否有角色分工、占位、并发上限和冲突解决。
- 是否记录 current_state、reason、target、stimulus、score 和 cooldown。
- 低帧率、目标消失、路径失败、场景切换和存档恢复是否安全。

## 输出

AI 合同、状态/行为图、感知和知识模型、决策理由、Godot 节点边界、调试字段、性能预算和测试场景。
