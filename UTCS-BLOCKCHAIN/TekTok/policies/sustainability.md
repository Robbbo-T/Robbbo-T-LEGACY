# Sustainability Policy — TeknIA Tokens (TekTok)

**Path:** `UTCS-BLOCKCHAIN/TekTok/policies/sustainability.md`  
**Scope:** Rules for allocating the **Sustainability Fund** and proving impact with **DET/CADET** evidence.

---

## 1) Purpose

Accelerate verifiable environmental impact across the C-AMEDEO ecosystem by funding initiatives that demonstrably:
- reduce **CO₂** and **energy** footprints,
- increase **Reuse%** (circularity),
- extend asset **life**,
- and reduce technical-financial **risk** (ΔCVaR).

All claims MUST be backed by **DET** evidence and summarized through **CADET KPI cuts**.

---

## 2) Funding rule

- **Allocation:** **10% of every mint** → **Sustainability Fund** (TKTK).  
- **Origin:** Weekly mints performed by `TekTokMonetaryPolicy` (based on PoI & Recovery oracles).  
- **Destination:** Grants to projects meeting the eligibility and evidence rules herein.

**Reference events (must be emitted as DET):**
- `DET:TOK:EMIT:*:*:mint_poi:V*` — mint batch recorded
- `DET:TOK:GRANT:*:*:award:V*` — grant award (treasury → grantee)
- `DET:TOK:GRANT:*:*:milestone:V*` — milestone release
- `DET:TOK:TREAS:*:*:reconcile:V*` — fund reconciliation

---

## 3) Eligibility

A proposal is **eligible** if it:
1. Targets at least **one** CADET KPI: **CO₂ saved**, **Energy saved**, **Reuse%**, **Life extension**, **Risk reduction (ΔCVaR)**.
2. Defines **measurable baselines**, methods, and SI units.
3. Commits to **DET** emission for all material actions (design/analysis/test/installation/sustainment).
4. Publishes impact in the monthly **CADET KPI cut**.
5. Accepts **audit** of data and methodology.

**Ineligible:** purely narrative reports, unverifiable offsets, opaque data, duplication of previously funded effort.

---

## 4) Prioritization (scoring)

Projects are ranked by a **Sustainability Score** computed from **CADET** deltas within the funding window:

