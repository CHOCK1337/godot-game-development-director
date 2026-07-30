#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from collections import deque
from pathlib import Path
from typing import Any

def validate(data: dict[str, Any]) -> list[str]:
    issues=[]; states=data.get("states",[]); state_set=set(states)
    if not states or len(states)!=len(state_set): issues.append("States must be non-empty and unique")
    initial=data.get("initial_state"); fallback=data.get("fallback_state")
    if initial not in state_set: issues.append("Initial state is missing")
    if fallback not in state_set: issues.append("Fallback state is missing")
    adj={s:[] for s in state_set}
    for t in data.get("transitions",[]):
        a,b=t.get("from"),t.get("to")
        if a not in state_set or b not in state_set: issues.append(f"Transition references missing state: {a}->{b}")
        else: adj[a].append(b)
        if not t.get("trigger"): issues.append(f"Transition {a}->{b} has no trigger")
    reachable=set()
    if initial in state_set:
        q=deque([initial])
        while q:
            s=q.popleft()
            if s in reachable: continue
            reachable.add(s); q.extend(adj.get(s,[]))
    if state_set-reachable: issues.append("Unreachable states: "+", ".join(sorted(state_set-reachable)))
    perception=data.get("perception") or {}
    if not any(bool(v) for v in perception.values() if isinstance(v,bool)): issues.append("No enabled perception channel")
    debug=data.get("debug_fields") or []
    if not debug or "state" not in debug: issues.append("Debug fields must include state and decision context")
    return issues

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("file",type=Path); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); issues=validate(json.loads(a.file.read_text(encoding="utf-8")))
    print(json.dumps({"valid":not issues,"issues":issues},ensure_ascii=False,indent=2) if a.json else ("valid" if not issues else "\n".join(f"- {x}" for x in issues)))
    return 0 if not issues else 1
if __name__=="__main__": raise SystemExit(main())
