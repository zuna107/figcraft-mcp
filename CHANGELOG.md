# Changelog

All notable changes to **FigCraft-MCP** are documented in this file.

## [1.1.0] - 2026-11-22

### Added
- **Token-Optimized Canvas Inspection Tools**:
  - `list_screens`: High-speed inspection tool that queries top-level screen frames on the page (IDs, names, positions, bounds) in < 200 tokens, saving 98%+ tokens compared to `inspect_document`.
  - `find_nodes`: Targeted search tool for layers within a screen frame by name, substring, or text content (`parent`, `query`, `type`), saving 90%+ tokens during UI edits and refactoring.
- **Universal Anti-Slop UI & Multi-Style Presets**:
  - Decoupled strict Shadcn enforcement into universal quality heuristics (banning AI fluff words, Unicode emojis, arbitrary gradients, and incomplete states) suitable for any design paradigm.
  - Added multi-style presets in `get_anti_slop_guidelines(style=...)`: `neutral_clean` (Shadcn/Slate), `ios_hig` (Apple HIG), `material_m3` (Google Material 3), and `dark_modern` (Obsidian Dark).
  - Added Few-Shot Canvas Style Learning workflow allowing agents to adopt existing project aesthetics directly from mature reference screens (e.g., Screen 4 and Screen 6 in `FinFlow.figcraft`).
- **Python SDK Enhancements (`FigCraftLive`)**:
  - Added `fc.list_screens(page_id=1)` and `fc.find_nodes(parent_id, query, node_type=None)` helper methods.

### Changed
- **Token-Preserving Batch Responses**:
  - `batch` executions now return a compact summary (`status`, `created_count`, `root_id`, `created_ids`) instead of full raw attribute trees, saving thousands of LLM output tokens per screen generation. Full raw responses remain accessible via `verbose: true`.
- **Modular Code Architecture**:
  - Extracted tool schemas to `src/figcraft_mcp/tools_schema.py`.
  - Extracted streaming batch execution to `src/figcraft_mcp/batch_streamer.py`.
- **Documentation & Rules**:
  - Updated `rules/AGENTS.md`, `skills/figcraft/SKILL.md`, and `skills/anti-slop-ui/SKILL.md` with token-saving rules and few-shot design heuristics.

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

