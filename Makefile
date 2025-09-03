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