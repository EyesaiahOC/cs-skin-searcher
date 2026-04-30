import cv2
from pathlib import Path

from PySide6.QtCore import QEvent, QFile, QObject, QSize, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtUiTools import QUiLoader

_REPO_ROOT = Path(__file__).parent.parent


def resolve_asset_path(stored_path: str, repo_root: Path = _REPO_ROOT) -> Path | None:
    """Resolve a stored asset path to an existing file.

    Accepts absolute paths (legacy or correct) and relative paths from the
    repo root. Returns None if the file cannot be found either way.
    """
    if not stored_path:
        return None
    p = Path(stored_path)
    if p.is_absolute():
        if p.exists():
            return p
        # Legacy absolute path pointing at the wrong machine location —
        # try rebasing onto the current repo root using the filename stem.
        candidate = repo_root / p.relative_to(p.anchor)
        if candidate.exists():
            return candidate
    else:
        candidate = repo_root / p
        if candidate.exists():
            return candidate
    return None

DARK_STYLE = """
QWidget {
    background-color: #1E2837;
    color: #E0E8F0;
    font-family: "Inter", "Ubuntu Sans", "Segoe UI", sans-serif;
    font-size: 13px;
}
QMainWindow, QDialog {
    background-color: #1E2837;
    border: 2px solid #3A6090;
}
QStatusBar {
    background-color: #162030;
    color: #6A7F9A;
    border-top: 1px solid #304060;
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 11px;
}
QFrame#nav_bar {
    background-color: #162030;
    border-bottom: 1px solid #304060;
}
QPushButton {
    background-color: #253347;
    color: #E0E8F0;
    border: 1px solid #304060;
    border-radius: 4px;
    padding: 5px 12px;
    min-height: 26px;
}
QPushButton:hover {
    background-color: #2D3F58;
    border-color: #4A7FB5;
}
QPushButton:pressed {
    background-color: #1A2840;
}
QPushButton:disabled {
    color: #4A6080;
    border-color: #1E2837;
    background-color: #1E2837;
}
QLineEdit {
    background-color: #162030;
    color: #E0E8F0;
    border: 1px solid #304060;
    border-radius: 4px;
    padding: 4px 8px;
    min-height: 26px;
}
QLineEdit:focus {
    border-color: #4A7FB5;
}
QComboBox {
    background-color: #253347;
    color: #E0E8F0;
    border: 1px solid #304060;
    border-radius: 4px;
    padding: 4px 8px;
    min-height: 26px;
}
QComboBox:hover {
    border-color: #4A7FB5;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #253347;
    color: #E0E8F0;
    selection-background-color: #2D3F58;
    border: 1px solid #304060;
    outline: 0;
}
QListWidget {
    background-color: #162030;
    color: #E0E8F0;
    border: 1px solid #304060;
    border-radius: 4px;
    outline: 0;
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 12px;
}
QListWidget::item {
    padding: 3px 6px;
}
QListWidget::item:selected {
    background-color: #2D3F58;
    color: #E0E8F0;
}
QListWidget::item:hover:!selected {
    background-color: #1E2D42;
}
QScrollArea, QAbstractScrollArea {
    background-color: #1E2837;
    border: none;
}
QScrollBar:vertical {
    background-color: #162030;
    width: 8px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background-color: #304060;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background-color: #4A7FB5;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background-color: #162030;
    height: 8px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background-color: #304060;
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #4A7FB5;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QProgressBar {
    background-color: #162030;
    border: 1px solid #304060;
    border-radius: 4px;
    text-align: center;
    color: #E0E8F0;
    min-height: 18px;
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 11px;
}
QProgressBar::chunk {
    background-color: #3D6FA8;
    border-radius: 3px;
}
QSlider::groove:horizontal {
    background-color: #304060;
    height: 4px;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background-color: #4A7FB5;
    width: 16px;
    height: 16px;
    border-radius: 8px;
    margin: -6px 0;
}
QSlider::sub-page:horizontal {
    background-color: #4A7FB5;
    border-radius: 2px;
}
QFrame[frameShape="4"],
QFrame[frameShape="5"] {
    color: #304060;
}
QLabel {
    background-color: transparent;
}
QFrame#card_frame {
    background-color: #253347;
    border: 1px solid #304060;
    border-radius: 6px;
}
QLabel#tile_frame {
    background-color: #1E2837;
    border: none;
    border-radius: 4px;
}

/* ---- Skin name headings ---- */
QLabel#detail_skin_name,
QLabel#skin_name_label,
QLabel#tagger_skin_name {
    font-size: 18px;
    font-weight: 600;
    color: #E0E8F0;
}

/* ---- Monospace metadata labels ---- */
QLabel#detail_weapon_label,
QLabel#detail_rarity_label,
QLabel#detail_collection_label,
QLabel#weapon_label,
QLabel#collection_label,
QLabel#tagger_weapon_label,
QLabel#tagger_collection_label {
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 12px;
    color: #6A7F9A;
}
QLabel#rarity_label,
QLabel#tagger_rarity_label {
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 12px;
}

/* ---- Frame counter + results count ---- */
QLabel#detail_frame_label,
QLabel#frame_label,
QLabel#tagger_frame_label,
QLabel#results_count_label {
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 11px;
    color: #6A7F9A;
}

/* ---- Tagger progress label ---- */
QLabel#progress_label,
QLabel#tagger_progress_label {
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 12px;
    font-weight: 600;
    color: #E0E8F0;
}

/* ---- Section headings ---- */
QLabel#detail_tags_heading,
QLabel#tags_heading,
QLabel#tagger_tags_heading {
    font-size: 11px;
    font-weight: 600;
    color: #6A7F9A;
}

/* ---- Tile labels ---- */
QLabel#tile_name {
    font-size: 12px;
    font-weight: 600;
    color: #E0E8F0;
}
QLabel#tile_rarity {
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 11px;
}
QLabel#tile_collection {
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 10px;
    color: #6A7F9A;
}

/* ---- Frame preview area ---- */
QLabel#detail_frame_display,
QLabel#frame_display,
QLabel#tagger_frame_display {
    background-color: #162030;
    border: 1px solid #304060;
    border-radius: 4px;
    color: #6A7F9A;
}

/* ---- CS2 rarity colors (set via rarity_key dynamic property) ---- */
QLabel[rarity_key="consumer-grade"]   { color: #B0C3D9; }
QLabel[rarity_key="industrial-grade"] { color: #5E98D9; }
QLabel[rarity_key="mil-spec-grade"]   { color: #4B69FF; }
QLabel[rarity_key="restricted"]       { color: #8847FF; }
QLabel[rarity_key="classified"]       { color: #D32CE6; }
QLabel[rarity_key="covert"]           { color: #EB4B4B; }
QLabel[rarity_key="contraband"]       { color: #E4AE39; }
QLabel[rarity_key="extraordinary"]    { color: #E4AE39; }

/* ---- CS2 rarity borders on skin tile cards ---- */
QFrame#card_frame[rarity_key="consumer-grade"]   { border: 2px solid #B0C3D9; }
QFrame#card_frame[rarity_key="industrial-grade"] { border: 2px solid #5E98D9; }
QFrame#card_frame[rarity_key="mil-spec-grade"]   { border: 2px solid #4B69FF; }
QFrame#card_frame[rarity_key="restricted"]       { border: 2px solid #8847FF; }
QFrame#card_frame[rarity_key="classified"]       { border: 2px solid #D32CE6; }
QFrame#card_frame[rarity_key="covert"]           { border: 2px solid #EB4B4B; }
QFrame#card_frame[rarity_key="contraband"]       { border: 2px solid #E4AE39; }
QFrame#card_frame[rarity_key="extraordinary"]    { border: 2px solid #E4AE39; }

/* ---- Home page ---- */
QLabel#home_featured_image {
    background-color: #0E1520;
    border: none;
    color: #6A7F9A;
}
QLabel#home_skin_name {
    font-size: 22px;
    font-weight: 700;
    color: #E0E8F0;
}
QLabel#home_weapon_label,
QLabel#home_collection_label {
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 13px;
    color: #6A7F9A;
}
QLabel#home_rarity_label {
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 13px;
}
QWidget#home_info_panel {
    background-color: #162030;
    border-top: 1px solid #304060;
}

/* ---- Tag chip pills ---- */
QPushButton#tag_chip {
    background-color: #253347;
    color: #E0E8F0;
    border: 1px solid #304060;
    border-radius: 4px;
    padding: 3px 8px;
    min-height: 22px;
    font-family: "JetBrains Mono", "Ubuntu Mono", "Consolas", monospace;
    font-size: 12px;
    font-weight: 400;
}
QPushButton#tag_chip:hover {
    background-color: #2D3F58;
    border-color: #4A7FB5;
}
QPushButton#tag_chip:pressed {
    background-color: #1A2840;
}
"""


