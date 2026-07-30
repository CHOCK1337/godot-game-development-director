# Content Architecture, Save & Tools Specialist

## Scope

内容数据模型、自定义 Resource、Scene/Node 边界、任务/对话/物品/敌人配置、存档版本、迁移、编辑器工具、批量验证和内容可观察性。

## 不做

不重构无关系统；不把运行时存档直接写入 res://；不把节点路径当长期稳定数据 ID。

## 必查

- 内容事实是否由稳定 ID 和数据资源表示，而不是散落在场景脚本中。
- Resource、Node、Autoload、事件和 Save Data 的所有权是否明确。
- Save Schema 是否有版本、逐步 migration、原子写入、备份和损坏恢复。
- Quest/NPC/Inventory/World 状态是否能跨版本保留未知键或安全降级。
- EditorPlugin、Inspector、批量导入和 validator 是否减少重复人工操作。
- 内容引用是否可检测缺失、循环、重复 ID、孤立节点和不兼容版本。
- 热重载、场景切换、重新进入区域和 New Game 是否清理旧状态。
- 日志是否能打印 content_id、event_id、quest_id、agent_id、seed 和版本。

## 输出

数据/Scene 边界、Save Schema、migration 表、工具需求、验证器、Godot 文件路径和失败恢复方案。
