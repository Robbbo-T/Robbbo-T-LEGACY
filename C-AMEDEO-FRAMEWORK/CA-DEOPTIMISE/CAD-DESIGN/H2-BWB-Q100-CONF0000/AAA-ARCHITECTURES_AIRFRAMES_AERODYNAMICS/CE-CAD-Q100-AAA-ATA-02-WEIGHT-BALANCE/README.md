# **CE-CAD-Q100-AAA-ATA-02-WEIGHT-BALANCE**

**UniversalStandard:** TechnicalElement-Design-iSpec2200-ATA 02-WeightBalance-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-HybridGeneration-AIR-AmedeoPelliccia-deadbeef-RemainingUsefulLife

**Configuration Envelope (CE):** CE-CAD-Q100-AAA-ATA-02-WEIGHT-BALANCE
**ATA Chapter:** 02 — Weight & Balance
**OwnerDomain:** AAA (Architectures\_Airframes\_Aerodynamics)
**MIC/CONF:** Q100 / H2-BWB-Q100-CONF0000
**Scope:** **CAD → PBS → BOM** (documentation is **downstream**)

---

## 1) Overview

This Configuration Envelope implements **Weight & Balance** (ATA 02) for the hydrogen-powered BWB. It defines how **mass properties**, **CG envelopes**, and **loading schemes** are modeled, versioned, and mapped to **PBS → EBOM/MBOM**. **S1000D/iSpec** publication is generated **downstream** from these CAD/PBS/BOM sources.

---

## 2) Atomic Structure (CE → CC → CI → CP)

**Naming patterns (this CE):**

```
CE-<CAX>-<MIC>-<DOM>-ATA-02-<descriptor>
CE-CC-<CAX>-<MIC>-<DOM>-ATA-02-<SS>-<descriptor>
CE-CC-CI-<CAX>-<MIC>-<DOM>-ATA-02-<SS>-<SS>-<descriptor>
CE-CC-CI-CP-<CAX>-<MIC>-<DOM>-ATA-02-<SS>-<SS>-<descriptor>-PBS-<WBSID>
```

### Component Cells (CC)

* **02-10 MASS-PROPERTIES** → [CE-CC-CAD-Q100-AAA-ATA-02-10-MASS-PROPERTIES](./CC/CE-CC-CAD-Q100-AAA-ATA-02-10-MASS-PROPERTIES/)
* **02-20 CG-ENVELOPE** → [CE-CC-CAD-Q100-AAA-ATA-02-20-CG-ENVELOPE](./CC/CE-CC-CAD-Q100-AAA-ATA-02-20-CG-ENVELOPE/)
* **02-30 LOADING-SCHEMES** → [CE-CC-CAD-Q100-AAA-ATA-02-30-LOADING-SCHEMES](./CC/CE-CC-CAD-Q100-AAA-ATA-02-30-LOADING-SCHEMES/)
* **02-40 BALLAST-AND-COMPENSATION** → [CE-CC-CAD-Q100-AAA-ATA-02-40-BALLAST-AND-COMPENSATION](./CC/CE-CC-CAD-Q100-AAA-ATA-02-40-BALLAST-AND-COMPENSATION/)
* **02-90 COMPLIANCE-AND-REPORTS** → [CE-CC-CAD-Q100-AAA-ATA-02-90-COMPLIANCE-AND-REPORTS](./CC/CE-CC-CAD-Q100-AAA-ATA-02-90-COMPLIANCE-AND-REPORTS/)

### Representative Component Items (CI)

