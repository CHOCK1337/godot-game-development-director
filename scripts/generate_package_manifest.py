#!/usr/bin/env python3
"""Generate the deterministic source-file manifest shipped with the package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

PACKAGE_VERSION = "0.1.0-alpha.1"
EXCLUDED_PARTS = {
    ".git",
    ".godot",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "release-build",
}
EXCLUDED_FILES = {"PACKAGE_MANIFEST.json"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def _files(root: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file()
            and path.name not in EXCLUDED_FILES
            and path.suffix.lower() not in EXCLUDED_SUFFIXES
            and not any(part in EXCLUDED_PARTS for part in path.relative_to(root).parts)
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path) -> dict[str, Any]:
    root = root.resolve()
    files = _files(root)
    return {
        "manifest_format": "godot-game-development-director/source-files/1",
        "package": "godot-game-development-director",
        "version": PACKAGE_VERSION,
        "maturity": "public-preview",
        "license": "Apache-2.0",
        "specialists": 27,
        "module_skills": 8,
        "installable_skills": 9,
        "scope": (
            "game content development; excludes store publishing, legal/privacy, "
            "LiveOps and production online backends"
        ),
        "file_count_excluding_manifest_and_dist": len(files),
        "files": [
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
            for path in files
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or (args.root / "PACKAGE_MANIFEST.json")
    payload = build_manifest(args.root)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {output}: {payload['file_count_excluding_manifest_and_dist']} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
