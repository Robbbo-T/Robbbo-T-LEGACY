#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

sha_file="Integrity/SHA256SUMS.txt"
manifest="Integrity/manifest.yaml"

# --- helpers ---
filesize() {
  if stat --version >/dev/null 2>&1; then
    stat -c%s "$1"       # GNU
  else
    stat -f%z "$1"       # BSD/macOS
  fi
}

sed_inplace() {
  if sed --version >/dev/null 2>&1; then
    sed -i "$@"
  else
    sed -i '' "$@"
  fi
}

iso_now() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

# --- hashes ---
echo "Generating SHA256SUMS.txt..."
find 3DModels Drawings -type f -print0 2>/dev/null | xargs -0 sha256sum > "$sha_file" || true

if [ -f "3DModels/fpb_assy_v3.step" ]; then
  SHA256_STEP=$(sha256sum 3DModels/fpb_assy_v3.step | awk '{print $1}')
  SIZE_STEP=$(filesize 3DModels/fpb_assy_v3.step)
  sed_inplace "s/\${SHA256_STEP}/$SHA256_STEP/g" "$manifest"
  sed_inplace "s/\${SIZE_STEP}/$SIZE_STEP/g" "$manifest"
fi

if [ -f "3DModels/fpb_assy_v3.CATPart" ]; then
  SHA256_CATPART=$(sha256sum 3DModels/fpb_assy_v3.CATPart | awk '{print $1}')
  SIZE_CATPART=$(filesize 3DModels/fpb_assy_v3.CATPart)
  sed_inplace "s/\${SHA256_CATPART}/$SHA256_CATPART/g" "$manifest"
  sed_inplace "s/\${SIZE_CATPART}/$SIZE_CATPART/g" "$manifest"
fi

if [ -f "3DModels/fpb_assy_v3.CATProduct" ]; then
  SHA256_CATPRODUCT=$(sha256sum 3DModels/fpb_assy_v3.CATProduct | awk '{print $1}')
  SIZE_CATPRODUCT=$(filesize 3DModels/fpb_assy_v3.CATProduct)
  sed_inplace "s/\${SHA256_CATPRODUCT}/$SHA256_CATPRODUCT/g" "$manifest"
  sed_inplace "s/\${SIZE_CATPRODUCT}/$SIZE_CATPRODUCT/g" "$manifest"
fi

if [ -f "Drawings/fpb_assy_v3.dxf" ]; then
  SHA256_DXF=$(sha256sum Drawings/fpb_assy_v3.dxf | awk '{print $1}')
  SIZE_DXF=$(filesize Drawings/fpb_assy_v3.dxf)
  sed_inplace "s/\${SHA256_DXF}/$SHA256_DXF/g" "$manifest"
  sed_inplace "s/\${SIZE_DXF}/$SIZE_DXF/g" "$manifest"
fi

if [ -f "Drawings/fpb_assy_v3.pdf" ]; then
  SHA256_PDF=$(sha256sum Drawings/fpb_assy_v3.pdf | awk '{print $1}')
  SIZE_PDF=$(filesize Drawings/fpb_assy_v3.pdf)
  sed_inplace "s/\${SHA256_PDF}/$SHA256_PDF/g" "$manifest"
  sed_inplace "s/\${SIZE_PDF}/$SIZE_PDF/g" "$manifest"
fi

if [ -f "Drawings/fpb_assy_v3.dwg" ]; then
  SHA256_DWG=$(sha256sum Drawings/fpb_assy_v3.dwg | awk '{print $1}')
  SIZE_DWG=$(filesize Drawings/fpb_assy_v3.dwg)
  sed_inplace "s/\${SHA256_DWG}/$SHA256_DWG/g" "$manifest"
  sed_inplace "s/\${SIZE_DWG}/$SIZE_DWG/g" "$manifest"
fi

# refresh timestamp
ts=$(iso_now)
sed_inplace "s/generated: \".*Z\"/generated: \"$ts\"/" "$manifest"

# --- extract Validation Properties (VP) ---
if [ -f "Integrity/extract_vp_from_step.py" ]; then
  echo "Extracting Validation Properties from STEP..."
  python3 Integrity/extract_vp_from_step.py || echo "⚠️ VP extraction failed"
else
  echo "⚠️ No extract_vp_from_step.py found, skipping VP extraction"
fi

echo "✅ Hashes, sizes and VP updated in $manifest"