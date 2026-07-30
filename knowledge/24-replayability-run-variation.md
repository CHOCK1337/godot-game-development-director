# Replayability and Run Variation

## 1. Meaningful Variation

变体必须至少改变一个决策轴：路线、目标优先级、资源、构筑、敌人组合、空间规则、时间压力或信息。只改变房间皮肤与数值不是重玩性。

## 2. Possibility Space Matrix

列出可变轴和约束：

| Axis | Examples | Constraint |
|---|---|---|
| topology | linear / hub / loop | goal reachable |
| encounter | swarm / elite / turret | counter available |
| reward | offense / defense / utility | no dead choice |
| mutator | darkness / low gravity | readable telegraph |
| objective | survive / escort / collect | compatible space |

组合前先检查 compatibility matrix，避免局部合法、组合无解。

## 3. Anti-Repetition

- **Shuffle bag**：一袋内容用完再洗牌。
- **History exclusion**：最近 N 次不重复。
- **Cooldown**：内容出现后若干房间不能再出现。
- **Pity**：长时间未出现的关键选项提高权重。
- **Reroll**：给玩家有限纠错权，但有明确成本。

## 4. Run Arc

每局需要局部叙事：建立规则、形成构筑、出现压力、提供恢复、测试组合、结算。随机内容按 arc slot 选择，不从一个大池无条件抽取。

## 5. Meta Progression

优先解锁新选择、信息和玩法轴；谨慎使用永久数值增长。若老玩家只靠永久属性绕过核心决策，重玩性会退化为刷取。

## 6. Telemetry

记录 seed、房间序列、选择、跳过、reroll、资源、死亡房间、完成、持续时间和生成版本。检查坏 seed、单一最优路线、内容曝光不均和选择淘汰。
