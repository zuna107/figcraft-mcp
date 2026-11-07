#!/usr/bin/env python3
"""
Cross-platform configuration & binary discovery for FigCraft Desktop and CLI.
Supports Windows, macOS, and Linux via environment variables, standard install paths, or PATH.
"""

import os
import shutil
import socket
import subprocess
import sys
import time

HOST = os.environ.get("FIGCRAFT_HOST", "127.0.0.1")
PORT = int(os.environ.get("FIGCRAFT_PORT", "7979"))
DEFAULT_DOC = os.environ.get("FIGCRAFT_DEFAULT_DOC", "")
STREAM_STEPS = os.environ.get("FIGCRAFT_STREAM_STEPS", "1") not in ("0", "false", "False")
STREAM_DELAY_MS = float(os.environ.get("FIGCRAFT_STREAM_DELAY_MS", "85"))


def resolve_cli_path() -> str:
    """Locate `figcraft-cli` across Windows, macOS, Linux, or custom env var."""
    env_cli = os.environ.get("FIGCRAFT_CLI_PATH")
    if env_cli and os.path.exists(env_cli):
        return env_cli

    which_cli = shutil.which("figcraft-cli")
    if which_cli:
        return which_cli

    candidates = [
        r"C:\Program Files\ArtCraft\FigCraft\figcraft-cli.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\FigCraft\figcraft-cli.exe"),
        "/Applications/FigCraft.app/Contents/MacOS/figcraft-cli",
        "/usr/local/bin/figcraft-cli",
        "/usr/bin/figcraft-cli",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return "figcraft-cli"


def resolve_app_path() -> str:
    """Locate `figcraft` desktop GUI across Windows, macOS, Linux, or custom env var."""
    env_app = os.environ.get("FIGCRAFT_APP_PATH")
    if env_app and os.path.exists(env_app):
        return env_app

    which_app = shutil.which("figcraft")
    if which_app:
        return which_app

    candidates = [
        r"C:\Program Files\ArtCraft\FigCraft\figcraft.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\FigCraft\figcraft.exe"),
        "/Applications/FigCraft.app/Contents/MacOS/figcraft",
        "/usr/local/bin/figcraft",
        "/usr/bin/figcraft",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return "figcraft"


def is_port_open(host: str = HOST, port: int = PORT, timeout: float = 0.12) -> bool:
    """Fast TCP probe to check if FigCraft Desktop control server is listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            return True
        except OSError:
            return False


def ensure_desktop_running(doc_path: str = DEFAULT_DOC, port: int = PORT) -> bool:
    """Ensure the visible FigCraft Desktop GUI is running with `--control <port>`."""
    if is_port_open(HOST, port):
        return True

    app_bin = resolve_app_path()
    if not os.path.exists(app_bin) and not shutil.which(app_bin):
        return False

    try:
        doc_arg = f' "{doc_path}"' if (doc_path and os.path.exists(doc_path)) else ""
        if sys.platform == "win32":
            ps_cmd = (
                "$s = New-Object -ComObject Shell.Application; "
                f"$s.ShellExecute('{app_bin}', '--control {port}{doc_arg}', '', 'open', 1)"
            )
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], timeout=4)
        else:
            args = [app_bin, "--control", str(port)]
            if doc_path and os.path.exists(doc_path):
                args.append(doc_path)
            subprocess.Popen(
                args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
    except Exception as exc:
        sys.stderr.write(f"[figcraft-mcp] Failed to launch FigCraft Desktop: {exc}\n")
        sys.stderr.flush()

    start = time.time()
    while time.time() - start < 5.0:
        if is_port_open(HOST, port):
            return True
        time.sleep(0.15)
    return is_port_open(HOST, port)

