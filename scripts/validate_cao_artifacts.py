#!/usr/bin/env python3
"""
CAO Artifacts Validation Script

Validates CAO (Computer-Aided Organization) artifacts against their JSON schemas:
- QAL Policy Pack
- Budget Vector  
- Risk Register
- QAL Bus Events
- DET Templates

Usage:
    python scripts/validate_cao_artifacts.py [files...]
    python scripts/validate_cao_artifacts.py --help
"""

import argparse
import json
import pathlib
import sys
from typing import Dict, List, Optional, Tuple

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("ERROR: jsonschema library not found. Install with: pip install jsonschema")
    sys.exit(1)


class CAOValidator:
    """CAO artifacts validator using JSON Schema."""
    
    def __init__(self, schemas_dir: pathlib.Path):
        """Initialize validator with schemas directory."""
        self.schemas_dir = schemas_dir
        self.schemas = {}
        self._load_schemas()
    
    def _load_schemas(self) -> None:
        """Load all CAO schemas from the schemas directory."""
        schema_files = {
            'utcs_mi': 'utcs_mi.schema.json',
            'policy_pack': 'cao_policy_pack.schema.json', 
            'budget_vector': 'cao_budget_vector.schema.json',
            'risk_register': 'cao_risk_register.schema.json',
            'qal_bus_events': 'cao_qal_bus_events.schema.json',
            'det_template': 'det_template.schema.json',
            'grpo': 'cao_grpo.schema.json'
        }
        
        for name, filename in schema_files.items():
            schema_path = self.schemas_dir / filename
            if not schema_path.exists():
                print(f"WARNING: Schema file not found: {schema_path}")
                continue
                
            try:
                with open(schema_path, 'r', encoding='utf-8') as f:
                    self.schemas[name] = json.load(f)
                print(f"✓ Loaded schema: {filename}")
            except Exception as e:
                print(f"ERROR: Failed to load schema {filename}: {e}")
                sys.exit(1)
    
    def _detect_artifact_type(self, data: dict) -> Optional[str]:
        """Detect the type of CAO artifact based on its structure."""
        if 'policies' in data and 'package_name' in data:
            return 'policy_pack'
        elif 'allocations' in data and 'period' in data:
            return 'budget_vector'
        elif 'risks' in data and 'register_utcs_mi_id' in data:
            return 'risk_register'
        elif 'events' in data:
            return 'qal_bus_events'
        elif 'det_id' in data and 'object_ref' in data:
            return 'det_template'
        elif ('resource_pools' in data or 'current_allocations' in data or 'allocation_summary' in data or 
              'optimization_config' in data or 'grpo' in data or 'matrix_metadata' in data or
              'conflict_resolution_framework' in data or 'active_conflicts' in data or
              'resolved_conflicts' in data or 'resolution_metadata' in data):
            return 'grpo'
        return None
    
    def validate_file(self, filepath: pathlib.Path) -> Tuple[bool, List[str]]:
        """Validate a single CAO artifact file."""
        errors = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]
        except Exception as e:
            return False, [f"Failed to read file: {e}"]
        
        # Detect artifact type
        artifact_type = self._detect_artifact_type(data)
        if not artifact_type:
            return False, ["Could not detect CAO artifact type"]
        
        if artifact_type not in self.schemas:
            return False, [f"No schema available for artifact type: {artifact_type}"]
        
        # Validate against schema - simplified validation without $ref resolution
        try:
            # Skip UTCS-MI reference validation for now
            schema = self.schemas[artifact_type].copy()
            if 'properties' in schema:
                for prop_name, prop_schema in schema['properties'].items():
                    if isinstance(prop_schema, dict) and '$ref' in prop_schema:
                        # Replace $ref with simple string validation for UTCS-MI
                        if prop_schema['$ref'] == 'utcs_mi.schema.json':
                            schema['properties'][prop_name] = {'type': 'string', 'minLength': 50}
            
            validate(instance=data, schema=schema)
            return True, []
            
        except ValidationError as e:
            error_path = " -> ".join(str(p) for p in e.absolute_path)
            error_msg = f"Validation error at '{error_path}': {e.message}"
            return False, [error_msg]
        except Exception as e:
            return False, [f"Schema validation failed: {e}"]
    
    def validate_utcs_mi(self, utcs_mi_id: str) -> Tuple[bool, List[str]]:
        """Validate a UTCS-MI identifier string."""
        if 'utcs_mi' not in self.schemas:
            return False, ["UTCS-MI schema not available"]
        
        try:
            validate(instance=utcs_mi_id, schema=self.schemas['utcs_mi'])
            return True, []
        except ValidationError as e:
            return False, [f"UTCS-MI validation failed: {e.message}"]
        except Exception as e:
            return False, [f"UTCS-MI validation error: {e}"]


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate CAO artifacts against JSON schemas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/validate_cao_artifacts.py QAL-Policy-Pack.json
    python scripts/validate_cao_artifacts.py *.json
    python scripts/validate_cao_artifacts.py --utcs-mi "EstándarUniversal:..."
        """
    )
    
    parser.add_argument(
        'files', 
        nargs='*', 
        help='CAO artifact files to validate'
    )
    
    parser.add_argument(
        '--utcs-mi',
        help='Validate a single UTCS-MI identifier'
    )
    
    parser.add_argument(
        '--schemas-dir',
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent.parent / 'schemas',
        help='Directory containing JSON schemas (default: ../schemas)'
    )
    
    args = parser.parse_args()
    
    if not args.files and not args.utcs_mi:
        parser.print_help()
        return 1
    
    # Initialize validator
    try:
        validator = CAOValidator(args.schemas_dir)
    except Exception as e:
        print(f"ERROR: Failed to initialize validator: {e}")
        return 1
    
    exit_code = 0
    
    # Validate UTCS-MI if provided
    if args.utcs_mi:
        success, errors = validator.validate_utcs_mi(args.utcs_mi)
        if success:
            print(f"✓ UTCS-MI valid: {args.utcs_mi}")
        else:
            print(f"✗ UTCS-MI invalid: {args.utcs_mi}")
            for error in errors:
                print(f"  {error}")
            exit_code = 1
    
    # Validate files
    for filepath_str in args.files:
        filepath = pathlib.Path(filepath_str)
        
        if not filepath.exists():
            print(f"✗ File not found: {filepath}")
            exit_code = 1
            continue
        
        if not filepath.suffix.lower() == '.json':
            print(f"⚠ Skipping non-JSON file: {filepath}")
            continue
        
        success, errors = validator.validate_file(filepath)
        
        if success:
            print(f"✓ {filepath}: Valid CAO artifact")
        else:
            print(f"✗ {filepath}: Validation failed")
            for error in errors:
                print(f"  {error}")
            exit_code = 1
    
    if exit_code == 0:
        print("\n🎉 All CAO artifacts validated successfully!")
    else:
        print(f"\n❌ Validation failed with {exit_code} errors")
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())