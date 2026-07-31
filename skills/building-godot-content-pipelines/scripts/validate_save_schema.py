#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def validate(data: dict[str, Any]) -> list[str]:
    issues=[]; version=data.get("schema_version")
    if not isinstance(version,int) or version<1: issues.append("Invalid schema version"); version=1
    keys=data.get("root_keys") or []
    if len(keys)!=len(set(keys)): issues.append("Duplicate root keys")
    for key in ["player","world","settings"]:
        if key not in keys: issues.append(f"Missing root key: {key}")
    pairs={(m.get("from"),m.get("to")) for m in data.get("migrations",[]) if isinstance(m,dict)}
    for v in range(1,version):
        if (v,v+1) not in pairs: issues.append(f"Missing sequential migration {v}->{v+1}")
    if not data.get("atomic_write"): issues.append("Atomic write is required")
    if int(data.get("backup_slots",0) or 0)<1: issues.append("At least one backup slot is required")
    if data.get("unknown_key_policy") not in {"preserve","ignore"}: issues.append("Unknown key policy should preserve or ignore for compatibility")
    return issues

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("file",type=Path); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); issues=validate(json.loads(a.file.read_text(encoding="utf-8")))
    print(json.dumps({"valid":not issues,"issues":issues},ensure_ascii=False,indent=2) if a.json else ("valid" if not issues else "\n".join(f"- {x}" for x in issues)))
    return 0 if not issues else 1
if __name__=="__main__": raise SystemExit(main())
