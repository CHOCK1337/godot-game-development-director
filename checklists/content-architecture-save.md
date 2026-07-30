# Content Architecture & Save Checklist
- [ ] 内容使用稳定 ID，不持久化 NodePath。
- [ ] Resource/Node/Autoload/Save 所有权清晰。
- [ ] Save schema 有版本和逐步 migration。
- [ ] 原子写入、备份和损坏恢复。
- [ ] 未知键策略和缺失内容 fallback 明确。
- [ ] Validator 检测重复 ID、缺失引用、孤立图和预算。
- [ ] 日志包含内容 ID、版本、seed 和状态。
