---
name: figcraft
description: Design, create, edit, inspect, and prototype UI screens, frames, components, and vector graphics live in FigCraft via the FigCraft-MCP server. Includes automatic step-by-step multiplayer cursor streaming, 40+ Lucide vector icons, interactive prototype wiring, few-shot style learning, and token-optimized inspection tools.
---

# FigCraft Live MCP Skill Guide

`figcraft-mcp` connects any AI coding agent directly to the live **FigCraft Desktop** canvas (`--attach 7979`) with automatic live collaboration room detection, step-by-step multiplayer cursor streaming (`collab.cursor` + live selection highlight), precomputed Lucide vector icons, multi-style design presets, and token-saving inspection tools (`list_screens`, `find_nodes`).

---

## 1. Optimized Workflow for Creating or Editing Screens

1. **Inspect Canvas Fast (`list_screens`)**:
   - Always call `list_screens` (`{"page": 1}`) to get screen names, IDs, positions, and bounds. Avoid calling `inspect_document` without depth limits to save 95%+ tokens.
2. **Apply Few-Shot Style or Load Preset**:
   - If clean screens already exist on canvas (e.g. Screen 4 - Review Transaction, Screen 6 - Manage Wallets), adopt their colors, card corner radii, and typography tokens.
   - If starting fresh, call `get_anti_slop_guidelines` with your preferred style (`"neutral_clean"`, `"ios_hig"`, `"material_m3"`, or `"dark_modern"`).
3. **Stream Elements Step-by-Step via `batch`**:
   - Group screen elements into a single `batch` call using `$ref` back-references.
   - `figcraft-mcp` automatically streams `batch` commands step-by-step (`~40ms` per element) with live multiplayer cursor movement, and returns a compact summary response to conserve LLM tokens.
4. **Targeted Modifications (`find_nodes`)**:
   - When modifying an existing screen, call `find_nodes(parent=screen_id, query="Button Name")` to quickly obtain node IDs instead of dumping the layer tree.
5. **Use Vector Icons (`place_lucide_icon`)**:
   - Never use Unicode emojis. Call `place_lucide_icon` (or `icon_cmds` in Python scripts) to place crisp 24x24 Lucide vector icons (`search`, `wallet`, `home`, `barChart`, `plus`, `x`, `check`, `chevronDown`, `user`, etc.).
6. **Wire Interactive Prototype Flows (`create_prototype_link`)**:
   - Connect triggers (`sourceId`) to destination screens (`targetFrameId`) with `smartAnimate`, `dissolve`, `push`, `slideIn`, or `moveOut`.
7. **Verify Visually & Save**:
   - Preview modified frames using `export` (`format: "png", scale: 2`) or `screenshot`, then call `save_file`.

---

## 2. High-Value MCP Tools

| Tool Name | Purpose & Token Optimization |
| :--- | :--- |
| `list_screens` | **Token Saver**: Lists top-level screen frames on the page (IDs, names, bounds) in < 200 tokens. |
| `find_nodes` | **Token Saver**: Substring search for layers by name or text within a frame, preventing full tree dumps. |
| `batch` | Creates and styles multiple layers in 1 request. Returns compact summary to preserve token budget. |
| `place_lucide_icon` | Places a scaled 24x24 Lucide vector icon inside any frame in 1 step with live cursor movement. |
| `create_prototype_link` | Connects a clickable element (`sourceId`) to a destination screen (`targetFrameId`) with animations. |
| `get_anti_slop_guidelines` | Returns universal quality heuristics, multi-style presets (`neutral_clean`, `ios_hig`, `material_m3`, `dark_modern`), and component recipes. |
| `get_node` / `inspect_document` | Inspects node properties (always specify `depth` when inspecting subtrees). |
| `create_node` / `set_properties` | Creates or updates individual layers. |
| `export` / `screenshot` | Renders crisp 2x PNG previews of any frame ID for visual verification. |
| `save_file` | Saves the active `.figcraft` document to disk. |

---

## 3. Python SDK (`figcraft_mcp.FigCraftLive`)

For programmatic automation, the Python SDK supports all high-level methods:

```python
from figcraft_mcp import FigCraftLive, icon_cmds

fc = FigCraftLive(step_delay=0.040)
screens = fc.list_screens(page_id=1)
print("Found screens:", [s["name"] for s in screens])

# Targeted node lookup
target_buttons = fc.find_nodes(parent_id=screens[0]["id"], query="Save", node_type="frame")

# Single batch execution
fc.batch([
    *icon_cmds(screens[0]["id"], "Search Icon", "search", 14, 12, 16, "#64748B", 1.8),
], label="Add Search Icon", stream=True)

fc.save()
fc.close()
```
