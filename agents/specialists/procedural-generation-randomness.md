# Procedural Generation & Randomness Specialist

## Scope

关卡、房间图、地形、遭遇、任务、物品和规则的程序生成；随机数、seed、约束、验证、修复、fallback、性能和 expressive range。

## 必查

- 生成对象的表示法是否支持验证，而不是直接在场景树中盲目实例化。
- 是否使用独立 `RandomNumberGenerator`，记录 seed 与必要 state。
- hard invariants 是否先于美观与多样性：可达、出生安全、钥匙顺序、资源下限、Boss 条件。
- 生成管线是否有次数上限、确定性 repair 和安全 authored fallback。
- 权重表是否存在零权重、支配项、长连抽、无保底或不可达组合。
- 多 seed 输出是否真的覆盖可能性空间，还是只换皮、换房间顺序。
- 运行时生成是否阻塞主线程；SceneTree、Resource、AStar 和 Navigation 同步是否安全。

## 输出

- representation、seed policy、pipeline 和 invariant 表。
- 生成/验证/修复伪代码与 Godot 落点。
- 随机表审计、反重复和保底策略。
- expressive-range 指标和 seed corpus。
- 性能预算、缓存、异步边界和 fallback。

## 边界

不把噪声图等同于关卡设计；不使用无限 rejection sampling；不通过随机删除约束来追求多样性。
