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
    from figcraft_mcp.tokens import (
        ANTI_SLOP_TOKENS,
        BANNED_PATTERNS,
        COMPONENT_RECIPES,
        FEW_SHOT_GUIDANCE,
        STYLE_PRESETS,
        UNIVERSAL_HEURISTICS,
    )
    from figcraft_mcp.batch_streamer import format_batch_result, stream_batch_commands
    from figcraft_mcp.tools_schema import EXTRA_TOOLS
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
    from .tokens import (
        ANTI_SLOP_TOKENS,
        BANNED_PATTERNS,
        COMPONENT_RECIPES,
        FEW_SHOT_GUIDANCE,
        STYLE_PRESETS,
        UNIVERSAL_HEURISTICS,
    )
    from .batch_streamer import format_batch_result, stream_batch_commands
    from .tools_schema import EXTRA_TOOLS


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

    def _format_batch_result(self, raw_results, verbose: bool = False):
        return format_batch_result(raw_results, verbose=verbose)

    def _stream_batch(self, args: dict):
        return stream_batch_commands(self, args)

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

            if tname == "list_screens":
                page_id = targs.get("page", 1)
                r = self._call_backend_tool("get_node", {"id": page_id, "depth": 1})
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
                    return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": f"Error parsing page nodes: {exc}"}], "isError": True}}
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"page": page_id, "count": len(screens), "screens": screens}, indent=2)}]}}

            if tname == "find_nodes":
                parent_id = targs["parent"]
                query = str(targs["query"]).lower()
                type_filter = targs.get("type")
                r = self._call_backend_tool("get_node", {"id": parent_id, "depth": 10})
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
                            if not type_filter or t == type_filter:
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
                    return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": f"Error searching nodes: {exc}"}], "isError": True}}
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"parent": parent_id, "query": query, "count": len(matches), "matches": matches}, indent=2)}]}}

            if tname == "get_anti_slop_guidelines":
                req_style = targs.get("style", "neutral_clean")
                if req_style == "all":
                    tokens_payload = STYLE_PRESETS
                else:
                    tokens_payload = STYLE_PRESETS.get(req_style, ANTI_SLOP_TOKENS)
                payload = {
                    "heuristics": UNIVERSAL_HEURISTICS,
                    "banned_patterns": BANNED_PATTERNS,
                    "active_preset": req_style,
                    "tokens": tokens_payload,
                    "recipes": COMPONENT_RECIPES,
                    "few_shot_guidance": FEW_SHOT_GUIDANCE.strip(),
                }
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
