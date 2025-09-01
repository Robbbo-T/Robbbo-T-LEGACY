---
applyTo:
  - "**/MBOM.yaml"
  - "**/process/**"
  - "**/routing*.yaml"
---

## CAM rules
- **MBOM.yaml** must include `routing{op,workcenter,process,time_min}`, QA gates (FAI/SPC), and `kits` when applicable.
- Keep process sheets under `process/` (machine-readable where possible).
- Emit DET for `mbom_change`, `fai`, `spc` with explicit **units** and `refs{ce,ci}`.
- Maintain EBOM↔MBOM linkage by `assembly_pn` and kit lists; do not duplicate EBOM content in MBOM.