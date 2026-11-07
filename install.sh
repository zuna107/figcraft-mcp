#!/usr/bin/env sh
# macOS / Linux One-Line Installer for FigCraft-MCP
set -e
echo "==> Installing MCP for FigCraft..."

TARGET_DIR="$HOME/.figcraft-mcp"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd || pwd)"

if [ -f "$SCRIPT_DIR/pyproject.toml" ]; then
  TARGET_DIR="$SCRIPT_DIR"
elif [ ! -d "$TARGET_DIR" ]; then
  git clone https://github.com/zuna107/figcraft-mcp.git "$TARGET_DIR"
fi

python3 -m pip install -e "$TARGET_DIR" --quiet
python3 "$TARGET_DIR/src/figcraft_mcp/server.py" setup
