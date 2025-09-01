#!/usr/bin/env python3
"""
Generate complete DET registry structure for CAX framework
Creates 15 domains × 7 CAX pillars = 105 DET evidence templates
"""

import os
import json
import yaml
from datetime import datetime

# Domain definitions
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
    "LCC": "LINKS_COMMUNICATIONS_CONTROL_IoT",
    "LIB": "LOGISTICS_INTEGRATED_BLOCKCHAIN",
    "MMM": "MECHANICAL_MATERIAL_MONITORING",
    "OOO": "OPERATING_SYSTEMS_NAVIGATION_HPC",
    "PPP": "PROPULSION_AND_FUEL"
}

# CAX pillar definitions
CAX_PILLARS = {
    "CAD": "Computer-Aided Design",
    "CAE": "Computer-Aided Engineering", 
    "CAM": "Computer-Aided Manufacturing",
    "CAT": "Computer-Aided Testing",
    "CAI": "Computer-Aided Integration",
    "CAS": "Computer-Aided Sustainment",
    "CAO": "Computer-Aided Organization"
}

# Sample ATA SNS codes for each domain
DOMAIN_ATA_MAPPING = {
    "AAA": ["02", "06", "11", "18", "20", "51", "52", "53", "55", "56", "57"],
    "AAP": ["01", "07", "12", "96"],
    "CCC": ["11", "21", "25", "33", "44", "45"],
    "CQH": ["28", "29", "75", "79"],
    "DDD": ["20", "46", "97"],
    "EDI": ["22", "23", "31", "34", "42"],
    "EEE": ["20", "30", "36", "98"],
    "EER": ["24", "26", "60", "61"],
    "IIF": ["07", "12", "96"],
    "IIS": ["22", "31", "42", "46"],
    "LCC": ["23", "31", "34", "42", "46"],
    "LIB": ["05", "07", "12"],
    "MMM": ["51", "52", "53", "54", "55", "56", "57", "71", "72", "73", "74", "75", "76", "77", "78", "79"],
    "OOO": ["22", "31", "34", "42", "46"],
    "PPP": ["70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85"]
}

def generate_det_template(cax, domain, ata_sns):
    """Generate DET evidence template for specific CAX-Domain-ATA combination"""
    timestamp = datetime.now().isoformat() + "Z"
    
    template = {
        "det_id": f"DET:{cax}:{domain}:{ata_sns}:template:V1",
        "ts": timestamp,
        "refs": {
            "ce": f"CE-{cax}-Q100-{domain}-ATA-{ata_sns}-TEMPLATE",
            "ci": f"CE-CC-CI-{cax}-Q100-{domain}-ATA-{ata_sns}-01-TEMPLATE-ITEM",
            "cadet_chain": f"CADET:{domain}:{cax}:V1"
        },
        "inputs": {
            "domain": domain,
            "domain_name": DOMAINS[domain],
            "cax_pillar": cax,
            "cax_description": CAX_PILLARS[cax],
            "ata_sns": ata_sns,
            "configuration": "H2-BWB-Q100-CONF0000"
        },
        "processing": {
            "tool": f"AQUA-OS:{cax.lower()}-registry@1.0",
            "params": {
                "domain_owner": domain,
                "cross_domain_refs": True,
                "ata_compliance": True,
                "circular_assurance": True
            }
        },
        "outputs": {
            "registry_status": "TEMPLATE_CREATED",
            "traceability_links": [],
            "compliance_status": "ATA_ALIGNED",
            "circularity_metrics": {
                "reuse_potential": "TBD",
                "sustainability_score": "TBD",
                "lifecycle_stage": "DESIGN"
            },
            "units": "dimensionless"
        },
        "traces": {
            "upstream_refs": [],
            "downstream_refs": [],
            "cross_domain_refs": [],
            "bidirectional": True
        },
        "cadet_metrics": {
            "circular_assurance": {
                "reuse_percentage": None,
                "co2_savings_kg": None,
                "energy_savings_kwh": None,
                "lifecycle_extension_months": None
            },
            "sustainability_kpis": {
                "iso14001_compliance": "PENDING",
                "csrd_reporting": "ENABLED", 
                "gri_alignment": "TRACKED"
            }
        },
        "hash": "SHA256_PLACEHOLDER_" + f"{cax}_{domain}_{ata_sns}".replace("-", "_"),
        "sig": {
            "alg": "Ed25519",
            "by": f"cadet-registry@{domain.lower()}"
        }
    }
    
    return template

