# 示例：3D 角色走路像漂浮

## 判定

主要问题不是“动作幅度小”，而是支撑期脚底仍在世界空间后滑，同时 CharacterBody3D 的速度比动画步幅快约一档；骨盆只有均匀上下浮动，没有左右承重。

## 证据示例

- 0.08–0.31 秒：左脚标记为接触，但脚底持续向后移动。
- 0.20 秒：骨盆处于最高点，却仍在吸收落脚，阶段冲突。
- 循环末尾：root 速度不连续，blend 到下一循环时身体轻微跳变。

## 修复

1. 重建左/右 contact window，固定接触期脚底，toe-off 前释放。
2. 计算动画 stride speed，匹配 CharacterBody 实际速度；决定 root motion 或代码位移只能有一个主导。
3. 把骨盆最低点移到 down，把最高点移到 passing/up；加入支撑侧髋位移与肩反扭。
4. 地形 IK influence 使用 0→1→0 曲线，只补偿坡面和小误差。

## Godot

- AnimationTree：速度参数同时控制 blend position 和必要的播放时间尺度。
- root motion 方案：读取 root motion delta 后传给 CharacterBody3D。
- 代码驱动方案：按实际水平速度选 clip/速度，不叠加 clip root 位移。
- SkeletonModifier3D/IK：左右脚独立接触权重，骨盆补偿设上限。

## 验收

在平地、10°坡、移动平台、0.7×/1.0×/1.3×速度下观察；接触期脚滑低于项目阈值，膝盖不锁死。
