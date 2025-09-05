# S1000D Governance — CAS Domain

This pack governs CAS domain S1000D content via **BREX** (Business Rules), **BRDP**
(Decision Points), and a lightweight repository profile. It complements existing
ATA/CE→CC→CI→CP→FE→QS hierarchies without refactoring historical material.

Artifacts:
- BREX: `BREX-CAS.yaml` — enforceable rules accepted by repo tooling.
- BRDP: `BRDP-CAS.yaml` — documented decisions behind the BREX rules.
- PROFILE: `PROFILE-CAS.yaml` — allowed DM codes, statuses, applicability.
- CI: GitHub Action to lint and validate BREX conformance on PRs.