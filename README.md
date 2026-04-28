# CS2 Skin Scraper

A tool for scraping CS2 weapon skin data from [csgoskins.gg](https://csgoskins.gg), downloading WebM skin previews, generating thumbnails, and browsing/tagging the results through a PySide6 desktop GUI.

## Features

- **Scraper** — fetches skin metadata (name, weapon, rarity, collection, pattern info, in-game inspect link, Steam Workshop link) and downloads the WebM preview video for every skin across all weapon types.
- **Thumbnail generator** — extracts and center-crops the first frame of each WebM into a 160×160 JPEG for fast grid display.
- **Browser GUI** — searchable, filterable grid of all scraped skins with a detail view that lets you scrub through preview frames and manage tags.
- **Tagger GUI** — a dedicated workflow for rapidly tagging untagged skins one by one, with keyboard navigation (→ to save and advance).

## Project Structure

```
skin-scraper/
├── scripts/               # Scraper and thumbnail pipeline
│   ├── main.py            # Entry point: scrapes all weapons end-to-end
│   ├── fetch_htmls.py     # Downloads and caches weapon listing pages
│   ├── html_to_weapon_urls.py  # Parses skin URLs from listing HTML
│   ├── weapon_url_to_json.py   # Scrapes individual skin pages → JSON
│   ├── generate_thumbnails.py  # Generates thumbnails from WebM files
│   └── constants.py       # WeaponType and Rarity enums
├── application/           # PySide6 GUI
│   ├── browser.py         # Main browser window (entry point)
│   ├── tagger.py          # Tagger window
│   ├── skin_tile.py       # Grid tile widget
│   ├── utils.py           # Shared helpers: dark theme, frame extractor, UI loader
│   └── ui_files/          # Qt Designer .ui layout files
├── raw_json/              # One JSON file per skin (output of scraper)
├── webm/                  # Downloaded WebM preview videos
└── webpages/              # Cached weapon listing HTML pages
```

## Setup

**Requirements:** Python 3.11+

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install PySide6 requests beautifulsoup4 opencv-python numpy
```

## Usage

### 1. Scrape skin data

Run from the repo root. Resumes automatically — already-scraped skins are skipped.

```bash
python -m scripts.main
```

This fetches every weapon's listing page, then scrapes each skin's detail page, downloading the WebM preview and saving a JSON record to `raw_json/`.

### 2. Generate thumbnails

```bash
python scripts/generate_thumbnails.py
```

Reads `raw_json/`, extracts the first frame of each WebM, saves a 160×160 JPEG to `application/thumbnails/`, and writes the path back into the JSON.

### 3. Launch the browser

```bash
cd application
python browser.py
```

- Use the weapon dropdown and search bar to filter skins.
- Click any tile to open the detail view with a frame scrubber.
- Add/remove tags directly in the detail view; changes are saved back to the JSON file on navigation.
- Click **Tagger** to open the dedicated tagging workflow.

### Tagger

The tagger window shows only skins that have no tags yet. Use the **Save & Next** button or the **→ arrow key** to save tags and move to the next skin. Use **Skip** to defer without saving.

## JSON Schema

Each skin is stored as a single JSON file in `raw_json/`:

```json
{
    "name": "AK-47 | Redline",
    "weapon": "AK-47",
    "rarity": "Classified",
    "collection": "The Phoenix Collection",
    "is_patterned_based": false,
    "webm_filepath": "/absolute/path/to/webm/ak-47-redline.webm",
    "in_game_url": "steam://rungame/...",
    "workshop_url": "https://steamcommunity.com/sharedfiles/filedetails/?id=...",
    "tags": ["stripes"],
    "thumbnail_path": "/absolute/path/to/thumbnails/ak-47-redline.jpg"
}
```

## Supported Weapons

All weapon categories are covered: pistols, SMGs, shotguns, machine guns, rifles, and sniper rifles — 34 weapon types in total as defined in `scripts/constants.py`.