#!/usr/bin/env python3
"""
ASI (Autonomous Sustainable Intelligence) Artifact Ranking Tool

Computes ASI scores for artifacts based on:
- CAV: Catalyze Additional Value
- CLI: Cluster Innovation  
- BAF: Boost Auto Finance

Only processes artifacts from official, affiliated repositories.
"""

import os
import sys
import glob
import json
import yaml
import argparse
import math
from collections import defaultdict
from datetime import datetime, timezone, timedelta

def load_yaml(path):
    """Load YAML file safely"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {}

def load_json(path):
    """Load JSON file safely"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {}

def utcnow():
    """Get current UTC timestamp"""
    return datetime.now(timezone.utc)

def get_nested(data, path, default=None):
    """Get nested dictionary value using dot notation"""
    current = data
    for key in path.split("."):
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def parse_timestamp(ts_str):
    """Parse ISO timestamp string"""
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except:
        return None

def within_days(timestamp, days):
    """Check if timestamp is within specified days from now"""
    if not timestamp:
        return False
    return (utcnow() - timestamp) <= timedelta(days=days)

def clamp(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))

def zscore(values, x):
    """Compute z-score with outlier clamping"""
    if len(values) < 2:
        return 0.0
    mu = sum(values) / len(values)
    variance = sum((v - mu) ** 2 for v in values) / len(values)
    std_dev = math.sqrt(variance) if variance > 0 else 1.0
    return clamp((x - mu) / std_dev, -3.0, 3.0)

def minmax01(values, x):
    """Normalize to 0-1 range"""
    if not values:
        return 0.0
    min_val, max_val = min(values), max(values)
    if max_val <= min_val:
        return 0.0
    return (x - min_val) / (max_val - min_val)

def inv_days_norm(days, half_life=30.0):
    """Inverse days normalization for velocity metrics"""
    return 1.0 / (1.0 + days / half_life)

def eligible_repo(packet, affiliates):
    """Check if packet comes from an eligible repository"""
    repo_field = affiliates["rules"]["repo_evidence_field"]
    repo_url = get_nested(packet, repo_field, "")
    
    if affiliates["rules"].get("require_repo_match", True):
        for org in affiliates.get("orgs", []):
            for repo in org.get("repos", []):
                if repo.get("url") and repo["url"] in str(repo_url):
                    return True
        return False
    
    if affiliates["rules"].get("require_signer_match", False):
        signer = get_nested(packet, "sig.by", "")
        allowed_signers = [s["id"] for s in affiliates.get("signers", [])]
        if signer not in allowed_signers:
            return False
    
    return True

def collect_packets(det_glob, lookback_days, affiliates):
    """Collect eligible DET packets"""
    packets = []
    
    for path in glob.glob(det_glob, recursive=True):
        try:
            packet = load_json(path)
            if not packet:
                continue
                
            # Validate signature and hash
            if get_nested(packet, "sig.alg") != "Ed25519":
                continue
            if len(get_nested(packet, "hash", "")) != 64:
                continue
            if not get_nested(packet, "outputs.units"):
                continue
                
            # Check timestamp
            timestamp = parse_timestamp(packet.get("ts", ""))
            if lookback_days and not within_days(timestamp, lookback_days):
                continue
                
            # Check repository eligibility
            if not eligible_repo(packet, affiliates):
                continue
                
            packets.append((path, packet))
            
        except Exception as e:
            print(f"Error processing {path}: {e}")
            continue
    
    return packets

def extract_domain(packet):
    """Extract domain code from DET ID"""
    det_id = packet.get("det_id", "")
    parts = det_id.split(":")
    return parts[2] if len(parts) >= 3 else "UNK"

def extract_pillar(packet):
    """Extract pillar from DET ID"""
    det_id = packet.get("det_id", "")
    parts = det_id.split(":")
    return parts[1] if len(parts) >= 2 else "UNK"

def extract_activity(packet):
    """Extract activity from DET ID"""
    det_id = packet.get("det_id", "")
    parts = det_id.split(":")
    return parts[4] if len(parts) >= 5 else "UNK"

def get_anchor_key(packet, primary_key="refs.ci", fallback_key="refs.ce"):
    """Get grouping anchor key"""
    anchor = get_nested(packet, primary_key)
    if not anchor:
        anchor = get_nested(packet, fallback_key, "UNK")
    return anchor

