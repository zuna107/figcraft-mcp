<div align="center">

<img src="./assets/banner.svg" alt="MCP for FigCraft Banner" width="820" />

<p>
  <b>English</b> · <a href="#-dokumentasi-bahasa-indonesia">Bahasa Indonesia (Di Bawah)</a> · <a href="./README.id.md">README.id.md</a>
</p>

<p><i>Universal Model Context Protocol (MCP) server, Python SDK, and Anti-Slop UI Design Engine for <b>FigCraft Desktop</b>.</i></p>

<p><b>Disclaimer:</b> This is a community-built MCP integration for FigCraft Desktop and compatible AI coding agents.</p>

<p>Prompt-assisted UI/UX design, real-time multiplayer cursor streaming, Anti-Slop UI auditing, and interactive prototyping — driven by AI.</p>

<p>
  <img src="https://img.shields.io/badge/version-1.0.0-6C5CE7?style=flat-square" alt="Version" />
  <img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/MCP-2024--11--05-00B894?style=flat-square" alt="MCP Protocol" />
  <img src="https://img.shields.io/badge/UI_Standard-Anti--Slop_UI-1E1E2D?style=flat-square" alt="Anti-Slop UI" />
  <img src="https://img.shields.io/badge/license-MIT-F59E0B?style=flat-square" alt="License MIT" />
</p>

</div>

---

## Quickstart

> **Note:** `figcraft-mcp` automatically attaches to your open **FigCraft Desktop** window on TCP port `7979`, detects your active live collaboration room (`doc.list` + `collab.peers`), moves the multiplayer AI cursor step-by-step (`~40ms` per element), and enforces **Anti-Slop UI** design tokens across any LLM.

**One command** sets up your AI apps (Google Antigravity, Claude Desktop, Claude Code, Cursor, Windsurf, VS Code) and links them to FigCraft:

### macOS / Linux

```bash
curl -LsSf https://raw.githubusercontent.com/your-username/FigCraft-MCP/main/install.sh | sh
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/your-username/FigCraft-MCP/main/install.ps1 | iex
```

From Command Prompt instead: `powershell -c "irm https://raw.githubusercontent.com/your-username/FigCraft-MCP/main/install.ps1 | iex"`

Prefer not to run a script, or already cloned this repository? Install with `uv` or `pip`, then run `setup`:

```powershell
git clone https://github.com/your-username/FigCraft-MCP.git
cd FigCraft-MCP
pip install -e .
figcraft-mcp setup
```

Already have `uv` installed? Run directly without manual cloning:

```bash
uvx --from git+https://github.com/your-username/FigCraft-MCP figcraft-mcp setup
```

`figcraft-mcp setup` automatically locates the MCP clients installed on your machine (**Google Antigravity**, **Claude Desktop**, **Claude Code**, **Cursor**, **Windsurf**, **VS Code**), adds the `figcraft` server entry, and saves a `.bak` backup of each config file it updates.

Then **fully quit and reopen your AI app**, open **FigCraft Desktop**, and ask your AI agent to design, audit, or prototype screens.

<details>
<summary><b>Manual setup, in case the automatic setup doesn't work</b></summary>

### 1. Add to `mcp_config.json` / `claude_desktop_config.json` / `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "figcraft": {
      "command": "python",
      "args": ["E:/Coding/FigCraft-MCP/src/figcraft_mcp/server.py"],
      "env": {
        "FIGCRAFT_PORT": "7979",
        "FIGCRAFT_STREAM_STEPS": "1",
        "FIGCRAFT_STREAM_DELAY_MS": "40"
      }
    }
  }
}
```

Or launch via **Node.js (`npx`)**:

```json
{
  "mcpServers": {
    "figcraft": {
      "command": "npx",
      "args": ["-y", "github:your-username/FigCraft-MCP"],
      "env": {
        "FIGCRAFT_PORT": "7979",
        "FIGCRAFT_STREAM_STEPS": "1",
        "FIGCRAFT_STREAM_DELAY_MS": "40"
      }
    }
  }
}
```

### 2. Install as a Full Agent Plugin (MCP + Skills + Rules)

To load the MCP server together with the **`figcraft`** skill, **`anti-slop-ui`** skill, and always-on **`rules/AGENTS.md`**:

```bash
# Google Antigravity (Global Plugin)
git clone https://github.com/your-username/FigCraft-MCP.git ~/.gemini/config/plugins/figcraft-mcp

