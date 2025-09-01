# UTCS-BLOCKCHAIN — Unified Traceability Criteria Specification

**Hierarchy**: UTCS-BLOCKCHAIN → **CADET** (assurance) → **DET** (evidence) → **TRACES** (traceability) → **DOMAINS** (15 domains × 7 pillars).

**DET ID**: `DET:<CAX>:<DOMAIN>:<SNS>:<activity>:<version>`
Example: `DET:CAD:AAA:52-10:design:V3` (Design, Doors 52-10).

**Security**: SHA-256 hashing + Ed25519 signatures. Each DET packet links to **`previous_hash`** (append-only chain).

**ATA SNS**: Use `CC-SS[-SS]` from **ATA iSpec 2200** for compliance mapping.

**S1000D**: Documentation lives under **CAS** only: `.../CAS-SUSTAINMENT/**/S1000D/`. Elsewhere: **downstream DMC pointers** only.

---

## Overview

Complete **Computer-Aided Excellence (CAX)** framework architecture with **TeknIA Tokens (TekTok)** integration for **proof-of-innovation** tokenomics and optional **ASI** (Autonomous Sustainable Intelligence) scoring. Evidence is produced as **DET** packets, aggregated in **CADET** KPI cuts, and traced to requirements via **TRACES**.

---

## Hierarchical Chain Structure

1. **UTCS-BLOCKCHAIN** — Root directory
2. **CADET** — Evolutionary assurance ledger (circularity KPIs, monthly cuts)
3. **DET** — Cryptographic evidence packets (append-only)
4. **TRACES** — Certification traceability (requirements ↔ artifacts)
5. **DOMAINS** — Technical implementation (15 domains × 7 pillars)

---

## Registry Nodes Generated

* **Total Domains**: 15
* **Total CAX Pillars**: 7
* **Total Registry Nodes**: **105** (15 × 7)

---

## DET Structure Pattern

```
UTCS-BLOCKCHAIN/DET/<CAX>/<DOMAIN>/<SNS>/<activity>/<version>/
├── manifest.yaml         # DET metadata, owner, compliance hints
├── det_packet.json       # Evidence packet (inputs / processing / outputs)
├── signature.ed25519     # Ed25519 signature over det_packet.json
├── previous_hash         # SHA256 of previous packet in this namespace
├── trace.yaml            # Requirement ↔ artifact links (TRACES)
└── cadet.yaml            # Circularity linkage (CADET KPI references)
```

**Versioning**: `V1, V2, …` are **monotonic** per `<CAX>/<DOMAIN>/<SNS>/<activity>`.
**Continuity**: `previous_hash` must equal the **sha256** of the previous `det_packet.json` in the same namespace.

---

## Minimal DET Template (copy/paste)

**`UTCS-BLOCKCHAIN/DET/CAD/AAA/52-10/design/V3/det_packet.json`**

```json
{
  "det_id": "DET:CAD:AAA:52-10:design:V3",
  "ts": "2025-09-01T12:00:00Z",
  "refs": { "ce": "CE-CAD-Q100-AAA-ATA-52-DOORS" },
  "inputs": { "cad_files": ["door_assy.step"] },
  "processing": { "tool": "CAD@2025.0", "params": { "qa": true } },
  "outputs": {
    "units": "mm,kg",
    "metrics": { "mass_kg": 125.5, "cg_x_mm": 15120 }
  },
  "hash": "SHA256_PLACEHOLDER",
  "sig": { "alg": "Ed25519", "by": "wb-bot@aqua" }
}
```

### Computing `previous_hash` (explicit)

`previous_hash` must equal the **SHA-256 of the prior** `det_packet.json` in the same `<CAX>/<DOMAIN>/<SNS>/<activity>` namespace.

```bash
# Example: writing previous_hash for V3 from the V2 packet
# Linux:
echo -n "$(cat .../V2/det_packet.json)" | sha256sum | awk '{print $1}' > .../V3/previous_hash
# macOS:
shasum -a 256 .../V2/det_packet.json | awk '{print $1}' > .../V3/previous_hash
```

You can also run the helper: `python UTCS-BLOCKCHAIN/DET/tools/link_previous_hash.py`.

---

## Example DET ID Pattern

```
DET:CAD:AAA:52-10:design:V3
```

---

## Domains (15 total)

* **AAA** — ARCHITECTURES_AIRFRAMES_AERODYNAMICS
* **AAP** — AIRPORTS_ADAPTATIONS
* **CCC** — COCKPIT_CABIN_CARGO_SYSTEMS
* **CQH** — CRYOGENICS_QUANTUM_INTERFACES_HYDROGEN_CELLS
* **DDD** — DEFENCE_CYBERSECURITY_SAFETY
* **EDI** — ELECTRONICS_DIGITAL_INSTRUMENTS
* **EEE** — ENVIRONMENTAL_REMEDIATION_CIRCULARITY
* **EER** — ENERGY_AND_RENEWABLE
* **IIF** — INFRASTRUCTURES_AND_FACILITIES_VALUE_CHAINS
* **IIS** — INTELLIGENT_SYSTEMS_ONBOARD_AI
* **LCC** — LINKS_COMMUNICATIONS_CONTROL_IoT
* **LIB** — LOGISTICS_INTEGRATED_BLOCKCHAIN
* **MMM** — MECHANICAL_MATERIAL_MONITORING
* **OOO** — OPERATING_SYSTEMS_NAVIGATION_HPC
* **PPP** — PROPULSION_AND_FUEL

