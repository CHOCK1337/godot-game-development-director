# 动作生成/返工提示模板

## 正向

Create a [duration] [loop/non-loop] animation for [character] performing [intent].
The motion must show [support/contact], [center-of-mass shift], and a clear phase structure:
[anticipation] → [drive] → [contact/impact] → [absorb/brake] → [recovery].
Match a travel distance of [distance] at [speed], viewed from [game camera].
Keep the start/end pose compatible with [state/combo].
Use [style-specific timing and silhouette rules].

## 具体负面

Avoid contact-foot sliding, floating pelvis, constant velocity, uniform easing, perfect bilateral symmetry, locked knees, over-smoothed arcs, missing anticipation, missing impact braking, hand/prop intersections, duplicated root displacement, and secondary motion that moves independently of the body.

## 强制交付

- contact frame/window list
- root displacement and facing change
- action event times
- start/end pose images
- known limitations
