# Contributing to FigCraft-MCP

Thank you for your interest in contributing to **FigCraft-MCP**! This document provides guidelines and instructions for contributing to the project.

---

## Ways to Contribute

- **Bug Reports**: Open an issue on [GitHub Issues](https://github.com/zuna107/figcraft-mcp/issues) describing the reproduction steps, operating system, FigCraft Desktop version, and AI client used.
- **New Lucide Vector Icons**: Add new 24x24 SVG path definitions and precomputed `(minx, miny, width, height)` bounding boxes in `src/figcraft_mcp/icons.py`.
- **Anti-Slop UI Component Recipes**: Propose clean, neutral UI component structures in `src/figcraft_mcp/tokens.py` and `skills/anti-slop-ui/SKILL.md`.
- **Client Setup Integrations**: Expand `src/figcraft_mcp/setup_cli.py` to support additional MCP clients and operating systems.

---

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/zuna107/figcraft-mcp.git
   cd figcraft-mcp
   ```
2. Install the package in editable mode:
   ```bash
   pip install -e .
   ```
3. Run the unit test suite:
   ```bash
   python -m unittest discover -s tests -p "test_*.py" -v
   ```

---

## Code & Design Standards

1. **Modularity**: Keep individual source files concise and modular (under 250-300 lines per file) with a clear separation of concerns.
2. **Zero External Runtime Dependencies**: The core MCP server (`src/figcraft_mcp/`) relies exclusively on the Python 3.10+ standard library so it can run anywhere without dependency conflicts.
3. **Anti-Slop UI Discipline**: All bundled prompts, skills, and tokens must enforce neutral surfaces (`#FFFFFF`, `#F8FAFC`, `#F1F5F9`), `1px` borders (`#E2E8F0`), and zero Unicode emojis.

---

## Pull Request Process

1. Create a feature branch (`git checkout -b feat/your-feature`).
2. Ensure all tests in `tests/test_server.py` pass (`python -m unittest discover -s tests`).
3. Open a Pull Request against the `main` branch with a clear summary of your changes.

