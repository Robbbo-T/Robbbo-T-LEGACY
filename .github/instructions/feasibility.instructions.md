---
applyTo:
  - "**/feasibility/**"
  - "**/trade-studies/**"
---

## CAD — Feasibility / Trade-study rules
- Include: `inputs/` (assumptions.yaml, constraints.yaml), `models/` (scripts/notebooks),
  `results/` (CSV/JSON), and a succinct `decision.md` (options, criteria, outcome).
- Record AMPEL360 ties when relevant (e.g., MILP/CP-SAT enumeration, CVaR ranking).  
- Emit DET:
  - `DET:CAD:<MIC>:<SNS>:feasibility_run:V<rev>` or `DET:CAD:<MIC>:<SNS>:trade_study:V<rev>`
  - Include `refs{ce,ci}`, `processing{tool,params}`, `outputs{metrics,units}`, and attachments (CSV/JSON).
- No large binaries in Git; summarize numerics and link locations if needed.