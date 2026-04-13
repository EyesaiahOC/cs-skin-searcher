import cv2

from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QSlider,
    QVBoxLayout,
    QWidget,
    QSizePolicy
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap


class WeaponPreview(QMainWindow):
    def __init__(self, weapon_data):
        super().__init__()

        self.weapon_data = weapon_data
        self.setWindowTitle(weapon_data["name"])

        # -----------------------------
        # WINDOW (movable, resizable)
        # -----------------------------
        self.resize(1200, 800)

        # -----------------------------
        # VIDEO
        # -----------------------------
        self.cap = cv2.VideoCapture(self.weapon_data["webm_filepath"])
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # store last frame for resize updates
        self.current_frame = None

        # -----------------------------
        # UI
        # -----------------------------
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)

        self.video_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10)

        # layout
        container = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.video_label, stretch=1)
        layout.addWidget(self.slider, stretch=0)

        container.setLayout(layout)
        self.setCentralWidget(container)

        # -----------------------------
        # signals
        # -----------------------------
        self.slider.valueChanged.connect(self.on_scrub)



    # -----------------------------
    # SCRUBBER
    # -----------------------------
    def on_scrub(self, value):
        norm = value / 10
        frame_index = int(norm * (self.total_frames - 1))
        self.show_frame(frame_index)

    # -----------------------------
    # FRAME LOADING
    # -----------------------------
    def show_frame(self, frame_index):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self.cap.read()

        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.current_frame = frame  # store for resize updates

        self.update_display()

    # -----------------------------
    # DISPLAY (handles scaling + aspect ratio)
    # -----------------------------
    def update_display(self):
        if self.current_frame is None:
            return

        frame = self.current_frame
        h, w, ch = frame.shape

        window_w = self.video_label.width()
        window_h = self.video_label.height()

        # target size
        target_w = int(window_w * 0.9)
        target_h = int(window_h * 0.9)

        # keep aspect ratio
        scale = min(target_w / w, target_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized = cv2.resize(frame, (new_w, new_h))

        bytes_per_line = ch * new_w

        qt_image = QImage(
            resized.data,
            new_w,
            new_h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    # -----------------------------
    # RESIZE EVENT (IMPORTANT)
    # -----------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_display()

    def showEvent(self, event):
        super().showEvent(event)

        # ensure layout is fully resolved before first render
        if not hasattr(self, "_initialised"):
            self._initialised = True
            self.show_frame(0)