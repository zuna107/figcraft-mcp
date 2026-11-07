<div align="center">

<img src="./assets/banner.svg" alt="MCP for FigCraft Banner" width="840" />

<h3>Hubungkan AI Coding Agent Anda secara live ke FigCraft Desktop.<br/>Desain, audit, dan buat prototype UI profesional secara real-time.</h3>

<p>
  <a href="https://github.com/zuna107/figcraft-mcp/releases"><img src="https://img.shields.io/github/v/release/zuna107/figcraft-mcp?style=flat-square&color=6C5CE7" alt="Release" /></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/MCP-2024--11--05-00B894?style=flat-square" alt="MCP Protocol" />
  <img src="https://img.shields.io/badge/UI_Standard-Anti--Slop_UI-1E1E2D?style=flat-square" alt="Anti-Slop UI" />
  <a href="https://github.com/zuna107/figcraft-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-F59E0B?style=flat-square" alt="License MIT" /></a>
</p>

<p>
  <a href="https://github.com/zuna107/figcraft-mcp/blob/main/README.md">English (README.md)</a> · <b>Bahasa Indonesia</b> · <a href="https://github.com/zuna107/figcraft-mcp/releases">Releases</a> · <a href="https://github.com/zuna107/figcraft-mcp/blob/main/CONTRIBUTING.md">Contributing</a>
</p>

<p><b>Disclaimer:</b> Proyek ini adalah integrasi komunitas berbasis Model Context Protocol (MCP) untuk FigCraft Desktop.</p>

</div>

