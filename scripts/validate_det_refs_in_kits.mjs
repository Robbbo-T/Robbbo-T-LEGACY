#!/usr/bin/env node
import fs from "fs";
import path from "path";
import { globSync } from "glob";
import yaml from "js-yaml";
import Ajv from "ajv";

const ajv = new Ajv({ allErrors: true, strict: false });
const detSchema = JSON.parse(fs.readFileSync("schemas/det.ref.schema.json", "utf8"));
const validate = ajv.compile(detSchema);

const files = process.argv.slice(2);
const patterns = files.length ? files : ["qal/**/kit.yaml"];
const paths = patterns.flatMap(pattern => globSync(pattern, { dot: false }));

let failed = 0;

function collectDetRefs(node, acc = []) {
  if (typeof node === "string" && /DET:/.test(node)) acc.push(node);
  if (Array.isArray(node)) node.forEach((v) => collectDetRefs(v, acc));
  else if (node && typeof node === "object")
    Object.values(node).forEach((v) => collectDetRefs(v, acc));
  return acc;
}

for (const p of paths) {
  const y = yaml.load(fs.readFileSync(p, "utf8"));
  const refs = collectDetRefs(y, []);
  let localFail = 0;
  for (const r of refs) {
    const ok = validate(r);
    if (!ok) {
      console.error(`✖ ${p}: det_ref inválida "${r}" -> ${ajv.errorsText(validate.errors)}`);
      failed++;
      localFail++;
    }
  }
  if (!localFail) console.log(`✔ ${p}: ${refs.length} det_ref válidas`);
}

process.exit(failed ? 1 : 0);