* **Mass properties master** → [CE-CC-CI-CAD-Q100-AAA-ATA-02-10-01-MASS-PROPS-MASTER](./CC/CE-CC-CAD-Q100-AAA-ATA-02-10-MASS-PROPERTIES/CI/CE-CC-CI-CAD-Q100-AAA-ATA-02-10-01-MASS-PROPS-MASTER/)
* **CG envelope definition** → [CE-CC-CI-CAD-Q100-AAA-ATA-02-20-01-CG-ENVELOPE-DEFINITION](./CC/CE-CC-CAD-Q100-AAA-ATA-02-20-CG-ENVELOPE/CI/CE-CC-CI-CAD-Q100-AAA-ATA-02-20-01-CG-ENVELOPE-DEFINITION/)
* **Standard loading cases** → [CE-CC-CI-CAD-Q100-AAA-ATA-02-30-01-STD-LOADING-CASES](./CC/CE-CC-CAD-Q100-AAA-ATA-02-30-LOADING-SCHEMES/CI/CE-CC-CI-CAD-Q100-AAA-ATA-02-30-01-STD-LOADING-CASES/)
* **Fuel distribution map** → [CE-CC-CI-CAD-Q100-AAA-ATA-02-30-02-FUEL-DISTRIBUTION-MAP](./CC/CE-CC-CAD-Q100-AAA-ATA-02-30-LOADING-SCHEMES/CI/CE-CC-CI-CAD-Q100-AAA-ATA-02-30-02-FUEL-DISTRIBUTION-MAP/)
* **Ballast kit** *(if applicable)* → [CE-CC-CI-CAD-Q100-AAA-ATA-02-40-01-BALLAST-KIT](./CC/CE-CC-CAD-Q100-AAA-ATA-02-40-BALLAST-AND-COMPENSATION/CI/CE-CC-CI-CAD-Q100-AAA-ATA-02-40-01-BALLAST-KIT/)
* **W\&B baseline report pack** → [CE-CC-CI-CAD-Q100-AAA-ATA-02-90-01-WB-BASELINE-REPORT-PACK](./CC/CE-CC-CAD-Q100-AAA-ATA-02-90-COMPLIANCE-AND-REPORTS/CI/CE-CC-CI-CAD-Q100-AAA-ATA-02-90-01-WB-BASELINE-REPORT-PACK/)

### Representative CP (PBS leaves)

* Mass-props parameters → under the CI's cp/…MASS-PROPS-PARAMS-PBS-Q100-02-10-01-0001/
* CG envelope curves → under the CI's cp/…CG-ENVELOPE-CURVES-PBS-Q100-02-20-01-0001/
* Loading case A → under the CI's cp/…STD-CASE-A-PBS-Q100-02-30-01-0001/
* Fuel map → under the CI's cp/…FUEL-MAP-PBS-Q100-02-30-02-0001/
* Ballast assembly → under the CI's cp/…BALLAST-ASSY-PBS-Q100-02-40-01-0001/
* Baseline reports → under the CI's cp/…WB-REPORTS-PBS-Q100-02-90-01-0001/

---

## 3) Folder shape (example)

```
CE-CAD-Q100-AAA-ATA-02-WEIGHT-BALANCE/
  CC/CE-CC-CAD-Q100-AAA-ATA-02-10-MASS-PROPERTIES/
    CI/CE-CC-CI-CAD-Q100-AAA-ATA-02-10-01-MASS-PROPS-MASTER/
      PBS.json · EBOM.yaml* · MBOM.yaml* · CADParameters.json · Effectivities.yaml · cad/
      cp/…MASS-PROPS-PARAMS-PBS-Q100-02-10-01-0001/
  CC/CE-CC-CAD-Q100-AAA-ATA-02-20-CG-ENVELOPE/
    CI/CE-CC-CI-CAD-Q100-AAA-ATA-02-20-01-CG-ENVELOPE-DEFINITION/
      design-data/{envelope_curves.csv, stations.json} · CADParameters.json · cp/…
  CC/CE-CC-CAD-Q100-AAA-ATA-02-30-LOADING-SCHEMES/
    CI/…-02-30-01-STD-LOADING-CASES/ {caseA.yaml, caseB.yaml, seatmap.png} · cp/…
    CI/…-02-30-02-FUEL-DISTRIBUTION-MAP/ {tanks_map.yaml, transfer_logic.yaml} · cp/…
  CC/CE-CC-CAD-Q100-AAA-ATA-02-40-BALLAST-AND-COMPENSATION/
    CI/…-02-40-01-BALLAST-KIT/ EBOM.yaml · MBOM.yaml · drawings/ · cp/…
  CC/CE-CC-CAD-Q100-AAA-ATA-02-90-COMPLIANCE-AND-REPORTS/
    CI/…-02-90-01-WB-BASELINE-REPORT-PACK/ baseline_report.json · pdf/ · cp/…
```

