#!/usr/bin/env python3
"""
Generate complete DOMAINS registry structure with all 15 domains
Updates C-AMEDEO-FRAMEWORK to include missing domains
"""

import os
import yaml

# Complete domain definitions
DOMAINS = {
    "AAA": {
        "name": "ARCHITECTURES_AIRFRAMES_AERODYNAMICS",
        "description": "Airframe structures, aerodynamic surfaces, and architectural systems",
        "ata_primary": ["02", "06", "11", "18", "20", "51", "52", "53", "55", "56", "57"],
        "co_domains": ["MMM", "EEE", "OOO"]
    },
    "AAP": {
        "name": "AIRPORTS_ADAPTATIONS", 
        "description": "Airport infrastructure interfaces and ground operation adaptations",
        "ata_primary": ["01", "07", "12", "96"],
        "co_domains": ["IIF", "LIB", "EDI"]
    },
    "CCC": {
        "name": "COCKPIT_CABIN_CARGO_SYSTEMS",
        "description": "Cockpit controls, cabin systems, and cargo handling",
        "ata_primary": ["11", "21", "25", "33", "44", "45"],
        "co_domains": ["EDI", "IIS", "AAA"]
    },
    "CQH": {
        "name": "CRYOGENICS_QUANTUM_INTERFACES_HYDROGEN_CELLS",
        "description": "Cryogenic systems, quantum interfaces, and hydrogen fuel cells",
        "ata_primary": ["28", "29", "75", "79"],
        "co_domains": ["PPP", "EER", "DDD"]
    },
    "DDD": {
        "name": "DEFENCE_CYBERSECURITY_SAFETY",
        "description": "Defense systems, cybersecurity protocols, and safety assurance", 
        "ata_primary": ["20", "46", "97"],
        "co_domains": ["EDI", "IIS", "OOO"]
    },
    "EDI": {
        "name": "ELECTRONICS_DIGITAL_INSTRUMENTS",
        "description": "Electronic systems and digital instrumentation",
        "ata_primary": ["22", "23", "31", "34", "42"],
        "co_domains": ["LCC", "IIS", "OOO"]
    },
    "EEE": {
        "name": "ENVIRONMENTAL_REMEDIATION_CIRCULARITY",
        "description": "Environmental systems and circular economy implementation",
        "ata_primary": ["20", "30", "36", "98"],
        "co_domains": ["EER", "LIB", "AAA"]
    },
    "EER": {
        "name": "ENERGY_AND_RENEWABLE",
        "description": "Energy systems and renewable power generation",
        "ata_primary": ["24", "26", "60", "61"],
        "co_domains": ["PPP", "CQH", "EDI"]
    },
    "IIF": {
        "name": "INFRASTRUCTURES_AND_FACILITIES_VALUE_CHAINS",
        "description": "Infrastructure systems and value chain management",
        "ata_primary": ["07", "12", "96"],
        "co_domains": ["LIB", "AAP", "MMM"]
    },
    "IIS": {
        "name": "INTELLIGENT_SYSTEMS_ONBOARD_AI",
        "description": "Intelligent systems and onboard artificial intelligence",
        "ata_primary": ["22", "31", "42", "46"],
        "co_domains": ["EDI", "OOO", "LCC"]
    },
    "LCC": {
        "name": "LINKS_COMMUNICATIONS_CONTROL_IoT",
        "description": "Communication links, control systems, and IoT integration",
        "ata_primary": ["23", "31", "34", "42", "46"],
        "co_domains": ["EDI", "IIS", "OOO"]
    },
    "LIB": {
        "name": "LOGISTICS_INTEGRATED_BLOCKCHAIN",
        "description": "Logistics management and integrated blockchain systems",
        "ata_primary": ["05", "07", "12"],
        "co_domains": ["IIF", "EEE", "AAP"]
    },
    "MMM": {
        "name": "MECHANICAL_MATERIAL_MONITORING",
        "description": "Mechanical systems, materials engineering, and monitoring",
        "ata_primary": ["51", "52", "53", "54", "55", "56", "57", "71", "72", "73", "74", "75", "76", "77", "78", "79"],
        "co_domains": ["AAA", "IIF", "PPP"]
    },
    "OOO": {
        "name": "OPERATING_SYSTEMS_NAVIGATION_HPC",
        "description": "Operating systems, navigation, and high-performance computing",
        "ata_primary": ["22", "31", "34", "42", "46"],
        "co_domains": ["IIS", "EDI", "LCC"]
    },
    "PPP": {
        "name": "PROPULSION_AND_FUEL",
        "description": "Propulsion systems and fuel management",
        "ata_primary": ["70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85"],
        "co_domains": ["CQH", "EER", "MMM"]
    }
}