def compute_cav_metrics(groups):
    """Compute CAV (Catalyze Additional Value) metrics"""
    for anchor, group in groups.items():
        # CAV Reuse Multiplier
        reuse_events = [p for p in group["packets"] if extract_activity(p) in ["design", "save_model", "baseline_freeze"]]
        group["cav_reuse_multiplier"] = len(reuse_events) * len(group["downstream_refs"])
        
        # CAV Energy Efficiency  
        energy_outputs = []
        for packet in group["packets"]:
            energy_val = get_nested(packet, "outputs.metrics.energy_saved_kwh", 0.0)
            if energy_val > 0:
                energy_outputs.append(energy_val)
        group["cav_energy_efficiency"] = sum(energy_outputs) / max(1, len(group["packets"]))
        
        # CAV Spillover Effect
        group["cav_spillover_effect"] = len(group["domains_involved"]) * len(group["pillars_involved"])

def compute_cli_metrics(groups):
    """Compute CLI (Cluster Innovation) metrics"""
    for anchor, group in groups.items():
        # CLI Novelty Score
        novelty_activities = ["design", "feasibility_run", "trade_study"]
        novelty_count = len([p for p in group["packets"] if extract_activity(p) in novelty_activities])
        group["cli_novelty_score"] = min(1.0, novelty_count / 10.0)
        
        # CLI Coherence
        activity_diversity = len(set(extract_activity(p) for p in group["packets"]))
        domain_diversity = len(group["domains_involved"])
        group["cli_coherence"] = activity_diversity / max(1, domain_diversity)
        
        # CLI Emergence Rate
        if group["first_ts"] and group["last_ts"]:
            days_span = (group["last_ts"] - group["first_ts"]).total_seconds() / 86400.0
            group["cli_emergence_rate"] = inv_days_norm(days_span)
        else:
            group["cli_emergence_rate"] = 0.0

def compute_baf_metrics(groups):
    """Compute BAF (Boost Auto Finance) metrics"""
    for anchor, group in groups.items():
        # BAF ROI Projection
        co2_saved = sum(get_nested(p, "outputs.metrics.co2_saved_kg", 0.0) for p in group["packets"])
        energy_saved = sum(get_nested(p, "outputs.metrics.energy_saved_kwh", 0.0) for p in group["packets"])
        group["baf_roi_projection"] = (co2_saved * 0.1) + (energy_saved * 0.05)  # Simple ROI heuristic
        
        # BAF Sustainability Alignment
        sustainability_activities = ["baseline_freeze", "process_update", "wo_close", "life_extension"]
        sustain_count = len([p for p in group["packets"] if extract_activity(p) in sustainability_activities])
        group["baf_sustainability_alignment"] = min(1.0, sustain_count / 5.0)
        
        # BAF Risk Mitigation
        risk_outputs = []
        for packet in group["packets"]:
            risk_val = get_nested(packet, "outputs.metrics.delta_cvar", 0.0)
            if risk_val != 0:
                risk_outputs.append(abs(risk_val))  # Use absolute value
        group["baf_risk_mitigation"] = sum(risk_outputs) / max(1, len(risk_outputs))

