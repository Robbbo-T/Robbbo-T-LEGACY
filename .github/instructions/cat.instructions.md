---
applyTo:
  - "**/CAT-SOURCE_CODE_SYSTEMS/**"
  - "**/*.sbom.json"
  - "**/sbom/**"
---

## CAT rules
- Keep code, tests, and build manifests consistent with repo tooling.
- Generate **SBOM** on builds and emit `sbom_generate` DET with summary (counts, vulnerabilities).
- Follow SLSA where applicable; never commit secrets/tokens.