# Anki Wykiati Toolkit

<div align="center">

  
  # Anki Wykiati Toolkit
  ### Automated Discord Image Ingestion, In-Memory WebP Transcoding, and AMOLED Theme Engine

  <p align="center">
    <strong>A modular, high-throughput Anki add-on engineered for students, medical researchers, language learners, and developers.</strong><br/>
    Streamline visual flashcard generation directly from Discord channels and local REST webhooks with automated in-memory WebP compression, cryptographic anti-duplication, and a true AMOLED visual system.
  </p>

  <p align="center">
    <a href="https://ankiweb.net/shared/addons/"><img src="https://img.shields.io/badge/Anki-2.1.50%2B%20%7C%2023.10%2B%20%7C%2024.04%2B-007ACC?style=flat-square" alt="Anki Compatibility" /></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-3776AB?style=flat-square" alt="Python Version" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License MIT" /></a>
    <a href="https://github.com/Andr3wGustavo/anki-wykiati-addon/actions"><img src="https://img.shields.io/badge/Tests-45%2F45%20Passing-brightgreen?style=flat-square" alt="Test Status" /></a>
  </p>

  <p align="center">
    <a href="#overview">Overview</a> •
    <a href="#visual-showcase">Visual Showcase</a> •
    <a href="#key-architectural-features">Key Features</a> •
    <a href="#system-architecture--data-flow">Architecture</a> •
    <a href="#installation--quick-start">Quick Start</a> •
    <a href="#discord-ingestion--command-syntax">Discord Ingestion</a> •
    <a href="#local-http-webhook-api">HTTP Webhook API</a> •
    <a href="#configuration-reference">Configuration</a> •
    <a href="#testing--developer-tooling">Developer Guide</a> •
    <a href="#troubleshooting">Troubleshooting</a> •
    <a href="#support--sponsorship">Support</a>
  </p>

</div>

---

## Overview

The process of creating flashcards is traditionally one of the highest friction points in spaced repetition workflows. Students in medicine, engineering, law, and language acquisition frequently capture anatomical diagrams, lecture slides, code snippets, and research charts within study groups on Discord or external productivity tools. Manually saving images, cropping, converting them to compressed formats, creating decks, and pasting content into Anki interrupts focus and consumes substantial storage.

**Anki Wykiati Toolkit** solves this bottleneck through a decoupled, event-driven architecture that bridges external data sources with Anki's native SQLite storage:

- **Automated Discord Media Ingestion**: Monitors designated Discord channels and converts image attachments into flashcards instantaneously.
- **In-Memory WebP Transcoding**: Automatically resizes high-resolution media and converts files to WebP in memory, reducing storage overhead by up to 85% while speeding up mobile synchronization.
- **Cryptographic Anti-Duplication**: Prevents redundant card generation and duplicate media downloads using SHA-256 content hashing.
- **True AMOLED Theme Engine**: Full `#000000` dark theme with WCAG-compliant dynamic luminance adaptation and customizable RGB palettes across Qt dialogs, the card reviewer, and webviews.
- **Embedded HTTP REST API**: Facilitates programmatic card insertion from CLI utilities, curl, Raycast, Alfred, and Obsidian plugins via `http://127.0.0.1:8765/api/card`.

---

## Visual Showcase

<div align="center">
  <a href="imgs/anki%20full%20black.png">
    <img src="imgs/anki%20full%20black.png" alt="Anki Wykiati Toolkit - AMOLED Black Theme and Operational Interface" width="94%" style="border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 10px 30px rgba(0,0,0,0.8);" />
  </a>
  <p><em>Figure 1: Deep AMOLED Void Black (#000000) Reviewer, Translucent Glass Dialogs, and Operational Sync Monitor.</em></p>
</div>

<br/>

<div align="center">
  <table>
    <tr>
      <td width="50%" align="center">
        <a href="imgs/discord%20and%20image%20settings.png">
          <img src="imgs/discord%20and%20image%20settings.png" alt="Discord Bot Settings and Image Ingestion" width="100%" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);" />
        </a>
        <br/>
        <strong>Automated Discord Ingestion Interface</strong>
        <p><em>Configure bot tokens, target channels, deck routing targets, and visual card layout templates.</em></p>
      </td>
      <td width="50%" align="center">
        <a href="imgs/rgb%20color%20background%20selector.png">
          <img src="imgs/rgb%20color%20background%20selector.png" alt="RGB Studio and Dynamic WCAG Contrast Engine" width="100%" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);" />
        </a>
        <br/>
        <strong>Interactive RGB Color Studio</strong>
        <p><em>Live color picker with adaptive WCAG luminance computation ensuring high readability across all UI elements.</em></p>
      </td>
    </tr>
  </table>
