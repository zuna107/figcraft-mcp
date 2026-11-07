---
name: figcraft
description: Design, create, edit, inspect, and prototype UI screens, frames, components, and vector graphics live in FigCraft via the FigCraft-MCP server. Includes automatic step-by-step multiplayer cursor streaming, 40+ Lucide vector icons, interactive prototype wiring, and Anti-Slop UI design tokens.
---

# FigCraft Live MCP Skill Guide

`figcraft-mcp` connects any AI coding agent directly to the live **FigCraft Desktop** canvas (`--attach 7979`) with automatic live collaboration room detection, step-by-step multiplayer cursor streaming (`collab.cursor` + live selection highlight), precomputed Lucide vector icons, and Anti-Slop UI design guidelines.

---

## 1. Workflow for Creating or Editing Screens

1. **Load Anti-Slop Design Tokens**:
   - Call `get_anti_slop_guidelines` (or read `skills/anti-slop-ui/SKILL.md`) before creating new screens to lock in the neutral color palette, typography scale (`Plus Jakarta Sans`), and spacing rules.
2. **Inspect Canvas Fast**:
   - Use `get_node` on Page 1 (`{"id": 1, "depth": 1, "fields": ["id", "name", "x", "y", "width", "height", "children"]}`) for a fast 4ms overview of top-level screen frames instead of dumping the entire document tree when possible.
3. **Stream Elements Step-by-Step via `batch`**:
   - Group screen elements into `batch` commands using `$ref` references.
   - `figcraft-mcp` automatically streams `batch` commands step-by-step (`~40ms` per element), moving the multiplayer cursor (`collab.cursor`) and highlighting each created node (`select: true`) live on the user's open FigCraft window.
4. **Use Vector Icons (`place_lucide_icon`)**:
   - Never use Unicode emojis. Call `place_lucide_icon` (or `icon_cmds` in Python scripts) to place any of the built-in 24x24 Lucide vector icons (`search`, `download`, `wallet`, `home`, `barChart`, `plus`, `x`, `check`, `chevronDown`, `chevronLeft`, `chevronRight`, `user`, `mail`, `lock`, `eyeOff`, `camera`, `image`, `folder`, `edit`, `trash2`, etc.).
5. **Wire Interactive Prototype Flows (`create_prototype_link`)**:
   - Call `create_prototype_link` with `sourceId`, `targetFrameId`, `transition` (`"smartAnimate"`, `"dissolve"`, `"push"`, `"slideIn"`, `"moveOut"`), `direction`, and `durationMs`.
6. **Verify Visually & Save**:
   - Export modified screens using `export` (`format: "png", scale: 2`) or `screenshot` to inspect alignment, contrast, and spacing, then call `save_file`.

---

## 2. High-Value MCP Tools

| Tool Name | Purpose |
| :--- | :--- |
| `get_anti_slop_guidelines` | Returns the neutral color tokens, typography scale, banned AI clichés, and component recipes. |
| `place_lucide_icon` | Places a scaled 24x24 Lucide vector icon inside any frame in 1 step with live cursor movement. |
| `create_prototype_link` | Connects a clickable element (`sourceId`) to a destination screen (`targetFrameId`) with transition animations. |
| `batch` | Creates and styles multiple layers using `$ref` back-references, streamed step-by-step live on canvas. |
| `get_node` / `inspect_document` | Inspects layer hierarchy, coordinates, and properties. |
| `create_node` / `set_properties` | Creates or updates individual frames, rectangles, text, ellipses, or vectors. |
| `export` / `screenshot` | Renders crisp 2x PNG previews of any frame ID for visual verification. |
| `save_file` | Saves the active `.figcraft` document to disk. |

---

## 3. Python SDK (`figcraft_mcp.FigCraftLive`)

For large multi-screen builds or automated audits, you can also import `FigCraftLive` directly in Python:

```python
from figcraft_mcp import FigCraftLive, icon_cmds

fc = FigCraftLive(step_delay=0.040)
fc.register_frame_origin(frame_id, 1700, 100)
fc.batch([
    *icon_cmds(frame_id, "Search Icon", "search", 14, 12, 16, "#64748B", 1.8),
], label="Add Search Icon", stream=True)
fc.save()
fc.close()
```

