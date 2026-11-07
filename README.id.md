<div align="center">

<img src="./assets/banner.svg" alt="MCP for FigCraft Banner" width="820" />

<p>
  <a href="./README.md">English (README.md)</a> · <b>Bahasa Indonesia</b>
</p>

<p><i>Server Model Context Protocol (MCP) Universal, Python SDK, dan Mesin Desain <b>Anti-Slop UI</b> untuk <b>FigCraft Desktop</b>.</i></p>

<p><b>Disclaimer:</b> Proyek ini adalah integrasi komunitas untuk menghubungkan FigCraft Desktop dengan berbagai AI Agent / LLM.</p>

<p>Desain UI/UX berbasis prompt, streaming kursor multiplayer real-time, audit Anti-Slop UI, dan pembuatan prototype interaktif — digerakkan oleh AI.</p>

<p>
  <img src="https://img.shields.io/badge/version-1.0.0-6C5CE7?style=flat-square" alt="Version" />
  <img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/MCP-2024--11--05-00B894?style=flat-square" alt="MCP Protocol" />
  <img src="https://img.shields.io/badge/UI_Standard-Anti--Slop_UI-1E1E2D?style=flat-square" alt="Anti-Slop UI" />
  <img src="https://img.shields.io/badge/license-MIT-F59E0B?style=flat-square" alt="License MIT" />
</p>

</div>

---

## Instalasi Cepat (Quickstart)

> **Catatan:** `figcraft-mcp` otomatis terhubung ke jendela **FigCraft Desktop** Anda pada port TCP `7979`, mendeteksi ruang kolaborasi aktif (`doc.list` + `collab.peers`), menggerakkan kursor multiplayer AI secara bertahap (`~40ms` per elemen), dan menerapkan standar desain **Anti-Slop UI** pada model AI apa pun.

**Satu perintah** untuk mengatur aplikasi AI Anda (Google Antigravity, Claude Desktop, Claude Code, Cursor, Windsurf, VS Code) dan menghubungkannya ke FigCraft:

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/your-username/FigCraft-MCP/main/install.ps1 | iex
```

### macOS / Linux

```bash
curl -LsSf https://raw.githubusercontent.com/your-username/FigCraft-MCP/main/install.sh | sh
```

### Instalasi dari Repository Lokal (`pip` / `uvx`)

```powershell
git clone https://github.com/your-username/FigCraft-MCP.git
cd FigCraft-MCP
pip install -e .
figcraft-mcp setup
```

Setelah selesai, **tutup dan buka kembali aplikasi AI / IDE Anda**, buka **FigCraft Desktop**, lalu minta AI untuk membuat atau mengedit desain UI.

---

## Tampilan & Screenshot Hasil

### 1. Kursor Multiplayer Real-Time & Live Streaming Bertahap
Setiap elemen (`frame`, `rectangle`, `text`, `vector icon`) dibuat secara bertahap dan cepat (`40ms/elemen`) disertai pergerakan kursor multiplayer (`Antigravity AI`) dan *highlight* seleksi langsung di layar FigCraft:

<p align="center">
  <img src="./assets/screenshots/05-live-cursor-streaming.jpg" alt="Live Cursor Streaming di FigCraft" width="380" />
  <img src="./assets/screenshots/07-live-session-join.jpg" alt="Sesi Kolaborasi Langsung di FigCraft" width="500" />
</p>

### 2. Output Desain Bersih & Bebas AI Slop (`anti-slop-ui`)
Dilengkapi aturan **`anti-slop-ui`** bawaan agar AI tidak menghasilkan badge berlebihan (`"Hasil Scan Struk AI"`, `"AI Matched"`), warna input mencolok, atau emoji Unicode:

<p align="center">
  <img src="./assets/screenshots/01-auth-screens.png" alt="Screen 0B & Screen 0 - Auth" width="440" />
  <img src="./assets/screenshots/02-dashboard-popups.jpg" alt="Screen 1, 2, 2B - Dashboard & Popup" width="440" />
</p>

<p align="center">
  <img src="./assets/screenshots/03-review-searchable-dropdown.jpg" alt="Screen 3, 4, 4B - Review & Searchable Dropdown" width="440" />
  <img src="./assets/screenshots/04-reports-and-wallets.jpg" alt="Screen 5, 5B, 6, 6B - Report & Wallets" width="440" />
</p>

### 3. Alur Prototype Interaktif
Menghubungkan tombol, tab switcher, popup bottom sheet, dan navigasi antar-frame secara otomatis dengan transisi `smartAnimate`, `dissolve`, `push`, `slideIn`, dan `moveOut`:

<p align="center">
  <img src="./assets/screenshots/06-prototype-mode.png" alt="Mode Prototype Interaktif di FigCraft" width="760" />
</p>

---

## Lisensi

Dirilis di bawah lisensi [MIT License](./LICENSE).