</div>

<br/>

<div align="center">
  <h3>Theme Presets & Dynamic Palette Gallery</h3>
  <table>
    <tr>
      <td width="50%" align="center">
        <a href="imgs/anki%20full%20black.png">
          <img src="imgs/anki%20full%20black.png" alt="AMOLED Void Black Theme" width="100%" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);" />
        </a>
        <br/>
        <strong>AMOLED Void Black (#000000)</strong>
        <p><em>True OLED black background with crisp white typography for zero eye fatigue and maximum power efficiency.</em></p>
      </td>
      <td width="50%" align="center">
        <a href="imgs/blue%20background.png">
          <img src="imgs/blue%20background.png" alt="Sapphire Blue Theme" width="100%" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);" />
        </a>
        <br/>
        <strong>Sapphire Blue Theme</strong>
        <p><em>Deep navy blue backdrop designed for high focus, coding sessions, and prolonged late-night study routines.</em></p>
      </td>
    </tr>
    <tr>
      <td width="50%" align="center">
        <a href="imgs/purple%20backgroud.png">
          <img src="imgs/purple%20backgroud.png" alt="Cosmic Purple Theme" width="100%" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);" />
        </a>
        <br/>
        <strong>Cosmic Purple Theme</strong>
        <p><em>Rich violet aesthetic providing a modern, vibrant ambiance with automatic luminance compensation.</em></p>
      </td>
      <td width="50%" align="center">
        <a href="imgs/white%20background.png">
          <img src="imgs/white%20background.png" alt="Arctic White Light Theme" width="100%" style="border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);" />
        </a>
        <br/>
        <strong>Arctic White Theme</strong>
        <p><em>Clean high-luminance theme with automatic dark text and borders calculated via WCAG contrast standards.</em></p>
      </td>
    </tr>
  </table>
</div>

---

## Key Architectural Features

### 1. Automated Discord Image Ingestion Pipeline
- **Zero-Friction Ingestion**: Post an image into any whitelisted Discord channel; the add-on fetches the attachment, transcodes the media, and builds the card in your specified deck.
- **Configurable Card Layout Modes**:
  - **Image Front Only (Visual Recognition)**: The image occupies the front face with an empty back. Designed for active recall drills such as medical histology, radiology, and anatomical recognition.
  - **Image Front / Caption Back**: Discord attachment is placed on the front; message captions or annotations are rendered on the reverse side.
  - **Question Front / Image Back**: Discord message text serves as the question prompt, revealing the diagram upon card flip.
- **On-Demand Backfill Synchronization**: Click **Pull Recent Discord Images Now** to retroactively synchronize the last 50 channel attachments without requiring real-time bot connectivity.

### 2. In-Memory WebP Image Optimizer
- **Storage and Bandwidth Optimization**: High-resolution 4K and 8K diagrams are clamped to a maximum bounding box (default: 1920px) and converted into the modern **WebP** container format at 85% quality.
- **Zero Intermediate Disk I/O**: The entire transcoding and compression pipeline executes within memory buffers (`io.BytesIO`) using Pillow before committing directly to Anki's `collection.media`. This reduces local disk writes and prevents synchronization bottlenecks on AnkiWeb, AnkiMobile (iOS), and AnkiDroid.

