# Repository instructions for GitHub Copilot coding agent

## Project overview
This repository implements the **C-AMEDEO** ecosystem across all pillars (**CAX**):
**CAD, CAE, CAO, CAP, CAT, CAM, CAI, CAS, CAEV**. The agent MUST:
- Preserve the **DI → CE → CC → CI → CP** hierarchy and **ATA iSpec 2200 SNS** in identifiers.
- Keep all documentation **in English**; make every DI/CE/CC/CI/CP item in lists a **Markdown link** (no backticks).
- Treat **S1000D** as **downstream output** generated from engineering sources (never commit DMRL/DMC outside CAS).

## Pillar-specific rules
- **CAD**: Work **CAD → PBS → EBOM/MBOM**, **Feasibility analysis**, and **Requirements definition**.
  - **Requirements (`requirements/`)**: machine-readable `requirements.yaml` (id, text, source, driver, acceptance, verification, links{ce,cc,ci}, status, owner, last_updated). Emit DET on `req_add`, `req_update`, `req_baseline`.
  - **Feasibility / Trade studies (`feasibility/` or `trade-studies/`)**: keep `inputs/` (assumptions/constraints), `models/`, `results/` (CSV/JSON), and `decision.md`. Emit DET on `feasibility_run` / `trade_study` (with refs and units).
  - **EBOM/MBOM** only for physical CIs (data-centric CIs use `design-data/`). Emit DET on `save_model`, `ebom_change`, `mbom_change`.
- **CAE**: Keep decks/BCs/meshes/results under `analysis/` or `design-data/`. Record reproducibility (`meshQ`, seeds, solver version). Emit `solver_run` DET with inputs/params/units.
- **CAM**: Use **MBOM.yaml** for routing/resources/QA (FAI/SPC). Keep process specs in `process/`. Emit DET on FAI/SPC and MBOM releases.
- **CAI**: Keep **ICD** in machine-readable form; installation/test records under `integration/` or `installation-records/`. Emit `install_signoff` / `sys_test` DET.
- **CAT**: Source code, tests, build manifests. Generate **SBOM**; follow SLSA. Emit `sbom_generate` / CI build DET.
- **CAS (S1000D only)**: S1000D artifacts (DMRL/DMC/issue packages) **MUST** live under `C-AMEDEO-FRAMEWORK/<FLOW>/CAS-SUSTAINMENT/**/S1000D/`. S1000D is **forbidden** elsewhere; use `downstream.dmc` pointers only.

## Build, test, validate
- Install: `pip install -r .github/requirements.txt`
- Lint YAML: `yamllint -s .`
- Markdown links: run `markdown-link-check` on all `*.md`
- Schema/tests (if present): `make validate` / `make test`
- PR acceptance (agent MUST satisfy):
  1) CI green (build/lint/schema/tests)
  2) No S1000D artifacts outside CAS-SUSTAINMENT
  3) DET templates updated when EBOM/MBOM, analysis, integration, requirements, feasibility, or compliance files change
  4) ≥1 human reviewer approval

## Coding & content conventions
- **IDs**: `CE<CAX><MIC><DOM>-ATA<SNS><Descriptor>`, etc.
- **PBS.json** MUST include: `owner_domain`, `sns`, `ce_id`, `cc_id`, `ci_id`, `criticality: DAL-x`, `effectivity`.
- **EBOM/MBOM** only for physical items. Data CIs: keep artifacts in `design-data/` (CSV/JSON + assumptions).
- **DET** packs MUST include `refs.ce`, `refs.ci` and **units** for numeric outputs.
- Do not remove UTCS-MI `UniversalStandard:` headers.

## Pull requests
- Title: `feat:`, `fix:`, `docs:`, `chore:` (add pillar tag, e.g., `[CAD]`, if helpful).
- PR body includes "Validation notes" with build/lint/test/schema outputs and a brief DET summary.