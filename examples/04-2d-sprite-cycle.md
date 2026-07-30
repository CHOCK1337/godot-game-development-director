# 示例：8 帧像素走路不能加帧

不增加帧数，重新分配：

- F1 左 contact：清楚脚底、髋偏左。
- F2 左 down：身体最低、膝弯。
- F3 passing：右脚经过，轮廓收窄。
- F4 up/push：身体最高、左脚推离。
- F5 右 contact。
- F6 右 down。
- F7 passing。
- F8 up/push。

关键不是每帧均匀播放。可让 contact/down 稍长，passing/up 稍短，产生重量和推进。保证每帧裁切基线一致；CharacterBody2D 每循环位移与画面步幅一致。
