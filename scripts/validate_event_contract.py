#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from typing import Any
PATTERN=re.compile(r"^[a-z0-9_]+(?:\.[a-z0-9_]+)+$")

def validate(data:dict[str,Any])->dict[str,list[str]]:
    errors=[]; warnings=[]; seen=set()
    events=data.get("events",[])
    if not isinstance(events,list) or not events: return {"errors":["events must be a non-empty list"],"warnings":[]}
    for i,e in enumerate(events):
        if not isinstance(e,dict): errors.append(f"events[{i}] must be an object"); continue
        eid=str(e.get("event_id","")).strip()
        if not PATTERN.match(eid): errors.append(f"invalid namespaced event_id: {eid or i}")
        if eid in seen: errors.append(f"duplicate event_id: {eid}")
        seen.add(eid)
        for k in ("producer","timing","dedupe","fallback"):
            if not str(e.get(k,"")).strip(): errors.append(f"event {eid or i} missing {k}")
        consumers=e.get("consumers",[])
        if not isinstance(consumers,list) or not consumers: errors.append(f"event {eid or i} has no consumers")
        elif len(consumers)!=len(set(map(str,consumers))): errors.append(f"event {eid or i} has duplicate consumers")
        if eid.endswith("requested") and any(c in {"music","bgm"} for c in consumers):
            warnings.append(f"{eid}: BGM should usually consume stable encounter/state events, not raw input requests")
        if "hit.confirmed" in eid and str(e.get("producer","")).lower() in {"animation","vfx","audio"}:
            warnings.append(f"{eid}: hit confirmation producer may not be authoritative")
        if "music" in consumers and not e.get("payload"):
            warnings.append(f"{eid}: music consumer has no payload/state semantics")
    return {"errors":errors,"warnings":warnings}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("contract",type=Path); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    try: data=json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: ap.error(str(exc))
    result=validate(data)
    if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for x in result["errors"]: print("ERROR:",x)
        for x in result["warnings"]: print("WARN:",x)
        print(f"summary: {len(result['errors'])} errors, {len(result['warnings'])} warnings")
    return 1 if result["errors"] else 0
if __name__=="__main__": raise SystemExit(main())