Berikan akses langsung secara *real-time* kepada **Google Antigravity**, **Cursor**, **Claude Code**, **Claude Desktop**, **Windsurf**, dan AI coding agent lainnya untuk mengendalikan kanvas **FigCraft Desktop** Anda melalui server [Model Context Protocol](https://modelcontextprotocol.io/) ini.

Berbeda dari *bridge* CLI biasa yang menampilkan hasil desain secara kaku sekaligus atau menghasilkan tampilan klise (*AI slop*), **FigCraft-MCP** mengeksekusi setiap komponen secara bertahap dengan pergerakan kursor multiplayer langsung (`~40ms/elemen`) serta menerapkan standar desain **Anti-Slop UI** setara **Shadcn UI**, **Radix Primitives**, dan **Apple HIG**.

[**Lihat panduan instalasi cepat ->**](#instalasi-cepat-quickstart) · [**Lihat panduan penggunaan langkah demi langkah ->**](#cara-penggunaan-dengan-figcraft-desktop)

---

## Galeri Visual & Demo

### 1. Kursor Multiplayer Real-Time & Live Streaming Bertahap
Setiap elemen (`frame`, `rectangle`, `text`, `vector icon`) dibuat secara bertahap dan cepat (`40ms/elemen`) disertai pergerakan kursor multiplayer (`Antigravity AI`) dan *highlight* seleksi langsung di atas kanvas FigCraft Anda:

<p align="center">
  <img src="./assets/screenshots/05-live-cursor-streaming.jpg" alt="Live Cursor Streaming pada Auth Screen di FigCraft" width="440" />
  <img src="./assets/screenshots/07-live-session-join.jpg" alt="Sesi Kolaborasi Langsung di FigCraft" width="440" />
</p>

### 2. Output Desain Bersih & Bebas AI Slop (Standar Shadcn / Radix / Apple HIG)
Aturan **`anti-slop-ui`** bawaan mencegah model AI membuat gradien neon, badge dekoratif berlebihan (`"Hasil Scan Struk AI"`, `"AI Matched"`), kotak input berwarna mencolok, maupun emoji Unicode:

<p align="center">
  <img src="./assets/screenshots/03-review-searchable-dropdown.jpg" alt="Screen 3, 4, 4B: Review Transaction dan Searchable Scrollable Dropdown Netral" width="440" />
  <img src="./assets/screenshots/04-reports-and-wallets.jpg" alt="Screen 5, 5B, 6, 6B: Report (Expenses & Income) dan Manage Wallets" width="440" />
</p>

### 3. Alur Prototype Interaktif
Hubungkan tombol, tab switcher, popup bottom sheet, dan navigasi bawah di seluruh layar dengan animasi `smartAnimate`, `dissolve`, `push`, `slideIn`, dan `moveOut` menggunakan `create_prototype_link`:

<p align="center">
  <img src="./assets/screenshots/06-prototype-mode.png" alt="Alur Prototype Interaktif di FigCraft" width="840" />
</p>

---

## Instalasi Cepat (Quickstart)

**Satu perintah** untuk menyiapkan aplikasi AI Anda (Google Antigravity, Claude Desktop, Claude Code, Cursor, Windsurf, VS Code) dan menghubungkannya ke FigCraft Desktop:

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/zuna107/figcraft-mcp/main/install.ps1 | iex
```

Dari Command Prompt (CMD): `powershell -c "irm https://raw.githubusercontent.com/zuna107/figcraft-mcp/main/install.ps1 | iex"`

### macOS / Linux

```bash
curl -LsSf https://raw.githubusercontent.com/zuna107/figcraft-mcp/main/install.sh | sh
```

Jika Anda memilih instalasi melalui Git clone lokal atau `uvx`:

```powershell
git clone https://github.com/zuna107/figcraft-mcp.git
cd figcraft-mcp
pip install -e .
figcraft-mcp setup
```

Atau jalankan langsung via `uvx` tanpa clone manual:

```bash
uvx --from git+https://github.com/zuna107/figcraft-mcp figcraft-mcp setup
```

Perintah `figcraft-mcp setup` otomatis mendeteksi aplikasi AI yang terpasang di komputer Anda (**Google Antigravity**, **Claude Desktop**, **Claude Code**, **Cursor**, **Windsurf**, **VS Code**), menambahkan konfigurasi server `figcraft`, dan menyimpan cadangan file lama dengan akhiran `.bak`.

Setelah selesai, **tutup dan buka kembali aplikasi AI / IDE Anda**, buka **FigCraft Desktop**, lalu minta AI untuk membuat, mengaudit, atau menghubungkan prototype desain UI.

<details>
<summary><b>Konfigurasi manual (jika setup otomatis tidak digunakan)</b></summary>

### 1. Tambahkan ke `mcp_config.json` / `claude_desktop_config.json` / `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "figcraft": {
      "command": "figcraft-mcp",
      "args": [],
      "env": {
        "FIGCRAFT_PORT": "7979",
        "FIGCRAFT_STREAM_STEPS": "1",
        "FIGCRAFT_STREAM_DELAY_MS": "40"
      }
    }
  }
}
```

Atau jalankan tanpa instalasi menggunakan **Node.js (`npx`)**:

```json
{
  "mcpServers": {
    "figcraft": {
      "command": "npx",
      "args": ["-y", "github:zuna107/figcraft-mcp"],
      "env": {
        "FIGCRAFT_PORT": "7979",
        "FIGCRAFT_STREAM_STEPS": "1",
        "FIGCRAFT_STREAM_DELAY_MS": "40"
      }
    }
  }
}
```

### 2. Pasang sebagai Plugin Lengkap (MCP + Skills + Rules)

Agar server MCP aktif bersama skill **`figcraft`**, skill **`anti-slop-ui`**, dan aturan **`rules/AGENTS.md`**:

```powershell
# Google Antigravity (Global Plugin)
git clone https://github.com/zuna107/figcraft-mcp.git "$HOME\.gemini\config\plugins\figcraft-mcp"

