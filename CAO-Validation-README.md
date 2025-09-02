# CAO Validation Infrastructure

This directory contains the complete JSON Schema validation system for CAO (Computer-Aided Organization) artifacts in the QAL ecosystem.

## Quick Start

### Validate CAO artifacts:
```bash
# Validate individual files
python scripts/validate_cao_artifacts.py QAL-Policy-Pack.json Budget-Vector.json

# Validate all JSON files in a directory
python scripts/validate_cao_artifacts.py governance/*.json

# Validate a UTCS-MI identifier
python scripts/validate_cao_artifacts.py --utcs-mi "EstándarUniversal:Politica-QAL-01.00-..."
```

## Schema Files

| Schema | Purpose | Validates |
|--------|---------|-----------|
| [`utcs_mi.schema.json`](schemas/utcs_mi.schema.json) | UTCS-MI v5.0 Universal Identifiers | `EstándarUniversal:...` IDs |
| [`cao_policy_pack.schema.json`](schemas/cao_policy_pack.schema.json) | QAL Policy Packs | Governance policies with UTCS-MI IDs |
| [`cao_budget_vector.schema.json`](schemas/cao_budget_vector.schema.json) | Budget Vectors | Financial allocations per domain/pillar |
| [`cao_risk_register.schema.json`](schemas/cao_risk_register.schema.json) | Risk Registers | CVaR-based risk management |
| [`cao_qal_bus_events.schema.json`](schemas/cao_qal_bus_events.schema.json) | QAL Bus Events | Event streams from CAO services |
| [`det_template.schema.json`](schemas/det_template.schema.json) | DET Templates | Digital Evidence Twin artifacts |

## Validation Script Features

- **Auto-detection**: Automatically identifies CAO artifact types
- **UTCS-MI validation**: Validates Universal Standard identifiers  
- **Detailed errors**: Provides precise validation error messages
- **Batch processing**: Validates multiple files efficiently
- **CI/CD ready**: Exit codes suitable for automated pipelines

## Example Artifacts

```json
// QAL Policy Pack
{
  "utcs_mi_id": "EstándarUniversal:Politica-QAL-01.00-PolicyPack-0007-v1.0-BlendedWingBodyProgramQ100-GeneracionHybrida-CROSS-Amedeo Pelliccia-b2c1f3a4d5e6f709-RestoDeVidaUtil",
  "package_name": "QAL Policy Pack — BWB-Q100", 
  "program": "BlendedWingBodyProgramQ100",
  "version": "1.0",
  "issued_by": "CAO-Compliance",
  "owner": "Amedeo Pelliccia",
  "effective_on": "2025-09-02",
  "det_ref": "DET:CAO:Policy:QAL-0007:V1.0",
  "policies": [...]
}
```

## Integration with CI/CD

Add to `.github/workflows/validation.yml`:
```yaml
- name: Validate CAO Artifacts
  run: |
    python scripts/validate_cao_artifacts.py $(find . -name "*.json" -path "*/governance/*" -o -path "*/resources/*" -o -path "*/compliance/*")
```

## Dashboard Wireframes

- [**Mermaid Wireframes**](CAO-Dashboard-Wireframe.md): Interactive diagrams showing CAO dashboard layout, navigation flow, and component specifications
- [**ASCII Wireframes**](CAO-Dashboard-ASCII.md): Text-based wireframes for environments without Mermaid support

The wireframes define:
- **KPI Dashboard**: Budget health, policy compliance, risk metrics, DET integrity
- **Policy Management**: QAL Policy Pack display and editing interface  
- **Budget Allocation**: FY2026Q2 budget vector with domain/pillar breakdown
- **Risk Register**: CVaR-based risk assessment and mitigation tracking
- **Mobile Layout**: Responsive design for mobile devices
- **Navigation Flow**: Complete user journey through CAO governance tools

## Repository Structure

```
├── schemas/                          # JSON Schema definitions
│   ├── utcs_mi.schema.json          # UTCS-MI identifier validation
│   ├── cao_policy_pack.schema.json  # Policy pack structure
│   ├── cao_budget_vector.schema.json # Budget allocation format
│   ├── cao_risk_register.schema.json # Risk management schema
│   ├── cao_qal_bus_events.schema.json # Event bus message format
│   └── det_template.schema.json     # Digital Evidence Twin format
├── scripts/
│   └── validate_cao_artifacts.py    # Main validation script
├── CAO-Dashboard-Wireframe.md       # Interactive dashboard wireframes
└── CAO-Dashboard-ASCII.md           # Text-based wireframes
```

## Requirements

- Python 3.7+
- `jsonschema` library (available in repo)
- `pathlib` (standard library)

## Exit Codes

- `0`: All artifacts valid
- `1`: Validation errors found  
- `2`: Invalid usage or missing files

## Contributing

When adding new CAO artifact types:
1. Create corresponding JSON schema in `schemas/`
2. Update `CAOValidator._detect_artifact_type()` 
3. Add schema loading in `_load_schemas()`
4. Update this README with examples

---

**Part of the C-AMEDEO QAL Ecosystem** | [Repository Guidelines](AGENTS.md) | [CAX Framework](CAX-FRAMEWORK-COMPLETE.md)