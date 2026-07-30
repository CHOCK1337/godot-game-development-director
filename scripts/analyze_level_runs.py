#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,statistics
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any

def _bool(v:str)->bool: return str(v).strip().lower() in {'1','true','yes','y','completed'}

def analyze(path:Path)->dict[str,Any]:
    with path.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    if not rows: return {'total_runs':0,'completion_rate':0.0,'unique_path_count':0,'path_diversity_ratio':0.0,'death_hotspots':[],'seed_outliers':[]}
    completed=[_bool(r.get('completed','')) for r in rows]
    durations=[float(r.get('duration_s') or 0) for r in rows]
    deaths=[int(float(r.get('deaths') or 0)) for r in rows]
    paths=[r.get('path_signature','').strip() for r in rows if r.get('path_signature','').strip()]
    room_counts=Counter()
    for r in rows:
        room=r.get('death_room','').strip(); count=int(float(r.get('deaths') or 0))
        if room and count>0: room_counts[room]+=count
    by_seed=defaultdict(list)
    for r,c,d in zip(rows,completed,deaths): by_seed[str(r.get('seed','unknown'))].append((c,d))
    global_rate=sum(completed)/len(completed); global_deaths=sum(deaths)/len(deaths)
    outliers=[]
    seed_stats={}
    for seed,vals in by_seed.items():
        rate=sum(1 for c,_ in vals if c)/len(vals); mean_d=sum(d for _,d in vals)/len(vals)
        seed_stats[seed]={'runs':len(vals),'completion_rate':round(rate,4),'mean_deaths':round(mean_d,3)}
        if len(vals)>=2 and (abs(rate-global_rate)>=0.40 or mean_d>=global_deaths+2): outliers.append(seed)
    total_deaths=sum(room_counts.values())
    hotspots=[{'room':room,'deaths':count,'share':round(count/total_deaths,4) if total_deaths else 0.0} for room,count in room_counts.most_common()]
    return {
        'total_runs':len(rows),'completion_rate':round(global_rate,4),
        'median_duration_s':round(statistics.median(durations),3),'mean_deaths':round(global_deaths,3),
        'unique_path_count':len(set(paths)),'path_diversity_ratio':round(len(set(paths))/len(paths),4) if paths else 0.0,
        'death_hotspots':hotspots,'seed_outliers':sorted(outliers),'seed_stats':seed_stats
    }

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('csv',type=Path); ap.add_argument('--pretty',action='store_true'); args=ap.parse_args()
    try: result=analyze(args.csv)
    except (OSError,ValueError) as exc: ap.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2 if args.pretty else None)); return 0
if __name__=='__main__': raise SystemExit(main())
