# QAL Taxonomía Extendida — BWB-Q100

**UTCS-MI v5.0 (encabezado canónico)**  
`EstándarUniversal:Artefacto-DesgloseDeProducto-ATA+S1000D-01.00-ProductBreakdownStructure-0001-v1.1-Ampel Treinta Sesenta Hidrogeno Blended Wing Body Q100-GeneracionHybrida-CROSS-Amedeo Pelliccia-deadbeef-RestoDeVidaUtil`

---

## Navegación

* **Índice dominio×nivel:** [docs/taxonomy/index-table.md](taxonomy/index-table.md)
* **Paquete de anclas:** [docs/taxonomy/anchors.html](taxonomy/anchors.html)
* **Diagrama de taxonomía:** [docs/diagrams/qal-taxonomy.svg](diagrams/qal-taxonomy.svg)
* **Dominios (placeholders):** [docs/taxonomy/placeholders/AAA.md](taxonomy/placeholders/AAA.md) *(AAP, CCC, …, ppp generados por script)*

> Sugerencia de inclusión (según tu stack):
>
> * MkDocs: usa `!include` o extensiones equivalentes.
> * Docusaurus/MDX: importa con `import` y `<Anchor />`/`<Markdown>`.

---

## 1) Taxonomía QAL extendida (definiciones + compatibilidad)

| Sigla   | Nombre                                     | Propósito                                                                      | Cardinalidad típica         | Ancla canónica                   | Compat / alias legado                                                                                                   |
| ------- | ------------------------------------------ | ------------------------------------------------------------------------------ | --------------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **TFA** | **Tail Final Asset / Top Figure Aircraft** | Activo final del programa (la aeronave o configuración "top")                  | 1 por programa / build      | `#tfa-<program>`                 | Sustituye "TA Top Assembly" → alias `#ta-bwb` apuntando a `#tfa-bwb`                                                    |
| **SI**  | **System Integration**                     | Línea base de integración de sistemas, *bring‑up* y orquestación interdominios | 1..n por build              | `#si-<dom>` y `#si-bwb` (global) | —                                                                                                                       |
| **CV**  | **Component Vendor**                       | Lista de proveedores aprobados (AVL) y *source control* por CI/CP/FE           | 1 por dominio / subconjunto | `#cv-<dom>`                      | Mantiene `#cv-*` previo                                                                                                 |
| **SE**  | **Station Envelop**                        | Sobre de estación / celda de producción (takt, recursos, kits)                 | n por línea                 | `#se-<dom>-NN`                   | Sustituye "SA Station Assembly" → alias `#sa-<dom>-NN` → `#se-<dom>-NN`                                                 |
| **DI**  | **Domain Interface**                       | Interfaces formales entre dominios (ICD/IFD)                                   | n por pareja de dominios    | `#di-<dom>`                      | **Cambio**: antes "Domain Invariant". Si aún lo usas, crea **legado** `#dinv-<dom>` para Invariants                     |
| **CE**  | **Component Equipped**                     | Configuración "equipada" (CI/CP + kit + vendor + as‑built)                     | n por CC/CI                 | `#ce-<dom>`                      | **Nota**: si tenías "CE = Configuration Envelope", usa `#cenv-<dom>` para ese contenido y deja `#ce-<dom>` a "Equipped" |
| **CC**  | **Component Cell**                         | Célula de configuración (subconjunto agrupador)                                | n                           | `#cc-<dom>`                      | —                                                                                                                       |
| **CI**  | **Component Item**                         | Ítem de configuración (unidad funcional)                                       | n                           | `#ci-<dom>`                      | —                                                                                                                       |
| **CP**  | **Component Particle/Part**                | Parte fabricada (PN/Rev)                                                       | n                           | `#cp-<dom>`                      | —                                                                                                                       |
| **FE**  | **Fundamental Element**                    | Elemento físico atómico (material/feature medible)                             | n                           | `#fe-<dom>`                      | —                                                                                                                       |
| **QS**  | **Quantum State**                          | Estado/resultado cuántico asociado a cualquier nivel (QUBO/VQE/QML)            | 0..n por entidad            | `#qs-<dom>-<nivel>-<id>`         | —                                                                                                                       |

