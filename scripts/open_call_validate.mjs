// Minimal validator for bounty YAMLs and royalty registry (no external deps).
import fs from "fs";

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error("Usage: node scripts/open_call_validate.mjs <bounty.yaml> [...]");
  process.exit(2);
}

function checkBounty(txt, path) {
  const must = ["bounty:", "id:", "title:", "remuneration:", "stablecoin_amount"];
  let ok = true;
  for (const k of must) {
    if (!txt.includes(k)) {
      console.error(`✖ ${path} missing key: ${k}`);
      ok = false;
    }
  }
  if (!/id:\s*\"?B-[A-Z0-9-]+\"?/.test(txt)) {
    console.error(`✖ ${path} invalid bounty id format`);
    ok = false;
  }
  return ok;
}

let failed = 0;
for (const f of files) {
  const t = fs.readFileSync(f, "utf8");
  const ok = checkBounty(t, f);
  if (ok) console.log(`✔ ${f}`);
  else failed++;
}
process.exit(failed ? 1 : 0);