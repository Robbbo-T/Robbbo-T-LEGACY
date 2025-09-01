# TeknIA Tokens (TekTok)

Utility token whose issuance is tied to **verifiable technical value**.

* **Proof-of-Innovation (PoI)** from **DET/CADET** (Reuse %, Energy saved, CO₂ saved, Life-extension, Risk reduction ΔCVaR).
* **Anti-corruption recoveries** (net, audited) via a **Recovery Oracle**.
* Fair distribution: **innovators**, **ecosystem treasury** (grants), **sustainability fund**, and **vesting**.

On-chain components: **ERC-20 TekTok**, **MonetaryPolicy**, **TekDAO** (timelock), **TekCred** (SBT reputation), **RecoveryVault**.
Off-chain: oracles sign weekly feeds (Ed25519) and publish normalized scores.

---

## 0) Repository context

* Root: `UTCS-BLOCKCHAIN/`

  * Evidence: `DET/` (sha256 + Ed25519, append-only)
  * Traceability: `TRACES/` (req ↔ artifact)
  * Circular assurance: `CADET/` (KPIs per cut)
  * Domains: `DOMAINS/` (15 domains × 7 pillars)

**DET ID format:** `DET:<CAX>:<DOMAIN>:<SNS>:<activity>:<version>`
Example: `DET:CAD:AAA:52-10:design:V3`

---

## 1) Why TekTok (value→token)

TekTok converts **measured, signed progress** into token issuance:

1. **PoI feed:** weekly aggregation of DET/CADET KPIs (Reuse %, kWh, CO₂, months of life extension, ΔCVaR) → normalized score.
2. **Recoveries feed:** audited **anti-corruption recoveries** (net of legal costs) → normalized value.
3. **MonetaryPolicy** consumes both feeds and mints within weekly caps, splitting to **innovators/treasury/sustainability/vesting**.

All mints and grants emit **DET\:TOK** events and are fully traceable.

---

## 2) Architecture

```mermaid
flowchart LR
  subgraph Evidence
    D[DET packs<br/>sha256 + Ed25519] --> C[CADET KPI cuts]
  end
  O1[PoI Oracle<br/>(DET+CADET feed)] --> MP[MonetaryPolicy]
  O2[Recovery Oracle<br/>(audited recouped funds)] --> MP
  MP -->|mint| TKTK[TekTok ERC-20]
  MP -->|emit DET:TOK:EMIT| Evt[DET:TOK events]
  TKTK --> DAO[TekDAO (timelock)]
  TKTK --> SUST[Sustainability Fund]
  TKTK --> INNO[Innovators]
  TKTK --> TREAS[Treasury (grants)]
  Cred[TekCred SBT] --> DAO
```

---

## 3) Tokenomics (overview)

See **`tokenomics.yaml`** for full rules:

* **Supply cap** and **weekly cadence** with **cooldown** and **max weekly mint %**.
* **PoI KPIs**: Reuse %, Energy saved (kWh), CO₂ saved (kg), Life extension (months), Risk reduction (ΔCVaR).
* **Recoveries**: net, audited amounts (USD 18-decimals) with **legal/AML/sanctions** checks.
* **Anti-gaming**: multi-signer oracles, outlier rejection (σ filters), time-weighting, duplicate detection.
* **Allocations (PoI mints)**: 55% **Innovators**, 25% **Treasury**, 10% **Sustainability**, 10% **Vesting**.
* **Allocations (Recoveries)**: configurable split across **whistleblowers/investigators**, **adopting org**, **treasury**, **sustainability**, **anti-fraud R\&D**.

> Path: `UTCS-BLOCKCHAIN/TekTok/tokenomics.yaml`

---

## 4) Oracles

**PoI Oracle** (DET+CADET):
`UTCS-BLOCKCHAIN/TekTok/oracle/det-cadet-oracle.spec.yaml`

* Inputs: `DET/**/DET:*`, `CADET/kpis/**.yaml`
* Output: `TekTok/oracle/feed.json` (signed; carries normalized score)

**Recovery Oracle** (anti-corruption):
`UTCS-BLOCKCHAIN/TekTok/oracle/recovery-oracle.spec.yaml`

* Inputs: `DET:TOK:RECOVER:*:*:recovery_attest:V*`, auditor/legal attestations
* Output: `TekTok/oracle/recovery_feed.json` (signed; recoupedUSD 18-decimals)

**Off-chain aggregator** (weekly cron):
`UTCS-BLOCKCHAIN/TekTok/oracle/offchain-aggregator.md`

---

## 5) Contracts (Solidity)

* **`contracts/TekTok.sol`** — ERC-20 with `MINTER_ROLE`.
* **`contracts/TekTokMonetaryPolicy.sol`** — consumes PoI + Recovery feeds; applies caps; mints; emits DET\:TOK events (off-chain).
* **`contracts/TekDAO.sol`** — Timelock-based governance.
* **`contracts/TekCred.sol`** — SBT reputation (non-transferable).
* **`contracts/TokenVesting.sol`** — linear vesting utility.
* **Interfaces:** `interfaces/IDetCadetOracle.sol`, `interfaces/IRecoveryOracle.sol`.

