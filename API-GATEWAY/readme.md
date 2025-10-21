```
Robbbo-T/
├── api-gateway/                    # 🎯 NEW: API Gateway Module
│   ├── openapi/
│   │   └── openapi.v1.yaml         # OpenAPI 3.1 specification
│   ├── proto/
│   │   └── ampel/
│   │       └── v1/
│   │           └── data.proto      # gRPC definitions
│   ├── mcp/
│   │   ├── manifest.json           # MCP server manifest
│   │   └── connection.schema.json  # MCP connection schema
│   ├── services/
│   │   ├── api-gateway.ts          # Express gateway implementation
│   │   ├── resource-resolver.ts    # ampel:// URI resolver
│   │   └── websocket-handler.ts    # WebSocket upgrade handler
│   ├── security/
│   │   ├── pqc-signer.ts          # PQC Dilithium3 signing
│   │   └── auth-middleware.ts      # OAuth2/mTLS middleware
│   ├── integration/
│   │   ├── ampel-aqua-bridge.ts   # AMPEL-AQUA integration
│   │   └── det-manager.ts         # DET evidence manager
│   ├── clients/
│   │   └── ts/
│   │       └── src/
│   │           └── client.ts      # TypeScript SDK
│   ├── docs/
│   │   ├── ws-data.md            # WebSocket contracts
│   │   └── api-endpoints.md      # Endpoint documentation
│   ├── tests/
│   │   ├── contract/             # API contract tests
│   │   ├── integration/          # Integration tests
│   │   └── smoke/               # Smoke tests
│   ├── monitoring/
│   │   └── prometheus.yml        # Prometheus config
│   ├── keys/                     # PQC keys (gitignored)
│   ├── docker-compose.yml        # Local development stack
│   ├── package.json             # Node.js dependencies
│   ├── tsconfig.json           # TypeScript config
│   └── .env.example            # Environment template
│
├── schemas/                     # 📌 EXISTING: Move MCP schemas here
│   ├── mcp-server-connection.schema.json
│   ├── mcp-server-connection.example.json
│   └── api-endpoints.json
│
├── .github/
│   └── workflows/
│       ├── api-contract.yml    # 🎯 NEW: API contract tests
│       └── [existing workflows]
│
├── pipeline_automation.md       # Your existing pipeline doc
└── README.md