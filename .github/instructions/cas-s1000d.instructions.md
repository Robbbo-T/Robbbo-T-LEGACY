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