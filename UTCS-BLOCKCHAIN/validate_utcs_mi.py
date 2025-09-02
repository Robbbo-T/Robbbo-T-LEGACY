#!/usr/bin/env python3
import re, sys, pathlib

RE = re.compile(r'^EstándarUniversal:'
                r'(?P<clase>[^:]+)-'
                r'(?P<fase>[^:]+)-'
                r'(?P<reg>[A-Z0-9+\-]+)-'
                r'(?P<capsec>\d{2}\.\d{2})-'
                r'(?P<categoria>[A-Z][a-zA-Z0-9]+)-'
                r'(?P<seq>\d{4})-'
                r'(?P<ver>v\d+\.\d+)-'
                r'(?P<programa>[A-Z][a-zA-Z0-9 ]+)-'
                r'(?P<gen>GeneracionHumana|GeneracionHybrida|GeneracionAuto)-'
                r'(?P<dom>AIR|SPACE|DEFENSE|GROUND|CROSS)-'
                r'(?P<idf>[^:]+)-'
                r'(?P<hash>[a-f0-9]{8})-'
                r'(?P<periodo>RestoDeVidaUtil|[A-Za-z→]+)$')

PROHIBITED = {"BWB","HE","UAV","VTOL","H2","FBW","FBQW"}  # extend as needed

def invalid_reason(s: str):
    m = RE.match(s.strip())
    if not m:
        return "regex_mismatch"
    cat = m["categoria"]; prog = m["programa"]
    # Prohibit acronyms in category/program (heuristic: all-caps tokens of length 2-6)
    caps_tokens = [t for t in prog.split() if t.isupper()] + [cat] if cat.isupper() else []
    if any(t in PROHIBITED or (t.isupper() and 2 <= len(t) <= 6) for t in caps_tokens):
        return "acronym_violation"
    return ""

def main():
    errs = []
    for p in sys.argv[1:]:
        for i, line in enumerate(pathlib.Path(p).read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("EstándarUniversal:"):
                why = invalid_reason(line)
                if why:
                    errs.append(f"{p}:{i}:{why}")
    if errs:
        print("\n".join(errs)); sys.exit(1)
    print("UTCS‑MI validation passed.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: validate_utcs_mi.py <files...>"); sys.exit(2)
    main()