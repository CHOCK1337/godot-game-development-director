---
name: polishing-game-presentation-accessibility
description: Use when Godot camera, HUD, menus, sound effects, voice, rendering, localization, subtitles, input, readability, motion comfort, or content presentation needs coordinated polish and accessibility. 当表现层需要保留玩法信息并提供等价感知渠道时使用。
---

# Polishing Game Presentation & Accessibility

## Boundary / 边界

Own presentation consumption and player-configurable access, not gameplay truth. Camera, SFX, VFX, HUD, captions, and music must consume authoritative semantic events and must degrade without hiding decisions.

负责表现层如何传达事实和无障碍设置，不拥有战斗、任务或 NPC 的规则真相。

## Required evidence / 所需证据

- Capture with input/state timeline and semantic event IDs.
- Camera modes, target resolutions/devices, render/audio budgets, and priority rules.
- Language list, text expansion, font/fallback coverage, input methods, focus order, subtitles/captions, and reduced-motion settings.
- Baseline measurements: frame time, overdraw/draw calls where relevant, loudness/voice priority, occlusion, and readability failures.

## Order / 顺序

1. Preserve gameplay facts and readable timing.
2. Establish camera composition and motion limits.
3. Establish sound cue meaning and mix priority.
4. Fit visual assets to measured rendering budgets.
5. Provide equivalent information channels and configurable motion/input.
6. Validate localization, focus order, text expansion and target-device profiles.

## Required output / 强制输出

Information-priority table; semantic event consumers; camera limits; audio cue/mix priority; rendering budget and degradation ladder; equivalent visual/audio/text channels; settings ownership; device/language/input test matrix; measurable pass thresholds and rollback.

Do not use screen shake, bass, bloom, particles or loudness to hide weak rules or animation.