\* **EBOM/MBOM** are **N/A** for purely data-centric CIs (keep data in design-data/). Use EBOM/MBOM for physical items (e.g., ballast).

---

## 4) CAD → PBS → EBOM/MBOM

* **PBS.json** *(per CI)* — pbs_id, owner_domain, sns, ce_id/cc_id/ci_id, wbs_id.
* **EBOM.yaml** — physical assemblies only (PN, qty, material, join); **data CIs**: use design-data/.
* **MBOM.yaml** — only for physical builds (routing, workcenters, time, QA: FAI/SPC, kitlists).
* **CADParameters.json** — datums (PLN_XY/YZ/ZX), MASTER_SKELETON_PART, named parameters (e.g., GRID_SPACING_MM, PANEL_THICK_MM), ranges.
* **Effectivities.yaml** — CONF variants and applicability.
* **cad/** — native CAD (CATIA/Creo/SolidWorks/NX).

---

## 5) Interfaces & cross-links

* **ATA 06** — stations/MAC references (owner of dimensions).
* **ATA 08** — certified **weigh-in** ingestion (Leveling & Weighing).
* **ATA 28** — fuel tank geometry & transfer logic (loading influence).
* **ATA 34** — navigation frames/stations (if used as references).

---

## 6) DET events (evidence)

All activities emit **DET** packs:

```
DET:CAD:Q100:02:<activity>:V<rev>
```

**Examples**

* mass_props_update — Δweight (kg), ΔCG (mm/%MAC), author, assumptions.
* cg_envelope_check — PASS/FAIL, min margin (%MAC), attachments (CSV/JSON).
* loading_case_validate — Case A/B/C trims & CG within limits (true/false + deltas).
* fuel_map_sync — tanks map/transfer sync; refs to ATA 28 items.
* ballast_mbom_release — MBOM release; FAI/SPC passed (ballast only).
* wb_baseline_freeze — baseline pack frozen for compliance/audit.

> Minimum fields: det_id, ts, refs{ce, ci}, inputs, processing{tool,params}, outputs{units}, hash, sig.

---

## 7) Acceptance criteria

* **Correct atomization:** DI→CE→CC→CI→CP present; no orphan tiers.
* **ATA-anchored IDs:** CE/CC/CI/CP follow ATA CC-SS-SS where applicable.
* **CAD-first discipline:** EBOM/MBOM only for hardware; data goes to design-data/.
* **Traceability:** EBOM↔MBOM linkage (pn, kits); PBS/WBS IDs present.
* **Evidence:** DET packs exist for each meaningful change; units explicit (kg, mm, %MAC).
* **Aliases:** alias.yml with OwnerDomain AAA and CoDomains (e.g., OOO, PPP, EER).

---

## 8) Status

🚧 **Under Development** — part of **CA-DEOPTIMISE** (Forward Creation Flow)

---

### Quick links

* CC **02-10 MASS-PROPERTIES** → [CE-CC-CAD-Q100-AAA-ATA-02-10-MASS-PROPERTIES](./CC/CE-CC-CAD-Q100-AAA-ATA-02-10-MASS-PROPERTIES/)
* CI **Mass-props master** → [CE-CC-CI-CAD-Q100-AAA-ATA-02-10-01-MASS-PROPS-MASTER](./CC/CE-CC-CAD-Q100-AAA-ATA-02-10-MASS-PROPERTIES/CI/CE-CC-CI-CAD-Q100-AAA-ATA-02-10-01-MASS-PROPS-MASTER/)