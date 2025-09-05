#!/usr/bin/env node
// Minimal BREX validator: text-based checks (no YAML parser dependency).
// Validates DM YAML files against a subset of BREX-CAS rules.

import fs from "fs";
import path from "path";

const argv = process.argv.slice(2);
if (argv.length === 0) {
  console.error("Usage: node scripts/s1000d_brex_validate.mjs <file1.yaml> [...]");
  process.exit(2);
}

// load BREX (as text) to pick allowed info codes and required fields
const BREX_PATH = "docs/S1000D-GOV/CAS/BREX-CAS.yaml";
const brexText = fs.readFileSync(BREX_PATH, "utf8");

// crude extractors
const allowedInfoCodes = Array.from(
  brexText.matchAll(/info_codes:\s*\[([^\]]+)\]/g)
).flatMap(m => m[1].split(",").map(s => s.trim().replace(/["']/g,"")));

const mustFields = ["links:", "title:", "issue:", "status:"];

let failed = 0;

for (const file of argv) {
  const txt = fs.readFileSync(file, "utf8");
  const rel = file;

  // brx-110: no binaries (by extension heuristic in repo paths)
  const bannedExts = [".bmp",".png",".jpg",".jpeg",".pdf",".zip"];
  if (bannedExts.some(ext => rel.toLowerCase().endsWith(ext))) {
    console.error(`✖ ${rel} brx-110: binary media not allowed`);
    failed++; continue;
  }

  // brx-200: info code policy — check presence and allowed code values
  const infoCodeLine = txt.match(/info_code:\s*"?(?<code>\d{3})"?/);
  if (infoCodeLine) {
    const code = infoCodeLine.groups?.code;
    if (code && !allowedInfoCodes.includes(code)) {
      console.error(`✖ ${rel} brx-200: info_code ${code} not in ${allowedInfoCodes.join(",")}`);
      failed++;
    }
  }

  // brx-300: required top-level fields presence (string search)
  for (const f of mustFields) {
    if (!txt.includes(f)) {
      console.error(`✖ ${rel} brx-300: missing required field ${f.replace(":","")}`);
      failed++;
    }
  }

  // brx-400/410: if procedure info_code (040/060), require 'applicability'
  const proc = txt.match(/info_code:\s*"(040|060)"/);
  if (proc && !txt.includes("applicability:")) {
    console.error(`✖ ${rel} brx-400: procedure requires applicability`);
    failed++;
  }

  if (failed === 0) {
    console.log(`✔ ${rel}`);
  }
}

process.exit(failed ? 1 : 0);