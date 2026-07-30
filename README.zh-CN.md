# Godot Game Development Director

**版本：** `v0.1.0-alpha` · **状态：** 公开预览 · **许可证：** Apache-2.0

Godot Game Development Director 是一套模块化游戏开发 **Skills、专职 Agent 定义、结构化合同、验证脚本、检查表、示例和 Godot 内容生产工作流**。

它重点完善可玩的游戏内容：角色动作、玩法、关卡、平衡、程序生成、随机玩法、叙事、NPC AI、镜头、渲染、音效、互动配乐、UX、无障碍、本地化、存档/内容管线和内容 QA。

> 这是实验性的工作流与知识包，不能替代真人创意判断、真实玩家测试、无障碍测试和具体项目中的引擎审查。

[English README](README.md) · [版本说明](RELEASE_NOTES.md) · [首次发布操作手册](docs/RELEASE_GUIDE.zh-CN.md) · [路线图](ROADMAP.md)

## 包含内容

- 27 个便携式专职 Agent
- 1 个总编排器
- 8 个可独立使用的 Skills
- 11 类结构化 JSON 合同与示例
- 确定性的路由、审计和验证工具
- Godot GDScript 集成示例
- 检查表、模板、知识库与压力测试
- 供 Codex 自动加载 Skill、自动选择专家的项目策略

## 快速安装到 Codex 项目

```bash
python scripts/install.py \
  --target codex \
  --preset godot-content-team \
  --destination /你的/Godot/项目路径

python scripts/doctor.py /你的/Godot/项目路径
```

安装器会把 Skills 放进 `.agents/skills/`。当目标项目还没有 `AGENTS.md` 时，它会复制本包的自动路由策略。

## 使用方式

你不需要逐个输入 `@agent`。正常描述问题，例如：

```text
检查 Boss 第二阶段。攻击动作没有重量，场地节奏单调，BGM 切换突兀，
并且存档重载后 Boss 状态偶尔错误。先分析，再给出可执行的 Godot 修改方案。
```

主 Agent 应先读取根 Skill，根据路由规则选择最少的相关专家，再由主线程统一修改共享资源并完成验证。

## 验证

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_public_release.py
python tests/validate_package.py
python -m unittest discover -s tests -v
```

## 构建 Release 附件

```bash
python scripts/build_release.py --version v0.1.0-alpha
```

输出：

```text
dist/godot-game-development-director-v0.1.0-alpha.zip
dist/SHA256SUMS
```

## 主要入口

- `SKILL.md`：总 Skill 与硬性编排规则
- `agents/orchestrator.md`：总编排器
- `agents/routing-table.md`：Agent 路由表
- `codex/AGENTS.md.example`：Codex 项目自动调用策略
- `skills/`：8 个模块 Skill
- `scripts/build_dispatch_plan.py`：确定性路由器
- `tests/`：验证和回归测试

## 当前边界

本版本专注游戏内容开发，暂不提供完整的商店上架、主机认证、营销、法律意见、隐私合规、LiveOps、支付和生产级在线后端工作流。

当前已经验证 Python、JSON/YAML、目录结构、示例合同和压缩包完整性；GDScript 示例仍需在你的 Godot 版本和真实工程中编译、运行与测试。

## 贡献与安全

贡献前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。不得提交商业游戏复制内容、未授权素材、私有项目文件、账号凭证或受版权保护资料的大段原文。

Agent 运行器可能执行命令和修改文件。使用前应检查权限，并对推送、发布、删除和网络访问保留人工确认。参见 [SECURITY.md](SECURITY.md)。

## 许可证

本仓库采用 Apache-2.0。外部资料仍归原权利人所有，本项目不计划重新分发第三方源素材。参见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 与 [SOURCES.md](SOURCES.md)。

Godot 是 Godot Foundation 的商标。本项目为独立社区项目，与 Godot Foundation 无隶属或背书关系。
