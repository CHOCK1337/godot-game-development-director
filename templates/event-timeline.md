# Cross-System Event Timeline

| 时间/条件 | 权威状态 | Gameplay Event | 动画/碰撞 | VFX/SFX | BGM | UI/镜头 | 可取消/去重 |
|---|---|---|---|---|---|---|---|
| 0.000 | input accepted | attack.requested | enter startup | input cue | no state change | reticle | request id |

规则：输入请求、动画标记、命中确认和 encounter 状态必须分开。修改 timing 后重新校对所有消费者。