CAX_PILLARS = ["CAD-DESIGN", "CAE-ENGINEERING", "CAM-MANUFACTURING", "CAT-SOURCE", "CAI-INTEGRATIONS", "CAS-SUSTAINMENT", "CAO-ORGANIZATION"]
FLOWS = ["CA-DEOPTIMISE", "CA-OPTIMISED"]

def create_domain_structure(base_path, flow, pillar, domain_code, domain_info):
    """Create complete domain structure for a CAX pillar"""
    
    # Create domain directory
    domain_dir_name = f"{domain_code}-{domain_info['name']}"
    domain_path = os.path.join(base_path, flow, pillar, "H2-BWB-Q100-CONF0000", domain_dir_name)
    os.makedirs(domain_path, exist_ok=True)
    
    # Create domain README
    domain_readme = f"""# {domain_code} - {domain_info['name']}

## Domain Overview
**Code**: {domain_code}  
**Name**: {domain_info['name']}  
**Description**: {domain_info['description']}

## ATA SNS Coverage
Primary ATA codes owned by this domain:
{', '.join([f'ATA-{code}' for code in domain_info['ata_primary']])}

## Cross-Domain References
Co-domains that reference this domain:
{', '.join([f'[{co}](../{co}-*/)'for co in domain_info['co_domains']])}

## CAX Pillar Integration
This domain participates in **{pillar.replace('-', ' ')}** activities within the **{flow}** lifecycle flow.

## Digital Evidence Twin (DET) Registry
All activities within this domain generate DET evidence packs with the pattern:
```
DET:{pillar.split('-')[0]}:{domain_code}:<SNS>:<activity>:V<rev>
```

## CADET Integration
- **Circular Assurance**: Sustainability and circularity metrics tracking
- **Evolutionary Capability**: Evidence evolution and lifecycle closure
- **Cross-Domain Traceability**: Bidirectional references via TRACES framework

## Configuration
- **Aircraft**: H2-BWB-Q100 (Hydrogen-powered Blended Wing Body)
- **Configuration**: CONF0000 (Baseline configuration)
- **Lifecycle Flow**: {flow}
- **CAX Pillar**: {pillar}

## Dependencies
- **AQUA-OS BRIDGE**: Deterministic execution environment
- **GAIA AIR RTOS**: Safety-critical partitioning
- **CADET**: Circular assurance tracking
- **TRACES**: Traceability framework
- **DET Registry**: Evidence management

## Structure
```
{domain_dir_name}/
├── README.md (this file)
├── alias.yml (cross-domain references)
├── domain-config.yaml (domain configuration)
└── [CE directories will be created as needed]
```

---
*Part of the C-AMEDEO Framework for {domain_info['description']}*"""
    
    with open(os.path.join(domain_path, "README.md"), 'w') as f:
        f.write(domain_readme)
    
    # Create alias.yml for cross-domain references
    alias_config = {
        "UniversalStandard": "UTCS-MI v5.0",
        "alias_version": "1.0.0",
        "owner_domain": domain_code,
        "domain_name": domain_info['name'],
        "description": domain_info['description'],
        "co_domains": domain_info['co_domains'],
        "canonical_path": f"C-AMEDEO-FRAMEWORK/{flow}/{pillar}/H2-BWB-Q100-CONF0000/{domain_dir_name}/",
        "cross_references": {
            co_domain: f"../../../{pillar}/H2-BWB-Q100-CONF0000/{co_domain}-*/"
            for co_domain in domain_info['co_domains']
        },
        "ata_sns_primary": domain_info['ata_primary'],
        "cadet_integration": {
            "enabled": True,
            "circularity_tracking": True,
            "sustainability_metrics": True
        },
        "det_registry": {
            "pattern": f"DET:{pillar.split('-')[0]}:{domain_code}:<SNS>:<activity>:V<rev>",
            "evidence_types": ["design", "analysis", "test", "integration", "sustainment", "organization"]
        },
        "meta": {
            "owner": f"{domain_code}-Domain-Lead",
            "reviewer": "Chief-Architect",
            "last_updated": "2025-01-14T12:00:00Z",
            "change_ref": f"INIT-{domain_code}-DOMAIN-V1"
        }
    }
    
    with open(os.path.join(domain_path, "alias.yml"), 'w') as f:
        yaml.dump(alias_config, f, default_flow_style=False, sort_keys=False)
    
    # Create domain-config.yaml
    domain_config = {
        "domain": {
            "code": domain_code,
            "name": domain_info['name'],
            "description": domain_info['description'],
            "version": "1.0.0"
        },
        "cax_integration": {
            "pillar": pillar,
            "flow": flow,
            "configuration": "H2-BWB-Q100-CONF0000"
        },
        "ata_coverage": {
            "primary_codes": domain_info['ata_primary'],
            "compliance_frameworks": ["ATA iSpec 2200", "S1000D", "DO-178C", "DO-254"]
        },
        "traceability": {
            "cross_domain_refs": domain_info['co_domains'],
            "traces_enabled": True,
            "bidirectional": True
        },
        "evidence": {
            "det_pattern": f"DET:{pillar.split('-')[0]}:{domain_code}:<SNS>:<activity>:V<rev>",
            "cadet_tracking": True,
            "hash_algorithm": "SHA-256",
            "signature_algorithm": "Ed25519"
        }
    }
    
    with open(os.path.join(domain_path, "domain-config.yaml"), 'w') as f:
        yaml.dump(domain_config, f, default_flow_style=False, sort_keys=False)
    
    return domain_path

