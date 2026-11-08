#!/usr/bin/env python3
"""
Universal FigCraft MCP Server with Built-in Live Step-by-Step Cursor Streaming
and Anti-Slop UI Design Tools (`place_lucide_icon`, `create_prototype_link`, `get_anti_slop_guidelines`).
"""

import json
import os
import subprocess
import sys
import time

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from figcraft_mcp.config import (
        DEFAULT_DOC,
        HOST,
        PORT,
        STREAM_DELAY_MS,
        STREAM_STEPS,
        ensure_desktop_running,
        is_port_open,
        resolve_cli_path,
    )
    from figcraft_mcp.icons import ICONS, icon_cmds
    from figcraft_mcp.tokens import ANTI_SLOP_TOKENS, BANNED_PATTERNS, COMPONENT_RECIPES
else:
    from .config import (
        DEFAULT_DOC,
        HOST,
        PORT,
        STREAM_DELAY_MS,
        STREAM_STEPS,
        ensure_desktop_running,
        is_port_open,
        resolve_cli_path,
    )
    from .icons import ICONS, icon_cmds
    from .tokens import ANTI_SLOP_TOKENS, BANNED_PATTERNS, COMPONENT_RECIPES

EXTRA_TOOLS = [
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
        "description": "Retrieve the Anti-Slop UI Design Tokens, neutral color palette, typography scale, banned AI clichés, and component recipes before creating or auditing screens.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


class FigCraftMCPServer:
    def __init__(self):
        # Never spawn GUI window on IDE startup; only attach if port is already listening
        attached = is_port_open(HOST, PORT)
        cli_args = [resolve_cli_path(), "mcp"]
        if attached:
            cli_args.extend(["--attach", str(PORT)])

        self.proc = subprocess.Popen(
            cli_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        self._internal_seq = 900000
        self.live_doc_id = None
        self.node_origins = {}
        self.peer_proc = None
        self.peer_seq = 1000

    def _rpc_backend(self, method: str, params: dict):
        self._internal_seq += 1
        req_id = self._internal_seq
        msg = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}
        self.proc.stdin.write(json.dumps(msg, separators=(",", ":")) + "\n")
        self.proc.stdin.flush()
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise EOFError("Backend figcraft-cli closed")
            res = json.loads(line)
            if res.get("id") == req_id:
                return res

    def _call_backend_tool(self, name: str, arguments: dict):
        if self.live_doc_id is not None and "document" not in arguments:
            if name not in ("open_file", "pointer", "key", "type_text", "inspect_ui", "list_commands"):
                cmd_name = arguments.get("command") if name == "run_command" else None
                if cmd_name not in ("collab.peers", "doc.list", "pref.userName", "collab.share"):
                    arguments = {**arguments, "document": self.live_doc_id}
        res = self._rpc_backend("tools/call", {"name": name, "arguments": arguments})
        return res.get("result", {"content": [{"type": "text", "text": json.dumps(res.get("error", {}))} ], "isError": True})

    def _ensure_peer_joined(self, peers_info: dict):
        """Ensure a headless collaborator peer 'Antigravity AI' is joined to the live session."""
        if self.peer_proc and self.peer_proc.poll() is None:
            return
        link = peers_info.get("url") or peers_info.get("link")
        if not link:
            return
        try:
            self.peer_proc = subprocess.Popen(
                [resolve_cli_path(), "mcp"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=sys.stderr,
                text=True,
                encoding="utf-8",
                bufsize=1,
            )
            # Initialize & join
            self._send_peer("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "antigravity-ai-peer", "version": "1.0"}})
            self._send_peer("tools/call", {"name": "run_command", "arguments": {"command": "pref.userName", "params": {"name": "Antigravity AI"}}})
            self._send_peer("tools/call", {"name": "run_command", "arguments": {"command": "collab.join", "params": {"link": link}}})
        except Exception as exc:
            sys.stderr.write(f"[figcraft-mcp] Could not spawn live peer: {exc}\n")

    def _send_peer(self, method: str, params: dict):
        if not self.peer_proc or self.peer_proc.poll() is not None:
            return None
        self.peer_seq += 1
        req_id = self.peer_seq
        msg = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}
        self.peer_proc.stdin.write(json.dumps(msg, separators=(",", ":")) + "\n")
        self.peer_proc.stdin.flush()
        while True:
            line = self.peer_proc.stdout.readline()
            if not line:
                return None
            try:
                res = json.loads(line)
                if res.get("id") == req_id:
                    return res
            except Exception:
                continue

    def _peer_cursor(self, x: float, y: float):
        if self.peer_proc and self.peer_proc.poll() is None:
            try:
                self._send_peer("tools/call", {"name": "run_command", "arguments": {"command": "collab.cursor", "params": {"x": x, "y": y}}})
            except Exception:
                pass

    def _detect_live_doc(self):
        try:
            res = self._call_backend_tool("run_command", {"command": "doc.list"})
            txt = res.get("content", [{}])[0].get("text", "[]")
            docs = json.loads(txt)
            if not isinstance(docs, list) or not docs:
                return
            p_res = self._call_backend_tool("run_command", {"command": "collab.peers"})
            peers = json.loads(p_res.get("content", [{}])[0].get("text", "{}"))
            if isinstance(peers, dict) and peers.get("status") == "live":
                for d in docs:
                    if d.get("active"):
                        self.live_doc_id = d["id"]
                        self._ensure_peer_joined(peers)
                        return
                self.live_doc_id = docs[0]["id"]
                self._ensure_peer_joined(peers)
                return
            self.live_doc_id = docs[0]["id"]
        except Exception:
            pass

    def _resolve_refs(self, obj, refs: dict):
        if isinstance(obj, dict):
            if "$ref" in obj and len(obj) == 1:
                return refs.get(obj["$ref"], obj)
            return {k: self._resolve_refs(v, refs) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._resolve_refs(v, refs) for v in obj]
        return obj

    def _stream_batch(self, args: dict):
        commands = args.get("commands", [])
        if not STREAM_STEPS or len(commands) <= 2 or args.get("stream") is False:
            return self._call_backend_tool("batch", args)

        refs = {}
        results = []
        i, n = 0, len(commands)
        delay = STREAM_DELAY_MS / 1000.0
        while i < n:
            cmd = self._resolve_refs(commands[i], refs)
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
                px, py = self.node_origins.get(pid, (0.0, 0.0))
                cx = px + float(params.get("x", 0.0)) + float(params.get("width", 30.0)) * 0.5
                cy = py + float(params.get("y", 0.0)) + float(params.get("height", 20.0)) * 0.5
                if cx != 0.0 or cy != 0.0:
                    micro.append({"command": "collab.cursor", "params": {"x": cx, "y": cy}})
                    self._peer_cursor(cx, cy)
                if c_name == "node.create":
                    params["select"] = True

            if is_vec_pair:
                micro.extend([cmd, commands[i + 1]])
                r = self._call_backend_tool("batch", {"commands": micro, "label": params.get("name", "Icon")})
                step_list = json.loads(r.get("content", [{}])[0].get("text", "[]"))
                if isinstance(step_list, list) and len(step_list) >= 2:
                    c_obj = step_list[-2]
                    refs[as_key] = c_obj["id"] if isinstance(c_obj, dict) else c_obj
                    results.extend(step_list[-2:])
                i += 2
            else:
                micro.append(cmd)
                r = self._call_backend_tool("batch", {"commands": micro, "label": params.get("name", c_name)})
                step_list = json.loads(r.get("content", [{}])[0].get("text", "[]"))
                if isinstance(step_list, list) and step_list:
                    main_res = step_list[-1]
                    if c_name == "node.create":
                        nid = main_res["id"] if isinstance(main_res, dict) else main_res
                        px, py = self.node_origins.get(params.get("parent"), (0.0, 0.0))
                        self.node_origins[nid] = (px + float(params.get("x", 0.0)), py + float(params.get("y", 0.0)))
                        if as_key:
                            refs[as_key] = nid
                    results.append(main_res)
                i += 1
            if delay > 0:
                time.sleep(delay)
        try:
            self._call_backend_tool("run_command", {"command": "collab.cursorChat", "params": {"text": ""}})
            self._call_backend_tool("select", {"ids": []})
        except Exception:
            pass
        return {"content": [{"type": "text", "text": json.dumps(results)}]}

    def handle_request(self, req: dict):
        method = req.get("method")
        req_id = req.get("id")
        params = req.get("params", {})

        if method == "initialize":
            res = self._rpc_backend(method, params)
            res["id"] = req_id
            return res

        if method == "tools/list":
            res = self._rpc_backend(method, params)
            tools = res.get("result", {}).get("tools", [])
            res["result"]["tools"] = tools + EXTRA_TOOLS
            res["id"] = req_id
            return res

        if method == "tools/call":
            tname = params.get("name")
            targs = params.get("arguments", {})
            if self.live_doc_id is None:
                self._detect_live_doc()

            if tname == "get_anti_slop_guidelines":
                payload = {"tokens": ANTI_SLOP_TOKENS, "banned_patterns": BANNED_PATTERNS, "recipes": COMPONENT_RECIPES}
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(payload, indent=2)}]}}

            if tname == "place_lucide_icon":
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
                return {"jsonrpc": "2.0", "id": req_id, "result": self._stream_batch({"commands": cmds, "label": f"Icon {targs['name']}"})}

            if tname == "create_prototype_link":
                transition = {"type": targs.get("transition", "smartAnimate")}
                if targs.get("direction"):
                    transition["direction"] = targs["direction"]
                try:
                    self._call_backend_tool("run_command", {"command": "proto.interaction.clear", "params": {"ids": [targs["sourceId"]]}})
                except Exception:
                    pass
                res = self._call_backend_tool(
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
                return {"jsonrpc": "2.0", "id": req_id, "result": res}

            if tname == "batch":
                return {"jsonrpc": "2.0", "id": req_id, "result": self._stream_batch(targs)}

            if tname == "create_node" and targs.get("type") == "text":
                if targs.get("width") == 100:
                    targs.pop("width", None)
                if targs.get("height") == 100:
                    targs.pop("height", None)

            if tname == "run_command" and targs.get("command") == "collab.join":
                self._call_backend_tool("run_command", {"command": "pref.userName", "params": {"name": "Antigravity AI"}})
                res = self._call_backend_tool(tname, targs)
                time.sleep(0.8)
                self._detect_live_doc()
                return {"jsonrpc": "2.0", "id": req_id, "result": res}

            return {"jsonrpc": "2.0", "id": req_id, "result": self._call_backend_tool(tname, targs)}

        # Notifications or other methods
        if req_id is None:
            self.proc.stdin.write(json.dumps(req, separators=(",", ":")) + "\n")
            self.proc.stdin.flush()
            return None
        res = self._rpc_backend(method, params)
        res["id"] = req_id
        return res

    def serve_forever(self):
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                resp = self.handle_request(req)
                if resp is not None:
                    sys.stdout.write(json.dumps(resp, separators=(",", ":")) + "\n")
                    sys.stdout.flush()
            except Exception as exc:
                sys.stderr.write(f"[figcraft-mcp] Error handling request: {exc}\n")
                sys.stderr.flush()


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("setup", "--setup", "install"):
        if __package__ in (None, ""):
            from figcraft_mcp.setup_cli import run_setup
        else:
            from .setup_cli import run_setup
        sys.exit(run_setup())
    server = FigCraftMCPServer()
    server.serve_forever()


if __name__ == "__main__":
    main()
