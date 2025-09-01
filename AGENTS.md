# AGENTS.md — Copilot coding agent instructions

## Role
Act as a cross-pillar contributor (CAD, CAE, CAI, CAM, CAT, CAS). Do **not** generate S1000D outside CAS; only add downstream pointers elsewhere.

## Guardrails
- No secrets/tokens/credentials.
- Respect DI → CE → CC → CI → CP and **ATA SNS** naming.
- When touching EBOM/MBOM/analysis/integration/requirements/feasibility/compliance, update DET templates and mention them in the PR body.

## Task patterns
- Small, scoped PRs (≤ 300 LOC).
- Prefer editing existing files over adding new formats.
- Run CI locally/ephemerally (lint/schema/tests) and paste a summary in PR.

## PR template (append)
- Summary:
- Pillar(s):
- Affected IDs (DI/CE/CC/CI/CP):
- Validation (build/lint/tests/schema):
- DET updates:
- Notes for reviewers: