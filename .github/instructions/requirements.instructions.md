---
applyTo:
  - "**/requirements.yaml"
  - "**/requirements/*.yaml"
---

## CAD — Requirements rules
- English only; unique `id` per requirement (e.g., `REQ-AAA-52-10-01-001`).
- Minimum fields:
  - `id`, `text`, `source` (reg/standard/ref), `driver` (perf/safety/sustainability),
    `acceptance` (pass/fail statements), `verification` (Analysis/Test/Inspection),
    `links` { `ce`, `cc`, `ci` }, `status` (draft/baselined), `owner`, `last_updated`.
- Emit DET on changes:
  - `DET:CAD:<MIC>:<SNS>:req_add|req_update|req_baseline:V<rev>` with `refs{ce,ci}` and evidence attachments.
- No binaries; use CSV/JSON/MD. Keep traceability to standards in `compliance/standards.yaml`.