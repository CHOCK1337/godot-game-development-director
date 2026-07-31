# Orchestration Routing / 编排路由

Route by authority and shared state, not by keyword count.

| Problem / 问题 | Primary owner / 主责 | Conditional consumers / 条件协作 |
|---|---|---|
| Core loop, verbs, feedback | Gameplay Core Loop | Economy, Encounter, Godot Integration |
| Level topology, gates, landmarks | Level Design & Architecture | Narrative, Encounter, Procedural Generation |
| Difficulty targets and numeric bounds | Balance & Difficulty | Gameplay, Encounter, Playtest |
| Seeded generation and hard constraints | Procedural Generation | Level, Replayability, Godot Integration |
| Quest meaning and dialogue state | Narrative, Quest & Cinematics | Content Architecture, Level, Audio |
| NPC knowledge and decisions | NPC AI & Simulation | Action, Encounter, Godot Integration |
| Camera behavior | Gameplay Camera & Composition | Action, UX, Godot Integration |
| SFX, Foley, VO, mix | Sound Design, Voice & Mix | Narrative, Godot Audio |
| Adaptive BGM | Interactive Music | Godot Audio, Encounter |
| HUD, input, accessibility, localization | UX, Accessibility & Localization | Camera, Audio, Godot Integration |
| Save schema, IDs, authoring tools | Content Architecture, Save & Tools | Narrative, Godot Integration |
| Rendering and runtime budgets | Technical Art & Rendering | Asset Style, Godot Integration |

## Wave order / 波次顺序

1. Scope and evidence.
2. Authoritative rules, state, IDs, topology, schemas, and events.
3. Presentation and runtime consumers.
4. Integration.
5. Content QA, then final acceptance.

Parallel work is allowed only after shared contracts are frozen. One file or mutable state has one writer per wave.

## Escalation / 升级

- More than six specialists: split into two waves.
- No reproducible evidence: return a bounded capture plan before prescribing a large rewrite.
- Conflicting recommendations: tests and player evidence outrank preference; state authority outranks presentation convenience.
- Missing Godot/runtime access: label static findings separately from live-engine claims.
