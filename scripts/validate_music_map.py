#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from collections import defaultdict,deque
from pathlib import Path
from typing import Any

def validate(data:dict[str,Any])->dict[str,list[str]]:
    errors=[]; warnings=[]
    states=data.get("states",[]); transitions=data.get("transitions",[])
    if not isinstance(states,list) or not states: errors.append("states must be a non-empty list"); states=[]
    ids=[]; smap={}
    for i,s in enumerate(states):
        sid=str(s.get("id","")).strip() if isinstance(s,dict) else ""
        if not sid: errors.append(f"states[{i}] missing id"); continue
        if sid in smap: errors.append(f"duplicate state id: {sid}")
        ids.append(sid); smap[sid]=s
        if not str(s.get("purpose","")).strip(): errors.append(f"state {sid} missing purpose")
        if not isinstance(s.get("bpm"),(int,float)) or s.get("bpm",0)<=0: errors.append(f"state {sid} has invalid bpm")
        if not re.match(r"^\d+/\d+$",str(s.get("meter",""))): errors.append(f"state {sid} has invalid meter")
        if float(s.get("min_hold_seconds",-1))<0: errors.append(f"state {sid} has invalid min_hold_seconds")
        layers=s.get("layers",[])
        if not isinstance(layers,list) or not layers: errors.append(f"state {sid} has no layers")
        elif len(layers)!=len(set(map(str,layers))): errors.append(f"state {sid} has duplicate layers")
    default=data.get("default_state")
    fallback=data.get("fallback_state",default)
    if default not in smap: errors.append("default_state does not reference a valid state")
    if fallback not in smap: errors.append("fallback_state does not reference a valid state")
    seen=set(); graph=defaultdict(list)
    for i,t in enumerate(transitions if isinstance(transitions,list) else []):
        if not isinstance(t,dict): errors.append(f"transitions[{i}] must be an object"); continue
        a,b=t.get("from"),t.get("to"); key=(a,b,t.get("trigger"))
        if a not in smap: errors.append(f"transition {i} has unknown from state: {a}")
        if b not in smap: errors.append(f"transition {i} has unknown to state: {b}")
        if key in seen: errors.append(f"duplicate transition: {key}")
        seen.add(key); graph[a].append(b)
        q=t.get("quantization")
        if q not in {"immediate","beat","bar","phrase","end"}: errors.append(f"transition {i} has invalid quantization")
        if float(t.get("cooldown_seconds",-1))<0: errors.append(f"transition {i} has invalid cooldown_seconds")
        if a in smap and b in smap and q in {"beat","bar","phrase"}:
            if (smap[a].get("bpm"),smap[a].get("meter")) != (smap[b].get("bpm"),smap[b].get("meter")) and not t.get("tempo_bridge"):
                warnings.append(f"{a}->{b} is quantized but tempo/meter changes without tempo_bridge")
        if q=="immediate" and not t.get("stinger"):
            warnings.append(f"{a}->{b} switches immediately without a stinger or explicit hard-cut justification")
    if default in smap:
        reached={default}; q=deque([default])
        while q:
            cur=q.popleft()
            for nxt in graph[cur]:
                if nxt not in reached: reached.add(nxt); q.append(nxt)
        for sid in smap:
            if sid not in reached: warnings.append(f"state unreachable from default_state: {sid}")
    if "Music" not in data.get("buses",[]): warnings.append("buses should normally include a Music bus")
    return {"errors":errors,"warnings":warnings}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("map",type=Path); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    try: data=json.loads(args.map.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as e: ap.error(str(e))
    result=validate(data)
    if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for x in result["errors"]: print("ERROR:",x)
        for x in result["warnings"]: print("WARN:",x)
        print(f"summary: {len(result['errors'])} errors, {len(result['warnings'])} warnings")
    return 1 if result["errors"] else 0
if __name__=="__main__": raise SystemExit(main())
