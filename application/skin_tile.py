from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel

from utils import ClickFilter, apply_rarity_style, load_ui

_TILE_UI = Path(__file__).parent / "ui_files" / "skin_tile_widget.ui"


def load_thumbnail(skin_data: dict) -> QPixmap:
    path = skin_data.get("thumbnail_path", "")
    if path and Path(path).exists():
        return QPixmap(path)
    return QPixmap()


class SkinTileWidget:
    def __init__(self, skin_data: dict, thumbnail: QPixmap, on_click):
        self.skin_data = skin_data
        self.widget = load_ui(_TILE_UI)

        frame_lbl: QLabel = self.widget.findChild(QLabel, "tile_frame")
        if not thumbnail.isNull():
            frame_lbl.setPixmap(thumbnail)

        self.widget.findChild(QLabel, "tile_name").setText(skin_data.get("name", ""))
        rarity_lbl = self.widget.findChild(QLabel, "tile_rarity")
        rarity_lbl.setText(skin_data.get("rarity", ""))
        apply_rarity_style(rarity_lbl, skin_data.get("rarity", ""))

        self._click_filter = ClickFilter(on_click)
        self.widget.installEventFilter(self._click_filter)
        self.widget.setCursor(Qt.PointingHandCursor)
