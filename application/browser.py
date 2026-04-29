import random
import sys
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, Qt, QUrl
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtWidgets import (
    QApplication, QComboBox, QLabel, QLineEdit,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy, QSlider, QStackedWidget, QWidget,
)

from skin_store import SkinStore
from skin_tile import SkinTileWidget, load_thumbnail
from tag_chip_widget import TagChipWidget
from utils import DARK_STYLE, ResizeFilter, apply_rarity_style, extract_frames, load_ui, resolve_asset_path


class _TaggerKeyFilter(QObject):
    """Application-level event filter for tagger keyboard shortcuts."""

    def __init__(self, parent, window, is_on_tagger, on_save_next, on_prev, on_skip):
        super().__init__(parent)
        self._window = window
        self._is_on_tagger = is_on_tagger
        self._on_save_next = on_save_next
        self._on_prev = on_prev
        self._on_skip = on_skip
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, _obj, event):
        if (event.type() == QEvent.Type.KeyPress
                and self._window.isActiveWindow()
                and self._is_on_tagger()):
            mod = event.modifiers()
            key = event.key()
            if mod == Qt.ControlModifier:
                if key in (Qt.Key_Return, Qt.Key_Enter):
                    self._on_save_next()
                    return True
                if key == Qt.Key_Left:
                    self._on_prev()
                    return True
                if key == Qt.Key_Backspace:
                    self._on_skip()
                    return True
        return False


_UI_PATH = Path(__file__).parent / "ui_files" / "main_window.ui"
_JSON_DIR = Path(__file__).parent.parent / "raw_json"
_TILE_WIDTH = 200
_FRAME_COUNT = 10

_PAGE_HOME = 0
_PAGE_RESULTS = 1
_PAGE_DETAIL = 2
_PAGE_TAGGER = 3


