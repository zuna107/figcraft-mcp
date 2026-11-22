#!/usr/bin/env python3
"""
Anti-Slop UI Design System Tokens, Multi-Style Presets & Component Recipes for FigCraft.
Enforces high aesthetic quality, clean typography, purposeful hierarchy, and prevents AI slop clichés
across multiple design paradigms (Neutral/Shadcn, iOS HIG, Material 3, and Dark Modern).
"""

# Default neutral tokens (backward compatible)
ANTI_SLOP_TOKENS = {
    "colors": {
        "surface_primary": "#FFFFFF",
        "surface_canvas": "#F8F9FA",
        "surface_input": "#F8FAFC",
        "surface_muted_track": "#F1F2F6",
        "surface_selected_row": "#F1F5F9",
        "border_subtle": "#E2E8F0",
        "border_default": "#CBD5E1",
        "text_primary": "#1E1E2D",
        "text_secondary": "#475569",
        "text_muted": "#8F92A1",
        "text_placeholder": "#94A3B8",
        "brand_primary": "#6C5CE7",
        "semantic_success": "#00B894",
        "semantic_danger": "#FF7675",
    },
    "typography": {
        "font_family": "Plus Jakarta Sans",
        "scale": {
            "hero_amount": {"size": 28, "style": "Bold", "color": "#1E1E2D"},
            "screen_title": {"size": 18, "style": "Bold", "color": "#1E1E2D"},
            "section_title": {"size": 14, "style": "Bold", "color": "#1E1E2D"},
            "input_value": {"size": 13.5, "style": "SemiBold", "color": "#1E1E2D"},
            "body_default": {"size": 12.5, "style": "Medium", "color": "#1E1E2D"},
            "field_label": {"size": 10.5, "style": "Bold", "color": "#8F92A1"},
            "caption_muted": {"size": 11.5, "style": "Regular", "color": "#8F92A1"},
        },
    },
    "spacing_radii": {
        "mobile_frame": {"width": 360, "height": 800, "radius": 24, "frame_gap_x": 400},
        "horizontal_padding": 20,
        "card_radius": 16,
        "input_radius": 12,
        "dropdown_radius": 12,
        "dropdown_row_radius": 7,
        "button_radius": 14,
    },
}

UNIVERSAL_HEURISTICS = [
    {
        "id": "no_ai_buzzwords",
        "title": "Banish AI Fluff & Buzzwords",
        "rule": "NEVER use AI clichés like 'Magic Scanning...', 'AI will auto-fill everything', '✨ AI Matched', or generic fluff subtitles like 'Manage your finances with confidence today'. Use clear, functional action verbs ('Memindai Struk...', 'Review Transaksi').",
    },
    {
        "id": "vector_icons_over_emojis",
        "title": "Strict Vector Icons Only",
        "rule": "NEVER place Unicode emojis (🔥, ✨, 💰, 📈, 🍔, 🚗) in text layers. Always use vector icons (via `place_lucide_icon` or `icon_cmds`).",
    },
    {
        "id": "spacing_grid_discipline",
        "title": "4pt / 8pt Spacing Grid",
        "rule": "All margins, paddings, and element dimensions must follow a 4pt/8pt grid (4, 8, 12, 16, 20, 24, 32px). Never use arbitrary random values (e.g. 13px, 17px, 23px).",
    },
    {
        "id": "purposeful_interaction_states",
        "title": "Real Functional States",
        "rule": "Interactive components must reflect real UX states: dropdowns must have max-height and scrollbars for overflow; search bars inside pickers; clear selected row indicators; active tab indicator in segmented switchers.",
    },
    {
        "id": "single_primary_cta",
        "title": "Single Primary Action",
        "rule": "Never duplicate primary actions in multiple locations (e.g., adding '+ Add Wallet' both in header and bottom). Keep one primary CTA per viewport.",
    },
    {
        "id": "locked_parent_backdrops",
        "title": "Layered Modal Backdrops",
        "rule": "Never render popups or bottom sheets over an empty dark void. Duplicate the parent screen at (0, 0) with locked=True, cover with a 45% opacity #0F172A scrim, and place the modal on top.",
    },
]

BANNED_PATTERNS = [
    "NEVER use Unicode emojis (🔥, ✨, 💰, 📈, 🍔) inside text layers; always use `place_lucide_icon` or `icon_cmds`.",
    "NEVER add gratuitous 'AI Insight', 'AI Matched', 'Hasil Scan AI', 'Magic', or sparkle badges on forms, headers, or summary cards.",
    "NEVER place arbitrary pastel/neon linear gradients on screen canvas backgrounds without intentional theme justification.",
    "NEVER color-code dropdown triggers or form inputs with loud orange/purple/neon backgrounds and borders (#FFF7ED / #F3F0FF).",
    "NEVER add colored arrow icons inside segmented tab switchers (keep tabs clean text-only with active pill highlight).",
    "NEVER duplicate primary action buttons (e.g., having '+ Add Wallet' in both the top header and the bottom of the screen).",
    "NEVER render popups/bottom sheets on an empty dark rectangle; always duplicate the underlying parent screen as a locked backdrop behind a 45% opacity #0F172A scrim.",
]

