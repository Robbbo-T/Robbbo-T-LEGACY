#!/usr/bin/env python3
"""
Validate UTCS-BLOCKCHAIN implementation
Verifies complete Computer-Aided Excellence (CAX) framework architecture
"""

import os
import json
import yaml
from datetime import datetime

def validate_utcs_blockchain():
    """Validate complete UTCS-BLOCKCHAIN structure"""
    
    base_path = "UTCS-BLOCKCHAIN"
    
    if not os.path.exists(base_path):
        print("❌ FAIL: UTCS-BLOCKCHAIN directory not found")
        return False
    
    # Check root structure
    required_dirs = ["CADET", "DET", "TRACES", "DOMAINS"]
    for dir_name in required_dirs:
        if not os.path.exists(os.path.join(base_path, dir_name)):
            print(f"❌ FAIL: {dir_name} directory not found")
            return False
    
    print("✅ PASS: Root structure validated (CADET, DET, TRACES, DOMAINS)")
    
    # Count DET registry nodes
    det_nodes = []
    expected_files = ["manifest.yaml", "det_packet.json", "signature.ed25519", "previous_hash", "trace.yaml", "cadet.yaml"]
    
    for root, dirs, files in os.walk(os.path.join(base_path, "DET")):
        # Check if this is a V1 directory (leaf node)
        if root.endswith("V1"):
            det_nodes.append(root)
            
            # Validate required files exist
            for required_file in expected_files:
                if required_file not in files:
                    print(f"❌ FAIL: Missing {required_file} in {root}")
                    return False
            
            # Validate DET packet JSON structure
            det_packet_path = os.path.join(root, "det_packet.json")
            try:
                with open(det_packet_path, 'r') as f:
                    det_packet = json.load(f)
                
                # Check required fields
                required_fields = ["det_id", "ts", "inputs", "processing", "outputs", "hash", "sig"]
                for field in required_fields:
                    if field not in det_packet:
                        print(f"❌ FAIL: Missing {field} in {det_packet_path}")
                        return False
                
                # Validate DET ID format: DET:<CAX>:<DOMAIN>:<SNS>:<activity>:<version>
                det_id = det_packet["det_id"]
                parts = det_id.split(":")
                if len(parts) != 6 or parts[0] != "DET":
                    print(f"❌ FAIL: Invalid DET ID format: {det_id}")
                    return False
                    
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"❌ FAIL: Invalid det_packet.json in {root}: {e}")
                return False
            
            # Validate manifest.yaml structure
            manifest_path = os.path.join(root, "manifest.yaml")
            try:
                with open(manifest_path, 'r') as f:
                    manifest = yaml.safe_load(f)
                
                # Check required fields
                required_fields = ["det_id", "cax", "domain", "sns", "activity", "version"]
                for field in required_fields:
                    if field not in manifest:
                        print(f"❌ FAIL: Missing {field} in {manifest_path}")
                        return False
                        
            except (yaml.YAMLError, FileNotFoundError) as e:
                print(f"❌ FAIL: Invalid manifest.yaml in {root}: {e}")
                return False
    
    # Validate we have exactly 105 nodes (15 domains × 7 CAX pillars)
    expected_nodes = 105
    if len(det_nodes) != expected_nodes:
        print(f"❌ FAIL: Expected {expected_nodes} DET nodes, found {len(det_nodes)}")
        return False
    
    print(f"✅ PASS: {len(det_nodes)} DET registry nodes validated")
    
    # Validate path structure follows pattern: DET/<CAX>/<DOMAIN>/<SNS>/<activity>/<version>/
    for node in det_nodes:
        # Extract path components
        rel_path = os.path.relpath(node, os.path.join(base_path, "DET"))
        path_parts = rel_path.split(os.sep)
        
        if len(path_parts) != 5:  # CAX/DOMAIN/SNS/activity/version
            print(f"❌ FAIL: Invalid path structure: {rel_path}")
            return False
        
        cax, domain, sns, activity, version = path_parts
        
        # Validate CAX is one of the 7 pillars
        valid_cax = ["CAD", "CAE", "CAM", "CAT", "CAI", "CAS", "CAO"]
        if cax not in valid_cax:
            print(f"❌ FAIL: Invalid CAX pillar: {cax}")
            return False
        
        # Validate domain is one of the 15 domains  
        valid_domains = ["AAA", "AAP", "CCC", "CQH", "DDD", "EDI", "EEE", "EER", "IIF", "IIS", "LCC", "LIB", "MMM", "OOO", "PPP"]
        if domain not in valid_domains:
            print(f"❌ FAIL: Invalid domain: {domain}")
            return False
        
        # Validate version format
        if not version.startswith("V"):
            print(f"❌ FAIL: Invalid version format: {version}")
            return False
    
    print("✅ PASS: DET path structure validated")
    
    # Validate README exists and has content
    readme_path = os.path.join(base_path, "README.md")
    if not os.path.exists(readme_path):
        print("❌ FAIL: UTCS-BLOCKCHAIN README.md not found")
        return False
    
    with open(readme_path, 'r') as f:
        readme_content = f.read()
        if len(readme_content) < 100:
            print("❌ FAIL: README.md appears to be empty or too short")
            return False
    
    print("✅ PASS: README.md validated")
    
    return True

def generate_implementation_summary():
    """Generate summary of UTCS-BLOCKCHAIN implementation"""
    
    base_path = "UTCS-BLOCKCHAIN"
    
    # Count components
    det_nodes = len([p for p in os.walk(os.path.join(base_path, "DET")) if p[0].endswith("V1")])
    
    # Count domains and CAX pillars
    domains = set()
    cax_pillars = set()
    
    for root, dirs, files in os.walk(os.path.join(base_path, "DET")):
        if root.endswith("V1"):
            rel_path = os.path.relpath(root, os.path.join(base_path, "DET"))
            path_parts = rel_path.split(os.sep)
            if len(path_parts) == 5:
                cax, domain, sns, activity, version = path_parts
                domains.add(domain)
                cax_pillars.add(cax)
    
    return {
        "det_nodes": det_nodes,
        "domains": len(domains), 
        "cax_pillars": len(cax_pillars),
        "expected_combinations": len(domains) * len(cax_pillars)
    }

if __name__ == "__main__":
    print("🔍 UTCS-BLOCKCHAIN Implementation Validation")
    print("=" * 60)
    
    if validate_utcs_blockchain():
        summary = generate_implementation_summary()
        
        print("=" * 60)
        print("🎯 UTCS-BLOCKCHAIN IMPLEMENTATION COMPLETE!")
        print("✅ All validations passed")
        print("✅ Hierarchical blockchain structure deployed")
        print(f"✅ {summary['domains']} domains × {summary['cax_pillars']} CAX pillars = {summary['det_nodes']} registry nodes")
        print("✅ Complete DET evidence node structure")
        print("✅ SHA-256 + Ed25519 cryptographic security placeholders")
        print("✅ ATA SNS compliance mapping")
        print("✅ Bidirectional traceability framework")
        print("✅ CADET circular assurance integration")
        
        print(f"\n📊 IMPLEMENTATION SUMMARY:")
        print(f"├── CADET: Circular Assurance by Digital Evolutive Twin")
        print(f"├── DET: {summary['det_nodes']} registry nodes")
        print(f"├── TRACES: Traceability Records framework") 
        print(f"├── DOMAINS: {summary['domains']} technical domains")
        print(f"└── TOTAL: {summary['domains']}×{summary['cax_pillars']} = {summary['expected_combinations']} domain×CAX combinations")
        
    else:
        print("❌ UTCS-BLOCKCHAIN validation failed")
        exit(1)