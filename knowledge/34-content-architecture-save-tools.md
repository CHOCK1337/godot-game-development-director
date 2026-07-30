# Content Architecture, Save & Tools

Custom Resource 适合可编辑、类型明确、可序列化的作者数据；Node 适合运行时生命周期和场景存在。保存数据应使用稳定 ID 和纯数据快照，不依赖场景节点引用。

## Save rules

- schema_version；逐版本 migration；原子临时文件替换；至少一个 backup。
- 读取时校验类型、范围、内容版本和缺失 ID。
- 未知键默认 preserve，便于回滚和跨版本兼容。
- 写入 `user://`，不写导出后只读的 `res://`。

## Tool rules

能用 validator 自动发现的错误，不写成长篇说明让人记住。
