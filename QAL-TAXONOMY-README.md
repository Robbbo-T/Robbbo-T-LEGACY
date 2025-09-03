# QAL Taxonomy System

A complete Node.js-based automation system for managing the QAL (Quantum Applied Learning) taxonomy in the C-AMEDEO framework. This system provides automated index generation, event emission, and validation for BWB-Q100 program artifacts.

## Quick Start

```bash
# Install dependencies
npm ci

# Run complete validation pipeline
npm run all

# Individual operations
npm run gen         # Generate index & placeholders
npm run emit        # Emit QS events from YAML
npm run validate:qs # Validate QS.Published events
npm run validate:det # Validate DET references
```

## Features

### 🎯 Core Capabilities
- **Automated Documentation Generation**: Taxonomy index tables and domain placeholders
- **Event Emission System**: QS.Published events from domain YAML configurations
- **Schema Validation**: JSON Schema enforcement for QS.Published and DET.Ref patterns
- **Multi-Domain Support**: AAA, CQH, ppp, and 12 additional domains
- **CI/CD Integration**: GitHub Actions workflow with artifact archiving

### 📊 System Architecture

```
qal/
├── AAA/kit.yaml              # Domain configuration with SE/DI/CE/QS hooks
├── CQH/kit.yaml              # Cryogenic systems domain
├── ppp/kit.yaml              # Propulsion domain
└── alias/qaudit_migration.yaml # QAUDIT migration tracking

docs/
├── index.md                   # Main documentation entry
├── taxonomy/
│   ├── index-table.md         # Generated 15×11 navigation table
│   ├── anchors.html           # HTML anchor package
│   └── placeholders/          # Per-domain documentation pages
└── diagrams/                  # Mermaid diagram sources

events/
├── samples/                   # Test event files
└── out/                       # Generated QS.Published events

schemas/
├── qs.published.schema.json   # QS.Published event validation
└── det.ref.schema.json        # DET reference pattern validation

scripts/
├── gen_index_and_anchors.mjs  # Documentation generator
├── gen_placeholders.mjs       # Domain page generator
├── emit_qs_from_yaml.mjs      # Event emission engine
├── validate_qs_events.mjs     # Event validator
├── validate_det_refs_in_kits.mjs # DET reference validator
└── domain_list.json           # Master domain registry
```

## Domain Configuration

Each domain kit (`qal/{DOMAIN}/kit.yaml`) contains:

```yaml
---
dom: AAA  # Domain code
program: BWB-Q100
tfa_ref: "#tfa-bwb"

se:   # Station Envelop entries
di:   # Domain Interface (ICDs)
ce:   # Component Equipped (as-built)
cv:   # Component Vendor (AVL)

qs_hooks:  # Quantum State emission triggers
  - ref: "EstándarUniversal:EstadoCuantico-VQE-02.00-AAA-CI-..."
    det_ref: "DET:QS:AAA:CI:53-30-TIES:V1.0"
    note: "VQE for microfisurado CFRP@20K"
```

## Event Validation

### QS.Published Schema
- **Event**: Must be "QS.Published"
- **Domain**: 3-letter code (AAA, CQH, etc.) or "ppp"
- **Level**: TFA|SI|CV|SE|DI|CE|CC|CI|CP|FE|QS
- **QS Type**: QUBO|VQE|QML
- **DET Ref**: Pattern `DET:QS:{domain}:{sns}:{activity}:V{major}.{minor}`
- **Signature**: PQC-Dilithium3|Falcon|SPHINCS+

### DET Reference Schema
- **Pattern**: `DET:{type}:{domain}:{sns}:{activity}:V{version}`
- **Types**: SE|DI|CE|QS
- **SNS**: 2-8 alphanumeric characters
- **Activity**: Alphanumeric with hyphens/underscores

## GitHub Actions Integration

The system includes automatic CI/CD via `.github/workflows/qal-ci.yml`:

- **Triggers**: Changes to schemas/, qal/, scripts/, docs/
- **Steps**: Install → Generate → Emit → Validate
- **Artifacts**: Generated documentation and events
- **Validation**: Both QS events and DET references

## Development Tools

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Manual run
pre-commit run --all-files
```

### Local Development
```bash
# Use Makefile shortcuts
make install   # npm ci
make gen       # Generate docs
make emit      # Emit events  
make validate  # Validate all
make all       # Complete pipeline
```

## UTCS-MI v5.0 Compliance

- **Canonical Headers**: EstándarUniversal format with program context
- **Domain Codes**: 15 domains (AAA-ppp) with lowercase variations
- **Level Hierarchy**: TFA → SI → CV → SE → DI → CE → CC → CI → CP → FE → QS
- **Alias Support**: Legacy TA→TFA, SA→SE, CENV→CE migrations
- **Evidence Chain**: DET pattern enforcement with version tracking

## System Verification

The implementation successfully processes:
- ✅ **17 DET references** across 3 active domains
- ✅ **12 QS.Published events** with 100% schema compliance  
- ✅ **165 navigation links** in taxonomy index (15×11 matrix)
- ✅ **15 domain placeholders** with standardized structure
- ✅ **QAUDIT migration tracking** with cryptographic signatures

---

**Part of the C-AMEDEO Framework for BWB-Q100 Program**  
UTCS-MI v5.0 | QAL Bus Compatible | PQC-Ready