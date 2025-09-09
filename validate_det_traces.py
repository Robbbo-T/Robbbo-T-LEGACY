#!/usr/bin/env python3
"""
DET Packet and Trace Validation Script
Validates all det_packet.json and trace.yaml files against their schemas
"""

import os
import json
import yaml
import sys
from pathlib import Path
import jsonschema
from jsonschema import validate, ValidationError

def load_schema(schema_path):
    """Load JSON schema from file"""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load schema {schema_path}: {e}")
        return None

def validate_det_packet(file_path, schema):
    """Validate a single det_packet.json file against schema"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        validate(instance=data, schema=schema)
        print(f"✅ Valid DET packet: {file_path}")
        return True
    except ValidationError as e:
        print(f"❌ Invalid DET packet {file_path}: {e.message}")
        return False
    except Exception as e:
        print(f"❌ Error reading DET packet {file_path}: {e}")
        return False

def validate_trace_file(file_path, schema):
    """Validate a single trace.yaml file against schema"""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        validate(instance=data, schema=schema)
        print(f"✅ Valid trace file: {file_path}")
        return True
    except ValidationError as e:
        print(f"❌ Invalid trace file {file_path}: {e.message}")
        return False
    except Exception as e:
        print(f"❌ Error reading trace file {file_path}: {e}")
        return False

def find_files(pattern, root_dir="."):
    """Find all files matching pattern"""
    root_path = Path(root_dir)
    return list(root_path.rglob(pattern))

def main():
    """Main validation function"""
    print("🔍 DET Packet and Trace Validation")
    print("=" * 50)
    
    # Load schemas
    det_schema_path = "UTCS-BLOCKCHAIN/DET/schemas/det-packet.schema.json"
    trace_schema_path = "UTCS-BLOCKCHAIN/DET/schemas/trace-record.schema.json"
    
    det_schema = load_schema(det_schema_path)
    trace_schema = load_schema(trace_schema_path)
    
    if not det_schema or not trace_schema:
        print("❌ Failed to load required schemas")
        return 1
    
    # Find all DET packet files
    det_files = find_files("det_packet.json")
    trace_files = find_files("trace.yaml")
    
    print(f"\n📊 Found {len(det_files)} DET packet files")
    print(f"📊 Found {len(trace_files)} trace files")
    
    # Validate DET packets
    det_valid = 0
    det_invalid = 0
    
    print(f"\n🔍 Validating DET packets...")
    for det_file in det_files:
        if validate_det_packet(det_file, det_schema):
            det_valid += 1
        else:
            det_invalid += 1
    
    # Validate trace files
    trace_valid = 0
    trace_invalid = 0
    
    print(f"\n🔍 Validating trace files...")
    for trace_file in trace_files:
        if validate_trace_file(trace_file, trace_schema):
            trace_valid += 1
        else:
            trace_invalid += 1
    
    # Summary
    print(f"\n📊 VALIDATION SUMMARY:")
    print(f"├── DET packets: {det_valid} valid, {det_invalid} invalid")
    print(f"└── Trace files: {trace_valid} valid, {trace_invalid} invalid")
    
    total_invalid = det_invalid + trace_invalid
    if total_invalid > 0:
        print(f"\n❌ VALIDATION FAILED: {total_invalid} invalid files")
        return 1
    else:
        print(f"\n✅ VALIDATION PASSED: All files valid")
        return 0

if __name__ == "__main__":
    sys.exit(main())