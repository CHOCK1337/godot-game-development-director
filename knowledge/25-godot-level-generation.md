# Godot Level Generation Implementation

## Data First

生成器先返回纯数据 `GenerationResult`，包含 seed、nodes、edges、placements、validation、repairs 和 warnings。只有结果通过后才实例化 Node。

## RNG Streams

为 layout、encounter、loot、decoration 创建独立 `RandomNumberGenerator`。使用主 seed 派生子 seed；保存主 seed、生成器版本与必要 state。

## 2D

- 用 `TileMapLayer` 分开 floor、walls、collision、navigation、decor 和 semantic debug。
- 用 `set_pattern()`/terrain connect 批量放置，避免每帧大量零散更新。
- 用 `AStarGrid2D` 或自有 graph 验证主路和支路；不要让多个线程共享同一 AStar 对象。

## 3D

- 用房间 `PackedScene` + socket/portal 元数据或 `GridMap` 生成结构。
- 先验证 portal graph，再实例化重资源。
- Navigation 变更后等待同步再查询；不要假设同帧立即可用。

## Threading

后台线程只生成和验证纯数据。活动 SceneTree、渲染节点和唯一 Resource 在主线程修改；跨线程结果通过 `call_deferred` 或安全队列提交。

## Versioning

每个生成结果记录：`generator_version`、`content_catalog_version`、`seed`、`platform`。修改算法后旧 seed 不保证生成相同内容，除非保留版本化生成器。

## Failure Handling

按固定顺序：局部 repair → 重新生成（有上限）→ 安全 authored layout。玩家不应看到无限加载或不可达关卡。
