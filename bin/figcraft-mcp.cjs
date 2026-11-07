#!/usr/bin/env node
/**
 * Zero-config Node.js / npx launcher for FigCraft-MCP.
 * Spawns the Python `figcraft_mcp.server` module with PYTHONPATH configured automatically.
 */
const { spawn } = require("child_process");
const path = require("path");

const srcDir = path.resolve(__dirname, "..", "src");
const pythonBin = process.env.PYTHON_BIN || (process.platform === "win32" ? "python" : "python3");

const env = {
  ...process.env,
  PYTHONPATH: process.env.PYTHONPATH
    ? `${srcDir}${path.delimiter}${process.env.PYTHONPATH}`
    : srcDir,
};

const child = spawn(pythonBin, ["-m", "figcraft_mcp.server", ...process.argv.slice(2)], {
  stdio: "inherit",
  env,
});

child.on("exit", (code) => {
  process.exit(code ?? 0);
});

