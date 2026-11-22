# FigCraft-MCP & Anti-Slop UI Design Rules

Always follow these rules when designing, modifying, or auditing UI screens in FigCraft:

## 1. Token Preservation & Inspection Efficiency (Strict)
- **NEVER** call `inspect_document` or `get_node` without depth limits on multi-screen documents (this dumps thousands of nodes and burns tens of thousands of tokens).
- **Inspect Canvas Fast**: Always call `list_screens` (`{"page": 1}`) first. It returns top-level screen names, IDs, positions, and bounds in < 200 tokens.
- **Targeted Modifications**: When editing or modifying an existing screen, call `find_nodes(parent=screen_id, query="...")` to look up the exact target node ID instead of dumping the screen hierarchy.
- **Single Batch Execution**: Always assemble new screens and components inside a single `batch` command using `$ref` back-references. Never call `create_node` sequentially 20-40 times.

## 2. Universal Anti-Slop Heuristics (Style-Agnostic)
These quality heuristics apply to any design style (Shadcn, iOS HIG, Material 3, Dark Modern):
- **Banish AI Buzzwords & Fluff**: Never add gratuitous "Magic...", "AI-Powered", "AI will auto-fill everything", "✨ AI Matched", or generic quote subtitles ("Manage your finances with confidence today"). Use direct, functional verbs ("Memindai Struk...", "Simpan Transaksi").
- **Zero-Emoji Policy**: NEVER place Unicode emojis (`✨`, `🔥`, `💰`, `📈`, `🍔`, `🚗`) inside text layers. Always use `place_lucide_icon` or `icon_cmds` for crisp vector icons.
- **No Arbitrary Canvas Gradients**: Never slap pastel/purple linear gradients on screen backgrounds without deliberate brand justification. Prefer solid, restful surfaces (`#FFFFFF`, `#F8F9FA`, or `#09090B`).
- **Spacing Grid Discipline**: Follow a strict 4pt/8pt grid (4, 8, 12, 16, 20, 24, 32px) for paddings, gaps, and dimensions.
- **Real Component States**: Dropdown menus must have max-height (`180px`) and scrollbars for overflow; segmented switchers must have a clear active pill indicator; search inputs must have placeholder states.
- **Single Primary Action**: Never duplicate primary action buttons in multiple places on one screen.

## 3. Few-Shot Style Learning (Match Existing Canvas)
- When working on an existing `.figcraft` document (like `FinFlow.figcraft`), inspect existing screens with `list_screens`.
- Identify clean reference screens (e.g. Screen 4 - Review Transaction, Screen 6 - Manage Wallets). Match their surface colors, border treatments, typography scale, and corner radii.
- For brand-new blank canvases, choose from `get_anti_slop_guidelines(style=...)` presets: `neutral_clean`, `ios_hig`, `material_m3`, or `dark_modern`.

## 4. Popup & Bottom Sheet Backdrop Rule
- Never place a popup modal or bottom sheet over a blank dark rectangle.
- Always duplicate the underlying parent screen at `(0, 0)` inside the popup frame (`locked: true`), place a full-screen scrim rectangle (`#0F172A`, `opacity: 0.45`) above it, and render the bottom sheet (`cornerRadius: [28, 28, 0, 0]`) on top.

## 5. Live Step-by-Step Cursor Streaming
- `figcraft-mcp` automatically streams `batch` commands step-by-step with multiplayer cursor movement and live selection highlights. Responses are compactly summarized (`{"status": "success", "created_count": N, "created_ids": [...]}`) to protect token budgets.
