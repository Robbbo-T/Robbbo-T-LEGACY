---
applyTo:
  - "**/analysis/**"
  - "**/design-data/**"
---

## CAE rules
- Store solver decks, BCs, meshes, seeds, and results under `analysis/` or `design-data/`.
- Record reproducibility: `meshQ`, random `seed`, solver version, major params.
- Emit DET on runs:
  - `DET:CAE:<MIC>:<SNS>:solver_run:V<rev>` with `inputs`, `processing{tool,params}`, `outputs{margins,units}`, `refs{ce,ci}`.
- Large binaries: do not commit; keep summaries (CSV/JSON) and link in DET attachments if needed.