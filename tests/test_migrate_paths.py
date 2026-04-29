import json
import pytest
from pathlib import Path

from scripts.migrate_paths import migrate_all, migrate_file, to_relative


# --- to_relative unit tests ---

def test_to_relative_strips_broken_prefix():
    broken = "/home/eyes/workspace/eyes/skin-scraper/webm/ak-47-foo.webm"
    assert to_relative(broken) == "webm/ak-47-foo.webm"


def test_to_relative_strips_thumbnail_prefix():
    broken = "/home/eyes/workspace/eyes/skin-scraper/application/thumbnails/ak-47-foo.jpg"
    assert to_relative(broken) == "application/thumbnails/ak-47-foo.jpg"


def test_to_relative_leaves_already_relative_unchanged():
    rel = "webm/ak-47-foo.webm"
    assert to_relative(rel) == rel


def test_to_relative_leaves_empty_unchanged():
    assert to_relative("") == ""


# --- migrate_file tests ---

def _make_json(tmp_path: Path, data: dict) -> Path:
    p = tmp_path / "skin.json"
    p.write_text(json.dumps(data, indent=4))
    return p


def test_migrate_file_rewrites_broken_webm(tmp_path):
    p = _make_json(tmp_path, {
        "name": "Test Skin",
        "webm_filepath": "/home/eyes/workspace/eyes/skin-scraper/webm/test.webm",
        "thumbnail_path": "",
    })
    changed = migrate_file(p)
    assert changed is True
    data = json.loads(p.read_text())
    assert data["webm_filepath"] == "webm/test.webm"


def test_migrate_file_rewrites_broken_thumbnail(tmp_path):
    p = _make_json(tmp_path, {
        "name": "Test Skin",
        "webm_filepath": "",
        "thumbnail_path": "/home/eyes/workspace/eyes/skin-scraper/application/thumbnails/test.jpg",
    })
    changed = migrate_file(p)
    assert changed is True
    data = json.loads(p.read_text())
    assert data["thumbnail_path"] == "application/thumbnails/test.jpg"


def test_migrate_file_does_not_touch_already_relative(tmp_path):
    p = _make_json(tmp_path, {
        "name": "Test Skin",
        "webm_filepath": "webm/test.webm",
        "thumbnail_path": "application/thumbnails/test.jpg",
    })
    changed = migrate_file(p)
    assert changed is False
    data = json.loads(p.read_text())
    assert data["webm_filepath"] == "webm/test.webm"


def test_migrate_file_does_not_corrupt_other_fields(tmp_path):
    original = {
        "name": "AK-47 | Test",
        "weapon": "AK-47",
        "rarity": "Covert",
        "tags": ["red", "dark"],
        "webm_filepath": "/home/eyes/workspace/eyes/skin-scraper/webm/test.webm",
        "thumbnail_path": "/home/eyes/workspace/eyes/skin-scraper/application/thumbnails/test.jpg",
    }
    p = _make_json(tmp_path, original)
    migrate_file(p)
    data = json.loads(p.read_text())
    assert data["name"] == original["name"]
    assert data["weapon"] == original["weapon"]
    assert data["rarity"] == original["rarity"]
    assert data["tags"] == original["tags"]


def test_migrate_all_returns_correct_counts(tmp_path):
    for i in range(3):
        (tmp_path / f"skin_{i}.json").write_text(json.dumps({
            "webm_filepath": "/home/eyes/workspace/eyes/skin-scraper/webm/skin.webm",
            "thumbnail_path": "/home/eyes/workspace/eyes/skin-scraper/application/thumbnails/skin.jpg",
        }))
    total, modified = migrate_all(tmp_path)
    assert total == 3
    assert modified == 3


def test_migrate_all_idempotent(tmp_path):
    (tmp_path / "skin.json").write_text(json.dumps({
        "webm_filepath": "/home/eyes/workspace/eyes/skin-scraper/webm/skin.webm",
        "thumbnail_path": "",
    }))
    migrate_all(tmp_path)
    _, modified_second = migrate_all(tmp_path)
    assert modified_second == 0
