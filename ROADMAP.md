# Roadmap

Planned enhancements for upcoming releases of **FigCraft-MCP**:

- [x] **v1.0.0**:
  - Real-time step-by-step multiplayer cursor streaming (`40ms/element`)
  - Auto-discovery of active live collaboration sessions (`doc.list` + `collab.peers`)
  - 39 precomputed 24x24 Lucide vector icons (`place_lucide_icon`)
  - Built-in Anti-Slop UI design tokens & audit guidelines (`get_anti_slop_guidelines`)
  - Interactive prototype flow wiring (`create_prototype_link`)
  - One-command client setup (`figcraft-mcp setup`, `install.ps1`, `install.sh`)
- [x] **v1.1.0**:
  - Token-saving canvas inspection (`list_screens`, 98% token reduction)
  - Targeted node query tool for editing/modifications (`find_nodes`, 90% token reduction)
  - Compact batch response summarization
  - Multi-style presets (`neutral_clean`, `ios_hig`, `material_m3`, `dark_modern`) in `get_anti_slop_guidelines`
  - Few-shot canvas style learning workflow
- [ ] **v1.2.0**:
  - Expanded Lucide vector icon pack (100+ icons)
  - Automated accessibility contrast audit tool (`audit_screen_contrast`)
- [ ] **v1.3.0**:
  - Direct Jetpack Compose (Material 3) & Tailwind CSS code exporter from selected FigCraft frames

