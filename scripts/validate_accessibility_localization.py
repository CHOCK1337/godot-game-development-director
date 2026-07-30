#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def validate(data: dict[str, Any]) -> list[str]:
    issues=[]; locales=data.get("locales") or []; subtitles=data.get("subtitles") or {}
    if not locales: issues.append("No locales declared")
    if not subtitles.get("enabled"): issues.append("Subtitles are not enabled")
    if not subtitles.get("speaker_labels"): issues.append("Subtitles lack speaker labels")
    if not data.get("input_remap"): issues.append("Input remapping is missing")
    if not data.get("reduced_motion"): issues.append("Reduced motion option is missing")
    if not data.get("screen_reader_labels"): issues.append("Screen reader labels are missing")
    expansion=data.get("text_expansion_test",0)
    if len(locales)>1 and (not isinstance(expansion,(int,float)) or expansion<1.3): issues.append("Text expansion test must be at least 1.3 for localized UI")
    return issues

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("file",type=Path); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); issues=validate(json.loads(a.file.read_text(encoding="utf-8")))
    print(json.dumps({"valid":not issues,"issues":issues},ensure_ascii=False,indent=2) if a.json else ("valid" if not issues else "\n".join(f"- {x}" for x in issues)))
    return 0 if not issues else 1
if __name__=="__main__": raise SystemExit(main())
