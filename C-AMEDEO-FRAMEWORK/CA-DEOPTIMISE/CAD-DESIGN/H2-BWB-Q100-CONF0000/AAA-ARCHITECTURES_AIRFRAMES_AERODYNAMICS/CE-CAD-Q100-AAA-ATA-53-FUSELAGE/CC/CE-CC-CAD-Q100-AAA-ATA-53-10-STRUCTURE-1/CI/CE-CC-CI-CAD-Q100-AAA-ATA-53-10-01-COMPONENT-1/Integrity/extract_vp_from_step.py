#!/usr/bin/env python3
"""
Extrae Validation Properties (VP) de un STEP AP242 ed2
y actualiza Integrity/manifest.yaml con los valores encontrados.
"""

import re
import yaml
from pathlib import Path

STEP_FILE = Path("3DModels/fpb_assy_v3.step")
MANIFEST_FILE = Path("Integrity/manifest.yaml")

# Patrones típicos de VP en AP242 (simplificados)
patterns = {
    "mass_kg": re.compile(r"MASS.*?REAL\(([\d\.\+\-Ee]+)\)", re.IGNORECASE),
    "cg_x_mm": re.compile(r"CG_X.*?REAL\(([\d\.\+\-Ee]+)\)", re.IGNORECASE),
    "cg_y_mm": re.compile(r"CG_Y.*?REAL\(([\d\.\+\-Ee]+)\)", re.IGNORECASE),
    "cg_z_mm": re.compile(r"CG_Z.*?REAL\(([\d\.\+\-Ee]+)\)", re.IGNORECASE),
    "bbox_x_mm": re.compile(r"BBOX_X.*?REAL\(([\d\.\+\-Ee]+)\)", re.IGNORECASE),
    "bbox_y_mm": re.compile(r"BBOX_Y.*?REAL\(([\d\.\+\-Ee]+)\)", re.IGNORECASE),
    "bbox_z_mm": re.compile(r"BBOX_Z.*?REAL\(([\d\.\+\-Ee]+)\)", re.IGNORECASE),
}

def extract_vp(step_path: Path) -> dict:
    txt = step_path.read_text(errors="ignore")
    results = {}
    for key, pat in patterns.items():
        m = pat.search(txt)
        if m:
            results[key] = float(m.group(1))
    return results

def update_manifest(manifest_path: Path, vp: dict):
    manifest_text = manifest_path.read_text()
    man = yaml.safe_load(manifest_text)
    for model in man["artifacts"]["3d_models"]:
        if model["file"].endswith(".step"):
            if "validation" not in model:
                model["validation"] = {}
            for k, v in vp.items():
                model["validation"][k] = v
    
    # Preserve YAML document start
    yaml_output = yaml.safe_dump(man, sort_keys=False)
    if not yaml_output.startswith('---'):
        yaml_output = '---\n' + yaml_output
    
    manifest_path.write_text(yaml_output)
    print(f"✅ Manifest actualizado con VP extraídos: {vp}")

if __name__ == "__main__":
    if not STEP_FILE.exists():
        print(f"❌ No se encontró {STEP_FILE}")
        exit(1)
    if not MANIFEST_FILE.exists():
        print(f"❌ No se encontró {MANIFEST_FILE}")
        exit(1)

    vp = extract_vp(STEP_FILE)
    if vp:
        update_manifest(MANIFEST_FILE, vp)
    else:
        print("⚠️ No se encontraron VP en el STEP (verifica exportación AP242+VP)")