# 互动配乐知识库

## 四类手段

- Horizontal resequencing：在段落/乐句间切换。
- Vertical remixing：同一时间轴增减 stem。
- Stinger：短暂确认事件，不承担持续状态。
- Parameter modulation：有限调整滤波、密度、发送或音量。

优先选择能满足需求的最小组合。

## 音乐状态轴

常见轴：danger、intensity、location、faction、stealth exposure、boss phase、narrative valence。轴必须来自玩家可感知且相对稳定的状态，避免直接绑定每帧波动值。

## 防抖

每个状态定义：进入阈值、退出阈值、最短停留、冷却、抢占优先级和 fallback。使用 hysteresis，避免在边界来回切换。

## 转场

- 即时：只用于必须立刻确认的事件，常由 stinger 承担。
- Beat/Bar：保持脉冲连续。
- Phrase：适合明显段落变化。
- End-of-clip：适合低频叙事状态。

所有并行 stem 必须共享长度、拍点、起点和循环边界，或明确证明异步层不会产生相位问题。

## 反 AI 味

- 不在所有状态使用完整频谱和满配器。
- 不让旋律与对白、提示音争夺中频和注意力。
- 不用随意半音上行、巨鼓和合唱作为通用“升级”。
- 用项目世界观的材质、节奏、空间和角色 motif 建立身份。
- 重复必须有功能：建立预测、记忆或节奏，不是因为素材不足。
