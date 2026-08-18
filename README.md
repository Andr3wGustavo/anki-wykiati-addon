# Anki Wykiati Toolkit

<div align="center">

  <img src="imgs/logo_nova.png" alt="Anki Wykiati Toolkit Logo" width="180" style="border-radius: 20px; margin-bottom: 12px;" />

  # ⚡ Anki Wykiati Toolkit
  ### Automated Discord Image Ingestion • In-Memory WebP Optimizer • True AMOLED Black Theme Studio

  <p align="center">
    <strong>A high-performance, modular Anki add-on engineered for students, medical researchers, language learners, and developers.</strong><br/>
    Seamlessly turn Discord study channels and REST Webhooks into flashcards with automated WebP compression and a gorgeous AMOLED visual design.
  </p>

  <p align="center">
    <a href="https://ankiweb.net/shared/addons/"><img src="https://img.shields.io/badge/Anki-2.1.50%2B%20%7C%2023.10%2B%20%7C%2024.04%2B-blue?style=for-the-badge&logo=anki&logoColor=white" alt="Anki Compatibility" /></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License MIT" /></a>
    <a href="https://buymeacoffee.com/wykiati"><img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-wykiati-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee" /></a>
  </p>

  <p align="center">
    <a href="#-key-features">Key Features</a> •
    <a href="#-visual-showcase--gallery">Visual Showcase</a> •
    <a href="#-quick-1-minute-setup">Quick Setup</a> •
    <a href="#-discord-ingestion-pipeline">Discord Ingestion</a> •
    <a href="#-local-http-webhook-api">HTTP Webhook API</a> •
    <a href="#-software-architecture">Architecture</a> •
    <a href="#-configuration-reference">Config Reference</a> •
    <a href="#-support--sponsorship">Support</a>
  </p>

</div>

---

## ☕ Support the Project

If **Anki Wykiati Toolkit** saves you study time, boosts your daily flashcard retention, or beautifies your Anki experience, consider buying a coffee to support continued development and official **AnkiWeb** hosting!

<div align="center">
  <a href="https://buymeacoffee.com/wykiati" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="220" style="border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.3);" />
  </a>
  <br/>
  <p><em>Every contribution directly supports new features, image occlusion AI, and lifetime updates on AnkiWeb.</em></p>
</div>

---

## 🌟 Visual Showcase & Gallery

<div align="center">
  <a href="imgs/anki%20full%20black.png">
    <img src="imgs/anki%20full%20black.png" alt="Anki Wykiati Toolkit - AMOLED Black Theme & Operational Interface" width="94%" style="border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 10px 30px rgba(0,0,0,0.8);" />
  </a>
  <p><em>Figure 1: Deep AMOLED Void Black (#000000) Reviewer, Translucent Glass Dialogs, and Operational Sync Monitor.</em></p>
</div>

<br/>

<div align="center">
  <table>
    <tr>
      <td width="50%" align="center">
        <img src="imgs/anki%20full%20black.png" alt="Discord Bot Settings & Image Ingestion" width="100%" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);" />
        <br/>
        <strong>🤖 Automated Discord Image Ingestion</strong>
        <p><em>Configure channel IDs, target decks (e.g., <code>Medicine::Anatomy</code>), and Front-Only visual card layouts.</em></p>
      </td>
      <td width="50%" align="center">
        <img src="imgs/anki%20full%20black.png" alt="RGB Studio & Dynamic WCAG Contrast Engine" width="100%" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);" />
        <br/>
        <strong>🎨 Interactive RGB Color Studio</strong>
        <p><em>Circular RGB Color Wheel with live adaptive contrast—text and buttons stay 100% readable regardless of background luminance.</em></p>
      </td>
    </tr>
  </table>
</div>

---

## 🚀 Key Features

### 1. 📥 Automated Discord Image Ingestion
- **Drop-and-Sync Workflow**: Share diagrams, screenshots, slides, or medical imaging in your private or group Discord channels. The add-on immediately downloads, processes, and inserts them as native Anki cards in your target deck.
- **Flexible Card Layouts**:
  - **Image Front-Only (Visual Card)**: The image occupies the front with an empty back—ideal for rapid visual recognition drills and anatomy practice.
  - **Image Front / Caption Back**: Discord message comments, notes, or explanations appear on the reverse side.
  - **Question Front / Image Back**: Message text serves as the question prompt, revealing the diagram upon card flip.

