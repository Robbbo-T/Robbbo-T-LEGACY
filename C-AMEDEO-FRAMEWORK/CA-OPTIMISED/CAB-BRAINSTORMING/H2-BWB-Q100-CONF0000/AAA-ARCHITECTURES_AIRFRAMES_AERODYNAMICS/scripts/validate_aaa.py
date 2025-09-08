#!/usr/bin/env python3
import sys, json, pathlib, re, glob, subprocess
from jsonschema import Draft7Validator
from ruamel.yaml import YAML

# Upgrade pip and install required packages
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([sys.executable, "-m", "pip", "install", "jsonschema", "ruamel.yaml"], check=True)

ROOT = pathlib.Path(__file__).resolve().parents[1]
yaml = YAML(typ="safe")

SCHEMAS = {
    "heur": ROOT.parents[6] / "schemas" / "heur_schema.json",
    "req":  ROOT.parents[6] / "schemas" / "aaa_requirement.schema.json",
}

FILES = {
    "domain_cfg": ROOT / "domain-config.yaml",
    "reqs":       ROOT / "requirements" / "requirements.yaml",
    "heur_glob":  ROOT / "det_samples" / "heur_cycles" / "**" / "*.json",
}

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def load_yaml(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.load(f)

def validate_json(instance, schema):
    v = Draft7Validator(schema)
    errs = sorted(v.iter_errors(instance), key=lambda e: e.path)
    return [f"{'/'.join([str(x) for x in e.path])}: {e.message}" for e in errs]

def validate_requirements(reqs, req_schema):
    errors = []
    warnings = []
    for i, r in enumerate(reqs or []):
        errs = validate_json(r, req_schema)
        errors += [f"[requirements[{i}]] {e}" for e in errs]
        links = (r or {}).get("links", {})
        if not links.get("ce"):
            warnings.append(f"[requirements[{i}]] missing links.ce")
        if not links.get("ci"):
            warnings.append(f"[requirements[{i}]] missing links.ci")
    return errors, warnings

def collect_ontology_nodes(domain_cfg):
    nodes = set()
    ont = domain_cfg.get("ontology", {}).get("internal_classes", {})
    for cls, spec in ont.items():
        for n in spec.get("nodes", []):
            nodes.add(f"{cls}.{n}")
    return nodes

def collect_goals(domain_cfg):
    return set(domain_cfg.get("goals", {}).get("list", {}).keys())

def collect_interfaces(domain_cfg):
    ifaces = set()
    for k, v in domain_cfg.get("ontology", {}).get("interfaced_classes", {}).items():
        for itf in v.get("interfaces", []):
            ifaces.add(f"{k}.{itf.get('name')}")
    return ifaces

def validate_rtm(domain_cfg, req_ids, nodes, goals, ifaces):
    errors = []
    rtm = domain_cfg.get("rtm", {}).get("rows", [])
    if not isinstance(rtm, list):
        return ["rtm.rows must be a list"]
    seen_reqs = set()
    seen_goals = set()

    for i, row in enumerate(rtm):
        context = f"[rtm.rows[{i}]]"
        req = row.get("req")
        if not req:
            errors.append(f"{context} missing 'req'")
            continue
        seen_reqs.add(req)
        if req not in req_ids:
            errors.append(f"{context} req '{req}' not found in requirements")

        for g in row.get("goals", []):
            if g not in goals:
                errors.append(f"{context} goal '{g}' not in goals.list")
            else:
                seen_goals.add(g)

        for n in row.get("ontology_nodes", []):
            if n not in nodes:
                errors.append(f"{context} ontology node '{n}' not defined")

        for itf in row.get("interfaces", []):
            if itf not in ifaces:
                errors.append(f"{context} interface '{itf}' not defined")

    uncovered = [r for r in req_ids if r not in seen_reqs]
    if uncovered:
        errors.append(f"[rtm] uncovered requirements: {', '.join(sorted(uncovered))}")

    # Enforce coverage: each goal must be hit by ≥1 REQ
    missing_goals = [g for g in goals if g not in seen_goals]
    if missing_goals:
        errors.append(f"[rtm] uncovered goals: {', '.join(sorted(missing_goals))}")
    return errors

def validate_heur_cycles(heur_schema):
    errors = []
    for p in glob.glob(str(FILES["heur_glob"]), recursive=True):
        try:
            inst = json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
            errs = validate_json(inst, heur_schema)
            errors += [f"[{p}] {e}" for e in errs]
        except Exception as ex:
            errors.append(f"[{p}] parse error: {ex}")
    return errors

def main():
    heur_schema = load_json(SCHEMAS["heur"])
    req_schema  = load_json(SCHEMAS["req"])

    domain_cfg = load_yaml(FILES["domain_cfg"])
    req_doc = load_yaml(FILES["reqs"])
    reqs = req_doc.get("requirements") if isinstance(req_doc, dict) else req_doc
    if not isinstance(reqs, list):
        print("ERROR: requirements file must be a list or have top-level 'requirements' list.", file=sys.stderr)
        sys.exit(2)

    req_errors, req_warnings = validate_requirements(reqs, req_schema)
    req_ids = {r.get("id") for r in reqs if isinstance(r, dict) and r.get("id")}
    nodes = collect_ontology_nodes(domain_cfg)
    goals = collect_goals(domain_cfg)
    ifaces = collect_interfaces(domain_cfg)

    rtm_errors = validate_rtm(domain_cfg, req_ids, nodes, goals, ifaces)
    heur_errors = validate_heur_cycles(heur_schema)

    all_errors = req_errors + rtm_errors + heur_errors
    if all_errors:
        print("VALIDATION FAILURES:")
        for e in all_errors:
            print(" -", e)
        sys.exit(1)
    if req_warnings:
        print("VALIDATION WARNINGS:")
        for w in req_warnings:
            print(" -", w)
    print("All AAA validations passed ✅")

    # Run make commands
    subprocess.run(["make", "det-aaa"], check=True)
    subprocess.run(["make", "validate-aaa"], check=True)

if __name__ == "__main__":
    main()
