#!/usr/bin/env python3
"""
Batch streaming & token-optimized response formatting for FigCraft-MCP.
"""

import json
import time
from .config import STREAM_DELAY_MS, STREAM_STEPS


def resolve_refs(obj, refs: dict):
    if isinstance(obj, dict):
        if "$ref" in obj and len(obj) == 1:
            return refs.get(obj["$ref"], obj)
        return {k: resolve_refs(v, refs) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve_refs(v, refs) for v in obj]
    return obj


def format_batch_result(raw_results, verbose: bool = False):
    if verbose:
        return {"content": [{"type": "text", "text": json.dumps(raw_results)}]}
    items = raw_results
    if isinstance(raw_results, str):
        try:
            items = json.loads(raw_results)
        except Exception:
            items = []
    created_ids = []
    if isinstance(items, list):
        for r in items:
            if isinstance(r, dict) and "id" in r:
                created_ids.append(r["id"])
            elif isinstance(r, int):
                created_ids.append(r)
    elif isinstance(items, dict):
        if "id" in items:
            created_ids.append(items["id"])
    summary = {
        "status": "success",
        "created_count": len(created_ids) if created_ids else (len(items) if isinstance(items, list) else 1),
        "root_id": created_ids[0] if created_ids else None,
        "created_ids": created_ids,
    }
    return {"content": [{"type": "text", "text": json.dumps(summary)}]}


def stream_batch_commands(server, args: dict):
    commands = args.get("commands", [])
    if not STREAM_STEPS or len(commands) <= 2 or args.get("stream") is False:
        raw_res = server._call_backend_tool("batch", args)
        if args.get("verbose") is True or raw_res.get("isError"):
            return raw_res
        txt = raw_res.get("content", [{}])[0].get("text", "[]")
        return format_batch_result(txt, verbose=False)

    refs = {}
    results = []
    i, n = 0, len(commands)
    delay = STREAM_DELAY_MS / 1000.0
    while i < n:
        cmd = resolve_refs(commands[i], refs)
        c_name = cmd.get("command")
        params = cmd.get("params", {})
        as_key = cmd.get("as")
        is_vec_pair = (
            c_name == "node.create"
            and params.get("type") == "vector"
            and as_key
            and i + 1 < n
            and commands[i + 1].get("command") == "node.set"
        )
        micro = []
        if c_name in ("node.create", "node.set"):
            if c_name == "node.create" and params.get("type") == "text":
                if params.get("width") == 100:
                    params.pop("width", None)
                if params.get("height") == 100:
                    params.pop("height", None)
            pid = params.get("parent")
            px, py = server.node_origins.get(pid, (0.0, 0.0))
            cx = px + float(params.get("x", 0.0)) + float(params.get("width", 30.0)) * 0.5
            cy = py + float(params.get("y", 0.0)) + float(params.get("height", 20.0)) * 0.5
            if cx != 0.0 or cy != 0.0:
                micro.append({"command": "collab.cursor", "params": {"x": cx, "y": cy}})
                server._peer_cursor(cx, cy)
            if c_name == "node.create":
                params["select"] = True

        if is_vec_pair:
            micro.extend([cmd, commands[i + 1]])
            r = server._call_backend_tool("batch", {"commands": micro, "label": params.get("name", "Icon")})
            step_list = json.loads(r.get("content", [{}])[0].get("text", "[]"))
            if isinstance(step_list, list) and len(step_list) >= 2:
                c_obj = step_list[-2]
                refs[as_key] = c_obj["id"] if isinstance(c_obj, dict) else c_obj
                results.extend(step_list[-2:])
            i += 2
        else:
            micro.append(cmd)
            r = server._call_backend_tool("batch", {"commands": micro, "label": params.get("name", c_name)})
            step_list = json.loads(r.get("content", [{}])[0].get("text", "[]"))
            if isinstance(step_list, list) and step_list:
                main_res = step_list[-1]
                if c_name == "node.create":
                    nid = main_res["id"] if isinstance(main_res, dict) else main_res
                    px, py = server.node_origins.get(params.get("parent"), (0.0, 0.0))
                    server.node_origins[nid] = (px + float(params.get("x", 0.0)), py + float(params.get("y", 0.0)))
                    if as_key:
                        refs[as_key] = nid
                results.append(main_res)
            i += 1
        if delay > 0:
            time.sleep(delay)
    try:
        server._call_backend_tool("run_command", {"command": "collab.cursorChat", "params": {"text": ""}})
        server._call_backend_tool("select", {"ids": []})
    except Exception:
        pass
    return format_batch_result(results, verbose=args.get("verbose", False))