# Plugin Khusus Workspace Proyek
git clone https://github.com/zuna107/figcraft-mcp.git ".agents\plugins\figcraft-mcp"
```

</details>

---

## Cara Penggunaan dengan FigCraft Desktop

Ikuti panduan langkah demi langkah berikut untuk mendesain, menginspeksi, mengaudit, dan membuat prototype layar UI secara langsung di FigCraft Desktop:

### Langkah 1: Buka FigCraft Desktop & Atur Bahasa Antarmuka (Opsional)
1. Anda **tidak perlu** menjalankan perintah khusus secara manual. Ketika AI Agent memanggil tool `figcraft`, `figcraft-mcp` otomatis memeriksa port TCP `7979` dan menjalankan aplikasi **FigCraft Desktop** dengan argumen `--control 7979` apabila belum terbuka.
2. Jika Anda membuka FigCraft Desktop sendiri melalui terminal atau shortcut, tambahkan flag `--control 7979`:
   ```powershell
   "C:\Program Files\ArtCraft\FigCraft\figcraft.exe" --control 7979
   ```
3. **Mengubah Bahasa Aplikasi FigCraft:** Tekan `Ctrl + ,` (atau klik ikon menu kiri atas -> `Edit` -> `Preferences` / `Preferensi` -> `Interface Language` / `Bahasa Antarmuka`) untuk mengganti bahasa tampilan antara `English` dan `Bahasa Indonesia`, atau minta AI menjalankan perintah `pref.language` dengan `{"language": "en"}` atau `{"language": "id"}`.

### Langkah 2: Hubungkan Kanvas Anda (Pilih Mode A atau Mode B)

#### Mode A: Koneksi Lokal Otomatis Tanpa Klik (Default)
- Cukup buka file `.figcraft` (atau buat tab baru) di FigCraft Desktop lalu kirim instruksi di aplikasi AI Anda.
- `figcraft-mcp` otomatis terhubung ke dokumen aktif dan mengeksekusi setiap `frame`, `rectangle`, `text`, serta `vector icon` satu per satu (`~40ms/elemen`) lengkap dengan *highlight* seleksi secara langsung.

#### Mode B: Sesi Kolaborasi Langsung & Kursor Multiplayer AI (`Share -> Live Session`)
- Ingin melihat kursor multiplayer ungu **`Antigravity AI`** bergerak secara *real-time* di atas kanvas saat AI menggambar komponen?
  1. Klik tombol **`Share` -> `Live Session`** (atau **`Bagikan` -> `Sesi langsung`**) di pojok kanan atas FigCraft Desktop, atau minta AI memulai sesi kolaborasi lokal melalui `collab.share` (`{"via": "local"}`).
  2. `figcraft-mcp` otomatis mendeteksi tab dokumen berstatus `live` melalui `doc.list` dan `collab.peers`, lalu mengirimkan koordinat kursor (`collab.cursor`) secara langsung sembari menyusun elemen di kanvas Anda.

### Langkah 3: Berikan Instruksi (Prompt) ke AI Agent

Anda dapat memberikan perintah dalam bahasa alami. Berikut tahapan alur kerja yang direkomendasikan:

1. **Membuat Layar UI Baru dari PRD (Standar Anti-Slop UI)**
   > *"Buat Screen Sign In dan Create Account berdampingan (360x800) mengikuti aturan anti-slop-ui dengan segmented tab switcher netral dan ikon vektor Lucide."*
2. **Membuat Popup Bottom Sheet & Menu Dropdown dengan Search + Scroll**
   > *"Buat Popup Bottom Sheet untuk Screen 2 dan Screen 3 di atas backdrop Screen 1 yang dikunci dengan scrim gelap 45%."*
   > *"Ubah bagian Category pada Screen 4 menjadi menu dropdown ringkas (tinggi maks 180px) dengan kolom search, scrollbar vertikal 4px di dalam menu, dan opsi `+ Category Baru` ketika kategori belum tersedia."*
3. **Mengaudit & Merapikan Layar dari AI Slop**
   > *"Audit Screen 5 dan Screen 6 menggunakan standar anti-slop-ui: hapus badge AI yang berlebihan, gunakan warna netral, dan pindahkan tombol `+ Add Wallet` tepat di bawah kartu Total Assets."*
4. **Menghubungkan & Menguji Alur Prototype Interaktif**
   > *"Hubungkan seluruh layar di Page 1 dengan transisi prototype interaktif (`smartAnimate` untuk pergantian tab, `slideIn` untuk popup bottom sheet, dan `push` untuk perpindahan halaman)."*
   - Untuk mencoba hasilnya di FigCraft Desktop, buka tab **`Prototype`** di panel kanan atau klik tombol **Play (`▶`)** di pojok kanan atas.

---

## Daftar Tool MCP (Total 25 Tool)

Selain meneruskan 22 tool bawaan `figcraft-cli` (`inspect_document`, `get_node`, `create_node`, `set_properties`, `batch`, `run_command`, `export`, `screenshot`, `save_file`, dll.), `figcraft-mcp` menyediakan **3 tool tingkat tinggi**:

| Nama Tool | Fungsi |
| :--- | :--- |
| `get_anti_slop_guidelines` | Mengambil sistem token warna netral (`#FFFFFF`, `#F8FAFC`, `#F1F5F9`, `#E2E8F0`), skala tipografi (`Plus Jakarta Sans`), daftar pola AI slop yang dilarang, dan resep komponen. |
| `place_lucide_icon` | Menempatkan **39 ikon garis vektor Lucide 24x24** (`search`, `download`, `wallet`, `home`, `barChart`, `plus`, `x`, `check`, `chevronDown`, `user`, `mail`, `lock`, dll.) secara presisi dalam 1 langkah. |
| `create_prototype_link` | Menghubungkan elemen pemicu (`sourceId`) ke frame tujuan (`targetFrameId`) dengan animasi `smartAnimate`, `dissolve`, `push`, `slideIn`, atau `moveOut`. |

