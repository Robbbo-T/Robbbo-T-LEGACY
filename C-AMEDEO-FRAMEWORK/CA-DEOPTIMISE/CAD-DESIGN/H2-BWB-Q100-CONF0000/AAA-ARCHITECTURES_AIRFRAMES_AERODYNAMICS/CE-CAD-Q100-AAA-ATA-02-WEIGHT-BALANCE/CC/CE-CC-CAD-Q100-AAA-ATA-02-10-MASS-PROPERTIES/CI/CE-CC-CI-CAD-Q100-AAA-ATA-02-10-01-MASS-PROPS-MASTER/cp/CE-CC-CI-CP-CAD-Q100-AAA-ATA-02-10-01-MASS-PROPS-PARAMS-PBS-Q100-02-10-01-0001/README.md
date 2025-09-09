# CE-CC-CI-CP-CAD-Q100-AAA-ATA-02-10-01-MASS-PROPS-PARAMS-PBS-Q100-02-10-01-0001

**UniversalStandard:** TechnicalElement-Design-iSpec2200-ATA 02-10-01-MassPropsParams-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-HybridGeneration-AIR-AmedeoPelliccia-deadbeef-RemainingUsefulLife

**Purpose.** This **CP (Component Particle / PBS leaf)** packages the **Weight & Balance parameters** for ATA **02-10-01** (Mass Properties Master): baseline weights, CG references, stations/MAC, and inertias. It is **CAD-first**, feeds **PBS → EBOM/MBOM**, and serves as the authoritative data bundle for analyses and downstream publication (S1000D generated later under **CAS**).

---

## 1) Identification & Links

- **WBS / PBS ID:** `Q100-02-10-01-0001`  
- **OwnerDomain:** AAA (Architectures_Airframes_Aerodynamics)  
- **CAX:** CAD  
- **SNS:** `02-10-01`  
- **Configuration:** `H2-BWB-Q100-CONF0000`

**Hierarchy (upwards):**

- **CI (Mass-Props Master):** [`CE-CC-CI-CAD-Q100-AAA-ATA-02-10-01-MASS-PROPS-MASTER`](../../..)
- **CC (Mass Properties):** [`CE-CC-CAD-Q100-AAA-ATA-02-10-MASS-PROPERTIES`](../../../../../)
- **CE (Weight & Balance):** `.../AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-02-WEIGHT-BALANCE/`

> **Scope note:** This CP is **data-centric**. **EBOM/MBOM** apply only to **physical** CIs; here we provide canonical **design-data** parameters.

---

## 2) Files in this package

```

.
├─ README.md                      # this file
├─ data/
│  ├─ mass\_props.csv              # weights & CGs by condition (units: kg, mm, %MAC)
│  ├─ inertias.json               # Ixx/Iyy/Izz/Ixy/Iyz/Izx (kg·m²) + ref point
│  ├─ stations.json               # reference coordinate frames, MAC, LEMAC, X0/Y0/Z0
│  └─ assumptions.md              # modeling assumptions & sources
└─ schema/
└─ mass\_props.schema.json      # JSON Schema for CSV->JSON normalized view

````

**Minimum columns in `mass_props.csv`**

| field              | type   | units | example        | notes                                |
|--------------------|--------|-------|----------------|--------------------------------------|
| condition          | string | —     | OEW            | BASIC_EMPTY, OEW, MZFW, MTOW, MLW…   |
| weight_kg          | number | kg    | 42150          | rounded to nearest 0.1 kg            |
| cg_x_mm            | number | mm    | 15120          | from reference X0                    |
| cg_y_mm            | number | mm    | 0              | lateral CG (0 for symmetric)         |
| cg_z_mm            | number | mm    | 2450           | vertical CG                          |
| cg_percent_mac     | number | %MAC  | 28.7           | computed from MAC & LEMAC            |
| notes              | string | —     | “OEW Rev C”    | provenance / remarks                 |

**`inertias.json` (example)**
```json
{
  "reference_point_mm": { "x": 0, "y": 0, "z": 0 },
  "units": { "I": "kg*m^2" },
  "conditions": [
    {
      "id": "OEW",
      "Ixx": 1.12e8, "Iyy": 2.05e8, "Izz": 3.01e8,
      "Ixy": 0.0, "Iyz": 0.0, "Izx": 0.0
    }
  ]
}
````

---

## 3) Parameter semantics (authoritative references)

* **Stations & MAC:** `data/stations.json` (defines **X0/Y0/Z0**, **MAC**, **LEMAC**, stations grid).
* **CG in %MAC:** computed from `cg_x_mm` vs. LEMAC/MAC in `stations.json`.
* **Inertias:** about **reference\_point\_mm**; specify if transported to another frame.
* **Units:** keep **SI** (`kg`, `mm`, `kg·m²`). Record unit transforms explicitly if applied.

---

## 4) DET evidence (CAD → PBS)

Emit a **DET** pack on every meaningful update:

```json
{
  "det_id": "DET:CAD:Q100:02-10-01:mass_props_update:V3",
  "ts": "2025-09-01T12:00:00Z",
  "refs": {
    "ce": "CE-CAD-Q100-AAA-ATA-02-WEIGHT-BALANCE",
    "ci": "CE-CC-CI-CAD-Q100-AAA-ATA-02-10-01-MASS-PROPS-MASTER"
  },
  "inputs": {
    "stations_ref": "./data/stations.json",
    "previous_hash": "c0ffee00"
  },
  "processing": { "tool": "W&B-Calc@1.0", "params": { "units": "kg,mm,%MAC" } },
  "outputs": {
    "mass_props_csv": "./data/mass_props.csv",
    "inertias_json": "./data/inertias.json",
    "delta": { "OEW.weight_kg": -35.0, "OEW.cg_percent_mac": -0.3 },
    "units": "kg, mm, %MAC, kg·m^2"
  },
  "hash": "deadbeef",
  "sig": { "alg": "Ed25519", "by": "wb-bot@aqua" }
}
```

**Related DET checks** (ATA-02 specific):

* `DET:CAD:Q100:02-20:cg_envelope_check:V*` (links to CE 02-20 CG envelope)
* `DET:CAD:Q100:02-30:fuel_map_sync:V*` (cross with ATA 28 fuel geometry, if applicable)

---

## 5) Validation checklist

* [ ] `mass_props.csv` parses; required columns present; units = **kg/mm/%MAC**
* [ ] `%MAC` computed from **stations.json** (LEMAC/MAC present)
* [ ] `inertias.json` includes **reference point** & **units**; values plausible
* [ ] **DET** `mass_props_update` emitted (with `refs.ce/refs.ci` and units)
* [ ] Trace to CI/CC/CE is correct (links above work)
* [ ] Changes reviewed and baselined (UTCS header hash updated if needed)

---

## 6) Cross-references (read-only)

* **CE:** Weight & Balance (ATA 02)
* **CC:** Mass Properties (ATA 02-10)
* **CI:** Mass-Props Master (ATA 02-10-01)
* **Dependent slices:** ATA **06** (stations/MAC), **08** (weigh-in ingestion), **28** (fuel), **34** (nav frames)

---

## 7) Versioning

* **Data version:** `V3` (example)
* **Baseline status:** Draft / Baselined (choose one)
* **Last updated:** 2025-09-01
* **Change note:** “OEW trimmed by -35 kg; CG shifted -0.3 %MAC after seat/galley update”

```
::contentReference[oaicite:0]{index=0}
```
