# Changelog

All notable changes to **FigCraft-MCP** are documented in this file.

## [1.0.0] - 2026-11-07

### Added
- **Universal Stdio MCP Server (`src/figcraft_mcp/server.py`)**:
  - Automatic step-by-step live cursor streaming middleware (`~40ms` per element) with real-time `collab.cursor` tracking and `select: true` bounding-box highlights.
  - Automatic detection of active `.figcraft` documents and live collaboration sessions (`doc.list` + `collab.peers` on port `7979`).
- **3 Built-in High-Level MCP Tools**:
  - `place_lucide_icon`: Places any of 39 pre-scaled 24x24 Lucide vector icons with precomputed bounding boxes (`ICON_BBOX`) in a single call.
  - `create_prototype_link`: Connects interactive prototype flows (`smartAnimate`, `dissolve`, `push`, `slideIn`, `moveOut`) between frames.
  - `get_anti_slop_guidelines`: Returns the neutral Anti-Slop UI token system, banned AI clichés, and component recipes.
- **One-Command Auto-Setup (`figcraft-mcp setup`, `install.ps1`, `install.sh`)**:
  - Automatically detects and configures Google Antigravity, Claude Desktop, Claude Code, Cursor, and Windsurf with automatic `.bak` backups.
- **Bundled Agent Plugin, Skills & Rules**:
  - Added `plugin.json`, `.claude-plugin/plugin.json`, `rules/AGENTS.md`, `skills/figcraft/SKILL.md`, and `skills/anti-slop-ui/SKILL.md`.
- **Python SDK (`FigCraftLive`)**:
  - Scriptable client in `src/figcraft_mcp/client.py` for automated multi-screen generation and UI auditing.
