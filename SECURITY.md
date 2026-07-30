# Security Policy

## Supported versions

Only the latest public preview receives security-related fixes.

## Reporting a vulnerability

Use GitHub private vulnerability reporting when it is enabled for the repository. Do not publish credentials, exploit details, private project data, or sensitive logs in a public issue.

If private reporting is unavailable, open a minimal issue titled `Security contact requested` without technical details and ask a maintainer for a private channel.

## Security boundaries

This repository contains prompts and scripts that may be used by agents capable of running commands or editing files. The package does not grant permissions by itself. Runtime permissions are controlled by the user's agent environment.

Recommended defaults:

- specialists are read-only unless an edit is necessary
- one main executor owns shared file changes
- network access is limited to reference research
- publishing, pushing, deleting, and credential access require human approval
- secrets never belong in prompts, logs, examples, or commits

## Out of scope

Security reports should concern this repository's scripts, workflow files, schemas, release artifacts, or documented agent behavior. General Godot engine vulnerabilities should be reported to the Godot project through its official process.
