#!/usr/bin/env python3
"""
AGUA-TRIPS Protocol Validation Script

Validates TRIPS events, system deltas, and CLI operations against schemas.
"""

import json
import sys
import os
from pathlib import Path
import jsonschema
from datetime import datetime

def load_schema(schema_name):
    """Load a JSON schema file."""
    schema_path = Path(__file__).parent / "schemas" / f"{schema_name}.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_trips_event(event_data):
    """Validate a TRIPS event against schema."""
    schema = load_schema("agua_trips")
    try:
        jsonschema.validate(event_data, schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, str(e)

def validate_system_delta(delta_data):
    """Validate a system delta against schema."""
    schema = load_schema("trips_system_delta")
    try:
        jsonschema.validate(delta_data, schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, str(e)

def validate_file(file_path):
    """Validate a single JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"JSON decode error: {e}"
    except Exception as e:
        return False, f"File read error: {e}"
    
    # Determine validation type based on content
    if "event_type" in data:
        if data["event_type"].startswith("TRIPS."):
            return validate_trips_event(data)
    elif "delta_id" in data:
        return validate_system_delta(data)
    elif "operations" in data and "from_version" in data:
        return validate_system_delta(data)
    elif "det_id" in data:
        # DET files - skip validation for now as they follow DET schema
        return True, "DET file - skipped"
    
    return False, "Unable to determine validation type"

def main():
    """Main validation function."""
    if len(sys.argv) < 2:
        print("Usage: python validate_trips.py <file1.json> [file2.json] ...")
        print("       python validate_trips.py --all")
        return 1
    
    files_to_validate = []
    
    if sys.argv[1] == "--all":
        # Find all TRIPS-related JSON files, excluding schemas
        trips_dirs = ["trips_data", "events", "examples"]
        for trips_dir in trips_dirs:
            trips_path = Path(trips_dir)
            if trips_path.exists():
                files_to_validate.extend(trips_path.glob("**/*.json"))
    else:
        files_to_validate = [Path(f) for f in sys.argv[1:]]
    
    total_files = len(files_to_validate)
    valid_files = 0
    errors = []
    
    print(f"Validating {total_files} TRIPS files...")
    print("-" * 60)
    
    for file_path in files_to_validate:
        if not file_path.exists():
            errors.append(f"File not found: {file_path}")
            print(f"✗ {file_path} - File not found")
            continue
        
        is_valid, error_msg = validate_file(file_path)
        
        if is_valid:
            valid_files += 1
            print(f"✓ {file_path}")
        else:
            errors.append(f"{file_path}: {error_msg}")
            print(f"✗ {file_path} - {error_msg}")
    
    print("-" * 60)
    print(f"Validation complete: {valid_files}/{total_files} files valid")
    
    if errors:
        print(f"\nErrors found in {len(errors)} files:")
        for error in errors:
            print(f"  • {error}")
        return 1
    
    print("All files validated successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())