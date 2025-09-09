#!/usr/bin/env node
import fs from "fs";
import Ajv from "ajv";
const ajv = new Ajv({ allErrors: true, strict: false });

const schema = JSON.parse(fs.readFileSync("schemas/qs.published.schema.json","utf8"));
const validate = ajv.compile(schema);

const files = process.argv.slice(2);
let failed = 0;
for (const f of files) {
  const data = JSON.parse(fs.readFileSync(f,"utf8"));
  const ok = validate(data);
  if (!ok) {
    console.error("✖", f, ajv.errorsText(validate.errors, { separator: "\n  - " }));
    failed++;
  } else {
    console.log("✔", f);
  }
}
process.exit(failed ? 1 : 0);