#!/usr/bin/env python3
"""
BREX-lite validator for AMPEL360 H2-BWB-Q requirements Markdown files.

Checks:
- Extracts YAML 'requirements:' block from Markdown.
- Validates against schemas/requirements.item.schema.json for required fields and enums.
- Validates ID, DAL, verification values, dates, and links.ce/cc/ci pattern.
- Optionally validates 'det_evidence' block counts vs actual requirements.
- Calls UTCS-BLOCKCHAIN/validate_utcs_mi.py on the UTCS-MI line if present.

Usage:
  python scripts/brex_lite_validate_requirements.py <files...>

Exit codes:
  0 on success; 1 on validation error.
"""
import sys, re, json, subprocess, pathlib
from typing import List, Dict, Any
try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:
    print("Please pip install pyyaml jsonschema", file=sys.stderr)
    sys.exit(1)

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQ_SCHEMA_PATH = ROOT / "schemas" / "requirements.item.schema.json"
UTCS_VALIDATOR = ROOT / "UTCS-BLOCKCHAIN" / "validate_utcs_mi.py"

ID_RE = re.compile(r"^REQ-[A-Z0-9]{2,}-[0-9]{2}-[0-9]{2}-[0-9]{3}$|^REQ-[A-Z0-9-]{6,}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"^CE-[A-Z]{2,3}[A-Z]-Q100-[A-Z0-9]{3}-\d{2}-\d{2}-[A-Z0-9-]+$")
DAL_SET = {"DAL-A","DAL-B","DAL-C","DAL-D","DAL-E"}
VERIF_SET = {"Analysis","Test","Inspection","Review"}

ALLOWED_UNITS = {"µs","ms","kN","bar","°C","ft","kg","Hz","%","km"}

def load_schema() -> Dict[str, Any]:
    with open(REQ_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_yaml_blocks(md_text: str) -> Dict[str, Any]:
    # Find the first fenced block containing 'requirements:' at the start
    req_match = re.search(r"```yaml\s+(requirements:\s[\s\S]*?)```", md_text, re.MULTILINE)
    det_match = re.search(r"```yaml\s+(det_evidence:\s[\s\S]*?)```", md_text, re.MULTILINE)
    data: Dict[str, Any] = {}
    if req_match:
        data["requirements"] = yaml.safe_load(req_match.group(1))["requirements"]
    if det_match:
        data["det_evidence"] = yaml.safe_load(det_match.group(1))["det_evidence"]
    return data

def validate_utcs_mi(md_text: str) -> List[str]:
    errors: List[str] = []
    # Grab UTCS-MI line (after 'EstándarUniversal:' prefix)
    utcs_line = None
    for line in md_text.splitlines():
        if "EstándarUniversal:" in line:
            utcs_line = line.strip().split("EstándarUniversal:",1)[1].strip()
            break
    if not utcs_line:
        errors.append("UTCS-MI line not found")
        return errors
    # Write to temp file and run validator
    tmp = ROOT / ".tmp_utcs_id.txt"
    try:
        tmp.write_text(utcs_line, encoding="utf-8")
        if UTCS_VALIDATOR.exists():
            try:
                subprocess.run([sys.executable, str(UTCS_VALIDATOR), str(tmp)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                errors.append(f"UTCS-MI validation failed: {e.stderr.decode('utf-8', errors='ignore') or e.stdout.decode('utf-8', errors='ignore')}")
        else:
            errors.append(f"UTCS validator not found at {UTCS_VALIDATOR}")
    finally:
        tmp.unlink(missing_ok=True)
    return errors

def unit_warnings(text_fields: List[str]) -> List[str]:
    warnings: List[str] = []
    for t in text_fields:
        if not isinstance(t, str):
            continue
        for token in re.findall(r"([A-Za-zµ°/%]+)", t):
            # crude filter: raise notice if looks like unit but not in allowed
            if token in {"ms","us","µs","kN","bar","°C","ft","kg","Hz","%","km"}:
                if token == "us":
                    warnings.append("Use 'µs' instead of 'us' for microseconds")
            elif token in {"C"}:
                warnings.append("Use '°C' for degrees Celsius")
    return warnings

def main(paths: List[str]) -> int:
    schema = load_schema()
    validator = Draft202012Validator(schema)
    errs_total: List[str] = []
    warns_total: List[str] = []

    for p in paths:
        md_path = pathlib.Path(p)
        if not md_path.exists():
            errs_total.append(f"File not found: {p}")
            continue
        text = md_path.read_text(encoding="utf-8")
        # UTCS-MI
        errs_total += validate_utcs_mi(text)

        data = extract_yaml_blocks(text)
        if "requirements" not in data:
            errs_total.append(f"{p}: requirements YAML block not found")
            continue
        reqs = data["requirements"]
        if not isinstance(reqs, list) or not reqs:
            errs_total.append(f"{p}: requirements block is empty or malformed")
            continue

        # Per-requirement checks
        verif_counts = {"Analysis":0,"Test":0,"Inspection":0,"Review":0}
        for i, r in enumerate(reqs, 1):
            # Schema validation
            for e in sorted(validator.iter_errors(r), key=lambda e: e.path):
                errs_total.append(f"{p}: requirement[{i}] schema: {e.message} at {list(e.path)}")
            # ID
            rid = r.get("id","")
            if not ID_RE.match(rid or ""):
                errs_total.append(f"{p}: requirement[{i}] id '{rid}' does not match expected pattern")
            # DAL
            crit = r.get("criticality","")
            if crit not in DAL_SET:
                errs_total.append(f"{p}: requirement[{i}] criticality '{crit}' must be one of {sorted(DAL_SET)}")
            # Verification (top-level)
            v = r.get("verification","")
            if v not in VERIF_SET:
                errs_total.append(f"{p}: requirement[{i}] verification '{v}' must be one of {sorted(VERIF_SET)}")
            else:
                verif_counts[v] += 1
            # last_updated
            lu = r.get("last_updated","")
            if not DATE_RE.match(lu or ""):
                errs_total.append(f"{p}: requirement[{i}] last_updated '{lu}' must be YYYY-MM-DD")
            # links.ce/cc/ci present and well-formed (best-effort)
            links = r.get("links",{})
            for k in ("ce","cc","ci"):
                val = links.get(k,"")
                if not val:
                    errs_total.append(f"{p}: requirement[{i}] links.{k} missing")
                elif not val.startswith("CE-"):
                    errs_total.append(f"{p}: requirement[{i}] links.{k} '{val}' must start with 'CE-'")
            # Units warnings
            warns_total += unit_warnings([r.get("acceptance",""), r.get("constraints","")])

        # det_evidence reconciliation
        if "det_evidence" in data:
            det = data["det_evidence"]
            covered = det.get("requirements_covered", -1)
            if covered != len(reqs):
                errs_total.append(f"{p}: det_evidence.requirements_covered={covered} does not match actual count {len(reqs)}")
            vs = det.get("verification_status", {})
            # Map to lower keys
            expected_map = {
                "analysis": verif_counts["Analysis"],
                "test": verif_counts["Test"],
                "inspection": verif_counts["Inspection"],
                "review": verif_counts["Review"],
            }
            for k, expected in expected_map.items():
                got = int(vs.get(k, -1))
                if got != expected:
                    errs_total.append(f"{p}: det_evidence.verification_status.{k}={got} != {expected} (from requirements)")
        else:
            warns_total.append(f"{p}: det_evidence block not found (recommended)")

    for w in sorted(set(warns_total)):
        print(f"WARNING: {w}", file=sys.stderr)
    if errs_total:
        for e in errs_total:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print("BREX-lite validation passed for all files.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default: scan canonical location
        default = list((ROOT / "docs" / "requirements").rglob("*.md"))
        if not default:
            print("No files provided and no defaults found under docs/requirements", file=sys.stderr)
            sys.exit(1)
        sys.exit(main([str(p) for p in default]))
    sys.exit(main(sys.argv[1:]))