---

## CAX Pillars (7 total)

* **CAD** — Computer-Aided Design
* **CAE** — Computer-Aided Engineering
* **CAM** — Computer-Aided Manufacturing
* **CAT** — Computer-Aided Testing
* **CAI** — Computer-Aided Integration
* **CAS** — Computer-Aided Sustainment
* **CAO** — Computer-Aided Organization

---

## Provenance (affiliates allowlist)

Only artifacts from **official, affiliated repositories** are ranked/scored by default.
Set allowlist in: `UTCS-BLOCKCHAIN/CADET/affiliates.yaml` (orgs, repos, optional signer IDs).
Emit repository URL inside `det_packet.json` at `inputs.provenance.git_url` for on-chain provenance.

**Example — `UTCS-BLOCKCHAIN/CADET/affiliates.yaml`**
```yaml
version: 1
orgs:
  - name: Robbbo-T
    repos:
      - url: "https://github.com/Robbbo-T/Robbbo-T"
# Optional signer allowlist (strengthens provenance checks)
signers:
  - "wb-bot@aqua"
  - "test-lab@ddd"
rules:
  require_repo_match: true
  require_signer_match: false
  require_signed_commits: false
  repo_evidence_field: "inputs.provenance.git_url"
```

Emit repository provenance inside each DET at `inputs.provenance.git_url`.

---

## Quick Start (emit & validate)

```bash
# 0) Create the namespace if needed
mkdir -p UTCS-BLOCKCHAIN/DET/CAD/AAA/52-10/design/V3/

# 1) Create a new DET packet (fill fields, sign, hash)
$EDITOR UTCS-BLOCKCHAIN/DET/CAD/AAA/52-10/design/V3/det_packet.json

# 2) Link previous_hash (sha256 of the **prior** det_packet.json in this namespace)
# Linux:
echo -n "$(cat UTCS-BLOCKCHAIN/DET/CAD/AAA/52-10/design/V2/det_packet.json)" | sha256sum | awk '{print $1}' \
  > UTCS-BLOCKCHAIN/DET/CAD/AAA/52-10/design/V3/previous_hash
# macOS:
shasum -a 256 UTCS-BLOCKCHAIN/DET/CAD/AAA/52-10/design/V2/det_packet.json | awk '{print $1}' \
  > UTCS-BLOCKCHAIN/DET/CAD/AAA/52-10/design/V3/previous_hash

# (Optional) helper to link all previous_hash files in one go:
python UTCS-BLOCKCHAIN/DET/tools/link_previous_hash.py

# 3) Lint & validate (schema + chain)
pip install pyyaml jsonschema yamllint
yamllint -s .
python validate_utcs_blockchain.py
```

**If validation fails**, you'll see targeted errors, for example:
* `ERROR: Missing required field 'outputs.units'` → add `outputs.units` (SI units) to the JSON.
* `ERROR: Hash mismatch at UTCS-BLOCKCHAIN/DET/CAD/AAA/52-10/design/V3` → recompute `previous_hash` from **V2/det_packet.json** and re-save it in **V3/previous_hash**.

**PR Gate**: CI runs schema + chain checks (`.github/workflows/utcs-validate.yml`).
**TRACES**: map requirements to DET in `UTCS-BLOCKCHAIN/TRACES/*.trace.yaml`.
**CADET**: publish monthly KPI cuts in `UTCS-BLOCKCHAIN/CADET/kpis/<YYYY-MM>.yaml`.

### Common validation failures (and quick fixes)

- **Schema**: `outputs.units` missing → add SI units (e.g., `"mm,kg"`).  
- **Chain**: `previous_hash` mismatch → recompute from the prior `det_packet.json`.  
- **Provenance**: not in allowlist → set `inputs.provenance.git_url` to an affiliated repo, or add the repo to `affiliates.yaml`.  
- **Signature**: `sig.alg` not `Ed25519` → sign with Ed25519 (and keep `hash` = sha256 of the JSON).

---

## Implementation Summary

* ✅ 105 DET registry nodes created
* ✅ Complete CAX framework architecture deployed
* ✅ Hierarchical blockchain structure: **CADET → DET → TRACES → DOMAINS**
* ✅ SHA-256 + Ed25519 cryptographic security
* ✅ ATA SNS compliance mapping
* ✅ Bidirectional traceability framework
* ✅ CADET circular assurance integration
* 🔁 Optional: **ASI** sustainability/decision-quality scoring & **TekTok** proof-of-innovation oracles (non-gating)

---

*Generated and maintained by the UTCS-BLOCKCHAIN implementation scripts.*
```

