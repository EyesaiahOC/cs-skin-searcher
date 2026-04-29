# GUI Redesign PRD
Source: GitHub issue #1 (EyesaiahOC/skin-scraper)

## Problem Statement

The current CS2 Skin Browser GUI has several compounding problems:
- No home/landing experience — app drops directly into search grid
- Tagger is a separate floating window with no connection to the browser
- Tagger has a broken import crash (`_RightArrowFilter` references `QApplication` before import)
- Right-arrow keyboard shortcut in Tagger conflicts with text cursor movement
- All 1,378 JSON records store broken absolute paths for `webm_filepath` and `thumbnail_path`
- Nav bar bleeds controls across all pages
- Results grid hardcoded at 5 columns (not responsive)
- Detail view: tags list capped at 80px, plain list widget, image not dominant
- Tags only saved on Back button press — closing window discards them
- Skin tile shows rarity text instead of rarity-coloured border
- Browser and tagger duplicate all skin loading/saving/searching logic

## Solution

4-page stacked navigation: Home → Results Grid → Detail View → Tagger Mode. Merge Tagger into browser. Shared `SkinStore` data layer. One-time path migration script + runtime resolver. Responsive grid. Image-first layouts. Tag chip/pill widgets. Auto-save on every change. Fixed keyboard shortcuts.

## Implementation Tasks

### Task 1: Path migration + runtime asset path resolver (Issue #2)
**Status: TODO**
**Blocked by: nothing**

- Migration script (`scripts/migrate_paths.py`) rewrites all JSONs in `raw_json/` — converts absolute `webm_filepath` and `thumbnail_path` to repo-relative paths (e.g. `webm/ak-47-aphrodite.webm`, `application/thumbnails/ak-47-aphrodite.jpg`)
- Migration is idempotent
- `resolve_asset_path(stored_path, repo_root)` added to `utils.py`: tries path as-is, then relative to repo root, returns `None` if neither resolves
- All existing `Path(path).exists()` checks replaced with resolver
- Tests: `tests/test_migrate_paths.py` and `tests/test_utils.py`

Acceptance criteria:
- Running the migration rewrites all JSONs to relative paths
- Migration is idempotent (running twice = running once)
- JSONs with already-correct relative paths are left unchanged
- `resolve_asset_path` returns absolute path for relative input with valid repo root
- `resolve_asset_path` returns stored path when it is already a valid absolute path
- `resolve_asset_path` returns `None` when neither form resolves
- Thumbnails and WebM frame previews load correctly after migration
- Tests pass

### Task 2: Central skin data layer — SkinStore (Issue #3)
**Status: TODO**
**Blocked by: nothing**

- New `application/skin_store.py` module
- `SkinStore(json_dir)` constructor
- `load_all() -> list[dict]`
- `save(index: int, skin: dict)`
- `search(query: str) -> list[int]`
- `untagged_indices() -> list[int]`
- Remove duplicated load/save/search logic from `browser.py` and `tagger.py`
- Tests: `tests/test_skin_store.py`

Acceptance criteria:
- `load_all()` returns correct count from temp JSON directory
- `save()` writes updated tag list without corrupting other fields
- `search("")` returns all indices
- `search("ak-47")` returns only weapon-matching indices
- `search("redline")` returns only name-matching indices
- `untagged_indices()` returns only indices where `tags` is absent or empty
- `untagged_indices()` excludes skins with at least one tag
- `browser.py` and `tagger.py` no longer contain duplicated data logic
- Tests pass

### Task 3: Responsive grid + rarity-border tile (Issue #4)
**Status: TODO**
**Blocked by: nothing**

- Grid recalculates column count on container resize (available width / ~200px tile width)
- Skin tile: remove rarity text label; add rarity-coloured border on card frame using existing design system palette
- Tiles show thumbnail + name only

Acceptance criteria:
- Column count increases/decreases with window width
- No dead horizontal space when maximised
- Tiles never overflow when narrow
- No rarity text label on tiles
- Border colour matches rarity (Covert=red, Restricted=purple, etc.)
- Tiles with no rarity render with neutral border
- Rarity border colours match design system palette

### Task 4: Tag chip widget (Issue #5)
**Status: TODO**
**Blocked by: nothing**

- New `application/tag_chip_widget.py` — reusable `TagChipWidget(QWidget)`
- `set_tags(tags: list[str])`
- `get_tags() -> list[str]`
- `tag_added` signal (str)
- `tag_removed` signal (str)
- Tags render as styled pills matching design system
- Click pill → remove immediately
- Type in input + Enter → add tag, clear input
- No duplicates

Acceptance criteria:
- Tags render as styled pills consistent with design system
- Clicking a pill removes that tag immediately
- Enter in input adds tag and clears input
- Duplicate tags are not added
- `set_tags()` replaces current pills with provided list
- `get_tags()` returns current tags in display order
- `tag_added` fires with new tag string
- `tag_removed` fires with removed tag string
- Widget is importable independently