# Workspace-Scoped Plugin
git clone https://github.com/your-username/FigCraft-MCP.git .agents/plugins/figcraft-mcp
```

</details>

---

## Visual Showcase & Screenshots

### 1. Real-Time Multiplayer Cursor & Step-by-Step Live Streaming
Unlike standard CLI bridges that dump an entire screen in a single frozen frame, `figcraft-mcp` streams every layer (`frame`, `rectangle`, `text`, `vector icon`) step-by-step at `40ms/element` with live multiplayer cursor tracking (`Antigravity AI`) and bounding-box selection highlights:

<p align="center">
  <img src="./assets/screenshots/05-live-cursor-streaming.jpg" alt="Live Cursor Streaming in FigCraft" width="380" />
  <img src="./assets/screenshots/07-live-session-join.jpg" alt="Live Collaboration Session in FigCraft" width="500" />
</p>

### 2. Clean, Anti-Slop UI Output (Shadcn / Radix / Apple HIG Standard)
Built-in **`anti-slop-ui`** rules prevent AI models from generating neon gradients, gratuitous `"AI Insight"` / `"AI Matched"` sparkle badges, loud orange/purple input boxes, or Unicode emojis:

<p align="center">
  <img src="./assets/screenshots/01-auth-screens.png" alt="Auth Screens - Sign In & Create Account" width="440" />
  <img src="./assets/screenshots/02-dashboard-popups.jpg" alt="Dashboard and Popup Bottom Sheets" width="440" />
</p>

<p align="center">
  <img src="./assets/screenshots/03-review-searchable-dropdown.jpg" alt="Review Transaction and Neutral Searchable Scrollable Dropdown" width="440" />
  <img src="./assets/screenshots/04-reports-and-wallets.jpg" alt="Reports (Expenses & Income) and Manage Wallets" width="440" />
</p>

### 3. Interactive Prototype Flows
Connect buttons, tabs, bottom sheets, and navigation bars across all frames with `smartAnimate`, `dissolve`, `push`, `slideIn`, and `moveOut` transitions using `create_prototype_link`:

<p align="center">
  <img src="./assets/screenshots/06-prototype-mode.png" alt="Interactive Prototype Flow Wiring in FigCraft" width="760" />
</p>

---

## How to Use with FigCraft Desktop

1. **Automatic Desktop Launch (`--control 7979`)**:
   - When your AI agent calls any `figcraft` MCP tool, `figcraft-mcp` checks if port `7979` is open. If FigCraft Desktop is not running yet, it automatically launches the visible desktop app with `--control 7979`.
2. **Joining or Hosting a Live Session**:
   - If you have an active **Live Collaboration Session** (`Bagikan` -> `Sesi langsung` in the top-right corner of FigCraft), `figcraft-mcp` automatically detects the document where `collab.peers` has `status == "live"` and streams all edits directly into your open tab.
3. **Example Prompts to Try**:
   - *"Create a Sign In and Create Account screen side-by-side following the anti-slop-ui guidelines with a clean segmented tab switcher."*
   - *"Create a Review Transaction screen with a compact searchable category dropdown, internal vertical scrollbar, and a `+ Category Baru` option when a category is not found."*
   - *"Audit Screen 5 and Screen 6 to remove any AI-slop badges, use neutral colors, and place `+ Add Wallet` right below the Total Assets card."*
   - *"Wire interactive prototype flows across all screens on Page 1."*

---

## Key Features & Architecture

| Feature | Description |
| :--- | :--- |
| **Step-by-Step Live Cursor Middleware** | Intercepts `batch` calls inside `server.py` and streams each element at `~40ms` with `collab.cursor` and `select: true` — works with **any** LLM without custom scripts. |
| **Zero-Emoji Lucide Vector Icons** | Built-in `place_lucide_icon` tool with **39 pre-scaled 24x24 Lucide SVG icons** and precomputed `ICON_BBOX` (0 extra RPC round-trips). |
| **Anti-Slop UI Token Engine** | Built-in `get_anti_slop_guidelines` tool + `skills/anti-slop-ui/SKILL.md` enforcing neutral surfaces (`#FFFFFF`, `#F8FAFC`, `#F1F5F9`), `1px` `#E2E8F0` borders, and clean typography. |
| **1-Call Prototype Wiring** | Built-in `create_prototype_link` tool to bind click triggers to target screens with `smartAnimate`, `dissolve`, `push`, `slideIn`, or `moveOut`. |
| **Popup Backdrop Standard** | Automatically teaches agents to duplicate the parent screen as a locked backdrop behind a `45%` `#0F172A` scrim for realistic modal & bottom-sheet states. |

