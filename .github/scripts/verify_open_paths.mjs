// Fail PR if any changed file is outside allowed CC→FE scope or inside QS.
// Usage: node verify_open_paths.mjs <changed-files-list.txt>

import fs from "fs";

const listFile = process.argv[2];
if (!listFile) {
  console.error("Usage: node verify_open_paths.mjs <changed-files-list.txt>");
  process.exit(2);
}

const changed = fs.readFileSync(listFile, "utf8")
  .split("\n")
  .map(s => s.trim())
  .filter(Boolean);

// Rules (case-insensitive):
// Allowed if path contains /CE-<something>/(CC|CI|CP|FE)/...
// Also allow nested canonical names (e.g., CC/CE-CC-... trees).
const ALLOW = [
  /\/CE-[^/]+\/(CC|CI|CP|FE)\//i,
  /\/CC\/CE-CC-/i,
  /\/CI\/CE-CC-CI-/i,
  /\/(cp|CP)\/CE-CC-CI-CP-/,
  /\/FE\/CE-CC-CI-CP-FE-/i
];

const DENY = [
  /\/CE-[^/]+\/(QS)\//i,        // QS not allowed in open scope
  /\/CE-[^/]+\/$/i,             // CE root
  /\/CE-[^/]+\/(requirements|compliance|matrices|architecture|docs)\//i
];

// Always ignored files (e.g., markdown in policy dir for this feature)
const IGNORE = [
  /^policy\/OPEN-PATHS-CC-FE\.md$/i
];

let violations = [];

for (const f of changed) {
  if (IGNORE.some(re => re.test(f))) continue;

  const isDeny = DENY.some(re => re.test(f));
  const isAllow = ALLOW.some(re => re.test(f));

  if (isDeny || !isAllow) {
    violations.push(f);
  }
}

if (violations.length) {
  console.error("✖ Open Paths gate: files outside CC→FE scope (or forbidden):");
  for (const v of violations) console.error("  - " + v);
  console.error("Rule: only CC/CI/CP/FE under a CE path are allowed; QS/CE-level are blocked.");
  process.exit(1);
}
console.log("✔ Open Paths gate: all files within CC→FE scope.");