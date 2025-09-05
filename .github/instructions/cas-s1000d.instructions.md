---
applyTo:
  - "**/S1000D/**"
  - "**/DMRL/**"
  - "**/DMC/**"
---

# CAS Sustainment — S1000D rules

## Location policy (MUST)
S1000D artifacts are allowed **only** under CAS:
```
C-AMEDEO-FRAMEWORK/*/CAS-SUSTAINMENT/**/S1000D/
```
They are **forbidden** anywhere else (CAD/CAE/CAO/CAP/CAT/CAM/CAI/CAEV).

## Content policy
- Keep generated packages and issue folders in `S1000D/`.
- Do not commit tool caches or binaries.
- Reference engineering sources (PBS/EBOM/MBOM/DET) via pointers, not duplicates.

## PR requirements
- PRs touching `S1000D/` must include:
  - Evidence references (DET ids) to upstream changes.
  - No new S1000D files outside the allowed CAS path.

<!-- BEGIN:S1000D-CAS-GOVERN -->
## S1000D Governance (CAS)

- Profile: `docs/S1000D-GOV/CAS/PROFILE-CAS.yaml`  
- Business Rules (BREX): `docs/S1000D-GOV/CAS/BREX-CAS.yaml`  
- Decision Points (BRDP): `docs/S1000D-GOV/CAS/BRDP-CAS.yaml`  
- CI Workflow: `.github/workflows/s1000d-cas-govern.yml`  
- Validator: `scripts/s1000d_brex_validate.mjs`

Scope:
- Governs DM‑ARCH/ICD/V&V and procedures relevant to CAS.
- Enforces: language/security, no binaries, DM code policy, applicability rules,
  and CE→…→QS traceability hooks.

<!-- END:S1000D-CAS-GOVERN -->