import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile


def load_ui(filename):
    loader = QUiLoader()
    file = QFile(filename)

    if not file.open(QFile.ReadOnly):
        raise RuntimeError(f"Cannot open file: {filename}")

    window = loader.load(file, None)  # IMPORTANT FIX HERE
    file.close()

    if window is None:
        raise RuntimeError("UI failed to load")

    return window


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = load_ui("/home/eyes/workspace/eyes/skin-scraper/application/ui_files/main_window.ui")

    window.show()

    sys.exit(app.exec())