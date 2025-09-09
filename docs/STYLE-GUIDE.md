# Style Guide (Guía de Estilo) — C-AMEDEO Framework

**UTCS-MI v5.0 Identifier**  
EstándarUniversal:Especificacion-Definicion-ARP4754A+DO178C+DO254+S1000D+CS25-00.00-StyleGuideForTechnicalDocumentation-0001-v1.0-Aerospace and Quantum United Agency-GeneracionHybrida-CROSS-Amedeo Pelliccia-f74d3e06-RestoDeVidaUtil

## Overview

This style guide establishes consistent formatting, language, and structural conventions for all technical documentation within the C-AMEDEO framework, supporting the BWB-Q100 program and UTCS-MI v5.0 compliance.

## Language Requirements

### Primary Language
- **English** is the primary language for all technical documentation
- All identifiers, technical specifications, and formal documentation must be in English
- Exception: User interface elements may be bilingual (English/Spanish) where appropriate

### Identifier Conventions
- Follow **UTCS-MI v5.0** 13-field identifier format
- Use descriptive CamelCase for programs/categories (no acronyms in UTCS-MI fields)
- Maintain **DI → CE → CC → CI → CP** hierarchy
- Include **ATA iSpec 2200 SNS** in technical identifiers

Example: `CE-CAD-Q100-AAA-ATA-52-DOORS`

## Document Structure

### Standard Headers
All documents must include:
```markdown
# Document Title

**UTCS-MI v5.0 Identifier**  
EstándarUniversal:[13-field-identifier]

## Overview
[Brief description of purpose and scope]
```

### Section Hierarchy
1. Use `#` for main title
2. Use `##` for major sections
3. Use `###` for subsections
4. Use `####` for detailed breakdowns
5. Maximum depth: 4 levels (`####`)

### Cross-References
- Make every DI/CE/CC/CI/CP item in lists a **Markdown link** (no backticks)
- Use relative paths for internal references
- Format: `[CE-CAD-Q100-AAA-ATA-52-DOORS](../path/to/document.md)`

## Content Guidelines

### Technical Specifications
- Include units for all numerical values
- Use SI units as primary (imperial in parentheses if needed)
- Maintain precision appropriate to context (e.g., `±0.1 mm` for manufacturing tolerances)

### DET References
- All major engineering changes must reference corresponding DET evidence
- Format: `DET:CAX:DOMAIN:SNS:activity:version`
- Example: `DET:CAD:AAA:52-10:design:V3`

### S1000D Integration
- S1000D artifacts are **downstream output** only
- Keep under `C-AMEDEO-FRAMEWORK/*/CAS-SUSTAINMENT/**/S1000D/`
- Use `downstream.dmc` pointers from engineering sources
- Never commit DMRL/DMC outside CAS pillar

## Formatting Standards

### Code Blocks
Use fenced code blocks with language specification:
```yaml
# Example YAML
component_id: "CE-CAD-Q100-AAA-ATA-52-DOORS"
status: "baselined"
```

### Tables
Use markdown tables with proper alignment:
| Component | Status | Owner | Last Updated |
|-----------|--------|-------|--------------|
| [CE-CAD-Q100-AAA-ATA-52-DOORS](link) | Baselined | Domain-AAA | 2024-01-15 |

### Lists
- Use `-` for unordered lists
- Use `1.` for ordered lists  
- Use `- [x]` for completed checklist items
- Use `- [ ]` for pending checklist items

### Emphasis
- Use **bold** for important terms and keywords
- Use *italics* for emphasis or foreign terms
- Use `inline code` for technical terms, filenames, and commands
- Use `> Blockquotes` for important notes or warnings

## File Naming Conventions

### General Rules
- Use kebab-case for file names: `style-guide.md`
- Include version in filename for versioned documents: `requirements-v1.2.yaml`
- Use descriptive names that indicate content and scope

### Document Types
- Requirements: `requirements.yaml`
- Specifications: `*-spec.md` or `*-srs.md`
- Procedures: `*-procedure.md`
- Templates: `*-template.md`
- S1000D Data Modules: Follow S1000D naming conventions

## Quality Assurance

### Required Checks
1. **YAML Lint**: All YAML files must pass `yamllint -s .`
2. **Markdown Links**: Run `markdown-link-check` on all `*.md` files
3. **Schema Validation**: Follow repository schemas where applicable
4. **UTCS-MI Compliance**: Verify 13-field identifier format

### Review Process
1. Self-review for style guide compliance
2. Automated CI checks (linting, schema validation)
3. Peer review focusing on technical accuracy
4. Final approval by domain owner

## Templates Reference

Standardized templates are available for:
- [Technical Requirements](templates/requirements-template.yaml)
- [Design Specifications](templates/design-spec-template.md)
- [Test Procedures](templates/test-procedure-template.md)
- [DET Evidence Packages](templates/det-template.json)
- [S1000D Data Modules](templates/s1000d-template.xml)

## Version Control

### Git Conventions
- Use conventional commits: `feat:`, `fix:`, `docs:`, `chore:`
- Include pillar tags: `[CAD]`, `[CAE]`, `[CAS]`, etc.
- Reference related issues/PRs in commit messages

### Document Versioning
- Use semantic versioning for major document releases
- Include version in UTCS-MI identifier
- Maintain changelog for significant updates
- Archive superseded versions appropriately

## Compliance Notes

- This style guide supports **ARP4754A**, **DO178C**, **DO254**, **S1000D**, and **CS25** compliance
- All documentation must maintain traceability to applicable regulations
- Use **DAL-x** for criticality classifications (never "CAT-A")
- Ensure proper effectivity management for configuration-controlled items

---

*This style guide is part of the C-AMEDEO framework for the AMPEL360-BWB-Q Program.*  
*For questions or clarifications, contact the Documentation Working Group.*