### 3. Cryptographic Anti-Duplication Engine
- **Binary Content Hashing**: Employs SHA-256 digests computed over raw image byte streams rather than relying on mutable Discord URLs or file names.
- **Persistent Message Tracking**: Retains an indexed registry of processed Discord message IDs and binary content hashes (`data/processed_messages.json`), guaranteeing that duplicate posts or backfill operations never create redundant flashcards.

### 4. AMOLED Void Black Theme and Dynamic RGB Studio
- **Pure Black Interface (#000000)**: Eliminates gray backdrops across Qt widgets, the Deck Browser, Card Reviewer, and Bottom Action Bars, minimizing OLED power consumption and reducing visual fatigue.
- **Dynamic WCAG Contrast Engine**: Calculates the relative luminance ($L = 0.2126R + 0.7152G + 0.0722B$) of user-selected theme colors in real time. Text, borders, and selection indicators automatically adjust between light and dark tones to ensure maximum contrast and accessibility.
- **Instant Hotkey Toggle**: Switch between custom styling and standard Anki presentation using `Ctrl+Shift+B`.

<div align="center">
  <a href="imgs/rgb%20color%20background%20selector.png">
    <img src="imgs/rgb%20color%20background%20selector.png" alt="Dynamic RGB Studio and WCAG Contrast Engine" width="85%" style="border-radius: 10px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 8px 24px rgba(0,0,0,0.7);" />
  </a>
  <p><em>Figure 2: Dynamic RGB Color Studio - Real-time color wheel, hex input, and automated contrast adaptation.</em></p>
</div>

### 5. Embedded HTTP REST Webhook Bridge
- **Local Integration Endpoint**: Runs a lightweight, non-blocking HTTP server on `http://127.0.0.1:8765`.
- **Cross-Application Interoperability**: Ingest flashcards or image URLs from terminal commands, shell scripts, Raycast workflows, Obsidian notes, Alfred triggers, or browser extensions.

### 6. Rule-Based Hierarchical Deck Routing
- **Pattern Matching**: Automatically directs incoming notes to nested decks (`Parent::Child`) based on tag matching (`#pathology` to `Medicine::Pathology`) or keyword matching in the note body.

### 7. Asynchronous Thread-Safe Worker
- **Non-Blocking Architecture**: Background operations (network retrieval, image processing, polling) execute on isolated worker threads with a persistent FIFO queue (`data/queue.json`).
- **Safe Main Thread Dispatching**: Flashcard creation and UI updates are scheduled onto Anki's main Qt event loop using Qt signal-slot adapters, preventing GUI freezing and database locking.

---

## System Architecture & Data Flow

The project adheres to Clean Architecture and SOLID design principles. Network communication, media transcoding, data persistence, and UI presentation are strictly decoupled.

```text
[Discord Channel / Bot API]      [Local HTTP REST: 8765]      [On-Demand Sync Action]
           │                                │                           │
           └────────────────────────────────┼───────────────────────────┘
                                            ▼
                              [Security & Authentication]
                          (Channel Whitelist & Rate Limiting)
                                            ▼
                                     [Discord Bridge]
                       (Attachment Extraction & Command Parser)
                                            ▼
                              [In-Memory Media Optimizer]
                       (Pillow WebP Transcoding & 1920px Resize)
                                            ▼
                              [Anti-Duplication Registry]
                           (SHA-256 Binary Content Hashing)
                                            ▼
                               [Persistent FIFO Queue]
                            (data/queue.json Backed Store)
                                            ▼
                               [Background Sync Worker]
                            (Asynchronous Retry Execution)
                                            ▼
                              [Smart Deck Routing Engine]
                            (Tag & Keyword Hierarchy Rules)
                                            ▼
                                [Qt Main-Thread Adapter]
                         (Thread-Safe Dispatch to mw.col API)
                                            ▼
                                   [Anki SQLite DB]
```

### Module Overview

| Package | Path | Responsibility |
|---|---|---|
| **Core** | `anki-addon/core/` | Configuration manager, Event Bus, logging subsystems, custom exceptions, and system interfaces. |
| **Discord** | `anki-addon/discord/` | Discord REST polling client, embedded HTTP server, message parser, command router, and payload models. |
| **Anki Interface** | `anki-addon/anki/` | In-memory media transcoding, note creation factory, deck hierarchy resolution, and safe collection operations. |
| **Synchronization** | `anki-addon/sync/` | Thread-safe FIFO queue, exponential retry handler, SHA-256 anti-duplication registry, and background worker. |
| **Routing** | `anki-addon/routing/` | Tag-based and keyword-based deck routing engine with hierarchical resolution. |
| **Theme Engine** | `anki-addon/theme/` | AMOLED `#000000` QSS stylesheets, WCAG contrast calculations, and WebView dark CSS injection. |
| **UI Components** | `anki-addon/ui/` | PyQt dialogs for Discord configuration, Routing rules, Theme Studio, Sync Monitor, and About views. |

---

## Installation & Quick Start

### Step 1: Install the Add-on
1. Download the latest `.ankiaddon` package from the [Releases](https://github.com/Andr3wGustavo/anki-wykiati-addon/releases) page, or build it locally using `python package_addon.py`.
2. In Anki, open **Tools -> Add-ons** (`Ctrl+Shift+A`).
3. Click **Install from file...** and select `anki-discord-toolkit.ankiaddon`.
4. Restart Anki to initialize the add-on subsystem.

### Step 2: Configure the Discord Bot
1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications) and create a New Application.
2. Under the **Bot** section, generate a **Bot Token**.
3. Under **Privileged Gateway Intents**, enable **Message Content Intent**.
4. Invite the bot to your target Discord server with `Read Messages/View Channels` and `Read Message History` permissions.
5. In Anki, navigate to **Tools -> Anki Wykiati Toolkit -> Discord & Image Settings...**:
   - Enter your **Bot Token**.
   - Specify the **Channel ID** to monitor (e.g., `119283746509182736`).
   - Select your target deck (e.g., `Medicine::Anatomy`).
   - Select your preferred layout mode (e.g., *Image on Front Only*).
6. Click **Save Settings**. Click **Pull Recent Discord Images Now** to verify connectivity and immediately backfill past attachments.

<div align="center">
  <a href="imgs/discord%20and%20image%20settings.png">
    <img src="imgs/discord%20and%20image%20settings.png" alt="Discord and Image Settings Dialog" width="85%" style="border-radius: 10px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 8px 24px rgba(0,0,0,0.7);" />
  </a>
  <p><em>Figure 3: Discord & Image Settings - Seamless channel listening, target deck routing, and layout controls.</em></p>
</div>

### Step 3: Customize Theme & Background Colors
1. In Anki, navigate to **Tools -> Anki Wykiati Toolkit -> Theme Settings...** or press `Ctrl+Shift+B`.
2. Select any background color via the interactive RGB color wheel or input a custom hex code:
   - **AMOLED Void Black**: `#000000` (Max OLED battery savings, zero distraction)
   - **Sapphire Blue**: `#0A192F` (Deep focus mode for programming and long study hours)
   - **Cosmic Purple**: `#1E1035` (Modern vibrant ambiance with adaptive contrast)
   - **Arctic White**: `#FFFFFF` (High-luminance clean light theme with auto-inverted dark typography)
3. The integrated WCAG luminance engine automatically calculates contrast and applies matching fonts, borders, and reviewer styles instantly.

---

## Discord Ingestion & Command Syntax

### 1. Automated Media Channel Ingestion
When an image is uploaded to a configured channel, the add-on processes the media attachment automatically according to your chosen layout mode. No command prefix is required.

### 2. Structured Card Commands
To create text-based or cloze flashcards directly from Discord chat, use the `!anki` command syntax:

#### Standard Q&A Card
```text
!anki
front: What is the primary function of the mitochondria?
back: Cellular respiration and adenosine triphosphate (ATP) synthesis.
deck: Biology::Cellular
tags: biology, cytology, exam-prep
```

#### Cloze Deletion Card
```text
!anki
front: The {{c1::TCP}} protocol provides reliable ordered delivery, while {{c2::UDP}} minimizes latency.
deck: Computer Science::Networking
tags: networking, transport-layer
```

### 3. Utility Bot Commands
| Command | Function |
|---|---|
| `!anki-help` | Outputs syntax instructions, formatting rules, and supported field templates. |
| `!anki-status` | Returns system uptime, active theme configuration, queue size, and processed card totals. |
| `!anki-decks` | Returns a list of all decks and subdecks present in the active Anki collection. |
| `!anki-ping` | Performs a low-latency heartbeat check against the running Anki desktop instance. |

---

## Local HTTP Webhook API

The integrated HTTP REST bridge runs locally on `127.0.0.1:8765`, enabling scriptable card ingestion from any programming language or workflow manager.

### Ingest a Standard Flashcard (JSON POST)

**Endpoint**: `POST http://127.0.0.1:8765/api/card`

```bash
curl -X POST http://127.0.0.1:8765/api/card \
  -H "Content-Type: application/json" \
  -d '{
    "front": "What is the time complexity of QuickSort in the average case?",
    "back": "O(n log n)",
    "deck": "Computer Science::Algorithms",
    "tags": ["dsa", "sorting"]
  }'
```

### Ingest an Image from a Remote URL

**Endpoint**: `POST http://127.0.0.1:8765/api/card`

```bash
curl -X POST http://127.0.0.1:8765/api/card \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/cardiac_conduction_system.png",
    "caption": "Cardiac Conduction System - SA Node to Purkinje Fibers",
    "deck": "Medicine::Cardiology",
    "tags": ["cardiology", "electrophysiology"]
  }'
```

### Health Check

**Endpoint**: `GET http://127.0.0.1:8765/health`

```bash
curl http://127.0.0.1:8765/health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "queue_size": 0
}
```

---

## Configuration Reference

All settings can be adjusted via GUI dialogs under **Tools -> Anki Wykiati Toolkit** or edited directly in `anki-addon/config.json`:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `addon_enabled` | `boolean` | `true` | Master switch enabling or disabling all add-on background routines. |
| `theme.enabled` | `boolean` | `true` | Activates the custom AMOLED and Liquid Glass design system. |
| `theme.background` | `string` | `"#000000"` | Hexadecimal background color (`#000000` for OLED black or custom RGB). |
| `theme.accent` | `string` | `"#0A84FF"` | Accent color used for buttons, active focus outlines, and indicator badges. |
| `theme.apply_to_webviews` | `boolean` | `true` | Injects dark CSS stylesheets into Anki webviews (reviewer and deck browser). |
| `theme.pure_black_reviewer` | `boolean` | `true` | Enforces true `#000000` background during card review sessions. |
| `discord.enabled` | `boolean` | `false` | Enables background Discord polling and webhook ingestion. |
| `discord.bot_token` | `string` | `""` | Authentication token for the Discord Bot Application. |
| `discord.image_channels` | `list[str]` | `[]` | Array of channel IDs monitored for automated image attachment ingestion. |
| `discord.image_default_deck` | `string` | `"Images::Discord"` | Default target deck for ingested images when no routing rules match. |
| `discord.image_card_layout` | `string` | `"image_front"` | Layout format: `"image_only_front"`, `"image_front"`, or `"image_back"`. |
| `discord.optimize_images` | `boolean` | `true` | Enables in-memory WebP compression and dimension downscaling. |
| `discord.max_image_dimension` | `integer` | `1920` | Maximum pixel width or height before automatic downscaling is applied. |
| `discord.image_quality` | `integer` | `85` | WebP compression quality level (1 to 100). |
| `discord.convert_to_webp` | `boolean` | `true` | Converts incoming PNG and JPEG attachments to the WebP container. |
| `discord.http_bridge_enabled` | `boolean` | `true` | Launches the local HTTP REST Webhook server. |
| `discord.http_bridge_port` | `integer` | `8765` | Port number bound by the local HTTP server (`127.0.0.1:8765`). |
| `anki.default_deck` | `string` | `"Default"` | Fallback deck assignment when no routing rule or metadata matches. |

---

## Testing & Developer Tooling

The repository includes a headless unit test suite and a Windows developer control console.

### Automated Unit Test Suite
Execute the full test suite in headless mode with mock Anki environment isolation:

```bash
python -m unittest discover -s anki-addon/tests -p "test_*.py" -v
```

### Windows Developer Console (`test_addon.bat`)
Run the interactive batch utility to manage local testing and deployment:

```cmd
test_addon.bat
```

- **[1] Run Unit Tests**: Executes all test suites with verbose output.
- **[2] Build Package (.ankiaddon)**: Packages a clean distribution archive in `release/`.
- **[3] Start HTTP Bridge**: Runs the standalone HTTP bridge server on port 8765.
- **[4] Send Test Card**: Dispatches a test card payload to the local webhook.
- **[5] Clean Reinstall to Anki**: Copies the current codebase to `%APPDATA%\Anki2\addons21\`.
- **[6] Open HTML Preview**: Renders the webview theme preview in default browser (`preview.html`).
- **[7] Launch Qt UI Preview**: Opens a standalone PyQt desktop window (`preview_ui.py`).

### Building Release Package for AnkiWeb

To generate the `.ankiaddon` distribution file:

```bash
python package_addon.py
```

The script removes build caches, compiled bytecode (`.pyc`), and runtime logs, producing the final archive at:
`release/anki-discord-toolkit.ankiaddon`

For detailed AnkiWeb submission requirements, refer to [docs/ANKIWEB_PUBLISHING_GUIDE.md](docs/ANKIWEB_PUBLISHING_GUIDE.md).

---

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| **Discord images not importing** | Missing **Message Content Intent** in Discord Developer Portal. | Go to [Discord Developer Portal](https://discord.com/developers/applications) -> Bot -> Enable **Message Content Intent**. |
| **HTTP Bridge port conflict (8765)** | Another service (or AnkiConnect) is bound to port 8765. | Change `discord.http_bridge_port` in `config.json` to an alternate port (e.g., `8766`). |
| **WebP conversion failure** | Pillow library missing from Python environment. | Ensure Pillow is installed via `pip install Pillow` (bundled automatically in packaged release). |
| **Theme not applying to reviewer** | Anki WebView caching old stylesheet. | Toggle the theme off and on using `Ctrl+Shift+B` or restart Anki. |
| **Duplicate cards ignored** | Content hash already present in registry. | The add-on protects against duplicate uploads. Clear `data/processed_messages.json` if re-import is required. |

---

## Technical Specifications

- **Target Ecosystem**: Anki 2.1.50+ / 23.10+ / 24.04+ (PyQt5 and PyQt6 compatible).
- **Python Compatibility**: Python 3.9, 3.10, 3.11, 3.12.
- **Supported Operating Systems**: Windows 10/11, macOS (Intel & Apple Silicon), Linux.
- **Repository**: [github.com/Andr3wGustavo/anki-wykiati-addon](https://github.com/Andr3wGustavo/anki-wykiati-addon)
- **Issue Tracker**: [github.com/Andr3wGustavo/anki-wykiati-addon/issues](https://github.com/Andr3wGustavo/anki-wykiati-addon/issues)
- **License**: MIT License ([LICENSE](LICENSE))

---

## Support & Sponsorship

If the **Anki Wykiati Toolkit** accelerates your study workflow, improves your flashcard retention, or enhances your daily review experience, consider supporting ongoing development:

<div align="center">
  <a href="https://buymeacoffee.com/wykiati" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="220" style="border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.3);" />
  </a>
  <br/><br/>
  <p>
    <strong>Direct Link:</strong> <a href="https://buymeacoffee.com/wykiati" target="_blank">https://buymeacoffee.com/wykiati</a>
  </p>
  <p><em>Direct contributions support the implementation of future features including Image Occlusion generation, offline OCR pipelines, and continuous maintenance on AnkiWeb.</em></p>
</div>
