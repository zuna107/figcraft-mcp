# Windows PowerShell One-Line Installer for FigCraft-MCP
$ErrorActionPreference = "Stop"
Write-Host "==> Installing MCP for FigCraft..." -ForegroundColor Cyan

$TargetDir = Join-Path $HOME ".figcraft-mcp"
if (Test-Path (Join-Path $PSScriptRoot "pyproject.toml")) {
    $TargetDir = $PSScriptRoot
} elseif (-not (Test-Path $TargetDir)) {
    git clone https://github.com/your-username/FigCraft-MCP.git $TargetDir
}

python -m pip install -e $TargetDir --quiet
python (Join-Path $TargetDir "src\figcraft_mcp\server.py") setup

