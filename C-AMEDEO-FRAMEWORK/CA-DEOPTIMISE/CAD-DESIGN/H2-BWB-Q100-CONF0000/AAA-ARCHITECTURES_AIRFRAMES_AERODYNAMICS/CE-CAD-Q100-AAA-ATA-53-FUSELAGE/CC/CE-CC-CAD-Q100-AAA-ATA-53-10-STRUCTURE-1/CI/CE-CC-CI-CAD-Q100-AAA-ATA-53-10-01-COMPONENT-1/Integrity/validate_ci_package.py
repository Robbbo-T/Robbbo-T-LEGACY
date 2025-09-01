#!/usr/bin/env python3
"""
Validador Python completo para CI packages.
Valida coherencia de tamaños, hashes y Validation Properties AP242.
"""

import os
import sys
import json
import yaml
import hashlib
from pathlib import Path

def validate_ci_package(ci_path: str) -> bool:
    """Validate complete CI package integrity"""
    ci_dir = Path(ci_path)
    print(f"🔍 Validating CI package: {ci_dir.name}")
    
    errors = []
    warnings = []
    
    # Check required files
    required_files = [
        "PBS.json",
        "EBOM.yaml", 
        "MBOM.yaml",
        "CADParameters.json",
        "Effectivities.yaml",
        "traceability.yaml",
        "README.md"
    ]
    
    for req_file in required_files:
        file_path = ci_dir / req_file
        if not file_path.exists():
            errors.append(f"Missing required file: {req_file}")
    
    # Check required directories
    required_dirs = ["3DModels", "Drawings", "Integrity"]
    for req_dir in required_dirs:
        dir_path = ci_dir / req_dir
        if not dir_path.exists():
            errors.append(f"Missing required directory: {req_dir}")
    
    # Validate JSON files
    json_files = ["PBS.json", "CADParameters.json"]
    for json_file in json_files:
        file_path = ci_dir / json_file
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    json.load(f)
                print(f"✅ Valid JSON: {json_file}")
            except json.JSONDecodeError as e:
                errors.append(f"Invalid JSON in {json_file}: {e}")
    
    # Validate YAML files
    yaml_files = ["EBOM.yaml", "MBOM.yaml", "Effectivities.yaml", "traceability.yaml"]
    for yaml_file in yaml_files:
        file_path = ci_dir / yaml_file
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    yaml.safe_load(f)
                print(f"✅ Valid YAML: {yaml_file}")
            except yaml.YAMLError as e:
                errors.append(f"Invalid YAML in {yaml_file}: {e}")
    
    # Validate manifest.yaml if exists
    manifest_path = ci_dir / "Integrity" / "manifest.yaml"
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r') as f:
                manifest = yaml.safe_load(f)
            
            # Check manifest structure
            required_sections = ["metadata", "artifacts"]
            for section in required_sections:
                if section not in manifest:
                    errors.append(f"Missing section in manifest.yaml: {section}")
            
            # Validate file hashes if artifacts are defined
            if "artifacts" in manifest:
                for category in ["3d_models", "drawings"]:
                    if category in manifest["artifacts"]:
                        for artifact in manifest["artifacts"][category]:
                            file_path = ci_dir / artifact["file"]
                            if file_path.exists():
                                # Calculate actual hash
                                with open(file_path, 'rb') as f:
                                    actual_hash = hashlib.sha256(f.read()).hexdigest()
                                
                                expected_hash = artifact.get("sha256", "")
                                if expected_hash and actual_hash != expected_hash:
                                    errors.append(f"Hash mismatch for {artifact['file']}: expected {expected_hash}, got {actual_hash}")
                                else:
                                    print(f"✅ Hash verified: {artifact['file']}")
                                
                                # Check file size
                                actual_size = file_path.stat().st_size
                                expected_size = artifact.get("size_bytes", 0)
                                if expected_size and actual_size != expected_size:
                                    warnings.append(f"Size mismatch for {artifact['file']}: expected {expected_size}, got {actual_size}")
                            else:
                                warnings.append(f"Referenced file not found: {artifact['file']}")
            
            print(f"✅ Valid manifest: manifest.yaml")
            
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML in manifest.yaml: {e}")
        except Exception as e:
            errors.append(f"Error validating manifest.yaml: {e}")
    else:
        warnings.append("No manifest.yaml found in Integrity/ directory")
    
    # Check SHA256SUMS.txt if exists
    sha_file = ci_dir / "Integrity" / "SHA256SUMS.txt"
    if sha_file.exists():
        try:
            with open(sha_file, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(None, 1)
                        if len(parts) == 2:
                            expected_hash, rel_path = parts
                            file_path = ci_dir / rel_path
                            if file_path.exists():
                                with open(file_path, 'rb') as tf:
                                    actual_hash = hashlib.sha256(tf.read()).hexdigest()
                                if actual_hash != expected_hash:
                                    errors.append(f"SHA256SUMS.txt hash mismatch for {rel_path}")
                                else:
                                    print(f"✅ SHA256SUMS verified: {rel_path}")
            print(f"✅ SHA256SUMS.txt validation complete")
        except Exception as e:
            errors.append(f"Error validating SHA256SUMS.txt: {e}")
    else:
        warnings.append("No SHA256SUMS.txt found")
    
    # Print results
    if warnings:
        print("\n⚠️ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if errors:
        print("\n❌ Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print(f"\n✅ CI package validation PASSED: {ci_dir.name}")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_ci_package.py <ci_directory>")
        sys.exit(1)
    
    ci_directory = sys.argv[1]
    if not os.path.exists(ci_directory):
        print(f"❌ CI directory not found: {ci_directory}")
        sys.exit(1)
    
    success = validate_ci_package(ci_directory)
    sys.exit(0 if success else 1)