def main():
    parser = argparse.ArgumentParser(description="Compute ASI scores for artifacts")
    parser.add_argument("--root", required=True, help="Root directory path")
    parser.add_argument("--config", required=True, help="ASI config file path")
    args = parser.parse_args()

    # Load configuration
    config = load_yaml(args.config)
    if not config:
        print("Failed to load ASI configuration")
        return 1

    # Load affiliates
    affiliates_ref = config["eligibility"]["affiliates_ref"]
    if affiliates_ref.startswith("UTCS-BLOCKCHAIN/"):
        # Remove the UTCS-BLOCKCHAIN prefix if root already includes it
        affiliates_path = os.path.join(args.root, affiliates_ref[len("UTCS-BLOCKCHAIN/"):])
    else:
        affiliates_path = os.path.join(args.root, affiliates_ref)
    affiliates = load_yaml(affiliates_path)
    if not affiliates:
        print("Failed to load affiliates configuration")
        return 1

    # Collect packets
    det_glob_pattern = config["eligibility"]["det_glob"]
    if det_glob_pattern.startswith("UTCS-BLOCKCHAIN/"):
        # Remove the UTCS-BLOCKCHAIN prefix if root already includes it
        det_glob = os.path.join(args.root, det_glob_pattern[len("UTCS-BLOCKCHAIN/"):])
    else:
        det_glob = os.path.join(args.root, det_glob_pattern)
    lookback_days = config["windows"]["lookback_days"]
    packets = collect_packets(det_glob, lookback_days, affiliates)
    
    print(f"Collected {len(packets)} eligible packets")

    # Group by anchor
    groups = defaultdict(lambda: {
        "domain": None,
        "det_ids": [],
        "packets": [],
        "repo": None,
        "first_ts": None,
        "last_ts": None,
        "domains_involved": set(),
        "pillars_involved": set(),
        "downstream_refs": set(),
        "raw_metrics": {}
    })

    for path, packet in packets:
        anchor = get_anchor_key(packet, 
                               config["grouping"]["artifact_key"], 
                               "refs.ce")
        if anchor == "UNK":
            continue
            
        group = groups[anchor]
        group["domain"] = group["domain"] or extract_domain(packet)
        group["det_ids"].append(packet["det_id"])
        group["packets"].append(packet)
        group["repo"] = group["repo"] or get_nested(packet, affiliates["rules"]["repo_evidence_field"], "")
        
        # Track timestamps
        ts = parse_timestamp(packet.get("ts"))
        if ts:
            group["first_ts"] = ts if not group["first_ts"] or ts < group["first_ts"] else group["first_ts"]
            group["last_ts"] = ts if not group["last_ts"] or ts > group["last_ts"] else group["last_ts"]
        
        # Track diversity
        group["domains_involved"].add(extract_domain(packet))
        group["pillars_involved"].add(extract_pillar(packet))
        
        # Track downstream references
        refs_ce = get_nested(packet, "refs.ce")
        if refs_ce:
            group["downstream_refs"].add(refs_ce)

    # Compute metrics
    compute_cav_metrics(groups)
    compute_cli_metrics(groups)
    compute_baf_metrics(groups)

    # Prepare for normalization
    all_metrics = defaultdict(list)
    
    for anchor, group in groups.items():
        for metric in ["cav_reuse_multiplier", "cav_energy_efficiency", "cav_spillover_effect",
                      "cli_novelty_score", "cli_coherence", "cli_emergence_rate",
                      "baf_roi_projection", "baf_sustainability_alignment", "baf_risk_mitigation"]:
            value = group.get(metric, 0.0)
            all_metrics[metric].append(value)

    # Compute scores
    leaderboard = []
    for anchor, group in groups.items():
        metrics_normalized = {}
        composite_score = 0.0
        
        for metric_name in config["metrics"]:
            raw_value = group.get(metric_name, 0.0)
            weight = config["metrics"][metric_name]["weight"]
            norm_method = config["metrics"][metric_name]["normalize"]
            
            # Apply normalization
            if norm_method == "zscore":
                normalized = zscore(all_metrics[metric_name], raw_value)
            elif norm_method == "minmax01":
                normalized = minmax01(all_metrics[metric_name], raw_value)
            elif norm_method == "domain_norm":
                # Simplified: use zscore for now
                normalized = zscore(all_metrics[metric_name], raw_value)
            elif norm_method == "inv_days_norm":
                normalized = raw_value  # Already normalized
            else:
                normalized = raw_value
            
            metrics_normalized[metric_name] = normalized
            composite_score += weight * normalized
        
        entry = {
            "anchor": anchor,
            "domain": group["domain"] or "UNK",
            "composite": composite_score,
            "metrics": metrics_normalized,
            "provenance": {
                "repo": group["repo"],
                "signer": "",
                "det_ids": group["det_ids"][:50]  # Cap at 50
            },
            "timestamp": utcnow().isoformat()
        }
        
        leaderboard.append(entry)

    # Sort by composite score
    leaderboard.sort(key=lambda x: x["composite"], reverse=True)

    # Create output directory
    output_dir_pattern = config["outputs"]["out_dir"]
    if output_dir_pattern.startswith("UTCS-BLOCKCHAIN/"):
        # Remove the UTCS-BLOCKCHAIN prefix if root already includes it
        output_dir = os.path.join(args.root, output_dir_pattern[len("UTCS-BLOCKCHAIN/"):])
    else:
        output_dir = os.path.join(args.root, output_dir_pattern)
    os.makedirs(output_dir, exist_ok=True)

    # Write JSON leaderboard
    json_path = os.path.join(output_dir, "leaderboard-global.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, indent=2)

    # Write Markdown leaderboard
    md_lines = []
    md_lines.append("# ASI Artifact Leaderboard — Global\n")
    md_lines.append("| # | Anchor | Domain | Score | CAV-Reuse | CAV-Energy | CLI-Novelty | BAF-Sustain |")
    md_lines.append("|---:|:------|:------:|------:|----------:|-----------:|------------:|------------:|")
    
    for i, entry in enumerate(leaderboard[:50], 1):
        m = entry["metrics"]
        md_lines.append(
            f"| {i} | `{entry['anchor']}` | {entry['domain']} | {entry['composite']:.3f} | "
            f"{m.get('cav_reuse_multiplier', 0):.2f} | {m.get('cav_energy_efficiency', 0):.2f} | "
            f"{m.get('cli_novelty_score', 0):.2f} | {m.get('baf_sustainability_alignment', 0):.2f} |"
        )
    
    md_path = os.path.join(output_dir, "leaderboard-global.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"✅ ASI scores computed for {len(leaderboard)} artifacts")
    print(f"📊 Output written to {output_dir}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())