STYLE_PRESETS = {
    "neutral_clean": {
        "name": "Neutral Clean (Shadcn / Radix inspired)",
        "surface_canvas": "#F8F9FA",
        "surface_card": "#FFFFFF",
        "surface_input": "#F8FAFC",
        "border": "#E2E8F0",
        "text_primary": "#1E1E2D",
        "text_muted": "#8F92A1",
        "brand_primary": "#6C5CE7",
        "card_radius": 16,
        "button_radius": 12,
        "font_family": "Plus Jakarta Sans",
    },
    "ios_hig": {
        "name": "Apple iOS Human Interface Guidelines",
        "surface_canvas": "#F2F2F7",
        "surface_card": "#FFFFFF",
        "surface_input": "#FFFFFF",
        "border": "#E5E5EA",
        "text_primary": "#000000",
        "text_muted": "#8E8E93",
        "brand_primary": "#007AFF",
        "card_radius": 14,
        "button_radius": 12,
        "font_family": "Inter",
    },
    "material_m3": {
        "name": "Google Material 3",
        "surface_canvas": "#FEF7FF",
        "surface_card": "#F7F2FA",
        "surface_input": "#ECE6F0",
        "border": "#CAC4D0",
        "text_primary": "#1D1B20",
        "text_muted": "#49454F",
        "brand_primary": "#6750A4",
        "card_radius": 16,
        "button_radius": 20,
        "font_family": "Roboto",
    },
    "dark_modern": {
        "name": "Modern Obsidian Dark",
        "surface_canvas": "#09090B",
        "surface_card": "#18181B",
        "surface_input": "#27272A",
        "border": "#27272A",
        "text_primary": "#FAFAFA",
        "text_muted": "#A1A1AA",
        "brand_primary": "#6366F1",
        "card_radius": 16,
        "button_radius": 12,
        "font_family": "Plus Jakarta Sans",
    },
}

FEW_SHOT_GUIDANCE = """
FEW-SHOT CANVAS STYLE LEARNING:
When working on an existing FigCraft project with prior screens:
1. Call `list_screens` first to discover existing screens.
2. Identify a clean, high-quality reference screen (e.g. Screen 4 - Review Transaction, Screen 6 - Manage Wallets).
3. Extract and match its design tokens:
   - Match canvas fill and card surface colors.
   - Match corner radii on cards, inputs, and buttons.
   - Match typography font family and scale.
4. Avoid mimicking slop screens (e.g., screens with gratuitous gradients, motivational quote greetings, or colorful emoji badges).
5. Only if starting a brand new blank document, ask the user or default to `neutral_clean`.
"""

COMPONENT_RECIPES = {
    "segmented_switcher": {
        "track": {"height": 40, "fill": "#F1F2F6", "cornerRadius": 12},
        "active_pill": {"height": 32, "fill": "#FFFFFF", "cornerRadius": 9, "textColor": "#1E1E2D", "fontStyle": "Bold"},
        "inactive_tab": {"textColor": "#8F92A1", "fontStyle": "Medium"},
        "rule": "No icons inside segmented tabs. Text only, centered.",
    },
    "searchable_scrollable_dropdown": {
        "trigger": {"height": 42, "fill": "#FFFFFF", "stroke": "#CBD5E1", "cornerRadius": 12},
        "menu": {"maxHeight": 180, "fill": "#FFFFFF", "stroke": "#E2E8F0", "cornerRadius": 12},
        "search_bar": {"height": 34, "fill": "#F8FAFC", "stroke": "#E2E8F0", "cornerRadius": 8},
        "active_row": {"height": 28, "fill": "#F1F5F9", "cornerRadius": 7, "textColor": "#1E1E2D", "checkIcon": "#1E1E2D"},
        "scrollbar": {"trackFill": "#F1F5F9", "thumbFill": "#CBD5E1", "width": 4},
        "not_found_state": "1 muted line ('Tidak ditemukan') + 1 clean action row ('+ Category Baru \"<query>\"').",
    },
    "popup_bottom_sheet": {
        "backdrop": "Duplicate the parent screen at (0, 0) with locked=True",
        "scrim": {"fill": "#0F172A", "opacity": 0.45, "width": 360, "height": 800},
        "sheet": {"fill": "#FFFFFF", "cornerRadius": [28, 28, 0, 0]},
    },
}
