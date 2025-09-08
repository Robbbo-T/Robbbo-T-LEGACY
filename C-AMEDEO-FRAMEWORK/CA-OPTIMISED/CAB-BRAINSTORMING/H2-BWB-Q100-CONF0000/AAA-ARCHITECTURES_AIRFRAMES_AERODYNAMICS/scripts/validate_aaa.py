import json
import pathlib

SCHEMA_DIR = pathlib.Path(__file__).resolve().parents[7] / "schemas"

SCHEMAS = {
    "heur": SCHEMA_DIR / "heur_schema.json",
    "req": SCHEMA_DIR / "aaa_requirement.schema.json"
}

def load_schema(schema_path):
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    heur_schema = load_schema(SCHEMAS["heur"])
    req_schema = load_schema(SCHEMAS["req"])
    # Aquí sigue tu lógica de validación...

if __name__ == "__main__":
    main()
