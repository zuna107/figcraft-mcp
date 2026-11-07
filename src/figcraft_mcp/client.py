#!/usr/bin/env python3
"""
FigCraftLive Python SDK Client for script-based high-speed step-by-step UI generation.
"""

import json
import os
import subprocess
import sys
import time

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from figcraft_mcp.config import DEFAULT_DOC, PORT, ensure_desktop_running, resolve_cli_path
else:
    from .config import DEFAULT_DOC, PORT, ensure_desktop_running, resolve_cli_path


class FigCraftLive:
    def __init__(self, step_delay: float = 0.040, auto_cursor: bool = True, doc_path: str = DEFAULT_DOC):
        self.step_delay = step_delay
        self.auto_cursor = auto_cursor
        self.doc_path = doc_path
        self._node_pos = {}

        attached = ensure_desktop_running(doc_path, PORT)
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
        self.req_id = 1
        self.doc_id = None
        self._call(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "figcraft-mcp-sdk", "version": "1.0.0"},
            },
        )
        self.lock_document(doc_path)

    def _call(self, method: str, params: dict):
        cid = self.req_id
        self.req_id += 1
        msg = {"jsonrpc": "2.0", "id": cid, "method": method, "params": params}
        self.proc.stdin.write(json.dumps(msg, separators=(",", ":")) + "\n")
        self.proc.stdin.flush()
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise ConnectionError("FigCraft CLI stream closed")
            try:
                res = json.loads(line)
                if res.get("id") == cid:
                    if "error" in res:
                        raise RuntimeError(res["error"].get("message", "MCP error"))
                    return res.get("result", {})
            except json.JSONDecodeError:
                continue

    def _raw_tool(self, name: str, args: dict):
        res = self._call("tools/call", {"name": name, "arguments": args})
        content = res.get("content", [])
        if res.get("isError"):
            raise RuntimeError(content[0].get("text") if content else "Tool error")
        txt = content[0].get("text") if content else None
        try:
            return json.loads(txt)
        except Exception:
            return txt

    def lock_document(self, path: str = ""):
        docs = self._raw_tool("run_command", {"command": "doc.list"})
        if not isinstance(docs, list) or not docs:
            return None
        active_first = sorted(docs, key=lambda d: 0 if d.get("active") else 1)
        for d in active_first:
            try:
                peers = self._raw_tool("run_command", {"command": "collab.peers", "document": d["id"]})
                if isinstance(peers, dict) and peers.get("status") == "live":
                    self.doc_id = d["id"]
                    return self.doc_id
            except Exception:
                pass
        for d in active_first:
            if (path and (d.get("path") or "").lower() == path.lower()) or d.get("active"):
                self.doc_id = d["id"]
                return self.doc_id
        self.doc_id = docs[0]["id"]
        return self.doc_id

    def tool(self, name: str, args: dict):
        if self.doc_id is not None and "document" not in args:
            if name not in ("open_file", "pointer", "key", "type_text", "inspect_ui", "list_commands"):
                args = {**args, "document": self.doc_id}
        return self._raw_tool(name, args)

    def register_frame_origin(self, node_id: int, x: float, y: float):
        self._node_pos[node_id] = (float(x), float(y))

    def _calc_abs_pos(self, parent_id, x, y, w=20, h=20):
        px, py = self._node_pos.get(parent_id, (0.0, 0.0))
        ax, ay = px + float(x or 0.0), py + float(y or 0.0)
        return ax, ay, ax + float(w or 20.0) * 0.5, ay + float(h or 20.0) * 0.5

    def _resolve_refs(self, obj, refs: dict):
        if isinstance(obj, dict):
            if "$ref" in obj and len(obj) == 1:
                return refs[obj["$ref"]]
            return {k: self._resolve_refs(v, refs) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._resolve_refs(v, refs) for v in obj]
        return obj

    def batch(self, commands: list, label: str = "Live Update", on_error: str = "abort", stream: bool = True):
        if not stream or len(commands) <= 2:
            return self.tool("batch", {"commands": commands, "label": label, "onError": on_error})

        refs, results = {}, []
        i, n = 0, len(commands)
        while i < n:
            cmd = self._resolve_refs(commands[i], refs)
            c_name = cmd.get("command")
            params = cmd.get("params", {})
            as_key = cmd.get("as")
            is_vec = (
                c_name == "node.create"
                and params.get("type") == "vector"
                and as_key
                and i + 1 < n
                and commands[i + 1].get("command") == "node.set"
            )
            micro = []
            if c_name in ("node.create", "node.set"):
                _, _, cx, cy = self._calc_abs_pos(
                    params.get("parent"), params.get("x", 0.0), params.get("y", 0.0), params.get("width", 40.0), params.get("height", 20.0)
                )
                if self.auto_cursor and (cx != 0.0 or cy != 0.0):
                    micro.append({"command": "collab.cursor", "params": {"x": cx, "y": cy}})
                if c_name == "node.create":
                    params["select"] = True

            if is_vec:
                micro.extend([cmd, commands[i + 1]])
                step_res = self.tool("batch", {"commands": micro, "label": params.get("name", "Icon"), "onError": on_error})
                created = step_res[-2]
                refs[as_key] = created["id"] if isinstance(created, dict) else created
                results.extend(step_res[-2:])
                i += 2
            else:
                micro.append(cmd)
                step_res = self.tool("batch", {"commands": micro, "label": params.get("name", c_name), "onError": on_error})
                main_res = step_res[-1]
                if c_name == "node.create":
                    nid = main_res["id"] if isinstance(main_res, dict) else main_res
                    ax, ay, _, _ = self._calc_abs_pos(params.get("parent"), params.get("x", 0.0), params.get("y", 0.0))
                    self._node_pos[nid] = (ax, ay)
                    if as_key:
                        refs[as_key] = nid
                results.append(main_res)
                i += 1
            if self.step_delay > 0:
                time.sleep(self.step_delay)
        return results

    def cursor(self, x: float, y: float, chat: str = None):
        cmds = [{"command": "collab.cursor", "params": {"x": float(x), "y": float(y)}}]
        if chat:
            cmds.append({"command": "collab.cursorChat", "params": {"text": str(chat)}})
        return self.tool("batch", {"commands": cmds, "label": "Cursor"})

    def save(self, doc_path: str = None):
        target = doc_path or self.doc_path
        return self.tool("save_file", {"path": target} if target else {})

    def close(self):
        try:
            self.proc.terminate()
        except Exception:
            pass