def main():
    """Generate complete DET registry structure"""
    base_dir = "DET-REGISTRY"
    os.makedirs(base_dir, exist_ok=True)
    
    # Create registry index
    registry_index = {
        "cadet_registry_version": "1.0.0",
        "generated_timestamp": datetime.now().isoformat() + "Z",
        "total_domains": len(DOMAINS),
        "total_cax_pillars": len(CAX_PILLARS),
        "total_combinations": len(DOMAINS) * len(CAX_PILLARS),
        "domains": DOMAINS,
        "cax_pillars": CAX_PILLARS,
        "det_templates": {}
    }
    
    # Generate DET templates for all combinations
    for domain_code, domain_name in DOMAINS.items():
        for cax_code, cax_name in CAX_PILLARS.items():
            # Create domain/CAX directory
            domain_cax_dir = os.path.join(base_dir, domain_code, cax_code)
            os.makedirs(domain_cax_dir, exist_ok=True)
            
            # Initialize registry entry
            if domain_code not in registry_index["det_templates"]:
                registry_index["det_templates"][domain_code] = {}
            registry_index["det_templates"][domain_code][cax_code] = []
            
            # Generate templates for relevant ATA SNS codes
            ata_codes = DOMAIN_ATA_MAPPING.get(domain_code, ["99"])
            
            for ata_sns in ata_codes:
                # Generate DET template
                det_template = generate_det_template(cax_code, domain_code, ata_sns)
                
                # Save DET template file
                filename = f"DET-{cax_code}-{domain_code}-{ata_sns}-template-V1.json"
                filepath = os.path.join(domain_cax_dir, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(det_template, f, indent=2)
                
                # Add to registry index
                registry_index["det_templates"][domain_code][cax_code].append({
                    "det_id": det_template["det_id"],
                    "filename": filename,
                    "ata_sns": ata_sns,
                    "filepath": filepath
                })
            
            # Create domain/CAX README
            readme_content = f"""# {cax_code} - {domain_code} Registry

## {cax_name} in {domain_name}

Domain: **{domain_code}** - {domain_name}  
CAX Pillar: **{cax_code}** - {cax_name}

## DET Evidence Templates

This directory contains Digital Evidence Twin templates for:
- Domain: {domain_code} ({domain_name})
- CAX Pillar: {cax_code} ({cax_name})
- ATA SNS Codes: {', '.join(DOMAIN_ATA_MAPPING.get(domain_code, ['99']))}

## Namespacing Pattern
```
DET:{cax_code}:{domain_code}:<SNS>:<activity>:<version>
```

## Files
"""
            
            for ata_sns in DOMAIN_ATA_MAPPING.get(domain_code, ["99"]):
                filename = f"DET-{cax_code}-{domain_code}-{ata_sns}-template-V1.json"
                readme_content += f"- [{filename}]({filename}) - ATA {ata_sns} evidence template\n"
            
            readme_path = os.path.join(domain_cax_dir, "README.md")
            with open(readme_path, 'w', encoding='utf_8') as f:
                f.write(readme_content)
    
    # Save registry index
    with open(os.path.join(base_dir, "registry-index.json"), 'w') as f:
        json.dump(registry_index, f, indent=2)
    
    # Create main README for DET registry
    main_readme = f"""# DET Registry - Digital Evidence Twin

## Overview
Complete registry of Digital Evidence Twin templates for the CAX framework.

- **Total Domains**: {len(DOMAINS)}
- **Total CAX Pillars**: {len(CAX_PILLARS)}  
- **Total Combinations**: {len(DOMAINS) * len(CAX_PILLARS)} DET template sets

## Domain Structure
"""
    
    for domain_code, domain_name in DOMAINS.items():
        main_readme += f"- **{domain_code}** - [{domain_name}]({domain_code}/)\n"
    
    main_readme += """
## CAX Pillars
"""
    
    for cax_code, cax_name in CAX_PILLARS.items():
        main_readme += f"- **{cax_code}** - {cax_name}\n"
    
    main_readme += """
## Registry Files
- [registry-index.json](registry-index.json) - Complete registry index
- Domain directories contain CAX pillar subdirectories
- Each CAX-Domain combination contains DET templates for relevant ATA SNS codes

## Namespacing
```
DET:<CAX>:<DOMAIN>:<SNS>:<activity>:<version>
```

Example: `DET:CAD:AAA:52-10:design:V3`
"""
    
    with open(os.path.join(base_dir, "README.md"), 'w', encoding='utf_8') as f:
        f.write(main_readme)
    
    print(f"Generated complete DET registry:")
    print(f"- {len(DOMAINS)} domains")
    print(f"- {len(CAX_PILLARS)} CAX pillars") 
    print(f"- {len(DOMAINS) * len(CAX_PILLARS)} domain×CAX combinations")
    print(f"- Registry saved in {base_dir}/")

if __name__ == "__main__":
    main()