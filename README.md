# Anki Wykiati Add-on (Anki Discord Toolkit)

A modular, production-grade Anki add-on providing automated flashcard creation from Discord channels and webhooks, featuring dedicated image channel auto-ingestion and an iOS-inspired Liquid Glass (Frosted Glassmorphism) theme with AMOLED black support.

---

## Table of Contents

1. [Overview and Key Features](#1-overview-and-key-features)
2. [Architecture and Data Flow](#2-architecture-and-data-flow)
3. [Discord Image Ingestion Pipeline](#3-discord-image-ingestion-pipeline)
4. [iOS Liquid Glass Visual Theme](#4-ios-liquid-glass-visual-theme)
5. [Discord Protocol and Commands](#5-discord-protocol-and-commands)
6. [Local HTTP Webhook Bridge](#6-local-http-webhook-bridge)
7. [Step-by-Step Testing Guide](#7-step-by-step-testing-guide)
8. [Installation and Distribution](#8-installation-and-distribution)
9. [Configuration Reference](#9-configuration-reference)
10. [Repository and Contribution](#10-repository-and-contribution)

---

## 1. Overview and Key Features

The Anki Wykiati Add-on connects Discord workflows with Anki collections:

- **Automated Image Channel Ingestion**: Point the add-on to a dedicated Discord channel that receives filtered images. Every image attachment is automatically downloaded, saved to Anki's media storage, and converted into an Anki note in your chosen deck without requiring manual triggers.
- **iOS Liquid Glass Theme**: Translucent frosted glassmorphism styling (`rgba(20, 22, 28, 0.75)` with subtle glass highlights and rounded modern buttons) over an AMOLED `#000000` base for high contrast and visual comfort.
- **Asynchronous Non-Blocking Queue**: Background daemon worker processes jobs and synchronizes notes onto Anki's main thread safely without freezing the user interface.
- **Cryptographic Anti-Duplication**: SHA-256 binary content and message fingerprinting prevents re-importing duplicate cards or images.
- **Smart Deck Routing**: Route notes dynamically based on message tags, keywords, or channel defaults.
- **Cloze Deletion Auto-Detection**: Automatically recognizes `{{c1::...}}` patterns and selects the Cloze note type.
- **Local HTTP Bridge Server**: Built-in REST API on `http://127.0.0.1:8765/api/card` for external scripts, browser extensions, and developer tools.

---

## 2. Architecture and Data Flow

The codebase is organized in decoupled layers following SOLID principles and Clean Architecture:

```text
  [Discord Bot REST Poller]        [Local HTTP Webhook]
             │                              │
             └──────────────┬───────────────┘
                            ▼
                [Authorization Policy]
            (Channel & User Whitelist, Rate Limit)
                            ▼
                    [Discord Bridge]
      (Detects Image Attachments vs. !anki Protocol)
                            ▼
             [Media Manager / Ingestion]
        (Downloads, Hashes SHA-256, Saves Media)
                            ▼
             [Anti-Duplication Registry]
            (Checks Duplicate Fingerprints)
                            ▼
             [Persistent FIFO Job Queue]
              (Disk-backed in data/queue.json)
                            ▼
               [Background Sync Worker]
                (Async Polling & Retry Loop)
                            ▼
              [Smart Deck Routing Engine]
            (Tag & Keyword Hierarchical Rules)
                            ▼
               [Anki Note & Deck Adapter]
            (Dispatched safely to Main GUI Thread)
                            ▼
                 [Anki Collection DB]
```

### Key Modules:
- `anki/media.py`: Handles downloading binary image data, computing SHA-256 hashes, and writing files directly to `mw.col.media`.
- `anki/notes.py` & `anki/decks.py`: Manages safe creation of notes and nested deck structures (`Parent::Child`).
- `discord/bridge.py`: Routes incoming messages and attachments to either image ingestion or structured parsing.
- `discord/client.py`: Dual-mode client with an embedded HTTP server and lightweight Discord REST poller.
- `theme/styles.py` & `theme/palette.py`: Generates iOS Liquid Glass QSS for Qt widgets and CSS for Anki webviews.
- `sync/queue.py` & `sync/worker.py`: Thread-safe persistent FIFO queue with automatic retries.

---

## 3. Discord Image Ingestion Pipeline

The primary use case is ingesting images from a dedicated Discord channel into an Anki deck:

1. In Anki, open **Tools -> Anki Discord Toolkit -> Discord Settings**.
2. Enter the channel ID in **Image Channels (IDs)** (e.g., `123456789012345678`).
3. Set your target deck in **Deck for Images** (e.g., `Images::Anatomy` or `Wykiati::Deck`).
4. Select card layout:
   - **Image on Front / Caption on Back** (Default): The downloaded image `<img src="discord_xxxx.png">` is placed on the front; message caption or text is placed on the back.
   - **Question on Front / Image on Back**: Text is placed on the front; image is placed on the back.
5. Save settings. Whenever an image is posted in the configured channel, the add-on automatically pulls the image into your Anki collection.

---

## 4. iOS Liquid Glass Visual Theme

The visual design is inspired by modern iOS frosted glassmorphism:

- **Backdrop**: AMOLED Pure Black `#000000`.
- **Glass Surfaces**: Translucent dark surfaces `rgba(18, 20, 26, 0.75)` with subtle borders `1px solid rgba(255, 255, 255, 0.14)`.
- **Glass Buttons**: Translucent rounded buttons with interactive hover highlights and active states.
- **Capsule Tabs and Inputs**: Floating glass capsules and soft dark inputs with focus borders.
- **Webviews**: Card review screens and deck browsers receive matching frosted glass containers and typography.
- **Shortcut**: Toggle the theme instantly inside Anki using `Ctrl+Shift+B`.

---

## 5. Discord Protocol and Commands

### Structured `!anki` Message Format:
```text
!anki
front: What is a Docker container?
back: A standardized unit of software that packages code and dependencies together.
deck: DevOps::Docker
tags: docker, containers, devops
```

### Cloze Deletion Example:
```text
!anki
front: The {{c1::TCP}} protocol provides reliable ordered delivery, while {{c2::UDP}} prioritizes low latency.
deck: Computer Science::Networking
tags: networking, protocols
```

### Operational Commands:
- `!anki-help`: Displays formatted usage instructions.
- `!anki-status`: Shows system status, theme state, and synchronization metrics.
- `!anki-decks`: Lists all decks available in the collection.
- `!anki-ping`: Tests add-on bridge connectivity.

---

## 6. Local HTTP Webhook Bridge

You can post cards and images directly from any programming language or tool:

### Text Card Creation (JSON POST):
```bash
curl -X POST http://127.0.0.1:8765/api/card \
  -H "Content-Type: application/json" \
  -d '{
    "front": "What is the time complexity of binary search?",
    "back": "O(log n) in sorted arrays.",
    "deck": "Computer Science::Algorithms",
    "tags": ["dsa", "algorithms"]
  }'
```

### Direct Image Ingestion (JSON POST):
```bash
curl -X POST http://127.0.0.1:8765/api/card \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/diagram.png",
    "caption": "Heart Blood Flow Diagram",
    "deck": "Medicine::Cardiology"
  }'
```

### Server Health Check:
```bash
curl http://127.0.0.1:8765/health
```

---

## 7. Step-by-Step Testing Guide

### Method A: Automated Test Suite (Windows Batch)
Double-click `test_addon.bat` in the root folder or execute it from the command line:

```cmd
test_addon.bat
```

Select:
- **[1]** to run all 38 automated unit tests.
- **[2]** to build the `.ankiaddon` package in the `release/` directory.
- **[3]** to start the standalone local HTTP bridge server for manual webhook testing.
- **[4]** to send a test flashcard via PowerShell.
- **[5]** to install the add-on directly into your local Anki installation directory.

### Method B: Running Tests via Terminal
```bash
python -m unittest discover -s anki-addon/tests -p "test_*.py" -v
```

All 38 test cases will execute in headless mode without requiring an active Anki GUI.

---

## 8. Installation and Distribution

### Option 1: Package and Install (.ankiaddon)
1. Run `python package_addon.py` to create `release/anki-discord-toolkit.ankiaddon`.
2. Open Anki and navigate to: **Tools -> Add-ons** (`Ctrl+Shift+A`).
3. Click **Install from file...** and select the `.ankiaddon` file.
4. Restart Anki.

### Option 2: Direct Directory Link (Windows)
Copy the `anki-addon` folder to `%APPDATA%\Anki2\addons21\anki_discord_toolkit` and restart Anki.

---

## 9. Configuration Reference

All settings can be customized through the GUI dialogs or directly in `config.json`:

| Setting Path | Type | Default | Description |
|---|---|---|---|
| `theme.enabled` | boolean | `true` | Enables or disables the visual theme |
| `theme.style_variant` | string | `"liquid_glass"` | Theme aesthetic (`"liquid_glass"` or `"pure_black"`) |
| `theme.accent` | string | `"#0A84FF"` | Accent color hex code |
| `discord.enabled` | boolean | `false` | Enables the Discord Bot polling worker |
| `discord.bot_token` | string | `""` | Discord Bot secret token |
| `discord.image_channels` | list | `[]` | Channel IDs where every image is automatically ingested |
| `discord.image_default_deck` | string | `"Images::Discord"` | Target deck for automatically ingested images |
| `discord.image_card_layout` | string | `"image_front"` | Layout mode (`"image_front"` or `"image_back"`) |
| `discord.channel_ids` | list | `[]` | Channels allowed for `!anki` commands |
| `discord.http_bridge_enabled` | boolean | `true` | Starts the local HTTP REST server |
| `discord.http_bridge_port` | integer | `8765` | Local HTTP server port |
| `anki.default_deck` | string | `"Default"` | Fallback deck for cards without deck specification |

---

## 10. Repository and Contribution

- Repository URL: `git@github.com:Andr3wGustavo/anki-wykiati-addon.git`
- License: [MIT License](LICENSE)
