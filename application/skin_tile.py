from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel

from utils import ClickFilter, load_ui

_TILE_UI = Path(__file__).parent / "ui_files" / "skin_tile_widget.ui"
_THUMB_PX = 160


class SkinTileWidget:
    def __init__(self, skin_data: dict, thumbnail: QPixmap, on_click):
        self.skin_data = skin_data
        self.widget = load_ui(_TILE_UI)

        frame_lbl: QLabel = self.widget.findChild(QLabel, "tile_frame")
        if not thumbnail.isNull():
            size = frame_lbl.minimumSize()
            # Expand to cover the square, then center-crop — keeps aspect ratio, fills box
            expanded = thumbnail.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            x = (expanded.width() - size.width()) // 2
            y = (expanded.height() - size.height()) // 2
            frame_lbl.setPixmap(expanded.copy(x, y, size.width(), size.height()))

        self.widget.findChild(QLabel, "tile_name").setText(skin_data.get("name", ""))
        self.widget.findChild(QLabel, "tile_rarity").setText(skin_data.get("rarity", ""))
        self.widget.findChild(QLabel, "tile_collection").setText(skin_data.get("collection") or "")

        self._click_filter = ClickFilter(on_click)
        self.widget.installEventFilter(self._click_filter)
        self.widget.setCursor(Qt.PointingHandCursor)
