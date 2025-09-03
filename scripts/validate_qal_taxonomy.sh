#!/usr/bin/env bash

# QAL Taxonomía Extendida — BWB-Q100
# CI validation script for UTCS-MI v5.0 compliance
set -euo pipefail

echo "🔍 Validating QAL Taxonomía Extendida — BWB-Q100..."

# Check required documentation files
echo "📋 Checking documentation files..."
test -f docs/taxonomy/index-table.md || { echo "❌ Missing docs/taxonomy/index-table.md"; exit 1; }
test -f docs/taxonomy/anchors.html || { echo "❌ Missing docs/taxonomy/anchors.html"; exit 1; }
test -f docs/diagrams/qal-taxonomy.mmd || { echo "❌ Missing docs/diagrams/qal-taxonomy.mmd"; exit 1; }
test -f docs/QAL-TAXONOMIA-EXTENDIDA-BWB-Q100.md || { echo "❌ Missing main documentation file"; exit 1; }

# Check domain placeholder files
echo "📄 Checking domain placeholders..."
for d in AAA AAP CCC CQH DDD EDI EEE EER IIF IIS LCC LIB MMM OOO ppp; do
  test -f "docs/taxonomy/placeholders/$d.md" || { echo "❌ Missing docs/taxonomy/placeholders/$d.md"; exit 1; }
done

# Check scripts and schemas
echo "⚙️ Checking scripts and schemas..."
test -f scripts/gen_index_and_anchors.mjs || { echo "❌ Missing generation script"; exit 1; }
test -f scripts/gen_placeholders.mjs || { echo "❌ Missing placeholders script"; exit 1; }
test -f scripts/emit_qs_from_yaml.mjs || { echo "❌ Missing QS emission script"; exit 1; }
test -f scripts/validate_qs_events.mjs || { echo "❌ Missing QS validation script"; exit 1; }
test -f schemas/qs.published.schema.json || { echo "❌ Missing QS schema"; exit 1; }

# Check domain configuration
echo "🌐 Checking domain configuration..."
test -f scripts/domain_list.json || { echo "❌ Missing domain list"; exit 1; }

# Validate domain count (should be 15 domains)
domain_count=$(jq '.domains | length' scripts/domain_list.json)
if [ "$domain_count" -ne 15 ]; then
  echo "❌ Expected 15 domains, found $domain_count"
  exit 1
fi

# Check for required domains
required_domains=("AAA" "CQH" "ppp" "DDD" "EDI" "EEE" "EER" "IIF" "IIS" "LCC" "LIB" "MMM" "OOO" "AAP" "CCC")
for domain in "${required_domains[@]}"; do
  if ! jq -e ".domains[] | select(.code == \"$domain\")" scripts/domain_list.json > /dev/null; then
    echo "❌ Missing required domain: $domain"
    exit 1
  fi
done

# Check QAL directories exist for key domains  
echo "📂 Checking QAL domain structure..."
for key_domain in AAA CQH ppp; do
  test -d "qal/$key_domain" || { echo "❌ Missing qal/$key_domain directory"; exit 1; }
  test -f "qal/$key_domain/kit.yaml" || { echo "❌ Missing qal/$key_domain/kit.yaml"; exit 1; }
done

# Validate NPM ecosystem
echo "📦 Checking NPM configuration..."
test -f package.json || { echo "❌ Missing package.json"; exit 1; }
test -f package-lock.json || { echo "❌ Missing package-lock.json"; exit 1; }

# Check that all NPM scripts exist
required_scripts=("gen" "emit" "validate:qs" "validate:det" "all")
for script in "${required_scripts[@]}"; do
  if ! jq -e ".scripts.\"$script\"" package.json > /dev/null; then
    echo "❌ Missing NPM script: $script"
    exit 1
  fi
done

# Test that generation works
echo "🔄 Testing generation pipeline..."
if ! npm run gen > /dev/null 2>&1; then
  echo "❌ Generation pipeline failed"
  exit 1
fi

# Test that emission works  
echo "📡 Testing QS emission..."
if ! npm run emit > /dev/null 2>&1; then
  echo "❌ QS emission failed"
  exit 1
fi

# Test validation
echo "✅ Testing validation pipeline..."
if ! npm run validate:qs > /dev/null 2>&1; then
  echo "❌ QS validation failed"
  exit 1
fi

if ! npm run validate:det > /dev/null 2>&1; then
  echo "❌ DET validation failed"
  exit 1
fi

# Check UTCS-MI v5.0 compliance in main documentation
echo "📋 Checking UTCS-MI v5.0 compliance..."
if ! grep -q "EstándarUniversal:" docs/QAL-TAXONOMIA-EXTENDIDA-BWB-Q100.md; then
  echo "❌ Missing UTCS-MI v5.0 canonical header"
  exit 1
fi

# Check BWB-Q100 program references
if ! grep -q "BWB-Q100" docs/QAL-TAXONOMIA-EXTENDIDA-BWB-Q100.md; then
  echo "❌ Missing BWB-Q100 program reference"
  exit 1
fi

# Validate taxonomy levels
echo "🏗️ Checking taxonomy levels..."
required_levels=("TFA" "SI" "CV" "SE" "DI" "CE" "CC" "CI" "CP" "FE" "QS")
for level in "${required_levels[@]}"; do
  if ! grep -q "$level" docs/QAL-TAXONOMIA-EXTENDIDA-BWB-Q100.md; then
    echo "❌ Missing taxonomy level: $level"
    exit 1
  fi
done

# Check alias support
echo "🔗 Checking alias support..."
required_aliases=("ta-" "sa-" "dinv-" "cenv-")
for alias in "${required_aliases[@]}"; do
  if ! grep -q "$alias" docs/QAL-TAXONOMIA-EXTENDIDA-BWB-Q100.md; then
    echo "❌ Missing alias reference: $alias"
    exit 1
  fi
done

echo "✔️ QAL Taxonomía: All validations passed!"
echo "🎯 BWB-Q100 program taxonomy is UTCS-MI v5.0 compliant"
echo "📊 System ready for production use"