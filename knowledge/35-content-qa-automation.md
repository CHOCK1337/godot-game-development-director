# Content QA Automation

自动化擅长结构、状态和重复回归；真人测试擅长理解、乐趣、节奏和审美。

## Layers

1. Static：ID、引用、Schema、拓扑、预算。
2. Simulation：Quest/NPC/经济/随机状态遍历。
3. Scene smoke：加载、输入、事件、存档、重入。
4. Matrix：语言、分辨率、输入设备、设置组合。
5. Human：可读性、情绪、难度、疲劳和身份。

每个失败必须包含 content_id、输入、期望、实际、版本、seed/状态和复现命令。
