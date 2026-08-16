# Design System & UI Architecture

> **Aesthetic Philosophy:** Minimalist, developer-grade interface design inspired by *Linear*, *Vercel*, and *Apple Pro Dark Mode*, combined with 100% native Anki desktop layout harmony.

---

## 1. Core Visual Tokens & Palette

The design system is built upon high-contrast Void Black base canvases, translucent glass overlays, and crisp typography.

```text
┌───────────────────────────────────────────────────────────┐
│ Token                     Hex / RGBA            Usage     │
├───────────────────────────────────────────────────────────┤
│ --canvas                  #000000               Void Base │
│ --surface-glass           rgba(255,255,255,0.03) Cards    │
│ --surface-elevated        rgba(255,255,255,0.06) Hover    │
│ --border-subtle           rgba(255,255,255,0.08) Dividers │
│ --border-focus            rgba(255,255,255,0.35) Focus    │
│ --text-primary            #FFFFFF               Headings  │
│ --text-secondary          #D4D4D8               Body Text │
│ --text-muted              #A1A1AA               Captions  │
│ --accent-blue             #0A84FF               iOS Blue  │
│ --accent-cyan             #38BDF8               Highlight │
│ --success-green           #30D158               Ingested  │
│ --warning-amber           #FF9F0A               Pending   │
│ --error-crimson           #FF453A               Failure   │
└───────────────────────────────────────────────────────────┘
```

---

## 2. Dialog Geometry & Responsive Layout Engine

To ensure modal dialogs feel unified with Anki's native Preferences and Add-on manager:

1. **Standardized Dimensions:**
   - Default Geometry: `width: 580px`, `height: 460px`.
   - Minimum Dimensions: `width: 440px`, `height: 320px`.
   - Dynamic Resizing: Enabled via `setSizeGripEnabled(True)` to adapt to smaller screens and ultrawide displays.

2. **Vertical-Only Scrollbar Engine:**
   - **Horizontal Scrolling Disabled:** `setHorizontalScrollBarPolicy(ScrollBarAlwaysOff)` prevents awkward horizontal shifting.
   - **Vertical Scrolling Dynamic:** `setVerticalScrollBarPolicy(ScrollBarAsNeeded)` displays a sleek 6px dark scrollbar only when content overflows.
   - **Scrollbar Styling:** Transparent track with rounded translucent thumb (`rgba(255, 255, 255, 0.18)`), expanding on hover to `rgba(255, 255, 255, 0.35)`.

3. **Subtle Window Transparency & Frosted Glass:**
   - Utilizes `Qt.WidgetAttribute.WA_StyledBackground` and background layers `rgba(10, 10, 14, 0.96)`.
   - Window borders use a hairline glass stroke `1px solid rgba(255, 255, 255, 0.10)`.

---

## 3. Button System & Controls

All interactive elements adhere to Anki's native proportions while featuring subtle glass aesthetics:

```text
  [ Secondary Glass Button ]           [ Primary Contrast Action ]
  ┌────────────────────────┐           ┌─────────────────────────┐
  │ Cancel                 │           │ Save Changes            │
  └────────────────────────┘           └─────────────────────────┘
  • background: rgba(255,255,255,0.05) • background: #FFFFFF
  • border: 1px rgba(255,255,255,0.12) • border: 1px #FFFFFF
  • color: #E4E4E7                     • color: #000000
  • border-radius: 6px                 • border-radius: 6px
  • font-weight: 500                   • font-weight: 600
```

### Form Inputs & Text Fields:
- Dark recessed background (`#060608`).
- Subtly rounded corners (`border-radius: 6px`).
- Monospaced typography for tokens, IDs, and ports (`font-family: 'JetBrains Mono', Consolas, monospace`).
- High-contrast focused state (`border: 1px solid rgba(255, 255, 255, 0.35)`).

---

## 4. Simplified, Didactic Theme Studio

To maximize clarity and eliminate visual clutter:
- **No Cluttered Preset Grids:** Removed oversized color tiles in favor of a clean, focused control panel.
- **Interactive RGB Wheel Widget:** Conical color gradient with radial dark overlay. Clicking or dragging dynamically computes Hue, Saturation, and Value (`HSV`) in real time.
- **Direct Hex Input with Live Swatch:** Instant bidirectional synchronization between text and color spectrum.
- **Live Flashcard Preview Card:** Demonstrates canvas background and active accent styling instantly.

---

## 5. Modern Flashcard CSS Templates (Zoom on Hover)

To give flashcards an ultra-premium aesthetic:
```css
/* Card Container */
.card {
    background-color: var(--canvas, #000000) !important;
    color: #FFFFFF !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    text-align: center;
    padding: 24px;
}

/* Image Flashcards with Smooth Zoom on Hover */
.card img {
    max-width: 95%;
    max-height: 500px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.10);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.9);
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease;
    cursor: zoom-in;
}

.card img:hover {
    transform: scale(1.03);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 1.0);
    border-color: rgba(255, 255, 255, 0.25);
}
```