```

score = w\_CO2  · normalize(CO2\_saved\_kg)
\+ w\_EN   · normalize(energy\_saved\_kwh)
\+ w\_RE   · reuse\_percent
\+ w\_LIFE · normalize(life\_extension\_months)
\+ w\_RISK · normalize(delta\_cvar)

````

**Default weights (tunable by TekDAO):**
- `w_CO2 = 0.40`, `w_EN = 0.15`, `w_RE = 0.25`, `w_LIFE = 0.15`, `w_RISK = 0.05`

**Normalization (defaults):**
- `normalize(CO2_saved_kg)   = CO2_saved_kg / 10_000`
- `normalize(energy_saved_kwh)= energy_saved_kwh / 100_000`
- `normalize(life_extension_months) = life_extension_months / 12`
- `reuse_percent` is used as % (0–100)
- `normalize(delta_cvar)` is model-dependent; use a signed fraction ∈ [−1, +1]

> All normalizers/weights live in `UTCS-BLOCKCHAIN/TekTok/tokenomics.yaml` for a single source of truth.

---

## 5) Evidence requirements (must-have)

- **DET packets** per activity (schemas under `DET/schemas/`):
  - `det_packet.json` with **SI units** and **refs.ce/refs.ci**
  - `signature.ed25519` over canonical JSON
  - `previous_hash` chaining
- **TRACES** linking each artifact to requirement(s) (`TRACES/.../*.trace.yaml`)
- **CADET KPI cut**: publish monthly results at  
  `UTCS-BLOCKCHAIN/CADET/kpis/<YYYY-MM>.yaml`

Example CADET entry:
```yaml
namespace: "DET:CAD:AAA"
cut: "2025-09"
kpis:
  reuse_percent: 41.8
  energy_saved_kwh: 38500
  co2_saved_kg: 1180
  life_extension_months: 12
  risk_reduction: 0.07
evidence:
  - "DET:CAD:AAA:53-10:design:V5"
  - "DET:CAE:AAA:53-10:solver_run:V3"
````

---

## 6) Grant lifecycle

1. **Submission** (`proposal.md` + `plan.yaml`) under the relevant domain pillar directory:

   * goals, scope, timelines, budget, risk, measurement plan, expected DET/CADET signals.
2. **Screening** (secretariat): eligibility + schema lint + duplicates check.
3. **Ranking** (automated): compute preliminary **score** from prior KPIs (if any) and projected deltas.
4. **Review & Vote** (TekDAO): discussion, optional interviews, final decision (timelock applies).
5. **Award**: `DET:TOK:GRANT:*:*:award:V1` plus on-chain transfer from treasury.
6. **Milestones**: each release requires **new DET** + **updated CADET** deltas; emit `DET:TOK:GRANT:*:*:milestone:V*`.
7. **Closeout**: impact report + final CADET cut; `DET:TOK:TREAS:*:*:reconcile:V*`.

---

## 7) Guardrails & anti-gaming

* **Outlier filter**: reject KPIs beyond `±3σ` unless independently replicated.
* **Min sources**: at least **2** independent DET sources for claims ≥ tier thresholds (set by DAO).
* **Double-count protection**: a DET packet can only support **one** funded claim for the same metric and window.
* **Energy/CO₂ factors**: document conversion factors and uncertainty; use conservative values approved by TekDAO.
* **Compliance**: when claims include **anti-corruption recoveries**, pass `kyc_aml_screening` and `sanctions_check`.

---

## 8) Transparency

* Publish monthly **KPI cuts** at `UTCS-BLOCKCHAIN/CADET/kpis/<YYYY-MM>.yaml`.
* Publish grant **award** and **milestone** DET events (paths under `DET:TOK:GRANT`).
* Keep a public ledger of:

  * proposals & awards,
  * KPI deltas,
  * treasury movements,
  * methodology changes.

---

## 9) Templates

**`proposal.md` (human-readable)**

```markdown
# Project Title
## Summary
## Expected KPIs (units & baselines)
## Methodology & measurement
## Timeline & budget
## Risks & mitigations
## Team & owner
```

**`plan.yaml` (machine-readable)**

```yaml
id: SUST-AAA-2025-09-001
owner: "org@example.com"
domain: AAA
pillar: CAD
period: "2025-10..2026-03"
targets:
  co2_saved_kg: 1500
  energy_saved_kwh: 50000
  reuse_percent: 45
  life_extension_months: 6
measurement:
  det_required: [design, solver_run, baseline_freeze]
  cadet_cut: "2025-10"
budget_tktk: 100000
milestones:
  - id: M1
    due: "2025-11-15"
    release_tktk: 30000
  - id: M2
    due: "2026-01-31"
    release_tktk: 30000
  - id: CLOSE
    due: "2026-03-31"
    release_tktk: 40000
```

---

## 10) Governance & changes

* Policy owner: **TekDAO** (timelock controller).
* Changes to weights/normalizers or eligibility require a DAO vote.
* Emergency pause available for fraud/security incidents.

---

## 11) Definitions

* **DET**: Digital Evidence Twin — signed, chained evidence packets.
* **CADET**: Circular Assurance — KPI aggregation with auditability.
* **Reuse%**: ratio of reused features/components at CI/EBOM/MBOM levels.
* **ΔCVaR**: reduction in tail risk from AMPEL360 decisions.

---

## 12) Version

* `sustainability.md` v1.1 — 2025-09-01
* Changelog: added DAO-tunable weights; clarified normalization and DET\:TOK events.

```
::contentReference[oaicite:0]{index=0}
```
