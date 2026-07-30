# Godot 3D 动画实现

## 导入与重定向

- 骨名相同不代表可直接共享动画；bone hierarchy、Bone Rest、骨长和轴向必须匹配。
- 使用 humanoid BoneMap/SkeletonProfile 和导入重定向选项时，逐项检查 hips/root、手脚方向和位置轨。
- Godot 4 的骨姿势包含 Bone Rest，旧教程或 Godot 3 工作流不能直接套用。
- 动画包出现统一塌腰、腿长变化、手腕翻转时，先查 retarget/rest，不要先修每个 clip。

## AnimationPlayer 与 AnimationTree

- AnimationPlayer/AnimationLibrary 保存并播放动画；AnimationTree负责高级混合、BlendSpace、状态机和 root motion 提取。
- RESET 动画用于默认姿势，不应当成普通循环播放。
- Blend 时间不是越长越自然。过长会让 contact、impact 和方向变化糊掉。
- 使用 filter/additive 时检查骨盆、脊柱和肩带边界，避免多层争夺同一骨骼。

## Root motion 与 CharacterBody3D

- root motion 能让动画步幅与地面移动一致；从 AnimationTree 读取 blended root motion，再映射到 CharacterBody3D。
- 若使用代码驱动速度，需把动画播放速度/BlendSpace 与真实水平速度对齐。
- CharacterBody3D 的 move_and_slide 应在 physics process 路径中使用；检查斜坡、移动平台、floor snap 和尺度。
- 不要同时把 root motion 和脚本位移完整叠加。

## IK 与 SkeletonModifier3D

- SkeletonModifier3D 在动画混合之后修改骨骼，适合 IK、约束和骨架物理层。
- 接触修正使用：地面探测 → 目标过滤 → 骨盆补偿 → 单脚 influence 曲线 → 膝盖 pole/极限。
- SkeletonIK3D 在部分版本文档中标记为 deprecated；不要把它写成唯一长期方案。优先依据项目版本选择当前 SkeletonModifier3D/IKModifier3D 工作流或自定义解算。
- LookAt、SpringBone、PhysicalBone 等 modifier 要明确执行顺序和 influence。

## 事件与同步

- 用动画方法/事件轨同步脚步声、hitbox、弹匣、VFX、相机冲击。
- 事件必须基于动作阶段，不应依赖不稳定的 blend 后姿势猜测。
