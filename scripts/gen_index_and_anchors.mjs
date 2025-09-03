#!/usr/bin/env node
import fs from "fs";
import path from "path";

const { domains } = JSON.parse(fs.readFileSync("scripts/domain_list.json", "utf8"));

const header = `| Dominio | TFA | SI | CV | SE | DI | CE | CC | CI | CP | FE | QS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
`;

const rows = domains.map(d =>
  `| **${d.code}** ${d.name} | [TFA](#tfa-bwb) | [SI](#si-${d.lower}) | [CV](#cv-${d.lower}) | [SE](#se-${d.lower}) | [DI](#di-${d.lower}) | [CE](#ce-${d.lower}) | [CC](#cc-${d.lower}) | [CI](#ci-${d.lower}) | [CP](#cp-${d.lower}) | [FE](#fe-${d.lower}) | [QS](#qs-${d.lower}) |`
).join("\n");

fs.mkdirSync("docs/taxonomy", { recursive: true });
fs.writeFileSync("docs/taxonomy/index-table.md", header + rows + "\n");

let anchors = [
  "<!-- Global TFA -->",
  '<a id="tfa-bwb"></a>',
  '<a id="ta-bwb"></a>' // alias legado
];

const levels = ["si","cv","se","di","ce","cc","ci","cp","fe","qs"];
for (const d of domains) {
  for (const l of levels) anchors.push(`<a id="${l}-${d.lower}"></a>`);
  anchors.push(`<a id="sa-${d.lower}"></a>`);    // alias SE legado
  if (d.lower === "aaa") anchors.push('<a id="dinv-aaa"></a><a id="cenv-aaa"></a>');
}

fs.writeFileSync("docs/taxonomy/anchors.html", anchors.join("\n") + "\n");

// Mermaid sources
fs.mkdirSync("docs/diagrams", { recursive: true });
fs.writeFileSync("docs/diagrams/qal-taxonomy.mmd",
`mindmap
  root((QAL Taxonomía Extendida))
    TFA(TFA · Top Figure Aircraft)
    SI(SI · System Integration)
    CV(CV · Component Vendor)
    SE(SE · Station Envelop)
    DI(DI · Domain Interface)
    CE(CE · Component Equipped)
    CC(CC · Component Cell)
    CI(CI · Component Item)
    CP(CP · Component Part)
    FE(FE · Fundamental Element)
    QS(QS · Quantum State)
`);
fs.writeFileSync("docs/diagrams/migration-map.mmd",
`flowchart LR
  CENV["CENV (old CE=Envelope)"] --> CE["CE (new: Component Equipped)"]
  TA["TA (Top Assembly)"] --> TFA["TFA (Top Figure Aircraft)"]
  SA["SA (Station Assembly)"] --> SE["SE (Station Envelop)"]
  DIINV["DI (Invariant)"] --> DINV["DINV (Invariant)"]
  DIIF["DI (Interface)"]:::now
  classDef now fill:#4CAF50,stroke:#222,color:#fff,stroke-width:2px
`);
console.log("✔ Índice, anclas y Mermaid generados");