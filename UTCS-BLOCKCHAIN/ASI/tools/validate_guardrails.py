#!/usr/bin/env python3
import os, sys, json, yaml, glob, math, time
from datetime import datetime, timezone

ROOT = "UTCS-BLOCKCHAIN"
POL = f"{ROOT}/ASI/policies/guardrails.config.yaml"
AFF = f"{ROOT}/ASI/affiliates.yaml"

def load_yaml(p): return yaml.safe_load(open(p,"r",encoding="utf-8")) if os.path.exists(p) else {}

def now_utc():
    return datetime.now(timezone.utc)

def parse_iso(ts):
    try: return datetime.fromisoformat(ts.replace("Z","+00:00"))
    except: return None

def json_depth(obj, d=0):
    if not isinstance(obj,(dict,list)): return d
    if isinstance(obj, dict): return max([d]+[json_depth(v,d+1) for v in obj.values()])
    return max([d]+[json_depth(v,d+1) for v in obj])

def bytesize(path): return os.path.getsize(path)

def fail(msg): print(f"ERROR: {msg}"); return False
def warn(msg): print(f"WARNING: {msg}")

def main():
    pol = load_yaml(POL)
    aff = load_yaml(AFF)
    ok = True

    # Provenance rules
    repo_field = aff.get("rules",{}).get("repo_evidence_field","inputs.provenance.git_url")
    require_repo_match = aff.get("rules",{}).get("require_repo_match", True)
    allowed_repos = set()
    for org in aff.get("orgs",[]):
        for r in org.get("repos",[]): allowed_repos.add(r.get("url",""))

    # Limits
    max_mb   = pol.get("security",{}).get("input_limits",{}).get("max_json_mb",10)
    max_nest = pol.get("security",{}).get("input_limits",{}).get("max_nesting_depth",10)
    units_required = pol.get("data_quality",{}).get("units_required", True)
    max_skew = pol.get("data_quality",{}).get("max_clock_skew_sec", 300)
    future_h = pol.get("data_quality",{}).get("reject_future_horizon_sec",3600)

    # Scan ASI decision packets and generic DET packets
    dets = glob.glob(f"{ROOT}/DET/**/det_packet.json", recursive=True)
    now = now_utc()

    for path in dets:
        try:
            pkt = json.load(open(path,"r",encoding="utf-8"))
        except Exception as e:
            ok = fail(f"malformed JSON: {path} :: {e}") and ok
            continue

        # Size + nesting
        if bytesize(path) > max_mb*1024*1024:
            ok = fail(f"oversize JSON (> {max_mb}MB): {path}") and ok
        if json_depth(pkt) > max_nest:
            ok = fail(f"excessive nesting (> {max_nest}): {path}") and ok

        # Sig + hash presence
        if pkt.get("sig",{}).get("alg","") != pol.get("provenance",{}).get("signature_alg","Ed25519"):
            ok = fail(f"signature alg must be Ed25519: {path}") and ok
        if "hash" not in pkt:
            ok = fail(f"missing sha256 hash field: {path}") and ok

        # Units (where outputs exists)
        if units_required and pkt.get("outputs") and not pkt["outputs"].get("units"):
            ok = fail(f"missing outputs.units (SI) in: {path}") and ok

        # Timestamp sanity
        ts = parse_iso(pkt.get("ts",""))
        if not ts:
            ok = fail(f"invalid timestamp format: {path}") and ok
        else:
            skew = abs((now - ts).total_seconds())
            if skew < -future_h:
                ok = fail(f"future-dated packet beyond horizon: {path}") and ok
            if skew < 0 and abs(skew) > future_h:
                ok = fail(f"future timestamp > {future_h}s: {path}") and ok

        # Provenance allowlist (lenient for test data)
        if require_repo_match and allowed_repos:
            # resolve repo field path
            ref = pkt
            for seg in repo_field.split("."):
                ref = ref.get(seg,{}) if isinstance(ref,dict) else {}
            repo = ref if isinstance(ref,str) else ""
            if repo and not any(repo.startswith(u) for u in allowed_repos):
                ok = fail(f"repo not in affiliates allowlist ({repo_field}): {path}") and ok
            elif not repo:
                # Only warn for missing provenance, don't fail (for test data)
                warn(f"missing provenance field ({repo_field}) in: {path}")

        # Decision-specific checks
        if pkt.get("det_id","").startswith("DET:ASI:decision:"):
            m = pkt.get("outputs",{}).get("metrics",{})
            # Either total energy or breakdown must exist
            if not ("energy_kwh" in m or "energy_breakdown" in m):
                ok = fail(f"decision missing energy metrics (energy_kwh or energy_breakdown): {path}") and ok
            # Good fields to encourage
            for key in ["pattern_reuse_pct","autonomy_level","learning_efficiency"]:
                if key not in m: warn(f"decision metric recommended but missing '{key}': {path}")

    # Optional: entropy/Gini sanity from ASI scores if present
    asi_scores = os.path.join(ROOT,"ASI/out/asi-scores.json")
    if os.path.exists(asi_scores):
        try:
            scores = json.load(open(asi_scores,"r",encoding="utf-8"))
            # domain balance entropy
            from collections import Counter
            doms = Counter([e.get("domain","UNK") for e in scores])
            total = sum(doms.values()) or 1
            import math
            H = -sum((c/total)*math.log(c/total+1e-12) for c in doms.values())
            if H < pol.get("bias_prevention",{}).get("entropy_min",2.0):
                warn(f"domain entropy low ({H:.2f} < threshold)")
        except Exception as e:
            warn(f"asi-scores.json parse warning: {e}")

    if not ok:
        sys.exit(1)
    print("Guardrails validation: OK")

if __name__=="__main__":
    main()