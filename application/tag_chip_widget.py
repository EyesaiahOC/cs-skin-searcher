from PySide6.QtCore import QPoint, QRect, QSize, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class _FlowLayout(QLayout):
    """Wrapping flow layout for chip widgets."""

    def __init__(self, parent=None, h_spacing: int = 4, v_spacing: int = 4):
        super().__init__(parent)
        self._items: list = []
        self._h = h_spacing
        self._v = v_spacing

    def addItem(self, item):
        self._items.append(item)

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int):
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index: int):
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        m = self.contentsMargins()
        return size + QSize(m.left() + m.right(), m.top() + m.bottom())

    def _do_layout(self, rect: QRect, test_only: bool) -> int:
        m = self.contentsMargins()
        eff = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        x, y, line_h = eff.x(), eff.y(), 0
        for item in self._items:
            hint = item.sizeHint()
            next_x = x + hint.width() + self._h
            if next_x - self._h > eff.right() and line_h > 0:
                x = eff.x()
                y += line_h + self._v
                next_x = x + hint.width() + self._h
                line_h = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), hint))
            x = next_x
            line_h = max(line_h, hint.height())
        return y + line_h - rect.y() + m.bottom()


class TagChipWidget(QWidget):
    tag_added = Signal(str)
    tag_removed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tags: list[str] = []
        self._chips: dict[str, QPushButton] = {}

        self._chips_area = QWidget()
        self._chips_area.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self._flow = _FlowLayout(self._chips_area, h_spacing=4, v_spacing=4)
        self._chips_area.setLayout(self._flow)

        self._scroll = QScrollArea()
        self._scroll.setWidget(self._chips_area)
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._scroll.setMinimumHeight(36)
        self._scroll.setMaximumHeight(120)
        self._scroll.setFrameShape(QFrame.NoFrame)

        self._input = QLineEdit()
        self._input.setPlaceholderText("Add tag…")
        self._input.returnPressed.connect(self._on_enter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(self._scroll)
        layout.addWidget(self._input)

    def set_tags(self, tags: list[str]) -> None:
        for chip in self._chips.values():
            chip.deleteLater()
        self._chips.clear()
        self._tags.clear()
        while self._flow.count():
            self._flow.takeAt(0)
        for tag in tags:
            self._create_chip(tag)
        self._chips_area.adjustSize()

    def get_tags(self) -> list[str]:
        return list(self._tags)

    def _on_enter(self) -> None:
        tag = self._input.text().strip()
        self._input.clear()
        if not tag or tag in self._tags:
            return
        self._create_chip(tag)
        self._chips_area.adjustSize()
        self.tag_added.emit(tag)

    def _create_chip(self, tag: str) -> None:
        btn = QPushButton(f"{tag}  ×")
        btn.setObjectName("tag_chip")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.clicked.connect(lambda _checked=False, t=tag: self._remove_chip(t))
        self._chips[tag] = btn
        self._tags.append(tag)
        self._flow.addWidget(btn)

    def _remove_chip(self, tag: str) -> None:
        if tag not in self._tags:
            return
        self._tags.remove(tag)
        chip = self._chips.pop(tag)
        while self._flow.count():
            self._flow.takeAt(0)
        for t in self._tags:
            self._flow.addWidget(self._chips[t])
        chip.deleteLater()
        self._chips_area.adjustSize()
        self.tag_removed.emit(tag)
