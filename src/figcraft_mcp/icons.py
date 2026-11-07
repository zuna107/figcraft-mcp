#!/usr/bin/env python3
"""
Precomputed 24x24 Lucide Vector Icon Library for FigCraft.
Eliminates Unicode emojis completely and provides 0-roundtrip `icon_cmds` for batch & live streaming.
"""

ICONS = {
    "logout": "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4 M16 17l5-5-5-5 M21 12H9",
    "wallet": "M21 12V7H5a2 2 0 0 1 0-4h14v4 M3 5v14a2 2 0 0 0 2 2h16v-5 M16 12h5v4h-5z",
    "utensils": "M18 2v20 M21 15V2a3 3 0 0 0-3 3v4a3 3 0 0 0 3 3z M6 2v6 M3 2v4a3 3 0 0 0 6 0V2 M6 8v14",
    "car": "M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2 M9 17h6 M7 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M17 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
    "shoppingBag": "M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z M3 6h18 M16 10a4 4 0 0 1-8 0",
    "gamepad2": "M6 11h4 M8 9v4 M15 12h.01 M18 10h.01 M17.3 5H6.7a4 4 0 0 0-3.9 3.2l-1.7 8a3 3 0 0 0 5.3 2.4L8 17h8l1.6 1.6a3 3 0 0 0 5.3-2.4l-1.7-8A4 4 0 0 0 17.3 5z",
    "activity": "M22 12h-4l-3 9L9 3l-3 9H2",
    "bookOpen": "M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z",
    "zap": "M13 2 3 14h9l-1 8 10-12h-9l1-8z",
    "trendingUp": "M22 7 13.5 15.5 8.5 10.5 2 17 M16 7h6v6",
    "box": "M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z M3.3 7 12 12l8.7-5 M12 22V12",
    "banknote": "M2 6h20v12H2z M6 12h.01 M18 12h.01 M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z",
    "building2": "M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2 M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2 M10 6h4 M10 10h4 M10 14h4 M10 18h4",
    "creditCard": "M3 5h18a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z M1 10h22",
    "home": "M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z M9 22V12h6v10",
    "barChart": "M18 20V10 M12 20V4 M6 20v-6",
    "plus": "M12 5v14 M5 12h14",
    "x": "M18 6 6 18 M6 6l12 12",
    "chevronLeft": "M15 18l-6-6 6-6",
    "chevronRight": "M9 18l6-6-6-6",
    "chevronDown": "M6 9l6 6 6-6",
    "arrowUpRight": "M7 17L17 7 M7 7h10v10",
    "arrowDownLeft": "M17 7L7 17 M17 17H7V7",
    "repeat": "M17 1l4 4-4 4 M3 11V9a4 4 0 0 1 4-4h14 M7 23l-4-4 4-4 M21 13v2a4 4 0 0 1-4 4H3",
    "shield": "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
    "sparkles": "m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3z",
    "trash2": "M3 6h18 M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6 M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2 M10 11v6 M14 11v6",
    "info": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z M12 16v-4 M12 8h.01",
    "trendUp": "M22 7 13.5 15.5 8.5 10.5 2 17 M16 7h6v6",
    "dot": "M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
    "mail": "M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z M22 6l-10 7L2 6",
    "lock": "M5 11h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2z M7 11V7a5 5 0 0 1 10 0v4",
    "eyeOff": "M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94 M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19 M1 1l22 22",
    "check": "M20 6 9 17l-5-5",
    "arrowRight": "M5 12h14 M12 5l7 7-7 7",
    "user": "M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2 M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
    "googleG": "M19.8 12H12.5 M17.66 6.34A8 8 0 1 0 19.8 13.5",
    "search": "M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z M21 21l-4.35-4.35",
    "download": "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4 M7 10l5 5 5-5 M12 15V3",
    "camera": "M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z M12 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6z",
    "image": "M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z M8.5 10a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z M21 15l-5-5L5 21",
    "folder": "M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z",
    "edit": "M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z",
}

