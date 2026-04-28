# CS2 Skin Browser — Design System

> An artist-friendly way to view Counter-Strike skin art.

**CS2 Skin Browser** (repo: `cs-skin-searcher`) is a desktop application that lets Counter-Strike skin artists browse the full library of existing CS2 weapon finishes **without the marketplace fluff**. No prices. No float values. No stickers, trade-ups, or inventory chrome. Just the skin, its identifying metadata, and a scrubbable preview of the in-game render — so artists can study reference, tag patterns, and find visual precedent without wading through a trading site.

---

## What the product does

**Browser** — a weapon-gridded wall of skin tiles (5 columns). A top bar filters by weapon type (All / AK-47 / AWP / …) and a text query searches across weapon name, skin name, and user-authored tags. Clicking a tile opens a detail view.

**Detail view** — one skin takes over the window. A large preview on the left plays through 10 sampled frames of the skin's showcase webm (via a slider). On the right: skin name, weapon, rarity, collection, and an editable tag list. Two external-launch buttons: open on **Steam Workshop** (browser) and **Inspect in-game** (via `steam://` URL).

**Tagger** — a dedicated modal for batch-tagging untagged skins. Same preview/scrubber UI, plus a progress bar through the untagged queue. Right-arrow key saves and advances.

---

## Sources provided

