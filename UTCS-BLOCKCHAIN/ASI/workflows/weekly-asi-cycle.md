# Weekly ASI Cycle Workflow

## Overview
The ASI (Autonomous Sustainable Intelligence) system runs a weekly cycle to compute artifact scores, detect innovation clusters, and generate proposals for the TekDAO.

## Schedule
- **Trigger**: Every Sunday at 03:00 UTC
- **Duration**: ~2-4 hours
- **Output**: Updated leaderboards and proposals

## Workflow Steps

### 1. Data Collection (30 min)
```bash
# Collect DET evidence packets
find UTCS-BLOCKCHAIN/DET -name "det_packet.json" -newer last_run.timestamp

# Collect CADET KPI cuts  
find UTCS-BLOCKCHAIN/CADET/kpis -name "*.yaml" -newer last_run.timestamp

# Collect TekTok oracle feeds
cat UTCS-BLOCKCHAIN/TekTok/oracle/feed.json
cat UTCS-BLOCKCHAIN/TekTok/oracle/recovery_feed.json
```

### 2. Eligibility Validation (15 min)
- Check repository provenance against affiliates allowlist
- Validate Ed25519 signatures and SHA-256 hashes
- Verify SI units in outputs
- Filter by lookback window (90 days)

### 3. Metric Computation (45 min)
- **CAV metrics**: reuse multiplier, energy efficiency, spillover effect
- **CLI metrics**: novelty score, coherence, emergence rate
- **BAF metrics**: ROI projection, sustainability alignment, risk mitigation

### 4. Normalization and Scoring (30 min)
- Apply z-score, min-max, and domain normalization
- Compute weighted composite scores
- Apply domain balancing

### 5. Cluster Detection (30 min)
- Group artifacts by sustainability themes
- Compute cluster coherence scores
- Identify emerging innovation patterns
- Track cluster evolution metrics

### 6. Leaderboard Generation (15 min)
- Sort by composite ASI scores
- Generate JSON and Markdown outputs
- Create theme-specific rankings (CAV, CLI, BAF)

### 7. Proposal Generation (30 min)
- Check for significant weight changes (>20%)
- Identify new high performers (>90th percentile)
- Detect cluster emergence (5+ artifacts)
- Draft human-reviewable proposals

### 8. Evidence Publication (15 min)
- Emit DET:ASI events for scores and clusters
- Sign outputs with Ed25519
- Update previous_hash chains

### 9. Quality Assurance (20 min)
- Validate output schemas
- Check for anomalous patterns
- Generate audit logs
- Verify signature integrity

## Error Handling

### Soft Errors (warnings)
- Late-arriving evidence within grace window
- Missing cross-domain traces
- Incomplete metric data

### Hard Errors (abort)
- Invalid signatures
- Missing required fields
- Schema validation failures
- Repository provenance violations

## Output Files
```
UTCS-BLOCKCHAIN/ASI/leaderboards/
├── leaderboard-global.json
├── leaderboard-global.md
├── leaderboard-cav.md
├── leaderboard-cli.md
└── leaderboard-baf.md

UTCS-BLOCKCHAIN/ASI/proposals/
├── YYYY-MM-DD-weight-changes.md
├── YYYY-MM-DD-cluster-emergence.md
└── YYYY-MM-DD-high-performers.md
```

## Monitoring
- Execution duration tracking
- Error rate monitoring
- Score distribution analysis
- Cluster stability metrics

## Human Review Points
1. **Proposal Review**: All generated proposals require TekDAO approval
2. **Anomaly Investigation**: Unexpected score changes or cluster formations
3. **Weight Adjustment**: Quarterly review of metric weights and normalization
4. **Affiliate Updates**: New repository/signer approvals