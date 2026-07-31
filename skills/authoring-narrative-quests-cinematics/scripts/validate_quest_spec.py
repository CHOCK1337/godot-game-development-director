#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from collections import deque
from pathlib import Path
from typing import Any

def validate(data: dict[str, Any]) -> list[str]:
    issues=[]
    nodes=data.get("nodes",[]); edges=data.get("edges",[]); start=data.get("start_node")
    ids=[n.get("id") for n in nodes if isinstance(n,dict)]
    idset={x for x in ids if isinstance(x,str) and x}
    if len(ids)!=len(idset): issues.append("Duplicate or empty node id")
    if start not in idset: issues.append("Start node does not exist")
    adj={x:[] for x in idset}
    for e in edges:
        if not isinstance(e,dict): issues.append("Edge must be an object"); continue
        a,b=e.get("from"),e.get("to")
        if a not in idset or b not in idset: issues.append(f"Edge references missing node: {a}->{b}")
        elif a in adj: adj[a].append(b)
    reachable=set()
    if start in idset:
        q=deque([start])
        while q:
            cur=q.popleft()
            if cur in reachable: continue
            reachable.add(cur); q.extend(adj.get(cur,[]))
    unreachable=sorted(idset-reachable)
    if unreachable: issues.append("Unreachable nodes: "+", ".join(unreachable))
    terminals={n.get("id") for n in nodes if isinstance(n,dict) and n.get("type")=="terminal"}
    if not terminals: issues.append("No terminal node defined")
    elif not (terminals & reachable): issues.append("No reachable terminal node")
    if not data.get("fail_states"): issues.append("No fail/abandon state declared")
    if not data.get("save_keys"): issues.append("No stable save keys declared")
    return issues

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("file",type=Path); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); data=json.loads(a.file.read_text(encoding="utf-8")); issues=validate(data)
    if a.json: print(json.dumps({"valid":not issues,"issues":issues},ensure_ascii=False,indent=2))
    else:
        print("valid" if not issues else "\n".join(f"- {x}" for x in issues))
    return 0 if not issues else 1
if __name__=="__main__": raise SystemExit(main())
