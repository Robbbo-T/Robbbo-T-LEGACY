---
applyTo: "**/compliance/*.yaml"
---

## Compliance mapping rules
- `standards.yaml` must include: `version`, `applies_to{cax,mic,sns,id}`, and `standards[]` with `id, org, title, clause, applicability, level, verification`.
- Map **DET** patterns per clause; do not commit binaries.
- Use **DAL-x** for criticality in PBS; never "CAT-A".
- S1000D stays **downstream**; allow only `downstream.dmc` pointers here.
- Add `meta{owner,reviewer,last_updated,change_ref}` for audit tracking.