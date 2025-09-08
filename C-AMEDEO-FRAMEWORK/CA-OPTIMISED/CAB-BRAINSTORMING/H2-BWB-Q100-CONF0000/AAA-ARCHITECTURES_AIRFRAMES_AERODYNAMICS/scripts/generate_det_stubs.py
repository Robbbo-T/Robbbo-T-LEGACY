#!/usr/bin/env python3
import sys, json, hashlib, datetime, pathlib
from ruamel.yaml import YAML

yaml = YAML(typ="safe")
ROOT = pathlib.Path(__file__).resolve().parents[1]
REQ_FILE = ROOT / "requirements" / "requirements.yaml"
OUT_DIR = ROOT / "det_samples" / "det_packs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Simple DET stub generator for req_add / req_update

def load_yaml(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.load(f)

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def det_pack(req: dict, action: str) -> dict:
    now = f"{datetime.datetime.now(datetime.timezone.utc).isoformat()}Z"
    rid = req.get("id")
    text = req.get("text", "")
    meta = {
        "det_id": f"DET:CAB:AAA:{rid}:{action}:V1",
        "refs": {"ce": req.get("links", {}).get("ce"), "ci": req.get("links", {}).get("ci")},
        "action": action,
        "timestamp": now,
        "units": {"timestamp": "UTC"},
    "change_ref": f"{rid}:{action}:{now}",
    }
    body = {
        "requirement": {
            "id": rid,
            "text": text,
            "status": req.get("status"),
            "owner": req.get("owner"),
            "last_updated": req.get("last_updated"),
        }
    }
    raw = json.dumps(body, sort_keys=True).encode("utf-8")
    meta["hash"] = {"alg": "SHA-256", "value": sha256_bytes(raw)}
    return {"meta": meta, "body": body}


def main():
    doc = load_yaml(REQ_FILE)
    reqs = doc.get("requirements", []) if isinstance(doc, dict) else []

    # For simplicity: generate/update one pack per requirement (idempotent)
    for req in reqs:
        rid = req.get("id")
        if not rid:
            continue
        # Decide action by status
        action = "req_add" if req.get("status", "").lower() == "proposed" else "req_update"
        pack = det_pack(req, action)
        out = OUT_DIR / f"{rid}-{action}.json"
        out.write_text(json.dumps(pack, indent=2), encoding="utf-8")
        print(f"wrote {out}")

if __name__ == "__main__":
    main()
