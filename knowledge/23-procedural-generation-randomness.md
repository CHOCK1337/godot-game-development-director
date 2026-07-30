# Procedural Generation and Randomness

## 1. Generation Pipeline

推荐管线：

`intent → representation → generate → validate hard invariants → repair → score soft goals → decorate → instantiate → telemetry`

抽象表示可以是 room graph、grid、grammar、constraint set 或 module sequence。直接生成完整场景会让验证和修复代价过高。

## 2. Hard vs Soft

**Hard invariants**：可达、出生安全、目标存在、钥匙顺序有效、资源底线、导航连通、性能上限。

**Soft goals**：分支数量、线性度、景观、战斗密度、节奏、多样性和主题匹配。

硬约束不参与“加权妥协”。失败后修复或 fallback。

## 3. Seed Discipline

Godot 的 `RandomNumberGenerator` 支持独立 seed/state，适合回放、网络、rewind 和问题复现。每次 run 记录：seed、生成器版本、内容版本、平台、关键 RNG state、选择历史。

不要在不同系统共享一个全局随机流；新增一次随机调用会改变后续所有结果。按地图、战利品、遭遇、装饰拆分 RNG stream。

## 4. Random Table Controls

- 权重归一化只用于解释，实际选择可使用相对权重。
- 使用 bag/history/cooldown 限制短期重复。
- 使用 pity 保证长尾体验，但明确重置条件。
- 对互斥、前置、唯一和资源预算使用约束，不靠极低概率回避。
- 记录实际选择频率，与期望概率比较。

## 5. Expressive Range

生成器不是输出越多越好。选择能代表设计目标的指标，例如 linearity、branching、leniency、resource pressure、combat density、recovery spacing。用大量 seed 映射分布，寻找空洞、偏置和坍缩。

## 6. Godot 技术边界

- `TileMapLayer` 更新批处理到帧末；大量运行时更新要分批。
- `AStarGrid2D` 适合网格验证，但同一对象不能被多线程同时使用。
- NavigationServer 更适合并行查询，但地图变更通常需等待物理帧同步。
- 活动 SceneTree 和唯一 Resource 不应被多个线程同时修改；后台生成纯数据，主线程实例化。
