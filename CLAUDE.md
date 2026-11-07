# CLAUDE.md - Project Context for AI Coding Agents

## Overview
`figcraft-mcp` is a zero-dependency Python 3.10+ Model Context Protocol (MCP) server, agent plugin, and SDK that connects AI agents to **FigCraft Desktop** on port `7979`.

## Key Commands
- **Run MCP Server (Stdio)**: `python -m figcraft_mcp.server`
- **Run Auto-Setup CLI**: `python -m figcraft_mcp.server setup`
- **Run Unit Tests**: `python -m unittest discover -s tests -p "test_*.py" -v`

## Architecture (`src/figcraft_mcp/`)
- `config.py`: Cross-platform binary resolution (`figcraft` & `figcraft-cli`), TCP port probe (`7979`), and desktop auto-launch.
- `server.py`: JSON-RPC stdio server wrapping `figcraft-cli mcp --attach 7979` with step-by-step live cursor streaming and 3 extra tools (`place_lucide_icon`, `create_prototype_link`, `get_anti_slop_guidelines`).
- `icons.py`: 39 Lucide 24x24 vector SVG paths and precomputed `ICON_BBOX` tuples.
- `tokens.py`: Neutral Anti-Slop UI tokens, banned patterns, and component recipes.
- `client.py`: `FigCraftLive` Python SDK for script-driven automation.
- `setup_cli.py`: Automatic configuration installer for Antigravity, Claude, Cursor, and Windsurf.