### 2. ⚡ One-Click On-Demand Channel Sync
- Missed images while Anki was closed? Open the settings dialog and press **📥 Pull Recent Discord Images Now** to fetch the last 50 channel attachments on-demand.
- Built-in **SHA-256 cryptographic anti-duplication** ensures no card or media file is ever imported twice.

### 3. 🖼️ In-Memory WebP Image Optimizer & Media Compressor
- **Massive Storage Savings**: High-resolution 4K/8K images are automatically downscaled (e.g. max 1920px width/height) and converted to high-efficiency **WebP** format at 85% quality.
- **Zero Disk Latency**: Media compression executes entirely in memory via Pillow before writing to Anki's `collection.media`, saving up to **85% disk space** and accelerating AnkiWeb mobile synchronization across iPhone, iPad, and Android.

### 4. 🌌 True AMOLED Void Black (`#000000`) & RGB Studio
- **Pure Zero-Light OLED Black**: True `#000000` background across all Qt widgets, Deck Browser, Card Reviewer, and Bottom Action Bars to save battery and reduce eye fatigue.
- **iOS Liquid Glass & Capsule Styling**: Translucent glass modals (`rgba(20, 22, 28, 0.75)`), floating pill buttons (`border-radius: 20px`), and minimalist sleek scrollbars.
- **Intelligent WCAG Adaptive Contrast**: Mathematical luminance calculation ensures fonts, borders, and selection highlights automatically adapt to dark or light tones when custom RGB hues are chosen.
- **One-Key Theme Toggle**: Instantly toggle the visual theme inside Anki using `Ctrl+Shift+B`.

### 5. 🌐 Local HTTP Webhook REST Bridge
- Built-in lightweight local REST API on `http://127.0.0.1:8765/api/card`.
- Send flashcards and images directly from Python scripts, curl, Raycast, Alfred workflows, Obsidian plugins, or custom browser extensions.

### 6. 🗂️ Smart Deck Routing Engine
- Rule-based routing engine that maps tags (`#biology` ➔ `Science::Biology`) and body keywords automatically to nested hierarchical decks (`Parent::Child`).

### 7. 🔒 Asynchronous Non-Blocking Sync Worker
- Thread-safe persistent FIFO queue (`data/queue.json`) with exponential retry backoff.
- Jobs execute safely on background threads and dispatch UI updates to Anki's main thread without interface stutter or UI freezing.

---

## ⏱️ Quick 1-Minute Setup

