#!/usr/bin/env python3
"""
Tool schemas for FigCraft-MCP high-level and token-optimized tools.
"""

from .icons import ICONS

EXTRA_TOOLS = [
    {
        "name": "list_screens",
        "description": "Fast and token-efficient overview of all top-level screen frames on the page (IDs, names, positions, sizes). Uses outline projection to save 90%+ tokens.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "default": 1, "description": "Page node ID (default: 1)"},
            },
        },
    },
    {
        "name": "find_nodes",
        "description": "Fast token-saving search for specific layers inside a screen or frame by name substring, text content, or node type. Use when inspecting or modifying existing screens.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "parent": {"type": "integer", "description": "Parent screen or frame node ID to search inside"},
                "query": {"type": "string", "description": "Case-insensitive substring to match against node name or text content"},
                "type": {
                    "type": "string",
                    "enum": ["frame", "text", "rectangle", "vector", "ellipse", "group"],
                    "description": "Optional node type filter",
                },
            },
            "required": ["parent", "query"],
        },
    },
    {
        "name": "create_from_template",
        "description": "Instantiate an official FigCraft starter template (mobile-app, dashboard, landing-page, design-system, wireframe-kit, social-posts, slides, icon-set). Generates a complete, beautiful, production-ready screen structure with auto-layout and 0 AI-slop in milliseconds.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template": {
                    "type": "string",
                    "enum": [
                        "mobile-app",
                        "landing-page",
                        "dashboard",
                        "design-system",
                        "wireframe-kit",
                        "social-posts",
                        "slides",
                        "icon-set",
                    ],
                    "description": "Starter template identifier to instantiate",
                },
                "name": {
                    "type": "string",
                    "description": "Optional custom name for the created document",
                },
            },
            "required": ["template"],
        },
    },
    {
        "name": "inspect_code",
        "description": "Generate production-ready code directly from any canvas layer/frame into Tailwind CSS v4, Jetpack Compose, SwiftUI, React TSX, Flutter, or HTML. Extremely fast native code generation without LLM hallucination.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nodeId": {
                    "type": "integer",
                    "description": "Layer/Frame ID to inspect (omit to use current selection)",
                },
                "language": {
                    "type": "string",
                    "enum": ["tailwind", "compose", "swiftui", "react", "flutter", "html", "css", "vue", "leptos"],
                    "default": "tailwind",
                    "description": "Target framework or language",
                },
            },
        },
    },
    {
        "name": "extract_canvas_tokens",
        "description": "Extract design tokens, color variables, typography styles, and component references directly from the active canvas. Compact, few-shot ready format for perfect design consistency.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "collection": {
                    "type": "string",
                    "description": "Optional collection filter name",
                },
            },
        },
    },
    {
        "name": "place_lucide_icon",
        "description": "Place a crisp 24x24 Lucide vector icon (never use Unicode emojis) inside a parent frame with automatic scaling and live cursor animation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "parent": {"type": "integer", "description": "Parent frame/node ID"},
                "name": {"type": "string", "description": "Layer name for the icon"},
                "icon": {
                    "type": "string",
                    "enum": sorted(ICONS.keys()),
                    "description": "Lucide icon key",
                },
                "x": {"type": "number", "description": "X coordinate inside parent"},
                "y": {"type": "number", "description": "Y coordinate inside parent"},
                "size": {"type": "number", "default": 16, "description": "Target icon size in px"},
                "color": {"type": "string", "default": "#1E1E2D", "description": "Stroke hex color"},
                "strokeWeight": {"type": "number", "default": 1.8, "description": "Stroke width"},
            },
            "required": ["parent", "name", "icon", "x", "y"],
        },
    },
    {
        "name": "create_prototype_link",
        "description": "Connect an interactive prototype flow link from a trigger node to a destination frame.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sourceId": {"type": "integer", "description": "Clickable trigger layer ID"},
                "targetFrameId": {"type": "integer", "description": "Destination screen frame ID"},
                "transition": {
                    "type": "string",
                    "enum": ["smartAnimate", "dissolve", "push", "slideIn", "moveOut", "instant"],
                    "default": "smartAnimate",
                },
                "direction": {
                    "type": "string",
                    "enum": ["left", "right", "top", "bottom"],
                    "default": "left",
                },
                "durationMs": {"type": "number", "default": 240},
            },
            "required": ["sourceId", "targetFrameId"],
        },
    },
    {
        "name": "get_anti_slop_guidelines",
        "description": "Retrieve Anti-Slop UI Quality Heuristics, multi-style presets (neutral_clean, ios_hig, material_m3, dark_modern), and few-shot guidance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "style": {
                    "type": "string",
                    "enum": ["neutral_clean", "ios_hig", "material_m3", "dark_modern", "all"],
                    "default": "neutral_clean",
                    "description": "Design preset style to retrieve tokens for",
                },
            },
        },
    },
]