class BrowserWindow:
    def __init__(self):
        self.store = SkinStore(_JSON_DIR)
        self.skins: list[dict] = []
        self.search_results: list[int] = []
        self.current_detail_index: int = -1
        self.detail_raw_frames: list[QPixmap] = []
        self._tiles: list[SkinTileWidget] = []
        self._grid_cols: int = 0
        self._featured_index: int = -1
        self._featured_pixmap: QPixmap | None = None
        self._tagger_queue: list[int] = []
        self._tagger_pos: int = 0
        self._tagger_raw_frames: list[QPixmap] = []

        self.window = load_ui(_UI_PATH)
        self._bind_widgets()
        self._connect_signals()

        self._detail_resize_filter = ResizeFilter(
            lambda: self._show_detail_frame(self.detail_frame_slider.value())
        )
        self.detail_frame_display.installEventFilter(self._detail_resize_filter)

        self._home_resize_filter = ResizeFilter(self._refresh_home_image)
        self.home_featured_image.installEventFilter(self._home_resize_filter)

        self._tagger_resize_filter = ResizeFilter(
            lambda: self._tagger_show_frame(self.tagger_frame_slider.value())
        )
        self.tagger_frame_display.installEventFilter(self._tagger_resize_filter)

        self._tagger_key_filter = _TaggerKeyFilter(
            QApplication.instance(),
            self.window,
            lambda: self.pages.currentIndex() == _PAGE_TAGGER,
            self._tagger_save_and_next,
            self._tagger_prev,
            self._tagger_skip,
        )

        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._grid_resize_filter = ResizeFilter(self._relayout_grid)
        self.results_scroll.viewport().installEventFilter(self._grid_resize_filter)

        self._reload_skins()
        self._populate_weapon_combo()
        self._run_search()
        self._load_home_page()

    def show(self):
        self.window.show()

    # ------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------

    def _reload_skins(self):
        self.skins = self.store.load_all()
        print(f"  Loaded {len(self.skins)} skins")

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _bind_widgets(self):
        w = self.window

        def fw(cls, name):
            return w.findChild(cls, name)

        self.pages = fw(QStackedWidget, "pages")

        # Home page
        self.home_featured_image   = fw(QLabel,      "home_featured_image")
        self.home_skin_name        = fw(QLabel,      "home_skin_name")
        self.home_weapon_label     = fw(QLabel,      "home_weapon_label")
        self.home_rarity_label     = fw(QLabel,      "home_rarity_label")
        self.home_collection_label = fw(QLabel,      "home_collection_label")
        self.home_search_input     = fw(QLineEdit,   "home_search_input")
        self.home_view_skin_btn    = fw(QPushButton, "home_view_skin_btn")
        self.home_tagger_btn       = fw(QPushButton, "home_tagger_btn")

        # Results page
        self.home_btn_1          = fw(QPushButton, "home_btn_1")
        self.weapon_type_combo   = fw(QComboBox,   "weapon_type_combo")
        self.search_input        = fw(QLineEdit,   "search_input")
        self.search_btn          = fw(QPushButton, "search_btn")
        self.results_count_label = fw(QLabel,      "results_count_label")
        self.results_scroll      = fw(QScrollArea, "results_scroll")
        results_container        = self.results_scroll.widget()
        self.results_grid        = results_container.layout()

        # Detail page
        self.home_btn_2              = fw(QPushButton, "home_btn_2")
        self.back_btn                = fw(QPushButton, "back_btn")
        self.detail_frame_display    = fw(QLabel,      "detail_frame_display")
        self.detail_frame_slider     = fw(QSlider,     "detail_frame_slider")
        self.detail_frame_label      = fw(QLabel,      "detail_frame_label")
        self.detail_skin_name        = fw(QLabel,      "detail_skin_name")
        self.detail_weapon_label     = fw(QLabel,      "detail_weapon_label")
        self.detail_rarity_label     = fw(QLabel,      "detail_rarity_label")
        self.detail_collection_label = fw(QLabel,      "detail_collection_label")
        self.detail_workshop_btn     = fw(QPushButton, "detail_workshop_btn")
        self.detail_inspect_btn      = fw(QPushButton, "detail_inspect_btn")

        detail_tags_panel = fw(QWidget, "detail_tags_panel")
        self.detail_chip_widget = TagChipWidget()
        detail_tags_panel.layout().addWidget(self.detail_chip_widget)

        # Tagger page
        self.home_btn_3              = fw(QPushButton,    "home_btn_3")
        self.tagger_progress_label   = fw(QLabel,         "tagger_progress_label")
        self.tagger_progress_bar     = fw(QProgressBar,   "tagger_progress_bar")
        self.tagger_skip_btn         = fw(QPushButton,    "tagger_skip_btn")
        self.tagger_content_stack    = fw(QStackedWidget, "tagger_content_stack")
        self.tagger_frame_display    = fw(QLabel,         "tagger_frame_display")
        self.tagger_frame_slider     = fw(QSlider,        "tagger_frame_slider")
        self.tagger_frame_label      = fw(QLabel,         "tagger_frame_label")
        self.tagger_skin_name        = fw(QLabel,         "tagger_skin_name")
        self.tagger_weapon_label     = fw(QLabel,         "tagger_weapon_label")
        self.tagger_rarity_label     = fw(QLabel,         "tagger_rarity_label")
        self.tagger_collection_label = fw(QLabel,         "tagger_collection_label")
        self.tagger_prev_btn         = fw(QPushButton,    "tagger_prev_btn")
        self.tagger_save_next_btn    = fw(QPushButton,    "tagger_save_next_btn")

        tagger_tags_panel = fw(QWidget, "tagger_tags_panel")
        self.tagger_chip_widget = TagChipWidget()
        tagger_tags_panel.layout().addWidget(self.tagger_chip_widget)

    def _connect_signals(self):
        # Home page
        self.home_search_input.returnPressed.connect(self._home_search)
        self.home_view_skin_btn.clicked.connect(self._home_view_skin)
        self.home_tagger_btn.clicked.connect(self._enter_tagger)

        # Results page
        self.home_btn_1.clicked.connect(self._go_home)
        self.search_btn.clicked.connect(self._run_search)
        self.search_input.returnPressed.connect(self._run_search)
        self.weapon_type_combo.currentIndexChanged.connect(self._run_search)

        # Detail page
        self.home_btn_2.clicked.connect(self._go_home)
        self.back_btn.clicked.connect(self._go_back)
        self.detail_frame_slider.valueChanged.connect(self._show_detail_frame)
        self.detail_chip_widget.tag_added.connect(lambda _: self._save_detail())
        self.detail_chip_widget.tag_removed.connect(lambda _: self._save_detail())
        self.detail_workshop_btn.clicked.connect(self._open_workshop)
        self.detail_inspect_btn.clicked.connect(self._open_inspect)

        # Tagger page
        self.home_btn_3.clicked.connect(self._go_home)
        self.tagger_skip_btn.clicked.connect(self._tagger_skip)
        self.tagger_frame_slider.valueChanged.connect(self._tagger_show_frame)
        self.tagger_prev_btn.clicked.connect(self._tagger_prev)
        self.tagger_save_next_btn.clicked.connect(self._tagger_save_and_next)

    def _populate_weapon_combo(self):
        self.weapon_type_combo.blockSignals(True)
        self.weapon_type_combo.clear()
        self.weapon_type_combo.addItem("All Weapons")
        weapons = sorted({s.get("weapon", "") for s in self.skins if s.get("weapon")})
        self.weapon_type_combo.addItems(weapons)
        self.weapon_type_combo.blockSignals(False)

    # ------------------------------------------------------------------
    # Home page
    # ------------------------------------------------------------------

    def _load_home_page(self):
        if not self.skins:
            return
        self._featured_index = random.randrange(len(self.skins))
        skin = self.skins[self._featured_index]

        self.home_skin_name.setText(skin.get("name", "—"))
        self.home_weapon_label.setText(skin.get("weapon", "—"))
        rarity = skin.get("rarity", "")
        self.home_rarity_label.setText(rarity or "—")
        apply_rarity_style(self.home_rarity_label, rarity)
        self.home_collection_label.setText(skin.get("collection") or "—")

        thumb = load_thumbnail(skin)
        self._featured_pixmap = thumb if not thumb.isNull() else None
        self._refresh_home_image()

        self.pages.setCurrentIndex(_PAGE_HOME)

    def _refresh_home_image(self):
        if not self._featured_pixmap:
            self.home_featured_image.setText("No preview available")
            return
        size = self.home_featured_image.size()
        if size.width() > 10 and size.height() > 10:
            self.home_featured_image.setPixmap(
                self._featured_pixmap.scaled(
                    size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

    def _home_search(self):
        query = self.home_search_input.text().strip()
        self.search_input.setText(query)
        self.weapon_type_combo.blockSignals(True)
        self.weapon_type_combo.setCurrentIndex(0)
        self.weapon_type_combo.blockSignals(False)
        self._run_search()
        self.pages.setCurrentIndex(_PAGE_RESULTS)

    def _home_view_skin(self):
        if self._featured_index >= 0:
            self._open_detail(self._featured_index)

    def _go_home(self):
        if self.pages.currentIndex() == _PAGE_TAGGER:
            if (self._tagger_queue
                    and self.tagger_content_stack.currentIndex() == 0
                    and self.tagger_chip_widget.get_tags()):
                self._tagger_save_current()
        else:
            self._save_detail()
        self.pages.setCurrentIndex(_PAGE_HOME)

    # ------------------------------------------------------------------
    # Search + grid
    # ------------------------------------------------------------------

    def _run_search(self):
        weapon = self.weapon_type_combo.currentText()
        text = self.search_input.text().strip()

        indices = self.store.search(text)
        if weapon != "All Weapons":
            indices = [i for i in indices if self.skins[i].get("weapon") == weapon]

        self.search_results = indices
        self._populate_grid(indices)

    def _populate_grid(self, indices: list[int]):
        container = self.results_scroll.widget()
        container.setUpdatesEnabled(False)

        while self.results_grid.count():
            item = self.results_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._tiles.clear()

        for idx in indices:
            skin = self.skins[idx]
            tile = SkinTileWidget(
                skin_data=skin,
                thumbnail=load_thumbnail(skin),
                on_click=lambda i=idx: self._open_detail(i),
            )
            tile.widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            self._tiles.append(tile)

        self._grid_cols = 0
        self._relayout_grid()

        container.setUpdatesEnabled(True)

        count = len(indices)
        self.results_count_label.setText(f"{count} result{'s' if count != 1 else ''}")

    def _relayout_grid(self):
        if not self._tiles:
            return
        viewport_width = self.results_scroll.viewport().width()
        cols = max(1, viewport_width // _TILE_WIDTH)
        if cols == self._grid_cols:
            return
        prev_cols = self._grid_cols
        self._grid_cols = cols
        for c in range(max(prev_cols, cols) + 2):
            self.results_grid.setColumnStretch(c, 0)
        for pos, tile in enumerate(self._tiles):
            row, col = divmod(pos, cols)
            self.results_grid.addWidget(tile.widget, row, col)
        self.results_grid.setColumnStretch(cols, 1)

    # ------------------------------------------------------------------
    # Detail view
    # ------------------------------------------------------------------

    def _open_detail(self, skin_index: int):
        self.current_detail_index = skin_index
        skin = self.skins[skin_index]

        self.detail_skin_name.setText(skin.get("name", "—"))
        self.detail_weapon_label.setText(f"Weapon: {skin.get('weapon', '—')}")
        rarity = skin.get("rarity", "")
        self.detail_rarity_label.setText(f"Rarity: {rarity or '—'}")
        apply_rarity_style(self.detail_rarity_label, rarity)
        self.detail_collection_label.setText(f"Collection: {skin.get('collection') or '—'}")

        tags = list(dict.fromkeys(
            skin.get("tags", []) + skin.get("colors", [])
        ))
        self.detail_chip_widget.set_tags(tags)

        webm = resolve_asset_path(skin.get("webm_filepath", ""))
        self.detail_raw_frames = (
            extract_frames(str(webm), count=_FRAME_COUNT) if webm else []
        )
        self.detail_frame_slider.setValue(0)
        self._show_detail_frame(0)

        self.detail_workshop_btn.setEnabled(bool(skin.get("workshop_url")))
        self.detail_inspect_btn.setEnabled(bool(skin.get("in_game_url")))

        self.pages.setCurrentIndex(_PAGE_DETAIL)

    def _show_detail_frame(self, idx: int):
        if self.detail_raw_frames and 0 <= idx < len(self.detail_raw_frames):
            size = self.detail_frame_display.size()
            if size.width() > 10 and size.height() > 10:
                self.detail_frame_display.setPixmap(
                    self.detail_raw_frames[idx].scaled(
                        size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
                )
        else:
            self.detail_frame_display.clear()
            self.detail_frame_display.setText("No preview")
        self.detail_frame_label.setText(f"Frame {idx + 1} / {_FRAME_COUNT}")

    def _go_back(self):
        self._save_detail()
        self.pages.setCurrentIndex(_PAGE_RESULTS)

    def _save_detail(self):
        if self.current_detail_index < 0:
            return
        skin = self.skins[self.current_detail_index]
        skin["tags"] = self.detail_chip_widget.get_tags()
        skin.pop("colors", None)
        self.store.save(self.current_detail_index, skin)

    # ------------------------------------------------------------------
    # Tagger mode
    # ------------------------------------------------------------------

    def _enter_tagger(self):
        self.skins = self.store.load_all()
        self._tagger_queue = self.store.untagged_indices()
        self._tagger_pos = 0
        self.tagger_chip_widget.set_tags([])
        if self._tagger_queue:
            self.tagger_content_stack.setCurrentIndex(0)
            self._tagger_load_skin(0)
        else:
            self.tagger_content_stack.setCurrentIndex(1)
        self.pages.setCurrentIndex(_PAGE_TAGGER)

    def _tagger_load_skin(self, pos: int):
        pos = max(0, min(pos, len(self._tagger_queue) - 1))
        self._tagger_pos = pos
        store_idx = self._tagger_queue[pos]
        skin = self.skins[store_idx]

        self.tagger_skin_name.setText(skin.get("name", "—"))
        self.tagger_weapon_label.setText(f"Weapon: {skin.get('weapon', '—')}")
        rarity = skin.get("rarity", "")
        self.tagger_rarity_label.setText(f"Rarity: {rarity or '—'}")
        apply_rarity_style(self.tagger_rarity_label, rarity)
        self.tagger_collection_label.setText(f"Collection: {skin.get('collection') or '—'}")

        tags = list(dict.fromkeys(
            skin.get("tags", []) + skin.get("colors", [])
        ))
        self.tagger_chip_widget.set_tags(tags)

        webm = resolve_asset_path(skin.get("webm_filepath", ""))
        self._tagger_raw_frames = (
            extract_frames(str(webm), count=_FRAME_COUNT) if webm else []
        )
        self.tagger_frame_slider.setValue(0)
        self._tagger_show_frame(0)
        self._tagger_update_progress()

    def _tagger_show_frame(self, idx: int):
        if self._tagger_raw_frames and 0 <= idx < len(self._tagger_raw_frames):
            size = self.tagger_frame_display.size()
            if size.width() > 10 and size.height() > 10:
                self.tagger_frame_display.setPixmap(
                    self._tagger_raw_frames[idx].scaled(
                        size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
                )
        else:
            self.tagger_frame_display.clear()
            self.tagger_frame_display.setText("No preview")
        self.tagger_frame_label.setText(f"Frame {idx + 1} / {_FRAME_COUNT}")

    def _tagger_update_progress(self):
        total = len(self._tagger_queue)
        pos = self._tagger_pos + 1
        self.tagger_progress_label.setText(f"Skin {pos} / {total} untagged")
        self.tagger_progress_bar.setMaximum(total)
        self.tagger_progress_bar.setValue(pos)

    def _tagger_save_current(self):
        if not self._tagger_queue:
            return
        store_idx = self._tagger_queue[self._tagger_pos]
        skin = dict(self.skins[store_idx])
        skin["tags"] = self.tagger_chip_widget.get_tags()
        skin.pop("colors", None)
        self.store.save(store_idx, skin)
        self.skins[store_idx] = skin

    def _tagger_save_and_next(self):
        if not self._tagger_queue or self.tagger_content_stack.currentIndex() != 0:
            return
        self._tagger_save_current()
        if self._tagger_pos < len(self._tagger_queue) - 1:
            self._tagger_load_skin(self._tagger_pos + 1)
        else:
            self.tagger_content_stack.setCurrentIndex(1)

    def _tagger_skip(self):
        if not self._tagger_queue or self.tagger_content_stack.currentIndex() != 0:
            return
        if self._tagger_pos < len(self._tagger_queue) - 1:
            self._tagger_load_skin(self._tagger_pos + 1)
        else:
            self.tagger_content_stack.setCurrentIndex(1)

    def _tagger_prev(self):
        if not self._tagger_queue or self.tagger_content_stack.currentIndex() != 0:
            return
        if self._tagger_pos > 0:
            self._tagger_load_skin(self._tagger_pos - 1)

    # ------------------------------------------------------------------
    # External links
    # ------------------------------------------------------------------

    def _open_workshop(self):
        url = self.skins[self.current_detail_index].get("workshop_url", "")
        if url:
            QDesktopServices.openUrl(QUrl(url))

    def _open_inspect(self):
        url = self.skins[self.current_detail_index].get("in_game_url", "")
        if url:
            QDesktopServices.openUrl(QUrl(url))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    browser = BrowserWindow()
    browser.show()
    sys.exit(app.exec())
