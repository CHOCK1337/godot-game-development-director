# Narrative, Quest & Cinematics

## Narrative causality

`player action → world state → character knowledge → dialogue/quest consequence → future option`。

## Quest graph safety

- start 必须存在；所有必须节点可达；至少一个可达 terminal。
- 支持 abandon、failure、reload、sequence break 和 missing actor/item。
- 奖励必须幂等；Cutscene skip 不得跳过状态提交。
- 对话节点保存 stable line_id 和 localization context。

## Anti-AI writing

避免所有角色同语气、过度解释、每句都有漂亮隐喻、分支只换措辞、角色知道不该知道的信息。用目标、知识边界、关系和具体行动约束台词。
