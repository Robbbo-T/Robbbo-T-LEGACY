#!/usr/bin/env node
import fs from "fs";
import path from "path";
import Handlebars from "handlebars";

const ROOT = process.cwd();
const { domains } = JSON.parse(fs.readFileSync("scripts/domain_list.json", "utf8"));

const tpl = `
# {{code}} — {{name}}
{{!-- Aliases/anchors --}}
<a id="si-{{lower}}"></a> <a id="cv-{{lower}}"></a> <a id="se-{{lower}}"></a>
<a id="di-{{lower}}"></a> <a id="ce-{{lower}}"></a>
<a id="cc-{{lower}}"></a> <a id="ci-{{lower}}"></a> <a id="cp-{{lower}}"></a> <a id="fe-{{lower}}"></a>
<a id="qs-{{lower}}"></a>
{{#if isAAA}}
<a id="dinv-aaa"></a> <a id="cenv-aaa"></a>
{{/if}}

> **Mini‑TOC**: [Volver arriba](../index-table.md) · [Anclas](../anchors.html)

## SI — System Integration ({{code}})
> Línea base de integración, bring‑up, issues interdominio. Entregables: SI‑Baseline, logs.

## CV — Component Vendor ({{code}})
> AVL: proveedores aprobados, CAGE, PPAP/FAI, lead time, riesgo supply.

## SE — Station Envelop ({{code}})
> Estaciones/takt/kits/recursos (alias legado SA→SE activo).

## DI — Domain Interface ({{code}})
> ICD/IFD con dominios vecinos. Verificación y versionado.

## CE — Component Equipped ({{code}})
> Configuraciones equipadas (as‑built + vendor kit + trazabilidad DET).

## CC — Component Cell ({{code}})
> Células agrupadoras de configuración (relación con CI/SE).

## CI — Component Item ({{code}})
> Ítems funcionales; parámetros, límites, ensayos.

## CP — Component Part ({{code}})
> Piezas PN/Rev; material, proceso, MBD/PMI.

## FE — Fundamental Element ({{code}})
> Elementos medibles (features/material/test point).

## QS — Quantum State ({{code}})
> QUBO/VQE/QML vinculados a {{code}}. Registrar en DET y emitir QS.Published.
`;

const compile = Handlebars.compile(tpl.trim());

fs.mkdirSync("docs/taxonomy/placeholders", { recursive: true });
for (const d of domains) {
  const out = compile({ ...d, isAAA: d.code === "AAA" });
  fs.writeFileSync(`docs/taxonomy/placeholders/${d.code}.md`, out + "\n");
}
console.log("✔ Placeholders por dominio generados en docs/taxonomy/placeholders/");