#!/usr/bin/env python3
"""Validate the repository before a public release.

The checks are deterministic and intentionally conservative. They validate the
package shape, Skill frontmatter, JSON/YAML syntax, Python syntax, forbidden
files, and a small set of high-confidence credential patterns.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_FILES = {
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "NOTICE.md",
    "THIRD_PARTY_NOTICES.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "CITATION.cff",
    "AGENTS.md",
    "SKILL.md",
    "RELEASE_NOTES.md",
    "manifest.json",
    "requirements-dev.txt",
    ".codex-plugin/plugin.json",
    ".github/dependabot.yml",
    "agents/orchestrator.md",
    "agents/routing-table.md",
    "codex/AGENTS.md.example",
    "docs/RELEASE_GUIDE.zh-CN.md",
    ".github/workflows/validate.yml",
    ".github/workflows/release.yml",
    "scripts/build_release.py",
    "scripts/install.py",
    "scripts/doctor.py",
    "scripts/generate_codex_agents.py",
    "scripts/generate_package_manifest.py",
    "scripts/run_godot_validation.py",
    "scripts/validate_skill_evals.py",
    "scripts/validate_skill_references.py",
    "skills/directing-godot-game-feel/SKILL.md",
    "tests/godot_fixture/project.godot",
    "tests/godot_fixture/validate_package_scripts.gd",
}

FORBIDDEN_NAMES = {
    ".env",
    ".DS_Store",
    "export_credentials.cfg",
    "id_rsa",
    "id_ed25519",
}
IGNORED_SCAN_PARTS = {".git"}
FORBIDDEN_PARTS = {".godot", "__pycache__", ".pytest_cache", ".mypy_cache"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".pem", ".key", ".p12", ".pfx"}

# Keep these patterns narrow enough to avoid flagging documentation placeholders.
SECRET_PATTERNS = {
    "GitHub classic token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"),
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}

FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---(?:\n|$)", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _relative_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and not any(part in IGNORED_SCAN_PARTS for part in path.relative_to(root).parts)
    )


def _validate_skill(path: Path, errors: list[str], expected_name: str | None = None) -> None:
    text = _read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"Skill frontmatter missing: {path}")
        return

    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"\'')

    name = fields.get("name", "")
    description = fields.get("description", "")
    if not NAME_RE.fullmatch(name):
        errors.append(f"Invalid Skill name '{name}' in {path}")
    if expected_name is not None and name != expected_name:
        errors.append(f"Skill name/path mismatch in {path}: {name!r} != {expected_name!r}")
    if not description.startswith("Use when"):
        errors.append(f"Skill description must start with 'Use when': {path}")


def _load_local_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load validator module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validate_skill_metadata(skill_dir: Path, errors: list[str]) -> None:
    path = skill_dir / "agents/openai.yaml"
    if not path.is_file():
        errors.append(f"Missing Skill UI metadata: {path}")
        return
    try:
        payload = _load_yaml(path)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Cannot parse Skill UI metadata {path}: {exc}")
        return
    interface = payload.get("interface", {}) if isinstance(payload, dict) else {}
    for field in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            errors.append(f"Skill UI metadata missing interface.{field}: {path}")
    short = interface.get("short_description", "")
    if isinstance(short, str) and not 25 <= len(short) <= 64:
        errors.append(f"Skill short_description must be 25-64 characters: {path}")
    prompt = interface.get("default_prompt", "")
    if isinstance(prompt, str) and f"${skill_dir.name}" not in prompt:
        errors.append(f"Skill default_prompt must mention ${skill_dir.name}: {path}")


def _load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover - dependency error is explicit
        raise RuntimeError("PyYAML is required; install requirements-dev.txt") from exc
    return yaml.safe_load(_read_text(path))


def validate_release(root: Path) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        return {"root": str(root), "errors": ["Release root does not exist"], "warnings": []}

    for rel in sorted(REQUIRED_FILES):
        if not (root / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    files = _relative_files(root)
    for path in files:
        rel = path.relative_to(root)
        if any(part in FORBIDDEN_PARTS for part in rel.parts):
            errors.append(f"Forbidden generated directory/file: {rel.as_posix()}")
        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"Forbidden file: {rel.as_posix()}")

        # Skip binary archives and images for text scans.
        if path.suffix.lower() in {".zip", ".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            continue
        try:
            text = _read_text(path)
        except UnicodeDecodeError:
            warnings.append(f"Skipped non-UTF-8 file: {rel.as_posix()}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"Possible {label} in {rel.as_posix()}")

    # Parse structured files.
    for path in files:
        rel = path.relative_to(root).as_posix()
        try:
            if path.suffix.lower() == ".json":
                json.loads(_read_text(path))
            elif path.suffix.lower() in {".yaml", ".yml"}:
                _load_yaml(path)
            elif path.suffix.lower() == ".py":
                compile(_read_text(path), rel, "exec")
        except Exception as exc:  # noqa: BLE001 - report all parser failures
            errors.append(f"Cannot parse {rel}: {exc}")

    skill_paths = sorted((root / "skills").glob("*/SKILL.md"))
    root_skill = root / "SKILL.md"
    if root_skill.is_file():
        _validate_skill(root_skill, errors, "directing-godot-game-feel")
    for skill in skill_paths:
        _validate_skill(skill, errors, skill.parent.name)
        _validate_skill_metadata(skill.parent, errors)

    reference_validator = _load_local_module(
        "release_skill_reference_validator",
        root / "scripts/validate_skill_references.py",
    )
    eval_validator = _load_local_module(
        "release_skill_eval_validator",
        root / "scripts/validate_skill_evals.py",
    )
    for skill_dir in [root, *(path.parent for path in skill_paths)]:
        for issue in reference_validator.validate_skill_directory(skill_dir):
            errors.append(f"{skill_dir}: {issue}")
    for skill in skill_paths:
        for issue in eval_validator.validate_skill_evals(skill.parent):
            errors.append(f"{skill.parent}: {issue}")

    specialists = sorted((root / "agents" / "specialists").glob("*.md"))
    module_skills = [path for path in skill_paths if path.parent.name != "directing-godot-game-feel"]
    if len(module_skills) != 8:
        errors.append(f"Expected exactly 8 module Skills, found {len(module_skills)}")
    if len(skill_paths) != 9:
        errors.append(f"Expected 9 installable Skills including the director, found {len(skill_paths)}")
    if len(specialists) < 27:
        errors.append(f"Expected at least 27 specialists, found {len(specialists)}")

    manifest_path = root / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(_read_text(manifest_path))
            notice = manifest.get("standard_notice", "")
            if "not part of the Agent Skills standard" not in notice:
                errors.append("manifest.json must state that its format is project-specific")
            version = manifest.get("package", {}).get("version")
            if version != "0.1.0-alpha.1":
                errors.append(f"manifest.json version mismatch: {version!r}")
        except Exception as exc:  # already reported above, keep useful context
            errors.append(f"Cannot validate manifest.json: {exc}")

    readme = root / "README.md"
    if readme.is_file():
        text = _read_text(readme)
        for phrase in ["v0.1.0-alpha.1", "27 specialist", "8 modular Skills", "Apache-2.0"]:
            if phrase not in text:
                errors.append(f"README.md missing public-release phrase: {phrase}")

    plugin_path = root / ".codex-plugin/plugin.json"
    if plugin_path.is_file():
        try:
            plugin = json.loads(_read_text(plugin_path))
            if plugin.get("version") != "0.1.0-alpha.1":
                errors.append("plugin.json version must match 0.1.0-alpha.1")
            if plugin.get("skills") != "./skills/":
                errors.append("plugin.json must expose ./skills/")
        except Exception as exc:
            errors.append(f"Cannot validate plugin.json: {exc}")

    package_manifest_path = root / "PACKAGE_MANIFEST.json"
    if package_manifest_path.is_file():
        try:
            manifest_generator = _load_local_module(
                "release_package_manifest_generator",
                root / "scripts/generate_package_manifest.py",
            )
            expected = manifest_generator.build_manifest(root)
            actual = json.loads(_read_text(package_manifest_path))
            if actual != expected:
                errors.append(
                    "PACKAGE_MANIFEST.json is stale; run scripts/generate_package_manifest.py"
                )
        except Exception as exc:
            errors.append(f"Cannot validate PACKAGE_MANIFEST.json: {exc}")

    digest = hashlib.sha256()
    for path in files:
        rel = path.relative_to(root).as_posix()
        if rel.startswith("dist/"):
            continue
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")

    return {
        "root": str(root),
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "files": len(files),
        "skills": len(skill_paths),
        "specialists": len(specialists),
        "content_sha256": digest.hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    report = validate_release(args.root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            f"validated {report.get('files', 0)} files, "
            f"{report.get('skills', 0)} installable Skills, "
            f"{report.get('specialists', 0)} specialists"
        )
        for warning in report.get("warnings", []):
            print(f"warning: {warning}", file=sys.stderr)
        for error in report.get("errors", []):
            print(f"error: {error}", file=sys.stderr)

    return 1 if report.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
