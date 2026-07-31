# Changelog

All notable public changes are documented here. The project uses Semantic Versioning for public releases.

## [Unreleased]

- No public changes yet.

## [0.1.0-alpha.1] - 2026-07-31

### Changed

- narrowed the root Skill to cross-domain orchestration and added conditional output contracts
- made all 9 installable Skills self-contained with Codex UI metadata
- added 36 balanced direct, indirect, incomplete-evidence, and negative routing evaluations
- split installation into `director`, `modules`, and `full` scopes while preserving legacy aliases
- made project `AGENTS.md` opt-in and non-overwriting
- added generation and Doctor validation for 28 project-scoped Codex custom agents

### Validation and supply chain

- added relative-reference and evaluation validators
- added a pinned Godot 4.6.3 headless compile and smoke fixture for all 9 shipped GDScript examples
- pinned GitHub Actions to immutable commits and added Dependabot updates
- added release artifact attestations and immutable tag/release checks

## [0.1.0-alpha] - 2026-07-30

First public preview, derived from the internal v6 content-team package.

### Added

- 27 bounded specialist agent definitions and one orchestrator
- 8 modular game-development Skills
- deterministic specialist routing and sequential fallback workflows
- motion, gameplay, level, balance, procedural generation, replayability, narrative, NPC AI, camera, technical art, audio, UX, accessibility, localization, save/content-pipeline, playtest, and QA knowledge
- structured JSON contracts, templates, examples, and validators
- Codex project routing policy example
- installer, doctor, public-release validator, deterministic release builder, and GitHub Actions workflows
- repository health, security, contribution, attribution, roadmap, and release documentation
- Windows-safe package filenames for case-insensitive filesystems

### Verification status

- Python tests, structured file parsing, schema examples, package structure, archive CRC, and SHA-256 generation are covered by automated checks.
- This historical build only performed static GDScript validation. Live Godot compilation was added in `0.1.0-alpha.1`.

### Historical note

Internal package labels v3 through v6 were development milestones and were never public releases. They do not imply prior public Semantic Versioning releases.
