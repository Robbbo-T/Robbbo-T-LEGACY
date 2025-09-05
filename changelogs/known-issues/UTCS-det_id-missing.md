# Known Issue: Missing det_id in UTCS-BLOCKCHAIN manifest
- Validator: validate_utcs_blockchain.py
- Finding: Missing det_id at DET/CAT/AAA/52-10/test_execution/V1/manifest.yaml
- Action: Do not modify legacy manifests in this PR. Track and fix in a dedicated UTCS PR.
- Link this note in the PR body.