- **GitHub repo:** [EyesaiahOC/cs-skin-searcher](https://github.com/EyesaiahOC/cs-skin-searcher) (public, default branch `main`)
  - `application/` — the PySide6/Qt desktop app (`main.py`, `browser.py`, `skin_tile.py`, `tagger.py`, `utils.py`)
  - `application/ui_files/*.ui` — Qt Designer layouts (not imported here; the Python code pulls them at runtime)
  - `scripts/` — scraping + JSON generation pipeline (weapon-type enum, rarity enum, fetchers)
  - `raw_json/` — 1,321 skin records (name, weapon, rarity, collection, webm path, tags)
  - `webm/` — local preview clips (not in repo)
  - `webpages/` — cached `csgoskins.gg` HTML used as scrape source
- **Additional direction from user:** "Counter-Strike style minimalist modern looking UI."

No Figma, no brand guide, no logo yet (the maintainer will provide one later). The design language below is **reverse-engineered from the Qt stylesheet (`utils.py` `DARK_STYLE`), the splash screen painter (`main.py`), and the CS2 visual idiom** (rarity color ladder, monospaced mil-tech feel, dark chrome HUDs).

---

## Content fundamentals

The app has very little prose — it's a tool, not a site — but the copy it does have is consistent:

**Tone:** terse, functional, utility-first. No marketing voice, no personality text. The app talks like a piece of lab equipment, not a storefront.

**Casing:**
- **Title Case** for product name ("CS2 Skin Browser"), weapon names ("AK-47", "Desert Eagle"), rarities ("Mil-Spec", "Covert"), and button labels ("Open on Workshop", "Add Tag").
- **Sentence case** for inline status text ("Loading skins…", "No preview", "3 results").
- **Lower-case hyphenated kebab** for user-authored tags (`sci-fi`, `orange`, `case-hardened`, `angles`, `geometry`).

**Label syntax:** key-value lines read `Label: value` with a single space after the colon — `Weapon: AK-47`, `Rarity: Covert`, `Collection: The Danger Zone Collection`. An em-dash (`—`) is the empty-state placeholder, never "N/A" or "–".

**Counts:** pluralize explicitly — `1 result` / `3 results` / `0 results`. Frames read `Frame 4 / 10`.

**Ellipses:** real Unicode ellipsis `…`, never three periods. Used on progress states ("Loading skins…", "Picking skin of the day…", "Building grid…").

**No emoji. No icon-only buttons.** Every action has a text label. Unicode is used sparingly: `—` (empty), `…` (progress), `/` (framecount + pluralization).

**I vs. you:** neither. The app describes state, not relationships. Tags are the only user-authored content and they're noun phrases, not sentences.

**The vibe:** a CS operator's HUD crossed with a reference-image archiver. Dark, dense, keyboard-friendly, no chrome that doesn't do work. Think Steam console + Qt Creator + an art-director's moodboard.

---

## Visual foundations

**Palette — operator navy.** The entire app lives in a narrow range of desaturated blues. The scale (measured from the `DARK_STYLE` in `application/utils.py`):

| Role | Hex | Usage |
|---|---|---|
| `bg-1` deepest | `#162030` | Nav bar, inputs, list rows, scrollbar track, tile background |
| `bg-2` base | `#1E2837` | Main window surface, scroll panes |
| `bg-3` card | `#253347` | Cards, tiles, combo boxes, default buttons |
| `bg-4` hover | `#2D3F58` | Button hover, selected list item |
| `bg-5` pressed | `#1A2840` | Button pressed state |
| `line` | `#304060` | Borders, dividers, scrollbar thumb |
| `line-strong` | `#3A6090` | Main-window border (2px) |
| `accent` | `#4A7FB5` | Focus rings, slider handle/fill, hover borders, progress nearly-full |
| `accent-deep` | `#3D6FA8` | Progress-bar chunk fill |
| `fg-1` text | `#E0E8F0` | Primary text |
| `fg-2` muted | `#6A7F9A` | Status-bar text, subtle labels |
| `fg-disabled` | `#4A6080` | Disabled button text |

**Rarity color ladder** (CS2 canonical, referenced in `scripts/constants.py` comments):

| Rarity | Color | Hex |
|---|---|---|
| Consumer Grade | White | `#B0C3D9` |
| Industrial Grade | Light Blue | `#5E98D9` |
| Mil-Spec | Blue | `#4B69FF` |
| Restricted | Purple | `#8847FF` |
| Classified | Pink | `#D32CE6` |
| Covert | Red | `#EB4B4B` |
| Contraband | Orange | `#E4AE39` |
| ★ Extraordinary (knives/gloves) | Gold | `#E4AE39` |

These are the ONLY saturated colors in the app. Rarities appear as small pills or a left-edge rarity bar on skin tiles — the art itself is already colorful, so the chrome stays monochrome.

**Type.** The Qt app uses Qt's default sans (`13px` base, `20pt bold` splash title, `11pt` subtitle). In this design system we render in:
- **Display / UI:** `Inter` (clean, neutral, modern-HUD feel; good CS2 match)
- **Labels / metadata:** `JetBrains Mono` (the weapon-stats, framecount, tag chips — reinforces the "operator console" read)
- **Base size:** 13px body, matching the Qt `font-size: 13px` base. Dense.

**Spacing.** Tight. Qt pads buttons at `5px 12px`, inputs at `4px 8px`, list items at `3px 6px`. Component min-heights are `26px` (buttons/inputs) and `18px` (progress). Our scale:
- `2 / 4 / 6 / 8 / 12 / 16 / 24 / 32` px. No 10, 14, 20 in between — the Qt code is strict about this.

**Corner radii.** Small. Buttons/inputs/combos use `4px`. Cards use `6px`. The slider handle is `8px` (circle, 16px diameter). Nothing is more rounded than 6px except pure circles (slider, scrollbar). No big softened cards.

**Borders vs. shadows.** Everything is bordered, nothing is shadowed. `1px solid #304060` is the universal hairline; the main window itself gets a heavier `2px solid #3A6090` frame (a Qt app-window convention, kept here as a brand mark). **No drop shadows, no elevation layers, no glow.** Depth is conveyed entirely through darker-deeper stacking (bg-1 inside bg-2 inside bg-3).

**Backgrounds.** Solid fills only. No gradients, no textures, no hero imagery, no grain. The one exception: the splash screen paints text directly on a solid `#1E2837` rectangle — still flat.

**Imagery.** Color vibe is dictated by the source material (skin renders) — saturated, warm-and-cool mixed, full spectrum. The chrome around it is cold blue-grey, which makes the art pop. Skin thumbnails are **cover-fit** (scaled by `KeepAspectRatioByExpanding` and center-cropped) inside tile frames.

**Animation.** There is none in the Qt code. Hover/press states switch instantly. **Design-system rule: animations are opt-in and should be ≤120ms linear or ease-out.** No bounces, no spring physics, no page transitions.

**Hover states.** Buttons: background lightens (`#253347` → `#2D3F58`), border shifts to accent (`#304060` → `#4A7FB5`). Inputs/combos: border shifts to accent only, no fill change. List items: subtle row tint (`#1E2D42`).

**Press states.** Buttons only: background darkens (`#1A2840`). No scale, no inset shadow.

**Focus states.** Input border changes to accent (`#4A7FB5`). No glow ring.

**Disabled states.** Text, border, and fill all collapse to the deepest bg (`#1E2837` / `#4A6080`) — effectively fades into the surface.

**Transparency / blur.** Never. Everything is opaque.

**Layout rules.**
- Main window has a fixed-height nav bar at top (`#162030` with a `1px #304060` bottom border).
- Status bar at bottom (`#162030`, muted text).
- Content fills the middle, either as a scrolling 5-column skin grid or a detail split (preview | metadata).
- Cards (`QFrame#card_frame`) group related controls — metadata card, tag-editor card.

**Scrollbars.** 8px track, `#304060` thumb → `#4A7FB5` on hover, no buttons (no up/down arrows). Same horizontal and vertical.

**Tiles (skin tiles).** Square-ish card, thumbnail on top, three-line label block below (name / rarity / collection). Hover changes cursor to pointer; click opens detail. No lift, no shadow — the border does the work.

**Sliders.** 4px track (`#304060`), 16px circular handle (`#4A7FB5`), sub-page fills in accent. Used exclusively for frame-scrubbing on webm previews.

**Progress bars.** 18px tall, `1px #304060` border, `#3D6FA8` fill chunk with 3px radius, centered text overlay.

**Layering / z.** Modals are QDialog or QSplashScreen — same bordered-rectangle idiom. No overlay scrim (Qt handles app-modality natively).

---

## Iconography

**The existing app uses no icons whatsoever.** Every action is a text button ("Search", "Open on Workshop", "Add Tag", "Remove", "Back", "Prev", "Save & Next", "Skip", "Tagger"). The Qt stylesheet hides the combo-box drop-down arrow entirely. There is no logo, no icon font, no SVG sprite, no PNG glyph anywhere in the repo.

**Design-system decision:** keep icons **minimal and functional** when we need them for UI density, matching the terse HUD feel. We use **Lucide** (via CDN) as the system font — thin-stroke (1.5px), 16px default, rendered in `currentColor` inheriting from text.

**Where icons appear in this design system's UI kit:**
- Search input (magnifier glyph left-padded)
- External-link buttons (arrow-up-right for Workshop, target for in-game Inspect)
- Scrubber controls (chevron-left / chevron-right for prev/next frame)
- Tag remove (× glyph)
- Navigation (chevron-left for back)

**Emoji: never.** Unicode symbols are restricted to `—`, `…`, `/`, `★` (for knife/glove rarity only).

A CDN substitution to Lucide is flagged — if the artist-owner wants a different stroke weight or a custom icon set, please attach it.

---

## Index — files in this folder

- **`README.md`** — this document
- **`SKILL.md`** — agent skill manifest (Claude Code-compatible)
- **`colors_and_type.css`** — CSS custom properties for color + typography
- **`fonts/`** — Inter + JetBrains Mono (Google Fonts substitution; see note below)
- **`assets/`** — logo marks, rarity chips, placeholder skin renders
- **`preview/`** — Design-System-tab card files (colors, type, components, brand)
- **`ui_kits/cs-art-viewer/`** — React (JSX) UI kit recreating the desktop app
  - `index.html` — interactive click-thru of the Browser + Detail view
  - Components: `TopBar`, `WeaponFilter`, `SearchInput`, `SkinTile`, `SkinGrid`, `DetailView`, `FrameScrubber`, `RarityPill`, `TagChip`, `MetadataCard`, `TaggerModal`

### Directory manifest

```
/
├── README.md                  — this document
├── SKILL.md                   — agent skill manifest
├── colors_and_type.css        — CSS custom properties + semantic styles
├── assets/
│   ├── logo.svg               — bracketed-crosshair mark (placeholder)
│   └── logo-mono.svg          — monochrome variant
├── preview/                   — Design-System-tab cards (registered)
│   ├── _card.css
│   ├── colors-core.html       — operator navy
│   ├── colors-text.html
│   ├── colors-rarity.html     — CS2 rarity ladder
│   ├── type-scale.html / type-mono.html
│   ├── spacing.html / radii-borders.html
│   ├── buttons.html / inputs.html / rarity-pills.html
│   ├── tags.html / slider-progress.html
│   ├── skin-tile.html / window-frame.html
│   ├── icons.html             — Lucide (CDN substitution)
│   └── logo.html
└── ui_kits/
    └── cs-art-viewer/
        ├── README.md
        ├── index.html         — click-thru prototype
        ├── styles.css
        ├── data.js            — mock skin records
        ├── components.jsx     — Brand, Icon, RarityPill, TagChip, SkinTile…
        └── views.jsx          — BrowserView, DetailView, TaggerModal
```

### Font substitution flag

The Qt application uses the platform default sans at 13px. **No custom font file is shipped with the repo.** This design system substitutes **Inter** (display/UI) and **JetBrains Mono** (labels/metadata) from Google Fonts as reasonable matches for the CS2-adjacent operator aesthetic. If the maintainer wants a different family — Rajdhani, Industry, Roboto Condensed, Share Tech Mono, or a proprietary file — please drop it into `fonts/` and flag the swap.