---

## Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `FIGCRAFT_PORT` | `7979` | TCP control port used to attach to the live FigCraft Desktop instance. |
| `FIGCRAFT_STREAM_STEPS` | `1` | `1` = stream `batch` commands step-by-step with live cursor movement; `0` = instant execution. |
| `FIGCRAFT_STREAM_DELAY_MS` | `40` | Delay in milliseconds between streamed elements (`40ms` = 25 elements/sec). |
| `FIGCRAFT_DEFAULT_DOC` | *(empty)* | Optional `.figcraft` file path to auto-open when launching FigCraft Desktop. |
| `FIGCRAFT_CLI_PATH` | *(auto)* | Custom path to `figcraft-cli` executable. |
| `FIGCRAFT_APP_PATH` | *(auto)* | Custom path to `figcraft` desktop executable. |

---
---

<div align="center" id="-dokumentasi-bahasa-indonesia">

# Dokumentasi Bahasa Indonesia

<p><i>Server MCP Universal, Python SDK, dan Mesin Desain <b>Anti-Slop UI</b> untuk <b>FigCraft Desktop</b>.</i></p>

</div>

## Ringkasan Fitur Utama

**MCP for FigCraft (`figcraft-mcp`)** menghubungkan aplikasi **FigCraft Desktop** secara langsung dengan berbagai AI Agent (**Google Antigravity**, **Claude Code**, **Claude Desktop**, **Cursor**, **Windsurf**, **Cline**, **VS Code Copilot**) dengan keunggulan:

1. **Live Update Bertahap & Kursor Bergerak Real-Time (`~40ms/elemen`)**:
   - Setiap pembuatan *frame*, *rectangle*, *text*, dan *vector icon* dieksekusi secara bertahap dan cepat satu per satu di atas kanvas FigCraft Anda, lengkap dengan pergerakan kursor multiplayer (`Antigravity AI`) dan *highlight* seleksi secara langsung.
2. **Otomatis Terhubung ke Sesi Kolaborasi Aktif (`Port 7979`)**:
   - Mendeteksi jendela FigCraft Desktop yang sedang terbuka (maupun tab **Sesi Langsung / Live Session**) secara otomatis tanpa perlu *hardcode* lokasi file proyek.
3. **Standar Desain Anti-Slop UI Terintegrasi (`anti-slop-ui`)**:
   - Mencegah AI menghasilkan tampilan klise (*AI slop*) seperti warna oranye/ungu mencolok pada form input, badge berlebihan (`"Hasil Scan Struk AI"`, `"AI Matched"`, `"Food is your largest category..."`), penggunaan emoji Unicode (`🍔`, `✨`, `💰`), atau tombol aksi ganda.
   - Menghasilkan antarmuka bersih, netral, dan profesional setara **Shadcn UI / Radix / Apple HIG** (`#FFFFFF` card, `#F8FAFC` input, `#F1F2F6` segmented switcher track, `#E2E8F0` border, dan tipografi `Plus Jakarta Sans`).
4. **39 Ikon Vektor Lucide & Koneksi Prototype Interaktif**:
   - Dilengkapi tool `place_lucide_icon` (menempatkan ikon vektor 24x24 secara presisi dalam 1 langkah) dan `create_prototype_link` (menghubungkan alur *prototype* antar-layar dengan animasi `smartAnimate`, `dissolve`, `push`, `slideIn`, `moveOut`).

---

## Cara Instalasi Cepat (Quickstart)

