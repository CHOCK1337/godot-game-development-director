#!/usr/bin/env python3
"""Summarize event-log CSV. Describes behavior; does not infer fun or causality."""
from __future__ import annotations
import argparse,csv,json,statistics
from collections import Counter,defaultdict
from pathlib import Path

def analyze(path:Path)->dict:
    with path.open(newline='',encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    required={"session_id","timestamp","event_name"}
    if not rows: raise ValueError("CSV has no rows")
    missing=required-set(rows[0])
    if missing: raise ValueError(f"missing columns: {sorted(missing)}")
    sessions=defaultdict(list); counts=Counter()
    for r in rows:
        try: t=float(r["timestamp"])
        except ValueError: raise ValueError(f"invalid timestamp: {r['timestamp']}")
        sessions[r["session_id"]].append((t,r["event_name"],r.get("value","")))
        counts[r["event_name"]]+=1
    durations=[]; completed=0; failed=0; retries=0; music_changes=0
    for events in sessions.values():
        events.sort(); durations.append(max(0.0,events[-1][0]-events[0][0]))
        names=[e[1] for e in events]
        completed += int("session.completed" in names)
        failed += names.count("player.failed")
        retries += names.count("player.retry")
        music_changes += names.count("music.state.changed")
    total_minutes=max(sum(durations)/60.0,1e-9)
    return {
        "sessions":len(sessions),"rows":len(rows),
        "completion_rate":completed/len(sessions),
        "median_session_seconds":statistics.median(durations),
        "failures":failed,"retries":retries,
        "music_state_changes_per_minute":music_changes/total_minutes,
        "top_events":counts.most_common(10),
        "caveat":"These metrics describe logged behavior and do not establish enjoyment or causality."
    }

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("csv",type=Path); ap.add_argument("--pretty",action="store_true"); ap.add_argument("--output",type=Path); args=ap.parse_args()
    try: result=analyze(args.csv)
    except (OSError,ValueError) as exc: ap.error(str(exc))
    text=json.dumps(result,ensure_ascii=False,indent=2 if args.pretty else None)
    if args.output: args.output.write_text(text+'\n',encoding='utf-8')
    else: print(text)
    return 0
if __name__=="__main__": raise SystemExit(main())
