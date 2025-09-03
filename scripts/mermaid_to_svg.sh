#!/usr/bin/env bash
set -euo pipefail
for f in docs/diagrams/*.mmd; do
  mmdc -i "$f" -o "${f%.mmd}.svg"
  echo "→ ${f%.mmd}.svg"
done