# ASI Guardrails Policy Snapshot Reference

This directory contains example ASI decision packets that demonstrate proper policy snapshot referencing as required by ASI Guardrails v2.0.

## Policy Snapshot Hash Generation

To generate the policy snapshot hash for inclusion in ASI decision packets:

```bash
shasum -a 256 UTCS-BLOCKCHAIN/ASI/policies/guardrails.config.yaml | awk '{print $1}'
```

Current policy hash: `df1f9dc78b75fd03b81593861fd0661e3aeecb9f29c8c35be0eaf42dc91dc051`

## Required Fields in ASI Decision Packets

Every `DET:ASI:decision:*` packet must include in the `inputs` section:

```json
{
  "inputs": {
    "policy_snapshot": "sha256:HASH_VALUE",
    "policy_path": "UTCS-BLOCKCHAIN/ASI/policies/guardrails.config.yaml",
    "optimizer": "asi-agent@VERSION",
    "constraints": ["list", "of", "applied", "constraints"]
  }
}
```

## Energy Metrics Requirement

ASI decision packets must include either:
- `outputs.metrics.energy_kwh` (total energy consumption), or  
- `outputs.metrics.energy_breakdown` (detailed energy breakdown)

## Validation

Run the guardrails validator to ensure compliance:

```bash
python UTCS-BLOCKCHAIN/ASI/tools/validate_guardrails.py
```

This validates:
- Policy snapshot references are present
- Energy metrics are included
- Signatures and hashes are properly formatted
- Temporal consistency requirements are met
- Repository provenance (where available)