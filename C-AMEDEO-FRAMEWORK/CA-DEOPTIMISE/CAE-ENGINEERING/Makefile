# AMPEL360 + CAE Pipeline Makefile
# Professional Engineering Optimization Workflow

.PHONY: help install clean cvar-select cae-pipeline full-pipeline test validate

# Default configuration
RISK_THRESHOLD ?= 0.95
MAX_CONFIGS ?= 1000
OUTPUT_DIR ?= ./ampel360_cae_results
PARALLEL_JOBS ?= 4

# Tool paths
CVAR_TOOL = tools/cvar_selection.py
CAE_TOOL = tools/cae_pipeline.py

help: ## Show this help message
	@echo "🚀 AMPEL360 + CAE Pipeline - Professional Engineering Optimization"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
	@echo ""
	@echo "Configuration variables:"
	@echo "  RISK_THRESHOLD=$(RISK_THRESHOLD)  CVaR risk threshold (0.95 = 95%)"
	@echo "  MAX_CONFIGS=$(MAX_CONFIGS)     Maximum configurations in G1 feasible set"
	@echo "  OUTPUT_DIR=$(OUTPUT_DIR)    Output directory"
	@echo "  PARALLEL_JOBS=$(PARALLEL_JOBS)              Maximum parallel CAE jobs"

install: ## Install dependencies and setup environment
	@echo "📦 Installing dependencies..."
	pip install -r .github/requirements.txt
	@echo "✅ Dependencies installed"

clean: ## Clean output directories and temporary files
	@echo "🧹 Cleaning output directories..."
	rm -rf $(OUTPUT_DIR)
	rm -rf ./ampel360_results
	rm -rf ./cae_pipeline_results
	rm -rf /tmp/CAE_CAMPAIGN_*
	@echo "✅ Cleanup complete"

cvar-select: ## Execute CVaR selection (G1→G2 optimization)
	@echo "🔄 Executing AMPEL360 CVaR Selection..."
	mkdir -p $(OUTPUT_DIR)
	python $(CVAR_TOOL) \
		--risk-threshold $(RISK_THRESHOLD) \
		--max-configs $(MAX_CONFIGS) \
		--output $(OUTPUT_DIR)/cvar_results \
		--cae-integration \
		--verbose
	@echo "✅ CVaR selection complete"

cae-pipeline: ## Execute CAE simulation pipeline (requires cvar-select first)
	@echo "🔄 Executing CAE Simulation Pipeline..."
	@if [ ! -f "$(OUTPUT_DIR)/cvar_results/cvar_selection_"*".json" ]; then \
		echo "❌ CVaR selection results not found. Run 'make cvar-select' first."; \
		exit 1; \
	fi
	python $(CAE_TOOL) \
		--cvar-results $$(ls $(OUTPUT_DIR)/cvar_results/cvar_selection_*.json | head -1) \
		--output $(OUTPUT_DIR)/cae_results \
		--parallel $(PARALLEL_JOBS) \
		--cav-integration \
		--verbose
	@echo "✅ CAE pipeline complete"

full-pipeline: clean cvar-select cae-pipeline ## Execute complete AMPEL360→CAE→CAV pipeline
	@echo "🎉 Complete pipeline execution finished!"
	@echo "📊 Results summary:"
	@if [ -f "$(OUTPUT_DIR)/cae_results/"*"_summary.json" ]; then \
		python -c "import json; data=json.load(open('$$(ls $(OUTPUT_DIR)/cae_results/*_summary.json | head -1)')); print(f\"   Configurations analyzed: {len(data['configuration_scores'])}\"); print(f\"   Simulations executed: {data['execution_summary']['total_simulations']}\"); print(f\"   Success rate: {data['execution_summary']['successful_simulations']}/{data['execution_summary']['total_simulations']}\"); print(f\"   Total execution time: {data['execution_summary']['total_execution_time_hrs']:.2f} hrs\")"; \
	fi
	@echo "📁 Output directory: $(OUTPUT_DIR)"

test: ## Run basic functionality tests
	@echo "🧪 Running AMPEL360 + CAE Pipeline tests..."
	@echo "Testing CVaR selection tool..."
	python $(CVAR_TOOL) --help > /dev/null
	@echo "Testing CAE pipeline tool..."
	python $(CAE_TOOL) --help > /dev/null
	@echo "✅ Basic tests passed"

validate: ## Validate YAML files and run linting
	@echo "🔍 Validating YAML files..."
	yamllint -s C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAE-ENGINEERING/ || true
	@echo "🔍 Checking Python syntax..."
	python -m py_compile $(CVAR_TOOL)
	python -m py_compile $(CAE_TOOL)
	@echo "✅ Validation complete"

demo: ## Run demonstration with small dataset
	@echo "🎬 Running AMPEL360 + CAE Pipeline demonstration..."
	$(MAKE) clean
	$(MAKE) cvar-select RISK_THRESHOLD=0.90 MAX_CONFIGS=100 OUTPUT_DIR=./demo_results
	$(MAKE) cae-pipeline PARALLEL_JOBS=2 OUTPUT_DIR=./demo_results
	@echo "🎉 Demonstration complete!"
	@echo "📁 Demo results in: ./demo_results"

quick-test: ## Quick test with minimal configuration
	@echo "⚡ Quick test execution..."
	python $(CVAR_TOOL) \
		--risk-threshold 0.95 \
		--max-configs 50 \
		--output ./quick_test \
		--cae-integration \
		--format json
	@echo "✅ Quick test complete"

benchmark: ## Run performance benchmark
	@echo "⏱️  Running performance benchmark..."
	@echo "Benchmarking CVaR selection..."
	time python $(CVAR_TOOL) \
		--risk-threshold 0.95 \
		--max-configs 1000 \
		--output ./benchmark_results \
		--format json
	@echo "✅ Benchmark complete"

# Documentation targets
docs-serve: ## Serve documentation (requires MkDocs)
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs serve; \
	else \
		echo "❌ MkDocs not installed. Install with: pip install mkdocs mkdocs-material"; \
	fi

docs-build: ## Build documentation
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs build; \
	else \
		echo "❌ MkDocs not installed. Install with: pip install mkdocs mkdocs-material"; \
	fi

# Development targets
dev-setup: install ## Setup development environment
	@echo "🛠️  Setting up development environment..."
	chmod +x $(CVAR_TOOL)
	chmod +x $(CAE_TOOL)
	@echo "✅ Development environment ready"

show-config: ## Show current configuration
	@echo "📋 Current Configuration:"
	@echo "  RISK_THRESHOLD: $(RISK_THRESHOLD)"
	@echo "  MAX_CONFIGS: $(MAX_CONFIGS)"
	@echo "  OUTPUT_DIR: $(OUTPUT_DIR)"
	@echo "  PARALLEL_JOBS: $(PARALLEL_JOBS)"
	@echo "  CVAR_TOOL: $(CVAR_TOOL)"
	@echo "  CAE_TOOL: $(CAE_TOOL)"