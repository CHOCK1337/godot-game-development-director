#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def validate(data: dict[str, Any]) -> list[str]:
    issues=[]; budgets=data.get("budgets") or {}; measurements=data.get("measurements") or {}
    if not data.get("platform_profile"): issues.append("Missing platform profile")
    if not budgets: issues.append("No budgets defined")
    for key,limit in budgets.items():
        if not isinstance(limit,(int,float)) or limit<0: issues.append(f"Invalid budget: {key}"); continue
        if key not in measurements: issues.append(f"Missing measurement: {key}"); continue
        value=measurements[key]
        if not isinstance(value,(int,float)) or value<0: issues.append(f"Invalid measurement: {key}")
        elif value>limit: issues.append(f"Over budget {key}: {value} > {limit}")
    return issues

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("file",type=Path); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); issues=validate(json.loads(a.file.read_text(encoding="utf-8")))
    print(json.dumps({"valid":not issues,"issues":issues},ensure_ascii=False,indent=2) if a.json else ("valid" if not issues else "\n".join(f"- {x}" for x in issues)))
    return 0 if not issues else 1
if __name__=="__main__": raise SystemExit(main())
