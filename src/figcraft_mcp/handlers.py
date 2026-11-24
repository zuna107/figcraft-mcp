#!/usr/bin/env python3
"""
Modular high-level tool handlers for FigCraft-MCP.
Keeps server.py clean, robust, and well under 250 lines.
"""

import json
import time
from .icons import icon_cmds
from .tokens import (
    ANTI_SLOP_TOKENS,
    BANNED_PATTERNS,
    COMPONENT_RECIPES,
    FEW_SHOT_GUIDANCE,
    STYLE_PRESETS,
    UNIVERSAL_HEURISTICS,
)


def rgba_to_hex(color_dict: dict) -> str:
    """Convert a FigCraft RGBA color dict (0.0-1.0) into a hex or rgba string."""
    if not isinstance(color_dict, dict):
        return str(color_dict)
    r = int(round(color_dict.get("r", 0.0) * 255))
    g = int(round(color_dict.get("g", 0.0) * 255))
    b = int(round(color_dict.get("b", 0.0) * 255))
    a = color_dict.get("a", 1.0)
    if a < 0.999:
        return f"rgba({r}, {g}, {b}, {round(a, 2)})"
    return f"#{r:02X}{g:02X}{b:02X}"


def handle_list_screens(server, targs: dict) -> dict:
    """Fast overview of top-level frames using outline=True for 90%+ token savings."""
    page_id = targs.get("page", 1)
    r = server._call_backend_tool("get_node", {"id": page_id, "depth": 1, "outline": True})
    txt = r.get("content", [{}])[0].get("text", "{}")
    screens = []
    try:
        node = json.loads(txt)
        children = node.get("children", [])
        for c in children:
            screens.append({
                "id": c.get("id"),
                "name": c.get("name"),
                "type": c.get("type"),
                "x": c.get("x", 0.0),
                "y": c.get("y", 0.0),
                "width": c.get("width", 0.0),
                "height": c.get("height", 0.0),
            })
    except Exception as exc:
        return {"content": [{"type": "text", "text": f"Error parsing page nodes: {exc}"}], "isError": True}
    return {"content": [{"type": "text", "text": json.dumps({"page": page_id, "count": len(screens), "screens": screens}, indent=2)}]}


def handle_find_nodes(server, targs: dict) -> dict:
    """Search for layers by query/type with depth 10 using outline=True for token economy."""
    parent_id = targs["parent"]
    query = str(targs["query"]).lower()
    type_filter = targs.get("type")
    r = server._call_backend_tool("get_node", {"id": parent_id, "depth": 10, "outline": True})
    txt = r.get("content", [{}])[0].get("text", "{}")
    matches = []
    try:
        root_node = json.loads(txt)

        def walk(curr):
            if not isinstance(curr, dict):
                return
            n = curr.get("name", "")
            chars = curr.get("characters", "")
            t = curr.get("type", "")
            matched = False
            if query in n.lower() or query in chars.lower():
                if not type_filter or t.lower() == type_filter.lower():
                    matched = True
            if matched and curr.get("id") != parent_id:
                item = {
                    "id": curr.get("id"),
                    "name": n,
                    "type": t,
                    "x": curr.get("x"),
                    "y": curr.get("y"),
                    "width": curr.get("width"),
                    "height": curr.get("height"),
                }
                if chars:
                    item["text"] = chars
                matches.append(item)
            for ch in curr.get("children", []):
                walk(ch)

        walk(root_node)
    except Exception as exc:
        return {"content": [{"type": "text", "text": f"Error searching nodes: {exc}"}], "isError": True}
    return {"content": [{"type": "text", "text": json.dumps({"parent": parent_id, "query": query, "count": len(matches), "matches": matches}, indent=2)}]}


def handle_get_anti_slop_guidelines(targs: dict) -> dict:
    """Retrieve quality heuristics, anti-slop rules, and style tokens."""
    req_style = targs.get("style", "neutral_clean")
    tokens_payload = STYLE_PRESETS if req_style == "all" else STYLE_PRESETS.get(req_style, ANTI_SLOP_TOKENS)
    payload = {
        "heuristics": UNIVERSAL_HEURISTICS,
        "banned_patterns": BANNED_PATTERNS,
        "active_preset": req_style,
        "tokens": tokens_payload,
        "recipes": COMPONENT_RECIPES,
        "few_shot_guidance": FEW_SHOT_GUIDANCE.strip(),
    }
    return {"content": [{"type": "text", "text": json.dumps(payload, indent=2)}]}


def handle_place_lucide_icon(server, targs: dict) -> dict:
    """Place a vector icon with animated multiplayer cursor feedback."""
    cmds = icon_cmds(
        targs["parent"],
        targs["name"],
        targs["icon"],
        float(targs["x"]),
        float(targs["y"]),
        float(targs.get("size", 16)),
        targs.get("color", "#1E1E2D"),
        float(targs.get("strokeWeight", 1.8)),
    )
    return server._stream_batch({"commands": cmds, "label": f"Icon {targs['name']}"})