### Task 5: 4-page navigation shell + Home page (Issue #6)
**Status: TODO**
**Blocked by: Task 1 (path migration), Task 2 (SkinStore)**

- Replace 2-page stacked widget with 4-page stack: Home(0), Results Grid(1), Detail View(2), Tagger Mode(3)
- Remove persistent nav bar
- Add small Home icon to top-left of pages 1, 2, 3
- Build Home page:
  - Randomly selected skin on each launch
  - Frame 0 image, full window width, aspect ratio locked
  - Name / weapon / rarity / collection below image
  - "View Skin Page" → Detail View for that skin
  - "Tagger Mode" → page 3
  - Search bar → Results Grid with query pre-filled on Enter

Acceptance criteria:
- App launches to Home page
- Different skin featured each launch
- Image fills full width, aspect ratio locked
- Name, weapon, rarity, collection displayed
- "View Skin Page" navigates to Detail View for featured skin
- "Tagger Mode" navigates to page 3
- Search bar + Enter navigates to Results Grid with query active
- No weapon dropdown or unrelated controls on Home page
- Home icon on pages 1/2/3 returns to Home
- Persistent nav bar removed

### Task 6: Results Grid page (Issue #7)
**Status: TODO**
**Blocked by: Task 3 (responsive tiles), Task 5 (navigation shell)**

- Wire Results Grid as page 1
- Search bar pre-filled from Home page query
- Search works for weapon type, skin name, and tags
- Result count label
- Back to Home button
- Responsive rarity-border tiles from Task 3

Acceptance criteria:
- Home page search pre-fills Results Grid and shows results immediately
- Weapon type search (e.g. "AK-47") returns all skins of that weapon
- Skin name substring search works
- Tag search works
- Result count label correct
- Grid uses responsive rarity-border tiles
- Clicking tile navigates to Detail View
- Back to Home button works
- Search bar placeholder communicates weapon/name/tag are all searchable

### Task 7: Detail View redesign (Issue #8)
**Status: TODO**
**Blocked by: Task 4 (tag chip widget), Task 5 (navigation shell)**

- Page 2 in navigation shell
- Frame preview: full window width, aspect ratio locked, ~70% vertical height
- Scrub slider always initialises to frame 0
- Bottom panel: metadata left, TagChipWidget right
- Every tag add/remove → immediate JSON write via SkinStore
- Workshop Link + Inspect In Game buttons (disabled when URL absent)
- Back to Home button

Acceptance criteria:
- Frame preview fills full width, aspect ratio preserved
- Frame preview ~70% window height
- Scrub slider initialises to frame 0
- Name, weapon, rarity, collection displayed
- Tags shown as chips via TagChipWidget
- Clicking chip removes it and immediately saves to disk
- Adding tag via Enter saves immediately to disk
- Navigating away does not lose tags
- Workshop Link button opens URL, disabled when absent
- Inspect In Game button opens URL, disabled when absent
- Back to Home works

### Task 8: Tagger Mode as page 3 (Issue #9)
**Status: TODO**
**Blocked by: Task 2 (SkinStore), Task 4 (tag chip widget), Task 5 (navigation shell)**

- Merge tagger into browser as page 3; remove separate `QMainWindow` from `tagger.py`
- Fix `_RightArrowFilter` import crash
- Queue from `SkinStore.untagged_indices()`, re-evaluated on each entry
- Replace broken shortcuts with: `Ctrl+Enter` (save & next), `Ctrl+←` (previous in session queue), `Ctrl+Backspace` (skip)
- Tags via TagChipWidget
- Auto-save on Back to Home if tags present
- "Tagging Complete" state when queue empty
- Progress bar + label

Acceptance criteria:
- Tagger Mode accessible as page 3 from Home
- Queue contains only untagged skins
- Queue re-evaluated fresh on each entry
- Frame preview dominant vertical space, aspect ratio locked
- Scrub slider initialises to frame 0
- Enter in tag input adds chip
- Ctrl+Enter saves and advances
- Ctrl+← goes to previous skin in session queue
- Ctrl+Backspace skips without saving
- All shortcuts work regardless of focus
- Back to Home with tags → auto-saves
- Back to Home without tags → leaves skin untagged
- Progress label and bar show position in queue
- "Tagging Complete" shown when queue empty
- No separate floating Tagger window
- `_RightArrowFilter` crash fixed

## Design System Notes

- Rarity colour palette: defined in `application/designsystem/` and `utils.py` — use existing tokens
- Tag chip/pill preview styles: already in `application/designsystem/`
- Rarity `Enum`: `scripts/constants.py` is authoritative — QSS map in `utils.py` must stay in sync
- `webm/` and `application/thumbnails/` are co-located with repo root
- Relative paths expressed from repo root (e.g. `webm/ak-47-aphrodite.webm`)
- 1,378 JSON records — migration must process one file at a time, not all in memory

## Out of Scope

- Search history / state preservation across navigation
- Weapon type navigation button
- Session tagging summary
- Re-queuing tagged skins in Tagger
- Autoplay / animated WebM (always scrubber-driven, no QMediaPlayer)
