# Procedural Generation Checklist

- [ ] 生成前定义抽象表示法，不直接盲目实例化场景。
- [ ] 使用独立 RNG streams，记录 seed、版本和必要 state。
- [ ] hard invariants 明确：可达、出生安全、钥匙顺序、资源底线、性能上限。
- [ ] 每个 hard invariant 都有自动验证。
- [ ] 生成重试有上限，并有确定性 repair 和 authored fallback。
- [ ] 权重表无重复 ID、非正权重、支配项和不可达结果。
- [ ] 稀有关键内容有适当 pity，常见内容有 anti-repeat。
- [ ] 多 seed 检查 expressive range、坏种子和内容坍缩。
- [ ] 后台线程只生成纯数据；主线程修改 SceneTree/Resource。
- [ ] Navigation/AStar/TileMapLayer 的同步和批处理符合项目版本。
