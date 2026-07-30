# AI 动作失败图谱

| 症状 | 可观察证据 | 常见根因 | 首选修复 |
|---|---|---|---|
| 地上飘/滑冰 | 支撑期脚在世界空间移动 | 动画速度与角色速度不匹配；无 root motion；接触帧不稳 | 锁定接触窗；匹配 stride speed；只在接触窗做 IK 修正 |
| 脚底吸地 | 脚长时间完全静止，膝盖拉直 | 全程 IK、目标不释放 | 接触权重曲线；toe-off 前降低 influence |
| 身体像上下电梯 | root/hips 只有垂直正弦运动 | 用周期函数代替重心转移 | 让 down/up 对应支撑与 passing；加入左右髋位移 |
| 木偶摆臂 | 左右完美镜像、同相或固定幅度 | 自动镜像、无负重/意图 | 肩带反向扭转；按速度、武器和性格调幅度 |
| 关节软化/橡胶 | 四肢持续平滑，无明确 key pose | 过度 spline、关键姿势弱 | 重新建立 extreme/contact/impact；调整 spacing 而非只加 key |
| 攻击没有力量 | 武器匀速穿过目标 | 无 anticipation、加速、hit stop、制动 | 压缩 impact 前 spacing；命中后短 hold/反冲；明确 recovery |
| 受击像播放动画 | 与攻击方向、命中点无关 | 通用 clip、无程序层 | 根据 hit vector 选 clip/叠加姿势；同步碰撞和反馈 |
| 待机像屏保 | 所有部位同频循环 | 单一正弦、随机噪声 | 分层频率；主意图优先；长周期稀疏事件 |
| 表情 uncanny | 眼、眉、嘴同时线性变化 | 无 gaze lead、肌群阶段 | 眼先于头；眉/眼睑/嘴分时；减少无意义对称 |
| 转身漂移 | 身体旋转但脚不换支撑 | 原地旋转覆盖 locomotion | 使用 turn-in-place/turn-start；按角速度切换或程序步伐 |
| 混合后塌腰 | 两 clip 骨盆/胸腔基准不一致 | rest pose、root、blend mask | 统一基准；修 clip；限制 additive/mask 范围 |
| 次级动作抢戏 | 头发/布料幅度大、无衰减 | 参数过强、与主动作脱节 | 由加速度驱动；限制振幅；分 LOD；碰撞后衰减 |

## 误诊警告

- 脚滑不一定来自动画：CharacterBody 速度、delta、地面平台、缩放和 retarget 都可能造成。
- “僵硬”不一定缺少帧：可能是 silhouette、timing、阶段、camera 或状态切换问题。
- “自然”不等于写实：游戏动作常需更清晰 anticipation、更短 recovery 或更强 hit pose。