ICON_BBOX = {
    "logout": (3.0, 3.0, 18.0, 18.0),
    "wallet": (3.0, 3.0, 18.0, 18.0),
    "utensils": (3.0, 2.0, 18.0, 20.0),
    "car": (2.0, 7.0, 20.0, 12.0),
    "shoppingBag": (3.0, 2.0, 18.0, 20.0),
    "gamepad2": (1.0, 5.0, 22.0, 14.0),
    "activity": (2.0, 3.0, 20.0, 18.0),
    "bookOpen": (2.0, 3.0, 20.0, 18.0),
    "zap": (3.0, 2.0, 18.0, 20.0),
    "trendingUp": (2.0, 7.0, 20.0, 10.0),
    "box": (3.0, 2.0, 18.0, 20.0),
    "banknote": (2.0, 6.0, 20.0, 12.0),
    "building2": (2.0, 2.0, 20.0, 20.0),
    "creditCard": (1.0, 5.0, 22.0, 14.0),
    "home": (3.0, 2.0, 18.0, 20.0),
    "barChart": (6.0, 4.0, 12.0, 16.0),
    "plus": (5.0, 5.0, 14.0, 14.0),
    "x": (6.0, 6.0, 12.0, 12.0),
    "chevronLeft": (9.0, 6.0, 6.0, 12.0),
    "chevronRight": (9.0, 6.0, 6.0, 12.0),
    "chevronDown": (6.0, 9.0, 12.0, 6.0),
    "arrowUpRight": (7.0, 7.0, 10.0, 10.0),
    "arrowDownLeft": (7.0, 7.0, 10.0, 10.0),
    "repeat": (3.0, 1.0, 18.0, 22.0),
    "shield": (4.0, 2.0, 16.0, 20.0),
    "sparkles": (3.0, 3.0, 18.0, 18.0),
    "trash2": (3.0, 2.0, 16.0, 20.0),
    "info": (2.0, 2.0, 20.0, 20.0),
    "trendUp": (2.0, 7.0, 20.0, 10.0),
    "dot": (10.0, 10.0, 4.0, 4.0),
    "mail": (2.0, 4.0, 20.0, 16.0),
    "lock": (3.0, 2.0, 18.0, 20.0),
    "eyeOff": (1.0, 1.0, 22.0, 22.0),
    "check": (4.0, 6.0, 16.0, 11.0),
    "arrowRight": (5.0, 5.0, 14.0, 14.0),
    "user": (5.0, 3.0, 14.0, 18.0),
    "googleG": (4.0, 4.0, 15.8, 16.0),
    "search": (3.0, 3.0, 18.0, 18.0),
    "download": (3.0, 3.0, 18.0, 18.0),
    "camera": (2.0, 4.0, 20.0, 16.0),
    "image": (3.0, 3.0, 18.0, 18.0),
    "folder": (2.0, 3.0, 20.0, 18.0),
    "edit": (2.0, 2.0, 20.0, 20.0),
}

_ICON_SEQ = 0


def icon_cmds(parent, name: str, key: str, x: float, y: float, size: float = 16.0, color: str = "#1E1E2D", weight: float = 1.8, as_ref: str = None):
    """Build a 2-step batch command pair (`node.create` + `node.set`) for placing a crisp scaled vector icon."""
    global _ICON_SEQ
    _ICON_SEQ += 1
    ref = as_ref or f"_ico_{_ICON_SEQ}"
    if key not in ICONS:
        raise ValueError(f"Unknown icon '{key}'. Available icons: {sorted(ICONS.keys())}")
    s = size / 24.0
    minx, miny, w, h = ICON_BBOX.get(key, (2.0, 2.0, 20.0, 20.0))
    return [
        {
            "command": "node.create",
            "as": ref,
            "params": {
                "type": "vector",
                "parent": parent,
                "name": name,
                "path": ICONS[key],
                "x": 0,
                "y": 0,
                "props": {
                    "stroke": color,
                    "strokeWeight": weight,
                    "fill": "none",
                },
            },
        },
        {
            "command": "node.set",
            "params": {
                "ids": [{"$ref": ref}],
                "x": x + minx * s,
                "y": y + miny * s,
                "width": w * s,
                "height": h * s,
                "strokeWeight": weight,
            },
        },
    ]