---

## Perbandingan Sebelum vs Sesudah Anti-Slop UI

| Komponen | Pola AI Slop (Dilarang) | Standar FigCraft-MCP (Diterapkan) |
| :--- | :--- | :--- |
| **Header & Kartu Ringkasan** | Penuh badge ungu/merah muda (`✨ Hasil Scan Struk AI`, `📈 18% vs Feb`, `✨ Food is your largest category`) | Bersih & fokus pada hierarki tipografi (`#1E1E2D` Bold & `#8F92A1` Muted) tanpa dekorasi berlebihan |
| **Segmented Tab Switcher** | Berisi ikon panah warna merah/hijau di dalam tab | Track netral `#F1F2F6`, pill aktif `#FFFFFF`, teks rata tengah tanpa ikon |
| **Menu Dropdown Kategori** | Trigger oranye terang (`#FFF7ED`), pill `"AI Matched"`, daftar memanjang tanpa batas | Menu ringkas `180px` `#FFFFFF`, border `#CBD5E1`, baris aktif `#F1F5F9`, scrollbar vertikal `4px`, dan baris `+ Category Baru` |
| **Ikonografi** | Emoji Unicode (`🍔`, `🚗`, `💰`, `✨`) | 100% ikon garis vektor **Lucide 24x24** melalui `place_lucide_icon` |
| **Popup & Bottom Sheet** | Melayang di atas kotak hitam kosong | Menduplikasi layar induk sebagai *locked backdrop* di belakang *scrim* `#0F172A` (`45%` opacity) |

---

## Variabel Lingkungan (Environment Variables)

| Variabel | Default | Keterangan |
| :--- | :--- | :--- |
| `FIGCRAFT_PORT` | `7979` | Port kontrol TCP untuk terhubung ke aplikasi FigCraft Desktop yang sedang berjalan. |
| `FIGCRAFT_STREAM_STEPS` | `1` | `1` mengeksekusi perintah `batch` satu per satu dengan kursor live; `0` mengeksekusi sekaligus. |
| `FIGCRAFT_STREAM_DELAY_MS` | `40` | Jeda waktu antar elemen saat live streaming (`40ms` = 25 elemen/detik). |
| `FIGCRAFT_DEFAULT_DOC` | *(kosong)* | Lokasi file `.figcraft` opsional untuk dibuka otomatis saat menjalankan FigCraft Desktop. |
| `FIGCRAFT_CLI_PATH` | *(otomatis)* | Path khusus menuju file executable `figcraft-cli`. |
| `FIGCRAFT_APP_PATH` | *(otomatis)* | Path khusus menuju aplikasi desktop `figcraft`. |

---

## Kontribusi & Komunitas

Kontribusi penambahan ikon vektor, resep komponen Anti-Slop UI, dan dukungan klien baru sangat terbuka!
- Baca [Panduan Kontribusi (CONTRIBUTING.md)](./CONTRIBUTING.md) untuk memulai pengembangan lokal dan menjalankan pengujian unit.
- Lihat [Roadmap](./ROADMAP.md), [Changelog](./CHANGELOG.md), dan [Kebijakan Keamanan (SECURITY.md)](./SECURITY.md).

---

## Lisensi

Dirilis di bawah lisensi [MIT License](./LICENSE).
