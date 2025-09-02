# Quick Start Guide

Get the AMPEL360 CVaR Selection and Automated CAE Pipeline running in minutes.

## Prerequisites

- Python 3.8+ 
- Linux/Unix environment (tested on Ubuntu 20.04+)
- Minimum 8GB RAM, 50GB disk space
- Multi-core CPU recommended for parallel CAE execution

## Installation

```bash
# Clone the repository
git clone https://github.com/Robbbo-T/Robbbo-T.git
cd Robbbo-T/C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAE-ENGINEERING

# Install dependencies
make install

# Setup development environment
make dev-setup
```

## 5-Minute Demo

Run a complete AMPEL360→CAE→CAV pipeline demonstration:

```bash
make demo
```

This executes:
1. **CVaR Selection**: Generates 100 configurations, selects top 5 using CVaR@0.90
2. **CAE Pipeline**: Runs 30 multi-physics simulations (FEA, CFD, Thermal, Modal)
3. **CAV Integration**: Creates certification-ready packages

## Basic Usage

### CVaR Selection Only
```bash
# Quick CVaR optimization
python tools/cvar_selection.py \
    --risk-threshold 0.95 \
    --max-configs 1000 \
    --output ./my_results \
    --cae-integration \
    --verbose
```

### CAE Pipeline Only
```bash
# Execute simulations on existing CVaR results
python tools/cae_pipeline.py \
    --cvar-results ./my_results/cvar_selection_*.json \
    --parallel 4 \
    --cav-integration \
    --output ./simulation_results
```

### Complete Pipeline
```bash
# Full optimization + simulation workflow
make full-pipeline \
    RISK_THRESHOLD=0.95 \
    MAX_CONFIGS=5000 \
    PARALLEL_JOBS=8
```

## Understanding Output

### CVaR Selection Results
```
📁 CVaR Results:
├── cvar_selection_YYYYMMDD_HHMMSS.csv      # Analysis-ready data
├── cvar_selection_YYYYMMDD_HHMMSS.json     # CAE integration format
├── DET_AMPEL360_CVaR_YYYYMMDD_HHMMSS.yaml  # Audit evidence
└── cae_seeding_hints.yaml                  # CAE automation hints
```

### CAE Pipeline Results
```
📁 CAE Results:
├── CAE_CAMPAIGN_ID_summary.json            # Executive summary
├── CAE_CAMPAIGN_ID_detailed_results.csv    # Per-simulation data
├── DET_CAE_CAMPAIGN_ID.yaml                # Evidence package
└── cav_certification_package.yaml         # Authority submission
```

## Configuration Options

### CVaR Selection Parameters
- `--risk-threshold`: CVaR confidence level (0.90-0.99, default: 0.95)
- `--max-configs`: G1 feasible set size (100-50000, default: 10000)
- `--format`: Output format (csv, json, det, all)

### CAE Pipeline Parameters
- `--parallel`: Maximum concurrent simulations (1-32, default: 4)
- `--config`: Custom solver configuration (YAML)
- `--cav-integration`: Generate certification packages

## Next Steps

- [Architecture Overview](architecture.md) - Understand the system design
- [AMPEL360 CVaR Selection](ampel360/overview.md) - Deep dive into optimization
- [CAE Pipeline](cae/architecture.md) - Multi-physics simulation details
- [Development Workflow](workflows/development.md) - Contributing guidelines

## Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
# Ensure dependencies are installed
make install
```

**CAE pipeline fails with solver errors**
```bash
# Check solver availability (mock solvers used in demo)
make test
```

**Memory/disk space issues**
```bash
# Reduce configuration set size
make demo MAX_CONFIGS=50 PARALLEL_JOBS=2
```

**Permission errors**
```bash
# Ensure scripts are executable
make dev-setup
```

### Support

- 📚 [Full Documentation](index.md)
- 🐛 [Issue Tracker](https://github.com/Robbbo-T/Robbbo-T/issues)
- 📧 [CAE Engineering Team](mailto:cae-engineering@example.com)
- 📖 [QAL Framework Documentation](compliance/qal.md)