> **Recomendación de compatibilidad**: mantener **alias** para no romper enlaces legados:
> `#ta-bwb → #tfa-bwb`, `#sa-* → #se-*`, `#di-* (invariant) → #dinv-*`, `#ce-* (envelope) → #cenv-*`.

---

## 2) Índice hiperlinkado **dominio × nivel** (TFA/SI/CV/SE/DI/CE/CC/CI/CP/FE/QS)

> PPP se mantiene en minúsculas `ppp`. Haz "clic" en cualquier celda para saltar.

| Dominio                                            |         **TFA** |        **SI** |        **CV** |        **SE** |        **DI** |        **CE** |        **CC** |        **CI** |        **CP** |        **FE** |        **QS** |
| -------------------------------------------------- | --------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: | ------------: |
| **AAA** Arquitecturas/Aeroestructuras/Aerodinámica | [TFA](#tfa-bwb) | [SI](#si-aaa) | [CV](#cv-aaa) | [SE](#se-aaa) | [DI](#di-aaa) | [CE](#ce-aaa) | [CC](#cc-aaa) | [CI](#ci-aaa) | [CP](#cp-aaa) | [FE](#fe-aaa) | [QS](#qs-aaa) |
| **AAP** Aeropuertos/Soporte Tierra                 | [TFA](#tfa-bwb) | [SI](#si-aap) | [CV](#cv-aap) | [SE](#se-aap) | [DI](#di-aap) | [CE](#ce-aap) | [CC](#cc-aap) | [CI](#ci-aap) | [CP](#cp-aap) | [FE](#fe-aap) | [QS](#qs-aap) |
| **CCC** Cabina/Cockpit/Carga                       | [TFA](#tfa-bwb) | [SI](#si-ccc) | [CV](#cv-ccc) | [SE](#se-ccc) | [DI](#di-ccc) | [CE](#ce-ccc) | [CC](#cc-ccc) | [CI](#ci-ccc) | [CP](#cp-ccc) | [FE](#fe-ccc) | [QS](#qs-ccc) |
| **CQH** Criogenia/Cuántica/H₂                      | [TFA](#tfa-bwb) | [SI](#si-cqh) | [CV](#cv-cqh) | [SE](#se-cqh) | [DI](#di-cqh) | [CE](#ce-cqh) | [CC](#cc-cqh) | [CI](#ci-cqh) | [CP](#cp-cqh) | [FE](#fe-cqh) | [QS](#qs-cqh) |
| **DDD** Defensa/Ciberseguridad/Safety              | [TFA](#tfa-bwb) | [SI](#si-ddd) | [CV](#cv-ddd) | [SE](#se-ddd) | [DI](#di-ddd) | [CE](#ce-ddd) | [CC](#cc-ddd) | [CI](#ci-ddd) | [CP](#cp-ddd) | [FE](#fe-ddd) | [QS](#qs-ddd) |
| **EDI** Electrónica/Instrumentos                   | [TFA](#tfa-bwb) | [SI](#si-edi) | [CV](#cv-edi) | [SE](#se-edi) | [DI](#di-edi) | [CE](#ce-edi) | [CC](#cc-edi) | [CI](#ci-edi) | [CP](#cp-edi) | [FE](#fe-edi) | [QS](#qs-edi) |
| **EEE** Medioambiente/Circularidad                 | [TFA](#tfa-bwb) | [SI](#si-eee) | [CV](#cv-eee) | [SE](#se-eee) | [DI](#di-eee) | [CE](#ce-eee) | [CC](#cc-eee) | [CI](#ci-eee) | [CP](#cp-eee) | [FE](#fe-eee) | [QS](#qs-eee) |
| **EER** Energía/Renovables                         | [TFA](#tfa-bwb) | [SI](#si-eer) | [CV](#cv-eer) | [SE](#se-eer) | [DI](#di-eer) | [CE](#ce-eer) | [CC](#cc-eer) | [CI](#ci-eer) | [CP](#cp-eer) | [FE](#fe-eer) | [QS](#qs-eer) |
| **IIF** Infraestructuras/Instalaciones             | [TFA](#tfa-bwb) | [SI](#si-iif) | [CV](#cv-iif) | [SE](#se-iif) | [DI](#di-iif) | [CE](#ce-iif) | [CC](#cc-iif) | [CI](#ci-iif) | [CP](#cp-iif) | [FE](#fe-iif) | [QS](#qs-iif) |
| **IIS** Sistemas Inteligentes/IA                   | [TFA](#tfa-bwb) | [SI](#si-iis) | [CV](#cv-iis) | [SE](#se-iis) | [DI](#di-iis) | [CE](#ce-iis) | [CC](#cc-iis) | [CI](#ci-iis) | [CP](#cp-iis) | [FE](#fe-iis) | [QS](#qs-iis) |
| **LCC** Enlaces/Comunicaciones/Control             | [TFA](#tfa-bwb) | [SI](#si-lcc) | [CV](#cv-lcc) | [SE](#se-lcc) | [DI](#di-lcc) | [CE](#ce-lcc) | [CC](#cc-lcc) | [CI](#ci-lcc) | [CP](#cp-lcc) | [FE](#fe-lcc) | [QS](#qs-lcc) |
| **LIB** Logística/Blockchain                       | [TFA](#tfa-bwb) | [SI](#si-lib) | [CV](#cv-lib) | [SE](#se-lib) | [DI](#di-lib) | [CE](#ce-lib) | [CC](#cc-lib) | [CI](#ci-lib) | [CP](#cp-lib) | [FE](#fe-lib) | [QS](#qs-lib) |
| **MMM** Mecánica/Materiales/Monitor.               | [TFA](#tfa-bwb) | [SI](#si-mmm) | [CV](#cv-mmm) | [SE](#se-mmm) | [DI](#di-mmm) | [CE](#ce-mmm) | [CC](#cc-mmm) | [CI](#ci-mmm) | [CP](#cp-mmm) | [FE](#fe-mmm) | [QS](#qs-mmm) |
| **OOO** SO/Navegación/HPC                          | [TFA](#tfa-bwb) | [SI](#si-ooo) | [CV](#cv-ooo) | [SE](#se-ooo) | [DI](#di-ooo) | [CE](#ce-ooo) | [CC](#cc-ooo) | [CI](#ci-ooo) | [CP](#cp-ooo) | [FE](#fe-ooo) | [QS](#qs-ooo) |
| **ppp** Propulsión/Combustibles                    | [TFA](#tfa-bwb) | [SI](#si-ppp) | [CV](#cv-ppp) | [SE](#se-ppp) | [DI](#di-ppp) | [CE](#ce-ppp) | [CC](#cc-ppp) | [CI](#ci-ppp) | [CP](#cp-ppp) | [FE](#fe-ppp) | [QS](#qs-ppp) |

---

## 3) Paquete de **anclas** (incluye anclas generadas automáticamente)

```html
<!-- include file: docs/taxonomy/anchors.html -->
```

---

Renderiza/expone el índice dominio×nivel:

```md
<!-- include file: docs/taxonomy/index-table.md -->
```

Diagrama (Mermaid export):

```md
![QAL Taxonomía Extendida](docs/diagrams/qal-taxonomy.svg)
```

---

## 4) Encabezados *placeholder* (ejemplo AAA) listos para rellenar

```md
# TFA — Top Figure Aircraft (BWB-Q100)
<a id="tfa-bwb"></a>
> Activo final: configuración certificable BWB-Q100. Vínculos: EBOM/MBOM, ICD global, plan de configuración.

## SI — System Integration (AAA)
<a id="si-aaa"></a>
> Integración de aeroestructura con CQH/ppp/EDI. Entregables: SI‑Baseline, issues de integración, logs de bring‑up.

## CV — Component Vendor (AAA)
<a id="cv-aaa"></a>
> AVL de AAA: CFRP (T800/M21), Ti‑6Al‑4V forjados, adhesivos estructurales. Campos: CAGE, PN, PPAP/FAI, LT.

## SE — Station Envelop (AAA)
<a id="se-aaa"></a>
> Estaciones: SE‑10 Wing‑box lower; SE‑20 Bubble array mate; SE‑30 Systems routing. Takt/recursos/kits.

## DI — Domain Interface (AAA)
<a id="di-aaa"></a>
> ICDs con CQH (contracción térmica), ppp (hardpoints BLI), EDI (SSPC routing). Versionado y verificación.

## CE — Component Equipped (AAA)
<a id="ce-aaa"></a>
> Configuración equipada: CI/CP + kit + vendor + *as‑built*. Enlace a FAI/PPAP y trazabilidad DET.

## CC — Component Cell (AAA)
<a id="cc-aaa"></a>
> Ej.: 53‑30 Multi‑bubble container (3 cells). Relación con CIs y Estaciones SE.

## CI — Component Item (AAA)
<a id="ci-aaa"></a>
> Ej.: 53‑30‑TIES (tensile ties grid). Parámetros, límites, ensayos asociados.

## CP — Component Part (AAA)
<a id="cp-aaa"></a>
> Ej.: P/N 53‑30‑01‑001 (Ti‑6Al‑4V tie). Rev, material, proceso, tolerancias MBD.

## FE — Fundamental Element (AAA)
<a id="fe-aaa"></a>
> Ej.: Preload nominal 45 kN (medible). Método de verificación, tolerancia.

## QS — Quantum State (AAA)
<a id="qs-aaa"></a>
> Estados cuánticos ligados (ej.): QUBO_budget_v2 (CAO), VQE_CFRP@20K_v1 (CAE), QML_surrogate_BLI_v3 (CAT/CFD).
```

> Repite el bloque para cada dominio (AAP, CCC, …, ppp) cambiando el identificador de ancla.

---

## 5) QS — Cómo referenciar "Quantum State" y encajarlo con DET/QAL Bus

**Identificador QS sugerido (UTCS‑MI v5.0):**

```
EstándarUniversal:EstadoCuantico-QUBO|VQE|QML-02.00-<Dominio>-<Nivel>-<Entidad>-<Secuencia>-v<Mayor.Minor>-<Programa>-<Categoría>-<Ámbito>-<Propietario>-<hash8>-RestoDeVidaUtil
```

**Ejemplos rápidos:**

* `EstándarUniversal:EstadoCuantico-QUBO-02.00-CAO-CE-BudgetVector-0007-v1.2-AmpelTreintaSesentaHidrogenoBlendedWingBodyQ100-CROSS-AMPEL360-CAO-Core-9a3f2b1c-RestoDeVidaUtil`
* `EstándarUniversal:EstadoCuantico-VQE-02.00-AAA-CI-53-30-TIES-0003-v1.0-AmpelTreintaSesentaHidrogenoBlendedWingBodyQ100-AIR-AMPEL360-CAE-Materials-7b821d44-RestoDeVidaUtil`

**Evento QAL Bus (esqueleto):**

```json
{
  "event": "QS.Published",
  "ts": "2025-09-02T00:00Z",
  "program": "AmpelTreintaSesentaHidrogenoBlendedWingBodyQ100",
  "domain": "AAA",
  "level": "CI",
  "entity": "53-30-TIES",
  "qs_type": "VQE",
  "utcs_mi_id": "EstándarUniversal:EstadoCuantico-VQE-02.00-AAA-CI-53-30-TIES-0003-v1.0-...",
  "det_ref": "DET:QS:AAA:CI:53-30-TIES:V1.0",
  "signature": "PQC-Dilithium3"
}
```

**Plantilla DET asociada:**

```
DET:QS:<DOM>:<LEVEL>:<ENTITY>:V<Major.Minor>
```

---

> Los siguientes bloques son *plantillas base*; el script ya genera 15 ficheros (AAA, AAP, …, ppp). Aquí se muestra **AAA** como ejemplo.

### TFA — Top Figure Aircraft (BWB-Q100) <a id="tfa-bwb"></a>

Activo final: build certificable **BWB-Q100**. Enlaces: EBOM/MBOM, ICD global, plan de configuración.

### SI — System Integration (AAA) <a id="si-aaa"></a>

Integración de aeroestructura con CQH/ppp/EDI. Entregables: **SI-Baseline**, issues de integración, logs de *bring-up*.

### CV — Component Vendor (AAA) <a id="cv-aaa"></a>

AVL de AAA: CFRP (T800/M21), Ti-6Al-4V, adhesivos estructurales. Campos: CAGE, PN, **PPAP/FAI**, *lead time*.

### SE — Station Envelop (AAA) <a id="se-aaa"></a>

SE-10 Wing-box lower · SE-20 Bubble array mate · SE-30 Systems routing. Definir **takt/recursos/kits**.

### DI — Domain Interface (AAA) <a id="di-aaa"></a>

ICDs con **CQH** (contracción térmica), **ppp** (hardpoints BLI), **EDI** (SSPC routing). Versionado y verificación.

### CE — Component Equipped (AAA) <a id="ce-aaa"></a>

CI/CP equipados con kit + vendor (*as-built*). Enlace a **FAI/PPAP** y trazabilidad **DET**.

### CC — Component Cell (AAA) <a id="cc-aaa"></a>

Ej.: **53-30** Multi-bubble container (3 *cells*). Relación con CIs y Estaciones SE.

### CI — Component Item (AAA) <a id="ci-aaa"></a>

Ej.: **53-30-TIES** (tensile ties grid). Parámetros, límites, ensayos.

### CP — Component Part (AAA) <a id="cp-aaa"></a>

Ej.: **P/N 53-30-01-001** (Ti-6Al-4V tie). Rev, material, proceso, tolerancias MBD.

### FE — Fundamental Element (AAA) <a id="fe-aaa"></a>

Ej.: **Preload nominal 45 kN** (medible). Método de verificación, tolerancia.

### QS — Quantum State (AAA) <a id="qs-aaa"></a>

Estados: **QUBO\_budget\_v2** (CAO), **VQE\_CFRP\@20K\_v1** (CAE), **QML\_surrogate\_BLI\_v3** (CAT/CFD).
DET asociado: `DET:QS:AAA:CI:53-30-TIES:V1.0`.

---

---

## 6) Snippets YAML "mínimos" por dominio (SE/DI/CE/CV + DET/QS)

Los archivos `qal/{DOMINIO}/kit.yaml` contienen la estructura normalizada para fluir directo al **QAL Bus** y a **DET**:

```yaml
# qal/<dominio>/kit.yaml
dom: AAA                     # dominio
programa: Ampel Treinta Sesenta Hidrogeno Blended Wing Body Q100  # canonical (sin siglas)
programa_alias:
  - BWB-Q100
  - AMPEL360

# — Station Envelop (SE) —
se:
  - id: SE-AAA-10
    objetivo: "Wing-box lower close-out"
    takt_h: 6
    recursos:
      operadores: 8
      robots: 2
      utillajes: [ "JIG-53-10-A", "VAC-INF-01" ]
    kits:
      bom_ref: "MBOM-AAA-53-10-v1.2"
      lote_min: 1
    det_ref: "DET:SE:AAA:SE-10:V1.2"

# — Domain Interface (DI) —
di:
  - id: DI-AAA↔CQH-01
    tipo: ICD
    descripcion: "Contracción térmica y clearances criogénicos"
    version: "v1.1"
    verificaciones: [ "stackup-clearance", "delta-L@20K" ]
    det_ref: "DET:DI:AAA:ICD-CQH:V1.1"

# — Component Equipped (CE) —
ce:
  - id: CE-AAA-53-30-TIES
    scope: "CI/CP equipados con kit y vendor"
    as_built: "EBOM-AAA-53-30-v3.0"
    vendor_pack: "AVL-AAA-2025Q3"
    det_ref: "DET:CE:AAA:53-30-TIES:V3.0"

# — Component Vendor (CV) —
cv:
  - cage: "L1234"
    proveedor: "Composite Advanced Europe"
    alcance: [ "CFRP-T800/M21", "adhesivo-epoxi" ]
    ppap: "PPAP-L1234-AAA-001-v1.0"
    fai:  "FAI-L1234-AAA-053-30-v1.0"
    lt_dias: 45

# — QS hooks (referenciados desde eventos) —
qs_hooks:
  - ref: "EstándarUniversal:EstadoCuantico-VQE-02.00-AAA-CI-53-30-TIES-0003-v1.0-AmpelTreintaSesentaHidrogenoBlendedWingBodyQ100-AIR-AMPEL360-CAE-Materials-7b821d44-RestoDeVidaUtil"
    det_ref: "DET:QS:AAA:CI:53-30-TIES:V1.0"
```

> Los archivos para todos los dominios (AAA, AAP, CCC, …, ppp) siguen esta estructura.

---

## 7) Esquemas (JSON Schema) para **QS.Published** y **DET IDs**

**a) Evento `QS.Published` (actualizado para UTCS-MI v5.0):**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "QS.Published",
  "type": "object",
  "required": ["event","ts","program","domain","level","entity","qs_type","utcs_mi_id","det_ref","signature"],
  "properties": {
    "event": { "const": "QS.Published" },
    "ts": { "type": "string", "format": "date-time" },
    "program": { "type": "string", "pattern": "^(AmpelTreintaSesentaHidrogenoBlendedWingBodyQ100|BWB-Q100|AMPEL360)$" },
    "domain": { "type": "string", "pattern": "^[A-Z]{3}|ppp$" },
    "level":  { "type": "string", "enum": ["TFA","SI","CV","SE","DI","CE","CC","CI","CP","FE","QS"] },
    "entity": { "type": "string", "minLength": 1 },
    "qs_type":{ "type": "string", "enum": ["QUBO","VQE","QML"] },
    "utcs_mi_id": { "type": "string", "minLength": 40 },
    "det_ref": { "type": "string", "pattern": "^DET:QS:[A-Z]{3}|ppp:[A-Z]{2}:[A-Za-z0-9\\-]+:V[0-9]+\\.[0-9]+$" },
    "signature": { "type": "string", "pattern": "^PQC-(Dilithium3|Falcon|SPHINCS\\+)$" },
    "meta": { "type": "object", "additionalProperties": true }
  },
  "additionalProperties": false
}
```

**b) `DET` refs (actualizado):**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DET.Ref",
  "type": "string",
  "pattern": "^(DET:(SE|DI|CE|QS):[A-Z]{3}|ppp:[A-Z]{2}:[A-Za-z0-9\\-]+:V[0-9]+\\.[0-9]+)$"
}
```

---

## 8) Validadores rápidos (regex) para IDs UTCS-MI v5.0 (QS)

**Regex sintáctico (aprox.) para `EstándarUniversal:EstadoCuantico-…`:**

```
^EstándarUniversal:EstadoCuantico-(QUBO|VQE|QML)-\d{2}\.\d{2}-[A-Z]{3}|ppp-[A-Z]{2}-[A-Za-z0-9\-]+-\d{4}-v\d+\.\d+-[A-Za-z0-9 ]+-[A-Z]{3,6}-[A-Za-z0-9\-]+-[A-Za-z0-9\-]+-[a-f0-9]{8}-RestoDeVidaUtil$
```

---

## 9) Aliases HTML/MD ya listos (redirecciones suaves)

```html
<!-- Aliases de programa/categoría (legado → canónico) -->
<a id="prog-bwb-q100" href="#tfa-bwb"></a>
<a id="prog-ampel360" href="#tfa-bwb"></a>
```

---

## 10) Notas UTCS-MI v5.0 (consistencia y nombres)

* **13 campos obligatorios** y **versión "vX.Y"**.
* **Programa/Categoría sin acrónimos** (v5.0): el programa canónico es `Ampel Treinta Sesenta Hidrogeno Blended Wing Body Q100`, con alias legados `BWB-Q100`, `AMPEL360`.
* **Reglas de compatibilidad** aplicadas: `#ta-* → #tfa-*`, `#sa-* → #se-*`, `#di(invariant) → #dinv-*`, `#ce(envelope) → #cenv-*`.

---

* **13 campos obligatorios** y **versión `vX.Y`**.
* **Programa/Categoría sin siglas** (canónico); siglas solo como **alias** con QAUDIT.
* **PPP** se mantiene en minúscula (`ppp`) en IDs y anclas.
* **Alias vigentes** por dos *major releases* y registrados como `DET:ALIAS:*` firmados (QAUDIT).

---

## 5) QS — Identificadores, evento QAL y DET

**ID QS (sugerido):**

```
EstándarUniversal:EstadoCuantico-QUBO|VQE|QML-02.00-<DOM>-<Nivel>-<Entidad>-<Sec>-v<M.m>-<ProgramaCanonico>-<Ámbito>-<Propósito>-<Owner>-<hash8>-RestoDeVidaUtil
```

**Ejemplo:**

```
EstándarUniversal:EstadoCuantico-VQE-02.00-AAA-CI-53-30-TIES-0003-v1.0-AmpelTreintaSesentaHidrogenoBlendedWingBodyQ100-AIR-AMPEL360-CAE-Materials-7b821d44-RestoDeVidaUtil
```

**Evento QAL Bus (`QS.Published`):**

```json
{
  "event": "QS.Published",
  "ts": "2025-09-02T00:00:00Z",
  "program": "BWB-Q100",
  "domain": "AAA",
  "level": "CI",
  "entity": "53-30-TIES",
  "qs_type": "VQE",
  "utcs_mi_id": "EstándarUniversal:EstadoCuantico-VQE-02.00-AAA-CI-53-30-TIES-0003-v1.0-...",
  "det_ref": "DET:QS:AAA:CI:53-30-TIES:V1.0",
  "signature": "PQC-Dilithium3"
}
```

**DET (extracto):**

```yaml
DET:
  id: DET:QS:AAA:CI:53-30-TIES:V1.0
  program: BWB-Q100
  qs:
    type: VQE
    utcs_mi_id: EstándarUniversal:EstadoCuantico-VQE-02.00-AAA-CI-53-30-TIES-0003-v1.0-...
    backend: TerraQuantum
    params: { cvar_alpha: 0.10, shots: 4096 }
  qaudit:
    signer: QAUDIT:BOT:SIG-01
    scheme: PQC-Dilithium3
    hash: sha3-256
    signature: base64:...
```

---

## 6) Compatibilidad y migración (alias)

| Legado              | Canónico       | Ámbito  | Política                                    |
| ------------------- | -------------- | ------- | ------------------------------------------- |
| `#ta-*`             | `#tfa-*`       | TFA     | Alias activo 2 *majors* + `DET:ALIAS`       |
| `#sa-<dom>-NN`      | `#se-<dom>-NN` | SE      | Idem                                        |
| `#di-* (invariant)` | `#dinv-*`      | DI/DINV | DI = Interfaces; invariantes quedan en DINV |
| `#ce-* (envelope)`  | `#cenv-*`      | CE/CENV | CE = Equipped; envelope vive en CENV        |

---

## 7) Artefactos generados por script (rutas)

* `docs/taxonomy/index-table.md` → tabla dominio×nivel
* `docs/taxonomy/anchors.html` → anclas de navegación
* `docs/diagrams/qal-taxonomy.svg` → diagrama Mermaid exportado
* `docs/taxonomy/placeholders/AAA.md` *(y AAP…ppp)* → secciones base

---

## 8) Checks mínimos de CI (shell)

```bash
test -f docs/taxonomy/index-table.md
test -f docs/taxonomy/anchors.html
test -f docs/diagrams/qal-taxonomy.svg
for d in AAA AAP CCC CQH DDD EDI EEE EER IIF IIS LCC LIB MMM OOO ppp; do
  test -f "docs/taxonomy/placeholders/$d.md"
done
echo "✔ QAL Taxonomía: artefactos presentes"
```

---

## 9) Metamapas (documentación viva)

```md
![Mapa de migración](docs/diagrams/migration-map.svg)
```

---

### Estado

**QAL Taxonomía Extendida — BWB-Q100** lista para producción: navegación estable, alias retrocompatibles, QS/DET/QAUDIT acoplados y validados bajo **UTCS-MI v5.0**. Próximo paso natural: enlazar desde *Processing Prompt UI* para que cada publicación de plantilla dispare **QS.Published** y autocoloque el DET en su placeholder de dominio.