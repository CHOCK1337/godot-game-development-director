# AI 生成、Mocap 与返工流程

## 生成前 Brief

必须锁定：角色、动作意图、起止姿势、阶段、地面接触、速度/距离、镜头、装备、循环/非循环、Godot 使用方式。

比“cinematic, fluid, natural”更有效的约束：

- 左脚在 0.00–0.18 秒承重，世界空间滑移小于项目阈值。
- 0.28 秒开始髋部驱动，0.42 秒武器命中，0.46 秒胸腔制动。
- 待机主循环 4 秒，但注视转移不固定重复。
- 8 帧 sprite 保留 2 个 contact、2 个 down、2 个 passing/up 组合帧。

## 生成后清理顺序

1. 删除语义错误和骨骼爆点。
2. 重建起止姿势、contact 和 impact。
3. 修 root、脚滑和地面穿插。
4. 修 timing/spacing 和阶段。
5. 修肩髋、力线和 silhouette。
6. 修手指、面部、附件和微动作。
7. 导入 Godot 后再验证 blend、速度、碰撞与事件。

## 负面词的正确用法

只写可观察失败：floating feet、contact foot sliding、constant velocity、perfect bilateral symmetry、locked knees、uniform easing、missing anticipation、missing impact recovery、hands intersecting props。

不要堆砌“no AI look、not generic、more soul”等不可执行词。
