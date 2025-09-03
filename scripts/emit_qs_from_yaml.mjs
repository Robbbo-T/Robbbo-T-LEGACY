#!/usr/bin/env node
import fs from "fs";
import path from "path";
import yaml from "js-yaml";

const root = "qal";
const out = "events/out";
fs.mkdirSync(out, { recursive: true });

function walk(dir) {
  for (const e of fs.readdirSync(dir)) {
    const p = path.join(dir, e);
    const s = fs.statSync(p);
    if (s.isDirectory()) walk(p);
    else if (e === "kit.yaml") processKit(p);
  }
}

function processKit(file) {
  const y = yaml.load(fs.readFileSync(file, "utf8"));
  (y.qs_hooks || []).forEach((q, i) => {
    const dom = y.dom;
    const entity = (q.ref.match(/-CI-([A-Za-z0-9\-]+)/) || [])[1] || "N_A";
    const qsType = /QUBO/.test(q.ref) ? "QUBO" : (/VQE/.test(q.ref) ? "VQE" : "QML");
    const payload = {
      event: "QS.Published",
      ts: new Date().toISOString(),
      program: "BWB-Q100",
      domain: dom,
      level: "CI",
      entity,
      qs_type: qsType,
      utcs_mi_id: q.ref,
      det_ref: q.det_ref,
      signature: "PQC-Dilithium3",
      meta: { source: path.relative(".", file) }
    };
    const fout = path.join(out, `qs_${dom}_${entity}_${Date.now()}_${i}.json`);
    fs.writeFileSync(fout, JSON.stringify(payload, null, 2));
    console.log("→ emitted", fout);
  });
}

walk(root);