# ASI Artifact Ranking — Metrics and Methods

This document defines how we compute innovation and on-chain added value for artifacts (grouped by CE/CI), restricted to official, affiliated repositories.

## Provenance (eligibility)
- Only artifacts whose DET packets include `inputs.provenance.git_url` that matches `affiliates.yaml`.
- Optional: allowlist signer IDs (`sig.by`) or signed commits upstream.
- All DET packets must include `outputs.units` and sha256 hash + Ed25519 signature.

## Metric definitions

### CAV — Catalyze Additional Value

**CAV Reuse Multiplier**  
Measures how many times an artifact's reuse features are adopted by downstream components. Computed as: `reuse_events × downstream_adoption_factor`.

**CAV Energy Efficiency**  
Energy saved (kWh) attributable to the artifact divided by implementation effort. Higher values indicate more efficient value creation.

**CAV Spillover Effect**  
Cross-domain and cross-pillar innovation adoption rate. Measures how innovations spread beyond their original domain.

### CLI — Cluster Innovation

**CLI Novelty Score (0..1)**  
Measures first-of-kind methods or breakthrough approaches. 1 if the artifact introduces new verified methods; 0 for incremental improvements.

**CLI Coherence (0..1)**  
Internal cluster consistency and synergy. Measures how well artifacts work together within innovation clusters.

**CLI Emergence Rate**  
Speed of cluster formation and growth, normalized using inverse time transformation: `1 / (1 + days / 30)`.

### BAF — Boost Auto Finance

**BAF ROI Projection**  
Projected return on investment efficiency based on sustainability metrics and implementation costs.

**BAF Sustainability Alignment (0..1)**  
Alignment with sustainability goals: energy savings, CO₂ reduction, lifecycle extension, circular economy principles.

**BAF Risk Mitigation**  
Risk reduction measures including ΔCVaR improvements, robustness increases, and uncertainty reduction.

## Normalization

- `zscore`: `(x - mean) / std` within eligible artifacts (clamped to ±3).
- `minmax01`: `(x - min) / (max - min)`.
- `domain_norm`: zscore computed per domain and then averaged globally.
- `inv_days_norm`: map days to (0..1) using `1 / (1 + days / H)` with H=30 days (tunable).

## Scoring

Global composite score:  
`S = Σ w_i · norm(M_i)` using weights from `asi-config.yaml`.

Ties resolved by: higher BAF sustainability alignment → higher CLI novelty score → earliest timestamp.

## Cluster Detection

Innovation clusters are identified by:
1. **Theme coherence**: artifacts addressing similar sustainability themes
2. **Temporal proximity**: formed within similar time windows  
3. **Cross-references**: artifacts that reference each other
4. **Domain spanning**: clusters that cross multiple domains/pillars

## Outputs

- JSON and Markdown leaderboards in `ASI/leaderboards/`
- Include per-artifact breakdown of raw metrics, normalizations, and final score
- Cluster analysis with coherence scores and emergence metrics
- Proposal drafts for significant changes requiring human review