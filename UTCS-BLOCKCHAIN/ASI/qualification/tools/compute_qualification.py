#!/usr/bin/env python3
import os, sys, json, yaml, glob, math
from datetime import datetime, timezone, timedelta
from collections import defaultdict

def load_yaml(p): 
    try:
        return yaml.safe_load(open(p,"r",encoding="utf-8"))
    except Exception as e:
        print(f"Error loading {p}: {e}")
        return {}

def load_json(p):
    try:
        return json.load(open(p,"r",encoding="utf-8"))
    except Exception as e:
        print(f"Error loading {p}: {e}")
        return {}

def now_iso(): 
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def get(d, path, default=None):
    cur=d
    for seg in path.split("."):
        if isinstance(cur, dict) and seg in cur: cur=cur[seg]
        else: return default
    return cur

def percentile(values, x):
    if not values: return 0.0
    s = sorted(values)
    lo = sum(v < x for v in s)
    eq = sum(v == x for v in s)
    return 100.0 * (lo + 0.5*eq) / len(s)

def eligibility_ok(pkt, cfg, affiliates, cutoff_dt):
    if cfg["eligibility"]["require_ed25519_signature"] and get(pkt,"sig.alg")!="Ed25519":
        return False
    if cfg["eligibility"]["require_si_units_in_outputs"] and not get(pkt,"outputs.units"):
        return False
    if cfg["eligibility"]["require_affiliated_repo"]:
        repo_field = get(affiliates,"rules.repo_evidence_field","inputs.provenance.git_url")
        repo = get(pkt, repo_field, "")
        ok=False
        for org in affiliates.get("orgs",[]):
            for rep in org.get("repos",[]):
                if rep.get("url") and rep["url"] in str(repo):
                    ok=True; break
            if ok: break
        if not ok: return False
    ts = pkt.get("ts","")
    try: dt = datetime.fromisoformat(ts.replace("Z","+00:00"))
    except: dt=None
    if dt and dt < cutoff_dt: return False
    return True

