# Anki Wykiati Add-on — Architecture, Design Preview, and Feature Roadmap

This document consolidates the technical architecture, design verification mechanisms, and proposals for next-generation features, including the **Integrated Pomodoro Study Timer** and **WhatsApp Daily Flashcard Digest**.

---

## 1. Executive Summary & Current State

The **Anki Wykiati Add-on (Anki Discord Toolkit)** is a modular, production-ready extension for Anki Desktop that bridges study material from Discord and HTTP APIs into Anki collections.

### Core Capabilities Implemented:
1. **Automated Discord Image Ingestion**: Dedicated image channels automatically ingest every posted image attachment without requiring text commands.
2. **Cryptographic Anti-Duplication**: SHA-256 binary image and text fingerprinting prevents duplicate notes.
3. **Media Collection Management**: Images are downloaded, hashed, and stored directly into Anki's official media directory.
4. **iOS Liquid Glass Theme**: Translucent frosted glassmorphism surfaces (`rgba(18, 21, 28, 0.72)`), AMOLED black background (`#000000`), rounded glass buttons, and SF Pro typography.
5. **Asynchronous Non-Blocking Worker**: Background queue worker processes jobs without freezing Anki's GUI.
6. **Smart Deck Routing**: Route notes dynamically by tag or keyword rules into hierarchical decks (e.g., `Medicine::Cardiology`).
7. **Comprehensive Test Suite**: 38 automated unit tests with 100% pass rate.

---

## 2. How to Preview the iOS Liquid Glass Design

You can preview and interact with the design using three methods:

### Method A: Interactive Web Preview (`preview.html`)
- Open the file `preview.html` located in the root repository folder by double-clicking it or opening it in any web browser (Chrome, Edge, Safari, Firefox).
- **Features in preview**:
  - Live card reviewer showing the exact frosted glass card container, image layout, question, and answer toggle.
  - Interactive iOS glass review buttons (Again, Hard, Good, Easy) with smooth hover and active animations.
  - Working Pomodoro Timer Capsule with real-time countdown simulation.
  - Real-time operational metrics and image channel configuration sidebar.

### Method B: Standalone Native Qt Preview (`preview_ui.py`)
- If you have Python and PyQt6/PyQt5 installed, run:
  ```cmd
  python preview_ui.py
  ```
  or select option **[7]** in `test_addon.bat`. This opens the actual Qt desktop window with the active QSS theme.

### Method C: Live Inside Anki Desktop
- Install the add-on using option **[5]** in `test_addon.bat` or by installing `release/anki-discord-toolkit.ankiaddon`.
- Open Anki. Navigate to **Tools -> Anki Discord Toolkit -> Dashboard and Metrics** (`Ctrl+Shift+D`) or toggle the theme with `Ctrl+Shift+B`.

---

## 3. Proposal: Integrated Pomodoro & Study Session Timer

### Concept
A floating, unobtrusive iOS Liquid Glass pill widget embedded directly into Anki's Reviewer and Main Window that tracks study intervals, calculates retention vs. study time, and logs historical session data.

### Architecture & Data Model:
```text
┌────────────────────────────────────────────────────────┐
│                   POMODORO ENGINE                      │
│  - Configurable Work/Break (e.g. 25m work / 5m break)  │
│  - State Machine: IDLE -> RUNNING -> PAUSED -> BREAK   │
│  - Audio Notification on Interval Completion          │
└───────────────────────────┬────────────────────────────┘
                            │ On Interval Finished
                            ▼
┌────────────────────────────────────────────────────────┐
│                  STUDY SESSION STORE                   │
│  - Session ID, Deck ID, Start Time, Duration Seconds   │
│  - Cards Reviewed, Cards Retained, Focus Score         │
│  - Persisted in data/study_history.json & SQLite       │
└────────────────────────────────────────────────────────┘
```

### JSON Schema (`data/study_history.json`):
```json
{
  "sessions": [
    {
      "id": "session_20260815_01",
      "timestamp_start": 1786770000,
      "duration_seconds": 1500,
      "deck": "Medicine::Cardiology",
      "cards_reviewed": 35,
      "retention_rate": 0.88,
      "status": "COMPLETED"
    }
  ],
  "total_study_time_seconds": 54000,
  "current_streak_days": 12
}
```

### UI Integration:
- Floating glass capsule in the top-right corner of the Card Reviewer.
- Visual circular progress bar and pulse animations.
- Dashboard analytics tab showing:
  - Daily & Weekly study hours heat-map.
  - Retention rate correlated with session length.

---

## 4. Proposal: WhatsApp Daily Flashcard Digest & Mobile Study

### Concept
An automated daily notification service that delivers daily review summaries and interactive flashcard challenges directly to WhatsApp so you can review cards on your smartphone without opening Anki.

### Architecture:
```text
┌────────────────────────┐
│ Anki Scheduler & Stats │
│ (Cards due today, hard)│
└───────────┬────────────┘
            │ Daily Cron / Timer (e.g. 08:00 AM)
            ▼
┌────────────────────────┐
│ Digest Generator Engine│ ➔ Generates text summary + Top 5 hardest cards
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  WhatsApp Gateway API  │ ➔ Evolution API / Baileys / WPPConnect / Twilio
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│    User's WhatsApp     │ 📱 "Good morning! You have 42 cards due today."
└────────────────────────┘
```

### Key Capabilities:
1. **Morning Due Digest**:
   - Sends a summary: *"Good morning! You have 38 cards due today in Medicine::Cardiology. Current streak: 7 days."*
2. **Hardest Cards Mini-Quiz**:
   - Sends the 5 cards with the lowest ease factor or highest lapse rate.
   - User replies with "1" (Again), "2" (Hard), "3" (Good), "4" (Easy) to log remote reviews via webhook!
3. **Image Card Ingestion from WhatsApp**:
   - Forward images directly from WhatsApp to your personal Anki bot number; they get downloaded and added to your deck automatically.

---

## 5. Proposal: Automatic OCR & Image Occlusion Pipeline

### Concept
When an anatomy diagram or technical chart is uploaded to the Discord image channel:
1. Local lightweight OCR (e.g. `pytesseract` or ONNX model) detects text labels and coordinates within the diagram.
2. Automatically generates **Image Occlusion** masks over key terminology.
3. Produces multi-cloze flashcards where each label is hidden sequentially.

---

## 6. Implementation Roadmap & Milestones

| Milestone | Feature | Complexity | Estimated Effort |
|---|---|---|---|
| **Phase 1 (Completed)** | Image Ingestion Pipeline, Anti-Duplication, iOS Liquid Glass Theme | High | Complete |
| **Phase 2 (Next)** | Integrated Pomodoro Study Timer & Study Session History Table | Medium | 1-2 Days |
| **Phase 3** | WhatsApp Daily Digest Gateway & Evolution API Connector | High | 2-3 Days |
| **Phase 4** | Automated Image Occlusion and On-Device Label Masking | High | 3-4 Days |
| **Phase 5** | Whisper AI Voice-to-Card transcription for Discord audio notes | Medium | 1-2 Days |
