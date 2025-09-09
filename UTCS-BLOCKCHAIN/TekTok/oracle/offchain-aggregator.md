# Off-chain Aggregator — PoI & Recoveries Feeds

**Purpose.** Produce weekly, signed oracle feeds from the UTCS-BLOCKCHAIN evidence:

* **PoI feed** (`feed.json`) — Proof-of-Innovation score derived from **DET** & **CADET**.
* **Recoveries feed** (`recovery_feed.json`) — net, audited **anti-corruption recoveries**.
* Feeds are **Ed25519-signed**, chained by **previous\_hash**, and consumed by **TekTokMonetaryPolicy**.

> DET ID convention: `DET:<CAX>:<DOMAIN>:<SNS>:<activity>:<version>`
> Example: `DET:CAD:AAA:52-10:design:V3`

---

## 0) Inputs & Outputs

**Inputs**

* **DET packets**: `UTCS-BLOCKCHAIN/DET/**/det_packet.json` (schema: `DET/schemas/det-packet.schema.json`)
* **CADET KPI cuts**: `UTCS-BLOCKCHAIN/CADET/kpis/**.yaml` (schema: `DET/schemas/cadet-record.schema.json`)
* **Tokenomics**: `UTCS-BLOCKCHAIN/TekTok/tokenomics.yaml`
* **Recoveries** *(if enabled)*: `UTCS-BLOCKCHAIN/DET/TOK/RECOVER/**/det_packet.json`
* **Auditor/legal artifacts**: `UTCS-BLOCKCHAIN/TekTok/oracle/audits/**.json` *(optional, if you store them)*

**Outputs**

* `UTCS-BLOCKCHAIN/TekTok/oracle/feed.json` (PoI; signed)
* `UTCS-BLOCKCHAIN/TekTok/oracle/recovery_feed.json` (Recoveries; signed)
* Both include: `{ timestamp, payload, previous_hash, signature }`

---

## 1) Data selection window (weekly cadence)

* **Window:** last **7 days** (configurable).
* **PoI data sources:**

  * DET packets with activities from tokenomics KPIs (e.g., `design`, `solver_run`, `baseline_freeze`, etc.)
  * CADET KPI cut(s) covering the week (e.g., `CADET/kpis/2025-09.yaml`)
* **Recoveries sources (if enabled):**

  * `DET:TOK:RECOVER:*:*:recovery_attest:V*` packets
  * Optional auditor/legal JSON evidence

> Anti-gaming guards are defined in `tokenomics.yaml` (min signers, outlier σ, time weighting, duplicate detector).

---

## 2) Normalization & scoring

Read **weights & normalizers** from `tokenomics.yaml` → `proof_of_innovation.kpis`.

**Default normalization (examples)**
*(Use your tokenomics file as the source of truth; below mirrors the spec.)*

* `reuse_percent` → average Δ over window (in pct → 0..100)
* `energy_saved_kwh` → sum over window, scaled per 100k kWh
* `co2_saved_kg` → sum over window, scaled per 10k kg
* `life_ext_months` → sum over window, scaled per 12 months
* `risk_reduction` (ΔCVaR) → average Δ over window
* `recouped_funds_usd` (recoveries) → sum of **net** confirmed USD; normalized per 1M USD

**PoI score (18-dec fixed-point)**

```
score = Σ_k  weight_k * normalize_k(kpi_k_window)
```

Produce an **int256 with 18 decimals** (multiply the floating score by 1e18).

**Recoveries amount (18-dec)**

* Convert net USD into `uint256` with **18 decimals** → `recoupedUSD18`.

---

## 3) Canonical hashing & signature

* Canonicalize the JSON payload:

  * Sort keys lexicographically; remove insignificant whitespace (JCS-like).
* `previous_hash` = **sha256** of the last feed file’s canonical JSON.
* **Ed25519 signature** over the **current canonical payload** (not including signature field).

> Keep **private keys** offline/secured (HSM if possible). If you need on-chain verification later, emit ECDSA feeds or add a precompile/adapter.

---

## 4) JSON shapes (strict)

### 4.1 PoI feed — `feed.json`

