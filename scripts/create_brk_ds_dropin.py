#!/usr/bin/env python3
"""
Create the drop-in bundle on /mnt/data and zip it for download

This script creates a comprehensive BRK_DS dropin bundle containing:
- MBOM/SBOM Markdown files with ATA+S1000D structure
- Crosswalk mapping between EBOM/MBOM/SBOM
- QAUDIT YAML files
- Event JSON samples
- EMS schemas for validation
- JavaScript utilities for watching and matrix generation
- Package.json with build scripts
- CI integration snippets
"""

import os
import json
import textwrap
import zipfile
import pathlib
from datetime import datetime


def create_brk_ds_dropin():
    """Create the complete BRK_DS dropin bundle"""
    
    base = "/mnt/data/BRK_DS_dropin"
    os.makedirs(base, exist_ok=True)

    # --- 1) Files provided by the user (MBOM/SBOM Markdown, Crosswalk, QAUDIT, Events) ---
    files_root = {
        "FAN1_MBOM.md": """# FAN1 — MBOM (Manufacturing Bill of Materials)
EstándarUniversal:Artefacto-ListaMateriales-ATA+S1000D-72.10-ManufacturingBOM-0001-v9.0-Aerospace and Quantum United Advanced Venture-GeneracionHybrida-ppp-Amedeo Pelliccia-7f2a9c41-RestoDeVidaUtil
DET:SE:ppp:SE:FAN1-MBOM:V9.0

## Estructura MBOM (Niveles L1/L2)

| Nivel | Código | Descripción                         | Material                      | Cant. | Op | Estación (SE)   | Proceso                                      | Notas |
|:----:|:------:|-------------------------------------|-------------------------------|:-----:|:--:|-----------------|----------------------------------------------|------|
| L1   | CWL3   | Carcasa/cowl externa del fan        | CFRP                          | 2     | 060 | SE:ppp:INTEG    | RTM                                         | Par emparejado |
| L1   | SPN4   | Cono/spinner (conjunto)             | Al 7075 / CFRP                | 1     | 060 | SE:ppp:INTEG    | Laminado + torneado precisión               | — |
| L1   | SHR8   | Anillo bypass (shroud)              | CMC                           | 1     | 060 | SE:ppp:INTEG    | Bobinado + sinterizado                      | — |
| L2   | HUB2   | Núcleo de cubo de fan               | Titanio 6Al-4V                | 1     | 010 | SE:ppp:ROT-A    | CNC + HT                                    | IQC/NDT OK |
| L2   | BRH6   | Alojamiento de raíz de pala         | Inconel 718                   | 24    | 020 | SE:ppp:ROT-A    | DMLS                                        | Micro-lattice check |
| L2   | BLD1   | Pala de fan compuesta               | CFRP–Titanio                  | 24    | 030 | SE:ppp:ROT-A    | AFP                                         | Telemetría Q embebida |
| L2   | FST7-B | Tornillo fijación pala (kit FST7)   | Inconel/Ti coat               | 96    | 040 | SE:ppp:ROT-A    | Ensamble atornillado alto par               | 150 Nm ±3% |
| L2   | FST7-N | Tuerca fijación pala (kit FST7)     | Inconel/Ti coat               | 96    | 040 | SE:ppp:ROT-A    | Ensamble atornillado alto par               | 150 Nm ±3% |
| L2   | FST7-W | Arandela fijación pala (kit FST7)   | Inconel/Ti coat               | 96    | 040 | SE:ppp:ROT-A    | Ensamble atornillado alto par               | 150 Nm ±3% |
| L2   | QSN5   | Nodo de sensor cuántico             | NV diamante + grafeno         | 4     | 070 | SE:ppp:CLEAN    | Nanofabricación / instalación en ISO7       | Calibración T-QCAL-100 |
| L2   | QIC9   | Cable de interfaz cuántica          | Polímero superconductor       | 2     | 070 | SE:ppp:CLEAN    | Extrusión criogénica / routing              | Q-Telemetry Bus |

## BOP — Bill of Process (ruta de fabricación)

| Op  | Estación (SE)   | WI               | Descripción                                     | Recursos/útiles         | QA Gate |
|:---:|-----------------|------------------|-------------------------------------------------|-------------------------|--------|
| 010 | SE:ppp:ROT-A    | WI-72-10-00      | Recepción HUB2/BRH6, IQC/NDT                    | T-NDT-MPI-K01           | IQC: HT OK / NDT pass |
| 020 | SE:ppp:ROT-A    | WI-72-10-02      | Ensamblar BRH6 en HUB2                          | Llave control par       | 100% inspección micro-lattice |
| 030 | SE:ppp:ROT-A    | WI-72-10-03      | Montaje BLD1 (secuencia de equilibrado)         | T-AFP-001               | Poka-Yoke orientación |
| 040 | SE:ppp:ROT-A    | WI-72-10-05      | FST7-B/N/W ×96; aplicar CNS10                   | T-TORQ-150              | 150 Nm ±3%; sello |
| 050 | SE:ppp:BAL-01   | WI-72-10-07      | Balanceo dinámico                               | T-BAL-015               | Residuo < 0,25 g·cm (ISO 1940 G0.4) |
| 060 | SE:ppp:INTEG    | WI-72-10-09      | Montaje CWL3/SHR8/SPN4                          | Útil posicionamiento    | Gap/Flush ≤ 0,5 mm; estanqueidad |
| 070 | SE:ppp:CLEAN    | WI-72-10-15      | Instalar QSN5/QIC9 + calibración                | ISO7, T-QCAL-100        | DO-160G EMI pass |
| 080 | SE:ppp:FINAL    | WI-72-10-19      | Pruebas funcionales + SimBridge e2e             | SimBridge, DAS          | FAT; emisión DET |

## Plan de Control (extracto)

| Punto | Característica      | Método                    | Freq | Límite             | DET Ref                              |
|------:|---------------------|---------------------------|:----:|--------------------|--------------------------------------|
| QC-01 | Torque fijaciones   | Llave digital trazable    | 100% | 150 Nm ±3%         | DET:SE:ppp:SE:FAN1-QC-TORQUE:V9.0    |
| QC-02 | Imbalance rotor     | ISO 1940 G0.4             | 100% | < 0,25 g·cm        | DET:SE:ppp:SE:FAN1-QC-BAL:V9.0       |
| QC-03 | Limpieza ISO 7      | ISO 14644 partículas      | 100% | Clase 7            | DET:SE:ppp:SE:FAN1-QC-CLEAN:V9.0     |
| QC-04 | Continuidad Q-Bus   | DAS-Q, DO-160G            | 100% | Pass               | DET:SE:ppp:SE:FAN1-QC-QBUS:V9.0      |
""",

        "FAN1_SBOM.md": """# FAN1 — SBOM (Service Bill of Materials)
EstándarUniversal:Artefacto-CatalogoPiezas-ATA+S1000D-72.10-ServiceBOM-0001-v9.0-Aerospace and Quantum United Advanced Venture-GeneracionHybrida-ppp-Amedeo Pelliccia-c18e04d3-RestoDeVidaUtil
DET:SE:ppp:SE:FAN1-SBOM:V9.0

## FRUs / Kits y Puentes S1000D

| FRU/KIT           | Acción    | DMC S1000D (ej.)       | AMM/FIM (ej.)  | Notas de servicio                         |
|-------------------|-----------|------------------------|----------------|-------------------------------------------|
| BLD1-SVC          | Rem/Inst  | 72-10-01-020-801-A     | AMM 72-10-01   | Re-equilibrar si >2 palas cambiadas       |
| CWL3-SVC (par)    | Rem/Inst  | 72-10-02-020-801-A     | AMM 72-10-02   | Suministro pareado (matching)             |
| SPN4-SVC          | Rem/Inst  | 72-10-03-020-801-A     | AMM 72-10-03   | Revisar holguras                          |
| SHR8-SVC          | Rem/Inst  | 72-10-04-020-801-A     | AMM 72-10-04   | Inspección térmica previa                 |
| QSN5-SVC          | Test/Cal  | 72-10-10-720-801-A     | FIM 72-10-F01  | Calibración T-QCAL-100                    |
| QIC9-SVC          | Rem/Inst  | 72-10-10-020-801-A     | AMM 72-10-10   | Radio curvatura ≥ 4×Ø                      |
| FAN-MOD-OH (core) | Swap OH   | 72-10-00-040-801-A     | AMM 72-10-00   | Devolver core con etiquetas y DET         |

## Políticas MRO
- **Core return** obligatorio para FAN-MOD-OH (RMA + DET de recepción).
- Kits de fijaciones **FST7**: consumo por intervención; registrar lote en DET.
""",

        "FAN1_CROSSWALK.md": """# Crosswalk EBOM → MBOM → SBOM (FAN1, ATA 72-10)

| EBOM (CI_Code) | MBOM (Nivel/Ítem)                       | SBOM (N.º Servicio) | Observaciones |
|----------------|-----------------------------------------|---------------------|---------------|
| BLD1           | L2: BLD1 ×24 (rotor)                    | BLD1-SVC (unidad)   | FRU individual; re-equilibrado si >2   |
| HUB2           | L2: HUB2 ×1                             | HUB2-NR             | No-reemplazable (D-Level)              |
| BRH6           | L2: BRH6 ×24                            | BRH6-NR             | Integrado al cubo en servicio          |
| FST7           | Explosión: FST7-B/N/W (96 c/u)          | KIT-BLD-FST-01      | EBOM set→MBOM piezas; SBOM Kit         |
| CWL3           | L1: CWL3 ×2                             | CWL3-SVC            | Par emparejado                          |
| SPN4           | L1: SPN4 ×1                             | SPN4-SVC            | FRU O-Level                             |
| SHR8           | L1: SHR8 ×1                             | SHR8-SVC            | Inspección térmica previa               |
| QSN5           | L2: QSN5 ×4                             | QSN5-SVC            | Recalibración T-QCAL-100                |
| QIC9           | L2: QIC9 ×2                             | QIC9-SVC            | Verif. conectores/routing               |
""",

        "FAN1_QAUDIT.yaml": """# QAUDIT stubs
---
id: "DET:SE:ppp:SE:FAN1-MBOM:V9.0"
owner: "Manufacturing Engineering Lead"
signer: "PQC-Dilithium3"
qaudit: { reviewer: "Compliance", verdict: "pending" }
links:
  - "AMP-BWB-Q100-25MAP0001-MFG-BOM-ENG-AS-PA-FAN1-RDIG-072-10-00-v9.0.0"
  - "WI-72-10-00 .. WI-72-10-19"
  - "SE:ppp:ROT-A"
---
id: "DET:SE:ppp:SE:FAN1-SBOM:V9.0"
owner: "MRO Engineering Lead"
signer: "PQC-Dilithium3"
qaudit: { reviewer: "CAS Authority", verdict: "pending" }
links:
  - "AMP-BWB-Q100-25MAP0001-MRO-IPC-ENG-AS-PA-FAN1-RDIG-072-10-00-v9.0.0"
  - "AMM/FIM refs"
  - "IPC Kit: KIT-BLD-FST-01"
"""
    }

    for name, content in files_root.items():
        with open(os.path.join(base, name), "w", encoding="utf-8") as f:
            f.write(content)

    # Events JSON
    events = {
        "CAM.MBOMReleased.json": {
            "event": "CAM.MBOMReleased",
            "ts": "2025-12-02T12:10:00Z",
            "program": "BWB-Q100",
            "domain": "ppp",
            "asset": "FAN1",
            "utcs_mi_id": "EstándarUniversal:Artefacto-ListaMateriales-ATA+S1000D-72.10-ManufacturingBOM-0001-v9.0-Aerospace and Quantum United Advanced Venture-GeneracionHybrida-ppp-Amedeo Pelliccia-7f2a9c41-RestoDeVidaUtil",
            "det_ref": "DET:SE:ppp:SE:FAN1-MBOM:V9.0",
            "signature": "PQC-Dilithium3",
            "meta": { "bop": ["SE:ppp:ROT-A","SE:ppp:BAL-01","SE:ppp:CLEAN","SE:ppp:INTEG","SE:ppp:FINAL"] }
        },
        "CAS.SBOMReleased.json": {
            "event": "CAS.SBOMReleased",
            "ts": "2025-12-02T12:12:00Z",
            "program": "BWB-Q100",
            "domain": "ppp",
            "asset": "FAN1",
            "utcs_mi_id": "EstándarUniversal:Artefacto-CatalogoPiezas-ATA+S1000D-72.10-ServiceBOM-0001-v9.0-Aerospace and Quantum United Advanced Venture-GeneracionHybrida-ppp-Amedeo Pelliccia-c18e04d3-RestoDeVidaUtil",
            "det_ref": "DET:SE:ppp:SE:FAN1-SBOM:V9.0",
            "signature": "PQC-Dilithium3",
            "meta": { "ipc": ["BLD1-SVC","KIT-BLD-FST-01","FAN-MOD-OH"] }
        }
    }
    for name, payload in events.items():
        with open(os.path.join(base, name), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    # --- 2) Schemas ---
    schemas_dir = os.path.join(base, "ems/schemas")
    os.makedirs(schemas_dir, exist_ok=True)

    schemas = {
        "envelope.schema.json": r"""{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "QAL Event Envelope",
  "type": "object",
  "required": ["event","ts","producer","payload","signature","hash"],
  "properties": {
    "event": { "type": "string" },
    "ts": { "type": "string", "format": "date-time" },
    "producer": { "type": "string", "minLength": 2 },
    "payload": { "type": "object" },
    "signature": {
      "type": "object",
      "required": ["scheme","value"],
      "properties": {
        "scheme": { "type": "string", "enum": ["PQC-Dilithium3","PQC-Falcon","PQC-SPHINCS+"] },
        "value": { "type": "string", "pattern": "^[A-Za-z0-9+/=_-]{20,}$" }
      },
      "additionalProperties": false
    },
    "hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" }
  },
  "additionalProperties": false
}""",

        "QICOCA.QS.Published.schema.json": r"""{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "QICOCA.QS.Published",
  "type": "object",
  "required": ["program","domain","level","entity","qs_type","utcs_mi_id","det_ref"],
  "properties": {
    "program": { "type": "string", "minLength": 3 },
    "domain": { "type": "string", "pattern": "^(?:[A-Z]{3}|ppp)$" },
    "level":  { "type": "string", "enum": ["CI","CE","CC","CP","FE","DI","SE","SI","CV","TFA","QS"] },
    "entity": { "type": "string", "minLength": 2 },
    "qs_type":{ "type": "string", "enum": ["QUBO","VQE","QML"] },
    "utcs_mi_id": {
      "type": "string",
      "pattern": "^EstándarUniversal:.+-.+-.+-[A-Z0-9]+-\\d{2}\\.\\d{2}-.+?-\\d{4}-v\\d+\\.\\d+-.+?-(GeneracionHumana|GeneracionHybrida|GeneracionAuto)-(AIR|SPACE|DEFENSE|GROUND|CROSS)-.+?-([a-fA-F0-9]{8})-.+$"
    },
    "det_ref": {
      "type": "string",
      "pattern": "^DET:QS:(?:[A-Z]{3}|ppp):QS:[A-Za-z0-9\\-]+:V\\d+\\.\\d+$"
    }
  },
  "additionalProperties": true
}""",

        "CAMPOS.CAM.MBOMReleased.schema.json": r"""{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CAMPOS.CAM.MBOMReleased",
  "type": "object",
  "required": ["program","domain","asset","mbom_ref","revision","utcs_mi_id","det_ref"],
  "properties": {
    "program": { "type": "string" },
    "domain":  { "type": "string", "pattern": "^(?:[A-Z]{3}|ppp)$" },
    "asset":   { "type": "string" },
    "mbom_ref":{ "type": "string", "pattern": "\\.?ya?ml$" },
    "revision":{ "type": "string", "pattern": "^V\\d+\\.\\d+$" },
    "utcs_mi_id": {
      "type": "string",
      "pattern": "^EstándarUniversal:.+$"
    },
    "det_ref": {
      "type": "string",
      "pattern": "^DET:SE:(?:[A-Z]{3}|ppp):SE:[A-Za-z0-9\\-]+:V\\d+\\.\\d+$"
    }
  },
  "additionalProperties": false
}""",

        "CAMPOS.CAS.SBOMReleased.schema.json": r"""{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CAMPOS.CAS.SBOMReleased",
  "type": "object",
  "required": ["program","domain","asset","sbom_ref","lockfile_sha256","utcs_mi_id","det_ref"],
  "properties": {
    "program": { "type": "string" },
    "domain":  { "type": "string", "pattern": "^(?:[A-Z]{3}|ppp)$" },
    "asset":   { "type": "string" },
    "sbom_ref":{ "type": "string", "pattern": "\\.?ya?ml$" },
    "lockfile_sha256": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
    "spdx_id": { "type": "string" },
    "utcs_mi_id": { "type": "string", "pattern": "^EstándarUniversal:.+$" },
    "det_ref": {
      "type": "string",
      "pattern": "^DET:SE:(?:[A-Z]{3}|ppp):SE:[A-Za-z0-9\\-]+:V\\d+\\.\\d+$"
    }
  },
  "additionalProperties": false
}""",

        "CADEV.CAV.ComplianceRolledUp.schema.json": r"""{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CADEV.CAV.ComplianceRolledUp",
  "type": "object",
  "required": ["program","domain","artifact","rule_id","status","utcs_mi_id","det_ref"],
  "properties": {
    "program": { "type": "string" },
    "domain":  { "type": "string", "pattern": "^(?:[A-Z]{3}|ppp)$" },
    "artifact":{ "type": "string" },
    "rule_id": { "type": "string", "pattern": "^BRK-[A-Z]+-\\d{3}$" },
    "status":  { "type": "string", "enum": ["Compliant","NonCompliant","InProgress","NotApplicable"] },
    "utcs_mi_id": { "type": "string", "pattern": "^EstándarUniversal:.+$" },
    "det_ref": {
      "type": "string",
      "pattern": "^DET:(QS|SE|DI|CE|CC|CI|CP|FE):(?:[A-Z]{3}|ppp):[A-Z]{2}:[A-Za-z0-9\\-]+:V\\d+\\.\\d+$"
    },
    "evidence_url": { "type": "string" }
  },
  "additionalProperties": false
}"""
    }
    for name, content in schemas.items():
        with open(os.path.join(schemas_dir, name), "w", encoding="utf-8") as f:
            f.write(content)

    # --- 3) Samples ---
    samples_dir = os.path.join(base, "samples")
    os.makedirs(samples_dir, exist_ok=True)
    samples = {
        "qs_payload.json": {
            "program": "Aerospace And Quantum United Advanced Venture",
            "domain": "ppp",
            "level": "QS",
            "entity": "FAN1-AuthorityMap",
            "qs_type": "QUBO",
            "utcs_mi_id": "EstándarUniversal:Especificacion-Validacion-ARP-4754A-00.00-QScoreQuantumSpecification-0001-v1.0-Aerospace-And-Quantum-United-Advanced-Venture-GeneracionHumana-CROSS-Amedeo-Pelliccia-8d7c2a1b-RestoDeVidaUtil",
            "det_ref": "DET:QS:ppp:QS:FAN1-AuthorityMap:V1.1"
        },
        "mbom_payload.json": {
            "program": "BWB-Q100",
            "domain": "ppp",
            "asset": "FAN1",
            "mbom_ref": "docs/CAMPOS/CAM/MBOM/MBOM-FAN1.yaml",
            "revision": "V1.1",
            "utcs_mi_id": "EstándarUniversal:Documento-Implementacion-ARP4754A-46.00-ManufacturingBillOfMaterialsRelease-0001-v1.0-Aerospace And Quantum United Advanced Venture-GeneracionHumana-CROSS-Amedeo Pelliccia-deadbeef-RestoDeVidaUtil",
            "det_ref": "DET:SE:ppp:SE:FAN1-MBOM:V1.1"
        },
        "sbom_payload.json": {
            "program": "BWB-Q100",
            "domain": "ppp",
            "asset": "FAN1",
            "sbom_ref": "docs/CAMPOS/CAS/SBOM/SBOM-FAN1.yaml",
            "lockfile_sha256": "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            "spdx_id": "SPDXRef-DOCUMENT",
            "utcs_mi_id": "EstándarUniversal:Documento-Implementacion-ISO27001-00.00-SoftwareBillOfMaterialsRelease-0001-v1.0-Aerospace And Quantum United Advanced Venture-GeneracionHumana-CROSS-Amedeo Pelliccia-cafebabe-RestoDeVidaUtil",
            "det_ref": "DET:SE:ppp:SE:FAN1-SBOM:V1.1"
        },
        "compliance_payload.json": {
            "program": "Aerospace And Quantum United Advanced Venture",
            "domain": "ppp",
            "artifact": "ANMN-Reflex-Layer",
            "rule_id": "BRK-IA-001",
            "status": "InProgress",
            "utcs_mi_id": "EstándarUniversal:Politica-Validacion-ARP4754A-00.00-ComplianceRollupForANMN-0001-v1.0-Aerospace And Quantum United Advanced Venture-GeneracionHumana-CROSS-Amedeo Pelliccia-baddcafe-RestoDeVidaUtil",
            "det_ref": "DET:DI:ppp:DI:ANMN-Reflex:V0.3",
            "evidence_url": "https://example.local/det/ANMN-Reflex-V0.3"
        }
    }
    for name, payload in samples.items():
        with open(os.path.join(samples_dir, name), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    # --- 4) EMS Utilities ---
    ems_dir = os.path.join(base, "ems")
    os.makedirs(ems_dir, exist_ok=True)
    
    # Create emit.mjs
    with open(os.path.join(ems_dir, "emit.mjs"), "w", encoding="utf-8") as f:
        f.write(textwrap.dedent("""\
        #!/usr/bin/env node
        /**
         * emit.mjs - Event emission utility with schema validation
         */
        import fs from "fs";
        import path from "path";
        import crypto from "crypto";
        import Ajv from "ajv";
        import addFormats from "ajv-formats";

        const ajv = new Ajv({ allErrors: true, strict: false });
        addFormats(ajv);

        // Parse command line arguments
        const argv = {};
        const args = process.argv.slice(2);
        for (let i = 0; i < args.length; i++) {
          const arg = args[i];
          if (arg.startsWith('--')) {
            if (arg.includes('=')) {
              // Format: --key=value
              const [key, ...valueParts] = arg.substring(2).split('=');
              argv[key] = valueParts.join('=');
            } else {
              // Format: --key value
              const key = arg.substring(2);
              const nextArg = args[i + 1];
              if (nextArg && !nextArg.startsWith('--')) {
                argv[key] = nextArg;
                i++; // Skip next argument
              } else {
                argv[key] = true;
              }
            }
          }
        }

        const TYPE = argv.type || "QICOCA.QS.Published";
        const PAYLOAD_FILE = argv.payload;
        const OUT_DIR = argv.out || "events/out";
        const SCHEMAS_DIR = argv.schemas || "ems/schemas";

        if (!PAYLOAD_FILE || PAYLOAD_FILE === true) {
          console.error("Usage: node ems/emit.mjs --type=EVENT_TYPE --payload=payload.json [--out=events/out] [--schemas=ems/schemas]");
          console.error("Received payload:", PAYLOAD_FILE, typeof PAYLOAD_FILE);
          process.exit(1);
        }

        function validatePayload(payload, schemaPath) {
          if (!fs.existsSync(schemaPath)) {
            console.warn(`Schema not found: ${schemaPath}`);
            return true;
          }
          
          const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
          const validate = ajv.compile(schema);
          const valid = validate(payload);
          
          if (!valid) {
            console.error("Validation errors:", validate.errors);
            return false;
          }
          return true;
        }

        function emitEvent() {
          fs.mkdirSync(OUT_DIR, { recursive: true });
          
          const payload = JSON.parse(fs.readFileSync(PAYLOAD_FILE, "utf8"));
          const ts = new Date().toISOString();
          const payloadStr = JSON.stringify(payload, null, 2);
          const hash = "sha256:" + crypto.createHash("sha256").update(payloadStr).digest("hex");
          
          const envelope = {
            event: TYPE,
            ts,
            producer: "EMS-Emitter",
            payload,
            signature: {
              scheme: "PQC-Dilithium3",
              value: "mock_signature_" + Math.random().toString(36).substr(2, 20)
            },
            hash
          };

          // Validate against schema if available
          const schemaFile = `${TYPE}.schema.json`;
          const schemaPath = path.join(SCHEMAS_DIR, schemaFile);
          
          if (!validatePayload(payload, schemaPath)) {
            console.error("Payload validation failed");
            process.exit(1);
          }

          const outFile = path.join(OUT_DIR, `${TYPE.replace(/\\./g, "_")}_${Date.now()}.json`);
          fs.writeFileSync(outFile, JSON.stringify(envelope, null, 2));
          
          console.log(`✓ Event emitted: ${outFile}`);
          console.log(`  Type: ${TYPE}`);
          console.log(`  Hash: ${hash.substr(0, 16)}...`);
          
          return outFile;
        }

        emitEvent();
        """))

    # Create validate.mjs
    with open(os.path.join(ems_dir, "validate.mjs"), "w", encoding="utf-8") as f:
        f.write(textwrap.dedent("""\
        #!/usr/bin/env node
        /**
         * validate.mjs - Validate events against schemas
         */
        import fs from "fs";
        import path from "path";
        import { glob } from "glob";
        import Ajv from "ajv";
        import addFormats from "ajv-formats";

        const ajv = new Ajv({ allErrors: true, strict: false });
        addFormats(ajv);

        const [eventsDir, schemasDir] = process.argv.slice(2);
        
        if (!eventsDir || !schemasDir) {
          console.error("Usage: node ems/validate.mjs <events-dir> <schemas-dir>");
          process.exit(1);
        }

        async function validateEvents() {
          const eventFiles = await glob(path.join(eventsDir, "*.json"));
          let errors = 0;
          
          console.log(`Validating ${eventFiles.length} event files...`);
          
          for (const eventFile of eventFiles) {
            try {
              const event = JSON.parse(fs.readFileSync(eventFile, "utf8"));
              const eventType = event.event || path.basename(eventFile).split("_")[0];
              
              const schemaFile = path.join(schemasDir, `${eventType}.schema.json`);
              
              if (!fs.existsSync(schemaFile)) {
                console.warn(`⚠ No schema found for ${eventType}: ${eventFile}`);
                continue;
              }
              
              const schema = JSON.parse(fs.readFileSync(schemaFile, "utf8"));
              const validate = ajv.compile(schema);
              
              // Validate payload if it's an envelope, otherwise validate the whole event
              const target = event.payload || event;
              const valid = validate(target);
              
              if (!valid) {
                console.error(`✗ ${eventFile}:`);
                validate.errors.forEach(err => {
                  console.error(`  - ${err.instancePath}: ${err.message}`);
                });
                errors++;
              } else {
                console.log(`✓ ${eventFile}`);
              }
              
            } catch (e) {
              console.error(`✗ ${eventFile}: ${e.message}`);
              errors++;
            }
          }
          
          console.log(`\\nValidation complete: ${eventFiles.length - errors}/${eventFiles.length} passed`);
          return errors === 0;
        }

        const success = await validateEvents();
        process.exit(success ? 0 : 1);
        """))

    # Create watcher
    with open(os.path.join(ems_dir, "watch.mjs"), "w", encoding="utf-8") as f:
        f.write(textwrap.dedent("""\
        #!/usr/bin/env node
        /**
         * EMS Watcher mejorado:
         *  - Emite MBOMReleased/SBOMReleased al añadir YAMLs.
         *  - Emite QICOCA.QS.Published cuando cambia alias.yml con un det_ref QS.
         */
        import chokidar from "chokidar";
        import fs from "fs";
        import path from "path";
        import { spawn } from "child_process";
        import yaml from "js-yaml";

        const OUT = "events/out";
        const SCHEMAS = "ems/schemas";

        function emit(type, payload) {
          const tmp = `.tmp_payload_${Date.now()}.json`;
          fs.writeFileSync(tmp, JSON.stringify(payload));
          spawn("node", ["ems/emit.mjs", `--type=${type}`, `--payload=${tmp}`, `--out=${OUT}`, `--schemas=${SCHEMAS}`], { stdio:"inherit" })
            .on("exit", () => { try { fs.unlinkSync(tmp); } catch {} });
          console.log("→ emitted", type, payload);
        }

        function tryEmitQSFromAlias(filePath) {
          try {
            const raw = fs.readFileSync(filePath, "utf8");
            const y = yaml.load(raw) || {};
            const det =
              y?.QS?.det_ref ||
              y?.det_qs ||
              (raw.match(/DET:QS:(?:[A-Z]{3}|ppp):QS:[A-Za-z0-9\\-]+:V\\d+\\.\\d+/) || [])[0];
            if (!det) return;
            const domain = (raw.match(/\\b(?:AAA|AAP|CCC|CQH|DDD|EDI|EEE|EER|IIF|IIS|LCC|LIB|MMM|OOO|ppp)\\b/) || ["ppp"])[0];
            const entity = y?.QS?.entity || path.basename(path.dirname(filePath));
            emit("QICOCA.QS.Published", {
              program: "Aerospace And Quantum United Advanced Venture",
              domain,
              level: "QS",
              entity,
              qs_type: "QUBO",
              utcs_mi_id: "EstándarUniversal:Especificacion-Validacion-ARP4754A-00.00-QScoreQuantumSpecification-0001-v1.0-Aerospace And Quantum United Advanced Venture-GeneracionHumana-CROSS-Amedeo Pelliccia-8d7c2a1b-RestoDeVidaUtil",
              det_ref: det
            });
          } catch { /* noop */ }
        }

        chokidar
          .watch([
            "docs/CAMPOS/CAM/MBOM/MBOM-*.y?(a)ml",
            "docs/CAMPOS/CAS/SBOM/SBOM-*.y?(a)ml",
            "docs/**/alias.yml"
          ], { ignoreInitial: true })
          .on("add", (p) => {
            const norm = p.replace(/\\\\/g,"/");
            if (/CAMPOS\\/CAM\\/MBOM\\/MBOM-.+\\.ya?ml$/.test(norm)) {
              const y = yaml.load(fs.readFileSync(p,"utf8")) || {};
              emit("CAMPOS.CAM.MBOMReleased", {
                program: "BWB-Q100",
                domain: "ppp",
                asset: y?.asset || "FAN1",
                mbom_ref: norm,
                revision: y?.revision || "V1.1",
                utcs_mi_id: "EstándarUniversal:Documento-Implementacion-ARP4754A-46.00-ManufacturingBillOfMaterialsRelease-0001-v1.0-Aerospace And Quantum United Advanced Venture-GeneracionHumana-CROSS-Amedeo Pelliccia-deadbeef-RestoDeVidaUtil",
                det_ref: "DET:SE:ppp:SE:FAN1-MBOM:V1.1"
              });
            }
            if (/CAMPOS\\/CAS\\/SBOM\\/SBOM-.+\\.ya?ml$/.test(norm)) {
              const y = yaml.load(fs.readFileSync(p,"utf8")) || {};
              emit("CAMPOS.CAS.SBOMReleased", {
                program: "BWB-Q100",
                domain: "ppp",
                asset: y?.asset || "FAN1",
                sbom_ref: norm,
                lockfile_sha256: y?.lockfile_sha256 || "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
                utcs_mi_id: "EstándarUniversal:Documento-Implementacion-ISO27001-00.00-SoftwareBillOfMaterialsRelease-0001-v1.0-Aerospace And Quantum United Advanced Venture-GeneracionHumana-CROSS-Amedeo Pelliccia-cafebabe-RestoDeVidaUtil",
                det_ref: "DET:SE:ppp:SE:FAN1-SBOM:V1.1"
              });
            }
          })
          .on("change", (p) => {
            if (/alias\\.yml$/.test(p)) tryEmitQSFromAlias(p);
          });

        console.log("👀 EMS watcher activo: MBOM/SBOM/alias.yml");
        """))

    # --- 5) Scripts directory and gen_matrix ---
    scripts_dir = os.path.join(base, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    with open(os.path.join(scripts_dir, "gen_matrix.mjs"), "w", encoding="utf-8") as f:
        f.write(textwrap.dedent("""\
        #!/usr/bin/env node
        /**
         * gen_matrix.mjs v1.1 (robusto)
         */
        import fs from "fs/promises";
        import fss from "fs";
        import path from "path";

        const argv = Object.fromEntries(
          process.argv.slice(2).map((v) => {
            const [k, ...rest] = v.replace(/^--/, "").split("=");
            return [k, rest.join("=") || true];
          })
        );

        const BASE = argv.base || "docs/C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000";
        const README = argv.readme || "README.md";
        const MARK_START = argv.start || "BEGIN:DOMAIN_MATRIX";
        const MARK_END = argv.end || "END:DOMAIN_MATRIX";
        const DOMAIN_RE = /^(AAA|AAP|CCC|CQH|DDD|EDI|EEE|EER|IIF|IIS|LCC|LIB|MMM|OOO|ppp)-/;

        async function exists(p) { try { await fs.access(p); return true; } catch { return false; } }
        async function listDirs(dir) {
          const ents = await fs.readdir(dir, { withFileTypes: true });
          return ents.filter(e => e.isDirectory()).map(e => path.join(dir, e.name));
        }
        const rel = (p) => path.posix.normalize(p.replace(/\\\\/g, "/"));
        function mdLink(label, relPath, anchor = "") { return `[${label}](${relPath}${anchor ? `#${anchor}` : ""})`; }
        async function findReadme(dir) { const p = path.join(dir, "README.md"); return (await exists(p)) ? p : null; }

        async function collectDomainRow(domainDirAbs) {
          const domainName = path.basename(domainDirAbs);
          const code = domainName.split("-")[0];
          const desc = domainName.split("-").slice(1).join(" ").replace(/_/g, " ");

          const domainReadme = await findReadme(domainDirAbs);
          const domainReadmeRel = domainReadme ? rel(path.relative(process.cwd(), domainReadme)) : "";

          const subdirs = await listDirs(domainDirAbs);
          const diDir = subdirs.find(d => path.basename(d).startsWith("DI-"));
          let diCell = "—";
          if (diDir) {
            const diReadme = path.join(diDir, "README.md");
            diCell = fss.existsSync(diReadme)
              ? mdLink("DI", rel(path.relative(process.cwd(), diReadme)))
              : (domainReadme ? mdLink("DI", domainReadmeRel, "di") : "—");
          } else if (domainReadme) {
            diCell = mdLink("DI", domainReadmeRel, "di");
          }

          const ceDirs = subdirs.filter(d => path.basename(d).startsWith("CE-"));
          let ceCell = "—";
          if (ceDirs.length) {
            const top = ceDirs.slice(0, 3).map(d => {
              const name = path.basename(d).replace(/^CE-/, "");
              const ceReadme = path.join(d, "README.md");
              const link = fss.existsSync(ceReadme) ? rel(path.relative(process.cwd(), ceReadme)) : rel(path.relative(process.cwd(), d));
              return mdLink(name, link);
            });
            ceCell = top.join(" · ");
          } else if (domainReadme) {
            ceCell = mdLink("CE", domainReadmeRel, "ce");
          }

          const linkOrDash = (tag) => domainReadme ? mdLink(tag, domainReadmeRel, tag.toLowerCase()) : "—";
          const siLink = linkOrDash("SI");
          const cvLink = linkOrDash("CV");
          const seLink = linkOrDash("SE");
          const ccLink = linkOrDash("CC");
          const ciLink = linkOrDash("CI");
          const cpLink = linkOrDash("CP");
          const feLink = linkOrDash("FE");
          const qsLink = (await exists(path.join(domainDirAbs, "alias.yml")))
            ? mdLink("QS", rel(path.relative(process.cwd(), path.join(domainDirAbs, "alias.yml"))))
            : linkOrDash("QS");

          const tfaLink = mdLink("TFA", "docs/C-AMEDEO-FRAMEWORK/README.md", "tfa-bwb");

          return `| **${code}** | ${desc} | ${tfaLink} | ${siLink} | ${cvLink} | ${seLink} | ${diCell} | ${ceCell} | ${ccLink} | ${ciLink} | ${cpLink} | ${feLink} | ${qsLink} |`;
        }

        async function buildMatrix() {
          const candidates = (await listDirs(BASE)).filter(d => DOMAIN_RE.test(path.basename(d)));
          const ORDER = ["AAA","AAP","CCC","CQH","DDD","EDI","EEE","EER","IIF","IIS","LCC","LIB","MMM","OOO","ppp"];
          const idx = (p) => ORDER.indexOf(path.basename(p).split("-")[0]);
          const domains = candidates.sort((a,b)=> idx(a)-idx(b));

          const header =
        `| Domain  | Description |       TFA       |   SI   |   CV   |   SE   |   DI   |    CE     |   CC   |   CI   |   CP   |   FE   |   QS   |
        |---------|-------------|:---------------:|:------:|:------:|:------:|:------:|:---------:|:------:|:------:|:------:|:------:|:------:|`;

          const rows = await Promise.all(domains.map(d => collectDomainRow(d)));
          return `${header}\\n${rows.join("\\n")}\\n`;
        }

        async function patchReadme(table) {
          const rd = await fs.readFile(README, "utf8");
          const start = `<!-- ${MARK_START} -->`;
          const end = `<!-- ${MARK_END} -->`;
          const block = `${start}\\n${table}${end}`;
          const out = (rd.includes(start) && rd.includes(end))
            ? rd.replace(new RegExp(`${start}[\\\\s\\\\S]*?${end}`), block)
            : rd.trimEnd() + `\\n\\n${block}\\n`;
          await fs.writeFile(README, out, "utf8");
          console.log("✔ Matriz actualizada en", README);
        }

        const table = await buildMatrix();
        await patchReadme(table);
        """))

    # --- 6) Seeds for watcher ---
    seed_paths = [
        "docs/CAMPOS/CAM/MBOM",
        "docs/CAMPOS/CAS/SBOM",
        "docs/ppp-DOMAIN"
    ]
    for p in seed_paths:
        os.makedirs(os.path.join(base, p), exist_ok=True)

    with open(os.path.join(base, "docs/CAMPOS/CAM/MBOM/MBOM-FAN1.yaml"), "w", encoding="utf-8") as f:
        f.write("asset: FAN1\nrevision: V1.1\nitems:\n  - pn: FAN1-HOUSING\n    qty: 1\n")

    with open(os.path.join(base, "docs/CAMPOS/CAS/SBOM/SBOM-FAN1.yaml"), "w", encoding="utf-8") as f:
        f.write("asset: FAN1\nlockfile_sha256: sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef\ncomponents:\n  - name: control-fw\n    version: 1.2.3\n")

    with open(os.path.join(base, "docs/ppp-DOMAIN/alias.yml"), "w", encoding="utf-8") as f:
        f.write("QS:\n  entity: FAN1-AuthorityMap\n  det_ref: DET:QS:ppp:QS:FAN1-AuthorityMap:V1.1\n")

    # --- 7) package.json snippet & CI snippet ---
    with open(os.path.join(base, "package.json"), "w", encoding="utf-8") as f:
        f.write(textwrap.dedent("""\
        {
          "name": "brk-ds-ems-dropin",
          "version": "1.0.0",
          "type": "module",
          "description": "BRK Data Sync EMS Drop-in Bundle",
          "scripts": {
            "matrix": "node scripts/gen_matrix.mjs --base docs/C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000 --readme README.md --start BEGIN:DOMAIN_MATRIX --end END:DOMAIN_MATRIX",
            "ems:emit": "node ems/emit.mjs",
            "ems:emit:qs": "node ems/emit.mjs --type QICOCA.QS.Published --payload samples/qs_payload.json",
            "ems:emit:mbom": "node ems/emit.mjs --type CAMPOS.CAM.MBOMReleased --payload samples/mbom_payload.json",
            "ems:emit:sbom": "node ems/emit.mjs --type CAMPOS.CAS.SBOMReleased --payload samples/sbom_payload.json",
            "ems:emit:compliance": "node ems/emit.mjs --type CADEV.CAV.ComplianceRolledUp --payload samples/compliance_payload.json",
            "ems:validate": "node ems/validate.mjs events/out ems/schemas",
            "ems:watch": "node ems/watch.mjs",
            "test": "npm run ems:emit:qs && npm run ems:emit:mbom && npm run ems:emit:sbom && npm run ems:validate"
          },
          "dependencies": {
            "ajv": "^8.17.1",
            "ajv-formats": "^3.0.1",
            "chokidar": "^3.6.0",
            "js-yaml": "^4.1.0",
            "glob": "^11.0.0"
          },
          "engines": { "node": ">=18.0.0" }
        }
        """))

    with open(os.path.join(base, "CI_snippet.yml"), "w", encoding="utf-8") as f:
        f.write(textwrap.dedent("""\
        - name: Install BRK DS EMS Dependencies
          run: npm ci
          working-directory: ./brk-ds-ems

        - name: Build Domain Matrix
          run: npm run matrix
          working-directory: ./brk-ds-ems

        - name: Emit sample events
          run: |
            npm run ems:emit:qs
            npm run ems:emit:mbom
            npm run ems:emit:sbom
            npm run ems:emit:compliance
          working-directory: ./brk-ds-ems

        - name: EMS validate events
          run: npm run ems:validate
          working-directory: ./brk-ds-ems

        - name: Start EMS watcher (background)
          run: npm run ems:watch &
          working-directory: ./brk-ds-ems
        """))

    # README for the bundle
    with open(os.path.join(base, "README.md"), "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(f"""\
        # BRK Data Sync — EMS Drop-in Bundle
        
        This bundle contains a complete Event Management System (EMS) for AMEDEO/QAL integration.
        
        Generated on: {datetime.now().isoformat()}
        
        ## Contents
        
        - **Root Files**: FAN1 MBOM/SBOM documentation and crosswalk
        - **ems/**: Event management utilities and schemas
        - **samples/**: Sample event payloads
        - **scripts/**: Matrix generation and utilities
        - **docs/**: Seed structures for testing
        
        ## Quick Start
        
        1. Extract bundle to your project
        2. `npm ci`
        3. `npm test`
        4. `npm run ems:watch` (for live file watching)
        
        ## Event Types Supported
        
        - `QICOCA.QS.Published` - Quantum Score events
        - `CAMPOS.CAM.MBOMReleased` - Manufacturing BOM releases
        - `CAMPOS.CAS.SBOMReleased` - Service BOM releases  
        - `CADEV.CAV.ComplianceRolledUp` - Compliance status updates
        
        ## Schema Validation
        
        All events are validated against JSON schemas in `ems/schemas/`.
        Use `npm run ems:validate` to check generated events.
        
        ## File Watching
        
        The EMS watcher monitors:
        - `docs/CAMPOS/CAM/MBOM/MBOM-*.yaml`
        - `docs/CAMPOS/CAS/SBOM/SBOM-*.yaml` 
        - `docs/**/alias.yml`
        
        ## Integration
        
        See `CI_snippet.yml` for GitHub Actions integration example.
        """))

    # README anchors helper
    os.makedirs(os.path.join(base, "docs/example-domain"), exist_ok=True)
    with open(os.path.join(base, "docs/example-domain/README.md"), "w", encoding="utf-8") as f:
        f.write(textwrap.dedent("""\
        # Example Domain README

        ## SI
        ## CV
        ## SE
        ## DI
        ## CE
        ## CC
        ## CI
        ## CP
        ## FE
        ## QS
        """))

    # Create events/out directory placeholder
    os.makedirs(os.path.join(base, "events/out"), exist_ok=True)
    with open(os.path.join(base, "events/out/.gitkeep"), "w") as f:
        f.write("# Events output directory\n")

    return base


def create_zip_bundle(base_dir):
    """Create zip bundle from base directory"""
    zip_path = "/mnt/data/BRK_DS_dropin.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(base_dir):
            for fn in files:
                fp = os.path.join(root, fn)
                z.write(fp, arcname=os.path.relpath(fp, base_dir))
    return zip_path


def print_tree_structure(dir_path, max_depth=3):
    """Print directory tree structure"""
    def _tree(path, prefix="", depth=0):
        if depth > max_depth:
            return
        
        items = []
        try:
            items = sorted(os.listdir(path))
        except (PermissionError, FileNotFoundError):
            return
            
        for i, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item}")
            
            if os.path.isdir(item_path) and depth < max_depth:
                next_prefix = prefix + ("    " if is_last else "│   ")
                _tree(item_path, next_prefix, depth + 1)

    print(f"📁 {os.path.basename(dir_path)}/")
    _tree(dir_path)


def main():
    """Main function to create the drop-in bundle"""
    print("🚀 Creating BRK DS drop-in bundle...")
    
    # Create the bundle
    base_dir = create_brk_ds_dropin()
    print(f"✅ Bundle created at: {base_dir}")
    
    # Show structure
    print("\n📋 Bundle structure:")
    print_tree_structure(base_dir)
    
    # Create zip
    zip_path = create_zip_bundle(base_dir)
    zip_size = os.path.getsize(zip_path) / 1024 / 1024
    print(f"\n📦 Zip bundle created: {zip_path} ({zip_size:.2f} MB)")
    
    # Count files
    file_count = sum([len(files) for r, d, files in os.walk(base_dir)])
    print(f"📊 Total files: {file_count}")
    
    print("\n🎯 Bundle ready for download!")


if __name__ == "__main__":
    main()