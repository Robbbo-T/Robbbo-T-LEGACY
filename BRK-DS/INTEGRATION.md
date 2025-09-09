# BRK-DS Integration Guide

## Quick Start

### 1. Using BRK-DS in Your Component Requirements

Copy the relevant requirements from BRK-DS domains into your component's `requirements/requirements.yaml` file:

```bash
# Example: Adding Basic Regulation requirements to a component
cp BRK-DS/BASIC/requirements.yaml \
   C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/\
   AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-53-FUSELAGE/\
   requirements/brk-basic-requirements.yaml
```

### 2. Mapping to DET Evidence Patterns

Update your DET emissions to include regulatory compliance:

```json
{
  "det_id": "DET:CAD:AAA:53-10:req_baseline:V1",
  "compliance_baseline": {
    "brk_requirements": ["BRK-BASIC-001", "BRK-BASIC-002"],
    "regulatory_source": "Basic Regulation (EU) 2018/1139",
    "evidence_attachments": ["compliance-matrix.csv", "legal-basis.pdf"]
  }
}
```

### 3. Integration with Compliance Matrix

Create or update your `compliance/standards.yaml` file:

```yaml
standards:
  - id: "EU-2018-1139"
    org: "EU"
    title: "Basic Regulation"
    clause: "Article 4"
    applicability: "All aviation products"
    level: "MUST"
    verification: ["Process", "Inspection"]
    brk_requirements: ["BRK-BASIC-001", "BRK-BASIC-002"]
    det_pattern: "DET:*:*:*:req_baseline:V*"
```

## Domain Selection Guide

### By Aircraft Type
- **Large Aircraft (CS-25)**: GOV, BASIC, IA, CS, CAW, OPS
- **Rotorcraft (CS-27/29)**: GOV, BASIC, IA, CS, CAW, OPS
- **UAS Operations**: GOV, BASIC, UAS, IS, OPS

### By Organisation Type
- **Design Organisation**: GOV, BASIC, IA, CS, IS
- **Production Organisation**: GOV, BASIC, CAW, IS  
- **Maintenance Organisation**: GOV, CAW, IS
- **Air Operator**: GOV, OPS, FCL, IS

### By Development Phase
- **Early Design**: GOV, BASIC, IA, CS
- **Certification**: GOV, IA, CS, CAW
- **Operations**: GOV, OPS, CAW, IS
- **Sustainment**: GOV, CAW, IS

## Advanced Integration

### TRACES Framework Integration
Link BRK-DS requirements to TRACES for bidirectional traceability:

```yaml
# In your trace.yaml file
upstream_refs:
  - source: "BRK-BASIC-001"
    type: "regulatory_requirement"
    evidence: "DET:CAD:AAA:53-10:req_baseline:V1"

downstream_refs:
  - target: "CE-CAD-Q100-AAA-ATA-53-FUSELAGE"
    type: "component_implementation"
    verification: "Analysis"
```

### CADET Circular Assurance Integration
Map regulatory requirements to sustainability metrics:

```yaml
# In your cadet.yaml file
regulatory_compliance:
  sustainability_impact: "BRK-IS-001"  # Info security reduces environmental impact
  circular_metrics:
    - requirement: "BRK-CAW-001"
      metric: "component_reuse_rate"
      target: ">80%"
```

## Compliance Matrix Template

Use this template to create a comprehensive compliance matrix:

| Domain | Requirement ID | Regulation | MoC | Evidence File | Status | Owner | Review Date |
|---------|---------------|------------|-----|---------------|--------|-------|-------------|
| GOV | BRK-GOV-001 | EU 2018/1139 | Process | compliance-baseline.xlsx | DONE | compliance-lead | 2025-Q2 |
| BASIC | BRK-BASIC-001 | EU 2018/1139 Art.4 | Inspection | scope-definition.pdf | DONE | regulatory-affairs | 2025-Q1 |

## Automation Scripts

### Requirements Sync Script
```bash
#!/bin/bash
# sync-brk-requirements.sh
# Automatically sync BRK-DS updates to component requirements

for domain in GOV BASIC IA CS CAW OPS IS UAS; do
    if [ -f "BRK-DS/${domain}/requirements.yaml" ]; then
        echo "Syncing ${domain} requirements..."
        # Add your component-specific sync logic here
    fi
done
```

### DET Integration Script
```python
#!/usr/bin/env python3
# emit-brk-det.py
# Emit DET evidence for BRK-DS compliance

import yaml
import json
from datetime import datetime

def emit_brk_det(component_path, brk_requirements):
    det_packet = {
        "det_id": f"DET:CAD:{component_path}:req_baseline:V1",
        "ts": datetime.now().isoformat() + "Z",
        "compliance_evidence": {
            "brk_requirements": brk_requirements,
            "status": "COMPLIANT",
            "evidence_date": datetime.now().isoformat() + "Z"
        }
    }
    # Emit to DET blockchain
    return det_packet
```

## Validation Checklist

Before submitting PR with BRK-DS integration:

- [ ] Requirements copied to appropriate component directories
- [ ] DET patterns updated with regulatory compliance evidence
- [ ] Compliance matrix updated with BRK requirement mappings
- [ ] TRACES linkage established for bidirectional traceability
- [ ] CADET integration completed for circular assurance
- [ ] YAML files validate with `yamllint -s .`
- [ ] All requirements have appropriate CE/CC/CI links
- [ ] Owner and reviewer assigned for each requirement
- [ ] Status field populated (draft/baselined)

## Support

For questions about BRK-DS integration:
- Technical: `compliance-lead@aqua-os`
- Regulatory: `regulatory-affairs@aqua-os`
- DET Integration: `det-support@aqua-os`