# FigCraft-MCP & Anti-Slop UI Design Rules

Always follow these rules when designing, modifying, or auditing UI screens in FigCraft:

## 1. Zero-Emoji & Vector Icon Policy
- **NEVER** place Unicode emojis (`✨`, `🔥`, `💰`, `📈`, `🍔`, `🚗`) inside any FigCraft text layer.
- Always use the `place_lucide_icon` MCP tool (or `figcraft_mcp.icons.icon_cmds` in batch calls) to render crisp 24x24 Lucide vector icons with precomputed bounding-box scaling.

## 2. Anti-Slop UI & Neutral Color Discipline
- **No AI Cliché Badges**: Never add gratuitous `"AI Insight"`, `"AI Matched"`, `"Hasil Scan Struk AI"`, or sparkle pill badges on headers, dropdown triggers, or summary cards.
- **Restrained Neutral Surfaces**:
  - Screen Background: `#FFFFFF` (forms/modals) or `#F8F9FA` (dashboard/analytics canvas).
  - Cards & Containers: `#FFFFFF` with `1px` border `#E2E8F0` and subtle shadow (`#0F172A0D`, offset `[0, 4]`, radius `12`).
  - Form Inputs & Dropdown Triggers: `#F8FAFC` or `#FFFFFF` fill, `#E2E8F0` or `#CBD5E1` border, `12px` corner radius. Never use loud orange/purple fills (`#FFF7ED`, `#F3F0FF`) on input fields or dropdown triggers.
- **Clean Segmented Switchers**:
  - Track: `#F1F2F6` (`height: 40..42px`, `cornerRadius: 12`).
  - Active Tab Pill: `#FFFFFF` (`height: 32..34px`, `cornerRadius: 9`), text `#1E1E2D` (`Bold`).
  - Inactive Tab: text `#8F92A1` (`Medium`).
  - **Never** put red/green arrows or colorful icons inside segmented switcher tabs.
- **Compact Searchable Dropdowns**:
  - Limit dropdown menu height (`132px..184px`) so it never stretches across the entire screen.
  - Include an internal `#F8FAFC` search input bar, neutral `#F1F5F9` active row highlight with `#1E1E2D` check icon, a `4px` vertical scrollbar track (`#F1F5F9`) & thumb (`#CBD5E1`), and a clean sticky footer action (`+ Category Baru`).
- **Single Primary Action Placement**:
  - Never duplicate action buttons (e.g., placing `+ Add Wallet` both in the top header and at the bottom of the screen). Place secondary creation triggers cleanly below the summary card (`Total Assets`).

## 3. Popup & Bottom Sheet Backdrop Rule
- Never place a popup modal or bottom sheet over a blank dark rectangle.
- Always duplicate the underlying parent screen at `(0, 0)` inside the popup frame (`locked: true`), place a full-screen scrim rectangle (`#0F172A`, `opacity: 0.45`) above it, and render the bottom sheet (`#FFFFFF`, `cornerRadius: [28, 28, 0, 0]`) on top.

## 4. Live Step-by-Step Cursor Streaming
- Prefer `batch` (which `figcraft-mcp` automatically streams step-by-step at `40ms` per element with multiplayer cursor movement and live selection highlights) so the user can watch the design assemble in real time on their canvas.

