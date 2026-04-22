import cv2
from pathlib import Path

from PySide6.QtCore import QEvent, QFile, QObject
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtUiTools import QUiLoader

DARK_STYLE = """
QWidget {
    background-color: #1E2837;
    color: #E0E8F0;
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
"""


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