### 1. Satu Perintah Instalasi Otomatis

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/your-username/FigCraft-MCP/main/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -LsSf https://raw.githubusercontent.com/your-username/FigCraft-MCP/main/install.sh | sh
```

**Atau melalui Git Clone Lokal:**
```powershell
git clone https://github.com/your-username/FigCraft-MCP.git
cd FigCraft-MCP
pip install -e .
figcraft-mcp setup
```

Perintah `figcraft-mcp setup` akan otomatis mendeteksi aplikasi AI di komputer Anda (**Google Antigravity**, **Claude Desktop**, **Claude Code**, **Cursor**, **Windsurf**), mencadangkan file konfigurasi lama ke `.bak`, dan mendaftarkan server MCP `figcraft`.

### 2. Instalasi sebagai Plugin Lengkap (MCP + Skills + Rules) di Antigravity
Agar `mcp_config.json`, skill `figcraft`, skill `anti-slop-ui`, dan aturan `rules/AGENTS.md` langsung aktif bersamaan:
```powershell
# Global Plugin (berlaku untuk semua proyek)
git clone https://github.com/your-username/FigCraft-MCP.git "$HOME\.gemini\config\plugins\figcraft-mcp"

# Atau khusus di dalam Workspace proyek tertentu
git clone https://github.com/your-username/FigCraft-MCP.git ".agents\plugins\figcraft-mcp"
```

---

## Cara Penggunaan dengan FigCraft Desktop

1. **Buka Aplikasi FigCraft Desktop**:
   - Anda dapat membuka file `.figcraft` secara langsung, atau membiarkan `figcraft-mcp` menyalakan aplikasi FigCraft Desktop secara otomatis melalui port kontrol `7979` (`figcraft.exe --control 7979`).
2. **Menggunakan Mode Sesi Langsung (Live Collaboration)**:
   - Jika Anda menyalakan fitur **Bagikan -> Sesi langsung** di pojok kanan atas FigCraft, server MCP otomatis mendeteksi dokumen dengan status `live` dan mengarahkan seluruh pembuatan komponen langsung ke kanvas yang sedang Anda lihat.
3. **Contoh Perintah (Prompt) ke AI Agent**:
   - *"Buat Screen Sign In dan Create Account berdampingan dengan gaya netral anti-slop-ui dan tab switcher untuk berpindah antar layar."*
   - *"Ubah bagian Category pada Screen 4 menjadi menu dropdown ringkas yang memiliki kolom search, scrollbar vertikal di dalamnya, dan opsi `+ Category Baru` ketika kategori tidak ditemukan."*
   - *"Audit Screen 5 dan Screen 6 agar warnanya netral, hapus badge AI yang terlalu ramai, dan letakkan tombol `+ Add Wallet` tepat di bawah kartu Total Assets."*
   - *"Buat koneksi prototype flow untuk seluruh layar di Page 1."*

---

## Perbandingan Sebelum vs Sesudah Anti-Slop UI

| Komponen | Sebelum (AI Slop) | Sesudah (`FigCraft-MCP` + `anti-slop-ui`) |
| :--- | :--- | :--- |
| **Header & Kartu Ringkasan** | Penuh badge ungu/hijau/merah muda (`✨ Hasil Scan Struk AI`, `📈 18% vs Feb`, `✨ Food is your largest category`) | Bersih & fokus pada hierarki tipografi (`#1E1E2D` Bold & `#8F92A1` Muted) tanpa badge dekoratif berlebihan |
| **Segmented Tab Switcher** | Berisi ikon panah warna merah/hijau di dalam setiap tab | Permukaan netral `#F1F2F6` dengan pill aktif `#FFFFFF` dan teks bersih tanpa ikon (seperti gaya `Screen 5`) |
| **Menu Dropdown Kategori** | Trigger berwarna oranye terang (`#FFF7ED`), pill `"AI Matched"`, dan kotak ungu besar | Trigger & menu putih bersih (`#FFFFFF`), border `#CBD5E1` / `#E2E8F0`, highlight baris `#F1F5F9`, scrollbar vertikal `4px`, dan baris aksi netral `+ Category Baru` |
| **Ikonografi** | Emoji Unicode (`🍔`, `🚗`, `💰`) yang tidak konsisten | 100% ikon garis vektor **Lucide 24x24** (`place_lucide_icon`) |

---

## Lisensi

Dirilis di bawah lisensi [MIT License](./LICENSE).
