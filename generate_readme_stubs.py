#!/usr/bin/env python3
"""
Generate README stubs for missing domain/pillar folders
Following the pattern established by existing AAA/PPP domains
"""

import os
import sys
from pathlib import Path

# Domain mappings from existing codebase
DOMAINS = {
    "AAA": "ARCHITECTURES_AIRFRAMES_AERODYNAMICS",
    "AAP": "AIRPORTS_ADAPTATIONS", 
    "CCC": "COCKPIT_CABIN_CARGO_SYSTEMS",
    "CQH": "CRYOGENICS_QUANTUM_INTERFACES_HYDROGEN_CELLS",
    "DDD": "DEFENCE_CYBERSECURITY_SAFETY",
    "EDI": "ELECTRONICS_DIGITAL_INSTRUMENTS",
    "EEE": "ENVIRONMENTAL_REMEDIATION_CIRCULARITY",
    "EER": "ENERGY_AND_RENEWABLE",
    "IIF": "INFRASTRUCTURES_AND_FACILITIES_VALUE_CHAINS",
    "IIS": "INTELLIGENT_SYSTEMS_ONBOARD_AI",
    "LCC": "LIFECYCLE_EXTENSION_AND_MAINTENANCE",
    "LIB": "LIBRARIES_STANDARDS_COMPONENTS",
    "MMM": "MATERIALS_CABIN_SEATS",
    "OOO": "OPERATIONS_PROCEDURES",
    "PPP": "PROPULSION_AND_FUEL"
}

CAX_PILLARS = {
    "CAD": ("DESIGN", "Computer-Aided Design"),
    "CAE": ("ENGINEERING", "Computer-Aided Engineering"), 
    "CAM": ("MANUFACTURING", "Computer-Aided Manufacturing"),
    "CAT": ("SOURCE", "Computer-Aided Testing"),
    "CAI": ("INTEGRATIONS", "Computer-Aided Integration"),
    "CAS": ("SUSTAINMENT", "Computer-Aided Sustainment"),
    "CAO": ("ORGANIZATION", "Computer-Aided Organization"),
    "CAP": ("PROCESS", "Computer-Aided Process")
}

FLOWS = ["CA-DEOPTIMISE", "CA-OPTIMISED"]

def generate_domain_readme(domain_code, domain_name, cax_code, cax_name, flow):
    """Generate README content for a domain directory"""
    return f"""# {domain_code} - {domain_name}

## Domain Overview
**Code**: {domain_code}  
**Name**: {domain_name}  
**CAX Pillar**: {cax_code} - {cax_name}  
**Flow**: {flow}  
**Configuration**: H2-BWB-Q100-CONF0000

## Description
This domain implements {domain_name.lower().replace('_', ' ')} within the {cax_name} pillar of the C-AMEDEO framework.

## Framework Integration

### Digital Evidence Twin (DET)
All activities within this domain generate DET evidence packs with the pattern:
```
DET:{cax_code}:{domain_code}:<SNS>:<ACTIVITY>:V<REV>
```

### S1000D Integration
This domain generates Data Module Codes (DMC) following the pattern:
```
DMC: Q100-<SNS>-<DC>-<IC>-<ICV>-<LC>-<ISSUE>
```

### Dependencies
- **AQUA-OS BRIDGE**: Provides deterministic execution environment
- **GAIA AIR RTOS**: Ensures safety-critical partitioning where applicable
- **CADET**: Tracks circularity and sustainability metrics
- **AMPEL360**: Risk-aware design optimization integration

## Structure
```
{domain_code}-{domain_name}/
├── README.md (this file)
├── [Configuration Envelopes will be created as needed]
└── [Domain-specific artifacts]
```

## Status
- **Framework**: C-AMEDEO {flow}
- **Pillar**: {cax_code}
- **Domain**: {domain_code}
- **Configuration**: H2-BWB-Q100-CONF0000

---
*Part of the C-AMEDEO Framework for {domain_name}*
"""

def main():
    """Generate README stubs for all missing domain directories"""
    print("🔍 Generating README stubs for domain/pillar folders")
    print("=" * 60)
    
    base_path = Path("C-AMEDEO-FRAMEWORK")
    generated_count = 0
    
    for flow in FLOWS:
        for cax_code, (pillar_suffix, cax_name) in CAX_PILLARS.items():
            pillar_dir = f"{cax_code}-{pillar_suffix}"
            
            for domain_code, domain_name in DOMAINS.items():
                domain_dir_name = f"{domain_code}-{domain_name}"
                domain_path = base_path / flow / pillar_dir / "H2-BWB-Q100-CONF0000" / domain_dir_name
                readme_path = domain_path / "README.md"
                
                # Only create if directory exists but README doesn't
                if domain_path.exists() and not readme_path.exists():
                    readme_content = generate_domain_readme(
                        domain_code, domain_name, cax_code, cax_name, flow
                    )
                    
                    with open(readme_path, 'w') as f:
                        f.write(readme_content)
                    
                    print(f"✅ Generated: {readme_path}")
                    generated_count += 1
                elif not domain_path.exists():
                    print(f"⏭️  Skipped (no directory): {domain_path}")
                else:
                    print(f"📄 Exists: {readme_path}")
    
    print(f"\n📊 SUMMARY:")
    print(f"├── Generated: {generated_count} README files")
    print(f"└── Status: {'✅ Complete' if generated_count > 0 else '📄 All existing'}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())