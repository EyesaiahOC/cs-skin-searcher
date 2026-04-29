import pytest

from application.tag_chip_widget import TagChipWidget


@pytest.fixture
def widget(qapp):
    w = TagChipWidget()
    yield w
    w.deleteLater()


def test_importable():
    from application.tag_chip_widget import TagChipWidget as T
    assert T is not None


def test_set_tags_populates_widget(widget):
    widget.set_tags(["alpha", "beta", "gamma"])
    assert widget.get_tags() == ["alpha", "beta", "gamma"]


def test_set_tags_replaces_existing(widget):
    widget.set_tags(["old1", "old2"])
    widget.set_tags(["new1"])
    assert widget.get_tags() == ["new1"]
    assert "old1" not in widget.get_tags()
    assert "old2" not in widget.get_tags()


def test_get_tags_preserves_display_order(widget):
    widget.set_tags(["c", "a", "b"])
    assert widget.get_tags() == ["c", "a", "b"]


def test_enter_adds_tag(widget):
    widget.set_tags([])
    widget._input.setText("red")
    widget._input.returnPressed.emit()
    assert "red" in widget.get_tags()


def test_enter_clears_input(widget):
    widget.set_tags([])
    widget._input.setText("blue")
    widget._input.returnPressed.emit()
    assert widget._input.text() == ""


def test_duplicate_not_added(widget):
    widget.set_tags(["red"])
    widget._input.setText("red")
    widget._input.returnPressed.emit()
    assert widget.get_tags().count("red") == 1


def test_remove_chip_updates_tags(widget):
    widget.set_tags(["alpha", "beta", "gamma"])
    widget._remove_chip("beta")
    assert widget.get_tags() == ["alpha", "gamma"]


def test_tag_added_signal_fires(widget):
    widget.set_tags([])
    emitted = []
    widget.tag_added.connect(emitted.append)
    widget._input.setText("new-tag")
    widget._input.returnPressed.emit()
    assert emitted == ["new-tag"]


def test_tag_added_not_fired_for_duplicate(widget):
    widget.set_tags(["existing"])
    emitted = []
    widget.tag_added.connect(emitted.append)
    widget._input.setText("existing")
    widget._input.returnPressed.emit()
    assert emitted == []


def test_tag_removed_signal_fires(widget):
    widget.set_tags(["to-remove"])
    emitted = []
    widget.tag_removed.connect(emitted.append)
    widget._remove_chip("to-remove")
    assert emitted == ["to-remove"]


def test_get_tags_returns_copy(widget):
    widget.set_tags(["a", "b"])
    tags = widget.get_tags()
    tags.append("c")
    assert widget.get_tags() == ["a", "b"]
