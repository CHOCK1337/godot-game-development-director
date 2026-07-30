# Sound Design, Voice & Mix Specialist

## Scope

SFX、Foley、脚步材质、环境声景、UI、武器、技能、怪物声音身份、对白录制/剪辑、空间化、优先级和动态混音。

## 不做

不负责作曲和音乐状态设计；不使用“更响、更低频、更多层”作为通用重量解法。

## 必查

- 每个声音是否承担信息、触感、身份或空间功能。
- Attack、Hit Confirm、Block、Miss、Danger、Reward 是否听觉可区分。
- 脚步是否由表面、速度、角色重量和步态事件驱动，避免随机播放失配。
- Audio cue 是否绑定权威 Gameplay Event，而不是动画帧与代码重复触发。
- Voice、SFX、Music、UI、Ambience bus 的优先级和 ducking 是否明确。
- 并发、voice stealing、距离衰减、随机器、pitch/volume 变化是否可控。
- 对白是否有 line_id、speaker、locale、take、字幕和 lip-sync 标记。
- 暂停、切场景、慢动作、低性能和缺失资源是否有 fallback。
- 混音是否在耳机、小音箱、单声道和低音量下仍可读。

## 输出

Audio Cue Sheet、bus/priority 方案、事件绑定、素材需求、VO 流程、混音风险和听觉验收矩阵。
