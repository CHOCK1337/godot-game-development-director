#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,importlib.util
from pathlib import Path
from typing import Any
HERE=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location('random_audit',HERE/'audit_random_table.py')
_audit=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_audit)

def validate(spec:dict[str,Any])->dict[str,list[str]]:
    errors=[]; warnings=[]
    required=('generator_id','content_type','seed_policy','representation','hard_invariants','generation_pipeline','validation','repair_policy','expressive_range_metrics','fallbacks')
    for key in required:
        if key not in spec: errors.append(f'missing required field: {key}')
    seed=spec.get('seed_policy',{})
    if not isinstance(seed,dict): errors.append('seed_policy must be object')
    else:
        if not seed.get('deterministic'): warnings.append('generator is not deterministic; bad seeds will be difficult to reproduce')
        if not seed.get('record_seed'): errors.append('seed_policy must record seed')
    invariants=spec.get('hard_invariants',[])
    inv_ids=[]
    if not isinstance(invariants,list) or not invariants: errors.append('hard_invariants must be non-empty')
    else:
        for i,inv in enumerate(invariants):
            iid=str(inv.get('id','')).strip() if isinstance(inv,dict) else ''
            if not iid: errors.append(f'hard_invariants[{i}] missing id')
            inv_ids.append(iid)
    validation=spec.get('validation',{})
    checks=set(map(str,validation.get('checks',[]))) if isinstance(validation,dict) else set()
    for iid in inv_ids:
        if iid and iid not in checks: errors.append(f'hard invariant not covered by validation: {iid}')
    try:
        attempts=int(validation.get('max_attempts',0))
        if attempts<=0: errors.append('validation max_attempts must be positive and bounded')
        elif attempts>1000: warnings.append('validation max_attempts is very high; loading stall risk')
    except (TypeError,ValueError,AttributeError): errors.append('validation max_attempts must be integer')
    pipeline=[str(x).lower() for x in spec.get('generation_pipeline',[]) if str(x).strip()]
    if not any('validate' in x for x in pipeline): errors.append('generation_pipeline has no validate phase')
    if not spec.get('repair_policy'): errors.append('repair_policy must be non-empty')
    if not spec.get('fallbacks'): errors.append('fallbacks must be non-empty')
    metrics=spec.get('expressive_range_metrics',[])
    if not isinstance(metrics,list) or len(metrics)<2: warnings.append('fewer than two expressive-range metrics limits generator evaluation')
    for table in spec.get('random_tables',[]) if isinstance(spec.get('random_tables',[]),list) else []:
        result=_audit.audit(table)
        errors.extend(f"random table {table.get('id','?')}: {x}" for x in result['errors'])
        warnings.extend(f"random table {table.get('id','?')}: {x}" for x in result['warnings'])
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