```json
{
  "version": "1.0.0",
  "timestamp": "2025-09-01T00:00:00Z",
  "window_days": 7,
  "kpis": {
    "reuse_percent": 41.8,
    "energy_saved_kwh": 38500,
    "co2_saved_kg": 1180,
    "life_ext_months": 12,
    "risk_reduction": 0.07
  },
  "score_18": "41800000000000000000", 
  "weights_ref": "TekTok/tokenomics.yaml#proof_of_innovation.kpis",
  "sources": {
    "det": ["DET:CAD:AAA:53-10:design:V5", "DET:CAE:AAA:53-10:solver_run:V3"],
    "cadet": ["CADET/kpis/2025-09.yaml"]
  },
  "guards": { "sigma_outlier": 3, "min_sources": 2 },
  "previous_hash": "sha256hex-of-last-feed",
  "signature": {
    "alg": "Ed25519",
    "signer": "oracle1@tek",
    "sig_b64": "BASE64_SIGNATURE"
  }
}
```

### 4.2 Recoveries feed — `recovery_feed.json`

```json
{
  "version": "1.0.0",
  "timestamp": "2025-09-01T00:00:00Z",
  "window_days": 90,
  "recoupedUSD18": "250000000000000000000", 
  "proof": {
    "det_recoveries": ["DET:TOK:RECOVER:ORG-42:case-2025-001:recovery_attest:V1"],
    "auditor_reports": ["TekTok/oracle/audits/ORG-42-case-2025-001.json"]
  },
  "compliance_checks": {
    "auditor_attestation": true,
    "legal_opinion": true,
    "kyc_aml_screening": true,
    "sanctions_check": true
  },
  "previous_hash": "sha256hex-of-last-recovery-feed",
  "signature": {
    "alg": "Ed25519",
    "signer": "oracle2@tek",
    "sig_b64": "BASE64_SIGNATURE"
  }
}
```

---

## 5) Weekly runbook

1. **Collect inputs**

   * Query DET and CADET for the window; validate against schemas.
2. **Normalize & score**

   * Apply tokenomics normalizers & weights (PoI) and net recoveries logic.
3. **Canonicalize JSON**

   * Sort keys; minify; compute `previous_hash` from last file.
4. **Sign Ed25519**

   * Produce `sig_b64` over canonical JSON.
5. **Write feeds**

   * `TekTok/oracle/feed.json` and/or `recovery_feed.json`.
6. **Log DET events (off-chain writer)**

   * Emit `DET:TOK:EMIT:*:mint_poi:V<n>` for mints and grants (optional, strongly recommended).

---

## 6) CLI pseudo-implementation (Python)

> This is a **reference**; use your stack of choice. Requires `pydantic`, `pyyaml`, `pynacl`.

```python
# run: python aggregate_feeds.py --root UTCS-BLOCKCHAIN --sign-key ed25519_sk.b64
import json, os, base64, hashlib, argparse, glob, yaml
from datetime import datetime, timezone
from nacl.signing import SigningKey

def canonical(obj):  # naive JCS-like: sort keys, separators to minify
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()

def sha256hex(b): return hashlib.sha256(b).hexdigest()

def load_yaml(p): return yaml.safe_load(open(p, "r", encoding="utf-8"))

def last_hash(path):
    try:
        with open(path, "rb") as f: return sha256hex(f.read())
    except FileNotFoundError:
        return "0"*64

def main(root, key_b64):
    sk = SigningKey(base64.b64decode(key_b64))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # --- Load tokenomics weights ---
    tok = load_yaml(os.path.join(root, "TekTok/tokenomics.yaml"))
    kpis_spec = tok["proof_of_innovation"]["kpis"]

    # --- Collect KPIs (demo values; replace with real aggregation) ---
    kpis = {"reuse_percent":41.8,"energy_saved_kwh":38500,"co2_saved_kg":1180,"life_ext_months":12,"risk_reduction":0.07}
    # normalize according to tokenomics (example scalers)
    norm = {
        "reuse_percent": kpis["reuse_percent"],             # pct as-is
        "energy_saved_kwh": kpis["energy_saved_kwh"]/100000,
        "co2_saved_kg": kpis["co2_saved_kg"]/10000,
        "life_ext_months": kpis["life_ext_months"]/12,
        "risk_reduction": kpis["risk_reduction"]
    }
    score = 0.0
    for name,val in norm.items():
        w = float(kpis_spec.get(name,{}).get("weight",0.0))
        score += w*val
    score_18 = str(int(score*1e18))

    # --- Build PoI feed ---
    poi_path = os.path.join(root, "TekTok/oracle/feed.json")
    poi_prev = last_hash(poi_path)
    poi = {
        "version":"1.0.0","timestamp":now,"window_days":7,
        "kpis":kpis,"score_18":score_18,
        "weights_ref":"TekTok/tokenomics.yaml#proof_of_innovation.kpis",
        "sources":{"det":[],"cadet":[]},
        "guards":{"sigma_outlier":3,"min_sources":2},
        "previous_hash":poi_prev
    }
    signed = sk.sign(canonical(poi)).signature
    poi["signature"]={"alg":"Ed25519","signer":"oracle1@tek","sig_b64":base64.b64encode(signed).decode()}
    with open(poi_path,"w",encoding="utf-8") as f: json.dump(poi,f,indent=2)

    # --- Build Recoveries feed (demo value) ---
    rec_path = os.path.join(root,"TekTok/oracle/recovery_feed.json")
    rec_prev = last_hash(rec_path)
    rec = {
        "version":"1.0.0","timestamp":now,"window_days":90,
        "recoupedUSD18": str(250_000 * 10**18),
        "proof":{"det_recoveries":[],"auditor_reports":[]},
        "compliance_checks":{"auditor_attestation":True,"legal_opinion":True,"kyc_aml_screening":True,"sanctions_check":True},
        "previous_hash":rec_prev
    }
    signed2 = sk.sign(canonical(rec)).signature
    rec["signature"]={"alg":"Ed25519","signer":"oracle2@tek","sig_b64":base64.b64encode(signed2).decode()}
    with open(rec_path,"w",encoding="utf-8") as f: json.dump(rec,f,indent=2)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True)
    ap.add_argument("--sign-key",required=True,help="ed25519 secret key b64")
    args=ap.parse_args()
    main(args.root,args.sign_key)
```