def handle_create_prototype_link(server, targs: dict) -> dict:
    """Create an interactive prototype navigation flow between screens."""
    transition = {"type": targs.get("transition", "smartAnimate")}
    if targs.get("direction"):
        transition["direction"] = targs["direction"]
    try:
        server._call_backend_tool("run_command", {"command": "proto.interaction.clear", "params": {"ids": [targs["sourceId"]]}})
    except Exception:
        pass
    return server._call_backend_tool(
        "run_command",
        {
            "command": "proto.interaction.add",
            "params": {
                "id": targs["sourceId"],
                "trigger": {"type": "onClick"},
                "action": {"type": "navigate", "dest": targs["targetFrameId"]},
                "transition": transition,
                "durationMs": int(targs.get("durationMs", 240)),
                "easing": "easeOut",
            },
        },
    )


def handle_create_from_template(server, targs: dict) -> dict:
    """Instantiate an official FigCraft starter template (instant layout, 0 AI-slop)."""
    template_id = targs["template"]
    name = targs.get("name") or template_id.replace("-", " ").title()
    res = server._call_backend_tool("run_command", {"command": "file.newFromTemplate", "params": {"template": template_id, "name": name}})
    server._detect_live_doc()
    return res


def handle_inspect_code(server, targs: dict) -> dict:
    """Natively compile a frame/node into Tailwind CSS, Compose, SwiftUI, React, or Flutter."""
    params = {"language": targs.get("language", "tailwind")}
    if "nodeId" in targs:
        params["id"] = targs["nodeId"]
    return server._call_backend_tool("run_command", {"command": "inspect.code", "params": params})


def handle_extract_canvas_tokens(server, targs: dict) -> dict:
    """Extract design tokens, variables, and typography styles directly from the canvas."""
    res_vars = server._call_backend_tool("run_command", {"command": "variable.export"})
    res_fonts = server._call_backend_tool("run_command", {"command": "file.fontReport"})

    raw_var_text = res_vars.get("content", [{}])[0].get("text", "{}")
    raw_font_text = res_fonts.get("content", [{}])[0].get("text", "{}")

    tokens = {"colors": {}, "spacing": {}, "radii": {}, "fonts": []}
    try:
        var_data = json.loads(raw_var_text)
        if isinstance(var_data, dict) and "text" in var_data and isinstance(var_data["text"], str):
            var_data = json.loads(var_data["text"])
        meta = var_data.get("meta", {})
        colls = meta.get("variableCollections", {})
        variables = meta.get("variables", {})

        mode_map = {}
        for c in colls.values():
            for m in c.get("modes", []):
                mode_map[m.get("modeId")] = m.get("name", "Default")

        for v in variables.values():
            v_name = v.get("name", "")
            v_type = v.get("resolvedType", "")
            vals = v.get("valuesByMode", {})
            clean_vals = {mode_map.get(m_id, m_id): (rgba_to_hex(val) if v_type == "COLOR" else val) for m_id, val in vals.items()}
            val_out = clean_vals if len(clean_vals) > 1 else next(iter(clean_vals.values()), None)

            if v_type == "COLOR":
                tokens["colors"][v_name] = val_out
            elif any(k in v_name.lower() for k in ("space", "gap", "padding")):
                tokens["spacing"][v_name] = val_out
            elif any(k in v_name.lower() for k in ("radius", "round")):
                tokens["radii"][v_name] = val_out
    except Exception:
        pass

    try:
        font_data = json.loads(raw_font_text)
        for f in font_data.get("fonts", []):
            if f.get("family") and f["family"] not in tokens["fonts"]:
                tokens["fonts"].append(f["family"])
    except Exception:
        pass

    return {"content": [{"type": "text", "text": json.dumps(tokens, indent=2)}]}


def handle_join_live_session(server, targs: dict) -> dict:
    """Join a FigCraft Live Session, poll until live sync completes, and lock live_doc_id."""
    user_name = targs.get("userName", "Antigravity AI")
    server._call_backend_tool("run_command", {"command": "pref.userName", "params": {"name": user_name}})
    server.live_doc_id = None
    server.node_origins.clear()

    join_params = {}
    if "link" in targs:
        join_params["link"] = targs["link"]
    if "code" in targs:
        join_params["code"] = targs["code"]

    res = server._call_backend_tool("run_command", {"command": "collab.join", "params": join_params})
    if res.get("isError"):
        return res

    peers_info = {}
    for _ in range(24):
        time.sleep(0.25)
        try:
            p_res = server._call_backend_tool("run_command", {"command": "collab.peers"})
            peers_info = json.loads(p_res.get("content", [{}])[0].get("text", "{}"))
            if isinstance(peers_info, dict) and peers_info.get("status") == "live":
                break
        except Exception:
            continue

    server._detect_live_doc(force_refresh=True)
    summary = {
        "status": peers_info.get("status", "unknown"),
        "document": server.live_doc_id,
        "fileName": peers_info.get("fileName"),
        "role": peers_info.get("role"),
        "pages": peers_info.get("pages", []),
    }
    return {"content": [{"type": "text", "text": json.dumps(summary, indent=2)}]}
