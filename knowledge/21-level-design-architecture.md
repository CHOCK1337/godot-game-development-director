# Level Design Architecture

## 1. 从空间职责开始

每个空间至少承担一种职责：Orientation、Teaching、Practice、Combination、Test、Recovery、Reward、Narrative、Transition。没有职责的房间通常只是时长填充。

## 2. 拓扑语言

- **Critical path**：完成关卡必须经过的节点。
- **Optional path**：用风险、资源、情报、捷径或策略变化换取价值。
- **Loop**：允许回收地标、打开捷径或重新理解空间。
- **Gate**：能力、钥匙、状态、时间或知识门槛。
- **Choke**：集中冲突和视线的狭窄点。
- **Hub**：多路线决策与认知重置。

先画图，再摆美术。关键路径必须可达；支路要么重新接回主路，要么有明确终点价值和退出方式。

## 3. 可读性

方向感来自多信号冗余：轮廓、地标、视线、光照、颜色、运动、声音、敌人朝向和任务反馈。不要只靠箭头 UI。

## 4. 强度曲线

关卡强度不是线性上升。使用 `setup → build → peak → release → reorientation`。高强度需要对比；连续高压会让所有事件失去层级。

## 5. 公平与出生

竞技/合作空间检查：到关键资源时间、掩体质量、视线长度、逃生路线、复活安全、地图边缘和单点控制。几何对称不等于策略公平。

## 6. Godot 映射

- 2D：`TileMapLayer` 分离视觉、碰撞、导航和语义层；`TileMapPattern` 保存模块；`AStarGrid2D` 用于抽象网格验证。
- 3D：`GridMap`/模块化 `PackedScene` 负责结构；NavigationRegion/Link 负责可达性。
- 将房间职责、门锁和生成标签放入 Resource 数据，不从节点名猜语义。
