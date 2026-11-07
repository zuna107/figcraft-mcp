"""
FigCraft-MCP: Universal Live-Streaming MCP Server & Anti-Slop UI Design Engine for FigCraft Desktop.
"""

__version__ = "1.0.0"

from .config import (
    resolve_cli_path,
    resolve_app_path,
    is_port_open,
    ensure_desktop_running,
    PORT,
    HOST,
)
from .icons import ICONS, ICON_BBOX, icon_cmds
from .tokens import ANTI_SLOP_TOKENS, BANNED_PATTERNS, COMPONENT_RECIPES
from .client import FigCraftLive

__all__ = [
    "__version__",
    "resolve_cli_path",
    "resolve_app_path",
    "is_port_open",
    "ensure_desktop_running",
    "PORT",
    "HOST",
    "ICONS",
    "ICON_BBOX",
    "icon_cmds",
    "ANTI_SLOP_TOKENS",
    "BANNED_PATTERNS",
    "COMPONENT_RECIPES",
    "FigCraftLive",
]

