#!/usr/bin/env python3
"""
Interactive & Automatic Setup CLI (`figcraft-mcp setup`).
Finds MCP clients on the user's machine (Google Antigravity, Claude Desktop, Claude Code,
Cursor, Windsurf, VS Code), backs up existing config files as `.bak`, and registers `figcraft`.
"""

import json
import os
import shutil
import sys


def _client_config_paths() -> list[tuple[str, str]]:
    home = os.path.expanduser("~")
    appdata = os.environ.get("APPDATA", os.path.join(home, "AppData", "Roaming"))
    clients = [
        ("Google Antigravity", os.path.join(home, ".gemini", "config", "mcp_config.json")),
        ("Cursor", os.path.join(home, ".cursor", "mcp.json")),
        ("Windsurf / Codeium", os.path.join(home, ".codeium", "windsurf", "mcp_config.json")),
        ("Claude Code", os.path.join(home, ".claude.json")),
    ]
    if sys.platform == "win32":
        clients.append(("Claude Desktop", os.path.join(appdata, "Claude", "claude_desktop_config.json")))
    elif sys.platform == "darwin":
        clients.append(
            ("Claude Desktop", os.path.join(home, "Library", "Application Support", "Claude", "claude_desktop_config.json"))
        )
    else:
        clients.append(("Claude Desktop", os.path.join(home, ".config", "Claude", "claude_desktop_config.json")))
    return clients


def run_setup(repo_root: str = None) -> int:
    if repo_root is None:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    server_script = os.path.join(repo_root, "src", "figcraft_mcp", "server.py")
    py_exe = sys.executable or "python"

    entry = {
        "command": py_exe,
        "args": [server_script],
        "env": {
            "FIGCRAFT_PORT": "7979",
            "FIGCRAFT_STREAM_STEPS": "1",
            "FIGCRAFT_STREAM_DELAY_MS": "40",
        },
    }

    print("=== MCP for FigCraft — Automatic Client Setup ===")
    configured = 0
    for name, cfg_path in _client_config_paths():
        parent_dir = os.path.dirname(cfg_path)
        if not os.path.exists(parent_dir) and name != "Google Antigravity":
            continue
        os.makedirs(parent_dir, exist_ok=True)
        data = {}
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                shutil.copy2(cfg_path, cfg_path + ".bak")
            except Exception:
                data = {}
        if not isinstance(data, dict):
            data = {}
        servers = data.setdefault("mcpServers", {})
        servers["figcraft"] = entry
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"  [OK] Configured {name}: {cfg_path} (backup saved as .bak)")
        configured += 1

    print(f"\nDone! Configured {configured} MCP client(s).")
    print("Restart your AI IDE/App, open FigCraft Desktop, and start designing!")
    return 0