def main():
    """Generate complete domain structure across all CAX pillars and flows"""
    base_path = "C-AMEDEO-FRAMEWORK"
    
    created_domains = []
    
    for flow in FLOWS:
        for pillar in CAX_PILLARS:
            for domain_code, domain_info in DOMAINS.items():
                domain_path = create_domain_structure(base_path, flow, pillar, domain_code, domain_info)
                created_domains.append(domain_path)
                print(f"Created: {domain_path}")
    
    # Create DOMAINS registry summary
    os.makedirs("DOMAINS-REGISTRY", exist_ok=True)
    
    domains_summary = {
        "domains_registry": {
            "version": "1.0.0",
            "total_domains": len(DOMAINS),
            "total_cax_pillars": len(CAX_PILLARS),
            "total_flows": len(FLOWS),
            "total_combinations": len(DOMAINS) * len(CAX_PILLARS) * len(FLOWS),
            "domains": DOMAINS,
            "cax_pillars": CAX_PILLARS,
            "lifecycle_flows": FLOWS
        }
    }
    
    with open("DOMAINS-REGISTRY/domains-summary.yaml", 'w') as f:
        yaml.dump(domains_summary, f, default_flow_style=False, sort_keys=False)
    
    # Create DOMAINS registry README
    domains_readme = f"""# DOMAINS Registry - Complete Technical Domain Coverage

## Overview
Complete deployment of all 15 technical domains across the CAX framework.

**Total Deployment:**
- **{len(DOMAINS)} Domains** × **{len(CAX_PILLARS)} CAX Pillars** × **{len(FLOWS)} Flows** = **{len(DOMAINS) * len(CAX_PILLARS) * len(FLOWS)} Total Combinations**

## 15 Technical Domains

| Code | Name | Description | Primary ATA Codes |
|------|------|-------------|-------------------|"""
    
    for code, info in DOMAINS.items():
        ata_codes = ', '.join(info['ata_primary'][:5]) + ('...' if len(info['ata_primary']) > 5 else '')
        domains_readme += f"\n| **{code}** | {info['name']} | {info['description']} | {ata_codes} |"
    
    domains_readme += f"""

## CAX Pillars (7 total)
- **CAD** - Computer-Aided Design
- **CAE** - Computer-Aided Engineering  
- **CAM** - Computer-Aided Manufacturing
- **CAT** - Computer-Aided Testing
- **CAI** - Computer-Aided Integration
- **CAS** - Computer-Aided Sustainment
- **CAO** - Computer-Aided Organization

## Lifecycle Flows (2 total)
- **CA-DEOPTIMISE** - Initial design and optimization
- **CA-OPTIMISED** - Optimized and production-ready

## Cross-Domain Integration
Each domain includes:
- **Cross-domain references** via alias.yml
- **ATA SNS compliance** mapping
- **DET evidence** generation
- **CADET integration** for circular assurance
- **TRACES framework** for traceability

## Registry Files
- [domains-summary.yaml](domains-summary.yaml) - Complete domain registry
- Domain implementations in C-AMEDEO-FRAMEWORK/*/*/H2-BWB-Q100-CONF0000/
"""
    
    with open("DOMAINS-REGISTRY/README.md", 'w') as f:
        f.write(domains_readme)
    
    print(f"\nDomains registry created:")
    print(f"- {len(DOMAINS)} domains")
    print(f"- {len(CAX_PILLARS)} CAX pillars")
    print(f"- {len(FLOWS)} lifecycle flows") 
    print(f"- {len(created_domains)} total domain implementations")
    print(f"- Registry saved in DOMAINS-REGISTRY/")

if __name__ == "__main__":
    main()