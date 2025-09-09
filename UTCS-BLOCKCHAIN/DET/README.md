# DET — Digital Evidence Twin

Emit evidence packets with:
- `det_packet.json` (schema in `DET/schemas/det-packet.schema.json`)
- `signature.ed25519` over `det_packet.json`
- `previous_hash` (sha256 of previous packet)
- `trace.yaml` (bidirectional links to TRACES)
- `cadet.yaml` (links to CADET KPI cuts)