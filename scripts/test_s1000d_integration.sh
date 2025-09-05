#!/usr/bin/env bash
# S1000D-Q System Integration Test
# Tests the complete S1000D-Q pack and governance system

set -euo pipefail

echo "🔍 S1000D-Q System Integration Test"
echo "=================================="

# Test 1: YAML Linting
echo "📋 Test 1: YAML Linting..."
yamllint -s docs/S1000D-Q/ATA-56/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/*.yaml
yamllint -s docs/S1000D-GOV/CAS/*.yaml
yamllint -s C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/architecture/*.yaml
yamllint -s C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/matrices/*.yaml
echo "✅ YAML Linting: PASS"

# Test 2: BREX Validation
echo "📋 Test 2: BREX Validation..."
node scripts/s1000d_brex_validate.mjs $(git ls-files 'docs/S1000D-Q/**/DM-*.yaml')
echo "✅ BREX Validation: PASS"

# Test 3: File Structure Validation
echo "📋 Test 3: File Structure..."
test -f docs/S1000D-Q/ATA-56/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/DM-ARCH.yaml || { echo "❌ DM-ARCH.yaml missing"; exit 1; }
test -f docs/S1000D-Q/ATA-56/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/DM-ICD.yaml || { echo "❌ DM-ICD.yaml missing"; exit 1; }
test -f docs/S1000D-Q/ATA-56/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/DM-VV.yaml || { echo "❌ DM-VV.yaml missing"; exit 1; }
test -f C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/architecture/hierarchy.yaml || { echo "❌ hierarchy.yaml missing"; exit 1; }
test -f C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/architecture/icd.signals.yaml || { echo "❌ icd.signals.yaml missing"; exit 1; }
test -f C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/matrices/rtm.yaml || { echo "❌ rtm.yaml missing"; exit 1; }
echo "✅ File Structure: PASS"

# Test 4: Requirements Traceability
echo "📋 Test 4: Requirements Traceability..."
for req in "REQ-WIN-01" "REQ-WIN-02" "REQ-WIN-03" "REQ-WIN-04" "REQ-WIN-05"; do
  grep -q "$req" C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/matrices/rtm.yaml || { echo "❌ $req missing from RTM"; exit 1; }
done
echo "✅ Requirements Traceability: PASS"

# Test 5: Hierarchy Model Validation
echo "📋 Test 5: Hierarchy Model..."
grep -q "CE→CC→CI→CP→FE→QS" C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/architecture/hierarchy.yaml || { echo "❌ Hierarchy model missing"; exit 1; }
echo "✅ Hierarchy Model: PASS"

# Test 6: S1000D-Q Pack Links
echo "📋 Test 6: S1000D-Q Pack Links in README..."
grep -q "S1000D‑Q Pack" C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CE-CAD-Q100-AAA-ATA-56-WINDOWS-PANORAMIC/README.md || { echo "❌ S1000D-Q pack links missing from README"; exit 1; }
echo "✅ S1000D-Q Pack Links: PASS"

echo ""
echo "🎯 S1000D-Q System Integration Test: ALL TESTS PASSED"
echo "✅ Ready for production use with ATA-56 panoramic windows"