> Note: Oracle signatures are **Ed25519 off-chain**. If you need on-chain verification, switch to **ECDSA** feeds or add a precompile/adapter.

---

## 6) Registry & DET\:TOK namespaces

**TekTok DET namespaces:**
`UTCS-BLOCKCHAIN/TekTok/registry/det-namespaces.yaml`

* `DET:TOK:EMIT:*` — token emission events
* `DET:TOK:GRANT:*` — grants disbursements
* `DET:TOK:TREAS:*` — treasury movements
* `DET:TOK:VEST:*` — vesting releases
* `DET:TOK:RECOVER:*` — recovery attestations

**DET ID rule:** `DET:<space>:<domain?>:<sns?>:<activity>:<version>`
Example: `DET:TOK:EMIT:AAA:52-10:mint_poi:V1`

---

## 7) Minting flow (weekly)

See details in `workflows/minting-flow.md`.

1. **Aggregator** computes PoI score and net recoveries; writes `feed.json` and `recovery_feed.json` (signed, with `previous_hash`).
2. **MonetaryPolicy** validates cooldown and caps; mints to **Innovators/Treasury/Sustainability/Vesting**.
3. Emit **DET\:TOK\:EMIT** with refs to CE/CI and CADET cut (off-chain writer).
4. **TekDAO** runs grant rounds (quadratic funding) from treasury allocation.

---

## 8) Security & compliance

* **Evidence integrity**: `sha256` + **Ed25519**, append-only via `previous_hash`.
* **Oracles**: multi-signer; outlier guards; KYC/AML and sanctions checks (recoveries).
* **S1000D**: documentation lives **only** under `CAS-SUSTAINMENT/**/S1000D/` (downstream pointers elsewhere).
* **Reg frameworks**: FCPA, UK Bribery Act, SOX, ISO 37001, GDPR (see `tokenomics.yaml/compliance`).
* **Disclaimer**: This is not financial or legal advice.

---

## 9) Quick start (dev)

* **Review**: `tokenomics.yaml`, oracle specs, and contract skeletons.
* **Compile** (example Hardhat/Foundry):

  * Add OpenZeppelin contracts (`@openzeppelin/contracts`).
  * Fix imports if your toolchain uses a different pathing.
* **Simulate mints**: mock oracle feeds, call `mintAccordingToFeeds()` and assert splits (55/25/10/10 pipeline).
* **Emit DET**: write a small script that serializes `det_packet.json` and signs it (Ed25519) after each mint and grant.

---

## 10) File map (key paths)

```
UTCS-BLOCKCHAIN/TekTok/
├─ tokenomics.yaml                       # full PoI + recoveries model, allocations, guards
├─ oracle/
│  ├─ det-cadet-oracle.spec.yaml         # PoI oracle spec
│  ├─ recovery-oracle.spec.yaml          # Anti-corruption oracle spec
│  └─ offchain-aggregator.md             # how to publish signed feeds
├─ contracts/
│  ├─ TekTok.sol                         # ERC-20 token
│  ├─ TekTokMonetaryPolicy.sol           # weekly mint logic
│  ├─ TekCred.sol                        # SBT reputation
│  ├─ TekDAO.sol                         # Timelock governance
│  ├─ TokenVesting.sol                   # vesting helper
│  └─ interfaces/
│     ├─ IDetCadetOracle.sol
│     └─ IRecoveryOracle.sol
├─ registry/det-namespaces.yaml          # DET:TOK* namespaces
├─ policies/sustainability.md            # grants & KPI priorities
└─ workflows/minting-flow.md             # end-to-end weekly process
```

---

## 11) Example DET node (evidence)

```
UTCS-BLOCKCHAIN/DET/CAD/AAA/52-10/design/V3/
├─ det_packet.json
├─ signature.ed25519
├─ previous_hash
├─ trace.yaml
└─ cadet.yaml
```

**`det_packet.json` (example)**

```json
{
  "det_id": "DET:CAD:AAA:52-10:design:V3",
  "ts": "2025-09-01T12:00:00Z",
  "refs": { "ce": "CE-CAD-Q100-AAA-ATA-52-DOORS", "ci": "CE-CC-CI-CAD-Q100-AAA-ATA-52-10-01-FWD-PAX-DOOR-LH" },
  "inputs": { "cad_files": ["./door_assy.SLDASM"] },
  "processing": { "tool": "SW@2025.0", "params": { "regen": true } },
  "outputs": { "units": "mm, kg", "metrics": { "mass_kg": 125.5, "cg_x_mm": 15120 } },
  "hash": "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
  "sig": { "alg": "Ed25519", "by": "wb-bot@aqua" }
}
```

---

## 12) Roadmap

* Add CI to validate every `det_packet.json` / `trace.yaml` against schemas.
* Add unit tests for MonetaryPolicy with mocked oracle feeds.
* Expand domain pillar READMEs and examples for all 105 namespaces.
* Optional: publish an on-chain PoI feed (ECDSA) if you want native verification.

---

**Contact:** airworthiness\@your-org • governance: TekDAO (see contracts) • sustainability: see `policies/sustainability.md`
