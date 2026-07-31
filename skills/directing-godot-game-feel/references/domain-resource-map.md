# Domain Resource Map / 领域资源图

Load only the module Skill relevant to the task:

- Gameplay loop, economy, encounters: `$designing-godot-gameplay`
- Levels, balance, procedural generation, run variation: `$designing-godot-levels-balance-randomness`
- Narrative, dialogue, quests, cinematics: `$authoring-narrative-quests-cinematics`
- NPC perception, decisions, navigation, simulation: `$designing-npc-ai-simulation`
- Adaptive music and BGM transitions: `$directing-interactive-game-music`
- Camera, sound, rendering, UX, accessibility, localization: `$polishing-game-presentation-accessibility`
- Scope, vertical slice, milestones, freeze, cuts: `$producing-game-content`
- Content data, stable IDs, saves, migrations, tools: `$building-godot-content-pipelines`

If a requested module is unavailable, preserve the same ownership boundary and state what could not be loaded.

## Common authoritative contracts / 常见权威合同

| Contract | Producer | Consumers |
|---|---|---|
| `quest.state.changed` | Quest authority | Dialogue, UI, world, save, audio |
| `npc.intent.committed` | NPC decision layer | Action, camera, sound, encounter |
| `combat.hit.confirmed` | Combat authority | Animation response, VFX, SFX, camera, HUD |
| `camera.mode.changed` | Camera authority | Camera rig, UX settings |
| `audio.cue.requested` | Semantic event adapter | Audio runtime |
| `content.version.loaded` | Content/save layer | Quests, items, NPCs, tools |
| `accessibility.settings.changed` | Player settings | Camera, VFX, audio, UI |

Use stable IDs, event serials where replay/duplication matters, explicit schema versions, and one producer for every mutable fact.
