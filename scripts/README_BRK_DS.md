# BRK DS Drop-in Bundle Generator

This script creates a complete Event Management System (EMS) drop-in bundle for AMEDEO/QAL integration.

## Usage

```bash
python3 scripts/create_brk_ds_dropin.py
```

The script will:
1. Create a complete bundle at `/mnt/data/BRK_DS_dropin/`
2. Generate a downloadable zip file at `/mnt/data/BRK_DS_dropin.zip`

## Bundle Contents

### Root Files
- **FAN1_MBOM.md**: Manufacturing Bill of Materials with ATA+S1000D structure
- **FAN1_SBOM.md**: Service Bill of Materials with FRU/Kit mappings
- **FAN1_CROSSWALK.md**: EBOM → MBOM → SBOM mapping table
- **FAN1_QAUDIT.yaml**: QAUDIT stub files for compliance tracking
- **CAM.MBOMReleased.json**: Sample CAM event for MBOM releases
- **CAS.SBOMReleased.json**: Sample CAS event for SBOM releases

### EMS Directory (`ems/`)
- **emit.mjs**: Event emission utility with schema validation
- **validate.mjs**: Event validation against JSON schemas
- **watch.mjs**: File system watcher for automatic event emission
- **schemas/**: JSON Schema files for all supported event types

### Samples Directory (`samples/`)
- **qs_payload.json**: Quantum Score event payload
- **mbom_payload.json**: MBOM release event payload
- **sbom_payload.json**: SBOM release event payload
- **compliance_payload.json**: Compliance rollup event payload

### Scripts Directory (`scripts/`)
- **gen_matrix.mjs**: Domain matrix generation utility

### Documentation Seeds (`docs/`)
- Sample MBOM/SBOM YAML files
- Example domain structure
- Alias files for QS event triggers

## Supported Event Types

- `QICOCA.QS.Published` - Quantum Score events
- `CAMPOS.CAM.MBOMReleased` - Manufacturing BOM releases
- `CAMPOS.CAS.SBOMReleased` - Service BOM releases  
- `CADEV.CAV.ComplianceRolledUp` - Compliance status updates

## Quick Start (Bundle Usage)

1. Extract bundle to your project directory
2. Install dependencies: `npm install`
3. Run tests: `npm test`
4. Start file watcher: `npm run ems:watch`

## Event Emission

```bash
# Emit a QS event
npm run ems:emit:qs

# Emit an MBOM release event
npm run ems:emit:mbom

# Emit an SBOM release event
npm run ems:emit:sbom

# Validate all events
npm run ems:validate
```

## Schema Validation

All events are automatically validated against their corresponding JSON schemas in `ems/schemas/`. The validation includes:

- Required field checks
- Format validation (e.g., UTCS-MI ID patterns)
- Domain and entity constraints
- DET reference pattern matching

## File Watching

The EMS watcher monitors:
- `docs/CAMPOS/CAM/MBOM/MBOM-*.yaml` → Emits `CAMPOS.CAM.MBOMReleased`
- `docs/CAMPOS/CAS/SBOM/SBOM-*.yaml` → Emits `CAMPOS.CAS.SBOMReleased`
- `docs/**/alias.yml` → Emits `QICOCA.QS.Published` (when QS det_ref found)

## CI/CD Integration

See `CI_snippet.yml` in the bundle for GitHub Actions integration example.

## Requirements

- Node.js >= 18.0.0
- npm or yarn package manager
- Access to `/mnt/data` directory (for script execution)

## Dependencies

The bundle includes these npm dependencies:
- `ajv` (JSON Schema validation)
- `ajv-formats` (Format validators)
- `chokidar` (File watching)
- `js-yaml` (YAML parsing)
- `glob` (File globbing)