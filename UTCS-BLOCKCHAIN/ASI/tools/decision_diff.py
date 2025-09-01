#!/usr/bin/env python3
import json, sys
new = json.load(open(sys.argv[1]))
old = json.load(open(sys.argv[2]))
n = new["outputs"]["metrics"]; o = old["outputs"]["metrics"]
diff = {
  "boiloff_improvement": n.get("expected_boiloff_pct_day",0) - o.get("expected_boiloff_pct_day",0),
  "compute_savings_kwh": o.get("energy_kwh",0) - n.get("energy_kwh",0),
  "pattern_reuse_delta": n.get("pattern_reuse_pct",0) - o.get("pattern_reuse_pct",0),
  "violations_delta": n.get("constraint_violations",0) - o.get("constraint_violations",0)
}
comment = f"""
🤖 **ASI Decision Analysis** — `{new.get('det_id','')}`

**Performance**
- Boil-off: {diff['boiloff_improvement']:+.3f} %/day
- Compute: {diff['compute_savings_kwh']:+.3f} kWh saved
- Pattern reuse: {diff['pattern_reuse_delta']:+.1f} %
- Constraint violations: {diff['violations_delta']:+d}

Sustainability: {"✅" if diff['compute_savings_kwh']>0 else "⚠️"}  
Safety: {"✅" if n.get('constraint_violations',0)<=o.get('constraint_violations',0) else "❌"}
"""
print(comment.strip())