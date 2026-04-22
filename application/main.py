import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen
from browser import BrowserWindow
from utils import DARK_STYLE


def _make_splash_pixmap(width: int = 480, height: int = 200) -> QPixmap:
    pixmap = QPixmap(width, height)
    pixmap.fill(QColor("#1E2837"))

    painter = QPainter(pixmap)

    title_font = QFont()
    title_font.setPointSize(20)
    title_font.setBold(True)
    painter.setFont(title_font)
    painter.setPen(QColor("#E0E8F0"))
    painter.drawText(pixmap.rect().adjusted(0, -40, 0, 0), Qt.AlignCenter, "CS2 Skin Browser")

    sub_font = QFont()
    sub_font.setPointSize(11)
    painter.setFont(sub_font)
    painter.setPen(QColor("#6A7F9A"))
    painter.drawText(pixmap.rect().adjusted(0, 40, 0, 0), Qt.AlignCenter, "Loading skins…")

    painter.end()
    return pixmap


if __name__ == "__main__":
    print("Starting CS2 Skin Browser…")
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)

    splash = QSplashScreen(_make_splash_pixmap(), Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    print("Picking skin of the day…")
    browser = BrowserWindow()
    print("Done — launching UI")
    splash.finish(browser.window)
    browser.show()
    sys.exit(app.exec())
