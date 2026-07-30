#!/usr/bin/env python3
"""Build a deterministic GitHub Release attachment and SHA256SUMS file."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import zipfile
from pathlib import Path
from typing import Any

PACKAGE_NAME = "godot-game-development-director"
EXCLUDED_PARTS = {".git", ".godot", "__pycache__", ".pytest_cache", ".mypy_cache", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
VERSION_RE = re.compile(r"^v?\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
ZIP_TIME = (2020, 1, 1, 0, 0, 0)


def _included_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        result.append(path)
    return sorted(result, key=lambda p: p.relative_to(root).as_posix())


def _write_deterministic_zip(root: Path, archive: Path, files: list[Path]) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            rel = path.relative_to(root).as_posix()
            arcname = f"{PACKAGE_NAME}/{rel}"
            info = zipfile.ZipInfo(arcname, ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if path.stat().st_mode & 0o111 else 0o644) << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_release(root: Path, output: Path, version: str = "v0.1.0-alpha") -> dict[str, Any]:
    root = root.resolve()
    output = output.resolve()
    if not VERSION_RE.fullmatch(version):
        raise ValueError(f"Invalid release version: {version}")
    tag = version if version.startswith("v") else f"v{version}"

    files = _included_files(root)
    if len(files) < 200:
        raise RuntimeError(f"Refusing to build unexpectedly small package: {len(files)} files")

    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"{PACKAGE_NAME}-{tag}.zip"
    checksums = output / "SHA256SUMS"
    temp_archive = archive.with_suffix(".zip.tmp")
    if temp_archive.exists():
        temp_archive.unlink()

    _write_deterministic_zip(root, temp_archive, files)
    temp_archive.replace(archive)

    with zipfile.ZipFile(archive) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"ZIP CRC validation failed at {bad}")
        if len(zf.infolist()) != len(files):
            raise RuntimeError("ZIP entry count mismatch")

    sha = _sha256(archive)
    checksums.write_text(f"{sha}  {archive.name}\n", encoding="utf-8", newline="\n")

    return {
        "archive": archive,
        "checksums": checksums,
        "sha256": sha,
        "file_count": len(files),
        "version": tag,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="v0.1.0-alpha")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output = args.output or (root / "dist")
    if args.clean and output.exists():
        shutil.rmtree(output)

    result = build_release(root, output, version=args.version)
    print(f"archive: {result['archive']}")
    print(f"files: {result['file_count']}")
    print(f"sha256: {result['sha256']}")
    print(f"checksums: {result['checksums']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
