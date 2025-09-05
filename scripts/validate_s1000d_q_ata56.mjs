#!/usr/bin/env node
// Simple validators for ATA-56 S1000D-Q pack (no external deps).
// Checks: DM headers/links, hierarchy parentage, RTM references, file existence.

import fs from "fs";
import path from "path";

const DM_DIR = "docs/S1000D-Q/ATA-56/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC";
const ARCH_DIR = "C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/architecture";
const MATR_DIR = path.dirname(ARCH_DIR) + "/matrices";

const fail = (m) => { console.error("✖", m); process.exitCode = 1; };
const ok =  (m) => { console.log("✔", m); };

function fileExists(p) { try { fs.accessSync(p); return true; } catch { return false; } }
function read(p) { return fs.readFileSync(p, "utf8"); }

function checkDMs() {
  const dms = ["DM-ARCH.yaml","DM-ICD.yaml","DM-VV.yaml"].map(f => path.join(DM_DIR, f));
  dms.forEach(fp => {
    if (!fileExists(fp)) return fail(`Missing DM: ${fp}`);
    const t = read(fp);
    if (!/model_ident_code:\s*"AMPEL360"/.test(t)) fail(`DM ${fp}: model_ident_code missing or wrong`);
    if (!/system_code:\s*"56"/.test(t))        fail(`DM ${fp}: system_code != "56"`);
    if (!/links:\s*\n\s*ce:\s*"CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC"/.test(t))
      fail(`DM ${fp}: links.ce missing or wrong`);
    // Info code policy (018/022/024)
    const m = t.match(/info_code:\s*"(\d{3})"/);
    if (m && !["018","022","024"].includes(m[1])) fail(`DM ${fp}: info_code ${m[1]} not allowed`);
    ok(`DM ok: ${fp}`);
  });
}

function checkHierarchy() {
  const hp = path.join(ARCH_DIR, "hierarchy.yaml");
  if (!fileExists(hp)) return fail(`Missing hierarchy: ${hp}`);
  const t = read(hp);
  const ce = t.match(/ce:\s*\n\s*id:\s*"([^"]+)"/)?.[1];
  if (ce !== "CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC") fail("Hierarchy: CE id mismatch");
  
  // Collect all IDs from hierarchy
  const ids = new Set([ce]);
  
  // Add CC level IDs (they have parent references in block format)
  for (const m of t.matchAll(/- id:\s*"([^"]+)"\s*\n\s*parent:/g)) {
    ids.add(m[1]);
  }
  
  // Collect parent references from flow-map entries and validate
  const parents = [];
  for (const m of t.matchAll(/id:\s*"([^"]+)"\s*,\s*parent:\s*"([^"]+)"/g)) {
    ids.add(m[1]); 
    parents.push(m[2]);
  }
  
  // Ensure all parents exist or are CE
  parents.forEach(p => {
    if (!ids.has(p)) fail(`Hierarchy: parent not found -> ${p}`);
  });
  ok("Hierarchy ok: parents found and linked");
}

function checkRTM() {
  const rp = path.join(MATR_DIR, "rtm.yaml");
  if (!fileExists(rp)) return fail(`Missing RTM: ${rp}`);
  const t = read(rp);
  // Require only known REQ-WIN-0X
  for (const m of t.matchAll(/req:\s*"([^"]+)"/g)) {
    if (!/^REQ-WIN-0[1-5]$/.test(m[1])) fail(`RTM: unknown req id ${m[1]}`);
  }
  // Ensure DMs referenced exist
  for (const m of t.matchAll(/dms:\s*\[([^\]]+)\]/g)) {
    const files = m[1].split(",").map(s => s.replace(/["\s]/g,""));
    files.forEach(f => {
      const fp = path.join(DM_DIR, f);
      if (!fileExists(fp)) fail(`RTM: DM not found -> ${fp}`);
    });
  }
  ok("RTM ok: requirements and DM refs validate");
}

function main() {
  checkDMs();
  checkHierarchy();
  checkRTM();
  if (process.exitCode) process.exit(process.exitCode);
  ok("S1000D-Q ATA-56 pack validation complete");
}

main();