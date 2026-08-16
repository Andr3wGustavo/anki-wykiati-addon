# Performance Optimization, Reliability & Logging Architecture

> **Engineering Standards:** Robust error handling, non-blocking asynchronous execution, zero-lag rendering, and centralized telemetry logging.

---

## 1. Centralized Rotating Logging Architecture

All errors, warnings, background sync cycles, and API requests are logged to `anki_wykiati_toolkit.log` under the add-on root directory.

### Key Architecture Components:
- **`RotatingFileHandler` Enforcement:**
  - Maximum File Size: **2 MB**.
  - Backup Count: **3 files** (`anki_wykiati_toolkit.log`, `.log.1`, `.log.2`).
  - Guarantees disk usage never grows indefinitely.
- **Traceback & Diagnostic Inspection:**
  - `logger.log_exception(exc, context="Component")` captures the complete Python stack trace.
  - `logger.read_recent_logs(max_lines=50)` allows the add-on and developer scripts to inspect runtime state prior to performing auto-repair or schema migration.

```text
[2026-08-16 13:00:01][AWT][INFO] [ThemeEngine] Theme activated (bg=#000000, accent=#0A84FF).
[2026-08-16 13:00:02][AWT][INFO] [SyncWorker] Background sync worker started.
[2026-08-16 13:00:02][AWT][INFO] [HttpBridgeServer] Listening on http://127.0.0.1:8765
[2026-08-16 13:00:15][AWT][INFO] [JobQueue] Enqueued Job 'a1bf2907' for deck 'Medicine::Anatomy'
```

---

## 2. Zero-Lag Hardware Accelerated Rendering

### CSS & Qt Optimization:
1. **GPU Layer Promotion:** WebViews use `translateZ(0)` to promote flashcard reviewer elements to dedicated compositor layers.
2. **Repaint Minimization:** Avoid expensive CSS filters like heavy `backdrop-filter: blur()`, which can induce frame drops during rapid card grading.
3. **Smooth Scroll Performance:** Native QScrollArea utilizes `setWidgetResizable(True)` without custom event loop overhead.

---

## 3. Asynchronous Thread Safety & Concurrency

Anki's collection database (`mw.col`) is strictly thread-affine and cannot be manipulated from background worker threads directly.

### Data Flow & Thread Synchronization:
```text
  [ Discord Bot Poller ] ──(Async Worker Thread)──> [ FIFO Job Queue ]
                                                           │
                                                           ▼ (Safe Queue Write)
                                                    [ data/queue.json ]
                                                           │
                                                           ▼ (Dispatched via QueryOp / main_thread)
                                                 [ Anki Note Adapter ]
                                                           │
                                                           ▼ (Main GUI Thread)
                                                 [ mw.col.add_note() ]
```

1. Background workers download images, compute SHA-256 hashes, and append jobs to disk.
2. Collection modifications are dispatched safely to Anki's main thread via `aqt.operations.QueryOp` or `mw.taskman.run_on_main()`.
3. If the database is locked during a review sync, the worker backs off exponentially without crashing the user interface.

---

## 4. Cryptographic Anti-Duplication Engine

To prevent accidental card re-creation when re-scanning Discord message history:
1. **Message ID Registry:** Tracks processed Discord snowflake IDs (`msg_123456789`).
2. **Binary Content Hash:** Computes SHA-256 digest of downloaded media files.
3. **Persistent Registry:** Stored in `data/processed_messages.json` with self-healing fallback if JSON corruption is detected.

---

## 5. Cross-Platform Compatibility Matrix

| Environment | Supported Versions | Status |
|---|---|---|
| **Operating Systems** | Windows 10/11, macOS (Intel & Apple Silicon), Linux (X11 & Wayland) | Verified |
| **Anki Core** | Anki 2.1.50+ up to Anki 26.x | Verified |
| **Python Runtimes** | Python 3.9, 3.10, 3.11, 3.12, 3.13 | Verified |
| **Qt Toolkits** | PyQt5, PyQt6, PySide6, aqt.qt | Verified |
