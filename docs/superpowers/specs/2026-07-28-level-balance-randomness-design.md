# Godot Level, Balance, Intensity, and Randomness v5 Design

## Goal

Extend the v4 Godot Game Feel Director into a fuller development-team package that can design and review level structure, global difficulty and balance, procedural generation, and run-to-run variety without collapsing those responsibilities into the existing encounter-pacing agent.

## Architecture

Add one independent Skill and four specialists:

1. `level-design-architecture`: spatial grammar, critical path, optional routes, landmarks, gating, traversal readability, encounter spaces, 2D/3D level structure.
2. `balance-difficulty`: challenge budgets, skill bands, fairness, damage/health/economy coupling, difficulty curves, DDA guardrails, telemetry and rollback thresholds.
3. `procedural-generation-randomness`: seeded deterministic generation, constraints, playability validation, weighted selection, generation repair, expressive-range evaluation and Godot runtime mapping.
4. `replayability-run-variation`: possibility space, run modifiers, encounter pools, drafts, random events, anti-repetition, pity/reroll policies and meaningful variation.

The existing `encounter-pacing` specialist retains local encounter rhythm and enemy composition. The new orchestrator routes only the smallest relevant set and resolves shared dependencies after parallel review.

## Contracts

Add validated JSON contracts for level specifications, balance models and generator specifications. Add deterministic tooling for validating those contracts, auditing weighted random tables and analyzing multi-seed playtest telemetry.

## Design Principles

- Randomness must produce bounded uncertainty, not arbitrary outcomes.
- Every generator must preserve hard invariants before optimizing variety.
- Seeds and RNG state must be reproducible for debugging, replays and multiplayer.
- Balance targets must be explicit; equal win rates are not universally the right target.
- Dynamic difficulty should adjust pacing or support first when possible, and must not secretly invalidate player mastery.
- Generated levels are evaluated by playability, fairness, readability, pacing and expressive range, not merely uniqueness.
- Level intensity is a curve with recovery and contrast, not a monotonic increase.

## Testing

- Package validation requires 18 specialists and all new modules.
- Router tests cover level-only, balance-only, procedural generation and combined roguelike requests.
- Validators reject disconnected critical paths, undefined balance metrics, missing generator invariants and unsafe random tables.
- Telemetry analysis identifies seed outliers, choke-point deaths, low path diversity and excessive difficulty variance.
