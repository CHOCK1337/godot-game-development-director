# Godot Game Development Director v0.1.0-alpha

First public preview of the project previously developed internally as the v6 content-team package.

## Highlights

- 27 specialist Agent definitions and one orchestrator
- 8 modular Skills
- motion, gameplay, level, balance, procedural generation, narrative, NPC AI, camera, rendering, audio, UX, save/content pipeline, and QA workflows
- deterministic specialist routing
- JSON contracts, validators, templates, examples, and tests
- Codex project policy for implicit Skill use and specialist selection
- public repository health files, installer, doctor, release builder, and GitHub Actions

## Verification performed

- package structure validation
- 56 Python unit tests
- 11 JSON Schema example validations
- Python syntax checks
- Python unit tests
- JSON and YAML parsing
- structured example validation
- forbidden-file and basic secret-pattern scan
- deterministic release ZIP build
- SHA-256 checksum generation
- ZIP CRC verification
- case-insensitive filename collision scan and Windows extraction smoke test

## Known limitations

- GDScript examples were not compiled in a live Godot editor in the build environment
- multi-Agent behavior has not been validated across every Codex or third-party runtime
- the project is Godot-focused; Unity and Unreal adapters are not included
- the package does not replace real player testing or professional accessibility review
- publishing, store operations, legal/privacy compliance, LiveOps, and production online backends are out of scope

## Upgrade status

This is the first public version. Internal v3-v6 numbers are preserved only as pre-public history in the changelog and must not be interpreted as prior public releases.
