---
applyTo: "**/{EBOM,MBOM}.yaml"
---

## EBOM / MBOM rules
- EBOM lists **physical items** only; data artifacts go to `design-data/` (CSV/JSON + assumptions.md).
- MBOM includes `routing`, `workcenters`, `time_min`, QA gates (FAI/SPC), and `kits` when applicable.
- Keep `assembly_pn`, `revision`, `units`, `weight_kg` when known.
- Run YAML lint and any repo schemas before opening a PR.