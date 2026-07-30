# Godot 2D 动画实现

## 逐帧与像素动画

- 帧数少时，优先保证 contact、extreme、passing、impact 和 settle。
- 用 hold 和不均匀 spacing 表达重量；不要所有帧等时长。
- 检查 sprite 原点和脚底基线，避免每帧裁切框变化导致视觉漂浮。
- 方向动画不要机械镜像含武器、徽章、光源或惯用手的细节。

## Cutout / Skeleton2D

- Skeleton2D 管理 Bone2D 层级；rest pose 错误会污染所有动作。
- 用 Polygon2D 权重时检查肘、膝、肩和髋的折叠。
- 2D IK/约束通过 SkeletonModificationStack2D 等机制实现时，仍要使用接触权重，避免锁死。
- AnimationPlayer 可同时驱动骨骼、Sprite、粒子、音效、shader 和方法事件。

## 状态与混合

- AnimationTree 可用于 2D/3D 的高级混合和状态切换；原始动画仍由 AnimationPlayer/AnimationLibrary 提供。
- 像素动画通常不适合长 crossfade。使用明确帧切换、过渡 clip 或方向/速度状态。
- 攻击事件、hurtbox、声音和 VFX 放在明确时间点，不依据“当前帧差不多到了”猜测。

## 2D 漂浮排查

1. 所有帧脚底像素是否在一致基线。
2. 节点位置是否与 sprite 内部位移叠加。
3. CharacterBody2D 速度是否与循环步幅一致。
4. 镜头平滑、像素吸附和 subpixel movement 是否造成视觉抖动/漂移。
5. 斜坡和台阶是否需要独立姿势或脚部程序修正。
