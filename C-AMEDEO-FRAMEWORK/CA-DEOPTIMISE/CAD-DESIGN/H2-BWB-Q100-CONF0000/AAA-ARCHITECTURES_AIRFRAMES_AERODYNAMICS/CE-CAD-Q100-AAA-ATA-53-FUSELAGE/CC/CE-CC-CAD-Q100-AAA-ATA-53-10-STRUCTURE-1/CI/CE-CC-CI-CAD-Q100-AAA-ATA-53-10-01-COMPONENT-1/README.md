# Q100-53-10-01-001 — Forward Pressure Bulkhead Assembly

**DET ID:** DET:CAD:AAA:53-10-01:design:V3  
**Part Number:** Q100-53-10-01-001  
**Revision:** A  
**Units:** EA  
**Weight:** 412.5 kg  

## 📌 Breakdown
- 010 — Skin panel CFRP (CFRP-T800) ×1
- 020 — Core sandwich (PMI Foam 18 mm) ×1
- 030 — Peripheral flange (CFRP-T800) ×1
- 040 — Hardpoint inserts (Ti-6Al-4V) ×8

## 📂 Estructura de carpetas y archivos

```
CE-CC-CI-CAD-Q100-AAA-ATA-53-10-01-COMPONENT-1-PBS-Q100-53-10-01-0001/
│
├── README.md                     # Descripción general del CI
│
├── CADParameters.json            # Parámetros geométricos / reglas CAD
├── EBOM.yaml                     # Engineering BOM
├── MBOM.yaml                     # Manufacturing BOM
├── Effectivities.yaml            # Efectividades / configuraciones
├── PBS.json                      # Product Breakdown Structure
├── traceability.yaml             # Vínculos entre artefactos y requisitos
│
├── 3DModels/                     # Modelos 3D nativos y neutros
│   ├── fpb_assy_v3.CATPart
│   ├── fpb_assy_v3.CATProduct
│   └── fpb_assy_v3.step          # STEP AP242 ed2 + VP
│
├── Drawings/                     # Planos 2D
│   ├── fpb_assy_v3.dwg           # nativo AutoCAD
│   ├── fpb_assy_v3.dxf           # neutro DXF
│   └── fpb_assy_v3.pdf           # PDF/A-2b firmado
│
└── Integrity/                    # Integridad y automatización
    ├── manifest.yaml             # Metadata, SHA256, tamaños, VP
    ├── SHA256SUMS.txt            # Lista de hashes generada
    ├── generate_hashes.sh        # Script para recalcular e inyectar
    ├── validate_ci_package.py    # Validador Python completo
    └── extract_vp_from_step.py   # Extractor de VP desde STEP
```

## 📂 Artefactos vinculados
- 3D Master (STEP AP242 ed2+VP) → [`3DModels/fpb_assy_v3.step`](3DModels/fpb_assy_v3.step)
- Nativo CAD (CATIA V5R30) → [`3DModels/fpb_assy_v3.CATPart`](3DModels/fpb_assy_v3.CATPart)
- Drawing (PDF/A-2b firmado) → [`Drawings/fpb_assy_v3.pdf`](Drawings/fpb_assy_v3.pdf)
- EBOM/MBOM/PBS/Trazabilidad → YAML/JSON adjuntos

## 🔒 Integridad
- Hashes SHA256 y tamaños gestionados vía [`Integrity/manifest.yaml`](Integrity/manifest.yaml)
- Scripts:
  - [`Integrity/generate_hashes.sh`](Integrity/generate_hashes.sh) → recalcula y actualiza manifest
  - [`Integrity/validate_ci_package.py`](Integrity/validate_ci_package.py) → valida CI completo
  - [`Integrity/extract_vp_from_step.py`](Integrity/extract_vp_from_step.py) → extrae VP desde STEP

## 📜 Normativa aplicable
- ASME Y14.5-2018 (GD&T)
- EASA CS-25.365 / CS-25.571
- AS9102 (First Article Inspection)
- STEP AP242 ed2 con Validation Properties

## ✅ Checklist de completitud

* [x] EBOM / MBOM con breakdown de partes.
* [x] PBS jerárquico en JSON.
* [x] 3D nativo + STEP AP242 ed2+VP.
* [x] 2D drawings (DWG/PDF/A-2b).
* [x] Manifest de integridad con SHA256/tamaños/VP.
* [x] Scripts de automatización (`generate_hashes.sh` + `validate_ci_package.py`).
* [x] Trazabilidad requisitos ↔ artefactos (`traceability.yaml`).

---

Con esta estructura el repositorio es **PLM-ready** y apto para **auditoría EASA/FAA**: cada artefacto tiene su hash, está vinculado al PBS, y se valida automáticamente en cada commit.