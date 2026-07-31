# Godot Game Development Director

**版本：** `v0.1.0-alpha.1` · **状态：** 公开预览 · **许可证：** Apache-2.0

Godot Game Development Director 是一套中英双语、证据驱动的游戏内容开发包。它包含 **1 个跨领域总 Skill、8 个模块 Skill、27 个专家角色、1 个总编排器、结构化合同、确定性验证器和 Godot 实现示例**。

覆盖玩法、关卡、平衡、程序生成、局内变化、叙事、任务、NPC AI、镜头、渲染、声音、互动配乐、UX、无障碍、本地化、内容数据、存档、工具和内容 QA。

> 本包不能替代真人创意判断、真实玩家测试、专业无障碍审查，以及目标 Godot 工程中的实际验证。

[English README](README.md) · [版本说明](RELEASE_NOTES.md) · [发布手册](docs/RELEASE_GUIDE.zh-CN.md) · [路线图](ROADMAP.md)

## 这一版为什么更严格

旧版规范的主要问题不是内容少，而是“什么都能触发、什么都要输出、安装后引用还可能失效”。本版把边界做成了可执行规则：

- 总 Skill 只处理跨领域、共享状态和多人所有权问题，不再承包所有 Godot 请求；
- 每个模块都有 UI 元数据，以及直接、间接、证据不足、负例四类触发评测；
- 每个安装后的 Skill 都是自包含目录，文档写到的相对脚本和参考文件不会丢；
- `director`、`modules`、`full` 三种预设范围真正不同，Doctor 会对照安装回执检查；
- `AGENTS.md` 改为显式选择，任何情况下都不会静默覆盖项目原文件；
- 完整 Codex 预设会从权威角色文件生成 28 个项目级 Custom Agent；
- CI 使用固定 Godot 4.6.3 和 SHA-256，真实编译 9 个 GDScript 并执行烟测；
- GitHub Actions 固定到提交 SHA，Release ZIP 带来源证明，已有标签和 Release 不可覆盖。

## 包含内容

- 27 个边界明确的专家角色和 1 个总编排器
- 1 个跨领域总 Skill + 8 个可独立使用的模块 Skill
- Skill UI 元数据和 36 个正负触发评测
- Gameplay、Event、Level、Balance、Generator、Quest、NPC AI、Accessibility、Content Budget、Save 等 JSON 合同
- 安装、诊断、路由、审计、分析、验证与可复现打包工具
- 9 个 GDScript 示例和真实引擎 headless 测试工程
- 检查表、模板、知识库、压力场景与回归测试
- Codex 插件清单和可选项目策略模板

## 安装

先安装验证依赖：

```bash
python -m pip install -r requirements-dev.txt
```

推荐的完整 Codex 项目安装：

```bash
python scripts/install.py \
  --target codex \
  --preset full \
  --destination /你的/Godot/项目路径

python scripts/doctor.py /你的/Godot/项目路径
```

`full` 会把 9 个 Skill 安装到 `.agents/skills/`，并把 28 个项目级 Codex Agent 安装到 `.codex/agents/`。

| 预设 | 安装范围 |
|---|---|
| `director` | 只安装跨领域总 Skill |
| `modules` | 只安装 8 个独立模块，不安装总 Skill |
| `full` | 总 Skill + 8 个模块；目标为 Codex 时还安装项目级 Agent |

旧参数仍兼容：`core → director`、`skills-only → modules`、`godot-content-team → full`。

如需在项目没有 `AGENTS.md` 时复制可选路由策略，增加 `--write-agents-md`。即使使用 `--force`，现有 `AGENTS.md` 也不会被覆盖。

仓库同时符合 Codex 插件目录：`.codex-plugin/plugin.json` 为插件清单，`skills/` 中有 9 个可发现 Skill。

## 怎么调用

跨领域任务显式调用总 Skill：

```text
使用 $directing-godot-game-feel 审查 Boss 第二阶段。
任务旗标、守卫 AI、镜头、音乐和存档重载后的状态不一致。
只选择必要领域，并给出 owner、实施顺序、自动测试、人工验收阈值和回滚。
```

单一领域直接调用模块，例如：

```text
使用 $designing-npc-ai-simulation 诊断守卫为什么能隔墙知道玩家位置，
并在路径失效后永久卡住。
```

总编排器必须选择最小团队。共享任务状态、存档 Schema、事件、seed、拓扑、资源或同一文件的专家必须分阶段执行，不能并行抢写。

## 验证

仓库与回归门禁：

```bash
python scripts/validate_public_release.py
python tests/validate_package.py
python -m unittest discover -s tests -v
```

真实 Godot 验证：

```bash
python scripts/run_godot_validation.py --godot /Godot4/可执行文件路径
```

CI 会下载官方 `Godot_v4.6.3-stable_linux.x86_64.zip`，校验固定 SHA-256，编译全部 `.gd` 并执行确定性烟测。这能证明这些脚本在该引擎构建中的语法和烟测合同，但不能证明兼容所有 Godot 4.x 版本和所有工程架构。

## 主要入口

- `SKILL.md`：总 Skill 源合同
- `skills/`：插件化总 Skill与 8 个自包含模块
- `agents/orchestrator.md`、`agents/routing-table.md`：权威角色和路由
- `scripts/install.py`、`scripts/doctor.py`：分范围安装与完整性诊断
- `scripts/generate_codex_agents.py`：项目级 Custom Agent 适配器
- `scripts/validate_skill_references.py`、`scripts/validate_skill_evals.py`：Skill 完整性门禁
- `tests/godot_fixture/`：真实引擎编译与烟测
- `codex/AGENTS.md.example`：可选项目策略模板

## 构建 Release 附件

```bash
python scripts/build_release.py --version v0.1.0-alpha.1 --clean
```

输出：

```text
dist/godot-game-development-director-v0.1.0-alpha.1.zip
dist/SHA256SUMS
```

Release 工作流只接受已经存在且指向本次验证提交的标签，不覆盖已有 Release，并对 ZIP 生成来源证明。

## 范围和限制

本版本专注游戏内容开发。商店上架、主机认证、营销、法律意见、隐私合规、LiveOps、支付和生产级在线后端不在范围内。

GDScript 是适配示例，不是通用插件。最终验收仍需目标工程、准确 Godot 版本、代表性存档、目标设备、语言/输入/无障碍矩阵和真人试玩。

## 贡献、安全与许可证

贡献前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。不得提交私有项目数据、凭证、商业游戏复制内容、未授权素材或受版权保护资料的大段原文。运行 Agent 前检查权限，并对发布、推送、删除、可见性变更和凭证访问保留人工确认；参见 [SECURITY.md](SECURITY.md)。

本仓库采用 Apache-2.0。外部资料仍归原权利人所有；参见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 和 [SOURCES.md](SOURCES.md)。

Godot 是 Godot Foundation 的商标。本项目为独立社区项目，与 Godot Foundation 无隶属或背书关系。