### Step 1: Install the Add-on
1. Download the latest `.ankiaddon` package from the [Releases](https://github.com/Andr3wGustavo/anki-wykiati-addon/releases) section or generate it locally via `python package_addon.py`.
2. In Anki, navigate to **Tools ➔ Add-ons** (`Ctrl+Shift+A`).
3. Click **Install from file...** and select `anki-discord-toolkit.ankiaddon`.
4. Restart Anki.

### Step 2: Configure Your Discord Bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create an Application.
2. In the **Bot** tab, generate a **Bot Token** and enable **Message Content Intent**.
3. Invite the bot to your study server with *Read Messages / View Channels* permissions.
4. In Anki, open **Tools ➔ Anki Wykiati Toolkit ➔ Discord & Image Settings...**:
   - Paste your **Bot Token**.
   - Enter your target **Channel ID** (e.g. `119283746509182736`).
   - Select your target deck (e.g. `Medicine::Anatomy`).
   - Choose your preferred layout (e.g. *Image on Front Only*).
5. Click **Save Settings** (or click **📥 Pull Recent Discord Images Now** to test immediate synchronization).

---

## 💬 Discord Commands & Syntax Guide

In addition to automated image channel ingestion, the bot listens for structured flashcard creation messages:

### Standard Q&A Flashcard
```text
!anki
front: What is the primary function of the mitochondria?
back: Cellular respiration and adenosine triphosphate (ATP) production.
deck: Biology::Cellular
tags: biology, cellular, exam-prep
```

### Cloze Deletion Flashcard
```text
!anki
front: The {{c1::TCP}} protocol provides reliable ordered delivery, while {{c2::UDP}} prioritizes low latency.
deck: Computer Science::Networking
tags: networking, protocols
```

### Operational Commands
| Command | Action |
|---|---|
| `!anki-help` | Displays interactive syntax and format instructions in Discord. |
| `!anki-status` | Returns system uptime, active theme state, and processed card counts. |
| `!anki-decks` | Lists all decks and subdecks available in the connected Anki collection. |
| `!anki-ping` | Verifies low-latency connectivity with the active Anki session. |

---

## 🌐 Local HTTP Webhook API

The integrated HTTP REST bridge runs locally on `127.0.0.1:8765`, enabling programmatic card creation from any tool or language:

### 1. Create a Standard Card (JSON POST)
```bash
curl -X POST http://127.0.0.1:8765/api/card \
  -H "Content-Type: application/json" \
  -d '{
    "front": "What is the time complexity of Binary Search?",
    "back": "O(log n) on sorted datasets.",
    "deck": "Computer Science::Algorithms",
    "tags": ["dsa", "algorithms"]
  }'
```

### 2. Ingest an Image Directly from a URL
```bash
curl -X POST http://127.0.0.1:8765/api/card \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/heart-anatomy.png",
    "caption": "Anatomy of the Human Heart - Anterior View",
    "deck": "Medicine::Cardiology",
    "tags": ["cardiology", "anatomy"]
  }'
```

### 3. Server Health Check
```bash
curl http://127.0.0.1:8765/health
```

---

## 📐 Software Architecture & Data Flow

The project follows Clean Architecture and SOLID design principles, strictly decoupling network ingestion, image optimization, anti-duplication, and UI rendering:

```text
  [Discord Bot REST Poller]        [Local HTTP Webhook /api/card]        [One-Click Sync]
             │                                   │                              │
             └───────────────────────────────────┼──────────────────────────────┘
                                                 ▼
                                     [Authorization & Policy]
                               (Channel Whitelist, Rate Limiter)
                                                 ▼
                                          [Discord Bridge]
                            (Image Attachment vs !anki Protocol Parser)
                                                 ▼
                                     [Media & Optimizer Engine]
                           (In-Memory WebP Conversion & 1920px Resize)
                                                 ▼
                                    [Anti-Duplication Registry]
                                 (SHA-256 Binary Content Check)
                                                 ▼
                                    [Persistent FIFO Job Queue]
                                     (Disk-backed data/queue.json)
                                                 ▼
                                      [Background Sync Worker]
                                      (Safe Async Retry Thread)
                                                 ▼
                                     [Smart Deck Routing Engine]
                                   (Tag & Keyword Hierarchy Rules)
                                                 ▼
                                      [Main Thread Qt Adapter]
                                  (Dispatched safely to UI Thread)
                                                 ▼
                                        [Anki SQLite DB]
```

### Key Modules & Directories
- `anki-addon/discord/client.py`: Dual-mode Discord REST client and embedded HTTP REST server.
- `anki-addon/discord/bridge.py`: Dispatches messages and attachments to image ingestion or note parsing pipelines.
- `anki-addon/anki/media.py`: Handles downloading, in-memory WebP compression, dimension downscaling, and SHA-256 hash tracking.
- `anki-addon/anki/notes.py` & `anki/decks.py`: Thread-safe note factory and hierarchical deck generator (`Parent::Child`).
- `anki-addon/theme/styles.py` & `palette.py`: Mathematical WCAG luminance adapter, AMOLED `#000000` QSS, and WebView dark CSS.
- `anki-addon/sync/queue.py` & `sync/worker.py`: Disk-backed FIFO queue with exponential retry backoff.
- `anki-addon/routing/router.py`: Tag and keyword rule-based routing engine.

---

## ⚙️ Configuration Reference

All settings can be customized through the GUI dialogs (**Tools ➔ Anki Wykiati Toolkit**) or edited in `config.json`:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `addon_enabled` | `boolean` | `true` | Master toggle for the add-on toolkit. |
| `theme.enabled` | `boolean` | `true` | Enables the AMOLED Void Black & Liquid Glass theme. |
| `theme.background` | `string` | `"#000000"` | Hex code for background (Full Black AMOLED or custom RGB). |
| `theme.accent` | `string` | `"#0A84FF"` | Accent color for highlights, badges, and focus rings. |
| `theme.apply_to_webviews` | `boolean` | `true` | Injects custom dark CSS into Anki webviews (reviewer & deck browser). |
| `theme.pure_black_reviewer` | `boolean` | `true` | Forces pure black background during card flashcard review. |
| `discord.enabled` | `boolean` | `false` | Enables background Discord channel polling worker. |
| `discord.bot_token` | `string` | `""` | Discord Bot secret authentication token. |
| `discord.image_channels` | `list[str]` | `[]` | Discord Channel IDs monitored for automated image ingestion. |
| `discord.image_default_deck` | `string` | `"Images::Discord"` | Default target deck for ingested images. |
| `discord.image_card_layout` | `string` | `"image_front"` | Layout mode (`"image_only_front"`, `"image_front"`, `"image_back"`). |
| `discord.optimize_images` | `boolean` | `true` | Enables in-memory WebP compression and dimension downscaling. |
| `discord.max_image_dimension` | `integer` | `1920` | Maximum pixel width/height before auto-downscaling. |
| `discord.image_quality` | `integer` | `85` | WebP compression quality factor (1–100). |
| `discord.convert_to_webp` | `boolean` | `true` | Converts heavy PNG/JPEG images to lightweight WebP. |
| `discord.http_bridge_enabled` | `boolean` | `true` | Starts the local HTTP REST Webhook server. |
| `discord.http_bridge_port` | `integer` | `8765` | Local HTTP REST port (`http://127.0.0.1:8765`). |
| `anki.default_deck` | `string` | `"Default"` | Fallback deck when no routing rule matches. |

---

## 🧪 Testing & Developer Tooling

The project includes an interactive Windows Developer Console and automated unit test suite:

### Option A: Windows Control Console
Double-click `test_addon.bat` or run from command line:
```cmd
test_addon.bat
```
- **[1] Run Unit Tests**: Executes the complete headless test suite with mock Anki environment.
- **[2] Build Package (.ankiaddon)**: Generates clean distribution archive in `release/`.
- **[3] Start HTTP Bridge**: Runs standalone local HTTP webhook server on port 8765.
- **[4] Send Test Card**: Pushes a sample card to the local webhook via PowerShell.
- **[5] Clean Reinstall to Anki**: Copies the latest code to `%APPDATA%\Anki2\addons21\`.
- **[6] Open HTML Preview**: Displays live webview theme preview (`preview.html`).
- **[7] Launch Qt UI Preview**: Launches standalone PyQt desktop dialog preview (`preview_ui.py`).

### Option B: Automated Headless Tests
```bash
python -m unittest discover -s anki-addon/tests -p "test_*.py" -v
```

---

## 📦 Packaging for AnkiWeb Distribution

To package the add-on for upload to **AnkiWeb**:

```bash
python package_addon.py
```

The script cleans all temporary files, cache, and logs, generating the ready-to-upload artifact at:
`release/anki-discord-toolkit.ankiaddon`

Refer to [docs/ANKIWEB_PUBLISHING_GUIDE.md](docs/ANKIWEB_PUBLISHING_GUIDE.md) for full step-by-step publishing instructions.

---

## 💖 Support & Contributions

Contributions, bug reports, and pull requests are warmly welcomed!

- **Buy Me A Coffee**: [buymeacoffee.com/wykiati](https://buymeacoffee.com/wykiati)
- **GitHub Repository**: [github.com/Andr3wGustavo/anki-wykiati-addon](https://github.com/Andr3wGustavo/anki-wykiati-addon)
- **Issue Tracker**: [github.com/Andr3wGustavo/anki-wykiati-addon/issues](https://github.com/Andr3wGustavo/anki-wykiati-addon/issues)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
Created and maintained with ❤️ by **Wykiati / Antigravity Engineering**.