---

## 7) Scheduling (cron / CI)

**Cron** (server)

```
# weekly (Sun 02:00 UTC)
0 2 * * 0 /usr/bin/python3 aggregate_feeds.py --root /data/UTCS-BLOCKCHAIN --sign-key $ED25519_SK_B64 >> /var/log/tektok-oracle.log 2>&1
```

**GitHub Actions** (if repo-local aggregation)

```yaml
name: tektok-oracle
on:
  schedule: [{ cron: "0 2 * * 0" }]
  workflow_dispatch: {}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install pyyaml pynacl
      - name: Aggregate & sign feeds
        env:
          ED25519_SK_B64: ${{ secrets.TEKTOK_ED25519_SK_B64 }}
        run: |
          python UTCS-BLOCKCHAIN/TekTok/oracle/aggregate_feeds.py \
            --root UTCS-BLOCKCHAIN \
            --sign-key "$ED25519_SK_B64"
      - name: Commit feeds
        run: |
          git config user.name "oracle-bot"
          git config user.email "oracle@bot"
          git add UTCS-BLOCKCHAIN/TekTok/oracle/*.json
          git commit -m "chore: weekly oracle feeds" || echo "no changes"
          git push
```

---

## 8) Quality gates & alerts

* **Schema validation**: refuse to publish if `det_packet.json`, CADET cuts, or feeds fail their JSON/YAML schemas.
* **Outlier rejection**: drop data points beyond **3σ** (configurable).
* **Min sources**: require ≥2 independent DET/CADET sources or abort.
* **Signing key health**: rotate Ed25519 keys periodically; store in KMS/HSM.
* **Audit trail**: log inputs → normalized values → score → signature → hashes.

---

## 9) Emitting DET\:TOK events (off-chain writer)

After a successful mint by **MonetaryPolicy**, write a **DET** event:

```
UTCS-BLOCKCHAIN/DET/TOK/EMIT/<DOMAIN>/<SNS>/mint_poi/V<n>/det_packet.json
```

Minimal fields:

```json
{
  "det_id": "DET:TOK:EMIT:AAA:52-10:mint_poi:V1",
  "ts": "2025-09-08T00:00:00Z",
  "refs": { "ce": "CE-CAD-Q100-AAA-ATA-52-DOORS" },
  "inputs": { "feed": "TekTok/oracle/feed.json" },
  "processing": { "tool": "oracle-bridge@1.0", "params": {} },
  "outputs": { "units": "token", "metrics": { "mint_amount": 123456.0 } },
  "hash": "sha256-of-det-packet",
  "sig": { "alg": "Ed25519", "by": "oracle-bridge@tek" }
}
```

---

## 10) Troubleshooting

* **Zero score**: No valid DET/CADET sources in window → check data paths & schemas.
* **Signature mismatch**: Ensure canonicalization (sorted keys, minified) before signing.
* **Outlier rejections**: Tune σ and time-weighting in `tokenomics.yaml`.
* **On-chain verification**: If you migrate to ECDSA feeds, update contracts & spec accordingly.

---

**Security & Compliance disclaimer**
This guide does not constitute legal or financial advice. Apply your organization’s KYC/AML/sanctions and audit policies to **recoveries** and consult counsel for any jurisdiction-specific requirements.
