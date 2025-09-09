#!/usr/bin/env python3
"""
Validate DET patterns for AAA interface brainstorming
Demonstrates compliance with C-AMEDEO framework DET requirements
"""

import json
import re
import sys
from pathlib import Path

def validate_det_pattern(det_id):
    """Validate DET ID follows CAB pattern: DET:CAB:DOMAIN:SNS:activity:Vrev"""
    pattern = r'^DET:CAB:[A-Z]{3}:SNS-\d{2}-\d{2}:[a-zA-Z_]+:V\d+$'
    return bool(re.match(pattern, det_id))

def validate_interface_det_file(det_file_path):
    """Validate a DET JSON file for interface brainstorming"""
    try:
        with open(det_file_path, 'r') as f:
            det_data = json.load(f)
            
        # Required fields
        required_fields = ['det_id', 'timestamp', 'refs', 'inputs', 'processing', 'outputs']
        for field in required_fields:
            if field not in det_data:
                return False, f"Missing required field: {field}"
                
        # Validate DET ID pattern
        det_id = det_data.get('det_id', '')
        if not validate_det_pattern(det_id):
            return False, f"Invalid DET ID pattern: {det_id}"
            
        # Validate interface scope
        inputs = det_data.get('inputs', {})
        interface_scope = inputs.get('interface_scope', [])
        expected_interfaces = ['CQH', 'PPP', 'DDD']
        
        if not all(iface in expected_interfaces for iface in interface_scope):
            return False, f"Invalid interface scope: {interface_scope}"
            
        # Validate quantum algorithms
        processing = det_data.get('processing', {})
        algorithms = processing.get('algorithms', [])
        expected_algorithms = ['QML_latent_navigation', 'QAOA_optimization', 
                              'Grover_patent_search', 'Maximum_entropy_diversity']
        
        if not any(alg in algorithms for alg in expected_algorithms):
            return False, f"No quantum algorithms detected: {algorithms}"
            
        # Validate outputs
        outputs = det_data.get('outputs', {})
        if 'quantum_confidence' not in outputs:
            return False, "Missing quantum_confidence in outputs"
            
        qc = outputs.get('quantum_confidence', 0)
        if not (0.0 <= qc <= 1.0):
            return False, f"Invalid quantum_confidence range: {qc}"
            
        return True, "Valid DET file"
        
    except Exception as e:
        return False, f"Error processing file: {str(e)}"

def main():
    """Main validation function"""
    print("🔍 Validating AAA Interface DET Patterns")
    print("=" * 50)
    
    # Find DET files in quantum-models
    base_path = Path("C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAB-BRAINSTORMING/H2-BWB-Q100-CONF0000")
    det_files = list(base_path.glob("**/det-*.json"))
    
    if not det_files:
        print("❌ No DET files found")
        return 1
        
    all_valid = True
    
    for det_file in det_files:
        print(f"\n📋 Validating: {det_file.name}")
        is_valid, message = validate_interface_det_file(det_file)
        
        if is_valid:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            all_valid = False
            
    print("\n" + "=" * 50)
    if all_valid:
        print("✅ All DET files are valid!")
        print("🚀 Ready for CAD handoff")
        return 0
    else:
        print("❌ Some DET files have issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())