def scale_pixmap_to_fit(pixmap: QPixmap, target_size: QSize) -> QPixmap:
    if target_size.width() <= 0 or target_size.height() <= 0:
        return pixmap
    return pixmap.scaled(target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)


def apply_rarity_style(label, rarity: str) -> None:
    key = (rarity or "").lower().replace(" ", "-")
    label.setProperty("rarity_key", key)
    label.style().unpolish(label)
    label.style().polish(label)
    label.update()


def load_ui(path: Path):
    loader = QUiLoader()
    f = QFile(str(path))
    if not f.open(QFile.ReadOnly):
        raise RuntimeError(f"Cannot open UI file: {path}")
    window = loader.load(f, None)
    f.close()
    if window is None:
        raise RuntimeError("UI failed to load")
    return window


def extract_frames(webm_path: str, count: int = 10) -> list[QPixmap]:
    cap = cv2.VideoCapture(webm_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total < 1:
        cap.release()
        return []
    positions = [int(i * (total - 1) / max(count - 1, 1)) for i in range(count)]
    pixmaps = []
    for pos in positions:
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ok, frame = cap.read()
        if ok:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            img = QImage(frame.data.tobytes(), w, h, ch * w, QImage.Format_RGB888)
            pixmaps.append(QPixmap.fromImage(img))
    cap.release()
    return pixmaps


class ResizeFilter(QObject):
    """Re-renders a label's pixmap whenever it is resized."""

    def __init__(self, callback):
        super().__init__()
        self._callback = callback

    def eventFilter(self, _obj, event):
        if event.type() == QEvent.Type.Resize:
            self._callback()
        return False


class ClickFilter(QObject):
    """Fires a callback on mouse press."""

    def __init__(self, callback):
        super().__init__()
        self._callback = callback

    def eventFilter(self, _obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            self._callback()
        return False
