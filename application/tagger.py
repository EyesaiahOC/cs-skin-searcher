import sys
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QPixmap


class _RightArrowFilter(QObject):
    def __init__(self, window, callback):
        super().__init__(QApplication.instance())
        self._window = window
        self._callback = callback
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.KeyPress
                and event.key() == Qt.Key_Right
                and self._window.isActiveWindow()):
            self._callback()
            return True
        return False
from PySide6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QListWidget,
    QProgressBar, QPushButton, QSlider,
)

from skin_store import SkinStore
from utils import DARK_STYLE, ResizeFilter, apply_rarity_style, extract_frames, load_ui, resolve_asset_path

_UI_PATH = Path(__file__).parent / "ui_files" / "tagger_window.ui"
_JSON_DIR = Path(__file__).parent.parent / "raw_json"
_FRAME_COUNT = 10


class TaggerWindow:
    def __init__(self, json_dir: Path = _JSON_DIR):
        self.store = SkinStore(json_dir)
        self.store.load_all()
        self.queue: list[int] = self.store.untagged_indices()
        self.queue_pos: int = 0
        self.current_data: dict = {}
        self.raw_frames: list[QPixmap] = []

        self.window = load_ui(_UI_PATH)
        self._bind_widgets()
        self._connect_signals()

        self._resize_filter = ResizeFilter(
            lambda: self._show_frame(self.frame_slider.value())
        )
        self.frame_display.installEventFilter(self._resize_filter)

        if self.queue:
            self._load_skin(0)

    def show(self):
        self.window.show()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _bind_widgets(self):
        w = self.window

        def fw(cls, name):
            return w.findChild(cls, name)

        self.progress_label   = fw(QLabel,       "progress_label")
        self.progress_bar     = fw(QProgressBar, "progress_bar")
        self.skip_btn         = fw(QPushButton,  "skip_btn")
        self.frame_display    = fw(QLabel,       "frame_display")
        self.frame_slider     = fw(QSlider,      "frame_slider")
        self.frame_label      = fw(QLabel,       "frame_label")
        self.skin_name_label  = fw(QLabel,       "skin_name_label")
        self.weapon_label     = fw(QLabel,       "weapon_label")
        self.rarity_label     = fw(QLabel,       "rarity_label")
        self.collection_label = fw(QLabel,       "collection_label")
        self.tags_list        = fw(QListWidget,  "tags_list")
        self.tag_input        = fw(QLineEdit,    "tag_input")
        self.add_tag_btn      = fw(QPushButton,  "add_tag_btn")
        self.remove_tag_btn   = fw(QPushButton,  "remove_tag_btn")
        self.prev_btn         = fw(QPushButton,  "prev_btn")
        self.save_next_btn    = fw(QPushButton,  "save_next_btn")

    def _connect_signals(self):
        self.frame_slider.valueChanged.connect(self._on_frame_changed)
        self.add_tag_btn.clicked.connect(self._add_tag)
        self.tag_input.returnPressed.connect(self._add_tag)
        self.remove_tag_btn.clicked.connect(self._remove_tag)
        self.prev_btn.clicked.connect(self._go_prev)
        self.save_next_btn.clicked.connect(self._save_and_next)
        self.skip_btn.clicked.connect(self._skip)

        self._right_arrow_filter = _RightArrowFilter(self.window, self._save_and_next)

    # ------------------------------------------------------------------
    # Skin loading
    # ------------------------------------------------------------------

    def _load_skin(self, queue_pos: int):
        queue_pos = max(0, min(queue_pos, len(self.queue) - 1))
        self.queue_pos = queue_pos
        store_idx = self.queue[queue_pos]
        self.current_data = dict(self.store.get(store_idx))

        self.skin_name_label.setText(self.current_data.get("name", "—"))
        self.weapon_label.setText(f"Weapon: {self.current_data.get('weapon', '—')}")
        rarity = self.current_data.get("rarity", "")
        self.rarity_label.setText(f"Rarity: {rarity or '—'}")
        apply_rarity_style(self.rarity_label, rarity)
        collection = self.current_data.get("collection") or "—"
        self.collection_label.setText(f"Collection: {collection}")

        # Merge legacy colors into tags on load
        tags = list(dict.fromkeys(
            self.current_data.get("tags", []) + self.current_data.get("colors", [])
        ))
        self.tags_list.clear()
        for tag in tags:
            self.tags_list.addItem(tag)

        webm = resolve_asset_path(self.current_data.get("webm_filepath", ""))
        self.raw_frames = extract_frames(str(webm)) if webm else []

        self.frame_slider.setValue(0)
        self._show_frame(0)
        self._update_progress()

    def _show_frame(self, idx: int):
        if self.raw_frames and 0 <= idx < len(self.raw_frames):
            size = self.frame_display.size()
            if size.width() > 10 and size.height() > 10:
                self.frame_display.setPixmap(
                    self.raw_frames[idx].scaled(
                        size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
                )
        else:
            self.frame_display.clear()
            self.frame_display.setText("No preview")
        self.frame_label.setText(f"Frame {idx + 1} / {_FRAME_COUNT}")

    def _update_progress(self):
        total = len(self.queue)
        self.progress_label.setText(f"Skin {self.queue_pos + 1} / {total} untagged")
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(self.queue_pos + 1)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _on_frame_changed(self, value: int):
        self._show_frame(value)

    def _add_tag(self):
        text = self.tag_input.text().strip()
        if not text:
            return
        existing = [self.tags_list.item(i).text() for i in range(self.tags_list.count())]
        if text not in existing:
            self.tags_list.addItem(text)
        self.tag_input.clear()

    def _remove_tag(self):
        for item in self.tags_list.selectedItems():
            self.tags_list.takeItem(self.tags_list.row(item))

    def _collect_list(self, widget: QListWidget) -> list[str]:
        return [widget.item(i).text() for i in range(widget.count())]

    def _save_current(self):
        self.current_data["tags"] = self._collect_list(self.tags_list)
        self.current_data.pop("colors", None)
        store_idx = self.queue[self.queue_pos]
        self.store.save(store_idx, self.current_data)

    def _save_and_next(self):
        self._save_current()
        if self.queue_pos < len(self.queue) - 1:
            self._load_skin(self.queue_pos + 1)

    def _skip(self):
        if self.queue_pos < len(self.queue) - 1:
            self._load_skin(self.queue_pos + 1)

    def _go_prev(self):
        if self.queue_pos > 0:
            self._load_skin(self.queue_pos - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    tagger = TaggerWindow()
    tagger.show()
    sys.exit(app.exec())
