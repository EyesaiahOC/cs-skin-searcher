# CS Art Viewer — UI Kit

High-fidelity web recreation of the PySide6/Qt desktop app (`EyesaiahOC/cs-skin-searcher/application/`).
Not a storefront — a reference-browser for skin artists.

## Files
- `index.html` — interactive click-thru (Browser → Detail → Tagger modal)
- `styles.css` — pulls in `../../colors_and_type.css`; defines all component styles
- `data.js` — mock skin records (shape matches `raw_json/*.json` in the real repo) + rarity color map
- `components.jsx` — `Brand`, `Icon`, `RarityPill`, `TagChip`, `SkinTile`, `TopBar`, `StatusBar`, `Scrubber`, `Card`
- `views.jsx` — `BrowserView`, `DetailView`, `TaggerModal`

## Source mapping
| Real app file | UI kit equivalent |
|---|---|
| `application/browser.py` | `BrowserView` + `DetailView` (split into two React views) |
| `application/skin_tile.py` | `SkinTile` component |
| `application/tagger.py` | `TaggerModal` |
| `application/utils.py` `DARK_STYLE` | `styles.css` + `../../colors_and_type.css` |
| `application/main.py` splash | logo mark in nav bar |
| `scripts/constants.py` `Rarity` enum | `RARITY` map in `data.js` |

## Things the real app has that this mock fakes
- Real webm frame extraction (`cv2.VideoCapture` → 10 `QPixmap` frames) — here, a gradient's hue rotates with the frame slider
- Steam `steam://` inspect links + Workshop URL opening — here, buttons are inert
- Reading/writing tags to disk — here, React state only

The *look* is lifted 1:1 from the Qt stylesheet.
