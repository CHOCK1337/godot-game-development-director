#!/usr/bin/env python3
"""Compile and smoke-test every shipped GDScript in a real Godot process."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def find_godot(explicit: str | None = None) -> str | None:
    if explicit:
        candidate = Path(explicit)
        if candidate.is_file():
            return str(candidate.resolve())
        return shutil.which(explicit)
    for name in ("godot4", "godot"):
        resolved = shutil.which(name)
        if resolved:
            return resolved
    return None


def validate_with_godot(root: Path, executable: str) -> int:
    root = root.resolve()
    fixture = root / "tests/godot_fixture"
    command = [
        executable,
        "--headless",
        "--path",
        str(fixture),
        "--script",
        "res://validate_package_scripts.gd",
        "--",
        "--source-root",
        str(root),
    ]
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    finally:
        shutil.rmtree(fixture / ".godot", ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", help="Godot executable name or path")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    executable = find_godot(args.godot)
    if executable is None:
        print(
            "Godot 4 executable not found. Pass --godot PATH or install godot4.",
            file=sys.stderr,
        )
        return 2
    return validate_with_godot(args.root, executable)


if __name__ == "__main__":
    raise SystemExit(main())
