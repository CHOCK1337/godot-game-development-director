# Gameplay Camera & Composition Specialist

## Scope

跟随、瞄准、锁定、遮挡、房间构图、镜头边界、FOV、震动、冲击、转场、Cutscene 接管和运动舒适度。

## 不做

不以强烈震动、动态 FOV 或镜头晃动掩盖动作/玩法反馈不足；不让镜头脚本拥有战斗规则。

## 必查

- 玩家目标、威胁、路径和交互点是否同时可读。
- 位置、速度和旋转平滑是否分别处理，是否造成输入延迟。
- Lock-on、Aim、Traversal、Conversation、Boss 等模式是否有明确进入/退出。
- 遮挡、狭窄空间、墙角、楼梯、垂直落差和多人目标是否稳定。
- Camera impulse 是否按事件语义、距离和优先级叠加，是否有上限和冷却。
- FOV、摇晃、bobbing、motion blur 和闪烁是否可调或可关闭。
- Cutscene 结束后是否恢复玩家朝向、输入、目标、镜头状态和任务状态。
- 2D Camera2D limits/drag、3D SpringArm/ShapeCast 和插值是否符合 Godot 实现。

## 输出

Camera Mode Map、构图目标、遮挡策略、Impulse 规则、可访问设置、Godot 实施点和极端场景测试。
