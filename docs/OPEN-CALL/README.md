# Open Call (R1) — Repo Guide

Artifacts:
- Announcement: `docs/OPEN-CALL/OPEN-CALL.md`
- Bounties: `bounties/*.yaml`
- Royalty registry: `payments/royalty.registry.yaml`
- Crypto payout policy: `payments/policy.md`
- Validators: `scripts/open_call_validate.mjs`
- CI: `.github/workflows/open-call.yml`
- DET samples: `events/samples/OpenCall.*.json`

Run locally:
- `yamllint -s bounties payments`
- `node scripts/open_call_validate.mjs bounties/*.yaml`