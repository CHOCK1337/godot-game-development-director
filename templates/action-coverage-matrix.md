# 动作覆盖矩阵

用于确认一次角色动作审查没有只看 locomotion。

| 域 | 需要的动作 | 接触/事件 | 过渡 | Godot 状态/层 |
|---|---|---|---|---|
| Idle/Acting | 呼吸、警觉、疲劳、对话 | gaze、手势 | idle↔move/action | base + face/look |
| Locomotion | start、walk、run、sprint、strafe、turn、stop | foot contact | speed/direction | locomotion BlendSpace |
| Air | jump、fall、land | takeoff/landing | ground↔air | airborne state |
| Traversal | climb、vault、ledge、swim | hand/foot targets | enter/loop/exit | interaction state |
| Combat | attacks、block、dodge、hit、death | hitbox/hurtbox | combo/cancel | action/OneShot |
| Ranged | aim、fire、reload | muzzle/magazine | aim↔move | upper body/full body |
| Magic | charge、release、recover | cast/VFX | locomotion override | action + events |
| Interaction | pickup、door、push、sit | socket/prop | align/use/exit | interaction state |
| Face/Hands | gaze、blink、emotion、grip | target/phoneme | layered | modifiers/additive |
| Secondary | hair、cloth、tail、weapon lag | collision | LOD/on-off | skeleton modifiers |
