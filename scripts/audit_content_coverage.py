#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path

def audit(path: Path) -> dict:
    with path.open(encoding="utf-8", newline="") as handle:
        rows=list(csv.DictReader(handle))
    ids=[r.get("content_id","").strip() for r in rows]
    duplicates=sorted(k for k,v in Counter(ids).items() if k and v>1)
    missing_owner=[x for x,r in zip(ids,rows) if not r.get("owner","").strip()]
    untested=[x for x,r in zip(ids,rows) if r.get("test_status","").strip().lower() not in {"pass","passed","done"}]
    blocked=[x for x,r in zip(ids,rows) if r.get("status","").strip().lower()=="blocked"]
    return {"rows":len(rows),"duplicate_ids":duplicates,"missing_owner":missing_owner,"untested":untested,"blocked":blocked,"complete":not any([duplicates,missing_owner,untested,blocked])}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("csv",type=Path); ap.add_argument("--pretty",action="store_true")
    a=ap.parse_args(); result=audit(a.csv); print(json.dumps(result,ensure_ascii=False,indent=2 if a.pretty else None)); return 0 if result["complete"] else 1
if __name__=="__main__": raise SystemExit(main())
