#!/usr/bin/env python3
"""
Anti-Slop UI Design System Tokens & Component Recipes for FigCraft.
Enforces neutral, restrained, human-designed interfaces inspired by Shadcn UI, Radix Primitives, and Apple HIG.
"""

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

BANNED_PATTERNS = [
    "NEVER use Unicode emojis (🔥, ✨, 💰, 📈, 🍔) inside text layers; always use `place_lucide_icon` or `icon_cmds`.",
    "NEVER add gratuitous 'AI Insight', 'AI Matched', 'Hasil Scan AI', or sparkle badges on forms, headers, or summary cards.",
    "NEVER color-code dropdown triggers or form inputs with loud orange/purple/neon backgrounds and borders (#FFF7ED / #F3F0FF).",
    "NEVER add colored arrow icons inside segmented tab switchers (keep tabs clean text-only on #F1F2F6 track + #FFFFFF active pill).",
    "NEVER duplicate primary action buttons (e.g., having '+ Add Wallet' in both the top header and the bottom of the screen).",
    "NEVER render popups/bottom sheets on an empty dark rectangle; always duplicate the underlying parent screen as a locked backdrop behind a 45% opacity #0F172A scrim.",
]

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

