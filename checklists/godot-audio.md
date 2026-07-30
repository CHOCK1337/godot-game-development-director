# Godot Audio Checklist

- [ ] 按项目 Godot 版本核对播放器、资源和 AudioServer API。
- [ ] Music/SFX/Dialogue/UI/Ambience bus 分层和发送明确。
- [ ] Ducking 有触发、attack/release、最大衰减和恢复规则。
- [ ] 音乐导演消费语义事件，不轮询大量节点私有变量。
- [ ] 加载失败、资源缺失和不支持功能有 fallback。
- [ ] 暂停、失焦、设备变化、场景切换和存档恢复明确。
- [ ] 并行 stem、效果与 3D voices 有性能预算和 LOD。
- [ ] 关键玩法提示在低音量/单声道/小音箱下仍可辨认。
