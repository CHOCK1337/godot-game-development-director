#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any

def validate(spec:dict[str,Any])->dict[str,list[str]]:
    errors=[]; warnings=[]
    required=('experience_goal','level_type','player_capabilities','topology','critical_path','intensity_curve','hard_invariants','playtest_hypotheses')
    for key in required:
        if key not in spec: errors.append(f'missing required field: {key}')
    topology=spec.get('topology',{}) if isinstance(spec.get('topology',{}),dict) else {}
    nodes=topology.get('nodes',[]) if isinstance(topology.get('nodes',[]),list) else []
    edges=topology.get('edges',[]) if isinstance(topology.get('edges',[]),list) else []
    ids=[]
    for i,node in enumerate(nodes):
        nid=str(node.get('id','')).strip() if isinstance(node,dict) else ''
        if not nid: errors.append(f'topology.nodes[{i}] missing id')
        ids.append(nid)
    if len(ids)!=len(set(ids)): errors.append('topology contains duplicate node ids')
    idset=set(ids)
    edge_set=set()
    for i,edge in enumerate(edges):
        if not isinstance(edge,dict): errors.append(f'topology.edges[{i}] must be an object'); continue
        a=str(edge.get('from','')); b=str(edge.get('to',''))
        if a not in idset or b not in idset: errors.append(f'topology edge references unknown node: {a}->{b}')
        edge_set.add((a,b))
        if edge.get('bidirectional'): edge_set.add((b,a))
    path=spec.get('critical_path',[]) if isinstance(spec.get('critical_path',[]),list) else []
    if len(path)<2: errors.append('critical_path needs at least start and goal')
    for n in path:
        if n not in idset: errors.append(f'critical_path references unknown node: {n}')
    for a,b in zip(path,path[1:]):
        if (a,b) not in edge_set: errors.append(f'critical_path edge missing: {a}->{b}')
    for route in spec.get('optional_routes',[]) if isinstance(spec.get('optional_routes',[]),list) else []:
        rpath=route.get('path',[]) if isinstance(route,dict) else []
        if len(rpath)<2: errors.append(f"optional route {route.get('id','?')} needs at least 2 nodes")
        if not route.get('rejoins',False) and not str(route.get('value','')).strip(): errors.append(f"optional route {route.get('id','?')} neither rejoins nor declares terminal value")
    curve=spec.get('intensity_curve',[]) if isinstance(spec.get('intensity_curve',[]),list) else []
    vals=[]
    for i,point in enumerate(curve):
        try: vals.append(float(point['intensity']))
        except (TypeError,ValueError,KeyError): errors.append(f'intensity_curve[{i}] missing numeric intensity')
    has_recovery=any(vals[i] < vals[i-1]-1 for i in range(1,len(vals))) if len(vals)>1 else False
    if vals and not has_recovery: warnings.append('intensity curve has no meaningful recovery drop')
    if not spec.get('landmarks'): warnings.append('no landmarks declared; orientation risk')
    hypotheses=spec.get('playtest_hypotheses',[])
    if not isinstance(hypotheses,list) or not hypotheses: errors.append('playtest_hypotheses must be non-empty')
    else:
        for i,h in enumerate(hypotheses):
            for k in ('hypothesis','measure','falsifier'):
                if not isinstance(h,dict) or not str(h.get(k,'')).strip(): errors.append(f'playtest_hypotheses[{i}] missing {k}')
    return {'errors':errors,'warnings':warnings}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('spec',type=Path); ap.add_argument('--json',action='store_true'); args=ap.parse_args()
    try: data=json.loads(args.spec.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as exc: ap.error(str(exc))
    result=validate(data)
    if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for x in result['errors']: print('ERROR:',x)
        for x in result['warnings']: print('WARN:',x)
        print(f"summary: {len(result['errors'])} errors, {len(result['warnings'])} warnings")
    return 1 if result['errors'] else 0
if __name__=='__main__': raise SystemExit(main())
