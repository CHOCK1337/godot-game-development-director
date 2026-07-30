# Godot Content Team v6 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans task-by-task.

**Goal:** Add nine content-production specialist agents, five installable skills, structured contracts, validators, Godot examples, auto-routing rules and verification to the v5 package.

**Architecture:** Extend the existing deterministic router and portable specialist contract. Keep design responsibilities isolated, route only relevant agents, merge shared facts through the orchestrator, then validate through content QA and final QA.

**Tech Stack:** Markdown Skills/Agents, JSON Schema, YAML, Python 3 standard library, GDScript examples.

## Global Constraints

- Do not add publishing, store, legal, rating, marketing, live-ops or online-service departments.
- Preserve all v5 behavior and tests.
- New scripts use Python standard library only.
- Specialists do not concurrently write shared .tscn/.tres/resources.
- GDScript is statically reviewed, not claimed engine-compiled.

## Tasks

1. Write failing tests for routing, required files and five validators.
2. Add nine specialist prompts and five modular Skills.
3. Add knowledge, checklists and templates for each content domain.
4. Add JSON schemas, validators, examples and Godot helper scripts.
5. Update router, orchestrator, root Skill, README, workflows and Codex policy.
6. Run all tests, schema checks, package validation and example commands.
7. Generate manifest, ZIP and SHA-256; verify ZIP integrity.
