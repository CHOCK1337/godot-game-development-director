#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any

def validate(model:dict[str,Any])->dict[str,list[str]]:
    errors=[]; warnings=[]
    required=('target_experience','skill_bands','challenge_dimensions','metrics','tuning_parameters','difficulty_curve','adaptation_policy','playtest_hypotheses')
    for key in required:
        if key not in model: errors.append(f'missing required field: {key}')
    bands=model.get('skill_bands',[])
    if not isinstance(bands,list) or not bands: errors.append('skill_bands must be non-empty')
    elif len(bands)!=len(set(map(str,bands))): errors.append('skill_bands contains duplicates')
    metrics=model.get('metrics',[])
    if not isinstance(metrics,list) or not metrics: errors.append('metrics must be non-empty')
    else:
        for i,m in enumerate(metrics):
            if not isinstance(m,dict): errors.append(f'metrics[{i}] must be object'); continue
            try:
                lo=float(m['target_min']); hi=float(m['target_max'])
                if lo>hi: errors.append(f"metric {m.get('id',i)} target_min exceeds target_max")
            except (KeyError,TypeError,ValueError): errors.append(f"metric {m.get('id',i)} missing numeric target range")
            if not str(m.get('segment','')).strip(): errors.append(f"metric {m.get('id',i)} missing segment")
    params=model.get('tuning_parameters',[])
    if not isinstance(params,list) or not params: errors.append('tuning_parameters must be non-empty')
    else:
        seen=set()
        for i,p in enumerate(params):
            if not isinstance(p,dict): errors.append(f'tuning_parameters[{i}] must be object'); continue
            pid=str(p.get('id','')).strip()
            if not pid: errors.append(f'tuning_parameters[{i}] missing id')
            if pid in seen: errors.append(f'duplicate tuning parameter: {pid}')
            seen.add(pid)
            try:
                lo=float(p['min']); hi=float(p['max']); default=float(p['default']); step=float(p['step'])
                if lo>hi: errors.append(f'parameter {pid or i} min exceeds max')
                if not lo<=default<=hi: errors.append(f'parameter {pid or i} default outside bounds')
                if step<=0: errors.append(f'parameter {pid or i} step must be positive')
            except (KeyError,TypeError,ValueError): errors.append(f'parameter {pid or i} has invalid numeric bounds')
    policy=model.get('adaptation_policy',{})
    if not isinstance(policy,dict): errors.append('adaptation_policy must be object')
    elif policy.get('enabled'):
        for k in ('signals','allowed_adjustments','cooldown_s','max_step','player_respect'):
            if k not in policy or policy[k] in ('',[],None): errors.append(f'adaptation_policy missing {k}')
        try:
            if float(policy.get('cooldown_s',0))<=0: errors.append('adaptation_policy cooldown_s must be positive')
        except (TypeError,ValueError): errors.append('adaptation_policy cooldown_s must be numeric')
        forbidden={'hidden_player_damage','hidden_hitbox','enemy_telegraph_speed'}
        if forbidden & set(map(str,policy.get('allowed_adjustments',[]))): warnings.append('adaptation policy changes learned combat facts; player trust risk')
    curve=model.get('difficulty_curve',[])
    if not isinstance(curve,list) or len(curve)<2: errors.append('difficulty_curve needs at least 2 stages')
    hypotheses=model.get('playtest_hypotheses',[])
    if not isinstance(hypotheses,list) or not hypotheses: errors.append('playtest_hypotheses must be non-empty')
    return {'errors':errors,'warnings':warnings}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('model',type=Path); ap.add_argument('--json',action='store_true'); args=ap.parse_args()
    try: data=json.loads(args.model.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as exc: ap.error(str(exc))
    result=validate(data)
    if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        for x in result['errors']: print('ERROR:',x)
        for x in result['warnings']: print('WARN:',x)
        print(f"summary: {len(result['errors'])} errors, {len(result['warnings'])} warnings")
    return 1 if result['errors'] else 0
if __name__=='__main__': raise SystemExit(main())
