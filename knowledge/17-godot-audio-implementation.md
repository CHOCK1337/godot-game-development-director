# Godot 音频实现

## 责任分层

- Composition assets：段落、stem、stinger、loop points、响度和交付格式。
- Music state model：状态、参数、阈值、转场和优先级。
- Runtime director：监听 Gameplay Event，调度播放器和总线。
- Mix：Music/SFX/Dialogue/UI/Ambience bus、ducking、效果和设备适配。

## 节点与资源

以项目版本的 Godot stable 文档为准。常用基础包括 AudioStreamPlayer/2D/3D、Audio buses 与 effects；支持时可评估 AudioStreamInteractive、AudioStreamSynchronized 等资源。不要把 `latest` 文档的 API 未经核对写进生产代码。

## 实现检查

- 音乐导演只消费语义事件，不直接读取几十个场景私有变量。
- 暂停、切场景、加载、存档恢复、窗口失焦后音乐时间线行为明确。
- 转场不会重复触发；异步加载失败有 fallback。
- SFX/Dialogue 需要优先时，Music bus 有可测的 ducking 规则。
- 低端设备减少并行 stem/效果，不改变关键玩法提示。
- 3D 环境声与非空间化 BGM 分层，避免错误定位。
