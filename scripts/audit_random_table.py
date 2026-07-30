#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any

def audit(table:dict[str,Any])->dict[str,Any]:
    errors=[]; warnings=[]; normalized=[]
    entries=table.get('entries',[])
    if not isinstance(entries,list) or not entries:
        return {'errors':['entries must be a non-empty list'],'warnings':[],'normalized':[]}
    ids=[]; parsed=[]
    for i,e in enumerate(entries):
        if not isinstance(e,dict): errors.append(f'entries[{i}] must be object'); continue
        eid=str(e.get('id','')).strip(); ids.append(eid)
        if not eid: errors.append(f'entries[{i}] missing id')
        try: weight=float(e.get('weight'))
        except (TypeError,ValueError): errors.append(f'entry {eid or i} weight must be numeric'); continue
        if weight<=0: errors.append(f'entry {eid or i} weight must be positive')
        parsed.append((eid,weight))
    if len(ids)!=len(set(ids)): errors.append('duplicate entry id')
    total=sum(max(w,0) for _,w in parsed)
    if total>0:
        normalized=[{'id':eid,'probability':max(w,0)/total} for eid,w in parsed]
        dominant=max(normalized,key=lambda x:x['probability'])
        policy=table.get('policy',{}) if isinstance(table.get('policy',{}),dict) else {}
        has_repeat_control=any(k in policy for k in ('max_repeat','history_size','cooldown_draws','shuffle_bag','pity_after'))
        if dominant['probability']>=0.60 and not has_repeat_control:
            warnings.append(f"dominant outcome {dominant['id']} has probability {dominant['probability']:.3f} without repeat control")
        if len(normalized)>1 and min(x['probability'] for x in normalized)<0.01 and 'pity_after' not in policy:
            warnings.append('rare outcome below 1% has no pity policy; long-tail frustration risk')
    return {'errors':errors,'warnings':warnings,'normalized':normalized}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('table',type=Path); ap.add_argument('--json',action='store_true'); args=ap.parse_args()
    try: data=json.loads(args.table.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as exc: ap.error(str(exc))
    result=audit(data)
    print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else json.dumps(result,ensure_ascii=False))
    return 1 if result['errors'] else 0
if __name__=='__main__': raise SystemExit(main())
