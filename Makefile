install:
	npm ci

gen:
	node scripts/gen_index_and_anchors.mjs
	node scripts/gen_placeholders.mjs
	bash scripts/mermaid_to_svg.sh

emit:
	node scripts/emit_qs_from_yaml.mjs

validate:
	node scripts/validate_qs_events.mjs events/out/*.json

all: install gen emit validate

validate-aaa:
	python C-AMEDEO-FRAMEWORK/CA-OPTIMISED/CAB-BRAINSTORMING/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/scripts/validate_aaa.py

det-aaa:
	python C-AMEDEO-FRAMEWORK/CA-OPTIMISED/CAB-BRAINSTORMING/H2-BWB-Q100-CONF0000/AAA-ARCHITECTURES_AIRFRAMES_AERODYNAMICS/scripts/generate_det_stubs.py