# 运行时与玩法约束

## 动画质量必须服务控制

视觉上完美但输入延迟过高的动作不是合格游戏动画。每项审查同时记录：

- 输入开始时间与视觉响应时间。
- movement lock、turn allowance、cancel window。
- hit/hurt/interaction 事件。
- root displacement 与碰撞体移动。
- 网络复制、预测和回滚需求。

## 动画驱动 vs 代码驱动

- 动画驱动：接触准确、电影化强，但需处理导航、碰撞和网络。
- 代码驱动：响应稳定，但易滑脚；需速度匹配、stride/phase 管理。
- 混合方案：代码控制宏观路径，root/stride/IK 修视觉；必须定义谁拥有位移真值。

## 状态机

- 状态边界按动作意义设计，不只按 clip 名字。
- locomotion、airborne、action、hit reaction、interaction 可分层，但要规定优先级和中断规则。
- OneShot、additive、upper-body mask 使用前先确定骨盆/胸/手的所有权。

## 性能与 LOD

- 远处角色减少 IK、面部、手指和次级骨骼更新。
- 群体角色用烘焙 clip、较低采样和共享动画资源。
- 网络中不复制每根骨骼；复制状态、时间、速度和必要目标，在客户端重建视觉层。
- 任何程序修正都需测试最坏角色数量和低帧率稳定性。
