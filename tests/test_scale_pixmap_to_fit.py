import pytest
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap

from utils import scale_pixmap_to_fit

TOLERANCE = 0.02


def make_pixmap(w: int, h: int) -> QPixmap:
    pm = QPixmap(w, h)
    pm.fill()
    return pm


@pytest.fixture(autouse=True)
def _require_qapp(qapp):
    pass


def test_output_never_exceeds_target_width():
    result = scale_pixmap_to_fit(make_pixmap(800, 400), QSize(200, 200))
    assert result.width() <= 200
    assert result.height() <= 200


def test_wider_than_target_width_equals_target():
    result = scale_pixmap_to_fit(make_pixmap(800, 200), QSize(400, 400))
    assert result.width() == 400


def test_taller_than_target_height_equals_target():
    result = scale_pixmap_to_fit(make_pixmap(200, 800), QSize(400, 400))
    assert result.height() == 400


def test_aspect_ratio_preserved():
    src = make_pixmap(600, 400)
    result = scale_pixmap_to_fit(src, QSize(300, 300))
    src_ratio = src.width() / src.height()
    out_ratio = result.width() / result.height()
    assert abs(src_ratio - out_ratio) < TOLERANCE


def test_smaller_than_target_fits_within():
    result = scale_pixmap_to_fit(make_pixmap(50, 30), QSize(200, 200))
    assert result.width() <= 200
    assert result.height() <= 200


def test_zero_width_target_returns_without_crash():
    pm = make_pixmap(100, 100)
    result = scale_pixmap_to_fit(pm, QSize(0, 100))
    assert not result.isNull()


def test_zero_height_target_returns_without_crash():
    pm = make_pixmap(100, 100)
    result = scale_pixmap_to_fit(pm, QSize(100, 0))
    assert not result.isNull()


def test_zero_size_target_returns_without_crash():
    pm = make_pixmap(100, 100)
    result = scale_pixmap_to_fit(pm, QSize(0, 0))
    assert not result.isNull()
