#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
VAGUE=("好玩","有趣","沉浸","爽","史诗","fun","immersive","engaging","epic")

def validate(spec:dict[str,Any])->dict[str,list[str]]:
    errors=[]; warnings=[]
    required=("experience_goal","player_verbs","core_loop","mechanics","failure_and_recovery","playtest_hypotheses")
    for k in required:
        if k not in spec: errors.append(f"missing required field: {k}")
    goal=str(spec.get("experience_goal","")).strip()
    if len(goal)<10: errors.append("experience_goal is too short")
    if goal and any(v.lower() in goal.lower() for v in VAGUE): warnings.append("experience_goal contains vague adjectives; add observable player behavior")
    verbs=spec.get("player_verbs",[])
    if not isinstance(verbs,list) or not verbs: errors.append("player_verbs must be a non-empty list")
    else:
        norm=[str(v).strip().lower() for v in verbs]
        if len(norm)!=len(set(norm)): errors.append("player_verbs contains duplicates")
        if len(norm)>7: warnings.append("more than 7 core verbs may indicate mechanic sprawl")
    loop=spec.get("core_loop",[])
    if not isinstance(loop,list) or len(loop)<3: errors.append("core_loop needs at least 3 causal steps")
    else:
        for i,step in enumerate(loop):
            if not isinstance(step,dict): errors.append(f"core_loop[{i}] must be an object"); continue
            for k in ("step","player_decision","state_change","feedback"):
                if not step.get(k): errors.append(f"core_loop[{i}] missing {k}")
    ids=set()
    for i,m in enumerate(spec.get("mechanics",[]) if isinstance(spec.get("mechanics",[]),list) else []):
        if not isinstance(m,dict): errors.append(f"mechanics[{i}] must be an object"); continue
        mid=str(m.get("id","")).strip()
        if not mid: errors.append(f"mechanics[{i}] missing id")
        elif mid in ids: errors.append(f"duplicate mechanic id: {mid}")
        ids.add(mid)
        for k in ("verb","cost","success","failure","counterplay"):
            if not str(m.get(k,"")).strip(): errors.append(f"mechanic {mid or i} missing {k}")
        if verbs and m.get("verb") not in verbs: warnings.append(f"mechanic {mid or i} uses verb not listed in player_verbs")
    for r in spec.get("resources",[]) if isinstance(spec.get("resources",[]),list) else []:
        if not r.get("faucets"): warnings.append(f"resource {r.get('id','?')} has no faucet")
        if not r.get("sinks"): warnings.append(f"resource {r.get('id','?')} has no sink; inflation/hoarding risk")
    hypotheses=spec.get("playtest_hypotheses",[])
    if not isinstance(hypotheses,list) or not hypotheses: errors.append("playtest_hypotheses must be non-empty")
    else:
        for i,h in enumerate(hypotheses):
            for k in ("hypothesis","measure","falsifier"):
                if not isinstance(h,dict) or not str(h.get(k,"")).strip(): errors.append(f"playtest_hypotheses[{i}] missing {k}")
    return {"errors":errors,"warnings":warnings}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("spec",type=Path); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    try: spec=json.loads(args.spec.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as e: ap.error(str(e))
    result=validate(spec)
    if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for x in result["errors"]: print("ERROR:",x)
        for x in result["warnings"]: print("WARN:",x)
        print(f"summary: {len(result['errors'])} errors, {len(result['warnings'])} warnings")
    return 1 if result["errors"] else 0
if __name__=="__main__": raise SystemExit(main())
