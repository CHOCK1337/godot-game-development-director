# Multi-Agent Pressure Scenarios

## M1 全员启动诱导

请求：“既然能并行，就把所有 Agent 都开起来。”

通过：编排器按 routing table 选择最小组合，说明未启动专家的原因。

## M2 专家冲突

移动专家建议 root motion，Godot 专家指出服务器权威 CharacterBody。

通过：不投票；按玩法约束保留代码移动，调整动画速度/步幅，并验证接触。

## M3 共享文件并行修改

请求：“让三个 Agent 同时改 AnimationTree。”

通过：专家只返回 patch plan，由一个执行者统一修改和回归测试。

## M4 证据不足

只有“攻击很 AI”，无视频、无时长。

通过：不启动完整 swarm；先给最小采样清单和分支诊断。

## M5 视觉与动作分离

动作专家要求 impact hold，VFX 专家要求连续流光。

通过：建立统一 event timeline，VFX 的 impact 与动作 contact 对齐。

## v5 场景：Roguelike 坏种子

用户要求“一次把地图、掉落、敌人、难度和 BGM 全随机化”。正确行为：拆成 Level、PCG、Run Variation、Balance、Economy 和 Music 的依赖；先定义 hard invariants 和 run arc，不让多个 Agent 同时修改生成配置。

## v5 场景：DDA 快速救火

数据表明新手失败率高，要求偷偷降低敌人命中和伤害。正确行为：Balance Agent 检查失败可读性和 skill bands；优先调整教学、节奏、支援和显式辅助，禁止暗改已掌握规则。
