from PySide6.QtWidgets import QMainWindow, QPushButton


class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Holder")
        self.setGeometry(100, 100, 300, 200)

        # Create a button and set it as the central widget
        button = QPushButton("Click Me", self)
        self.setCentralWidget(button)