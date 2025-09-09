# DOMAINS — Evidence Index (thin)

This directory is a **navigation index** for the 15 technical domains across all **CAX pillars**.  
**Engineering source of truth lives in C-AMEDEO.** Here we only reference **evidence** (DET), **traceability** (TRACES), and **circularity KPIs** (CADET).

---

## What lives here (and what does not)

- ✅ **Thin indexes** per domain/pillar pointing to:
  - **DET** nodes: `UTCS-BLOCKCHAIN/DET/<CAX>/<DOMAIN>/<SNS>/<activity>/<version>/`
  - **TRACES** records: `UTCS-BLOCKCHAIN/TRACES/**.trace.yaml`
  - **CADET** KPI cuts: `UTCS-BLOCKCHAIN/CADET/kpis/<YYYY-MM>.yaml`
  - **alias.yml** with canonical engineering path and DET namespaces
- ❌ No EBOM/MBOM, long requirements, or heavy design text (keep those in **C-AMEDEO**)
- ❌ No S1000D except under **CAS-SUSTAINMENT/** (downstream only)

> **DET ID rule:** `DET:<CAX>:<DOMAIN>:<SNS>:<activity>:<version>`  
> Example: `DET:CAD:AAA:52-10:design:V3`

---

## Domains (codes → names)

- **AAA** — ARCHITECTURES_AIRFRAMES_AERODYNAMICS  
- **AAP** — AIRPORTS_ADAPTATIONS  
- **CCC** — COCKPIT_CABIN_CARGO_SYSTEMS  
- **CQH** — CRYOGENICS_QUANTUM_INTERFACES_HYDROGEN_CELLS  
- **DDD** — DEFENCE_CYBERSECURITY_SAFETY  
- **EDI** — ELECTRONICS_DIGITAL_INSTRUMENTS  
- **EEE** — ENVIRONMENTAL_REMEDIATION_CIRCULARITY  
- **EER** — ENERGY_AND_RENEWABLE  
- **IIF** — INFRASTRUCTURES_AND_FACILITIES_VALUE_CHAINS  
- **IIS** — INTELLIGENT_SYSTEMS_ONBOARD_AI  
- **LCC** — LINKS_COMMUNICATIONS_CONTROL_IoT  
- **LIB** — LOGISTICS_INTEGRATED_BLOCKCHAIN  
- **MMM** — MECHANICAL_MATERIAL_MONITORING  
- **OOO** — OPERATING_SYSTEMS_NAVIGATION_HPC  
- **PPP** — PROPULSION_AND_FUEL

Each domain contains **7 pillars**: **CAD, CAE, CAM, CAT, CAI, CAS, CAO**.  
Inside each pillar folder you’ll find a **thin README** (evidence index) and an optional `alias.yml`.

---

## Canonical engineering (C-AMEDEO)

Keep engineering content in:
```

C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/\<CAX\_PILLAR>/H2-BWB-Q100-CONF0000/<DOMAIN-NAME>/

```
Example (AAA CAD):
```

C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES\_AIRFRAMES\_AERODYNAMICS/

```

---

## Evidence locations (repeatable pattern)

- **DET** evidence (append-only, sha256 + Ed25519):
```

UTCS-BLOCKCHAIN/DET/<CAX>/<DOMAIN>/<SNS>/<activity>/<version>/
├─ det\_packet.json
├─ signature.ed25519
├─ previous\_hash
├─ trace.yaml
└─ cadet.yaml

```
- **TRACES** (bidirectional): `UTCS-BLOCKCHAIN/TRACES/**.trace.yaml`  
- **CADET** KPIs (monthly): `UTCS-BLOCKCHAIN/CADET/kpis/<YYYY-MM>.yaml`

---

## Link policy (no duplication)

- Make **Markdown links** to the canonical **C-AMEDEO** CE/CC/CI folders when needed.
- **Do not** paste EBOM/MBOM tables, long requirements, or large narratives here.
- Keep files **English-only**.

---

## S1000D policy

S1000D artifacts are allowed **only** under:
```

C-AMEDEO-FRAMEWORK/<FLOW>/CAS-SUSTAINMENT/\*\*/S1000D/

```
Everywhere else, reference downstream **DMC** pointers.

---

## Quick start for a new evidence slice

1. Put the engineering in **C-AMEDEO** (CE/CC/CI/CP).  
2. Emit **DET** packet in `UTCS-BLOCKCHAIN/DET/<CAX>/<DOMAIN>/<SNS>/<activity>/<version>/`.  
3. Create **TRACES** record linking requirement(s) ↔ `det_id`.  
4. Update the relevant domain/pillar **thin README** with links (keep it short).  
5. If KPIs changed, update the monthly **CADET** cut.

---
```

