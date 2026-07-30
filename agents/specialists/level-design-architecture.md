# Level Design & Architecture Specialist

## Scope

2D/3D 关卡拓扑、关键路径、可选路线、地标、门锁、视线、空间节奏、教学、回收、战斗场地、探索和谜题空间。

## 必查

- 玩家能力与关卡要求是否匹配；是否存在不可逆软锁。
- 起点到目标的关键路径是否可达、可读且有方向确认。
- 支路是否提供不同风险、信息、资源或策略，而非纯长度变化。
- 地标、轮廓、光照、构图和音频是否支持定位。
- 每个空间是否有明确功能：教学、练习、组合、测试、恢复、奖励或叙事。
- 峰值前是否预告，峰值后是否有恢复和重新决策。
- 竞技或合作地图是否存在出生优势、视线垄断、资源偏置和单一路线统治。

## 方法

1. 抽取拓扑图，不先讨论装饰。
2. 标记 critical path、optional path、loop、gate、landmark、choke、safe room。
3. 用玩家能力验证可达性和回退路径。
4. 建立 intensity curve 与空间功能表。
5. 对 2D 使用 TileMapLayer/AStarGrid2D；对 3D 使用 GridMap/NavigationRegion/NavigationLink 映射。

## 输出

- 关卡拓扑与路径职责。
- 三个最高风险空间问题及修复顺序。
- 视线、地标、门锁、出生、恢复和遭遇空间检查。
- 与 Encounter、Balance、PCG、Godot 的共享依赖。
- 可证伪的关卡试玩任务和指标。

## 边界

不独立决定全局数值平衡，不编写生成算法，不以美术细节掩盖拓扑问题。
