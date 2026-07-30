# Contributing

Thank you for improving Godot Game Development Director.

## Good contributions

- add a clearly scoped game-development technique
- improve routing without launching unnecessary specialists
- add a failing evaluation before changing Skill behavior
- add a validator or reproducible example
- correct Godot integration guidance using stable official documentation
- document failure cases from real projects without exposing private assets

## Before opening a pull request

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_public_release.py
python tests/validate_package.py
python -m unittest discover -s tests -v
```

Run the relevant example validators when changing schemas or tools.

## Skill requirements

Every Skill directory must contain `SKILL.md` with valid YAML frontmatter:

```yaml
---
name: lowercase-hyphenated-name
description: Use when ...
---
```

Descriptions must explain when the Skill applies. They should not replace the detailed workflow in the body.

## Agent requirements

A specialist must have:

- one bounded responsibility
- explicit exclusions
- required evidence
- a stable output contract
- clear edit ownership
- tests proving routing and expected behavior

Do not add a new Agent when an existing Skill, checklist, or deterministic script is sufficient.

## Copyright and privacy

Do not submit:

- copied commercial game content or proprietary design documents
- unlicensed images, music, models, fonts, or animations
- API keys, tokens, credentials, private URLs, or personal data
- large excerpts from books, courses, or documentation
- private Godot project files without authorization

## Pull request format

Explain:

1. the problem and affected users
2. the new behavior
3. evidence or references
4. tests added or changed
5. compatibility and migration risks
6. what is intentionally out of scope
