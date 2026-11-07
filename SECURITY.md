# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Architecture

- **Local Loopback Control Only**: `figcraft-mcp` connects strictly to `127.0.0.1` (default port `7979`) to communicate with the local FigCraft Desktop instance via standard input/output (stdio).
- **Zero External Network Calls**: The MCP server does not transmit design documents, tokens, or telemetry to any external server.
- **Safe Config Backups**: When running `figcraft-mcp setup`, existing IDE configuration files are automatically backed up with a `.bak` extension before adding the `figcraft` server entry.

## Reporting a Vulnerability

If you discover a security vulnerability within `figcraft-mcp`, please report it via [GitHub Security Advisories](https://github.com/zuna107/figcraft-mcp/security/advisories) or open a security issue on the repository rather than posting sensitive exploit details publicly.
