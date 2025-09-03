# QAL Taxonomía Extendida — BWB-Q100

**UTCS-MI v5.0 (encabezado canónico)**  
`EstándarUniversal:Artefacto-DesgloseDeProducto-ATA+S1000D-01.00-ProductBreakdownStructure-0001-v1.1-Aerospace and Quantum United Advanced Venture-GeneracionHybrida-CROSS-Amedeo Pelliccia-deadbeef-RestoDeVidaUtil`

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

## 1) Taxonomía extendida (TFA, SI, CV, SE, DI, CE, CC, CI, CP, FE, QS)

|   Sigla | Nombre                  | Propósito resumido                                                   |
| ------: | ----------------------- | -------------------------------------------------------------------- |
| **TFA** | Top Figure Aircraft     | Activo final (build certificable del programa).                      |
|  **SI** | System Integration      | Línea base de integración y *bring-up* interdominios.                |
|  **CV** | Component Vendor        | AVL/PPAP/FAI y *source control* por CI/CP/FE.                        |
|  **SE** | Station Envelop         | Sobre de estación de fabricación (takt, recursos, kits).             |
|  **DI** | Domain Interface        | Interfaces formales (ICD/IFD) entre dominios.                        |
|  **CE** | Component Equipped      | Configuración equipada (*as-built* + kit + vendor).                  |
|  **CC** | Component Cell          | Célula de configuración (agrupador de ítems).                        |
|  **CI** | Component Item          | Unidad funcional configurable.                                       |
|  **CP** | Component Particle/Part | Parte fabricada (PN/Rev).                                            |
|  **FE** | Fundamental Element     | Elemento físico atómico/medible.                                     |
|  **QS** | Quantum State           | Estado/resultado cuántico (QUBO/VQE/QML) enlazado a cualquier nivel. |

**Compatibilidad / alias legado**

* `#ta-* → #tfa-*` · `#sa-<dom>-NN → #se-<dom>-NN` · `#di(invariant) → #dinv-*` · `#ce(envelope) → #cenv-*`

---

## 2) Enlaces internos y anclas

Incluye el paquete de anclas generado automáticamente:

```html
<!-- include file: docs/taxonomy/anchors.html -->
```

Renderiza/expone el índice dominio×nivel:

```md
<!-- include file: docs/taxonomy/index-table.md -->
```

Diagrama (Mermaid export):

```md
![QAL Taxonomía Extendida](docs/diagrams/qal-taxonomy.svg)
```

---

## 3) Placeholders por dominio

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

## 4) Notas UTCS-MI v5.0 (conformidad dura)

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