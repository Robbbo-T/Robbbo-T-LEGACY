# Open Call · Genesis Bounties (R1) — 🇪🇸/🇬🇧

> **Purpose**: accelerate milestones with **crypto remuneration** and **Genesis royalties**
> (OEGI-ready), aligned with S1000D‑Q, CAS governance, and CE→CC→CI→CP→FE→QS.

## 🇪🇸 Resumen
- Pagos en **stablecoins** (no custodia) + **royalties de génesis** (GL‑EU BY‑RF 1.0).
- Aceptación: PRs que cumplan **yamllint**, **BREX validator**, **tests** y **DET**.
- Foco R1: ATA‑56 (ventanas panorámicas), GenesisMap (ingesta), y validador BREX.

## 🇬🇧 Summary
- **Stablecoin** payouts (non‑custodial) + **genesis royalties** (GL‑EU BY‑RF 1.0).
- Acceptance via PRs that pass **yamllint**, **BREX validator**, **tests**, **DET**.
- R1 focus: ATA‑56 S1000D‑Q docs, GenesisMap ingestion, BREX validator hardening.

### How to participate
1. Open an issue using the **Open Call Task** template (choose a bounty).
2. Submit a PR referencing the bounty ID.
3. Ensure CI green; include DET events and checklist below.

### Acceptance checklist (summary)
- CI green (yamllint/schema/tests).
- English-only for docs; markdown links for DI/CE/CC/CI/CP.
- DET updates for EBOM/MBOM/analysis/integration/requirements/compliance.
- BREX validator PASS (if DM-*.yaml).
- RTM/ICD consistency unchanged unless bounty requires updates.

### Remuneration
- **Bounty**: fixed stablecoin amount.
- **Genesis Royalty**: % share recorded in `payments/royalty.registry.yaml`.
- Payouts: non‑custodial transfer to contributor wallet (KYC may apply > threshold).
- This is **not** an investment instrument; no token sale; no expectation of profit
  from others' efforts (work‑for‑bounty + royalty on *use*).

### Compliance & Ethics (brief)
- MiCA/GDPR/TDM compliant processes; opt‑outs and privacy respected.
- Use GL‑EU licenses (BY / BY‑RC / BY‑RF). See `LICENSES/GL-EU-*`.
- Read `payments/policy.md` before claiming a bounty.