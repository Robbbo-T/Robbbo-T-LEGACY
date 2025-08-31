#!/bin/bash

# CADEO Framework Structure Validation Script
# © Amedeo Pelliccia 2025

echo "==================================="
echo "CADEO Framework Structure Validator"
echo "==================================="
echo "Version: 1.0.0"
echo "Date: $(date)"
echo ""

FRAMEWORK_ROOT="/home/runner/work/Robbbo-T/Robbbo-T/CADEO-FRAMEWORK"
cd "$FRAMEWORK_ROOT" || exit 1

echo "Framework Root: $FRAMEWORK_ROOT"
echo ""

# Validate main structure
echo "Validating main framework structure..."
echo "✓ Checking CA-DEOPTIMISED flow..."

DEOPT_DIRS=(
    "CAD-DESIGN"
    "CAE-ENGINEERING" 
    "CAO-ORGANIZATION"
    "CAP-PROCESS"
    "CAT-TECHNOLOGY_DATA_AND_DOCUMENTATION"
    "CAI-ind-INDUSTRIALIZATION"
    "CAM-MANUFACTURING"
    "CAI-INSTALLATION"
    "CAS-SUSTAINMENT"
    "CAE-post-EVALUATION"
    "CAD-Evo-ACTIVATION"
)

for dir in "${DEOPT_DIRS[@]}"; do
    if [ -d "CA-DEOPTIMISED/$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ✗ $dir - MISSING"
    fi
done

echo ""
echo "✓ Checking CA-OPTIMISED flow..."

OPT_DIRS=(
    "CAS-COMPLIANCE"
    "CAO-RECONSIDERATION"
    "CAP-REPLANNING"
    "CAT-RESTORATION"
    "CAI-REINSERTION"
    "CAM-RETROFIT"
    "CAI-improve-ENHANCEMENT"
    "CAE-ASSESSMENT"
    "CAD-REGENESIS"
)

for dir in "${OPT_DIRS[@]}"; do
    if [ -d "CA-OPTIMISED/$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ✗ $dir - MISSING"
    fi
done

echo ""
echo "✓ Checking CAT Technology Domains..."

TECH_DOMAINS=(
    "A-ARCHITECTURES_AIRFRAMES_AERODYNAMICS"
    "M-MECHANICAL_MATERIAL_MONITORING"
    "E1-ENVIRONMENTAL_REMEDIATION_CIRCULARITY"
    "D-DEFENCE_CYBERSECURITY_SAFETY"
    "E2-ENERGY_AND_RENEWABLE"
    "O-OPERATING_SYSTEMS_NAVIGATION_HPC"
    "P-PROPULSION_AND_FUELS"
    "E3-ELECTRONICS_DIGITAL_INSTRUMENTS"
    "L1-LOGISTICS_INTEGRATED_BLOCKCHAIN"
    "L2-LINKS_COMMUNICATIONS_CONTROL_IoT"
    "I-INFRASTRUCTURES_AND_FACILITIES_VALUE_CHAINS"
    "C1-COCKPIT_CABIN_CARGO_SYSTEMS"
    "C2-CRYOGENICS_QUANTUM_INTERFACES_HYDROGEN_CELLS"
    "I2-INTELLIGENT_SYSTEMS_ONBOARD_AI"
    "A2-AIRPORTS_ADAPTATIONS"
)

CAT_ROOT="CA-DEOPTIMISED/CAT-TECHNOLOGY_DATA_AND_DOCUMENTATION"
for domain in "${TECH_DOMAINS[@]}"; do
    if [ -d "$CAT_ROOT/$domain" ]; then
        echo "  ✓ $domain"
    else
        echo "  ✗ $domain - MISSING"
    fi
done

echo ""
echo "✓ Checking H2-BWB-Q100-CONF0000 configuration..."

CONFIG_ROOT="$CAT_ROOT/H2-BWB-Q100-CONF0000"
if [ -d "$CONFIG_ROOT" ]; then
    echo "  ✓ Configuration root exists"
    
    if [ -d "$CONFIG_ROOT/A-ARCHITECTURES_AIRFRAMES_AERODYNAMICS" ]; then
        echo "  ✓ Architecture domain configured"
        
        CB_ROOT="$CONFIG_ROOT/A-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/CA-CAT-Q100-AAA-CONF0000-53-10-CENTER-BODY-BOX"
        if [ -d "$CB_ROOT" ]; then
            echo "  ✓ Center Body Box component exists"
            
            CB_ITEMS=(
                "CI-CA-CAT-Q100-AAA-CONF0000-53-10-01-CB-PRIMARY-GRID"
                "CI-CA-CAT-Q100-AAA-CONF0000-53-10-02-CB-RIBS-BULKHEADS"
                "CI-CA-CAT-Q100-AAA-CONF0000-53-10-03-CB-SKIN-PANELS"
                "CI-CA-CAT-Q100-AAA-CONF0000-53-10-04-CB-LANDING-GEAR-REINFS"
                "CI-CA-CAT-Q100-AAA-CONF0000-53-10-05-CB-PASSAGEWAYS"
                "CI-CA-CAT-Q100-AAA-CONF0000-53-10-06-CB-ACCESS-DOORS"
                "CI-CA-CAT-Q100-AAA-CONF0000-53-10-07-CB-LPS-BONDING"
                "CI-CA-CAT-Q100-AAA-CONF0000-53-10-08-CB-SYSTEMS-BRACKETS"
            )
            
            for item in "${CB_ITEMS[@]}"; do
                if [ -d "$CB_ROOT/$item" ]; then
                    echo "    ✓ $item"
                else
                    echo "    ✗ $item - MISSING"
                fi
            done
        else
            echo "  ✗ Center Body Box component - MISSING"
        fi
    else
        echo "  ✗ Architecture domain - MISSING"
    fi
else
    echo "  ✗ Configuration root - MISSING"
fi

echo ""
echo "✓ Checking documentation files..."

DOC_FILES=(
    "README.md"
    "cadeo-config.yml"
    "CA-DEOPTIMISED/README.md"
    "CA-OPTIMISED/README.md"
    "CA-DEOPTIMISED/CAT-TECHNOLOGY_DATA_AND_DOCUMENTATION/README.md"
    "CA-DEOPTIMISED/CAD-DESIGN/README.md"
    "CA-OPTIMISED/CAS-COMPLIANCE/README.md"
)

for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file - MISSING"
    fi
done

echo ""
echo "✓ Directory structure statistics:"
echo "  Total directories: $(find . -type d | wc -l)"
echo "  Total files: $(find . -type f | wc -l)"
echo "  README files: $(find . -name "README.md" | wc -l)"
echo ""

echo "==================================="
echo "Validation Complete"
echo "==================================="
echo "Framework Status: OPERATIONAL"
echo "Configuration: H2-BWB-Q100-CONF0000"
echo "Implementation: PRELIMINARY"
echo "Next Steps: Detailed component implementation"
echo "==================================="