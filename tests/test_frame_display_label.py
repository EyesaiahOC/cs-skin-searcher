import pytest
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap

from utils import FrameDisplayLabel


@pytest.fixture(autouse=True)
def _require_qapp(qapp):
    pass


def test_size_hint_is_small():
    label = FrameDisplayLabel()
    hint = label.sizeHint()
    assert hint.width() <= 4
    assert hint.height() <= 4


def test_minimum_size_hint_is_small():
    label = FrameDisplayLabel()
    hint = label.minimumSizeHint()
    assert hint.width() <= 4
    assert hint.height() <= 4


def test_size_hint_matches_minimum_size_hint():
    label = FrameDisplayLabel()
    assert label.sizeHint() == label.minimumSizeHint()


def test_size_hint_unchanged_after_large_pixmap():
    label = FrameDisplayLabel()
    pm = QPixmap(1920, 1080)
    pm.fill()
    label.setPixmap(pm)
    assert label.sizeHint().width() <= 4
    assert label.sizeHint().height() <= 4


def test_minimum_size_hint_unchanged_after_large_pixmap():
    label = FrameDisplayLabel()
    pm = QPixmap(1920, 1080)
    pm.fill()
    label.setPixmap(pm)
    assert label.minimumSizeHint().width() <= 4
    assert label.minimumSizeHint().height() <= 4


def test_importable_from_utils():
    from utils import FrameDisplayLabel as FDL  # noqa: F401
    assert issubclass(FDL, FrameDisplayLabel)