def main():
    root = "."
    cfg = load_yaml(os.path.join("UTCS-BLOCKCHAIN/ASI/qualification/qualification-config.yaml"))
    
    # Handle path references properly
    affiliates_ref = cfg["inputs"]["affiliates_ref"]
    if affiliates_ref.startswith("UTCS-BLOCKCHAIN/"):
        affiliates_path = affiliates_ref
    else:
        affiliates_path = os.path.join("UTCS-BLOCKCHAIN", affiliates_ref)
    affiliates = load_yaml(affiliates_path)

    # Load ASI scores (artifact-level)
    asi_path = cfg["inputs"]["asi_scores_json"]
    if not os.path.exists(asi_path):
        print("ASI scores not found:", asi_path)
        print("Creating empty leaderboards...")
        asi = []
    else:
        asi = load_json(asi_path)

    # Composite list for percentiles (cert-agnostic)
    composites = [ float(e.get(cfg["scoring"]["field"], 0.0)) for e in asi ]
    
    # Sustainability floors are checked via DET references (optional quick guard)
    det_packets = []
    cutoff_dt = datetime.now(timezone.utc) - timedelta(days=int(cfg["eligibility"]["lookback_days"]))
    
    # Handle DET glob path properly
    det_glob = cfg["inputs"]["det_glob"]
    if not det_glob.startswith("/"):
        det_glob = os.path.join(".", det_glob)
    
    for p in glob.glob(det_glob, recursive=True):
        try: pkt = load_json(p)
        except: continue
        if eligibility_ok(pkt, cfg, affiliates, cutoff_dt): det_packets.append(pkt)

    # Index DET packets per anchor and contributor
    per_anchor = defaultdict(list)
    contrib_map = defaultdict(set)
    for pkt in det_packets:
        anc = get(pkt,"refs.ci", get(pkt,"refs.ce",""))
        if not anc: continue
        per_anchor[anc].append(pkt)
        for field in cfg["grouping"]["contributor_fields"]:
            cid = str(get(pkt, field, "")).strip()
            if cid:
                contrib_map[cid].add(anc)

    # Sustainability floors
    floors = cfg["floors"]
    def artifact_meets_floors(anchor):
        # Thin check: if any strong negative appears, block unless risk reduction > allow_if_risk_reduction_gt
        rr = 0.0; co2=0.0; en=0.0; reuse=0.0
        for pkt in per_anchor.get(anchor, []):
            mets = pkt.get("outputs",{}).get("metrics",{})
            rr += float(mets.get("delta_cvar",0.0))
            co2 = max(co2, float(mets.get("co2_saved_kg",0.0)))
            en  = max(en,  float(mets.get("energy_saved_kwh",0.0)))
            reuse = max(reuse, float(mets.get("reuse_percent",0.0)))
        if (co2 < floors["co2_saved_kg_min"] or
            en  < floors["energy_saved_kwh_min"] or
            reuse < floors["reuse_percent_min"]) and rr <= floors["allow_if_risk_reduction_gt"]:
            return False
        return True

    # Map percentiles → classes
    class_cfg_art = cfg["classes"]["artifact"]
    ordered_art = sorted(
        ((e.get("anchor"), e) for e in asi),
        key=lambda t: float(t[1].get(cfg["scoring"]["field"], 0.0)),
        reverse=True
    )

    def class_for_percentile(pct, table):
        for name, rule in table.items():
            if pct >= float(rule["percentile_min"]): return name
        return "Q1-Seed"

    # Artifact qualification
    artifacts_out=[]
    for anchor, e in ordered_art:
        if not artifact_meets_floors(anchor):
            q="Q1-Seed"
        else:
            comp = float(e.get(cfg["scoring"]["field"],0.0))
            pct = percentile(composites, comp)
            q = class_for_percentile(pct, class_cfg_art)
        
        # Extract domain and pillar from anchor or DET ID
        domain = e.get("domain", "UNK")
        pillar = "UNK"
        sns = ""
        # Try to extract from anchor format (CI-CAD-AAA-53-10-CB-001)
        if "-" in anchor:
            parts = anchor.split("-")
            if len(parts) >= 3:
                pillar = parts[1] if parts[1] in ["CAD","CAE","CAM","CAT","CAI","CAS","CAO"] else "UNK"
                domain = parts[2] if len(parts[2]) == 3 else domain
                if len(parts) >= 5:
                    sns = f"{parts[3]}-{parts[4]}"
        
        artifacts_out.append({
            "anchor": anchor,
            "domain": domain,
            "pillar": pillar,
            "sns": sns,
            "qualification": q,
            "percentile": percentile(composites, float(e.get(cfg["scoring"]["field"],0.0))),
            "composite": float(e.get(cfg["scoring"]["field"],0.0)),
            "display_score": float(e.get(cfg["scoring"]["display_field"], e.get(cfg["scoring"]["field"],0.0))),
            "provenance": e.get("provenance",{})
        })

    # Contributor qualification
    # Aggregate composite across their artifacts (mean), apply min_artifacts thresholds
    class_cfg_con = cfg["classes"]["contributor"]
    contrib_scores=[]
    for cid, anchors in contrib_map.items():
        if len(anchors) < cfg["grouping"]["min_packets_per_contributor"]:
            continue
        comps=[]
        for anc in anchors:
            a = next((x for x in artifacts_out if x["anchor"]==anc), None)
            if a: comps.append(a["composite"])
        if not comps: continue
        contrib_scores.append((cid, sum(comps)/len(comps), list(anchors)))

    contrib_comps = [s for _,s,_ in contrib_scores]
    contributors_out=[]
    for cid, score, anchors in sorted(contrib_scores, key=lambda x: x[1], reverse=True):
        pct = percentile(contrib_comps, score)
        # pick class respecting min_artifacts
        q="Q1-Seed"
        for name, rule in class_cfg_con.items():
            if pct >= float(rule["percentile_min"]) and len(anchors) >= int(rule["min_artifacts"]):
                q=name; break
        contributors_out.append({
            "contributor_id": cid or "unknown",
            "qualification": q,
            "percentile": pct,
            "composite": score,
            "artifacts": anchors[:50]
        })

    outdir = cfg["outputs"]["dir"]
    os.makedirs(outdir, exist_ok=True)
    
    # Write JSON outputs
    with open(os.path.join(outdir,cfg["outputs"]["artifact_file_json"]),"w",encoding="utf-8") as f:
        json.dump(artifacts_out, f, indent=2)
    with open(os.path.join(outdir,cfg["outputs"]["contributor_file_json"]),"w",encoding="utf-8") as f:
        json.dump(contributors_out, f, indent=2)

    # Markdown summaries
    def md_table_art():
        rows = ["# ASI Qualification — Artifacts",
                "",
                "| # | Anchor | Domain | Pillar | Class | Pctl | Composite |",
                "|---:|:------|:-----:|:-----:|:-----:|----:|---------:|"]
        for i,a in enumerate(sorted(artifacts_out, key=lambda x: x["composite"], reverse=True)[:50], start=1):
            rows.append(f"| {i} | `{a['anchor']}` | {a['domain']} | {a['pillar']} | {a['qualification']} | {a['percentile']:.1f}% | {a['composite']:.3f} |")
        return "\n".join(rows)

    def md_table_contrib():
        rows = ["# ASI Qualification — Contributors",
                "",
                "| # | Contributor | Class | Pctl | Composite | Artifacts |",
                "|---:|:-----------|:-----:|----:|---------:|:----------|"]
        for i,c in enumerate(sorted(contributors_out, key=lambda x: x["composite"], reverse=True)[:50], start=1):
            rows.append(f"| {i} | `{c['contributor_id']}` | {c['qualification']} | {c['percentile']:.1f}% | {c['composite']:.3f} | {len(c['artifacts'])} |")
        return "\n".join(rows)

    with open(os.path.join(outdir, cfg["outputs"]["artifact_file_md"]),"w",encoding="utf-8") as f:
        f.write(md_table_art()+"\n")
    with open(os.path.join(outdir, cfg["outputs"]["contributor_file_md"]),"w",encoding="utf-8") as f:
        f.write(md_table_contrib()+"\n")

    # Optional TekCred queue (SBT) — leave execution to DAO ops
    queue=[
      {"contributor_id": c["contributor_id"], "qualification": c["qualification"]}
      for c in contributors_out if c["qualification"].startswith("Q4") or c["qualification"].startswith("Q5")
    ]
    with open(os.path.join(outdir, cfg["outputs"]["tekcred_queue"]),"w",encoding="utf-8") as f:
        json.dump(queue, f, indent=2)

    # Emit minimal DET:ASI evidence stub (off-chain writer)
    if cfg.get("det_emit",{}).get("enable",False):
        detdir = cfg["det_emit"]["dir"]
        os.makedirs(detdir, exist_ok=True)
        det={
          "det_id": f"DET:ASI:qualification_publish:ASI-QUAL-{now_iso()}:V1",
          "ts": now_iso(),
          "refs": {"ce": ""},
          "inputs": {"asi_scores": cfg["inputs"]["asi_scores_json"]},
          "processing": {"tool": "compute_qualification@1.0", "params": {}},
          "outputs": {"units":"class","metrics":{"artifacts":len(artifacts_out),"contributors":len(contributors_out)}},
          "hash":"", "sig":{"alg":"Ed25519","by": cfg["det_emit"]["signer"]}
        }
        with open(os.path.join(detdir,"det_packet.json"),"w",encoding="utf-8") as f:
            json.dump(det, f, indent=2)

    print(f"✅ ASI qualification computed for {len(artifacts_out)} artifacts and {len(contributors_out)} contributors")
    print(f"📊 Output written to {outdir}")

if __name__=="__main__":
    main()