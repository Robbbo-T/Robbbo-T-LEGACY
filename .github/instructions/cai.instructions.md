---
applyTo:
  - "**/ICD*.yml"
  - "**/ICD*.yaml"
  - "**/ICD*.json"
  - "**/integration/**"
  - "**/installation-records/**"
---

## CAI rules
- Keep **ICD** in YAML/JSON; installation/test logs under `integration/` or `installation-records/`.
- Emit DET for `install_signoff` and `sys_test` (PASS/FAIL + attachments + units) with `refs{ce,ci}`.
- No secrets or credentials in logs.