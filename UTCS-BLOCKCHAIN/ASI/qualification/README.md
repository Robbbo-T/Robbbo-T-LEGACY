# ASI Qualification — Innovator & Innovation Classes (PMI-like)

**Purpose.** Provide an *automatic* qualification (PMI-like) for:
- **Innovation (artifact)**: per CE/CI anchor ranked by ASI.
- **Innovator (contributor/team)**: aggregated across their ranked artifacts.

**Design constraints**
- **Certification helps but never gates**. Qualification uses **ASI composite** (cert-agnostic) and applies **sustainability floors**. Any certification signals remain bonus/tiebreaker only (see ASI certification policy).
- **Evidence-first**: Only DET packets with **Ed25519** signatures, **sha256** hash, **SI units**, and **affiliated provenance** are considered.

**Outputs**
- JSON & Markdown leaderboards with **Qualification Class** (Q1..Q5).
- Evidence events: `DET:ASI:qualification_publish:<object_id>:V<n>` (optional, off-chain writer).
- Optional queue for **TekCred (SBT)** issuance by TekDAO.

See config: `qualification-config.yaml`.